"""Typed recovered25 Weaken admission without a guessed numeric COM1."""
from dataclasses import dataclass
import hashlib

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime
from tools.stoneage_weaken_model import CALLBACK_NAME, COMMAND_NAME, WeakenOption, parse_weaken_option

RECOVERED25_WEAKEN_IDS = (575, 576)
EXPECTED_OPTION_SHA256 = "f58b7a4fdfc76fcefd2eca1a688b46a04c3c3e1a4516fc4a1364436f58d4fed6"
EXPECTED_METADATA = {575: (1, 6, 2, 3000), 576: (1, 3, 2, 0)}


@dataclass(frozen=True)
class EnemyAiWeakenSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    option: WeakenOption = WeakenOption(3, 50)
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self):
        if not str(self.participant_id) or not 0 <= int(self.skill_slot) < 7:
            raise ValueError("Weaken requires participant and seven-slot identity")
        if int(self.skill_id) not in RECOVERED25_WEAKEN_IDS or self.callback != CALLBACK_NAME:
            raise ValueError("Weaken recovered ID/callback drift")
        if not 0 <= int(self.source_target_slot) < 10:
            raise ValueError("Weaken target outside enemy/player-side domain")
        if self.option != WeakenOption(3, 50) or self.semantic_command_name != COMMAND_NAME:
            raise ValueError("Weaken OPTION/command symbol drift")
        object.__setattr__(self, "participant_id", str(self.participant_id))
        for key in ("skill_slot", "skill_id", "source_target_slot"):
            object.__setattr__(self, key, int(getattr(self, key)))


def validate_recovered25_weaken_population(runtime: Recovered25PetSkillRuntime):
    rows = tuple(sorted((e for e in runtime.skills.values() if e.function_name == CALLBACK_NAME),
                        key=lambda e: e.skill_id))
    if tuple(e.skill_id for e in rows) != RECOVERED25_WEAKEN_IDS:
        raise ValueError("Weaken requires the verified exact two-row callback population")
    for e in rows:
        raw = bytes(e.option_bytes)
        if ((e.field, e.target, e.cost, e.illegal) != EXPECTED_METADATA[e.skill_id]
                or len(raw) != 15 or hashlib.sha256(raw).hexdigest() != EXPECTED_OPTION_SHA256):
            raise ValueError("Weaken verified full metadata/OPTION hash drift")
        e.unambiguous_cp950_big5_option()
        if (parse_weaken_option(raw, encoding="cp950") != WeakenOption(3, 50)
                or parse_weaken_option(raw, encoding="big5") != WeakenOption(3, 50)):
            raise ValueError("Weaken encoding/semantic OPTION drift")


def resolve_enemy_ai_weaken_submission(spawned: SpawnedEnemy, *, skill_slot: int,
                                      target_slot: int, petskill_runtime: Recovered25PetSkillRuntime):
    validate_recovered25_weaken_population(petskill_runtime)
    slots = tuple(int(i) for i in spawned.template.skill_slot_ids)
    if len(slots) != 7 or not 0 <= int(skill_slot) < 7 or slots[int(skill_slot)] not in RECOVERED25_WEAKEN_IDS:
        raise ValueError("Weaken requires authoritative selected seven-slot identity")
    if spawned.participant.side != "enemy" or spawned.participant.kind != "enemy":
        raise ValueError("Weaken recovered bridge currently admits enemy actors only")
    return EnemyAiWeakenSubmission(str(spawned.participant.participant_id), int(skill_slot),
                                  slots[int(skill_slot)], CALLBACK_NAME, int(target_slot))
