#!/usr/bin/env python3
"""Stable-descendant first battle-round command/order boundary.

This module reconstructs the command envelope and action-order seam without
inventing player input or enemy AI. Commands are explicit inputs. Later skills,
combo rewriting, profession systems and full action execution remain outside
this R1 boundary.
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
    attribute_adjusted_damage,
    critical_damage,
    critical_per_10000,
    dodge_per_10000,
    early_action_value,
    early_item_action_value,
    effective_defense_newpower,
    effective_defense_preserved_old,
    guard_damage,
    physical_base_damage,
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


SIDE_OFFSET = 10
BATTLE_SLOT_COUNT = 20
ORDINARY_RESOLUTION_COMMANDS = frozenset(
    {BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_WAIT}
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


@dataclass(frozen=True)
class ResolvedOrdinaryRound:
    events: tuple[OrdinaryRoundEvent, ...]
    hp_by_participant_id: Mapping[str, int]
    hp_by_slot: Mapping[int, int]
    action_order: tuple[str, ...]


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
) -> int | None:
    target_side = 1 - _slot_side(actor_slot)
    candidates = tuple(
        slot
        for slot in range(
            target_side * SIDE_OFFSET,
            target_side * SIDE_OFFSET + SIDE_OFFSET,
        )
        if slot in by_slot and int(hp_by_slot.get(slot, 0)) > 0
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
    field_attr: str = "none",
    field_power: int = 0,
) -> ResolvedOrdinaryRound:
    """Execute the first status-free attack/guard/wait battle seam.

    Guard stance is taken from the submitted command set before action sorting,
    matching BATTLE_AttackSeq's inspection of the defender's COM1 rather than
    requiring the guard actor's own execution turn to occur first.
    """
    for entry in prepared.ordered_entries:
        if entry.command.command1 not in ORDINARY_RESOLUTION_COMMANDS:
            raise ValueError(
                "ordinary resolver accepts only ATTACK/GUARD/WAIT commands"
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

        rolls = attack_rolls.get(participant_id)
        if rolls is None:
            raise KeyError(f"missing ordinary attack rolls for {participant_id}")

        original_target = int(entry.command.command2)
        target = original_target
        retargeted = False

        target_alive = (
            target in by_slot
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

    return ResolvedOrdinaryRound(
        events=tuple(events),
        hp_by_participant_id=MappingProxyType(dict(hp_by_id)),
        hp_by_slot=MappingProxyType(dict(hp_by_slot)),
        action_order=tuple(
            entry.participant.participant_id
            for entry in prepared.ordered_entries
        ),
    )
