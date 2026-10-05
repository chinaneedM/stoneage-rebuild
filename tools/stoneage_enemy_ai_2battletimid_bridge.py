#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_2BattleTimid admission boundary.

This bridge binds the exact recovered ID636 row and the two positive enemy
template uses to the conditional descendant callback model.  The original
numeric COM1 identity remains unresolved under DD-019, so ATTACK is only the
modern ordering carrier used by the round runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from tools.stoneage_2battletimid_reference_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    PROFILE_BIG5,
    PROFILE_UTF8,
    TwoBattleTimidPost,
    TwoBattleTimidSetup,
    resolve_2battletimid_post_damage,
    resolve_2battletimid_setup,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillRuntime,
)

RECOVERED25_2BATTLETIMID_IDS=(636,)
EXPECTED_METADATA=(1,7,2,10000)
EXPECTED_OPTION_LENGTH=17
EXPECTED_OPTION_SHA256=(
    "8e6b5dd952bf3bc81e522f1df382db48473b1aeec13f9ff08c7bb76d2c06f9e5"
)
EXPECTED_POSITIVE_TEMPLATE_SLOTS={
    178:(101872,{3:636}),
    179:(101873,{3:636}),
}
EXECUTION_PROFILES=frozenset({PROFILE_UTF8,PROFILE_BIG5})


@dataclass(frozen=True)
class EnemyAiTwoBattleTimidSubmission:
    participant_id:str
    skill_slot:int
    skill_id:int
    callback:str
    source_target_slot:int
    profile:str
    raw_option:bytes
    setup:TwoBattleTimidSetup
    semantic_command_name:str=COMMAND_NAME

    def __post_init__(self)->None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        profile=str(self.profile)
        raw=bytes(self.raw_option)
        if not participant_id:
            raise ValueError("2BattleTimid participant id must be non-empty")
        if skill_id != 636:
            raise ValueError("2BattleTimid runtime admits only recovered ID636")
        if not 0 <= skill_slot < 7:
            raise ValueError("2BattleTimid skill slot must be in 0..6")
        if self.callback != CALLBACK_NAME:
            raise ValueError("2BattleTimid callback drift")
        if not 0 <= target < 10:
            raise ValueError(
                "recovered enemy 2BattleTimid target must be player-side 0..9"
            )
        if profile not in EXECUTION_PROFILES:
            raise ValueError("2BattleTimid execution charset profile must be explicit")
        if (
            len(raw)!=EXPECTED_OPTION_LENGTH
            or b"\0" in raw
            or hashlib.sha256(raw).hexdigest()!=EXPECTED_OPTION_SHA256
        ):
            raise ValueError("2BattleTimid raw OPTION identity drift")
        if not isinstance(self.setup,TwoBattleTimidSetup):
            raise TypeError("2BattleTimid setup has wrong type")
        if not self.setup.accepted or not self.setup.command_written:
            raise ValueError("2BattleTimid submission requires accepted callback setup")
        if int(self.setup.target_slot)!=target:
            raise ValueError("2BattleTimid setup/source target drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("2BattleTimid semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)
        object.__setattr__(self,"profile",profile)
        object.__setattr__(self,"raw_option",raw)

    def post_damage(
        self,
        *,
        draw:int | None,
        damage:int,
        target_is_pet:bool,
        source_target_slot:int,
        default_pet_slot:int,
        pet_noreturn:bool,
        active_original_reaction:bool=False,
    )->TwoBattleTimidPost:
        return resolve_2battletimid_post_damage(
            self.raw_option,
            profile=self.profile,
            damage=int(damage),
            draw=draw,
            target_is_pet=bool(target_is_pet),
            source_target_slot=int(source_target_slot),
            default_pet_slot=int(default_pet_slot),
            pet_noreturn=bool(pet_noreturn),
            active_original_reaction=bool(active_original_reaction),
        )


