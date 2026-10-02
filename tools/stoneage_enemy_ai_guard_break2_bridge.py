#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_GuardBreak2 semantic boundary.

Recovered25 data ID 543 is intentionally kept separate from the fixed-source
PETSKILL_GUARDBREAK2 macro value 542. No historical numeric COM1 is assigned.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_guard_break2_model import CALLBACK_NAME, COMMAND_NAME
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime


RECOVERED25_GUARD_BREAK2_IDS=(543,)


@dataclass(frozen=True)
class EnemyAiGuardBreak2Submission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("GuardBreak2 participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("GuardBreak2 skill slot must be in 0..6")
        if skill_id not in RECOVERED25_GUARD_BREAK2_IDS:
            raise ValueError("GuardBreak2 skill-id outside recovered25 set")
        if self.callback != CALLBACK_NAME:
            raise ValueError("GuardBreak2 callback drift")
        if not 0 <= target < 10:
            raise ValueError(
                "current enemy-AI GuardBreak2 target must be player-side 0..9"
            )
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("GuardBreak2 semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)


def resolve_enemy_ai_guard_break2_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiGuardBreak2Submission:
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI GuardBreak2 skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI GuardBreak2 target must be player-side 0..9")

    rows=tuple(sorted(
        (
            entry for entry in petskill_runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    if tuple(int(entry.skill_id) for entry in rows) != RECOVERED25_GUARD_BREAK2_IDS:
        raise ValueError("recovered25 GuardBreak2 callback population must be ID 543")

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_GUARD_BREAK2_IDS:
        raise ValueError(
            "enemy AI selected skill slot outside recovered25 GuardBreak2 ID"
        )

    entry=petskill_runtime.skills[skill_id]
    if (
        int(entry.field)!=1
        or int(entry.target)!=6
        or int(entry.cost)!=2
        or int(entry.illegal)!=1000
        or bytes(entry.option_bytes)!=b""
    ):
        raise ValueError("recovered25 GuardBreak2 row metadata drift")

    return EnemyAiGuardBreak2Submission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
    )
