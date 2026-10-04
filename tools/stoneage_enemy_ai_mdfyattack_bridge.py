"""Typed recovered25 Mdfyattack admission; historical COM1 stays unassigned."""
from dataclasses import dataclass

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_mdfyattack_model import CALLBACK_NAME, COMMAND_NAME, MdfyAttackOption, ELEMENT_CODES
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime

RECOVERED25_MDFYATTACK_IDS = (548, 549, 550, 551)


@dataclass(frozen=True)
class EnemyAiMdfyAttackSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self):
        if not str(self.participant_id) or not 0 <= int(self.skill_slot) < 7:
            raise ValueError('Mdfyattack participant/skill slot outside admitted domain')
        if int(self.skill_id) not in RECOVERED25_MDFYATTACK_IDS or self.callback != CALLBACK_NAME:
            raise ValueError('Mdfyattack recovered ID/callback drift')
        if not 0 <= int(self.source_target_slot) < 10:
            raise ValueError('Mdfyattack target outside recovered enemy/player-side domain')
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError('Mdfyattack command symbol drift')
        for key in ('skill_slot', 'skill_id', 'source_target_slot'):
            object.__setattr__(self, key, int(getattr(self, key)))
        object.__setattr__(self, 'participant_id', str(self.participant_id))

    @property
    def option(self):
        return MdfyAttackOption(self.skill_id - 548, 100)


def resolve_enemy_ai_mdfyattack_submission(spawned: SpawnedEnemy, *, skill_slot: int,
                                          target_slot: int, petskill_runtime: Recovered25PetSkillRuntime):
    rows = tuple(sorted((e for e in petskill_runtime.skills.values() if e.function_name == CALLBACK_NAME),
                        key=lambda e: e.skill_id))
    if tuple(e.skill_id for e in rows) != RECOVERED25_MDFYATTACK_IDS:
        raise ValueError('Mdfyattack requires the verified exact four-row callback population')
    for e in rows:
        if (e.field, e.target, e.cost, e.illegal, bytes(e.option_bytes)) != (
                1, 6, 2, 2000, ELEMENT_CODES[e.skill_id - 548] + b'|100'):
            raise ValueError('Mdfyattack verified full metadata/OPTION drift')
    slots = tuple(int(i) for i in spawned.template.skill_slot_ids)
    if len(slots) != 7 or not 0 <= int(skill_slot) < 7 or slots[int(skill_slot)] not in RECOVERED25_MDFYATTACK_IDS:
        raise ValueError('Mdfyattack requires authoritative selected seven-slot identity')
    if spawned.participant.side != 'enemy' or spawned.participant.kind != 'enemy':
        raise ValueError('Mdfyattack recovered bridge currently admits enemy actors only')
    return EnemyAiMdfyAttackSubmission(str(spawned.participant.participant_id), int(skill_slot),
                slots[int(skill_slot)], CALLBACK_NAME, int(target_slot))
