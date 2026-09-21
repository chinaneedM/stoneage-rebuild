#!/usr/bin/env python3
"""Stable-descendant first battle-round command/order boundary.

This module reconstructs the command envelope and action-order seam without
inventing player input or enemy AI. Commands are explicit inputs. Later skills and profession systems remain outside this R1 boundary. Stable
base combo formation is reconstructed as an explicit opt-in rewrite after
action sorting; combo damage execution remains a separate seam.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_battle_core_model import (
    ENEMY,
    OTHER,
    PET,
    PLAYER,
    BattleCaptureInputs,
    BattleCaptureResolution,
    BattleEscapeInputs,
    BattleEscapeResolution,
    BattleCounterCheckInputs,
    BattleCounterCheckResolution,
    COUNTER_WEAPON_FIST,
    attribute_adjusted_damage,
    critical_damage,
    critical_per_10000,
    counter_weapon_blocks_counter,
    dodge_per_10000,
    early_action_value,
    early_item_action_value,
    effective_defense_newpower,
    effective_defense_preserved_old,
    guard_damage,
    physical_base_damage,
    resolve_battle_capture_attempt,
    resolve_battle_counter_check,
    resolve_battle_escape_attempt,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


BATTLE_COM_NONE = 0
BATTLE_COM_ATTACK = 1
BATTLE_COM_GUARD = 2
BATTLE_COM_CAPTURE = 3
BATTLE_COM_ESCAPE = 4
BATTLE_COM_PETIN = 5
BATTLE_COM_PETOUT = 6
BATTLE_COM_ITEM = 7
BATTLE_COM_BOOMERANG = 8
BATTLE_COM_COMBO = 9
BATTLE_COM_COMBOEND = 10
BATTLE_COM_WAIT = 11

BASE_COMMAND_CODES = frozenset(
    {
        BATTLE_COM_NONE,
        BATTLE_COM_ATTACK,
        BATTLE_COM_GUARD,
        BATTLE_COM_CAPTURE,
        BATTLE_COM_ESCAPE,
        BATTLE_COM_PETIN,
        BATTLE_COM_PETOUT,
        BATTLE_COM_ITEM,
        BATTLE_COM_BOOMERANG,
        BATTLE_COM_COMBO,
        BATTLE_COM_COMBOEND,
        BATTLE_COM_WAIT,
    }
)

NO_ACTION_COMMANDS = frozenset({BATTLE_COM_NONE, BATTLE_COM_WAIT})


@dataclass(frozen=True)
class BattleCommand:
    """Mirrors the stable COM1/COM2/COM3 command storage boundary."""

    command1: int
    command2: int = -1
    command3: int = 0
    input_complete: bool = True

    def __post_init__(self) -> None:
        command1 = int(self.command1)
        if command1 not in BASE_COMMAND_CODES:
            raise ValueError(
                "R1 accepts only stable base command codes 0..11"
            )
        object.__setattr__(self, "command1", command1)
        object.__setattr__(self, "command2", int(self.command2))
        object.__setattr__(self, "command3", int(self.command3))
        object.__setattr__(self, "input_complete", bool(self.input_complete))

    @property
    def produces_action(self) -> bool:
        return self.command1 not in NO_ACTION_COMMANDS


@dataclass(frozen=True)
class RoundEntry:
    participant: BattleParticipant
    command: BattleCommand
    action_value: int
    source_order: int
    combo_id: int = 0

    @property
    def ready_to_execute(self) -> bool:
        return (
            self.command.input_complete
            and int(self.participant.hp) > 0
        )


@dataclass(frozen=True)
class PreparedBattleRound:
    ordered_entries: tuple[RoundEntry, ...]
    executable_entries: tuple[RoundEntry, ...]
    no_action_entries: tuple[RoundEntry, ...]
    tie_break_was_required: bool


def command_action_value(
    participant: BattleParticipant,
    command: BattleCommand,
    *,
    random_subtract: int,
) -> int:
    """Stable older command-speed profile.

    ITEM has the preserved +15% offset. Other base commands fall through the
    ordinary QUICK+20 minus RAND(0,30%) path in BATTLE_DexCalc.
    """
    if command.command1 == BATTLE_COM_ITEM:
        return early_item_action_value(
            participant.quick,
            int(random_subtract),
        )
    return early_action_value(
        participant.quick,
        int(random_subtract),
    )


def _tie_rank(
    participant_id: str,
    tie_break_order: Sequence[str],
) -> int:
    try:
        return tuple(tie_break_order).index(participant_id)
    except ValueError as exc:
        raise ValueError(
            f"missing explicit tie-break rank for {participant_id}"
        ) from exc


def prepare_battle_round(
    participants: Sequence[BattleParticipant],
    commands: Mapping[str, BattleCommand],
    initiative_random_subtracts: Mapping[str, int],
    *,
    tie_break_order: Sequence[str] | None = None,
) -> PreparedBattleRound:
    """Calculate command-relative action values then sort descending.

    The fixed source uses qsort with comparator pC2->dex - pC1->dex. Its
    ordering for equal values is not a historical contract. If a tie occurs,
    callers must supply an explicit tie_break_order rather than having this
    reconstruction silently invent one.
    """
    entries = []
    seen_ids: set[str] = set()
    for source_order, participant in enumerate(participants):
        participant_id = str(participant.participant_id)
        if participant_id in seen_ids:
            raise ValueError(f"duplicate battle participant id {participant_id}")
        seen_ids.add(participant_id)
        if participant_id not in commands:
            raise KeyError(f"missing command for {participant_id}")
        if participant_id not in initiative_random_subtracts:
            raise KeyError(
                f"missing initiative random result for {participant_id}"
            )
        command = commands[participant_id]
        entries.append(
            RoundEntry(
                participant=participant,
                command=command,
                action_value=command_action_value(
                    participant,
                    command,
                    random_subtract=initiative_random_subtracts[participant_id],
                ),
                source_order=source_order,
            )
        )

    values: dict[int, list[str]] = {}
    for entry in entries:
        values.setdefault(entry.action_value, []).append(
            entry.participant.participant_id
        )
    tied_ids = [
        participant_id
        for ids in values.values()
        if len(ids) > 1
        for participant_id in ids
    ]
    tie_required = bool(tied_ids)

    if tie_required:
        if tie_break_order is None:
            raise ValueError(
                "equal action values require explicit tie_break_order; "
                "fixed-source qsort tie order is unspecified"
            )
        ranking = tuple(str(x) for x in tie_break_order)
        if len(ranking) != len(set(ranking)):
            raise ValueError("tie_break_order contains duplicate ids")
        for participant_id in tied_ids:
            _tie_rank(participant_id, ranking)

        ordered = tuple(
            sorted(
                entries,
                key=lambda entry: (
                    -entry.action_value,
                    _tie_rank(entry.participant.participant_id, ranking)
                    if entry.participant.participant_id in tied_ids
                    else entry.source_order,
                ),
            )
        )
    else:
        ordered = tuple(
            sorted(entries, key=lambda entry: -entry.action_value)
        )

    executable = tuple(
        entry
        for entry in ordered
        if entry.ready_to_execute
    )
    no_action = tuple(
        entry
        for entry in executable
        if not entry.command.produces_action
    )
    return PreparedBattleRound(
        ordered_entries=ordered,
        executable_entries=executable,
        no_action_entries=no_action,
        tie_break_was_required=tie_required,
    )


def apply_base_combo_rewrite(
    prepared: PreparedBattleRound,
    profiles: Mapping[str, "BattleCombatProfile"],
    start_rolls_1_100: Mapping[str, int] | None,
) -> PreparedBattleRound:
    """Mirror stable ComboCheck() on the already action-sorted entry list.

    This is the common base branch only: enemy starters use 20 percent,
    non-enemy starters use 50 percent, and later _ITEM_ADDCOMBO equipment
    bonuses are excluded. A successful starter consumes its own roll even when
    no later actor ultimately joins it. Actors that join an active group do not
    consume a start roll.
    """
    if start_rolls_1_100 is None:
        return prepared

    entries=list(prepared.ordered_entries)
    start: int | None=None
    old_target=-3
    old_side: str | None=None
    next_combo_id=1

    def with_combo(entry: RoundEntry, combo_id: int) -> RoundEntry:
        return RoundEntry(
            participant=entry.participant,
            command=BattleCommand(
                BATTLE_COM_COMBO,
                command2=entry.command.command2,
                command3=entry.command.command3,
                input_complete=entry.command.input_complete,
            ),
            action_value=entry.action_value,
            source_order=entry.source_order,
            combo_id=int(combo_id),
        )

    for i in range(len(entries)):
        entry=entries[i]
        participant=entry.participant
        participant_id=str(participant.participant_id)
        if participant_id not in profiles:
            raise KeyError(f"missing combat profile for {participant_id}")
        command=entry.command
        side=str(participant.side)
        movable=int(participant.hp)>0
        throwing=counter_weapon_blocks_counter(
            profiles[participant_id].counter_weapon_type
        )

        if start is not None:
            if (
                command.command1 != BATTLE_COM_ATTACK
                or int(command.command2) != int(old_target)
                or side != old_side
                or throwing
                or not movable
            ):
                start=None
                old_side=side
            else:
                group_id=next_combo_id
                entries[i]=with_combo(entry,group_id)
                entries[start]=with_combo(entries[start],group_id)

        if start is None:
            if (
                command.command1 == BATTLE_COM_ATTACK
                and not throwing
                and movable
            ):
                if participant_id not in start_rolls_1_100:
                    raise KeyError(
                        f"missing combo start roll for eligible actor {participant_id}"
                    )
                roll=_validated_roll(
                    start_rolls_1_100[participant_id],
                    1,
                    100,
                    "combo_start_roll_1_100",
                )
                per=20 if participant.kind=="enemy" else 50
                if roll <= per:
                    start=i
                    old_target=int(command.command2)
                    old_side=side
                    next_combo_id+=1

    ordered=tuple(entries)
    executable=tuple(entry for entry in ordered if entry.ready_to_execute)
    no_action=tuple(
        entry for entry in executable if not entry.command.produces_action
    )
    return PreparedBattleRound(
        ordered_entries=ordered,
        executable_entries=executable,
        no_action_entries=no_action,
        tie_break_was_required=prepared.tie_break_was_required,
    )


SIDE_OFFSET = 10
BATTLE_SLOT_COUNT = 20
ORDINARY_RESOLUTION_COMMANDS = frozenset(
    {
        BATTLE_COM_ATTACK,
        BATTLE_COM_GUARD,
        BATTLE_COM_CAPTURE,
        BATTLE_COM_ESCAPE,
        BATTLE_COM_WAIT,
    }
)


@dataclass(frozen=True)
class BattleCombatProfile:
    """Explicit fixed-stat/element inputs not inferred from display labels."""

    fixed_dex: int
    fixed_luck: int
    earth: int
    water: int
    fire: int
    wind: int
    weapon_critical: int = 0
    counter_weapon_type: str = COUNTER_WEAPON_FIST

    @property
    def elements(self) -> tuple[int, int, int, int]:
        return (
            int(self.earth),
            int(self.water),
            int(self.fire),
            int(self.wind),
        )


@dataclass(frozen=True)
class OrdinaryAttackRolls:
    """All RAND results consumed by one ordinary single-hit attack path."""

    critical_roll_1_10000: int
    damage_roll: int
    dodge_roll_1_10000: int | None = None
    guard_roll_1_100: int | None = None
    minimum_damage_roll_0_1: int | None = None
    retarget_roll: int | None = None


@dataclass(frozen=True)
class CounterAttemptRolls:
    """Explicit RNG consumed by one BATTLE_Counter() attempt."""

    counter_check_roll_1_10000: int | None
    attack_rolls: OrdinaryAttackRolls | None = None


@dataclass(frozen=True)
class OrdinaryCaptureRolls:
    """RAND values consumed by TargetAdjust + BATTLE_CaptureCheck."""
    capture_roll_1_100: int | None
    retarget_roll: int | None = None


@dataclass(frozen=True)
class OrdinaryCaptureContext:
    """Non-random player/target state not carried by BattleParticipant."""
    attacker_charm: int
    pick_all_pet: bool = False
    temporary_capture_modifier: int = 0
    target_sleep_by_participant_id: Mapping[str,int] | None = None
    required_items_present_by_participant_id: Mapping[str,bool] | None = None
    occupied_pet_slots: tuple[int,...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self,'attacker_charm',int(self.attacker_charm))
        object.__setattr__(
            self,'temporary_capture_modifier',int(self.temporary_capture_modifier)
        )
        object.__setattr__(
            self,
            'target_sleep_by_participant_id',
            MappingProxyType({
                str(key):int(value)
                for key,value in (self.target_sleep_by_participant_id or {}).items()
            }),
        )
        object.__setattr__(
            self,
            'required_items_present_by_participant_id',
            MappingProxyType({
                str(key):bool(value)
                for key,value in (
                    self.required_items_present_by_participant_id or {}
                ).items()
            }),
        )
        object.__setattr__(
            self,
            'occupied_pet_slots',
            tuple(int(slot) for slot in self.occupied_pet_slots),
        )


@dataclass(frozen=True)
class OrdinaryEscapeRolls:
    """RAND(1,100) consumed by BATTLE_EscapeCheck outside PvP."""
    escape_roll_1_100: int | None


@dataclass(frozen=True)
class OrdinaryEscapeContext:
    """Non-random source state needed by BATTLE_Escape/BATTLE_EscapeCheck."""
    stored_escape_count_before: int
    actor_rare: int = 0
    opponent_abio_by_participant_id: Mapping[str,bool] | None = None
    pvp: bool = False
    forced_exit: bool = False

    def __post_init__(self) -> None:
        count=int(self.stored_escape_count_before)
        if count < 0:
            raise ValueError("stored escape count cannot be negative")
        object.__setattr__(self,'stored_escape_count_before',count)
        object.__setattr__(self,'actor_rare',int(self.actor_rare))
        object.__setattr__(
            self,
            'opponent_abio_by_participant_id',
            MappingProxyType({
                str(pid):bool(value)
                for pid,value in (
                    self.opponent_abio_by_participant_id or {}
                ).items()
            }),
        )


@dataclass(frozen=True)
class OrdinaryRoundEvent:
    participant_id: str
    slot: int
    command1: int
    action_value: int
    result: str
    original_target_slot: int | None = None
    resolved_target_slot: int | None = None
    retargeted: bool = False
    critical: bool = False
    damage: int = 0
    target_hp_before: int | None = None
    target_hp_after: int | None = None
    capture_resolution: BattleCaptureResolution | None = None
    escape_resolution: BattleEscapeResolution | None = None
    is_counter: bool = False
    counter_attempt: int | None = None
    counter_check_resolution: BattleCounterCheckResolution | None = None


@dataclass(frozen=True)
class ResolvedOrdinaryRound:
    events: tuple[OrdinaryRoundEvent, ...]
    hp_by_participant_id: Mapping[str, int]
    hp_by_slot: Mapping[int, int]
    action_order: tuple[str, ...]
    exited_participant_ids: tuple[str, ...] = ()
    escaped_participant_ids: tuple[str, ...] = ()


def _participant_battle_kind(participant: BattleParticipant) -> str:
    if participant.kind == "player":
        return PLAYER
    if participant.kind == "pet":
        return PET
    if participant.kind == "enemy":
        return ENEMY
    return OTHER


def _source_luck(
    participant: BattleParticipant,
    profile: BattleCombatProfile,
) -> int:
    # The stable dodge/critical paths read FIXLUCK only for player actors.
    return int(profile.fixed_luck) if participant.kind == "player" else 0


def _validated_roll(value: int | None, lo: int, hi: int, name: str) -> int:
    if value is None:
        raise ValueError(f"{name} is required on this execution path")
    value = int(value)
    if not lo <= value <= hi:
        raise ValueError(f"{name} must be in {lo}..{hi}")
    return value


def _slot_side(slot: int) -> int:
    return 0 if int(slot) < SIDE_OFFSET else 1


def _effective_defense_for_round(
    participant: BattleParticipant,
    defense_profile: str,
) -> float:
    if defense_profile == "newpower_70pct":
        return effective_defense_newpower(participant.defense, stone=False)
    if defense_profile == "preserved_old_mixed":
        if participant.fixed_vital is None:
            raise ValueError(
                "preserved_old_mixed requires explicit defender.fixed_vital"
            )
        return effective_defense_preserved_old(
            participant.defense,
            participant.quick,
            participant.fixed_vital,
            stone=False,
        )
    raise ValueError(f"unknown defense profile: {defense_profile}")


def _resolve_counter_chain(
    *,
    initial_attacker_slot: int,
    initial_defender_slot: int,
    by_slot: Mapping[int, BattleParticipant],
    hp_by_slot: dict[int, int],
    hp_by_id: dict[str, int],
    profiles: Mapping[str, BattleCombatProfile],
    command_by_slot: Mapping[int, BattleCommand],
    action_value_by_slot: Mapping[int, int],
    counter_rolls: Sequence[CounterAttemptRolls],
    counter_abio_by_participant_id: Mapping[str, bool],
    defense_profile: str,
    field_attr: str,
    field_power: int,
) -> tuple[OrdinaryRoundEvent, ...]:
    """Execute the stable base alternating BATTLE_Counter() loop.

    This is deliberately limited to the already-recovered status-free,
    no-guardian/no-reaction ordinary physical seam. The source permits at most
    five alternating attempts after a main attack's continuation flag remains
    true. Each successful counter uses BATTLE_AttackSeq-style dodge/critical/
    damage resolution, then scales positive damage to 75 percent.
    """
    supplied=tuple(counter_rolls)
    if len(supplied) > 5:
        raise ValueError("stable counter chain accepts at most five attempts")

    resolved: list[OrdinaryRoundEvent] = []
    for attempt_index in range(5):
        actor_slot=(
            int(initial_defender_slot)
            if attempt_index % 2 == 0
            else int(initial_attacker_slot)
        )
        target_slot=(
            int(initial_attacker_slot)
            if attempt_index % 2 == 0
            else int(initial_defender_slot)
        )
        actor=by_slot[actor_slot]
        target=by_slot[target_slot]
        actor_id=str(actor.participant_id)
        target_id=str(target.participant_id)
        action_value=int(action_value_by_slot[actor_slot])
        before=int(hp_by_slot[target_slot])

        if int(hp_by_slot[actor_slot]) <= 0 or before <= 0:
            resolved.append(
                OrdinaryRoundEvent(
                    actor_id,
                    actor_slot,
                    BATTLE_COM_ATTACK,
                    action_value,
                    "counter_ineligible_dead",
                    original_target_slot=target_slot,
                    resolved_target_slot=target_slot,
                    target_hp_before=before,
                    target_hp_after=before,
                    is_counter=True,
                    counter_attempt=attempt_index + 1,
                )
            )
            break

        if command_by_slot[actor_slot].command1 != BATTLE_COM_ATTACK:
            resolved.append(
                OrdinaryRoundEvent(
                    actor_id,
                    actor_slot,
                    BATTLE_COM_ATTACK,
                    action_value,
                    "counter_ineligible_command",
                    original_target_slot=target_slot,
                    resolved_target_slot=target_slot,
                    target_hp_before=before,
                    target_hp_after=before,
                    is_counter=True,
                    counter_attempt=attempt_index + 1,
                )
            )
            break

        if bool(counter_abio_by_participant_id.get(actor_id,False)):
            resolved.append(
                OrdinaryRoundEvent(
                    actor_id,
                    actor_slot,
                    BATTLE_COM_ATTACK,
                    action_value,
                    "counter_ineligible_abio",
                    original_target_slot=target_slot,
                    resolved_target_slot=target_slot,
                    target_hp_before=before,
                    target_hp_after=before,
                    is_counter=True,
                    counter_attempt=attempt_index + 1,
                )
            )
            break

        if attempt_index >= len(supplied):
            raise KeyError(
                "missing explicit counter attempt rolls for "
                f"{actor_id} at chain attempt {attempt_index + 1}"
            )
        attempt=supplied[attempt_index]
        actor_profile=profiles[actor_id]
        target_profile=profiles[target_id]
        check=resolve_battle_counter_check(
            BattleCounterCheckInputs(
                attacker_kind=_participant_battle_kind(actor),
                defender_kind=_participant_battle_kind(target),
                attacker_fixed_dex=int(actor_profile.fixed_dex),
                defender_fixed_dex=int(target_profile.fixed_dex),
                attacker_fixed_luck=_source_luck(actor,actor_profile),
                attacker_weapon_type=str(actor_profile.counter_weapon_type),
                defender_weapon_type=str(target_profile.counter_weapon_type),
            ),
            roll_1_10000=attempt.counter_check_roll_1_10000,
        )
        if not check.success:
            resolved.append(
                OrdinaryRoundEvent(
                    actor_id,
                    actor_slot,
                    BATTLE_COM_ATTACK,
                    action_value,
                    (
                        "counter_blocked_weapon"
                        if check.blocked_by_throwing_weapon
                        else "counter_check_failed"
                    ),
                    original_target_slot=target_slot,
                    resolved_target_slot=target_slot,
                    target_hp_before=before,
                    target_hp_after=before,
                    is_counter=True,
                    counter_attempt=attempt_index + 1,
                    counter_check_resolution=check,
                )
            )
            break

        rolls=attempt.attack_rolls
        if rolls is None:
            raise ValueError(
                f"counter attack rolls required after successful check for {actor_id}"
            )

        target_guarding=(
            command_by_slot[target_slot].command1 == BATTLE_COM_GUARD
        )
        if not target_guarding:
            dodge_roll=_validated_roll(
                rolls.dodge_roll_1_10000,
                1,
                10000,
                "counter dodge_roll_1_10000",
            )
            dodge_probability=dodge_per_10000(
                actor_profile.fixed_dex,
                target_profile.fixed_dex,
                defender_luck=_source_luck(target,target_profile),
                attacker_type=_participant_battle_kind(actor),
                defender_type=_participant_battle_kind(target),
            )
            if dodge_roll <= dodge_probability:
                resolved.append(
                    OrdinaryRoundEvent(
                        actor_id,
                        actor_slot,
                        BATTLE_COM_ATTACK,
                        action_value,
                        "counter_dodge",
                        original_target_slot=target_slot,
                        resolved_target_slot=target_slot,
                        target_hp_before=before,
                        target_hp_after=before,
                        is_counter=True,
                        counter_attempt=attempt_index + 1,
                        counter_check_resolution=check,
                    )
                )
                continue

        critical_roll=_validated_roll(
            rolls.critical_roll_1_10000,
            1,
            10000,
            "counter critical_roll_1_10000",
        )
        critical_probability=critical_per_10000(
            actor_profile.fixed_dex,
            target_profile.fixed_dex,
            attacker_luck=_source_luck(actor,actor_profile),
            weapon_critical=int(actor_profile.weapon_critical),
            attacker_type=_participant_battle_kind(actor),
            defender_type=_participant_battle_kind(target),
        )
        is_critical=critical_roll < critical_probability

        base_damage=physical_base_damage(
            actor.attack,
            _effective_defense_for_round(target,defense_profile),
            int(rolls.damage_roll),
        )
        damage=attribute_adjusted_damage(
            base_damage,
            actor_profile.elements,
            target_profile.elements,
            field_attr=field_attr,
            field_power=field_power,
        )
        if is_critical:
            damage=critical_damage(
                damage,
                target.defense,
                actor.level,
                target.level,
            )

        if target_guarding:
            guard_roll=_validated_roll(
                rolls.guard_roll_1_100,
                1,
                100,
                "counter guard_roll_1_100",
            )
            damage=guard_damage(damage,guard_roll)

        if damage < 1:
            damage=_validated_roll(
                rolls.minimum_damage_roll_0_1,
                0,
                1,
                "counter minimum_damage_roll_0_1",
            )

        if damage == 0:
            attack_seq_result=(
                "counter_allguard" if target_guarding else "counter_miss"
            )
        else:
            attack_seq_result=(
                "counter_critical" if is_critical else "counter_normal"
            )
            damage=max(1,int(float(damage)*0.75))

        after=max(0,before-int(damage))
        hp_by_slot[target_slot]=after
        hp_by_id[target_id]=after
        resolved.append(
            OrdinaryRoundEvent(
                actor_id,
                actor_slot,
                BATTLE_COM_ATTACK,
                action_value,
                attack_seq_result,
                original_target_slot=target_slot,
                resolved_target_slot=target_slot,
                critical=(attack_seq_result=="counter_critical"),
                damage=int(damage),
                target_hp_before=before,
                target_hp_after=after,
                is_counter=True,
                counter_attempt=attempt_index + 1,
                counter_check_resolution=check,
            )
        )

        if attack_seq_result in {"counter_miss","counter_critical"} or after <= 0:
            break

    return tuple(resolved)


def _build_slot_maps(
    prepared: PreparedBattleRound,
    slots: Mapping[str, int],
) -> tuple[dict[int, BattleParticipant], dict[str, int]]:
    by_slot: dict[int, BattleParticipant] = {}
    normalized: dict[str, int] = {}
    for entry in prepared.ordered_entries:
        participant = entry.participant
        participant_id = str(participant.participant_id)
        if participant_id not in slots:
            raise KeyError(f"missing battle slot for {participant_id}")
        slot = int(slots[participant_id])
        if not 0 <= slot < BATTLE_SLOT_COUNT:
            raise ValueError("battle slots must be in 0..19")
        expected_side = "player" if slot < SIDE_OFFSET else "enemy"
        if participant.side != expected_side:
            raise ValueError(
                f"slot {slot} belongs to {expected_side} side, "
                f"not {participant.side}"
            )
        if slot in by_slot:
            raise ValueError(f"duplicate occupied battle slot {slot}")
        by_slot[slot] = participant
        normalized[participant_id] = slot
    return by_slot, normalized


def _retarget_slot(
    actor_slot: int,
    by_slot: Mapping[int, BattleParticipant],
    hp_by_slot: Mapping[int, int],
    roll: int | None,
    *,
    excluded_slots: Sequence[int] = (),
) -> int | None:
    target_side = 1 - _slot_side(actor_slot)
    excluded={int(slot) for slot in excluded_slots}
    candidates = tuple(
        slot
        for slot in range(
            target_side * SIDE_OFFSET,
            target_side * SIDE_OFFSET + SIDE_OFFSET,
        )
        if (
            slot in by_slot
            and slot not in excluded
            and int(hp_by_slot.get(slot, 0)) > 0
        )
    )
    if not candidates:
        return None
    index = _validated_roll(
        roll,
        0,
        len(candidates) - 1,
        "retarget_roll",
    )
    return candidates[index]


def resolve_ordinary_round(
    prepared: PreparedBattleRound,
    *,
    slots: Mapping[str, int],
    profiles: Mapping[str, BattleCombatProfile],
    attack_rolls: Mapping[str, OrdinaryAttackRolls],
    defense_profile: str,
    capture_contexts: Mapping[str, OrdinaryCaptureContext] | None = None,
    capture_rolls: Mapping[str, OrdinaryCaptureRolls] | None = None,
    escape_contexts: Mapping[str, OrdinaryEscapeContext] | None = None,
    escape_rolls: Mapping[str, OrdinaryEscapeRolls] | None = None,
    counter_rolls_by_attack_id: Mapping[
        str,Sequence[CounterAttemptRolls]
    ] | None = None,
    counter_abio_by_participant_id: Mapping[str,bool] | None = None,
    field_attr: str = "none",
    field_power: int = 0,
) -> ResolvedOrdinaryRound:
    """Execute the status-free attack/guard/capture/escape/wait battle seam.

    Passing counter_rolls_by_attack_id enables the recovered base counter loop;
    leaving it as None preserves the earlier no-counter R1 boundary. Guard
    stance is taken from the submitted command set before action sorting,
    matching BATTLE_AttackSeq's inspection of the defender's COM1 rather than
    requiring the guard actor's own execution turn to occur first.
    """
    for entry in prepared.ordered_entries:
        if entry.command.command1 not in ORDINARY_RESOLUTION_COMMANDS:
            raise ValueError(
                "ordinary resolver accepts only ATTACK/GUARD/CAPTURE/ESCAPE/WAIT commands"
            )

    by_slot, slot_by_id = _build_slot_maps(prepared, slots)
    hp_by_slot = {
        slot: max(0, int(participant.hp))
        for slot, participant in by_slot.items()
    }
    hp_by_id = {
        participant.participant_id: hp_by_slot[slot]
        for slot, participant in by_slot.items()
    }

    for participant_id in slot_by_id:
        if participant_id not in profiles:
            raise KeyError(f"missing combat profile for {participant_id}")

    guarding = {
        slot_by_id[entry.participant.participant_id]
        for entry in prepared.ordered_entries
        if entry.command.command1 == BATTLE_COM_GUARD
        and int(entry.participant.hp) > 0
        and entry.command.input_complete
    }

    events: list[OrdinaryRoundEvent] = []
    exited_slots: set[int] = set()
    exited_ids: list[str] = []
    capture_contexts=dict(capture_contexts or {})
    capture_rolls=dict(capture_rolls or {})
    escape_contexts=dict(escape_contexts or {})
    escape_rolls=dict(escape_rolls or {})
    normalized_counter_rolls=(
        None
        if counter_rolls_by_attack_id is None
        else {
            str(participant_id):tuple(rolls)
            for participant_id,rolls in counter_rolls_by_attack_id.items()
        }
    )
    normalized_counter_abio={
        str(participant_id):bool(value)
        for participant_id,value in (
            counter_abio_by_participant_id or {}
        ).items()
    }
    command_by_slot={
        slot_by_id[entry.participant.participant_id]:entry.command
        for entry in prepared.ordered_entries
    }
    action_value_by_slot={
        slot_by_id[entry.participant.participant_id]:int(entry.action_value)
        for entry in prepared.ordered_entries
    }
    escaped_ids: list[str] = []

    def append_counter_chain(
        main_actor_id: str,
        main_actor_slot: int,
        target_slot: int,
    ) -> None:
        if normalized_counter_rolls is None:
            return
        events.extend(
            _resolve_counter_chain(
                initial_attacker_slot=int(main_actor_slot),
                initial_defender_slot=int(target_slot),
                by_slot=by_slot,
                hp_by_slot=hp_by_slot,
                hp_by_id=hp_by_id,
                profiles=profiles,
                command_by_slot=command_by_slot,
                action_value_by_slot=action_value_by_slot,
                counter_rolls=normalized_counter_rolls.get(
                    str(main_actor_id),()
                ),
                counter_abio_by_participant_id=normalized_counter_abio,
                defense_profile=defense_profile,
                field_attr=field_attr,
                field_power=field_power,
            )
        )

    for entry in prepared.ordered_entries:
        participant = entry.participant
        participant_id = participant.participant_id
        slot = slot_by_id[participant_id]

        if not entry.command.input_complete:
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    entry.command.command1,
                    entry.action_value,
                    "skipped_incomplete",
                )
            )
            continue
        if hp_by_slot[slot] <= 0:
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    entry.command.command1,
                    entry.action_value,
                    "skipped_dead",
                )
            )
            continue
        if slot in exited_slots:
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    entry.command.command1,
                    entry.action_value,
                    "skipped_exited",
                )
            )
            continue

        if entry.command.command1 == BATTLE_COM_WAIT:
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_WAIT,
                    entry.action_value,
                    "wait",
                )
            )
            continue

        if entry.command.command1 == BATTLE_COM_GUARD:
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_GUARD,
                    entry.action_value,
                    "guard",
                )
            )
            continue

        if entry.command.command1 == BATTLE_COM_ESCAPE:
            # Stable BATTLE_Command ignores ESCAPE for CHAR_TYPEPET.
            if participant.kind == "pet":
                events.append(
                    OrdinaryRoundEvent(
                        participant_id,
                        slot,
                        BATTLE_COM_ESCAPE,
                        entry.action_value,
                        "escape_ignored_pet",
                    )
                )
                continue
            if participant_id not in escape_contexts:
                raise KeyError(f"missing escape context for {participant_id}")
            if participant_id not in escape_rolls:
                raise KeyError(f"missing escape rolls for {participant_id}")
            context=escape_contexts[participant_id]
            esc_rolls=escape_rolls[participant_id]
            opponent_side=1-_slot_side(slot)
            opponents=tuple(
                by_slot[other_slot]
                for other_slot in sorted(by_slot)
                if (
                    _slot_side(other_slot)==opponent_side
                    and other_slot not in exited_slots
                )
            )
            opponent_levels=tuple(int(opponent.level) for opponent in opponents)
            opponent_abio=tuple(
                bool(
                    context.opponent_abio_by_participant_id.get(
                        str(opponent.participant_id),
                        False,
                    )
                )
                for opponent in opponents
            )
            actor_profile=profiles[participant_id]
            resolution=resolve_battle_escape_attempt(
                BattleEscapeInputs(
                    actor_level=int(participant.level),
                    actor_kind=str(participant.kind),
                    actor_fixed_luck=int(actor_profile.fixed_luck),
                    actor_rare=int(context.actor_rare),
                    stored_escape_count_before=int(
                        context.stored_escape_count_before
                    ),
                    opponent_levels=opponent_levels,
                    opponent_abio_flags=opponent_abio,
                    pvp=bool(context.pvp),
                    forced_exit=bool(context.forced_exit),
                ),
                roll_1_100=esc_rolls.escape_roll_1_100,
            )
            if resolution.exits_battle:
                exited_slots.add(slot)
                escaped_ids.append(str(participant_id))
                # BATTLE_Exit(player) also clears the active pet battle entry.
                if participant.side=="player" and participant.kind=="player":
                    for other_slot,other in by_slot.items():
                        if (
                            other.side=="player"
                            and other.kind=="pet"
                            and other_slot not in exited_slots
                        ):
                            exited_slots.add(other_slot)
                            escaped_ids.append(str(other.participant_id))
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_ESCAPE,
                    entry.action_value,
                    (
                        "escape_success"
                        if resolution.exits_battle
                        else "escape_failed"
                    ),
                    escape_resolution=resolution,
                )
            )
            continue

        if entry.command.command1 == BATTLE_COM_CAPTURE:
            if participant_id not in capture_contexts:
                raise KeyError(
                    f"missing capture context for {participant_id}"
                )
            if participant_id not in capture_rolls:
                raise KeyError(
                    f"missing capture rolls for {participant_id}"
                )
            context=capture_contexts[participant_id]
            cap_rolls=capture_rolls[participant_id]
            original_target=int(entry.command.command2)
            target=original_target
            retargeted=False
            target_alive=(
                target in by_slot
                and target not in exited_slots
                and int(hp_by_slot.get(target,0))>0
            )
            if not target_alive:
                target=_retarget_slot(
                    slot,
                    by_slot,
                    hp_by_slot,
                    cap_rolls.retarget_roll,
                    excluded_slots=exited_slots,
                )
                retargeted=True
            if target is None:
                events.append(
                    OrdinaryRoundEvent(
                        participant_id,
                        slot,
                        BATTLE_COM_CAPTURE,
                        entry.action_value,
                        "no_target",
                        original_target_slot=original_target,
                        retargeted=True,
                    )
                )
                continue
            defender=by_slot[target]
            defender_id=str(defender.participant_id)
            if defender.capturable is None:
                raise ValueError(
                    f"capture target {defender_id} lacks PETFLG provenance"
                )
            if defender.capture_default is None:
                raise ValueError(
                    f"capture target {defender_id} lacks enemybase GET provenance"
                )
            attacker_profile=profiles[participant_id]
            defender_profile=profiles[defender_id]
            inputs=BattleCaptureInputs(
                attacker_level=int(participant.level),
                attacker_charm=int(context.attacker_charm),
                attacker_fixed_dex=int(attacker_profile.fixed_dex),
                attacker_fixed_luck=int(attacker_profile.fixed_luck),
                target_level=int(defender.level),
                target_hp=int(hp_by_slot[target]),
                target_max_hp=int(defender.max_hp),
                target_fixed_dex=int(defender_profile.fixed_dex),
                target_capture_default=int(defender.capture_default),
                target_is_enemy=(defender.kind=="enemy"),
                target_capturable=bool(defender.capturable),
                pick_all_pet=bool(context.pick_all_pet),
                temporary_capture_modifier=int(
                    context.temporary_capture_modifier
                ),
                target_sleep=int(
                    context.target_sleep_by_participant_id.get(defender_id,0)
                ),
                required_items_present=bool(
                    context.required_items_present_by_participant_id.get(
                        defender_id,True
                    )
                ),
                occupied_pet_slots=context.occupied_pet_slots,
            )
            resolution=resolve_battle_capture_attempt(
                inputs,
                roll_1_100=cap_rolls.capture_roll_1_100,
            )
            before=int(hp_by_slot[target])
            if resolution.success:
                exited_slots.add(target)
                exited_ids.append(defender_id)
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_CAPTURE,
                    entry.action_value,
                    (
                        "capture_success"
                        if resolution.success
                        else str(resolution.failure_reason)
                    ),
                    original_target_slot=original_target,
                    resolved_target_slot=target,
                    retargeted=retargeted,
                    target_hp_before=before,
                    target_hp_after=before,
                    capture_resolution=resolution,
                )
            )
            continue

        rolls = attack_rolls.get(participant_id)
        if rolls is None:
            raise KeyError(f"missing ordinary attack rolls for {participant_id}")

        original_target = int(entry.command.command2)
        target = original_target
        retargeted = False

        target_alive = (
            target in by_slot
            and target not in exited_slots
            and int(hp_by_slot.get(target, 0)) > 0
        )
        if target_alive and _slot_side(target) == _slot_side(slot):
            raise ValueError(
                "same-side ordinary attacks are outside the status-free R1 seam"
            )
        if not target_alive:
            target = _retarget_slot(
                slot,
                by_slot,
                hp_by_slot,
                rolls.retarget_roll,
                excluded_slots=exited_slots,
            )
            retargeted = True

        if target is None:
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_ATTACK,
                    entry.action_value,
                    "no_target",
                    original_target_slot=original_target,
                    retargeted=True,
                )
            )
            continue

        defender = by_slot[target]
        defender_id = defender.participant_id
        attacker_profile = profiles[participant_id]
        defender_profile = profiles[defender_id]
        before = hp_by_slot[target]

        # BATTLE_DuckCheck immediately returns FALSE for a guarding defender.
        if target not in guarding:
            dodge_roll = _validated_roll(
                rolls.dodge_roll_1_10000,
                1,
                10000,
                "dodge_roll_1_10000",
            )
            dodge_probability = dodge_per_10000(
                attacker_profile.fixed_dex,
                defender_profile.fixed_dex,
                defender_luck=_source_luck(defender, defender_profile),
                attacker_type=_participant_battle_kind(participant),
                defender_type=_participant_battle_kind(defender),
            )
            if dodge_roll <= dodge_probability:
                events.append(
                    OrdinaryRoundEvent(
                        participant_id,
                        slot,
                        BATTLE_COM_ATTACK,
                        entry.action_value,
                        "dodge",
                        original_target_slot=original_target,
                        resolved_target_slot=target,
                        retargeted=retargeted,
                        target_hp_before=before,
                        target_hp_after=before,
                    )
                )
                append_counter_chain(participant_id,slot,target)
                continue

        critical_roll = _validated_roll(
            rolls.critical_roll_1_10000,
            1,
            10000,
            "critical_roll_1_10000",
        )
        critical_probability = critical_per_10000(
            attacker_profile.fixed_dex,
            defender_profile.fixed_dex,
            attacker_luck=_source_luck(participant, attacker_profile),
            weapon_critical=int(attacker_profile.weapon_critical),
            attacker_type=_participant_battle_kind(participant),
            defender_type=_participant_battle_kind(defender),
        )
        # Stable source uses RAND(1,10000) < per for criticals.
        is_critical = critical_roll < critical_probability

        base_damage = physical_base_damage(
            participant.attack,
            _effective_defense_for_round(defender, defense_profile),
            int(rolls.damage_roll),
        )
        damage = attribute_adjusted_damage(
            base_damage,
            attacker_profile.elements,
            defender_profile.elements,
            field_attr=field_attr,
            field_power=field_power,
        )
        if is_critical:
            damage = critical_damage(
                damage,
                defender.defense,
                participant.level,
                defender.level,
            )

        if target in guarding:
            guard_roll = _validated_roll(
                rolls.guard_roll_1_100,
                1,
                100,
                "guard_roll_1_100",
            )
            damage = guard_damage(damage, guard_roll)

        if damage < 1:
            damage = _validated_roll(
                rolls.minimum_damage_roll_0_1,
                0,
                1,
                "minimum_damage_roll_0_1",
            )

        if damage == 0:
            result = "allguard" if target in guarding else "miss"
        else:
            result = "critical" if is_critical else "normal"

        after = max(0, before - int(damage))
        hp_by_slot[target] = after
        hp_by_id[defender_id] = after
        events.append(
            OrdinaryRoundEvent(
                participant_id,
                slot,
                BATTLE_COM_ATTACK,
                entry.action_value,
                result,
                original_target_slot=original_target,
                resolved_target_slot=target,
                retargeted=retargeted,
                critical=is_critical,
                damage=int(damage),
                target_hp_before=before,
                target_hp_after=after,
            )
        )
        if result != "critical" and target not in guarding and after > 0:
            append_counter_chain(participant_id,slot,target)

    return ResolvedOrdinaryRound(
        events=tuple(events),
        hp_by_participant_id=MappingProxyType(dict(hp_by_id)),
        hp_by_slot=MappingProxyType(dict(hp_by_slot)),
        action_order=tuple(
            entry.participant.participant_id
            for entry in prepared.ordered_entries
        ),
        exited_participant_ids=tuple(exited_ids),
        escaped_participant_ids=tuple(escaped_ids),
    )