def validate_recovered25_2battletimid_population(
    runtime:Recovered25PetSkillRuntime,
)->None:
    if not isinstance(runtime,Recovered25PetSkillRuntime):
        raise TypeError("2BattleTimid bridge requires recovered25 pet-skill runtime")
    rows=tuple(sorted(
        (
            entry for entry in runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids=tuple(int(entry.skill_id) for entry in rows)
    if ids != RECOVERED25_2BATTLETIMID_IDS:
        raise ValueError(
            "2BattleTimid requires exact recovered callback population ID636"
        )
    entry=rows[0]
    if (
        int(entry.field),
        int(entry.target),
        int(entry.cost),
        int(entry.illegal),
    ) != EXPECTED_METADATA:
        raise ValueError("recovered25 2BattleTimid row metadata drift")
    raw=bytes(entry.option_bytes)
    if (
        len(raw)!=EXPECTED_OPTION_LENGTH
        or b"\0" in raw
        or hashlib.sha256(raw).hexdigest()!=EXPECTED_OPTION_SHA256
    ):
        raise ValueError("recovered25 2BattleTimid OPTION identity drift")


def resolve_enemy_ai_2battletimid_submission(
    spawned:SpawnedEnemy,
    *,
    skill_slot:int,
    target_slot:int,
    petskill_runtime:Recovered25PetSkillRuntime,
    profile:str,
    fixed_strength:int,
    fixed_toughness:int,
    fixed_dex:int,
)->EnemyAiTwoBattleTimidSubmission:
    validate_recovered25_2battletimid_population(petskill_runtime)
    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    profile=str(profile)
    if profile not in EXECUTION_PROFILES:
        raise ValueError("2BattleTimid execution charset profile must be explicit")
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI 2BattleTimid skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI 2BattleTimid target must be player-side 0..9")
    if spawned.participant.side!="enemy" or spawned.participant.kind!="enemy":
        raise ValueError("2BattleTimid recovered bridge admits enemy actors only")

    tempno=int(spawned.template.tempno)
    if tempno not in EXPECTED_POSITIVE_TEMPLATE_SLOTS:
        raise ValueError("2BattleTimid actor outside exact positive templates")
    expected_graphic,allowed=EXPECTED_POSITIVE_TEMPLATE_SLOTS[tempno]
    if int(spawned.template.graphic_id)!=expected_graphic:
        raise ValueError("2BattleTimid recovered template graphic identity drift")

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots)!=7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    if skill_slot not in allowed or slots[skill_slot] != allowed[skill_slot]:
        raise ValueError("selected slot is not an exact positive 2BattleTimid use")

    entry=petskill_runtime.skills[636]
    fixed_powers=(
        int(fixed_strength),
        int(fixed_toughness),
        int(fixed_dex),
    )
    if any(value<0 for value in fixed_powers):
        raise ValueError("2BattleTimid fixed powers cannot be negative")
    setup=resolve_2battletimid_setup(
        bytes(entry.option_bytes),
        profile=profile,
        target_slot=target_slot,
        # Source LOW(COM3) array identity is not numerically proven for this
        # recovered build. Zero is a modern carrier placeholder, not history.
        skill_array=0,
        packed_com3_before=0,
        fixed_powers=fixed_powers,
        powers_before=fixed_powers,
        valid_actor=True,
    )
    return EnemyAiTwoBattleTimidSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=636,
        callback=entry.function_name,
        source_target_slot=target_slot,
        profile=profile,
        raw_option=bytes(entry.option_bytes),
        setup=setup,
    )


__all__=[
    "RECOVERED25_2BATTLETIMID_IDS",
    "EXPECTED_METADATA",
    "EXPECTED_OPTION_LENGTH",
    "EXPECTED_OPTION_SHA256",
    "EXPECTED_POSITIVE_TEMPLATE_SLOTS",
    "EnemyAiTwoBattleTimidSubmission",
    "resolve_enemy_ai_2battletimid_submission",
    "validate_recovered25_2battletimid_population",
]
