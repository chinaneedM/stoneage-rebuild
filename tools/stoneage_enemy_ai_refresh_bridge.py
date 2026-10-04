"""Typed recovered25 Refresh admission without a guessed numeric COM1."""

from dataclasses import dataclass
import hashlib

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime
from tools.stoneage_refresh_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    parse_refresh_option,
)

RECOVERED25_REFRESH_IDS = (583, 584, 591, 592, 593)
RECOVERED25_REFRESH_POSITIVE_IDS = (583, 592)
EXPECTED_METADATA = {
    583: (1, 2, 2, 2000),
    584: (1, 2, 2, 5000),
    591: (1, 1, 2, 5000),
    592: (1, 2, 2, 8000),
    593: (1, 2, 2, 5000),
}
EXPECTED_OPTION_SHA256_BY_ID = {
    583: "e74d4cfac9bf29fbc42059b2082102066ba14d8580014e75a7d84bac762a41d2",
    584: "2653ee645d61ad296ef9af3b7adee729b070341991505ce090cc6ba5e6149433",
    591: "0dfd390b761a2528895e7a7cae6f179dc2fe1302de9e967bf41976a6c92df33b",
    592: "ac95b687bdf0d6fbcc9773bcc0eeeb1d57598e2034919156fd52b74ae193334e",
    593: "8854b46bbf8d23b3b5aa0c309dc863278e27ddb14d72addedcb19254ef866ef6",
}
EXPECTED_IRIS_CP950_STATUS_BY_ID = {
    583: 10,
    584: 8,
    591: 9,
    592: 0,
    593: 7,
}


@dataclass(frozen=True)
class EnemyAiRefreshSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    status_index: int
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        participant_id = str(self.participant_id)
        if not participant_id or not 0 <= int(self.skill_slot) < 7:
            raise ValueError("Refresh requires participant and seven-slot identity")
        if int(self.skill_id) not in RECOVERED25_REFRESH_POSITIVE_IDS:
            raise ValueError("Refresh executable submission requires a positively referenced recovered ID")
        if self.callback != CALLBACK_NAME:
            raise ValueError("Refresh callback drift")
        if not 0 <= int(self.source_target_slot) < 10:
            raise ValueError("Refresh target outside recovered enemy-AI player-side domain")
        expected_status = EXPECTED_IRIS_CP950_STATUS_BY_ID[int(self.skill_id)]
        if int(self.status_index) != expected_status:
            raise ValueError("Refresh conditional status interpretation drift")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("Refresh semantic command symbol drift")
        object.__setattr__(self, "participant_id", participant_id)
        for name in ("skill_slot", "skill_id", "source_target_slot", "status_index"):
            object.__setattr__(self, name, int(getattr(self, name)))


def validate_recovered25_refresh_population(runtime: Recovered25PetSkillRuntime) -> None:
    rows = tuple(sorted(
        (entry for entry in runtime.skills.values() if entry.function_name == CALLBACK_NAME),
        key=lambda entry: entry.skill_id,
    ))
    if tuple(entry.skill_id for entry in rows) != RECOVERED25_REFRESH_IDS:
        raise ValueError("Refresh requires the verified exact five-row callback population")
    for entry in rows:
        skill_id = int(entry.skill_id)
        raw = bytes(entry.option_bytes)
        if (int(entry.field), int(entry.target), int(entry.cost), int(entry.illegal)) != EXPECTED_METADATA[skill_id]:
            raise ValueError("Refresh verified metadata drift")
        if len(raw) != 2 or b"\0" in raw:
            raise ValueError("Refresh requires exact two-byte non-NUL recovered OPTION")
        if hashlib.sha256(raw).hexdigest() != EXPECTED_OPTION_SHA256_BY_ID[skill_id]:
            raise ValueError("Refresh verified OPTION hash drift")
        # The recovered bytes are known to converge under CP950/Big5.  Runtime
        # execution is still explicitly a conditional iris CP950 descendant
        # reference, not an original-binary charset claim.
        entry.unambiguous_cp950_big5_option()
        status = parse_refresh_option(
            raw,
            profile="iris",
            execution_charset="cp950",
        )
        if status != EXPECTED_IRIS_CP950_STATUS_BY_ID[skill_id]:
            raise ValueError("Refresh conditional CP950 status parse drift")


def resolve_enemy_ai_refresh_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
) -> EnemyAiRefreshSubmission:
    validate_recovered25_refresh_population(petskill_runtime)
    slots = tuple(int(value) for value in spawned.template.skill_slot_ids)
    skill_slot = int(skill_slot)
    if len(slots) != 7 or not 0 <= skill_slot < 7:
        raise ValueError("Refresh requires authoritative selected seven-slot identity")
    skill_id = int(slots[skill_slot])
    if skill_id not in RECOVERED25_REFRESH_POSITIVE_IDS:
        raise ValueError("Refresh selected slot is not one of the six positively referenced uses")
    if spawned.participant.side != "enemy" or spawned.participant.kind != "enemy":
        raise ValueError("Refresh recovered bridge currently admits enemy actors only")
    return EnemyAiRefreshSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=skill_slot,
        skill_id=skill_id,
        callback=CALLBACK_NAME,
        source_target_slot=int(target_slot),
        status_index=EXPECTED_IRIS_CP950_STATUS_BY_ID[skill_id],
    )
