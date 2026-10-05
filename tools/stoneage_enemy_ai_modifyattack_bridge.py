"""Exact positive recovered25 Modifyattack admission; no historical COM1."""
from dataclasses import dataclass
import hashlib

from tools.stoneage_modifyattack_reference_model import (
    CALLBACK_NAME, COMMAND_NAME, ModifyAttackOption,
)
from tools.stoneage_recovered25_modifyattack_probe import (
    EXPECTED_CALLBACK_IDS, EXPECTED_EXACT_ROWS,
)

EXPECTED_POSITIVE_TEMPLATE_SLOTS = {
    18: (101543, 3, 546),
    19: (101533, 4, 545),
    20: (101532, 3, 544),
}


@dataclass(frozen=True)
class EnemyAiModifyAttackSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    template_tempno: int
    template_graphic: int
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self):
        if not isinstance(self.participant_id, str) or not self.participant_id:
            raise ValueError("Modifyattack participant id required")
        for key in ('skill_slot', 'skill_id', 'source_target_slot', 'template_tempno', 'template_graphic'):
            if type(getattr(self, key)) is not int:
                raise ValueError("Modifyattack identity fields require integers")
        if self.template_tempno not in EXPECTED_POSITIVE_TEMPLATE_SLOTS:
            raise ValueError("Modifyattack outside exact positive templates")
        graphic, slot, skill = EXPECTED_POSITIVE_TEMPLATE_SLOTS[self.template_tempno]
        if (self.template_graphic, self.skill_slot, self.skill_id) != (graphic, slot, skill):
            raise ValueError("Modifyattack exact template/graphic/slot/ID drift")
        if not 0 <= self.source_target_slot < 10:
            raise ValueError("Modifyattack target must be player-side 0..9")
        if self.callback != CALLBACK_NAME or self.semantic_command_name != COMMAND_NAME:
            raise ValueError("Modifyattack callback/semantic command drift")

    @property
    def option(self):
        return ModifyAttackOption(self.skill_id - 544, 20)


def validate_recovered25_modifyattack_population(runtime):
    rows = tuple(sorted((entry for entry in runtime.skills.values()
                         if entry.function_name == CALLBACK_NAME), key=lambda entry: entry.skill_id))
    if tuple(entry.skill_id for entry in rows) != EXPECTED_CALLBACK_IDS:
        raise ValueError("Modifyattack complete population must be 544..547")
    for entry, expected in zip(rows, EXPECTED_EXACT_ROWS):
        raw = bytes(entry.option_bytes)
        actual = (entry.skill_id, entry.field, entry.target, entry.cost,
                  entry.illegal, len(raw), hashlib.sha256(raw).hexdigest(), b'\0' in raw)
        pinned = (*expected[:5], *expected[6:9])
        if actual != pinned:
            raise ValueError("Modifyattack full metadata/OPTION identity drift")


def resolve_enemy_ai_modifyattack_submission(spawned, *, skill_slot, target_slot, petskill_runtime):
    validate_recovered25_modifyattack_population(petskill_runtime)
    if type(skill_slot) is not int or type(target_slot) is not int:
        raise ValueError("Modifyattack slot and target require integers")
    if spawned.participant.side != 'enemy' or spawned.participant.kind != 'enemy':
        raise ValueError("Modifyattack bridge admits recovered enemy actors only")
    tempno = int(spawned.template.tempno)
    if tempno not in EXPECTED_POSITIVE_TEMPLATE_SLOTS:
        raise ValueError("Modifyattack actor outside exact positive templates")
    graphic, slot, skill = EXPECTED_POSITIVE_TEMPLATE_SLOTS[tempno]
    slots = tuple(int(value) for value in spawned.template.skill_slot_ids)
    if (len(slots) != 7 or int(skill_slot) != slot or slots[slot] != skill
            or int(spawned.template.graphic_id) != graphic):
        raise ValueError("Modifyattack selected authoritative template/slot drift")
    return EnemyAiModifyAttackSubmission(
        str(spawned.participant.participant_id), slot, skill, CALLBACK_NAME,
        int(target_slot), tempno, graphic,
    )
