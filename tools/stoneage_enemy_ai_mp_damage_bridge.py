#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_MpDamage semantic submission boundary.

The recovered guarded numeric COM1 is not proven.  This bridge binds only the
hard-probed skill identity, target and OPTION semantics. Ordinary ATTACK remains
an internal scheduling/physical-resolution carrier in the reconstructed round.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_mp_damage_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    MpDamageOption,
    parse_mp_damage_option,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime,
)


RECOVERED25_MP_DAMAGE_IDS = (506, 507, 508)
RECOVERED25_MP_PERCENT_BY_ID = {
    506: 50,
    507: 75,
    508: 100,
}


@dataclass(frozen=True)
class EnemyAiMpDamageSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    option: MpDamageOption
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("MpDamage submission participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("MpDamage submission skill slot must be in 0..6")
        if skill_id not in RECOVERED25_MP_DAMAGE_IDS:
            raise ValueError("MpDamage submission skill-id outside recovered25 set")
        if self.callback != CALLBACK_NAME:
            raise ValueError("MpDamage submission callback drift")
        if not 0 <= target < 10:
            raise ValueError("MpDamage source target must be player-side 0..9")
        if not isinstance(self.option,MpDamageOption):
            raise TypeError("MpDamage submission option has wrong type")
        if int(self.option.callback_integer_ratio) != 0:
            raise ValueError("recovered25 MpDamage attack-power ratio must be zero")
        if int(self.option.attack_adjust_token) != 50:
            raise ValueError("recovered25 MpDamage token1 drift")
        expected=RECOVERED25_MP_PERCENT_BY_ID[skill_id]
        if int(self.option.mp_percent) != expected:
            raise ValueError("recovered25 MpDamage percentage drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("MpDamage semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)


def resolve_enemy_ai_mp_damage_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiMpDamageSubmission:
    """Resolve one hard-probed recovered25 MpDamage wa[] selection."""

    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI MpDamage skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI MpDamage target must be player-side 0..9")

    callback_rows=tuple(sorted(
        (
            entry for entry in petskill_runtime.skills.values()
            if entry.function_name == CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids=tuple(int(entry.skill_id) for entry in callback_rows)
    if ids != RECOVERED25_MP_DAMAGE_IDS:
        raise ValueError(
            "recovered25 MpDamage callback population must be IDs 506/507/508"
        )

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_MP_DAMAGE_IDS:
        raise ValueError(
            "enemy AI selected skill slot outside recovered25 MpDamage IDs"
        )
    entry=petskill_runtime.skills[skill_id]
    if entry.function_name != CALLBACK_NAME:
        raise ValueError("selected recovered MpDamage callback drift")

    option=parse_mp_damage_option(entry.ascii_option())
    if option.token_count != 2:
        raise ValueError("recovered25 MpDamage OPTION must have exactly two fields")
    return EnemyAiMpDamageSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
        option=option,
    )
