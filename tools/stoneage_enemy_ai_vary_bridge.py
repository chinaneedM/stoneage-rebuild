#!/usr/bin/env python3
"""Recovered25 enemy-AI PETSKILL_Vary admission with explicit source profile."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime
from tools.stoneage_vary_runtime_state import (
    CALLBACK_NAME,
    PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK,
    PROFILE_GAVIN_IRIS_ATTACK_QUICK,
    VARY_PROFILES,
    VaryParticipantRuntime,
    cast_vary,
    create_vary_participant_runtime,
)


RECOVERED25_VARY_IDS = (600,)
RECOVERED25_VARY_TEMPNOS = (981, 982, 983, 984)
RECOVERED25_VARY_SLOT_INDEX = 2  # enemybase PETSKILL3
EXPECTED_METADATA = (1, 5, 2, 1000)
EXPECTED_OPTION_LENGTH = 22
EXPECTED_OPTION_SHA256 = (
    "17e7ff6e7530a5fc2a0964432699f6c82a3dcc79374a2bad6fc547bbdc5e6f99"
)
EXPECTED_GRAPHIC_BY_TEMPNO = {
    981: 101427,
    982: 101424,
    983: 101425,
    984: 101426,
}
SEMANTIC_COMMAND_NAME = "BATTLE_COM_S_VARY"


@dataclass(frozen=True)
class EnemyAiVarySubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_carrier: int
    runtime_after_callback: VaryParticipantRuntime
    semantic_command_name: str = SEMANTIC_COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id = str(self.participant_id)
        skill_slot = int(self.skill_slot)
        skill_id = int(self.skill_id)
        target = int(self.source_target_carrier)
        if not participant_id:
            raise ValueError("Vary participant id must be non-empty")
        if skill_slot != RECOVERED25_VARY_SLOT_INDEX:
            raise ValueError("recovered25 Vary is admitted only from PETSKILL3")
        if skill_id != 600:
            raise ValueError("Vary submission requires recovered25 skill ID 600")
        if self.callback != CALLBACK_NAME:
            raise ValueError("Vary callback drift")
        # TARGET=5 is PETSKILL_TARGET_NONE. Enemy AI still forwards a battle
        # target carrier and the callback writes it to COM2; it is not player
        # target-selection evidence.
        if not 0 <= target < 10:
            raise ValueError("Vary source target carrier must be player-side slot 0..9")
        if not isinstance(self.runtime_after_callback, VaryParticipantRuntime):
            raise TypeError("Vary callback runtime has wrong type")
        if not self.runtime_after_callback.active:
            raise ValueError("Vary submission must carry the post-callback wolf state")
        if self.semantic_command_name != SEMANTIC_COMMAND_NAME:
            raise ValueError("Vary semantic command-name drift")
        object.__setattr__(self, "participant_id", participant_id)
        object.__setattr__(self, "skill_slot", skill_slot)
        object.__setattr__(self, "skill_id", skill_id)
        object.__setattr__(self, "source_target_carrier", target)


def validate_recovered25_vary_population(
    runtime: Recovered25PetSkillRuntime,
) -> None:
    rows = tuple(
        sorted(
            (
                entry
                for entry in runtime.skills.values()
                if entry.function_name == CALLBACK_NAME
            ),
            key=lambda entry: int(entry.skill_id),
        )
    )
    if tuple(int(entry.skill_id) for entry in rows) != RECOVERED25_VARY_IDS:
        raise ValueError("Vary requires the verified exact callback population ID 600")
    entry = rows[0]
    if (
        int(entry.field),
        int(entry.target),
        int(entry.cost),
        int(entry.illegal),
    ) != EXPECTED_METADATA:
        raise ValueError("recovered25 Vary row metadata drift")
    raw = bytes(entry.option_bytes)
    if len(raw) != EXPECTED_OPTION_LENGTH or b"\0" in raw:
        raise ValueError("recovered25 Vary OPTION shape drift")
    if hashlib.sha256(raw).hexdigest() != EXPECTED_OPTION_SHA256:
        raise ValueError("recovered25 Vary OPTION hash drift")


def resolve_enemy_ai_vary_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_carrier: int,
    petskill_runtime: Recovered25PetSkillRuntime,
    profile: str,
    fixed_attack: int,
    fixed_defense: int,
    fixed_quick: int,
) -> EnemyAiVarySubmission:
    validate_recovered25_vary_population(petskill_runtime)
    profile = str(profile)
    if profile not in VARY_PROFILES:
        raise ValueError("Vary source profile must be explicit")

    skill_slot = int(skill_slot)
    target_carrier = int(target_carrier)
    slots = tuple(int(value) for value in spawned.template.skill_slot_ids)
    if len(slots) != 7:
        raise ValueError("Vary requires authoritative seven-slot pet-skill identity")
    if skill_slot != RECOVERED25_VARY_SLOT_INDEX or slots[skill_slot] != 600:
        raise ValueError("Vary selected slot must be recovered PETSKILL3 / ID 600")

    tempno = int(spawned.template.tempno)
    if tempno not in RECOVERED25_VARY_TEMPNOS:
        raise ValueError("Vary actor is outside recovered TEMPNO 981..984")
    expected_graphic = EXPECTED_GRAPHIC_BY_TEMPNO[tempno]
    if int(spawned.template.graphic_id) != expected_graphic:
        raise ValueError("Vary recovered template graphic identity drift")
    if spawned.participant.side != "enemy" or spawned.participant.kind != "enemy":
        raise ValueError("Vary recovered bridge currently admits enemy actors only")

    state = create_vary_participant_runtime(
        profile=profile,
        tempno=tempno,
        base_image=expected_graphic,
        fixed_attack=int(fixed_attack),
        fixed_defense=int(fixed_defense),
        fixed_quick=int(fixed_quick),
    )
    state = cast_vary(state)
    return EnemyAiVarySubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=600,
        callback=CALLBACK_NAME,
        source_target_carrier=target_carrier,
        runtime_after_callback=state,
    )


__all__ = [
    "EnemyAiVarySubmission",
    "PROFILE_BISMARCK_ATTACK_DEFENSE_QUICK",
    "PROFILE_GAVIN_IRIS_ATTACK_QUICK",
    "resolve_enemy_ai_vary_submission",
    "validate_recovered25_vary_population",
]
