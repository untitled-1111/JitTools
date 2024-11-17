import copy
import collections
from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass

import ljd.ast.nodes as nodes
import bcdiff.utils
from bcdiff.types import BlockInfo
from ljd.ast.slotworks import SlotReference


class CompareState:
    # Maps slot IDs from those in the 'A' function to the corresponding IDs of those in the 'B' function
    slot_maps: Dict[int, int]

    # Reverse of the above, 'B' to 'A' slot IDs
    rev_slot_maps: Dict[int, int]

    def __init__(self):
        self.slot_maps = dict()
        self.rev_slot_maps = dict()


@dataclass()
class AssignmentInfo:
    is_pure: bool
    slot_ids: Set[int]


def compare_func_meta(a: nodes.FunctionDefinition, b: nodes.FunctionDefinition, state: CompareState):
    # Compare the functions, though note the blocks are excluded
    # This maps the slot IDs of the arguments
    _state_compare(a, b, state, exclude={"_instructions_count"})


def compare_blocks(a: nodes.Block, a_info: BlockInfo, b: nodes.Block, b_info: BlockInfo, state: CompareState):
    actions_a = _build_actions(a, a_info, state)
    actions_b = _build_actions(b, b_info, state)

    assert len(actions_a) == len(actions_b)

    # ljd.ast.printast.dump("block-a", actions_a)
    # ljd.ast.printast.dump("block-b", actions_b)

    for a, b in zip(actions_a, actions_b):
        a.check_eq(b)


def _build_actions(block: nodes.Block, info: BlockInfo, state: CompareState):
    actions: List[Action] = []

    assignments: List[nodes.Assignment] = list()

    def flush_assignments(blocked_slots: Optional[Set[int]]):
        if len(assignments) == 0:
            return

        # Rather than writing out all our assignments to a single action, move the
        #  assignments as late in the file as we can without making any observable
        #  changes. There are cases where stuff can be moved like this that would
        #  otherwise make functionally identical programs differ.
        # This is controlled by the blocked_slot arguments. If we've been able to
        #  keep track of every slot access between when these assignments were made
        #  up until now, then we don't have to flush pure assignments (such as
        #  setting a slot to a constant or primitive) around so long as their slot
        #  hasn't been referenced anywhere.

        action = AssignmentsAction(state)

        # Make a temporary copy of the assignments, since we'll be removing from it
        for assn in list(assignments):
            dest_id = assn.destinations.contents[0].id
            assert dest_id != -1

            # If this is a pure slot that hasn't been used anywhere, no need to write it yet.
            if blocked_slots is not None and dest_id not in blocked_slots:
                continue

            assignments.remove(assn)

            # It should be impossible to make two writes to the same slot, since the first
            # would be unobservable elsewhere and thus numbered differently
            assert dest_id not in action.assigned_slots

            action.assignments.append(assn)
            action.assigned_slots[dest_id] = assn

        if len(action.assignments) == 0:
            return

        action.validate()
        actions.append(action)

    def drop_node(node):
        block.contents.remove(node)

        # If drop_node is called before we're added to the slot list, stop here
        if node in assignments:
            assignments.remove(node)

    for node in list(block.contents):
        assn_info = _get_assignment_info(node)
        if assn_info is not None and assn_info.is_pure:
            dst = node.destinations.contents[0]
            assert isinstance(dst, nodes.Identifier)
            assert dst.type == nodes.Identifier.T_SLOT

            # Recalculate the slot info if it's invalid
            info.validate_slot(dst.id)

            # Skip assignments that don't do anything
            dst_refs = info.slots_by_id[dst.id].references
            if len(dst_refs) < 1:
                drop_node(node)
                continue

            # If this is a constant, we can inline it anywhere we want, including outside
            # this action, such as these two sets of bytecode:
            #   slot0 = 1     |   slot0 = f
            #   slot1 = f     |   slot1 = 1
            #   slot1(slot0)  |   slot0(slot1)
            # This won't completely solve the problem (if the above had been loading from
            # a slot rather than a constant we still would have failed), but it's an improvement.
            curr_src = node.expressions.contents[0]
            if isinstance(curr_src, nodes.Constant) and len(dst_refs) == 2:
                _replace_reference(dst_refs[1], curr_src)
                drop_node(node)
                continue

            assignments.append(node)

            # Eliminate any temporary slots
            # This should exclude upvalues?
            if not isinstance(curr_src, nodes.Identifier):
                continue

            # Update the slot information if needed
            # WARNING: do not use dst_refs past this point, since it may be invalid!
            info.validate_slot(curr_src.id)

            # TODO check for modifications inside this assignment block, eg:
            # s1_1001 = s0_1000
            # s1_1000 = nil
            # s3_1003 = s1_1001
            # We can probably inline most of these safely, but be careful!

            slot = info.slots_by_id[curr_src.id]
            if len(slot.references) > 2:
                continue

            # Check if this slot has been previously set in the same block, and we should be able to inline it
            other = slot.references[0]
            assert node not in other.path
            if block not in other.path:
                continue

            # If it hasn't been set in this assignment action, swap it and remove this assignment. Otherwise
            # we have to fix up the action first (and note that system removes the previous assignment).
            prev_list = [a for a in assignments if a.destinations.contents[0].id == curr_src.id]
            if len(prev_list) == 0:
                # Swap over the identifier
                _replace_reference(other, dst)

                # Remove this node from the assignments actions
                drop_node(node)

                # Mark both the old source and destination slots as dirty, so we'll recalculate the slot info
                # before using them
                info.mark_dirty(curr_src.id)
                info.mark_dirty(dst.id)
                continue

            # If this slot has been reassigned within the block, it should be on it's own isolated ID
            # TODO slots used as upvalues
            assert len(slot.references) == 2

            assert len(prev_list) == 1
            prev = prev_list[0]
            # print("Alias %s->%s" % (prev, node))

            drop_node(prev)
            node.expressions.contents[0] = prev.expressions.contents[0]

            continue

        action = MiscAction(state, node)

        if assn_info is not None:
            action.blocked_slots = assn_info.slot_ids

        flush_assignments(action.blocked_slots)
        actions.append(action)

    flush_assignments(None)
    actions.append(MiscAction(state, block.warp))

    return actions


