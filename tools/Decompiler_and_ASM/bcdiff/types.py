from dataclasses import dataclass, field
from typing import List, Dict, Set

# Typing only!
from ljd.ast.slotworks import SlotInfo
import ljd.ast.nodes as nodes
import ljd.ast.slotfinder as slotfinder


@dataclass()
class BlockInfo:
    """ Stores extra information that may be relevant to a given block, such as the slot information """

    function: nodes.FunctionDefinition

    slots: List[SlotInfo] = field(init=False)

    slots_by_id: Dict[int, SlotInfo] = field(init=False)
    """ Slots indexed by Identifier.id """

    dirty_slots: Set[int] = field(default_factory=set)
    """ The slot IDs of all the 'dirty' slots. The slot info should be rebuilt before these slots are used again """

    def __post_init__(self):
        self._update_slots()

    def _update_slots(self):
        self.dirty_slots.clear()
        self.slots = slotfinder.collect_slots(self.function)

        self.slots_by_id = dict()

        for si in self.slots:
            sid = si.references[0].identifier.id
            assert sid not in self.slots
            self.slots_by_id[sid] = si

    def mark_dirty(self, slot_id):
        self.dirty_slots.add(slot_id)

    def validate_slot(self, slot_id):
        if slot_id not in self.dirty_slots:
            return

        self._update_slots()
