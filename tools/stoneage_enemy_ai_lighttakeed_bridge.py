#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_Lighttakeed admission boundary."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_ABSROB,
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_lighttakeed_model import (
    LIGHTTAKEED_PROFILES,
    PROFILE_BISMARCK_COPY_PLUS_ONE,
    PROFILE_GAVIN_IRIS_COPY,
)
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime


CALLBACK_NAME="PETSKILL_Lighttakeed"
SEMANTIC_COMMAND_NAME="BATTLE_COM_S_LIGHTTAKE"
RECOVERED25_LIGHTTAKEED_IDS=(609,610,611)
EXPECTED_METADATA=(1,7,2,5000)
EXPECTED_OPTION_BY_ID={
    609:(
        "28e420f6e618020e7fdba9f49433a94c5f88cbd6edba2d521104f880b416c5e7",
        DAMAGE_REACT_ABSROB,
    ),
    610:(
        "73bef6383b8b2e301ef6860a573f7b7d703c651aa3e90df3e1efe6f1b28fce01",
        DAMAGE_REACT_REFLEC,
    ),
    611:(
        "a715b2ee62e500775e7eca86facd327f5cdc6501f4064dd322f8fc6e1ddbf96b",
        DAMAGE_REACT_VANISH,
    ),
}
EXPECTED_POSITIVE_TEMPLATE_SLOTS={
    70:(101550,{3:610}),
    157:(101283,{3:610,4:611}),
}


@dataclass(frozen=True)
class EnemyAiLighttakeedSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    marker_kind: int
    profile: str
    attack_power: int
    defense_power: int
    semantic_command_name: str = SEMANTIC_COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        skill_slot=int(self.skill_slot)
        skill_id=int(self.skill_id)
        target=int(self.source_target_slot)
        attack_power=int(self.attack_power)
        defense_power=int(self.defense_power)
        if not participant_id:
            raise ValueError("Lighttakeed participant id must be non-empty")
        if skill_id not in {610,611}:
            raise ValueError("runtime Lighttakeed admits only positive IDs 610/611")
        if not 0 <= skill_slot < 7:
            raise ValueError("Lighttakeed skill slot must be in 0..6")
        if self.callback != CALLBACK_NAME:
            raise ValueError("Lighttakeed callback drift")
        if not 0 <= target < 10:
            raise ValueError(
                "recovered enemy Lighttakeed target must be player-side slot 0..9"
            )
        if int(self.marker_kind) != EXPECTED_OPTION_BY_ID[skill_id][1]:
            raise ValueError("positive recovered Lighttakeed skill/marker identity drift")
        expected_slots={
            slot
            for _,slots in EXPECTED_POSITIVE_TEMPLATE_SLOTS.values()
            for slot,source_id in slots.items()
            if source_id==skill_id
        }
        if skill_slot not in expected_slots:
            raise ValueError("positive recovered Lighttakeed skill/slot identity drift")
        if str(self.profile) not in LIGHTTAKEED_PROFILES:
            raise ValueError("Lighttakeed source profile must be explicit")
        if attack_power < 0 or defense_power < 0:
            raise ValueError("Lighttakeed work powers cannot be negative")
        if self.semantic_command_name != SEMANTIC_COMMAND_NAME:
            raise ValueError("Lighttakeed semantic command-name drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",skill_slot)
        object.__setattr__(self,"skill_id",skill_id)
        object.__setattr__(self,"source_target_slot",target)
        object.__setattr__(self,"marker_kind",int(self.marker_kind))
        object.__setattr__(self,"profile",str(self.profile))
        object.__setattr__(self,"attack_power",attack_power)
        object.__setattr__(self,"defense_power",defense_power)


