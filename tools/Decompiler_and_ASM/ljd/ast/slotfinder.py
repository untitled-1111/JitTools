# See doc/SlotFinder.md for context

from typing import List, Optional, Dict, Set
import weakref
from dataclasses import dataclass, field

import ljd.ast.traverse as traverse
import ljd.ast.nodes as nodes
from ljd.ast.slotworks import SlotInfo, SlotReference


# Find and link up all the slots for a given function. This should be done before any warping
# is performed.
# If a FunctionDefinition is found inside the AST, process will be called a second time from _InputOutputBuilder
def process(ast: nodes.FunctionDefinition):
    _process(ast, _SlotIdentifier())


def _process(ast: nodes.FunctionDefinition, visitor: '_SlotIdentifier'):
    traverse.traverse(visitor, ast)
    _flow_function(ast.statements.contents)
    _finalise(ast.statements.contents, visitor)


def _flow_function(blocks: List[nodes.Block]):
    # Setup the flow_ins, to trace back how we could get to a given point
    for blk in blocks:
        for tgt in _BlockMeta.get(blk).flow_out:
            _BlockMeta.get(tgt).flow_in.append(blk)

    # See the SlotFinder doc for an explanation of all this. TL;DR we link up
    # each input with the outputs of all blocks leading to it, and if any of
    # those blocks don't output it we propagate to the blocks leading to that
    # block, and so on.
    dirty: Set[nodes.Block] = set(blocks)
    while len(dirty) > 0:
        old_dirty = dirty
        dirty = set()
        for block in old_dirty:
            _flow_block(block, lambda b: dirty.add(b))


# Finalisation: Collect all the slots and assign them IDs
def _finalise(blocks: List[nodes.Block], visitor: '_SlotIdentifier'):
    # First build a set of all the SlotInfo instances, which should represent every slot in the function.

    # First build a set of all the SlotNets of the inputs and outputs
    # Also include the function arguments, in case they aren't used elsewhere
    slot_nets: Set[_SlotNet] = set(visitor.func_arguments.values())
    for blk in blocks:
        meta = _BlockMeta.get(blk)
        slot_nets |= set(meta.inputs.values())
        slot_nets |= set(meta.outputs.values())

    # Then convert it to the slot infos and add in the internals, which is our complete list
    slots: List[SlotInfo] = [n.get() for n in slot_nets]
    for blk in blocks:
        slots += _BlockMeta.get(blk).internals

    # Move the slot numbers to each Identifier, since that's the only thing that stays around
    # after cleanup, and also isn't broken by Identifiers being removed by Slotworks.
    for slot in slots:
        # Build a list of all the identifiers relating to this SlotInfo.
        idents = [r.identifier for r in slot.references]

        # And finally write the IDs out to the references
        for ref in idents:
            ref.id = slot.slot_id

    # Clean up
    for blk in blocks:
        delattr(blk, '_block_slot_meta')


# For a given function, link up it's inputs
def _flow_block(block: nodes.Block, mark_dirty):
    meta = _BlockMeta.get(block)
    for slot_num, slot in meta.inputs.items():
        # If this is some weird orphan block (see the weird_bytecode_expression
        # test), then skip it rather than crashing - it's something weird with
        # the AST, not something wrong with us.
        if len(meta.flow_in) == 0 and block.index != 0:
            continue

        # If an import runs out the top of a function, that's a big issue
        if len(meta.flow_in) == 0:
            continue

        for src in meta.flow_in:
            src_meta = _BlockMeta.get(src)
            if slot_num in src_meta.outputs:
                slot.merge(src_meta.outputs[slot_num])
            else:
                src_meta.outputs[slot_num] = slot
                src_meta.inputs[slot_num] = slot
                mark_dirty(src)


