#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_Nocast semantic submission boundary."""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_nocast_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    NocastOption,
    parse_nocast_option,
)
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime


RECOVERED25_NOCAST_IDS=(580,)
RECOVERED25_NOCAST_OPTION=NocastOption(turn=3,success_offset=50)


@dataclass(frozen=True)
class EnemyAiNocastSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    option: NocastOption
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("Nocast participant id must be non-empty")
        if not 0 <= skill_slot < 7:
            raise ValueError("Nocast skill slot must be in 0..6")
        if skill_id not in RECOVERED25_NOCAST_IDS:
            raise ValueError("Nocast skill-id outside recovered25 set")
        if self.callback != CALLBACK_NAME:
            raise ValueError("Nocast callback drift")
        if not 0 <= target < 10:
            raise ValueError("current enemy-AI Nocast target must be player-side 0..9")
        if self.option != RECOVERED25_NOCAST_OPTION:
            raise ValueError("recovered25 Nocast OPTION drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("Nocast semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)


def resolve_enemy_ai_nocast_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiNocastSubmission:
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI Nocast skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI Nocast target must be player-side 0..9")

    rows=tuple(sorted(
        (
            entry for entry in petskill_runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    if tuple(int(entry.skill_id) for entry in rows) != RECOVERED25_NOCAST_IDS:
        raise ValueError("recovered25 Nocast callback population must be ID 580")

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError("enemy template lacks authoritative seven-slot pet-skill identity")
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_NOCAST_IDS:
        raise ValueError("enemy AI selected skill slot outside recovered25 Nocast ID")
    entry=petskill_runtime.skills[skill_id]
    if (
        int(entry.field)!=1
        or int(entry.target)!=3
        or int(entry.cost)!=2
        or int(entry.illegal)!=1000
    ):
        raise ValueError("recovered25 Nocast row metadata drift")
    entry.unambiguous_cp950_big5_option()
    option=parse_nocast_option(entry.option_bytes,encoding="cp950")
    return EnemyAiNocastSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
        option=option,
    )
