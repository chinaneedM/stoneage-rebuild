"""Typed recovered25 WildViolentAttack admission under a conditional CP950 reference.

The recovered numeric COM1 and original compiler execution charset remain
unassigned.  This bridge admits only the exact recovered callback population
and only the positively referenced ID 541 as an enemy-AI selected skill.
"""
from dataclasses import dataclass
import hashlib

from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime
from tools.stoneage_wildviolent_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    WildViolentSetup,
    resolve_wildviolent_setup,
)

RECOVERED25_WILDVIOLENT_IDS = (541, 652)
RECOVERED25_REFERENCED_IDS = (541,)
EXPECTED_METADATA = {
    541: (1, 6, 2, 1000),
    652: (1, 6, 2, 1000),
}
EXPECTED_OPTION_SHA256 = {
    541: "f63637633ee0e144f8807548d25f51b72f654756f1ec7858e40be0a5f796cb2c",
    652: "9f1b961b626838f19d00f234527f3fd99ca86883befe4204cbdf33ef9bc783b1",
}
CONDITIONAL_EXECUTION_CHARSET = "cp950"
# All three pinned descendants converge for the exact non-empty recovered rows
# under CP950 execution literals.  One profile is used only to run the common
# callback model; this is not a claim about the original recovered compiler.
CONDITIONAL_REFERENCE_PROFILE = "gavin"


@dataclass(frozen=True)
class EnemyAiWildViolentSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    setup: WildViolentSetup
    conditional_execution_charset: str = CONDITIONAL_EXECUTION_CHARSET
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self):
        if not str(self.participant_id) or not 0 <= int(self.skill_slot) < 7:
            raise ValueError("WildViolentAttack requires participant and seven-slot identity")
        if int(self.skill_id) not in RECOVERED25_REFERENCED_IDS or self.callback != CALLBACK_NAME:
            raise ValueError("WildViolentAttack recovered selected ID/callback drift")
        if not 0 <= int(self.source_target_slot) < 10:
            raise ValueError("WildViolentAttack target outside recovered enemy/player-side domain")
        if not isinstance(self.setup, WildViolentSetup):
            raise TypeError("WildViolentAttack callback setup has wrong type")
        if (
            not self.setup.source_return_value
            or self.setup.command_name != COMMAND_NAME
            or int(self.setup.target_slot) != int(self.source_target_slot)
            or self.setup.mode_name != "BATTLE_CHARMODE_C_OK"
            or self.setup.option is None
        ):
            raise ValueError("WildViolentAttack conditional callback setup drift")
        if not 0 <= int(self.setup.option.additive_dodge_percent_points) <= 32767:
            raise ValueError("WildViolentAttack requires defined HIGH(COM3) domain")
        if self.conditional_execution_charset != CONDITIONAL_EXECUTION_CHARSET:
            raise ValueError("WildViolentAttack runtime is conditional-CP950 only")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("WildViolentAttack command symbol drift")
        object.__setattr__(self, "participant_id", str(self.participant_id))
        for key in ("skill_slot", "skill_id", "source_target_slot"):
            object.__setattr__(self, key, int(getattr(self, key)))


def validate_recovered25_wildviolent_population(runtime: Recovered25PetSkillRuntime):
    rows = tuple(
        sorted(
            (entry for entry in runtime.skills.values() if entry.function_name == CALLBACK_NAME),
            key=lambda entry: entry.skill_id,
        )
    )
    if tuple(entry.skill_id for entry in rows) != RECOVERED25_WILDVIOLENT_IDS:
        raise ValueError("WildViolentAttack requires the verified exact two-row callback population")
    for entry in rows:
        raw = bytes(entry.option_bytes)
        if (
            (entry.field, entry.target, entry.cost, entry.illegal) != EXPECTED_METADATA[entry.skill_id]
            or len(raw) != 20
            or hashlib.sha256(raw).hexdigest() != EXPECTED_OPTION_SHA256[entry.skill_id]
        ):
            raise ValueError("WildViolentAttack verified metadata/OPTION hash drift")
        # Data decoding must stay unambiguous before the conditional execution
        # charset is applied.  The callback model then rejects undefined HIGH.
        entry.unambiguous_cp950_big5_option()
        setup = resolve_wildviolent_setup(
            option=raw,
            execution_charset=CONDITIONAL_EXECUTION_CHARSET,
            profile=CONDITIONAL_REFERENCE_PROFILE,
            target_slot=0,
            fixed_strength=1,
            fixed_toughness=1,
            attack_power_before=1,
            defense_power_before=1,
            packed_com3_before=0,
        )
        if setup.option is None or not 0 <= setup.option.additive_dodge_percent_points <= 32767:
            raise ValueError("WildViolentAttack recovered OPTION leaves defined HIGH domain")
    return rows


def resolve_enemy_ai_wildviolent_submission(
    spawned: SpawnedEnemy,
    *,
    skill_slot: int,
    target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime,
    fixed_strength: int,
    fixed_toughness: int,
    attack_power_before: int,
    defense_power_before: int,
    packed_com3_before: int = 0,
):
    rows = validate_recovered25_wildviolent_population(petskill_runtime)
    slots = tuple(int(skill_id) for skill_id in spawned.template.skill_slot_ids)
    if (
        len(slots) != 7
        or not 0 <= int(skill_slot) < 7
        or slots[int(skill_slot)] not in RECOVERED25_REFERENCED_IDS
    ):
        raise ValueError("WildViolentAttack requires authoritative positive seven-slot identity")
    if spawned.participant.side != "enemy" or spawned.participant.kind != "enemy":
        raise ValueError("WildViolentAttack recovered bridge currently admits enemy actors only")
    skill_id = slots[int(skill_slot)]
    entry = next(row for row in rows if row.skill_id == skill_id)
    setup = resolve_wildviolent_setup(
        option=bytes(entry.option_bytes),
        execution_charset=CONDITIONAL_EXECUTION_CHARSET,
        profile=CONDITIONAL_REFERENCE_PROFILE,
        target_slot=int(target_slot),
        fixed_strength=int(fixed_strength),
        fixed_toughness=int(fixed_toughness),
        attack_power_before=int(attack_power_before),
        defense_power_before=int(defense_power_before),
        packed_com3_before=int(packed_com3_before),
    )
    return EnemyAiWildViolentSubmission(
        participant_id=str(spawned.participant.participant_id),
        skill_slot=int(skill_slot),
        skill_id=skill_id,
        callback=CALLBACK_NAME,
        source_target_slot=int(target_slot),
        setup=setup,
    )
