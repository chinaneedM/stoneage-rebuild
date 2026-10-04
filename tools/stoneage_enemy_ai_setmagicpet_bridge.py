"""Typed recovered25 SetMagicPet admission without a guessed numeric COM1."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime
from tools.stoneage_setmagicpet_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    SetMagicPetOption,
    parse_setmagicpet_option,
)


RECOVERED25_SETMAGICPET_IDS = (601, 602, 603, 604)
RECOVERED25_SETMAGICPET_POSITIVE_IDS = (601,)
EXPECTED_METADATA = {
    601: (1, 2, 2, 2500),
    602: (1, 2, 2, 2500),
    603: (1, 2, 2, 2500),
    604: (1, 2, 2, 2500),
}
EXPECTED_OPTION_LENGTH_BY_ID = {601: 8, 602: 9, 603: 8, 604: 8}
EXPECTED_OPTION_SHA256_BY_ID = {
    601: "9f79d3271fc37e9a8f16a0fc664a3149efab9b2fb2d8026a89032c331f6ea6a8",
    602: "f696651e7561190d5f9018aa246dd0a5ba8d9ea7b35a92d94b5e9a0a53b272de",
    603: "9e56ba09b3efd92d37969ff10b39441ce14e9fc3eddbe7c806ee3e5a243cb39d",
    604: "3c627e924f3b3f5e19f2d7c6db7811e174ac6958c2ba3f4067f98822def3cbf2",
}
EXPECTED_OPTION_FACTS_BY_ID = {
    601: (3, 15, "TGH"),
    602: (3, 3000, "HP"),
    603: (3, 10, "STR"),
    604: (3, 15, "DEX"),
}


@dataclass(frozen=True)
class EnemyAiSetMagicPetSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    option: SetMagicPetOption
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        if not participant_id or not 0 <= int(self.skill_slot) < 7:
            raise ValueError("SetMagicPet requires participant and seven-slot identity")
        if int(self.skill_id) not in RECOVERED25_SETMAGICPET_POSITIVE_IDS:
            raise ValueError(
                "SetMagicPet executable submission requires the positively "
                "referenced recovered ID 601"
            )
        if self.callback != CALLBACK_NAME:
            raise ValueError("SetMagicPet callback drift")
        if not 0 <= int(self.source_target_slot) < 10:
            raise ValueError(
                "SetMagicPet target outside recovered enemy-AI player-side domain"
            )
        option=self.option
        if not isinstance(option,SetMagicPetOption):
            raise TypeError("SetMagicPet OPTION has wrong type")
        if (option.turn,option.amount,option.kind) != EXPECTED_OPTION_FACTS_BY_ID[601]:
            raise ValueError("SetMagicPet positive OPTION semantic drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("SetMagicPet semantic command symbol drift")
        object.__setattr__(self,"participant_id",participant_id)
        for name in ("skill_slot","skill_id","source_target_slot"):
            object.__setattr__(self,name,int(getattr(self,name)))


def validate_recovered25_setmagicpet_population(
    runtime: Recovered25PetSkillRuntime,
) -> None:
    rows=tuple(sorted(
        (
            entry
            for entry in runtime.skills.values()
            if entry.function_name == CALLBACK_NAME
        ),
        key=lambda entry:entry.skill_id,
    ))
    if tuple(entry.skill_id for entry in rows) != RECOVERED25_SETMAGICPET_IDS:
        raise ValueError(
            "SetMagicPet requires the verified exact four-row callback population"
        )
    for entry in rows:
        skill_id=int(entry.skill_id)
        raw=bytes(entry.option_bytes)
        if (
            int(entry.field),int(entry.target),int(entry.cost),int(entry.illegal)
        ) != EXPECTED_METADATA[skill_id]:
            raise ValueError("SetMagicPet verified metadata drift")
        if len(raw) != EXPECTED_OPTION_LENGTH_BY_ID[skill_id] or b"\0" in raw:
            raise ValueError("SetMagicPet verified OPTION byte-length drift")
        if hashlib.sha256(raw).hexdigest() != EXPECTED_OPTION_SHA256_BY_ID[skill_id]:
            raise ValueError("SetMagicPet verified OPTION hash drift")
        parsed=parse_setmagicpet_option(raw)
        if (parsed.turn,parsed.amount,parsed.kind) != EXPECTED_OPTION_FACTS_BY_ID[skill_id]:
            raise ValueError("SetMagicPet verified OPTION semantic drift")


def resolve_enemy_ai_setmagicpet_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiSetMagicPetSubmission:
    validate_recovered25_setmagicpet_population(petskill_runtime)
    slots=tuple(int(value) for value in spawned.template.skill_slot_ids)
    skill_slot=int(skill_slot)
    if len(slots) != 7 or not 0 <= skill_slot < 7:
        raise ValueError(
            "SetMagicPet requires authoritative selected seven-slot identity"
        )
    skill_id=int(slots[skill_slot])
    if skill_id not in RECOVERED25_SETMAGICPET_POSITIVE_IDS:
        raise ValueError(
            "SetMagicPet selected slot is not one of the six positive ID-601 uses"
        )
    if spawned.participant.side != "enemy" or spawned.participant.kind != "enemy":
        raise ValueError(
            "SetMagicPet recovered bridge currently admits enemy actors only"
        )
    entry=petskill_runtime.skills[skill_id]
    option=parse_setmagicpet_option(bytes(entry.option_bytes))
    return EnemyAiSetMagicPetSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=CALLBACK_NAME,
        source_target_slot=int(target_slot),
        option=option,
    )