def validate_recovered25_lighttakeed_population(
    runtime: Recovered25PetSkillRuntime,
) -> None:
    rows=tuple(sorted(
        (
            entry for entry in runtime.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids=tuple(int(entry.skill_id) for entry in rows)
    if ids != RECOVERED25_LIGHTTAKEED_IDS:
        raise ValueError(
            "Lighttakeed requires exact recovered callback population 609/610/611"
        )
    for entry in rows:
        skill_id=int(entry.skill_id)
        if (
            int(entry.field),
            int(entry.target),
            int(entry.cost),
            int(entry.illegal),
        ) != EXPECTED_METADATA:
            raise ValueError("recovered25 Lighttakeed row metadata drift")
        raw=bytes(entry.option_bytes)
        if len(raw)!=6 or b"\0" in raw:
            raise ValueError("recovered25 Lighttakeed OPTION shape drift")
        expected_hash,_=EXPECTED_OPTION_BY_ID[skill_id]
        if hashlib.sha256(raw).hexdigest()!=expected_hash:
            raise ValueError("recovered25 Lighttakeed OPTION hash drift")


def resolve_enemy_ai_lighttakeed_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
    profile: str,
    fixed_strength: int,
    fixed_toughness: int,
) -> EnemyAiLighttakeedSubmission:
    validate_recovered25_lighttakeed_population(petskill_runtime)
    profile=str(profile)
    if profile not in LIGHTTAKEED_PROFILES:
        raise ValueError("Lighttakeed source profile must be explicit")

    skill_slot=int(skill_slot)
    target_slot=int(target_slot)
    if not 0 <= skill_slot < 7:
        raise ValueError("enemy AI Lighttakeed skill slot must be in 0..6")
    if not 0 <= target_slot < 10:
        raise ValueError("enemy AI Lighttakeed target must be player-side 0..9")

    if spawned.participant.side!="enemy" or spawned.participant.kind!="enemy":
        raise ValueError("Lighttakeed recovered bridge currently admits enemy actors only")

    tempno=int(spawned.template.tempno)
    if tempno not in EXPECTED_POSITIVE_TEMPLATE_SLOTS:
        raise ValueError("Lighttakeed actor outside exact positive recovered templates")
    expected_graphic,allowed=EXPECTED_POSITIVE_TEMPLATE_SLOTS[tempno]
    if int(spawned.template.graphic_id)!=expected_graphic:
        raise ValueError("Lighttakeed recovered template graphic identity drift")

    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots)!=7:
        raise ValueError(
            "enemy template lacks authoritative seven-slot pet-skill identity"
        )
    if skill_slot not in allowed or slots[skill_slot] != allowed[skill_slot]:
        raise ValueError("selected slot is not an exact positive Lighttakeed use")

    skill_id=int(slots[skill_slot])
    entry=petskill_runtime.skills[skill_id]
    expected_hash,marker_kind=EXPECTED_OPTION_BY_ID[skill_id]
    raw=bytes(entry.option_bytes)
    if hashlib.sha256(raw).hexdigest()!=expected_hash:
        raise ValueError("selected Lighttakeed OPTION hash drift")

    fixed_strength=int(fixed_strength)
    fixed_toughness=int(fixed_toughness)
    if fixed_strength < 0 or fixed_toughness < 0:
        raise ValueError("Lighttakeed fixed powers cannot be negative")

    return EnemyAiLighttakeedSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=entry.function_name,
        source_target_slot=target_slot,
        marker_kind=marker_kind,
        profile=profile,
        attack_power=int(fixed_strength*0.7),
        defense_power=int(fixed_toughness*0.5),
    )


__all__=[
    "CALLBACK_NAME",
    "SEMANTIC_COMMAND_NAME",
    "RECOVERED25_LIGHTTAKEED_IDS",
    "EnemyAiLighttakeedSubmission",
    "PROFILE_BISMARCK_COPY_PLUS_ONE",
    "PROFILE_GAVIN_IRIS_COPY",
    "resolve_enemy_ai_lighttakeed_submission",
    "validate_recovered25_lighttakeed_population",
]
