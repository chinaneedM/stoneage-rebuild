#!/usr/bin/env python3
"""Recovered25 enemy-AI ENEMYSKILL_ReHP semantic submission boundary.

The recovered25 build's guarded numeric COM1 is not proven. This bridge
therefore carries only the recovered callback identity and submitted target.
The round coordinator uses ordinary ATTACK solely as an internal scheduling
carrier, then intercepts it before physical execution. No historical ReHP
numeric command value is asserted here.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_enemy_rehp_model import CALLBACK_NAME, COMMAND_NAME
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime,
)


RECOVERED25_REHP_SKILL_ID = 501


@dataclass(frozen=True)
class EnemyAiReHpSubmission:
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
            raise ValueError("enemy ReHP submission participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("enemy ReHP submission skill slot must be in 0..6")
        if skill_id != RECOVERED25_REHP_SKILL_ID:
            raise ValueError("enemy ReHP submission skill-id drift from recovered25")
        if self.callback != CALLBACK_NAME:
            raise ValueError("enemy ReHP submission callback drift")
        if not 0 <= target < 10:
            raise ValueError("enemy ReHP submitted target must be player-side 0..9")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("enemy ReHP semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)


def resolve_enemy_ai_rehp_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiReHpSubmission:
    """Resolve one recovered enemy wa[] ReHP selection without inventing COM1."""

    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI ReHP skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI ReHP target must be player-side 0..9")

    callback_rows=tuple(
        entry
        for entry in petskill_runtime.skills.values()
        if entry.function_name == CALLBACK_NAME
    )
    if len(callback_rows) != 1:
        raise ValueError(
            "recovered25 ReHP runtime must contain exactly one callback row"
        )
    only=callback_rows[0]
    if int(only.skill_id) != RECOVERED25_REHP_SKILL_ID:
        raise ValueError(
            "recovered25 ReHP callback ID drifted from hard-probed ID 501"
        )

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id != RECOVERED25_REHP_SKILL_ID:
        raise ValueError(
            "enemy AI selected skill slot outside recovered25 ReHP ID 501"
        )
    try:
        entry=petskill_runtime.skills[skill_id]
    except KeyError as exc:
        raise ValueError("enemy AI selected unresolved ReHP skill ID 501") from exc
    if entry.function_name != CALLBACK_NAME:
        raise ValueError(
            "enemy AI selected pet-skill callback outside ReHP submission "
            f"boundary: {entry.function_name}"
        )

    return EnemyAiReHpSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
    )