def _replace_reference(ref: SlotReference, replacement: Any):
    holder = ref.path[-2]
    # There's probably quite a few other places, make them show up here
    assert isinstance(holder, (nodes.ExpressionsList, nodes.VariablesList))

    holder.contents[holder.contents.index(ref.identifier)] = replacement


def _get_assignment_info(node) -> Optional[AssignmentInfo]:
    if not isinstance(node, nodes.Assignment):
        return None
    src = node.expressions.contents
    dest = node.destinations.contents
    if len(src) != 1 or len(dest) != 1:
        return None

    slots = set()
    slots = _get_pure_slot(src[0], slots)
    slots = _get_pure_slot(dest[0], slots)

    pure = _is_expr_pure(src[0]) and _is_expr_pure(dest[0])
    return AssignmentInfo(pure, slots)


def _is_expr_pure(expr):
    if isinstance(expr, nodes.Identifier):
        return expr.type == nodes.Identifier.T_SLOT
    elif isinstance(expr, nodes.Constant):
        return True
    elif isinstance(expr, nodes.Primitive):
        return True
    elif isinstance(expr, nodes.UnaryOperator) or isinstance(expr, nodes.BinaryOperator):
        # Since the user can set stuff on the metatable, reordering these operations may have side-effects
        return False
    else:
        return False


def _get_pure_slot(expr, base: Optional[Set[int]]) -> Optional[Set[int]]:
    if base is None:
        return None

    # Note this does NOT imply that table elements are not observable - just that they only
    # read from slots referenced in the table and index, so we can move pure assignments past
    # this one safely.
    if isinstance(expr, nodes.TableElement):
        return _get_pure_slot(expr.table, _get_pure_slot(expr.key, base))

    if isinstance(expr, nodes.Constant):
        return base

    if not isinstance(expr, nodes.Identifier):
        return None

    if expr.type == nodes.Identifier.T_BUILTIN:
        assert expr.name == "_env"
        return base

    assert expr.type == nodes.Identifier.T_SLOT
    assert expr.id != -1
    base.add(expr.id)
    return base


def _state_compare(node_a, node_b, state: CompareState, exclude: Optional[Set] = None):
    def _check_identifier(a: nodes.Identifier, b: nodes.Identifier) -> Optional[bool]:
        if a.type != nodes.Identifier.T_SLOT or b.type != nodes.Identifier.T_SLOT:
            return None

        assert a.id != -1
        assert b.id != -1

        if a.id in state.slot_maps:
            assert state.slot_maps[a.id] == b.id
            return True

        assert b.id not in state.rev_slot_maps

        # print("Mapping slot %d to %d" % (a.id, b.id))
        state.slot_maps[a.id] = b.id
        state.rev_slot_maps[b.id] = a.id

        return True

    bcdiff.utils.recursive_eq(node_a, node_b, exclude=exclude, type_checkers={
        nodes.Identifier: _check_identifier,

        # We visit the block contents via actions, don't
        # go and visit them via warps or anything
        nodes.Block: lambda x, y: True,
    })


class Action:
    def __init__(self, state: CompareState):
        self._state = state

    def check_eq(self, other) -> bool:
        raise Exception("Abstract method")

    def _node_compare(self, a, b):
        _state_compare(a, b, self._state)


