"""Bounded BattleModel scheduling and post-AttackSeq no-ride lifecycle.

AttackSeq is an explicit injected dependency, not reconstructed by this module.
This seam executes target selection, marker settlement and status in order. It
does not enable the round/coordinator path or certify production AttackSeq.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Callable, Mapping

from tools.stoneage_enemy_ai_battlemodel_bridge import EnemyAiBattleModelSubmission
from tools.stoneage_battlemodel_reference_model import BattleModelAttackObject
from tools.stoneage_battle_damage_react_model import (
    BaseDamageReactState, BaseDamageReactResolution, resolve_base_damage_react,
    DAMAGE_REACT_REFLEC, DAMAGE_REACT_ABSROB, DAMAGE_REACT_VANISH,
)
from tools.stoneage_battle_core_model import (
    BattleUltimateDamageInputs, resolve_battle_ultimate_damage,
    BattleDeathUltimateInputs, resolve_battle_death_ultimate_override,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime, BaseStatusAttackInputs, BaseStatusApplicationResolution,
    active_base_status_names, resolve_base_damage_wakeup, resolve_base_status_application,
)

HIT_LOOP_SCOPE_R1 = "reduced_SIDE_OFFSET10_no_ride_nonthrowing_no_ItemCrush_gDamageDiv0"


def _int(value: int, name: str, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in {low}..{high}")
    return value


def resolve_battlemodel_marker_settlement(
    state: BaseDamageReactState, *, raw_damage: int, attacker_hp: int,
    attacker_max_hp: int, defender_hp: int, defender_max_hp: int,
) -> BaseDamageReactResolution:
    """Physical marker branch only: nonthrowing, no ride, base reactions."""
    _int(raw_damage, "raw damage", 0, 2**31 - 1)
    result = resolve_base_damage_react(
        state, raw_damage=raw_damage, attacker_hp=attacker_hp,
        attacker_max_hp=attacker_max_hp, defender_hp=defender_hp,
        defender_max_hp=defender_max_hp, attacker_uses_throwing_weapon=False,
    )
    if result.effective_kind == DAMAGE_REACT_REFLEC:
        # DamageSub's BattleModel marker suppresses both HP subtractions.
        # Reported damage and charge consumption survive; helper wakes defender.
        result = replace(result, attacker_hp_after=attacker_hp,
                         defender_hp_after=defender_hp, damage_target="none",
                         wakeup_target="defender")
    return result


@dataclass(frozen=True)
class BattleModelEntry:
    participant_id: str
    kind: str
    hp: int
    max_hp: int
    paralysis_resistance: int
    status_runtime: BaseBattleStatusRuntime = field(default_factory=BaseBattleStatusRuntime)
    reaction: BaseDamageReactState = field(default_factory=BaseDamageReactState)
    accumulated_overkill: int = 0
    marker: int = 0
    command_cleared: bool = False
    ultimate_flag: bool = False
    abio: bool = False
    target_check_allowed: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.participant_id, str) or not self.participant_id:
            raise ValueError("entry participant identity required")
        if self.kind not in {"player", "pet", "enemy"}:
            raise ValueError("bounded BattleModel entry kind required")
        _int(self.max_hp, "max HP", 1, 2**31 - 1)
        _int(self.hp, "HP", 0, self.max_hp)
        _int(self.paralysis_resistance, "paralysis resistance", -(2**31), 2**31 - 1)
        _int(self.accumulated_overkill, "accumulated overkill", 0, 2**31 - 1)
        _int(self.marker, "preserved marker", -(2**31), 2**31 - 1)
        if not isinstance(self.status_runtime, BaseBattleStatusRuntime):
            raise TypeError("BattleModel status runtime required")
        if not isinstance(self.reaction, BaseDamageReactState):
            raise TypeError("BattleModel base reaction state required")
        for name in ("command_cleared", "ultimate_flag", "abio", "target_check_allowed"):
            if type(getattr(self, name)) is not bool:
                raise ValueError(name + " must be explicit bool")

    @property
    def live_target(self) -> bool:
        # Ultimate entry flags do not independently appear in TargetCheck.
        return self.hp > 0 and self.target_check_allowed


@dataclass(frozen=True)
class BattleModelDraw:
    ordinal: int
    owner: str
    value: int

    def __post_init__(self) -> None:
        _int(self.ordinal, "scheduled ordinal", 0, 9)
        if self.owner not in {"target_selection", "status", "critical_death",
                              "attackseq_dodge", "attackseq_critical", "attackseq_damage",
                              "attackseq_guard", "attackseq_minimum"}:
            raise ValueError("unknown BattleModel RNG owner")
        _int(self.value, "draw", -(2**31), 2**31 - 1)


@dataclass(frozen=True)
class BattleModelTrace:
    phase: str
    ordinal: int
    target_slot: int
    draw: BattleModelDraw | None = None


class BattleModelAttackSeqRng:
    """Only AttackSeq owners are exposed to the injected physical resolver."""
    def __init__(self, take: Callable[[str, int, int], int]):
        self._take = take

    def take(self, owner: str, low: int, high: int) -> int:
        if owner not in {"attackseq_dodge", "attackseq_critical", "attackseq_damage",
                         "attackseq_guard", "attackseq_minimum"}:
            raise ValueError("AttackSeq cannot consume target/status/death RNG")
        return self._take(owner, low, high)


@dataclass(frozen=True)
class BattleModelAttackSeqResult:
    outcome: str
    raw_damage: int
    guardian_slot: int | None = None

    def __post_init__(self) -> None:
        if self.outcome not in {"normal", "critical", "miss", "dodge", "allguard"}:
            raise ValueError("unsupported bounded AttackSeq outcome")
        _int(self.raw_damage, "AttackSeq raw damage", 0, 2**31 - 1)
        if self.guardian_slot is not None:
            _int(self.guardian_slot, "Guardian slot", 0, 9)


@dataclass(frozen=True)
class BattleModelHitEvent:
    ordinal: int
    attack: BattleModelAttackObject
    outcome: str
    actual_defender_slot: int | None = None
    reported_damage: int = 0
    hp_loss: int = 0
    reaction: BaseDamageReactResolution | None = None
    status_application: BaseStatusApplicationResolution | None = None
    ultimate_kind: int = 0
    pet_presentation_damage: int = 0  # modern safe no-ride/DODGE value


@dataclass(frozen=True)
class BattleModelHitLoopResolution:
    initial_living_slots: tuple[int, ...]
    entries: Mapping[int, BattleModelEntry]
    events: tuple[BattleModelHitEvent, ...]
    trace: tuple[BattleModelTrace, ...]
    draws_consumed: tuple[BattleModelDraw, ...]
    cleared_command_slots: frozenset[int]


def execute_battlemodel_post_attackseq_loop(
    submission: EnemyAiBattleModelSubmission, *, actor_slot: int,
    execution_scope: str,
    entries: Mapping[int, BattleModelEntry], initial_living_slots: tuple[int, ...],
    draws: tuple[BattleModelDraw, ...],
    attack_sequence: Callable[[BattleModelAttackObject, Mapping[int, BattleModelEntry],
                               BattleModelAttackSeqRng], BattleModelAttackSeqResult],
    source_pet_guard_flags: tuple[bool, ...] | None = None,
) -> BattleModelHitLoopResolution:
    """Execute source-ordered no-ride ID638 helper composition.

    The caller supplies an authoritative initial MultiList order and an
    AttackSeq dependency (including Guardian eligibility and physical RNG).
    Mount/throwing/Weaken, ItemCrush, nonzero gDamageDiv, numeric COM1 and round-exit integration
    are outside this seam and cannot be certified through this API.
    """
    if not isinstance(submission, EnemyAiBattleModelSubmission):
        raise TypeError("exact typed BattleModel submission required")
    if execution_scope != HIT_LOOP_SCOPE_R1:
        raise ValueError("explicit reduced BattleModel execution scope required")
    if submission.setup.attack_type != 5 or submission.setup.object_count != 4:
        raise ValueError("only admitted physical four-object ID638 is bounded")
    shape = submission.option_shape
    if shape.status_index not in (None, 2) or shape.turn_value != 1 or shape.hit_value != 30:
        raise ValueError("only admitted ID638 paralysis/unknown profile is bounded")
    _int(actor_slot, "enemy actor slot", 10, 19)
    current = dict(entries)
    for slot, entry in current.items():
        _int(slot, "entry slot", 0, 19)
        if not isinstance(entry, BattleModelEntry):
            raise TypeError("immutable BattleModel entries required")
    if len({e.participant_id for e in current.values()}) != len(current):
        raise ValueError("duplicate participant entry identity")
    if (actor_slot not in current or current[actor_slot].kind != "enemy"
        or current[actor_slot].participant_id != submission.participant_id
        or not current[actor_slot].live_target):
        raise ValueError("live enemy actor entry required")
    living = tuple(initial_living_slots)
    if not living or len(living) > 10 or len(set(living)) != len(living):
        raise ValueError("nonempty unique initial MultiList required")
    for slot in living:
        _int(slot, "opposing slot", 0, 9)
        if slot not in current or not current[slot].live_target:
            raise ValueError("initial list contains unavailable target")
        if current[slot].kind == "enemy":
            raise ValueError("bounded opposing target must be player or pet")
    if any(current[s].kind == "pet" for s in living):
        if source_pet_guard_flags is None or len(source_pet_guard_flags) != 20:
            raise ValueError("pet target requires explicit twenty-entry source guard flags")
    if source_pet_guard_flags is not None:
        if len(source_pet_guard_flags) != 20 or any(type(v) is not bool for v in source_pet_guard_flags):
            raise ValueError("source pet guard flags require twenty bool entries")
        if any(current[s].ultimate_flag != source_pet_guard_flags[s] for s in current):
            raise ValueError("source flags and mapped entry ultimate flags disagree")
    flags = list(source_pet_guard_flags or (False,) * 20)
    for slot, entry in current.items():
        flags[slot] = entry.ultimate_flag
    tape = tuple(draws)
    if any(not isinstance(d, BattleModelDraw) for d in tape):
        raise TypeError("typed RNG tape required")
    trace, events, consumed = [], [], []
    position = 0
    cleared = {s for s, e in current.items() if e.command_cleared}

    def take(owner: str, low: int, high: int, ordinal: int, target: int) -> int:
        nonlocal position
        if position >= len(tape):
            raise ValueError(f"missing {owner} draw at ordinal{ordinal}")
        draw = tape[position]
        if draw.ordinal != ordinal or draw.owner != owner:
            raise ValueError(f"RNG chronology/owner mismatch at ordinal{ordinal}: expected {owner}")
        _int(draw.value, owner + " draw", low, high)
        position += 1
        consumed.append(draw)
        trace.append(BattleModelTrace("rng", ordinal, target, draw))
        return draw.value

    # Do not precompute excess selections: each follows prior hit/status work.
    count = max(4, len(living))
    for ordinal in range(count):
        if ordinal < min(4, len(living)):
            obj, target = ordinal, living[ordinal]
        elif len(living) > 4:
            obj, target = (ordinal - 4) % 4, living[ordinal]
        else:
            obj = ordinal
            selected = take("target_selection", 0, len(living) - 1, ordinal, -1)
            target = living[selected]
        action = shape.action_numbers[obj % len(shape.action_numbers)] if shape.action_numbers else -1
        attack = BattleModelAttackObject(obj, target, action)
        entry = current[target]
        if not entry.live_target:
            events.append(BattleModelHitEvent(ordinal, attack, "skipped_target"))
            trace.append(BattleModelTrace("skip_target", ordinal, target))
            continue
        if entry.kind == "pet" and flags[target + 5]:
            events.append(BattleModelHitEvent(ordinal, attack, "skipped_source_pet_flag"))
            trace.append(BattleModelTrace("skip_source_pet_flag", ordinal, target))
            continue
        trace.append(BattleModelTrace("attackseq", ordinal, target))
        rng = BattleModelAttackSeqRng(lambda owner, low, high: take(owner, low, high, ordinal, target))
        hit = attack_sequence(attack, MappingProxyType(dict(current)), rng)
        if not isinstance(hit, BattleModelAttackSeqResult):
            raise TypeError("AttackSeq dependency must return typed result")
        defender_slot = target
        if hit.guardian_slot is not None:
            candidate = current.get(hit.guardian_slot)
            if candidate is not None and candidate.live_target:
                defender_slot = hit.guardian_slot
        defender = current[defender_slot]
        before = defender.hp
        trace.append(BattleModelTrace("marker_enter", ordinal, defender_slot))
        if hit.outcome == "dodge":
            # Native iPetDamage is undefined here. Safe modern zero is explicit.
            events.append(BattleModelHitEvent(ordinal, attack, "dodge", defender_slot))
            trace.append(BattleModelTrace("marker_restore", ordinal, defender_slot))
            continue
        actor = current[actor_slot]
        settlement = resolve_battlemodel_marker_settlement(
            defender.reaction, raw_damage=hit.raw_damage, attacker_hp=actor.hp,
            attacker_max_hp=actor.max_hp, defender_hp=defender.hp, defender_max_hp=defender.max_hp,
        )
        # Only NONE subtracts HP in this bounded marker transaction. Use raw
        # subtraction, including overkill, rather than the clamped HP delta.
        hp_damage = hit.raw_damage if settlement.effective_kind == 0 else 0
        ultimate = resolve_battle_ultimate_damage(BattleUltimateDamageInputs(
            hit.raw_damage, hp_damage, defender.hp, defender.max_hp, defender.accumulated_overkill,
        ))
        runtime = defender.status_runtime
        reported = 0 if hit.outcome == "miss" else hit.raw_damage
        trace.append(BattleModelTrace("settlement", ordinal, defender_slot))
        woke = resolve_base_damage_wakeup(
            runtime.status, damage_count_before=runtime.damage_count, damage=reported,
            absorb_or_vanish=settlement.effective_kind in (DAMAGE_REACT_ABSROB, DAMAGE_REACT_VANISH),
        )
        runtime = replace(runtime, status=woke.status_after, damage_count=woke.damage_count_after)
        if woke.wakeup_applied:
            trace.append(BattleModelTrace("wakeup", ordinal, defender_slot))
        ultimate_kind = ultimate.ultimate_kind
        status = None
        if settlement.defender_hp_after <= 0:
            needs_death_draw = hit.outcome == "critical" and defender.kind != "player" and not defender.abio
            death_roll = take("critical_death", 1, 100, ordinal, defender_slot) if needs_death_draw else None
            death = resolve_battle_death_ultimate_override(BattleDeathUltimateInputs(
                ultimate_kind, defender.kind, defender.abio, hit.outcome == "critical",
            ), critical_roll_1_100=death_roll)
            ultimate_kind = death.ultimate_kind
        elif reported > 0 and shape.status_index == 2:
            status_roll = None
            if not active_base_status_names(runtime.status):
                status_roll = take("status", 1, 100, ordinal, defender_slot)
            # Paralysis's shared primitive uses 20-resistance. Other fields
            # are unused placeholders, not guessed participant attributes.
            inputs = BaseStatusAttackInputs("paralysis", 0, 0, False, 0, 0, 0, 0, 0,
                                            defender.paralysis_resistance, 30, 30, 1.0)
            status = resolve_base_status_application(inputs, runtime.status, turn=1, roll_1_100=status_roll)
            runtime = replace(runtime, status=status.status_after)
            if status.command_cleared:
                cleared.add(defender_slot)
                trace.append(BattleModelTrace("command_clear", ordinal, defender_slot))
        current[defender_slot] = replace(
            defender, hp=settlement.defender_hp_after, reaction=settlement.state_after,
            status_runtime=runtime, accumulated_overkill=ultimate.accumulated_overkill_after,
            command_cleared=defender_slot in cleared,
            ultimate_flag=defender.ultimate_flag or ultimate_kind > 0,
        )
        flags[defender_slot] = current[defender_slot].ultimate_flag
        events.append(BattleModelHitEvent(
            ordinal, attack, hit.outcome, defender_slot, reported,
            before - settlement.defender_hp_after, settlement, status, ultimate_kind,
        ))
        trace.append(BattleModelTrace("marker_restore", ordinal, defender_slot))
    if position != len(tape):
        raise ValueError("unused BattleModel RNG tape draw(s)")
    return BattleModelHitLoopResolution(
        living, MappingProxyType(dict(current)), tuple(events), tuple(trace), tuple(consumed), frozenset(cleared),
    )
