#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_BatFly admission boundary.

This bridge binds exact recovered ID633 and its two positive slots on TEMPNO1160
to the bounded BatFly source model. The unresolved historical numeric COM1 is
not guessed; ordinary ATTACK remains only the modern action-order carrier.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from tools.stoneage_batfly_reference_model import (
    BatFlyExecutionGate,
    BatFlyResolution,
    BatFlySetup,
    BatFlyTarget,
    CALLBACK_NAME,
    COMMAND_NAME,
    resolve_batfly_effect,
    resolve_batfly_execution_gate,
    resolve_batfly_setup,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime

RECOVERED25_BATFLY_IDS=(633,)
EXPECTED_METADATA=(1,3,2,5000)
EXPECTED_OPTION_LENGTH=0
EXPECTED_OPTION_SHA256=(
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
EXPECTED_POSITIVE_TEMPLATE_SLOTS={
    1160:(101815,{0:633,3:633}),
}


@dataclass(frozen=True)
class EnemyAiBatFlySubmission:
    participant_id:str
    skill_slot:int
    skill_id:int
    callback:str
    source_target_slot:int
    setup:BatFlySetup
    semantic_command_name:str=COMMAND_NAME

    def __post_init__(self)->None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        if not participant_id:
            raise ValueError("BatFly participant id must be non-empty")
        if skill_id != 633:
            raise ValueError("BatFly runtime admits only recovered ID633")
        if not 0 <= skill_slot < 7:
            raise ValueError("BatFly skill slot must be in 0..6")
        if self.callback != CALLBACK_NAME:
            raise ValueError("BatFly callback drift")
        if not 0 <= target < 10:
            raise ValueError("recovered enemy BatFly target must be player-side 0..9")
        if not isinstance(self.setup,BatFlySetup):
            raise TypeError("BatFly setup has wrong type")
        if not (
            self.setup.command_written
            and self.setup.target_written
            and self.setup.mode_written
            and self.setup.skill_written
        ):
            raise ValueError("BatFly submission requires complete callback writes")
        if int(self.setup.target_slot)!=target:
            raise ValueError("BatFly setup/source target drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("BatFly semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)

    def execution_gate(
        self,
        *,
        living_opposing_slots:tuple[int,...],
        retarget_roll:int|None,
    )->BatFlyExecutionGate:
        return resolve_batfly_execution_gate(
            source_target_slot=int(self.source_target_slot),
            living_opposing_slots=tuple(int(slot) for slot in living_opposing_slots),
            retarget_roll=retarget_roll,
        )

    def effect(
        self,
        *,
        attacker_hp:int,
        attacker_max_hp:int,
        targets:tuple[BatFlyTarget,...],
    )->BatFlyResolution:
        return resolve_batfly_effect(
            attacker_hp=int(attacker_hp),
            attacker_max_hp=int(attacker_max_hp),
            targets=targets,
        )


def validate_recovered25_batfly_population(
    runtime:Recovered25PetSkillRuntime,
)->None:
    if not isinstance(runtime,Recovered25PetSkillRuntime):
        raise TypeError("BatFly bridge requires recovered25 pet-skill runtime")
    rows=tuple(sorted(
        (
            entry for entry in runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids=tuple(int(entry.skill_id) for entry in rows)
    if ids != RECOVERED25_BATFLY_IDS:
        raise ValueError("BatFly requires exact recovered callback population ID633")
    entry=rows[0]
    if (
        int(entry.field),
        int(entry.target),
        int(entry.cost),
        int(entry.illegal),
    ) != EXPECTED_METADATA:
        raise ValueError("recovered25 BatFly row metadata drift")
    raw=bytes(entry.option_bytes)
    if (
        len(raw)!=EXPECTED_OPTION_LENGTH
        or hashlib.sha256(raw).hexdigest()!=EXPECTED_OPTION_SHA256
    ):
        raise ValueError("recovered25 BatFly OPTION identity drift")


def resolve_enemy_ai_batfly_submission(
    spawned:SpawnedEnemy,
    *,
    skill_slot:int,
    target_slot:int,
    petskill_runtime:Recovered25PetSkillRuntime,
)->EnemyAiBatFlySubmission:
    validate_recovered25_batfly_population(petskill_runtime)
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI BatFly skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI BatFly target must be player-side 0..9")
    if spawned.participant.side!="enemy" or spawned.participant.kind!="enemy":
        raise ValueError("BatFly recovered bridge admits enemy actors only")

    tempno=int(spawned.template.tempno)
    if tempno not in EXPECTED_POSITIVE_TEMPLATE_SLOTS:
        raise ValueError("BatFly actor outside exact positive template")
    expected_graphic,allowed=EXPECTED_POSITIVE_TEMPLATE_SLOTS[tempno]
    if int(spawned.template.graphic_id)!=expected_graphic:
        raise ValueError("BatFly recovered template graphic identity drift")
    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots)!=7:
        raise ValueError("enemy template lacks authoritative seven-slot pet-skill identity")
    if skill_slot not in allowed or slots[skill_slot] != allowed[skill_slot]:
        raise ValueError("selected slot is not an exact positive BatFly use")

    entry=runtime.skills[633]
    setup=resolve_batfly_setup(
        target_slot=target_slot,
        skill_array=0,
        packed_com3_before=0,
    )
    return EnemyAiBatFlySubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=633,
        callback=entry.function_name,
        source_target_slot=target_slot,
        setup=setup,
    )


__all__=[
    "RECOVERED25_BATFLY_IDS",
    "EXPECTED_METADATA",
    "EXPECTED_OPTION_LENGTH",
    "EXPECTED_OPTION_SHA256",
    "EXPECTED_POSITIVE_TEMPLATE_SLOTS",
    "EnemyAiBatFlySubmission",
    "resolve_enemy_ai_batfly_submission",
    "validate_recovered25_batfly_population",
]