# (see the SlotInfo Wrappers section in the markdown file)
# SlotNet is a wrapper around a SlotInfo. It's required because blocks input and output slots that
# need to be linked together. If we used raw SlotInfo objects, it'd require some slightly messy code
# to go through and update all of them.
class _SlotNet:
    class _Ctx:
        # Store the slots as weak references, otherwise we'd have cyclic references that
        # could keep this all alive.
        refs: List
        slot: SlotInfo

        def __init__(self, slot: SlotInfo):
            self.slot = slot
            self.refs = []

        def add(self, net: '_SlotNet'):
            self.refs.append(weakref.ref(net))

        # noinspection PyProtectedMember
        def merge(self, other: '_SlotNet._Ctx'):
            self.slot.references += other.slot.references
            self.slot.assignments += other.slot.assignments
            self.refs += other.refs

    _ctx: _Ctx

    def __init__(self, slot):
        self._ctx = self._Ctx(slot)
        self._ctx.add(self)

    def get(self) -> SlotInfo:
        return self._ctx.slot

    def slot(self) -> int:
        return self.get().slot

    def merge(self, other: '_SlotNet', is_uv: bool = False):
        if not is_uv:
            assert other.slot() == self.slot()

        if other._ctx == self._ctx:
            return

        # Merge the contexts
        self._ctx.merge(other._ctx)

        # Migrate all the SlotNets to pointing to the same context
        for ref in other._ctx.refs:
            net: '_SlotNet' = ref()
            if not net:
                continue
            net._ctx = self._ctx
            if ref in self._ctx.refs:
                continue
            self._ctx.refs.append(ref)

        assert other._ctx == self._ctx

    def __eq__(self, o):
        return isinstance(o, _SlotNet) and o._ctx == self._ctx

    def __hash__(self):
        return hash(self._ctx)

    def __str__(self):
        return "Net[%d,%d]" % (self.get().slot, self.get().slot_id)


# A mapping between the VM slot numbers and their associated SlotInfo, wrapped by SlotNet
# Used quite a bit, hence the alias
_SlotDict = Dict[int, _SlotNet]


# Stores all the metadata about a single block, hence we don't use lots of fields on that
# block, and also conveniently get type inference for PyCharm's autocomplete.
class _BlockMeta:
    inputs: _SlotDict
    outputs: _SlotDict
    internals: List[SlotInfo]

    flow_in: List[nodes.Block]
    flow_out: List[nodes.Block]

    @staticmethod
    def get(block: nodes.Block) -> '_BlockMeta':
        # noinspection PyUnresolvedReferences,PyProtectedMember
        return block._block_slot_meta


# Since for both _SlotIdentifier and _SlotCollector we have to identify which
# slots are assignments (including those that don't look like it, such as the
# numeric for loop) this abstract superclass is where this should be put.
class _SlotMarkerBase(traverse.Visitor):
    def _slot_set(self, setter, slot: nodes.Identifier) -> SlotInfo:
        raise Exception("_slot_set not overridden!")

    def _write_and_pin(self, setter, node: nodes.Identifier):
        if node.type == nodes.Identifier.T_LOCAL:
            print('Nuh uh. Slot type still isn\'t supposed to be T_LOCAL. Why is it here then? Line: 197')

            return

        slot = self._slot_set(setter, node)
        slot.is_pinned = True

    # Note: for loops show up as warps before unwarping the AST, and as actual
    # elements afterwards. Handle both.
    def visit_numeric_loop_warp(self, node: nodes.NumericLoopWarp):
        self._write_and_pin(node, node.index)

    def visit_numeric_for(self, node: nodes.NumericFor):
        self._write_and_pin(node, node.variable)

    # Same thing with iterator warps
    def visit_iterator_for(self, node: nodes.IteratorFor):
        for var in node.identifiers.contents:
            self._write_and_pin(node, var)

    def visit_iterator_warp(self, node: nodes.IteratorWarp):
        for var in node.variables.contents:
            self._write_and_pin(node, var)