class AssignmentsAction(Action):
    assignments: List[nodes.Assignment]
    assigned_slots: Dict[int, nodes.Assignment]

    def __init__(self, state: CompareState):
        super().__init__(state)
        self.assignments = []
        self.assigned_slots = dict()

    def check_eq(self, other) -> bool:
        assert isinstance(other, AssignmentsAction)
        assert len(self.assignments) == len(other.assignments)

        # Since the slots don't reference each other and can be rearranged without
        # altering the program's behaviour, go through and compare them one-by-one so
        # them getting rearranged doesn't prevent files from matching.
        #
        # There is an important question here: which assignment do we compare each to?
        # If we compare the wrong assignments, we'll fail matching files. Thus we should
        # go over each of the source slots and constants, and for each one compare all
        # the assignments loading from that. For those where the mappings between the
        # destination slot IDs is known compare them first, for the others it doesn't
        # matter what order we compare them in since they'll be mapped while comparing.

        # Find a list of all the assignments coming from a given source, for the A and B actions
        assn_list = List[nodes.Assignment]
        by_src: Dict[Any, (assn_list, assn_list)] = collections.defaultdict(lambda: ([], []))

        # Get a hashable value of a given source. This is the SlotFinder ID for identifiers, and
        # the type/value pair as a tuple for constants.
        # noinspection PyShadowingNames
        def get_hashable_src(assn: nodes.Assignment):
            src = assn.expressions.contents[0]
            if isinstance(src, nodes.Identifier):
                return src.id
            elif isinstance(src, nodes.Primitive):
                return nodes.Primitive, src.type
            else:
                assert isinstance(src, nodes.Constant)
                return src.type, src.value

        for assn in self.assignments:
            src = get_hashable_src(assn)
            by_src[src][0].append(assn)

        for assn in other.assignments:
            # Map the ID from B to A - we should have compared the assignment to this slot so far.
            # Only convert it if it's an int (representing a slot number), not a constant
            b_src = get_hashable_src(assn)
            src = self._state.rev_slot_maps[b_src] if type(b_src) == int else b_src
            by_src[src][1].append(assn)

        # A safety net to make sure we have compared everything
        compared = set()

        for assignments in by_src.values():
            assert len(assignments[0]) == len(assignments[1])

            # Sort B's assignments out by which slot they assign to so we can grab the right one when comparing
            # Also store the list where the destination mapping isn't known
            b_by_dest: Dict[int, nodes.Assignment] = dict()
            assorted_others: List[nodes.Assignment] = list()

            for assn in assignments[1]:
                a_id = self._state.rev_slot_maps.get(assn.destinations.contents[0].id, None)
                if a_id is None:
                    assorted_others.append(assn)
                else:
                    b_by_dest[a_id] = assn

            for assn in assignments[0]:
                dest = assn.destinations.contents[0].id

                if dest in b_by_dest:
                    peer = b_by_dest[dest]
                else:
                    # TODO fix slot comparison ordering
                    # If a bunch of never-before-seen slots are set, compare them in the order they appear.
                    # (that is, compare A[0] = B[0], A[1] = B[1] etc rather than popping them off as we did before).
                    # Ideally this shouldn't matter and we should be able to group them correctly from the inputs
                    # and outputs as used elsewhere, but we're not there yet.
                    # This is particularly important since we move all assignments as late as possible, as we're
                    # more likely to run into issues with this.
                    peer = assorted_others[0]
                    del assorted_others[0]

                self._node_compare(assn, peer)

                compared.add(assn)
                compared.add(peer)

        # Make sure we did a comparison on every assignment
        assert compared.issuperset(set(self.assignments))
        assert compared.issuperset(set(other.assignments))

        return True

    def validate(self):
        # Check each assignment has a slot - we'll check they match up below
        assert len(self.assignments) == len(self.assigned_slots)

        for assn in self.assignments:
            # Make sure the destination is a single slot identifier
            assert len(assn.destinations.contents) == 1
            dst = assn.destinations.contents[0]
            assert isinstance(dst, nodes.Identifier)
            assert dst.type == nodes.Identifier.T_SLOT

            # Make sure the assigned slots dict matches up
            assert self.assigned_slots[dst.id] == assn

            # Make sure the source is a single value
            assert len(assn.expressions.contents) == 1
            src = assn.expressions.contents[0]

            # Constants are fine and don't need any further checking for
            # connections with previous assignments like slots do.
            if isinstance(src, nodes.Constant) or isinstance(src, nodes.Primitive):
                continue

            assert isinstance(src, nodes.Identifier)
            assert src.type == nodes.Identifier.T_SLOT

            # Make sure it's not reading a previously assigned slot
            # It's fine to read the same slot number, but this makes sure
            # the slot finder has properly split it up or it has been
            # inlined while the action was built.
            # This invariant is useful since it means the assignments can
            # be rearranged without affecting the behaviour of the program, which
            # gives us more lenience for matching programs when slots have
            # been introduced or eliminated.
            # TODO handle slots used by upvalues
            assert src.id not in self.assigned_slots


class MiscAction(Action):
    _state: CompareState = None

    blocked_slots: Optional[Set[int]] = None
    """The slots that this action uses and thus these slots cannot move past it. None means no movement is allowed"""

    def __init__(self, state: CompareState, node):
        super().__init__(state)
        self.node = node

    def check_eq(self, other) -> bool:
        assert isinstance(other, MiscAction)
        self._node_compare(self.node, other.node)
        return True
