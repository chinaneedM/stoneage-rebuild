#!/usr/bin/env python3
"""Exact recovered25 enemy-AI BecomeFox admission; execution remains separate."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

from tools.stoneage_becomefox_reference_model import (
    FoxState,
    TransformDecision,
    resolve_postattack_transform,
)
from tools.stoneage_becomefox_runtime_state import (
    BECOMEFOX_SOURCE_PROFILES,
    FoxParticipantRuntime,
    arrange_guard_active,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime

CALLBACK_NAME="PETSKILL_BecomeFox"
RECOVERED25_BECOMEFOX_IDS=(625,)
RECOVERED25_BECOMEFOX_TEMPNOS=(148,149)
RECOVERED25_BECOMEFOX_SLOT_INDEX=2  # enemybase PETSKILL3 / report slot3
EXPECTED_METADATA=(1,1,2,3000)
EXPECTED_OPTION_LENGTH=0
EXPECTED_OPTION_SHA256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EXPECTED_TEMPLATE_IDENTITIES={
    148:(101743,(32,40,26,30,150)),
    149:(101744,(28,45,22,32,150)),
}
SEMANTIC_COMMAND_NAME="BATTLE_COM_S_BECOMEFOX"


def validate_recovered25_becomefox_population(
    runtime: Recovered25PetSkillRuntime,
) -> None:
    if not isinstance(runtime,Recovered25PetSkillRuntime):
        raise TypeError("BecomeFox requires recovered25 pet-skill runtime")
    rows=tuple(sorted(
        (entry for entry in runtime.skills.values()
         if entry.function_name==CALLBACK_NAME),
        key=lambda entry:int(entry.skill_id),
    ))
    if tuple(int(entry.skill_id) for entry in rows)!=RECOVERED25_BECOMEFOX_IDS:
        raise ValueError("BecomeFox requires exact callback population ID625")
    entry=rows[0]
    if (
        int(entry.field),int(entry.target),int(entry.cost),int(entry.illegal)
    )!=EXPECTED_METADATA:
        raise ValueError("recovered25 BecomeFox row metadata drift")
    raw=bytes(entry.option_bytes)
    if len(raw)!=EXPECTED_OPTION_LENGTH or b"\0" in raw:
        raise ValueError("recovered25 BecomeFox OPTION shape drift")
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_OPTION_SHA256:
        raise ValueError("recovered25 BecomeFox OPTION identity drift")


def _validate_template(spawned: SpawnedEnemy,skill_slot: int) -> None:
    template=spawned.template
    tempno=int(template.tempno)
    if tempno not in EXPECTED_TEMPLATE_IDENTITIES:
        raise ValueError("BecomeFox actor outside exact positive templates")
    graphic,base=EXPECTED_TEMPLATE_IDENTITIES[tempno]
    actual_base=(
        int(template.base_vital),int(template.base_strength),
        int(template.base_toughness),int(template.base_dexterity),int(template.ai),
    )
    if int(template.graphic_id)!=graphic or actual_base!=base:
        raise ValueError("BecomeFox graphic/base-stat/MODAI identity drift")
    slots=tuple(int(value) for value in template.skill_slot_ids)
    if len(slots)!=7:
        raise ValueError("BecomeFox requires authoritative seven-slot identity")
    if (
        int(skill_slot)!=RECOVERED25_BECOMEFOX_SLOT_INDEX
        or slots[int(skill_slot)]!=625
    ):
        raise ValueError("BecomeFox admits only runtime index2/report slot3 ID625")


@dataclass(frozen=True)
class EnemyAiBecomeFoxSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    source_profile: str
    semantic_command_name: str=SEMANTIC_COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        if not participant_id:
            raise ValueError("BecomeFox participant id required")
        if int(self.skill_slot)!=RECOVERED25_BECOMEFOX_SLOT_INDEX:
            raise ValueError("BecomeFox submission slot drift")
        if int(self.skill_id)!=625 or self.callback!=CALLBACK_NAME:
            raise ValueError("BecomeFox submission callback/ID drift")
        target=int(self.source_target_slot)
        if not 0<=target<10:
            raise ValueError("enemy BecomeFox target carrier must be player-side 0..9")
        profile=str(self.source_profile)
        if profile not in BECOMEFOX_SOURCE_PROFILES:
            raise ValueError("BecomeFox source profile must be explicit")
        if self.semantic_command_name!=SEMANTIC_COMMAND_NAME:
            raise ValueError("BecomeFox semantic command identity drift")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"skill_slot",int(self.skill_slot))
        object.__setattr__(self,"skill_id",int(self.skill_id))
        object.__setattr__(self,"source_target_slot",target)
        object.__setattr__(self,"source_profile",profile)

    @property
    def arrange_guard_active(self) -> bool:
        return arrange_guard_active(self.source_profile)

    def postattack(
        self,
        target_state: FoxState,
        *,
        attack_result: str,
        target_alive: bool,
        draw_mod_100: int | None,
        target_is_player: bool,
        target_petflag: int,
        attacker_pig_marker: int,
        current_turn: int,
    ) -> tuple[TransformDecision,FoxParticipantRuntime | None]:
        decision=resolve_postattack_transform(
            target_state,
            command_is_becomefox=True,
            attack_result=str(attack_result),
            target_alive=bool(target_alive),
            draw_mod_100=draw_mod_100,
            target_is_player=bool(target_is_player),
            target_petflag=int(target_petflag),
            attacker_pig_marker=int(attacker_pig_marker),
            arrange_guard_active=self.arrange_guard_active,
            pig_guard_active=True,
            current_turn=int(current_turn),
        )
        runtime=(
            FoxParticipantRuntime(self.source_profile,decision.state)
            if decision.transformed else None
        )
        return decision,runtime


def resolve_enemy_ai_becomefox_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
    source_profile: str,
) -> EnemyAiBecomeFoxSubmission:
    validate_recovered25_becomefox_population(petskill_runtime)
    if spawned.participant.side!="enemy" or spawned.participant.kind!="enemy":
        raise ValueError("BecomeFox recovered bridge admits enemy actors only")
    _validate_template(spawned,int(skill_slot))
    return EnemyAiBecomeFoxSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=int(skill_slot),
        skill_id=625,
        callback=CALLBACK_NAME,
        source_target_slot=int(target_slot),
        source_profile=str(source_profile),
    )


__all__=[
    "CALLBACK_NAME","RECOVERED25_BECOMEFOX_IDS",
    "RECOVERED25_BECOMEFOX_TEMPNOS","RECOVERED25_BECOMEFOX_SLOT_INDEX",
    "EnemyAiBecomeFoxSubmission","resolve_enemy_ai_becomefox_submission",
    "validate_recovered25_becomefox_population",
]
