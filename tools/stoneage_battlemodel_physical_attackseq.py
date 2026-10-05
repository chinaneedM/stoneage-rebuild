"""Explicit equipment-free physical adapter for the bounded ID638 loop.

Reuses accepted physical primitives. This is an experimental composition,
not admission to ordinary rounds or a certification of an original build.
All equipment/later feature modifiers and nonneutral global modifiers are
excluded by the required scope; current HP/status/reactions come from each hit.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_battle_core_model import (
    effective_defense_newpower, effective_defense_preserved_old,
    physical_base_damage, attribute_adjusted_damage, critical_per_10000,
    dodge_per_10000, critical_damage, guard_damage,
)
from tools.stoneage_battle_damage_react_model import base_damage_react_active
from tools.stoneage_battle_guardian_model import GuardianRegistration, guardian_redirect_allowed
from tools.stoneage_battle_status_model import base_status_can_move
from tools.stoneage_battlemodel_hit_loop import (
    BattleModelEntry, BattleModelDraw, BattleModelAttackSeqRng,
    BattleModelAttackSeqResult, BattleModelHitLoopResolution,
    execute_battlemodel_post_attackseq_loop, _int,
)
from tools.stoneage_battlemodel_reference_model import BattleModelAttackObject
from tools.stoneage_enemy_ai_battlemodel_bridge import EnemyAiBattleModelSubmission

PHYSICAL_SCOPE_R1 = "equipment_free_no_bow_no_later_features_neutral_globals_R1"
DEFENSE_PROFILES = frozenset({"newpower_70pct", "preserved_old_mixed"})


@dataclass(frozen=True)
class BattleModelPhysicalProfile:
    participant_id: str
    level: int
    fixed_dex: int
    fixed_luck: int
    defense_power: int
    quick: int
    elements: tuple[int, int, int, int]
    fixed_vital: int | None = None
    command: str = "none"
    no_dodge: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.participant_id, str) or not self.participant_id:
            raise ValueError("physical participant identity required")
        _int(self.level, "level", 1, 2**31 - 1)
        for name in ("fixed_dex", "fixed_luck", "defense_power", "quick"):
            _int(getattr(self, name), name, 0, 2**31 - 1)
        if self.fixed_vital is not None:
            _int(self.fixed_vital, "fixed vital", 0, 2**31 - 1)
        if type(self.elements) is not tuple or len(self.elements) != 4:
            raise ValueError("four explicit elements required")
        for value in self.elements:
            _int(value, "element", 0, 100)
        if sum(self.elements) > 100:
            raise ValueError("total elements must not exceed 100")
        if self.command not in {"none", "guard"}:
            raise ValueError("only neutral/guard commands are in physical scope")
        if type(self.no_dodge) is not bool:
            raise ValueError("explicit no_dodge bool required")


@dataclass(frozen=True)
class BattleModelPhysicalContext:
    scope: str
    defense_profile: str
    profiles: Mapping[int, BattleModelPhysicalProfile]
    guardians: Mapping[int, GuardianRegistration]
    field_attr: str = "none"
    field_power: int = 0

    def __post_init__(self) -> None:
        if self.scope != PHYSICAL_SCOPE_R1:
            raise ValueError("explicit equipment-free neutral physical scope required")
        if self.defense_profile not in DEFENSE_PROFILES:
            raise ValueError("explicit supported defense profile required")
        if self.field_attr not in {"none", "earth", "water", "fire", "wind"}:
            raise ValueError("supported field attribute required")
        _int(self.field_power, "field power", 0, 100)
        if self.field_attr == "none" and self.field_power:
            raise ValueError("neutral field must have zero power")
        profiles, guardians = dict(self.profiles), dict(self.guardians)
        for slot, profile in profiles.items():
            _int(slot, "physical slot", 0, 19)
            if not isinstance(profile, BattleModelPhysicalProfile):
                raise TypeError("typed physical profiles required")
            if self.defense_profile == "preserved_old_mixed" and profile.fixed_vital is None:
                raise ValueError("old defense requires explicit fixed vital")
        for slot, registration in guardians.items():
            _int(slot, "guarded slot", 0, 9)
            if not isinstance(registration, GuardianRegistration):
                raise TypeError("typed Guardian registrations required")
            if registration.guardian_slot > 9:
                raise ValueError("Guardian must be on bounded opposing side")
            if slot not in profiles or registration.guardian_slot not in profiles:
                raise ValueError("Guardian endpoints require physical profiles")
        object.__setattr__(self, "profiles", MappingProxyType(profiles))
        object.__setattr__(self, "guardians", MappingProxyType(guardians))


def _bind_context(submission, actor_slot, entries, context):
    if not isinstance(submission, EnemyAiBattleModelSubmission):
        raise TypeError("exact typed BattleModel submission required")
    if not isinstance(context, BattleModelPhysicalContext):
        raise TypeError("typed physical context required")
    _int(actor_slot, "enemy actor slot", 10, 19)
    if set(entries) != set(context.profiles):
        raise ValueError("physical profiles must exactly cover mapped entries")
    for slot, entry in entries.items():
        _int(slot, "physical entry slot", 0, 19)
        if not isinstance(entry, BattleModelEntry):
            raise TypeError("typed bounded entries required")
        if context.profiles[slot].participant_id != entry.participant_id:
            raise ValueError("physical participant identity mismatch")
    if (actor_slot not in entries or entries[actor_slot].kind != "enemy"
        or entries[actor_slot].participant_id != submission.participant_id
        or not entries[actor_slot].live_target):
        raise ValueError("physical actor must match admitted enemy")
    actor = context.profiles[actor_slot]
    if (actor.defense_power, actor.quick) != submission.setup.powers[1:]:
        raise ValueError("actor defense/quick must match post-setup work powers")
    _int(submission.setup.powers[0], "post-setup attack power", 0, 2**31 - 1)


def resolve_battlemodel_physical_attackseq(
    submission: EnemyAiBattleModelSubmission, *, actor_slot: int,
    attack: BattleModelAttackObject, entries: Mapping[int, BattleModelEntry],
    context: BattleModelPhysicalContext, rng: BattleModelAttackSeqRng,
) -> BattleModelAttackSeqResult:
    """Duck(original) -> Guardian -> critical/damage(actual) -> guard -> floor.

    Caller must pass the current immutable hit snapshot, never initial status.
    No bow/throwing/ride/equipment RNG, counter/combo or global modifications.
    """
    _bind_context(submission, actor_slot, entries, context)
    if not isinstance(attack, BattleModelAttackObject) or not isinstance(rng, BattleModelAttackSeqRng):
        raise TypeError("typed attack and owned RNG required")
    target = _int(attack.target_slot, "physical target", 0, 9)
    if target not in entries or entries[target].kind not in {"player", "pet"} or not entries[target].live_target:
        raise ValueError("live bounded opposing physical target required")
    actor, original = entries[actor_slot], entries[target]
    ap, dp = context.profiles[actor_slot], context.profiles[target]

    def guarding(slot):
        return context.profiles[slot].command == "guard" and not entries[slot].command_cleared

    # GUARD suppresses Duck even when confused; GuardAdjust has a separate gate.
    if (not guarding(target) and not base_damage_react_active(original.reaction)
        and base_status_can_move(original.status_runtime.status)
        and not dp.no_dodge and not original.abio):
        extra = (rng.take("attackseq_drunk_dodge", 20, 30)
                 if actor.status_runtime.status.drunk > 0 else 0)
        per = dodge_per_10000(ap.fixed_dex, dp.fixed_dex,
            dp.fixed_luck if original.kind == "player" else 0,
            attacker_type=actor.kind, defender_type=original.kind,
            extra_percent_points=extra)
        if rng.take("attackseq_dodge", 1, 10000) <= per:
            return BattleModelAttackSeqResult("dodge", 0)

    guardian = None
    registration = context.guardians.get(target)
    if registration is not None:
        candidate = entries[registration.guardian_slot]
        status = candidate.status_runtime.status
        if guardian_redirect_allowed(
            guardian_exists=True, guardian_slot=registration.guardian_slot,
            defender_slot=target, guardian_alive=candidate.live_target,
            guardian_flag=registration.guardian_flag, guardian_sleep=status.sleep,
            guardian_confusion=status.confusion, guardian_paralysis=status.paralysis,
            guardian_stone=status.stone, guardian_barrier=registration.guardian_barrier,
            guardian_is_attacker=registration.guardian_slot == actor_slot,
            attacker_uses_throw_weapon=False,
        ):
            guardian = registration.guardian_slot
    actual = target if guardian is None else guardian
    defender, dp = entries[actual], context.profiles[actual]
    critical = rng.take("attackseq_critical", 1, 10000) < critical_per_10000(
        ap.fixed_dex, dp.fixed_dex, attacker_luck=0, weapon_critical=0,
        attacker_type=actor.kind, defender_type=defender.kind,
    )
    stone = defender.status_runtime.status.stone > 0
    defense = (effective_defense_newpower(dp.defense_power, stone)
               if context.defense_profile == "newpower_70pct" else
               effective_defense_preserved_old(dp.defense_power, dp.quick, dp.fixed_vital, stone))
    power = submission.setup.powers[0]
    high = 1 if defense > power else int(power / (16 if power < defense * (8 / 7) else 8))
    damage = physical_base_damage(power, defense, rng.take("attackseq_damage", 0, high))
    damage = attribute_adjusted_damage(damage, ap.elements, dp.elements,
                                      field_attr=context.field_attr, field_power=context.field_power)
    if critical:
        damage = critical_damage(damage, dp.defense_power, ap.level, dp.level)
    outcome = "critical" if critical else "normal"
    guard = guarding(actual) and defender.status_runtime.status.confusion <= 0
    if guard:
        damage = guard_damage(damage, rng.take("attackseq_guard", 1, 100))
    if damage < 1:
        damage = rng.take("attackseq_minimum", 0, 1)
    if damage == 0:
        outcome = "miss"
        if guardian is not None:
            outcome, damage = "normal", 1
        elif guard:
            outcome = "allguard"
    return BattleModelAttackSeqResult(outcome, damage, guardian)


def execute_battlemodel_physical_loop(
    submission: EnemyAiBattleModelSubmission, *, actor_slot: int,
    execution_scope: str, entries: Mapping[int, BattleModelEntry],
    initial_living_slots: tuple[int, ...], draws: tuple[BattleModelDraw, ...],
    context: BattleModelPhysicalContext,
    source_pet_guard_flags: tuple[bool, ...] | None = None,
) -> BattleModelHitLoopResolution:
    """Connect real shared physical arithmetic to the accepted ordered loop."""
    _bind_context(submission, actor_slot, entries, context)
    return execute_battlemodel_post_attackseq_loop(
        submission, actor_slot=actor_slot, execution_scope=execution_scope,
        entries=entries, initial_living_slots=initial_living_slots, draws=draws,
        source_pet_guard_flags=source_pet_guard_flags,
        attack_sequence=lambda attack, snapshot, rng: resolve_battlemodel_physical_attackseq(
            submission, actor_slot=actor_slot, attack=attack, entries=snapshot,
            context=context, rng=rng),
    )
