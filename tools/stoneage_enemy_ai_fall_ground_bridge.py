#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_FallGround semantic submission boundary.

The guarded numeric FALLRIDE COM1 is not assigned to recovered25 here.
Submission carries the recovered skill identity, source target and the
unambiguous CP950/Big5 OPTION mechanics. Ordinary ATTACK is used only as a
modern scheduling / physical-resolution carrier.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_fall_ground_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    FallGroundOption,
    fall_ground_attack_power,
    parse_fall_ground_option,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime,
)


RECOVERED25_FALL_GROUND_IDS = (210,)
RECOVERED25_ATTACK_PERCENT_BY_ID = {210: -30.0}


@dataclass(frozen=True)
class EnemyAiFallGroundSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    option: FallGroundOption
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("FallGround submission participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("FallGround submission skill slot must be in 0..6")
        if skill_id not in RECOVERED25_FALL_GROUND_IDS:
            raise ValueError("FallGround submission skill-id outside recovered25 set")
        if self.callback != CALLBACK_NAME:
            raise ValueError("FallGround submission callback drift")
        if not 0 <= target < 10:
            raise ValueError("FallGround source target must be player-side 0..9")
        if not isinstance(self.option,FallGroundOption):
            raise TypeError("FallGround submission option has wrong type")
        if not self.option.marker_present or self.option.attack_percent is None:
            raise ValueError("recovered25 FallGround requires numeric attack marker")
        expected=RECOVERED25_ATTACK_PERCENT_BY_ID[skill_id]
        if float(self.option.attack_percent) != float(expected):
            raise ValueError("recovered25 FallGround attack percent drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("FallGround semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)

    def callback_attack_power(self,fixed_strength:int) -> int:
        return fall_ground_attack_power(int(fixed_strength),self.option)


def resolve_enemy_ai_fall_ground_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiFallGroundSubmission:
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI FallGround skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI FallGround target must be player-side 0..9")

    rows=tuple(sorted(
        (
            entry for entry in petskill_runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids=tuple(int(entry.skill_id) for entry in rows)
    if ids != RECOVERED25_FALL_GROUND_IDS:
        raise ValueError("recovered25 FallGround callback population must be ID 210")

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_FALL_GROUND_IDS:
        raise ValueError(
            "enemy AI selected skill slot outside recovered25 FallGround ID"
        )
    entry=petskill_runtime.skills[skill_id]
    if entry.function_name != CALLBACK_NAME:
        raise ValueError("selected recovered FallGround callback drift")
    option=parse_fall_ground_option(entry.unambiguous_cp950_big5_option())
    return EnemyAiFallGroundSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
        option=option,
    )
