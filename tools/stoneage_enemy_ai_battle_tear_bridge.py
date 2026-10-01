#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_BattleTearDamage semantic boundary."""

from __future__ import annotations
from dataclasses import dataclass

from tools.stoneage_battle_tear_damage_model import (
    CALLBACK_NAME,COMMAND_NAME,BattleTearSetup,
    battle_tear_callback_setup,c_atoi,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime

RECOVERED25_BATTLE_TEAR_IDS=(615,616)
RECOVERED25_WOUND_PERCENT_BY_ID={615:20,616:50}

@dataclass(frozen=True)
class EnemyAiBattleTearSubmission:
    participant_id:str
    skill_slot:int
    skill_id:int
    callback:str
    source_target_slot:int
    wound_percent:int
    semantic_command_name:str=COMMAND_NAME

    def __post_init__(self):
        pid=str(self.participant_id); slot=int(self.skill_slot)
        skill_id=int(self.skill_id); target=int(self.source_target_slot)
        percent=int(self.wound_percent)
        if not pid: raise ValueError("BattleTear participant id must be non-empty")
        if not 0 <= slot < 7: raise ValueError("BattleTear skill slot must be in 0..6")
        if skill_id not in RECOVERED25_BATTLE_TEAR_IDS:
            raise ValueError("BattleTear skill-id outside recovered25 set")
        if self.callback != CALLBACK_NAME: raise ValueError("BattleTear callback drift")
        if not 0 <= target < 10: raise ValueError("BattleTear target must be player-side 0..9")
        if percent != RECOVERED25_WOUND_PERCENT_BY_ID[skill_id]:
            raise ValueError("BattleTear wound percent drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("BattleTear semantic command-name drift")
        object.__setattr__(self,"participant_id",pid)
        object.__setattr__(self,"skill_slot",slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)
        object.__setattr__(self,"wound_percent",percent)

    def callback_setup(self,*,fixed_strength:int,fixed_toughness:int)->BattleTearSetup:
        return battle_tear_callback_setup(
            fixed_strength=int(fixed_strength),
            fixed_toughness=int(fixed_toughness),
            skill_array=int(self.skill_id),
        )

def resolve_enemy_ai_battle_tear_submission(
    spawned:SpawnedEnemy,*,skill_slot:int,target_slot:int,
    petskill_runtime:Recovered25PetSkillRuntime,
)->EnemyAiBattleTearSubmission:
    skill_slot=int(skill_slot); target_slot=int(target_slot)
    if not 0 <= skill_slot < 7: raise ValueError("enemy AI BattleTear skill slot must be in 0..6")
    if not 0 <= target_slot < 10: raise ValueError("enemy AI BattleTear target must be player-side 0..9")
    rows=tuple(sorted(
        (e for e in petskill_runtime.skills.values() if e.function_name==CALLBACK_NAME),
        key=lambda e:int(e.skill_id),
    ))
    if tuple(int(e.skill_id) for e in rows) != RECOVERED25_BATTLE_TEAR_IDS:
        raise ValueError("recovered25 BattleTear callback population must be IDs 615/616")
    slots=tuple(int(x) for x in spawned.template.skill_slot_ids)
    if len(slots)!=7: raise ValueError("enemy template lacks authoritative seven-slot pet-skill identity")
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_BATTLE_TEAR_IDS:
        raise ValueError("enemy AI selected skill slot outside recovered25 BattleTear IDs")
    entry=petskill_runtime.skills[skill_id]
    if (
        int(entry.field)!=1 or int(entry.target)!=1 or int(entry.cost)!=2
        or int(entry.illegal)!=10000
    ):
        raise ValueError("recovered25 BattleTear row metadata drift")
    return EnemyAiBattleTearSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,skill_id=skill_id,callback=entry.function_name,
        source_target_slot=target_slot,wound_percent=c_atoi(entry.ascii_option()),
    )