# A visitor that scans through a the root function of the AST (calling process again to handle
# any nested functions) which identifies:
# The input, output and internal slots for each block
# The warps between blocks
class _SlotIdentifier(_SlotMarkerBase):
    func_arguments: _SlotDict
    upvalues: _SlotDict

    _next_slot_id: int = 1000
    _path: List
    _func: nodes.FunctionDefinition = None

    _skip = None
    _block: Optional[nodes.Block] = None

    _current: _SlotDict
    _inputs: _SlotDict
    _internals: List[SlotInfo]

    # Used to track which VM slots we've already written to in this block. Something being in
    # current may mean it's already been written to, but it's also set when inputting something.
    # This distinction is important when adding something to the internals, since we have to be
    # careful not to put something in the inputs and the internals.
    _written: Set[int]

    def __init__(self):
        super().__init__()
        self._path = []
        self.func_arguments = dict()
        self.upvalues = dict()

    # Create a new SlotInfo (and an associated SlotNet) for the given VM slot number
    def _new_slot(self, vm_slot_id) -> (SlotInfo, _SlotNet):
        info = SlotInfo(self._next_slot_id)
        info.function = self._func
        info.slot = vm_slot_id
        self._next_slot_id += 1
        return info, _SlotNet(info)

    # Called when a slot is assigned to, and shuffles around the output table and internals list appropriately
    def _slot_set(self, setter, slot: nodes.Identifier) -> SlotInfo:
        assert isinstance(slot, nodes.Identifier)

        assert slot.type == nodes.Identifier.T_SLOT

        # If we've already written to this slot, the previous value can't escape to later blocks.
        # Note it down so we can number it later.
        if slot.slot in self._written:
            self._internals.append(self._current[slot.slot].get())

        info, net = self._new_slot(slot.slot)
        if setter is nodes.Assignment:
            info.assignment = setter
        info.assignments = [setter]
        self._current[slot.slot] = net
        self._written.add(slot.slot)

        return info

    # Called to mark that a given VM slot number has been read. Returns the SlotNet representing that VM slot.
    def _slot_get(self, slot: nodes.Identifier) -> _SlotNet:
        assert isinstance(slot, nodes.Identifier)

        num = slot.slot

        if slot.type == nodes.Identifier.T_UPVALUE:
            net = self.upvalues.get(num)
            if not net:
                _, net = self._new_slot(num)
                self.upvalues[num] = net
            return net

        assert slot.type == nodes.Identifier.T_SLOT

        if self._func.arguments.contains_id(slot):
            info, net = self._new_slot(slot.slot)
            self.func_arguments[num] = net
            return net

        net = self._current.get(num)
        if not net:
            info, net = self._new_slot(slot.slot)
            self._current[num] = net
            self._inputs[num] = net

        return net

    def visit_assignment(self, node):
        # When visiting an assignment, we have to do three things in order:
        # 1. visit the expressions
        # 2. update the slots to reflect the results of the assignment
        # 3. visit the destinations to register references to the new SlotInfo objects from step 2

        # Thus we have to do this manually to get it done before we update the slots
        self._visit(node.expressions)

        # Prevent the expressions from being re-visited
        self._skip = node.expressions

        for slot in node.destinations.contents:
            # If we're assigning to a global or table element, MULTRES or something like that, skip
            # that since it doesn't affect the slots
            if not isinstance(slot, nodes.Identifier):
                continue

            if slot.type == nodes.Identifier.T_UPVALUE:
                continue

            if slot.type == nodes.Identifier.T_LOCAL:
                print('Slot type isn\'t supposed to be T_LOCAL when it gets here? Line: 331')
                continue

            self._slot_set(node, slot)

    def leave_assignment(self, node):
        self._skip = None

    def visit_identifier(self, node: nodes.Identifier):
        # TODO handle locals, upvalues and builtins properly
        if node.type != nodes.Identifier.T_SLOT and node.type != nodes.Identifier.T_UPVALUE:
            return

        assert node.slot != -1

        info = self._slot_get(node).get()

        ref = SlotReference()
        ref.identifier = node
        ref.path = self._path[:]
        info.references.append(ref)

    def visit_block(self, node):
        self._current = dict()
        self._inputs = dict()
        self._internals = []
        self._written = set()
        self._block = node

        # The first block inherits all the function arguments
        if self._block.index == 0:
            self._current.update(self.func_arguments)

    def leave_block(self, node):
        meta = _BlockMeta()
        meta.inputs = self._inputs
        meta.outputs = self._current
        meta.internals = self._internals

        # Take note of the blocks that could come after this block. Used to track back the sources of slots.
        # Derived from ljd.ast.unwarper._find_warps_to
        warp = node.warp
        if isinstance(warp, nodes.ConditionalWarp):
            refs = [warp.true_target, warp.false_target]
        elif isinstance(warp, nodes.UnconditionalWarp):
            # peace at last
            refs = [hasattr(warp, 'fixed_target') and warp.fixed_target or warp.target]
        elif isinstance(warp, nodes.EndWarp):
            refs = []
        else:
            refs = [warp.way_out, warp.body]

        # Make sure there aren't any Nones hiding in there
        for ref in refs:
            assert ref

        meta.flow_in = []
        meta.flow_out = refs

        node._block_slot_meta = meta
        self._block = None

    def _visit_node(self, handler, node):
        self._path.append(node)
        traverse.Visitor._visit_node(self, handler, node)

    def _leave_node(self, handler, node):
        self._path.pop()
        traverse.Visitor._leave_node(self, handler, node)

    def _visit(self, node):
        # Skip is set while we visit the contents of a assignment. Since we're not interested in
        # those references (they're added manually to get the order correct), we skip them.
        if self._skip == node:
            return

        # In order to avoid storing a state stack between the different functions, recursively call
        # into process to repeat the whole thing for any nested functions.
        if isinstance(node, nodes.FunctionDefinition):
            if self._func is not None:
                visitor = _SlotIdentifier()
                # Swap the slot IDs around while visiting the function so they're not repeated in
                # different functions. Thus every local variable in the entire AST should have a
                # different slot ID. This means one can safely find/replace over a file, and will
                # also simplify the implementation of upvalues.
                visitor._next_slot_id = self._next_slot_id
                _process(node, visitor)
                self._next_slot_id = visitor._next_slot_id
                self._link_upvalues(visitor.upvalues, node.upvalues)
                return
            else:
                self._func = node

        traverse.Visitor._visit(self, node)

    def _link_upvalues(self, nets: _SlotDict, ids: List[int]):
        for num, net in nets.items():
            # Identify what the upvalue is attached to - see fs_fixup_uv2 in LuaJIT
            # Mask off 0x4000 which is the immutable flag
            try:
                uv_id = ids[num] & ~0x4000
            except IndexError:
                print('Warning: an error occurred while linking upvalues.')

                continue

            parent_id = uv_id & ~0x8000

            # Use the standard _slot_get mechanism rather than just pulling the
            # slot out of _current, in case it hasn't been used in this block and
            # should be inherited from another.
            fake_slot = nodes.Identifier()
            fake_slot.slot = parent_id

            if parent_id != uv_id:
                fake_slot.type = nodes.Identifier.T_SLOT
            else:
                # Upvalue bound to upvalue
                fake_slot.type = nodes.Identifier.T_UPVALUE

            local_net = self._slot_get(fake_slot)
            local_net.merge(net, is_uv=True)


