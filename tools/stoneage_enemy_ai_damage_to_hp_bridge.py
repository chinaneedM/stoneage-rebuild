#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_DamageToHp semantic submission boundary.

The recovered guarded COM1 number is not proven. Submission therefore carries
only recovered skill identity, source target and parsed fixed-source OPTION.
Ordinary ATTACK is used by the round layer only as an internal ordering and
physical-resolution carrier.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_damage_to_hp_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    DamageToHpOption,
    parse_damage_to_hp_option,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime,
)


RECOVERED25_DAMAGE_TO_HP_IDS = (503, 504, 505)
RECOVERED25_RECOVERY_PERCENT_BY_ID = {
    503: 50,
    504: 70,
    505: 100,
}


@dataclass(frozen=True)
class EnemyAiDamageToHpSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    option: DamageToHpOption
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("DamageToHp submission participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("DamageToHp submission skill slot must be in 0..6")
        if skill_id not in RECOVERED25_DAMAGE_TO_HP_IDS:
            raise ValueError("DamageToHp submission skill-id outside recovered25 set")
        if self.callback != CALLBACK_NAME:
            raise ValueError("DamageToHp submission callback drift")
        if not 0 <= target < 10:
            raise ValueError("DamageToHp source target must be player-side 0..9")
        if not isinstance(self.option,DamageToHpOption):
            raise TypeError("DamageToHp submission option has wrong type")
        if int(self.option.callback_integer_ratio) != 0:
            raise ValueError(
                "recovered25 DamageToHp attack-power ratio must remain zero"
            )
        expected=RECOVERED25_RECOVERY_PERCENT_BY_ID[skill_id]
        if int(self.option.recovery_percent) != expected:
            raise ValueError("recovered25 DamageToHp recovery percent drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("DamageToHp semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)


def resolve_enemy_ai_damage_to_hp_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiDamageToHpSubmission:
    """Resolve one hard-probed recovered25 DamageToHp wa[] selection."""

    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI DamageToHp skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI DamageToHp target must be player-side 0..9")

    callback_rows=tuple(
        sorted(
            (
                entry
                for entry in petskill_runtime.skills.values()
                if entry.function_name == CALLBACK_NAME
            ),
            key=lambda entry:int(entry.skill_id),
        )
    )
    ids=tuple(int(entry.skill_id) for entry in callback_rows)
    if ids != RECOVERED25_DAMAGE_TO_HP_IDS:
        raise ValueError(
            "recovered25 DamageToHp callback population must be IDs "
            "503/504/505"
        )

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_DAMAGE_TO_HP_IDS:
        raise ValueError(
            "enemy AI selected skill slot outside recovered25 DamageToHp IDs"
        )
    entry=petskill_runtime.skills[skill_id]
    if entry.function_name != CALLBACK_NAME:
        raise ValueError("selected recovered DamageToHp callback drift")

    option=parse_damage_to_hp_option(entry.ascii_option())
    if option.token_count != 2:
        raise ValueError("recovered25 DamageToHp OPTION must have exactly two fields")
    return EnemyAiDamageToHpSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
        option=option,
    )
