"""Exact recovered25 BattleModel admission, before ordered runtime integration.

Report slots are one-based; all submission indices are zero-based. The raw
OPTION is supplied at runtime, never reconstructed from report summaries.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from types import MappingProxyType

from tools.stoneage_battlemodel_reference_model import (
    BASE_STATUS_LITERALS_BY_SOURCE, CHARSETS, CALLBACK_NAME, COMMAND_NAME,
    BattleModelOptionShape, BattleModelSetup, BattleModelTargetPlan,
    inspect_battlemodel_option, resolve_battlemodel_setup,
    resolve_battlemodel_target_plan,
)
from tools.stoneage_recovered25_battlemodel_probe import (
    EXPECTED_CALLBACK_IDS, EXPECTED_EXACT_ROWS, EXPECTED_TEMPLATE_ROWS,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime


# Schema of the independently accepted exact-data probe, with no slot-count
# or codec summaries included in the runtime row identity.
EXPECTED_ROW_IDENTITIES = MappingProxyType({
    row[0]: (*row[1:5], row[6], row[7]) for row in EXPECTED_EXACT_ROWS
})
EXPECTED_TEMPLATE_IDENTITIES = MappingProxyType({
    row[0]: (row[1], tuple(row[2:7]), MappingProxyType({
        report_slot - 1: skill_id
        for report_slot, skill_id in zip(row[7], row[8])
    })) for row in EXPECTED_TEMPLATE_ROWS
})


def _integer(value: int, name: str) -> int:
    if type(value) is not int:
        raise ValueError(name + " must be an integer")
    return value


def _option_identity(raw: bytes) -> tuple[int, str]:
    if type(raw) is not bytes or b"\0" in raw:
        raise ValueError("BattleModel OPTION requires non-NUL bytes")
    return len(raw), hashlib.sha256(raw).hexdigest()


def validate_recovered25_battlemodel_population(runtime: Recovered25PetSkillRuntime) -> None:
    if not isinstance(runtime, Recovered25PetSkillRuntime):
        raise TypeError("BattleModel requires recovered25 pet-skill runtime")
    rows = {skill_id: row for skill_id, row in runtime.skills.items()
            if row.function_name == CALLBACK_NAME}
    if tuple(sorted(rows)) != EXPECTED_CALLBACK_IDS:
        raise ValueError("BattleModel complete callback population drift")
    for skill_id, row in rows.items():
        actual = (row.field, row.target, row.cost, row.illegal,
                  *_option_identity(row.option_bytes))
        if actual != EXPECTED_ROW_IDENTITIES[skill_id]:
            raise ValueError(f"BattleModel row identity drift for ID{skill_id}")


def _validate_template(tempno: int, graphic: int, base: tuple[int, ...],
                       slots: tuple[int, ...], selected: int) -> None:
    if tempno not in EXPECTED_TEMPLATE_IDENTITIES:
        raise ValueError("BattleModel actor outside exact positive templates")
    expected_graphic, expected_base, allowed = EXPECTED_TEMPLATE_IDENTITIES[tempno]
    if graphic != expected_graphic or base != expected_base:
        raise ValueError("BattleModel graphic/base-stat/AI identity drift")
    if len(slots) != 7:
        raise ValueError("BattleModel requires authoritative seven-slot identity")
    positive = {index: value for index, value in enumerate(slots)
                if value in EXPECTED_CALLBACK_IDS}
    if positive != dict(allowed):
        raise ValueError("BattleModel positive slot population drift")
    if selected not in allowed or slots[selected] != 638:
        raise ValueError("BattleModel admits only runtime index2 (report slot3)")


@dataclass(frozen=True)
class EnemyAiBattleModelSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_carrier: int
    template_tempno: int
    template_graphic: int
    template_base_identity: tuple[int, ...]
    template_skill_slots: tuple[int, ...]
    profile: str
    source_profile: str
    powers_before: tuple[int, int, int]
    raw_option: bytes = field(repr=False)
    setup: BattleModelSetup
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self) -> None:
        if not isinstance(self.participant_id, str) or not self.participant_id:
            raise ValueError("BattleModel participant id required")
        for name in ("skill_slot", "skill_id", "source_target_carrier",
                     "template_tempno", "template_graphic"):
            _integer(getattr(self, name), name)
        if self.skill_id != 638 or self.callback != CALLBACK_NAME:
            raise ValueError("BattleModel runtime admits only exact positive ID638")
        if not 0 <= self.source_target_carrier < 10:
            raise ValueError("BattleModel scheduling carrier must be player-side 0..9")
        if self.profile not in CHARSETS or self.source_profile not in BASE_STATUS_LITERALS_BY_SOURCE:
            raise ValueError("BattleModel charset and source profiles must be explicit")
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError("BattleModel symbolic command identity drift")
        base = tuple(_integer(v, "template base") for v in self.template_base_identity)
        slots = tuple(_integer(v, "template skill") for v in self.template_skill_slots)
        _validate_template(self.template_tempno, self.template_graphic, base, slots, self.skill_slot)
        if _option_identity(self.raw_option) != EXPECTED_ROW_IDENTITIES[638][-2:]:
            raise ValueError("BattleModel positive OPTION identity drift")
        powers = tuple(_integer(v, "work power") for v in self.powers_before)
        if len(powers) != 3 or any(v < 0 for v in powers):
            raise ValueError("BattleModel requires three nonnegative current work powers")
        expected = resolve_battlemodel_setup(
            self.raw_option, profile=self.profile, skill_array=0,
            powers_before=powers, object_count_roll=None,
        )
        if not isinstance(self.setup, BattleModelSetup) or self.setup != expected:
            raise ValueError("BattleModel callback setup does not match authoritative inputs")
        object.__setattr__(self, "template_base_identity", base)
        object.__setattr__(self, "template_skill_slots", slots)
        object.__setattr__(self, "powers_before", powers)

    @property
    def option_shape(self) -> BattleModelOptionShape:
        return inspect_battlemodel_option(
            self.raw_option, profile=self.profile, source_profile=self.source_profile,
        )

    def target_plan(self, *, living_opposing_slots: tuple[int, ...],
                    excess_target_rolls: tuple[int, ...]) -> BattleModelTargetPlan:
        living = tuple(_integer(v, "living player slot") for v in living_opposing_slots)
        if any(not 0 <= v < 10 for v in living):
            raise ValueError("BattleModel opposing slots must be player-side 0..9")
        draws = tuple(_integer(v, "excess target draw") for v in excess_target_rolls)
        return resolve_battlemodel_target_plan(
            attack_type=self.setup.attack_type, object_count=self.setup.object_count,
            living_opposing_slots=living, action_numbers=self.option_shape.action_numbers,
            excess_target_rolls=draws,
        )


def resolve_enemy_ai_battlemodel_submission(
    spawned: SpawnedEnemy, *, skill_slot: int, target_slot: int,
    petskill_runtime: Recovered25PetSkillRuntime, profile: str,
    source_profile: str, powers_before: tuple[int, int, int],
) -> EnemyAiBattleModelSubmission:
    validate_recovered25_battlemodel_population(petskill_runtime)
    _integer(skill_slot, "skill_slot")
    _integer(target_slot, "target_slot")
    if spawned.participant.side != "enemy" or spawned.participant.kind != "enemy":
        raise ValueError("BattleModel recovered bridge admits enemy actors only")
    template = spawned.template
    base = (template.base_vital, template.base_strength, template.base_toughness,
            template.base_dexterity, template.ai)
    slots = tuple(template.skill_slot_ids)
    _validate_template(template.tempno, template.graphic_id, base, slots, skill_slot)
    raw = petskill_runtime.skills[638].option_bytes
    setup = resolve_battlemodel_setup(
        raw, profile=profile, skill_array=0, powers_before=powers_before,
        object_count_roll=None,
    )
    return EnemyAiBattleModelSubmission(
        participant_id=spawned.participant.participant_id,
        skill_slot=skill_slot, skill_id=638, callback=CALLBACK_NAME,
        source_target_carrier=target_slot, template_tempno=template.tempno,
        template_graphic=template.graphic_id, template_base_identity=base,
        template_skill_slots=slots, profile=profile, source_profile=source_profile,
        powers_before=powers_before, raw_option=raw, setup=setup,
    )