# Slots finder
# This isn't used by any of the above code, but it's put here since it's fairly heavily related - it
# reads back the IDs assigned from the above system to form SlotInfo objects.

def collect_slots(ast: nodes.FunctionDefinition, uv_refs: List[int] = None) -> List[SlotInfo]:
    # Note that we can only safely work on full function definitions - while the old
    # slot elimination system put up with incorrect eliminations from time to time, the
    # whole point of slotfinder is to prevent that.
    assert isinstance(ast, nodes.FunctionDefinition)

    visitor = _SlotCollector()

    if isinstance(uv_refs, list):
        setattr(visitor, 'uv_refs', uv_refs)

    traverse.traverse(visitor, ast)
    return list(visitor.slots.values()) + visitor.nested_func_slots


class _SlotCollector(_SlotMarkerBase):
    # The types of nodes that have side-effects and we can't eliminate across
    IMPURE_NODES = (nodes.Block, nodes.FunctionDefinition, nodes.FunctionCall, nodes.TableElement,
                    nodes.BinaryOperator, nodes.UnaryOperator, nodes.MULTRES)

    @dataclass()
    class _PureInfo:
        passed: List[nodes.Assignment] = field(default_factory=list)

    nested_func_slots: List[SlotInfo]
    slots: Dict[int, SlotInfo]
    _path: List
    _func: nodes.FunctionDefinition = None
    _next_slot_id: int = 0

    # Use this to find out what OAs (Observable Actions) have occurred between the assignment of an identifier and
    #  it's first use. This is used to block inlining if that would result in observably different output.
    # See doc/SideEffectTracing
    # The basic idea here is that each identifier has a bit of information associated with it (_PureInfo). This
    #  contains a list of all the assignments containing an OA that have 'passed' (occured between the assignment
    #  and first use, as per above).
    # Whenever we enter an assignment we set _current_assignment (CA) and clear _current_assignment_observable (CAO).
    # When we visit an OA, if CA is not set then clear all the pure identifiers, since we don't support inlining past
    #  anything other than assignments. If CA is set, then:
    # * If CAO is already skip, continue as before. Otherwise, set CAO and add CA to the passed list ofr each PureInfo.
    # The reason we do it like this rather than just adding the OAs to PureInfo whenever we visit one is that one
    #  assignment can contain multiple OAs, and it should be treated the same as containing one.
    # Also we can't add the PureInfo to the passed list when we exit the assignment - the reference might be used
    #  after passing the OA but before exiting the assignment. For example, in this case:
    #
    # local my_local = gbl
    # local res = some_local_func(f(), my_local)
    #
    # Then my_local should clearly list f() as an OA, however we visit that reference before leaving the assignment.
    # The above case will never occur in the directly disassembled bytecode, but since slot elimination may be run
    #  many times we can end up with that, and it's tested in the side_effect_reordering test.
    _pure_identifiers: Dict[nodes.Identifier, _PureInfo]  # For each identifier, keeps track of what OAs it has passed
    _current_assignment: Optional[nodes.Assignment] = None
    _current_assignment_observable: bool = False

    def __init__(self):
        super().__init__()
        self.slots = dict()
        self.nested_func_slots = []
        self._path = []
        self._pure_identifiers = dict()

    def _get_info(self, node: nodes.Identifier) -> SlotInfo:
        assert node.slot != -1
        assert node.id != -1

        info = self.slots.get(node.id)
        if not info:
            info = SlotInfo(self._next_slot_id)
            info.function = self._func
            info.slot = node.slot
            self._next_slot_id += 1
            self.slots[node.id] = info

        return info

    def _slot_set(self, setter, slot: nodes.Identifier) -> SlotInfo:
        info = self._get_info(slot)
        info.assignments.append(info)
        return info

    def visit_identifier(self, node: nodes.Identifier):
        # TODO handle locals, upvalues and builtins properly
        if node.type == nodes.Identifier.T_UPVALUE and hasattr(self, 'uv_refs'):
            if node.id != -1:
                self.uv_refs.append(node.id)

            return

        if node.type != nodes.Identifier.T_SLOT:
            return

        info = self._get_info(node)

        # If it's an argument, pin it so it can't be eliminated
        if self._func and self._func.arguments.contains_id(node):
            info.is_pinned = True

        assn = self._path[-3]
        if isinstance(assn, nodes.Assignment) and isinstance(self._path[-2], nodes.VariablesList):
            # Use the first assignment we find as the 'main' assignment
            # However, if there's already a non-Assignment write, leave that blank
            if len(info.assignments) == 0:
                info.assignment = assn

            # We're being directly set by an assignment
            info.assignments.append(assn)

        actions = None
        if node in self._pure_identifiers:
            actions = self._pure_identifiers[node].passed
            del self._pure_identifiers[node]

        ref = SlotReference()
        ref.identifier = node
        ref.path = self._path[:]
        ref.observable_actions = actions
        info.references.append(ref)

    def visit_assignment(self, node: nodes.Assignment):
        assert self._current_assignment is None
        self._current_assignment = node
        self._current_assignment_observable = False

    def leave_assignment(self, node: nodes.Assignment):
        # Add the PureInfo for each destination slot
        # Note we have to do this now rather than when visiting, otherwise this
        #  assignment would be marked as an OA for it's destinations.
        for dst in node.destinations.contents:
            if isinstance(dst, nodes.Identifier) and dst.type == nodes.Identifier.T_SLOT:
                self._pure_identifiers[dst] = self._PureInfo()

        self._current_assignment = None

    def _visit_node(self, handler, node):
        self._path.append(node)
        traverse.Visitor._visit_node(self, handler, node)

    def _leave_node(self, handler, node):
        if isinstance(node, self.IMPURE_NODES):
            if self._current_assignment is None:
                self._pure_identifiers.clear()
            elif not self._current_assignment_observable:
                self._current_assignment_observable = True
                for info in self._pure_identifiers.values():
                    info.passed.append(self._current_assignment)

        self._path.pop()
        traverse.Visitor._leave_node(self, handler, node)

    def _visit(self, node):
        if not isinstance(node, nodes.FunctionDefinition):
            return super()._visit(node)

        if not self._func:
            self._func = node
            return super()._visit(node)

        uv_refs = []
        self.nested_func_slots += collect_slots(node, uv_refs)

        # For some reason, when a variable is referenced as an upvalue, it doesn't
        # count as a reference, so the temporary slot eliminator might merge it
        # into another variable as if it didn't have any references at all.
        # I'm not sure if this is a dirty hack or a valid fix, it needs some testing.
        for id in uv_refs:
            info = self.slots.get(id)

            if info:
                setattr(info, 'ref_as_uv', True)


