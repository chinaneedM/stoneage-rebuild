#!/usr/bin/env python3
"""Recovered25 enemy-AI ENEMYSKILL_ReLife semantic submission boundary."""

from __future__ import annotations
from dataclasses import dataclass

from tools.stoneage_enemy_relife_model import CALLBACK_NAME, COMMAND_NAME
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime

RECOVERED25_RELIFE_SKILL_ID=500
EXPECTED_ROW=(1,2,2,0,b"")
EXPECTED_TEMPLATE_IDENTITIES={
    39:(100370,4),
    909:(100071,1),
    1165:(101814,3),
}

@dataclass(frozen=True)
class EnemyAiReLifeSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_attack_target_slot: int
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_attack_target_slot)
        if not participant_id:
            raise ValueError("enemy ReLife participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("enemy ReLife skill slot must be in 0..6")
        if skill_id != RECOVERED25_RELIFE_SKILL_ID:
            raise ValueError("enemy ReLife skill-id drift")
        if self.callback != CALLBACK_NAME:
            raise ValueError("enemy ReLife callback drift")
        if not 0 <= target < 10:
            raise ValueError("enemy ReLife fallback carrier must be player-side 0..9")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("enemy ReLife semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_attack_target_slot",target)

def resolve_enemy_ai_relife_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiReLifeSubmission:
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI ReLife skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI ReLife fallback carrier must be player-side 0..9")

    callback_rows=tuple(
        entry for entry in petskill_runtime.skills.values()
        if entry.function_name == CALLBACK_NAME
    )
    if len(callback_rows) != 1:
        raise ValueError("recovered25 ReLife runtime must contain one callback row")
    only=callback_rows[0]
    if int(only.skill_id) != RECOVERED25_RELIFE_SKILL_ID:
        raise ValueError("recovered25 ReLife callback ID drift")
    actual_row=(
        int(only.field),int(only.target),int(only.cost),int(only.illegal),
        bytes(only.option_bytes),
    )
    if actual_row != EXPECTED_ROW:
        raise ValueError("recovered25 ReLife exact row drift")

    tempno=int(spawned.template.tempno)
    if tempno not in EXPECTED_TEMPLATE_IDENTITIES:
        raise ValueError("enemy ReLife actor is outside positive template domain")
    expected_graphic,expected_slot=EXPECTED_TEMPLATE_IDENTITIES[tempno]
    if int(spawned.template.graphic_id) != int(expected_graphic):
        raise ValueError("enemy ReLife graphic identity drift")
    if skill_slot != expected_slot:
        raise ValueError("enemy ReLife selected slot drift from recovered template")
    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError("enemy template lacks authoritative seven-slot identity")
    if int(slots[skill_slot]) != RECOVERED25_RELIFE_SKILL_ID:
        raise ValueError("enemy ReLife template/slot identity drift")

    return EnemyAiReLifeSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=RECOVERED25_RELIFE_SKILL_ID,
        callback=CALLBACK_NAME,
        source_attack_target_slot=target_slot,
    )