# Slot splitter
#
# Imagine you have the following code:
#
#  slot0 = gbl_a
#  if not slot0 then
#    slot0 = gbl_b
#  end
#  print(slot0)
#
# And then, thanks to unwarper's expression unwarping, that's transformed down to:
#
#  slot0 = gbl_a
#  slot0 = slot or gbl_b
#  print(slot0)
#
# At this point, our method of searching for slot references has been too strong. The
# slot now refers to two different values - a temporary for gbl_a and the result of
# the 'or' expression. Thus we provide a function where unwarper can tell us they've
# made a change, and we should check if the SlotInfo can be split in two.
#
# This takes an assignment and a slot, and checks if all subsequent reads from that
# slot occur within the assignment's parent. If so then we clearly know who can only
# observe the old value and who can only observe the new one, and thus we can safely
# split the slot.

def check_slot_split(func: nodes.FunctionDefinition, assn: nodes.Assignment, ident: nodes.Identifier):
    assert isinstance(func, nodes.FunctionDefinition)
    assert isinstance(assn, nodes.Assignment)
    assert isinstance(ident, nodes.Identifier)

    # TODO this will probably have a significant performance impact
    # One possibility to speed this up would be storing in each SlotInfo the highest
    # node that contains all the references, so we don't have to scan anything that
    # certainly won't contain references to it (unless it was shifted around, so
    # we'd need some way to invalidate it after that)
    slots = collect_slots(func)

    # Find the SlotInfo in question
    slot: Optional[SlotInfo] = None
    max_slot_id = 0
    max_ref_id = 0
    for s in slots:
        ref_id = s.references[0].identifier.id
        max_slot_id = max(max_slot_id, s.slot_id)
        max_ref_id = max(max_ref_id, ref_id)
        if ref_id == ident.id:
            slot = s
            break

    if slot is None:
        return

    # Make sure we're not trying to eliminate the first assignment
    # While it may seem weird (and usually shouldn't happen), it can
    # happen: see the weird_bytecode_expression test for an example of this.
    if assn == slot.assignments[0]:
        return

    # Find the path to the relevant identifier
    reference: Optional[SlotReference] = None
    for ref in slot.references:
        if id(ref.identifier) == id(ident):
            reference = ref
            break

    assert reference
    reference_idx = slot.references.index(reference)

    # Make sure the caller isn't lying
    assert assn == reference.path[-3]

    # Check if there are any references on a scope outside that of the assignment.
    # We only check for references to the old value, before assignment. This is because
    # when a slot is eliminated it should be folded into an expression, so we
    # shouldn't have anything complex above us.
    scope = reference.path[-4]
    for idx, ref in enumerate(slot.references[:reference_idx]):
        if scope not in ref.path:
            return

    # Split the slot up
    # Give it a new sequential ID - I'm not sure if that matters at this point?
    new = SlotInfo(max_slot_id + 1)
    ref_id = max_ref_id + 1

    new.references = slot.references[reference_idx:]
    del slot.references[reference_idx:]

    new.assignments = slot.assignments[slot.assignments.index(assn):]
    del slot.assignments[slot.assignments.index(assn):]

    for ref in new.references:
        ref.identifier.id = ref_id
