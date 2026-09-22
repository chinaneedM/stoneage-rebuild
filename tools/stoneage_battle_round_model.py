#!/usr/bin/env python3
"""Stable-descendant first battle-round command/order boundary.

This module reconstructs the command envelope and action-order seam without
inventing player input or enemy AI. Commands are explicit inputs. Later skills and profession systems remain outside this R1 boundary. Stable
base combo formation is reconstructed as an explicit opt-in rewrite after
action sorting; combo damage execution remains a separate seam.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
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
from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_REFLEC,
    BaseComboMemberDamageReactResolution,
    BaseDamageReactResolution,
    BaseDamageReactState,
    base_damage_react_active,
    base_damage_react_blocks_main_continuation,
    resolve_base_combo_member_damage_react,
    resolve_base_damage_react,
)
from tools.stoneage_battle_guardian_model import (
    GuardianRegistration,
    guardian_redirect_allowed,
)
from tools.stoneage_battle_status_model import (
    BASE_STATUS_NAME_BY_INDEX,
    STATUS_POISON,
    BaseBattleStatusRuntime,
    BasePhysicalOnHitStatusInputs,
    BaseStatusApplicationResolution,
    BaseStatusCombatProfile,
    BaseStatusTickInputs,
    BaseStatusTickResult,
    BaseStatusTurnRolls,
    base_status_can_move,
    base_stone_defense_multiplier,
    resolve_base_damage_wakeup,
    resolve_base_physical_on_hit_status_application,
    resolve_base_status_tick,
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

# Stable unguarded pet-skill command sequence begins at 1000.
BATTLE_COM_S_GUARDIAN_ATTACK = 1003
BATTLE_COM_S_GUARDIAN_GUARD = 1004  # enum-only in pinned common Guardian handler
BATTLE_COM_S_STATUSCHANGE = 1008


def battle_command3_low(value: int) -> int:
    return int(value) & 0xFFFF


def battle_command3_high(value: int) -> int:
    return int(value) >> 16


def pack_battle_command3(*, low: int, high: int) -> int:
    """Mirror CHAR_SETWORKINT_LOW/HIGH for the common positive COM3 payloads."""
    return (int(high) << 16) | (int(low) & 0xFFFF)


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
        BATTLE_COM_S_GUARDIAN_ATTACK,
        BATTLE_COM_S_GUARDIAN_GUARD,
        BATTLE_COM_S_STATUSCHANGE,
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
                "unsupported command outside reconstructed base/pet-skill seam"
            )
        object.__setattr__(self, "command1", command1)
        object.__setattr__(self, "command2", int(self.command2))
        object.__setattr__(self, "command3", int(self.command3))
        object.__setattr__(self, "input_complete", bool(self.input_complete))

    @property
    def produces_action(self) -> bool:
        return self.command1 not in NO_ACTION_COMMANDS


@dataclass(frozen=True)
class BattleCommandSetupEffects:
    """Work-state mutations already performed by command/skill submission.

    These are deliberately separate from BattleCommand because the fixed
    source stores them outside COM1/COM2/COM3 (work attack/defense power,
    battle flags, and BattleArray guardian registration).
    """

    attack_power: int | None = None
    defense_power: int | None = None
    guardian_flag: bool = False
    guardian_for_slot: int | None = None
    guardian_barrier: int = 0

    def __post_init__(self) -> None:
        if self.attack_power is not None:
            object.__setattr__(self,"attack_power",int(self.attack_power))
        if self.defense_power is not None:
            object.__setattr__(self,"defense_power",int(self.defense_power))
        object.__setattr__(self,"guardian_flag",bool(self.guardian_flag))
        if self.guardian_for_slot is not None:
            slot=int(self.guardian_for_slot)
            if not 0 <= slot < BATTLE_SLOT_COUNT:
                raise ValueError("guardian_for_slot must be in 0..19")
            object.__setattr__(self,"guardian_for_slot",slot)
        barrier=int(self.guardian_barrier)
        if barrier < 0:
            raise ValueError("guardian_barrier cannot be negative")
        object.__setattr__(self,"guardian_barrier",barrier)


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
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None,
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
    status_runtime={
        str(participant_id):runtime
        for participant_id,runtime in (
            base_status_runtime_by_participant_id or {}
        ).items()
    }
    for participant_id,runtime in status_runtime.items():
        if not isinstance(runtime,BaseBattleStatusRuntime):
            raise TypeError(
                f"base status runtime for combo actor {participant_id} has wrong type"
            )
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
        runtime=status_runtime.get(
            participant_id,
            BaseBattleStatusRuntime(),
        )
        movable=(
            int(participant.hp)>0
            and base_status_can_move(runtime.status)
        )
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
        BATTLE_COM_COMBO,
        BATTLE_COM_WAIT,
        BATTLE_COM_S_GUARDIAN_ATTACK,
        BATTLE_COM_S_STATUSCHANGE,
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
class ComboExecutionRolls:
    """Explicit RNG consumed by one stable combo execution."""

    member_attack_rolls: tuple[OrdinaryAttackRolls, ...]
    retarget_roll: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "member_attack_rolls",
            tuple(self.member_attack_rolls),
        )


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
    is_combo: bool = False
    combo_id: int | None = None
    combo_member_index: int | None = None
    profit_participant_ids: tuple[str, ...] = ()
    status_tick_resolution: BaseStatusTickResult | None = None
    status_application_resolution: BaseStatusApplicationResolution | None = None
    guardian_redirected: bool = False
    guarded_target_slot: int | None = None
    guardian_slot: int | None = None
    damage_react_resolution: BaseDamageReactResolution | None = None
    combo_damage_react_resolution: BaseComboMemberDamageReactResolution | None = None
    combo_settlement: bool = False


@dataclass(frozen=True)
class ResolvedOrdinaryRound:
    events: tuple[OrdinaryRoundEvent, ...]
    hp_by_participant_id: Mapping[str, int]
    hp_by_slot: Mapping[int, int]
    action_order: tuple[str, ...]
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None
    base_damage_react_state_by_participant_id: Mapping[
        str,BaseDamageReactState
    ] | None = None
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


def _effective_attack_power(
    participant: BattleParticipant,
    effects_by_participant_id: Mapping[str,BattleCommandSetupEffects],
) -> int:
    effects=effects_by_participant_id.get(str(participant.participant_id))
    if effects is not None and effects.attack_power is not None:
        return int(effects.attack_power)
    return int(participant.attack)


def _effective_defense_power(
    participant: BattleParticipant,
    effects_by_participant_id: Mapping[str,BattleCommandSetupEffects],
) -> int:
    effects=effects_by_participant_id.get(str(participant.participant_id))
    if effects is not None and effects.defense_power is not None:
        return int(effects.defense_power)
    return int(participant.defense)


def _effective_defense_for_round(
    participant: BattleParticipant,
    defense_profile: str,
    *,
    stone: bool = False,
    work_defense: int | None = None,
) -> float:
    defense=(
        int(participant.defense)
        if work_defense is None
        else int(work_defense)
    )
    if defense_profile == "newpower_70pct":
        return effective_defense_newpower(
            defense,
            stone=bool(stone),
        )
    if defense_profile == "preserved_old_mixed":
        if participant.fixed_vital is None:
            raise ValueError(
                "preserved_old_mixed requires explicit defender.fixed_vital"
            )
        return effective_defense_preserved_old(
            defense,
            participant.quick,
            participant.fixed_vital,
            stone=bool(stone),
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
    setup_effects_by_participant_id: Mapping[
        str,BattleCommandSetupEffects
    ],
    status_runtime_by_participant_id: dict[str,BaseBattleStatusRuntime],
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

        target_defense=_effective_defense_power(
            target,setup_effects_by_participant_id
        )
        target_runtime=status_runtime_by_participant_id[target_id]
        base_damage=physical_base_damage(
            _effective_attack_power(
                actor,setup_effects_by_participant_id
            ),
            _effective_defense_for_round(
                target,
                defense_profile,
                stone=(
                    base_stone_defense_multiplier(
                        target_runtime.status
                    ) > 1.0
                ),
                work_defense=target_defense,
            ),
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
                target_defense,
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
        if int(damage)>0:
            target_runtime=status_runtime_by_participant_id[target_id]
            wake=resolve_base_damage_wakeup(
                target_runtime.status,
                damage_count_before=target_runtime.damage_count,
                damage=int(damage),
            )
            status_runtime_by_participant_id[target_id]=replace(
                target_runtime,
                status=wake.status_after,
                damage_count=wake.damage_count_after,
            )
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


def _resolve_combo_group_with_reactions(
    *,
    combo_id: int,
    members: Sequence[RoundEntry],
    original_target_slot: int,
    target_slot: int,
    retargeted: bool,
    by_slot: Mapping[int, BattleParticipant],
    hp_by_slot: dict[int, int],
    hp_by_id: dict[str, int],
    profiles: Mapping[str, BattleCombatProfile],
    status_runtime_by_participant_id: dict[str,BaseBattleStatusRuntime],
    damage_react_state_by_participant_id: dict[str,BaseDamageReactState],
    guarding: set[int],
    rolls: ComboExecutionRolls,
    defense_profile: str,
    field_attr: str,
    field_power: int,
) -> tuple[OrdinaryRoundEvent, ...]:
    """Execute the stable per-member Combo DamageReact path."""
    group=tuple(members)
    member_rolls=tuple(rolls.member_attack_rolls)
    if len(member_rolls) != len(group):
        raise ValueError(
            "combo execution requires one attack-roll bundle per live member"
        )
    target=by_slot[int(target_slot)]
    target_id=str(target.participant_id)
    if int(hp_by_slot[int(target_slot)]) <= 0:
        raise ValueError("combo target must be alive at execution")
    target_profile=profiles[target_id]
    target_runtime=status_runtime_by_participant_id[target_id]
    target_guarding=int(target_slot) in guarding
    if base_damage_react_active(
        damage_react_state_by_participant_id[target_id]
    ):
        return _resolve_combo_group_with_reactions(
            combo_id=combo_id,
            members=members,
            original_target_slot=original_target_slot,
            target_slot=target_slot,
            retargeted=retargeted,
            by_slot=by_slot,
            hp_by_slot=hp_by_slot,
            hp_by_id=hp_by_id,
            profiles=profiles,
            status_runtime_by_participant_id=(
                status_runtime_by_participant_id
            ),
            damage_react_state_by_participant_id=(
                damage_react_state_by_participant_id
            ),
            guarding=guarding,
            rolls=rolls,
            defense_profile=defense_profile,
            field_attr=field_attr,
            field_power=field_power,
        )
    actor_ids=tuple(str(x.participant.participant_id) for x in group)
    slot_by_id={
        str(participant.participant_id):int(slot)
        for slot,participant in by_slot.items()
    }

    resolved=[]
    accumulated=0
    for member_index,(entry,attack_roll) in enumerate(
        zip(group,member_rolls),start=1
    ):
        actor=entry.participant
        actor_id=str(actor.participant_id)
        actor_slot=slot_by_id[actor_id]
        if int(hp_by_slot[actor_slot]) <= 0:
            raise ValueError("dead combo member reached execution helper")
        actor_profile=profiles[actor_id]

        critical_roll=_validated_roll(
            attack_roll.critical_roll_1_10000,1,10000,
            "combo critical_roll_1_10000",
        )
        is_critical=critical_roll < critical_per_10000(
            actor_profile.fixed_dex,
            target_profile.fixed_dex,
            attacker_luck=_source_luck(actor,actor_profile),
            weapon_critical=int(actor_profile.weapon_critical),
            attacker_type=_participant_battle_kind(actor),
            defender_type=_participant_battle_kind(target),
        )
        damage=attribute_adjusted_damage(
            physical_base_damage(
                actor.attack,
                _effective_defense_for_round(
                    target,
                    defense_profile,
                    stone=(
                        base_stone_defense_multiplier(
                            target_runtime.status
                        ) > 1.0
                    ),
                ),
                int(attack_roll.damage_roll),
            ),
            actor_profile.elements,
            target_profile.elements,
            field_attr=field_attr,
            field_power=field_power,
        )
        if is_critical:
            damage=critical_damage(
                damage,target.defense,actor.level,target.level
            )
        if target_guarding:
            damage=guard_damage(
                damage,
                _validated_roll(
                    attack_roll.guard_roll_1_100,1,100,
                    "combo guard_roll_1_100",
                ),
            )
        if damage < 1:
            damage=_validated_roll(
                attack_roll.minimum_damage_roll_0_1,0,1,
                "combo minimum_damage_roll_0_1",
            )
        result=(
            ("combo_allguard" if target_guarding else "combo_miss")
            if damage == 0
            else ("combo_critical" if is_critical else "combo_normal")
        )
        contribution=max(1,int(damage))

        react=resolve_base_combo_member_damage_react(
            damage_react_state_by_participant_id[target_id],
            raw_damage=contribution,
            attacker_hp=int(hp_by_slot[actor_slot]),
            attacker_max_hp=int(actor.max_hp),
            defender_hp=int(hp_by_slot[int(target_slot)]),
            defender_max_hp=int(target.max_hp),
            attacker_uses_throwing_weapon=counter_weapon_blocks_counter(
                actor_profile.counter_weapon_type
            ),
        )
        damage_react_state_by_participant_id[target_id]=react.state_after
        hp_by_slot[actor_slot]=int(react.attacker_hp_after)
        hp_by_id[actor_id]=int(react.attacker_hp_after)
        hp_by_slot[int(target_slot)]=int(react.defender_hp_after)
        hp_by_id[target_id]=int(react.defender_hp_after)
        accumulated+=int(react.accumulated_damage)

        wake_id=(
            actor_id if react.wakeup_target=="attacker"
            else target_id if react.wakeup_target=="defender"
            else None
        )
        if wake_id is not None:
            runtime=status_runtime_by_participant_id[wake_id]
            wake=resolve_base_damage_wakeup(
                runtime.status,
                damage_count_before=runtime.damage_count,
                damage=contribution,
            )
            status_runtime_by_participant_id[wake_id]=replace(
                runtime,
                status=wake.status_after,
                damage_count=wake.damage_count_after,
            )
            if wake_id==target_id:
                target_runtime=status_runtime_by_participant_id[target_id]

        if react.effective_kind == DAMAGE_REACT_REFLEC:
            event_slot=actor_slot
            event_before=int(react.attacker_hp_before)
            event_after=int(react.attacker_hp_after)
        else:
            event_slot=int(target_slot)
            event_before=int(react.defender_hp_before)
            event_after=int(react.defender_hp_after)

        resolved.append(
            OrdinaryRoundEvent(
                actor_id,
                int(actor_slot),
                BATTLE_COM_COMBO,
                int(entry.action_value),
                result,
                original_target_slot=int(original_target_slot),
                resolved_target_slot=int(event_slot),
                retargeted=bool(retargeted),
                critical=bool(is_critical),
                damage=contribution,
                target_hp_before=event_before,
                target_hp_after=event_after,
                is_combo=True,
                combo_id=int(combo_id),
                combo_member_index=int(member_index),
                combo_damage_react_resolution=react,
            )
        )

    # BATTLE_DamageSub2 applies only the non-reacted accumulated damage after
    # the final attack-list member, with reactions disabled for settlement.
    if accumulated > 0:
        before=int(hp_by_slot[int(target_slot)])
        after=max(0,before-int(accumulated))
        hp_by_slot[int(target_slot)]=after
        hp_by_id[target_id]=after
        last=group[-1]
        last_id=str(last.participant.participant_id)
        resolved.append(
            OrdinaryRoundEvent(
                last_id,
                int(slot_by_id[last_id]),
                BATTLE_COM_COMBO,
                int(last.action_value),
                "combo_settlement",
                original_target_slot=int(original_target_slot),
                resolved_target_slot=int(target_slot),
                retargeted=bool(retargeted),
                damage=int(accumulated),
                target_hp_before=before,
                target_hp_after=after,
                is_combo=True,
                combo_id=int(combo_id),
                combo_settlement=True,
                profit_participant_ids=actor_ids,
            )
        )
    return tuple(resolved)


def _resolve_combo_group(
    *,
    combo_id: int,
    members: Sequence[RoundEntry],
    original_target_slot: int,
    target_slot: int,
    retargeted: bool,
    by_slot: Mapping[int, BattleParticipant],
    hp_by_slot: dict[int, int],
    hp_by_id: dict[str, int],
    profiles: Mapping[str, BattleCombatProfile],
    status_runtime_by_participant_id: dict[str,BaseBattleStatusRuntime],
    damage_react_state_by_participant_id: dict[str,BaseDamageReactState],
    guarding: set[int],
    rolls: ComboExecutionRolls,
    defense_profile: str,
    field_attr: str,
    field_power: int,
) -> tuple[OrdinaryRoundEvent, ...]:
    """Execute the status-free/no-reaction stable combo damage seam."""
    group=tuple(members)
    if len(group) < 1:
        raise ValueError("combo execution requires at least one live member")
    member_rolls=tuple(rolls.member_attack_rolls)
    if len(member_rolls) != len(group):
        raise ValueError(
            "combo execution requires one attack-roll bundle per live member"
        )

    target=by_slot[int(target_slot)]
    target_id=str(target.participant_id)
    before=int(hp_by_slot[int(target_slot)])
    if before <= 0:
        raise ValueError("combo target must be alive at execution")
    target_profile=profiles[target_id]
    target_runtime=status_runtime_by_participant_id[target_id]
    target_guarding=int(target_slot) in guarding
    actor_ids=tuple(
        str(entry.participant.participant_id) for entry in group
    )
    slot_by_actor_id={
        str(participant.participant_id):int(slot)
        for slot,participant in by_slot.items()
    }

    rows=[]
    total_damage=0
    for member_index,(entry,attack_roll) in enumerate(
        zip(group,member_rolls),
        start=1,
    ):
        actor=entry.participant
        actor_id=str(actor.participant_id)
        actor_slot=slot_by_actor_id[actor_id]
        if int(hp_by_slot[actor_slot]) <= 0:
            raise ValueError("dead combo member reached execution helper")
        actor_profile=profiles[actor_id]

        critical_roll=_validated_roll(
            attack_roll.critical_roll_1_10000,
            1,
            10000,
            "combo critical_roll_1_10000",
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
            _effective_defense_for_round(
                target,
                defense_profile,
                stone=(
                    base_stone_defense_multiplier(
                        target_runtime.status
                    ) > 1.0
                ),
            ),
            int(attack_roll.damage_roll),
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
                attack_roll.guard_roll_1_100,
                1,
                100,
                "combo guard_roll_1_100",
            )
            damage=guard_damage(damage,guard_roll)

        if damage < 1:
            damage=_validated_roll(
                attack_roll.minimum_damage_roll_0_1,
                0,
                1,
                "combo minimum_damage_roll_0_1",
            )

        if damage == 0:
            result="combo_allguard" if target_guarding else "combo_miss"
        else:
            result="combo_critical" if is_critical else "combo_normal"

        contribution=max(1,int(damage))
        total_damage+=contribution
        wake=resolve_base_damage_wakeup(
            target_runtime.status,
            damage_count_before=target_runtime.damage_count,
            damage=contribution,
        )
        target_runtime=replace(
            target_runtime,
            status=wake.status_after,
            damage_count=wake.damage_count_after,
        )
        status_runtime_by_participant_id[target_id]=target_runtime
        rows.append(
            (
                entry,
                actor_slot,
                result,
                is_critical,
                contribution,
                member_index,
            )
        )

    after=max(0,before-int(total_damage))
    hp_by_slot[int(target_slot)]=after
    hp_by_id[target_id]=after

    resolved=[]
    for row_index,(
        entry,
        actor_slot,
        result,
        is_critical,
        contribution,
        member_index,
    ) in enumerate(rows):
        is_last=(row_index==len(rows)-1)
        resolved.append(
            OrdinaryRoundEvent(
                str(entry.participant.participant_id),
                int(actor_slot),
                BATTLE_COM_COMBO,
                int(entry.action_value),
                result,
                original_target_slot=int(original_target_slot),
                resolved_target_slot=int(target_slot),
                retargeted=bool(retargeted),
                critical=bool(is_critical),
                damage=int(contribution),
                target_hp_before=before,
                target_hp_after=(after if is_last else before),
                is_combo=True,
                combo_id=int(combo_id),
                combo_member_index=int(member_index),
                profit_participant_ids=actor_ids,
            )
        )
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
    combo_rolls_by_starter_id: Mapping[
        str,ComboExecutionRolls
    ] | None = None,
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None,
    base_status_rolls_by_participant_id: Mapping[
        str,BaseStatusTurnRolls
    ] | None = None,
    base_status_combat_profiles_by_participant_id: Mapping[
        str,BaseStatusCombatProfile
    ] | None = None,
    status_application_rolls_by_attack_id: Mapping[str,int] | None = None,
    guardian_registrations_by_defender_slot: Mapping[
        int,GuardianRegistration
    ] | None = None,
    command_setup_effects_by_participant_id: Mapping[
        str,BattleCommandSetupEffects
    ] | None = None,
    base_damage_react_state_by_participant_id: Mapping[
        str,BaseDamageReactState
    ] | None = None,
    field_attr: str = "none",
    field_power: int = 0,
) -> ResolvedOrdinaryRound:
    """Execute the status-free base battle seam.

    Passing counter_rolls_by_attack_id enables the recovered base counter loop.
    Prepared COMBO groups additionally require combo_rolls_by_starter_id. Guard
    stance is taken from the submitted command set before action sorting,
    matching BATTLE_AttackSeq's inspection of the defender's COM1 rather than
    requiring the guard actor's own execution turn to occur first.
    """
    for entry in prepared.ordered_entries:
        if entry.command.command1 not in ORDINARY_RESOLUTION_COMMANDS:
            raise ValueError(
                "ordinary resolver accepts reconstructed base commands plus "
                "S_GUARDIAN_ATTACK and S_STATUSCHANGE; the pinned common "
                "Guardian handler does not execute enum-only S_GUARDIAN_GUARD"
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
    normalized_combo_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            combo_rolls_by_starter_id or {}
        ).items()
    }
    combo_groups: dict[int,list[RoundEntry]]={}
    for combo_entry in prepared.ordered_entries:
        if combo_entry.command.command1 != BATTLE_COM_COMBO:
            continue
        if int(combo_entry.combo_id) <= 0:
            raise ValueError("prepared COMBO command lacks a positive combo_id")
        combo_groups.setdefault(int(combo_entry.combo_id),[]).append(combo_entry)
    for combo_id,group in combo_groups.items():
        if len(group) < 2:
            raise ValueError(f"prepared combo {combo_id} has fewer than two members")
    processed_combo_ids: set[int]=set()

    supplied_status_runtime={
        str(participant_id):runtime
        for participant_id,runtime in (
            base_status_runtime_by_participant_id or {}
        ).items()
    }
    unknown_status_ids=sorted(
        set(supplied_status_runtime)-set(slot_by_id)
    )
    if unknown_status_ids:
        raise ValueError(
            f"base status runtime references unknown actors: {unknown_status_ids}"
        )
    status_runtime={
        participant_id:supplied_status_runtime.get(
            participant_id,
            BaseBattleStatusRuntime(),
        )
        for participant_id in slot_by_id
    }
    for participant_id,runtime in status_runtime.items():
        if not isinstance(runtime,BaseBattleStatusRuntime):
            raise TypeError(
                f"base status runtime for {participant_id} has wrong type"
            )
    status_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            base_status_rolls_by_participant_id or {}
        ).items()
    }
    unknown_status_roll_ids=sorted(set(status_rolls)-set(slot_by_id))
    if unknown_status_roll_ids:
        raise ValueError(
            f"base status RNG references unknown actors: {unknown_status_roll_ids}"
        )
    status_combat_profiles={
        str(participant_id):profile
        for participant_id,profile in (
            base_status_combat_profiles_by_participant_id or {}
        ).items()
    }
    unknown_status_profile_ids=sorted(
        set(status_combat_profiles)-set(slot_by_id)
    )
    if unknown_status_profile_ids:
        raise ValueError(
            f"base status combat profiles reference unknown actors: "
            f"{unknown_status_profile_ids}"
        )
    for participant_id,profile in status_combat_profiles.items():
        if not isinstance(profile,BaseStatusCombatProfile):
            raise TypeError(
                f"base status combat profile for {participant_id} has wrong type"
            )
    status_application_rolls={
        str(participant_id):int(roll)
        for participant_id,roll in (
            status_application_rolls_by_attack_id or {}
        ).items()
    }
    unknown_status_application_ids=sorted(
        set(status_application_rolls)-set(slot_by_id)
    )
    if unknown_status_application_ids:
        raise ValueError(
            f"status application RNG references unknown actors: "
            f"{unknown_status_application_ids}"
        )
    setup_effects={
        str(participant_id):effects
        for participant_id,effects in (
            command_setup_effects_by_participant_id or {}
        ).items()
    }
    unknown_setup_effect_ids=sorted(set(setup_effects)-set(slot_by_id))
    if unknown_setup_effect_ids:
        raise ValueError(
            f"command setup effects reference unknown actors: "
            f"{unknown_setup_effect_ids}"
        )
    for participant_id,effects in setup_effects.items():
        if not isinstance(effects,BattleCommandSetupEffects):
            raise TypeError(
                f"command setup effects for {participant_id} have wrong type"
            )

    supplied_damage_react={
        str(participant_id):react_state
        for participant_id,react_state in (
            base_damage_react_state_by_participant_id or {}
        ).items()
    }
    unknown_damage_react_ids=sorted(
        set(supplied_damage_react)-set(slot_by_id)
    )
    if unknown_damage_react_ids:
        raise ValueError(
            f"base damage-react state references unknown actors: "
            f"{unknown_damage_react_ids}"
        )
    damage_react_state={
        participant_id:supplied_damage_react.get(
            participant_id,
            BaseDamageReactState(),
        )
        for participant_id in slot_by_id
    }
    for participant_id,react_state in damage_react_state.items():
        if not isinstance(react_state,BaseDamageReactState):
            raise TypeError(
                f"base damage-react state for {participant_id} has wrong type"
            )

    guardian_registrations={
        int(defender_slot):registration
        for defender_slot,registration in (
            guardian_registrations_by_defender_slot or {}
        ).items()
    }
    for defender_slot,registration in guardian_registrations.items():
        if not 0 <= int(defender_slot) <= 19:
            raise ValueError("guardian defender slot must be in 0..19")
        if not isinstance(registration,GuardianRegistration):
            raise TypeError(
                f"guardian registration for slot {defender_slot} has wrong type"
            )

    # Explicit command-submission effects carry the defensive Guardian
    # branch, whose COM1 is indistinguishable from an ordinary GUARD.
    for guardian_id,effects in setup_effects.items():
        if (
            not effects.guardian_flag
            or effects.guardian_for_slot is None
        ):
            continue
        guardian_slot=int(slot_by_id[guardian_id])
        guarded_slot=int(effects.guardian_for_slot)
        registration=GuardianRegistration(
            guardian_slot=guardian_slot,
            guardian_flag=True,
            guardian_barrier=int(effects.guardian_barrier),
        )
        if (
            guarded_slot in guardian_registrations
            and guardian_registrations[guarded_slot] != registration
        ):
            raise ValueError(
                f"conflicting guardian registrations for slot {guarded_slot}"
            )
        guardian_registrations[guarded_slot]=registration

        # PETSKILL_Guardian attack mode sets COM1=S_GUARDIAN_ATTACK, marks the
    # actor with CHAR_BATTLEFLG_GUARDIAN, and registers its front-row owner.
    # This registration exists before action sorting/execution.
    for guardian_entry in prepared.ordered_entries:
        if (
            guardian_entry.command.command1
            != BATTLE_COM_S_GUARDIAN_ATTACK
            or not guardian_entry.command.input_complete
            or int(guardian_entry.participant.hp) <= 0
        ):
            continue
        guardian_id=str(guardian_entry.participant.participant_id)
        guardian_slot=int(slot_by_id[guardian_id])
        side=_slot_side(guardian_slot)
        ownerpos=guardian_slot-5-side*SIDE_OFFSET
        if ownerpos < 0 or ownerpos > 19:
            continue
        guarded_slot=side*SIDE_OFFSET+ownerpos
        auto=GuardianRegistration(
            guardian_slot=guardian_slot,
            guardian_flag=True,
        )
        if (
            guarded_slot in guardian_registrations
            and guardian_registrations[guarded_slot] != auto
        ):
            raise ValueError(
                f"conflicting guardian registrations for slot {guarded_slot}"
            )
        guardian_registrations[guarded_slot]=auto

    if guardian_registrations and combo_groups:
        raise ValueError(
            "guardian interaction with combo execution is a separate seam"
        )
    has_active_base_status=any(
        any(int(getattr(runtime.status,name))>0 for name in (
            "poison","paralysis","sleep","stone","drunk","confusion"
        ))
        for runtime in status_runtime.values()
    )

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
                setup_effects_by_participant_id=setup_effects,
                status_runtime_by_participant_id=status_runtime,
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
        current_status_tick=None

        if (
            entry.command.command1 == BATTLE_COM_COMBO
            and int(entry.combo_id) in processed_combo_ids
        ):
            continue

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

        command=entry.command
        runtime=status_runtime[str(participant_id)]
        status_before=runtime.status
        if any(int(getattr(status_before,name))>0 for name in (
            "poison","paralysis","sleep","stone","drunk","confusion"
        )):
            rolls=status_rolls.get(
                str(participant_id),
                BaseStatusTurnRolls(),
            )
            valid_target_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            tick=resolve_base_status_tick(
                BaseStatusTickInputs(
                    hp=int(hp_by_slot[slot]),
                    status=status_before,
                    poison_stat_sum=runtime.poison_stat_sum,
                    actor_slot=int(slot),
                    valid_target_slots=valid_target_slots,
                    confusion_action_roll_1_100=(
                        rolls.confusion_action_roll_1_100
                    ),
                    confusion_side_roll_0_1=(
                        rolls.confusion_side_roll_0_1
                    ),
                    confusion_pos_roll_0_9=(
                        rolls.confusion_pos_roll_0_9
                    ),
                    work_quick=runtime.work_quick,
                    ride_work_quick=runtime.ride_work_quick,
                )
            )
            current_status_tick=tick
            hp_by_slot[slot]=int(tick.hp_after)
            hp_by_id[str(participant_id)]=int(tick.hp_after)
            runtime=replace(
                runtime,
                status=tick.status_after,
                work_quick=tick.work_quick_after,
            )
            status_runtime[str(participant_id)]=runtime
            events.append(
                OrdinaryRoundEvent(
                    str(participant_id),
                    int(slot),
                    int(entry.command.command1),
                    int(entry.action_value),
                    "status_tick",
                    original_target_slot=int(slot),
                    resolved_target_slot=int(slot),
                    damage=int(tick.poison_damage),
                    target_hp_before=int(tick.hp_before),
                    target_hp_after=int(tick.hp_after),
                    status_tick_resolution=tick,
                )
            )
            if tick.command_override == "none":
                command=BattleCommand(
                    BATTLE_COM_NONE,
                    command2=entry.command.command2,
                    command3=entry.command.command3,
                    input_complete=entry.command.input_complete,
                )
                guarding.discard(slot)
            elif tick.command_override == "attack":
                if tick.target_override is None:
                    raise ValueError("confusion attack rewrite lacks target")
                if int(tick.target_override) < 0:
                    events.append(
                        OrdinaryRoundEvent(
                            str(participant_id),
                            int(slot),
                            BATTLE_COM_NONE,
                            int(entry.action_value),
                            "confusion_no_target",
                        )
                    )
                    command_by_slot[slot]=BattleCommand(BATTLE_COM_NONE)
                    continue
                command=BattleCommand(
                    BATTLE_COM_ATTACK,
                    command2=int(tick.target_override),
                    command3=entry.command.command3,
                    input_complete=entry.command.input_complete,
                )
                guarding.discard(slot)
            command_by_slot[slot]=command

        if command.command1 == BATTLE_COM_NONE:
            events.append(
                OrdinaryRoundEvent(
                    str(participant_id),
                    int(slot),
                    BATTLE_COM_NONE,
                    int(entry.action_value),
                    "status_no_action",
                )
            )
            continue

        if command.command1 == BATTLE_COM_WAIT:
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

        if command.command1 == BATTLE_COM_GUARD:
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

        if command.command1 == BATTLE_COM_ESCAPE:
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

        if command.command1 == BATTLE_COM_CAPTURE:
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
            original_target=int(command.command2)
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

        if command.command1 == BATTLE_COM_COMBO:
            group=combo_groups[int(entry.combo_id)]
            current_index=group.index(entry)
            live_members=[entry]

            # Source COMBO execution advances over all later members now. Each
            # later member runs BATTLE_StatusSeq at this early point and is
            # included iff it is alive and can move after that tick. Its COM1
            # rewrite (including confusion) does not cancel membership.
            for candidate in group[current_index+1:]:
                candidate_id=str(candidate.participant.participant_id)
                candidate_slot=int(slot_by_id[candidate_id])
                if (
                    not candidate.command.input_complete
                    or candidate_slot in exited_slots
                    or int(hp_by_slot.get(candidate_slot,0)) <= 0
                ):
                    continue

                candidate_runtime=status_runtime[candidate_id]
                candidate_status=candidate_runtime.status
                if any(
                    int(getattr(candidate_status,name))>0
                    for name in (
                        "poison","paralysis","sleep",
                        "stone","drunk","confusion",
                    )
                ):
                    candidate_rolls=status_rolls.get(
                        candidate_id,
                        BaseStatusTurnRolls(),
                    )
                    valid_target_slots=tuple(
                        other_slot
                        for other_slot in sorted(by_slot)
                        if (
                            other_slot not in exited_slots
                            and int(hp_by_slot.get(other_slot,0)) > 0
                        )
                    )
                    tick=resolve_base_status_tick(
                        BaseStatusTickInputs(
                            hp=int(hp_by_slot[candidate_slot]),
                            status=candidate_status,
                            poison_stat_sum=candidate_runtime.poison_stat_sum,
                            actor_slot=candidate_slot,
                            valid_target_slots=valid_target_slots,
                            confusion_action_roll_1_100=(
                                candidate_rolls.confusion_action_roll_1_100
                            ),
                            confusion_side_roll_0_1=(
                                candidate_rolls.confusion_side_roll_0_1
                            ),
                            confusion_pos_roll_0_9=(
                                candidate_rolls.confusion_pos_roll_0_9
                            ),
                            work_quick=candidate_runtime.work_quick,
                            ride_work_quick=candidate_runtime.ride_work_quick,
                        )
                    )
                    hp_by_slot[candidate_slot]=int(tick.hp_after)
                    hp_by_id[candidate_id]=int(tick.hp_after)
                    candidate_runtime=replace(
                        candidate_runtime,
                        status=tick.status_after,
                        work_quick=tick.work_quick_after,
                    )
                    status_runtime[candidate_id]=candidate_runtime
                    events.append(
                        OrdinaryRoundEvent(
                            candidate_id,
                            candidate_slot,
                            int(candidate.command.command1),
                            int(candidate.action_value),
                            "status_tick",
                            original_target_slot=candidate_slot,
                            resolved_target_slot=candidate_slot,
                            damage=int(tick.poison_damage),
                            target_hp_before=int(tick.hp_before),
                            target_hp_after=int(tick.hp_after),
                            status_tick_resolution=tick,
                        )
                    )
                    if tick.command_override=="none":
                        command_by_slot[candidate_slot]=BattleCommand(
                            BATTLE_COM_NONE,
                            command2=candidate.command.command2,
                            command3=candidate.command.command3,
                            input_complete=candidate.command.input_complete,
                        )
                        guarding.discard(candidate_slot)
                    elif tick.command_override=="attack":
                        command_by_slot[candidate_slot]=BattleCommand(
                            BATTLE_COM_ATTACK,
                            command2=(
                                -1
                                if tick.target_override is None
                                else int(tick.target_override)
                            ),
                            command3=candidate.command.command3,
                            input_complete=candidate.command.input_complete,
                        )
                        guarding.discard(candidate_slot)

                    if not tick.can_move_after_tick:
                        continue

                if int(hp_by_slot.get(candidate_slot,0)) <= 0:
                    continue
                live_members.append(candidate)

            live_group=tuple(live_members)
            starter_id=str(participant_id)
            if starter_id not in normalized_combo_rolls:
                raise KeyError(
                    f"missing combo execution rolls for starter {starter_id}"
                )
            combo_rolls=normalized_combo_rolls[starter_id]
            original_target=int(entry.command.command2)
            target=original_target
            retargeted=False
            target_alive=(
                target in by_slot
                and target not in exited_slots
                and int(hp_by_slot.get(target,0)) > 0
            )
            if target_alive and _slot_side(target)==_slot_side(slot):
                raise ValueError(
                    "same-side combo attacks require a separate provenance seam"
                )
            if not target_alive:
                target=_retarget_slot(
                    slot,
                    by_slot,
                    hp_by_slot,
                    combo_rolls.retarget_roll,
                    excluded_slots=exited_slots,
                )
                retargeted=True
            if target is None:
                events.append(
                    OrdinaryRoundEvent(
                        str(participant_id),
                        int(slot),
                        BATTLE_COM_COMBO,
                        int(entry.action_value),
                        "combo_no_target",
                        original_target_slot=original_target,
                        retargeted=True,
                        is_combo=True,
                        combo_id=int(entry.combo_id),
                    )
                )
                continue
            for candidate in live_group:
                if candidate.participant.side != participant.side:
                    raise ValueError("combo group crossed battle sides")
                if int(candidate.command.command2) != original_target:
                    raise ValueError("combo group target drift")
            events.extend(
                _resolve_combo_group(
                    combo_id=int(entry.combo_id),
                    members=live_group,
                    original_target_slot=original_target,
                    target_slot=int(target),
                    retargeted=retargeted,
                    by_slot=by_slot,
                    hp_by_slot=hp_by_slot,
                    hp_by_id=hp_by_id,
                    profiles=profiles,
                    status_runtime_by_participant_id=status_runtime,
                    damage_react_state_by_participant_id=damage_react_state,
                    guarding=guarding,
                    rolls=combo_rolls,
                    defense_profile=defense_profile,
                    field_attr=field_attr,
                    field_power=field_power,
                )
            )
            processed_combo_ids.add(int(entry.combo_id))
            continue

        rolls = attack_rolls.get(participant_id)
        if rolls is None:
            raise KeyError(f"missing ordinary attack rolls for {participant_id}")
        attack_command_code=int(command.command1)
        if attack_command_code in {
            BATTLE_COM_S_GUARDIAN_ATTACK,
            BATTLE_COM_S_STATUSCHANGE,
        }:
            command_by_slot[slot]=BattleCommand(
                BATTLE_COM_ATTACK,
                command2=command.command2,
                command3=command.command3,
                input_complete=command.input_complete,
            )

        original_target = int(command.command2)
        target = original_target
        retargeted = False

        target_alive = (
            target in by_slot
            and target not in exited_slots
            and int(hp_by_slot.get(target, 0)) > 0
        )
        if (
            target_alive
            and _slot_side(target) == _slot_side(slot)
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            raise ValueError(
                "same-side ordinary attacks require confusion provenance"
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
                    attack_command_code,
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
        continuation_blocked_by_reaction=(
            base_damage_react_blocks_main_continuation(
                damage_react_state[str(participant_id)],
                damage_react_state[str(defender_id)],
            )
        )

        # Source order: dodge is checked against the original/adjusted target
        # before BATTLE_GuardianCheck can redirect the physical hit.
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
                        attack_command_code,
                        entry.action_value,
                        "dodge",
                        original_target_slot=original_target,
                        resolved_target_slot=target,
                        retargeted=retargeted,
                        target_hp_before=before,
                        target_hp_after=before,
                    )
                )
                if not continuation_blocked_by_reaction:
                    append_counter_chain(participant_id,slot,target)
                continue

        counter_target_slot=int(target)
        damage_target_slot=int(target)
        guardian_redirected=False
        guarded_target_slot=None
        guardian_slot=None
        registration=guardian_registrations.get(int(target))
        if registration is not None:
            candidate_slot=int(registration.guardian_slot)
            candidate=by_slot.get(candidate_slot)
            candidate_runtime=(
                None
                if candidate is None
                else status_runtime[str(candidate.participant_id)]
            )
            if guardian_redirect_allowed(
                guardian_exists=(
                    candidate is not None
                    and candidate_slot not in exited_slots
                ),
                guardian_slot=candidate_slot,
                defender_slot=int(target),
                guardian_alive=(
                    candidate is not None
                    and candidate_slot not in exited_slots
                    and int(hp_by_slot.get(candidate_slot,0)) > 0
                ),
                guardian_flag=bool(registration.guardian_flag),
                guardian_sleep=(
                    0 if candidate_runtime is None
                    else int(candidate_runtime.status.sleep)
                ),
                guardian_confusion=(
                    0 if candidate_runtime is None
                    else int(candidate_runtime.status.confusion)
                ),
                guardian_paralysis=(
                    0 if candidate_runtime is None
                    else int(candidate_runtime.status.paralysis)
                ),
                guardian_stone=(
                    0 if candidate_runtime is None
                    else int(candidate_runtime.status.stone)
                ),
                guardian_barrier=int(registration.guardian_barrier),
                guardian_is_attacker=(candidate_slot==int(slot)),
                attacker_uses_throw_weapon=counter_weapon_blocks_counter(
                    attacker_profile.counter_weapon_type
                ),
            ):
                guardian_redirected=True
                guarded_target_slot=int(target)
                guardian_slot=candidate_slot
                damage_target_slot=candidate_slot

        defender = by_slot[damage_target_slot]
        defender_id = defender.participant_id
        defender_profile = profiles[defender_id]
        before = hp_by_slot[damage_target_slot]

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

        defender_work_defense=_effective_defense_power(
            defender,setup_effects
        )
        base_damage = physical_base_damage(
            _effective_attack_power(participant,setup_effects),
            _effective_defense_for_round(
                defender,
                defense_profile,
                stone=(
                    base_stone_defense_multiplier(
                        status_runtime[str(defender_id)].status
                    ) > 1.0
                ),
                work_defense=defender_work_defense,
            ),
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
                defender_work_defense,
                participant.level,
                defender.level,
            )

        if damage_target_slot in guarding:
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

        if damage == 0 and guardian_redirected:
            # AttackSeq forces a redirected zero-damage result to NORMAL/1.
            damage=1
            result="normal"
        elif damage == 0:
            result = (
                "allguard"
                if damage_target_slot in guarding
                else "miss"
            )
        else:
            result = "critical" if is_critical else "normal"

        reaction_defender=defender
        reaction_defender_id=str(defender_id)
        reaction_resolution=resolve_base_damage_react(
            damage_react_state[reaction_defender_id],
            raw_damage=int(damage),
            attacker_hp=int(hp_by_slot[slot]),
            attacker_max_hp=int(participant.max_hp),
            defender_hp=int(hp_by_slot[damage_target_slot]),
            defender_max_hp=int(reaction_defender.max_hp),
            attacker_uses_throwing_weapon=counter_weapon_blocks_counter(
                attacker_profile.counter_weapon_type
            ),
        )
        damage_react_state[reaction_defender_id]=reaction_resolution.state_after

        hp_by_slot[slot]=int(reaction_resolution.attacker_hp_after)
        hp_by_id[str(participant_id)]=int(
            reaction_resolution.attacker_hp_after
        )
        hp_by_slot[damage_target_slot]=int(
            reaction_resolution.defender_hp_after
        )
        hp_by_id[reaction_defender_id]=int(
            reaction_resolution.defender_hp_after
        )

        if reaction_resolution.effective_kind == DAMAGE_REACT_REFLEC:
            resolved_damage_slot=int(slot)
            resolved_damage_id=str(participant_id)
            before=int(reaction_resolution.attacker_hp_before)
            after=int(reaction_resolution.attacker_hp_after)
            status_target_slot=int(slot)
        else:
            resolved_damage_slot=int(damage_target_slot)
            resolved_damage_id=reaction_defender_id
            before=int(reaction_resolution.defender_hp_before)
            after=int(reaction_resolution.defender_hp_after)
            status_target_slot=int(damage_target_slot)

        if (
            int(damage) > 0
            and reaction_resolution.wakeup_target is not None
        ):
            wake_target_id=(
                str(participant_id)
                if reaction_resolution.wakeup_target == "attacker"
                else reaction_defender_id
            )
            wake_runtime=status_runtime[wake_target_id]
            wake=resolve_base_damage_wakeup(
                wake_runtime.status,
                damage_count_before=wake_runtime.damage_count,
                damage=int(damage),
            )
            status_runtime[wake_target_id]=replace(
                wake_runtime,
                status=wake.status_after,
                damage_count=wake.damage_count_after,
            )

        status_application=None
        if (
            int(damage) > 0
            and attack_command_code == BATTLE_COM_S_STATUSCHANGE
        ):
            status_index=battle_command3_low(command.command3)
            status_name=BASE_STATUS_NAME_BY_INDEX.get(status_index)
            if status_name is not None:
                status_target=by_slot[status_target_slot]
                status_target_id=str(status_target.participant_id)
                if status_target_id not in status_combat_profiles:
                    raise KeyError(
                        f"missing base status combat profile for {status_target_id}"
                    )
                status_profile=status_combat_profiles[status_target_id]
                target_runtime=status_runtime[status_target_id]
                status_application=resolve_base_physical_on_hit_status_application(
                    BasePhysicalOnHitStatusInputs(
                        status=status_name,
                        attacker_level=int(participant.level),
                        defender_level=int(status_target.level),
                        pvp=False,
                        attacker_fixed_luck=int(attacker_profile.fixed_luck),
                        defender_vital=int(status_profile.vital),
                        defender_str=int(status_profile.strength),
                        defender_tough=int(status_profile.tough),
                        defender_dex=int(status_profile.dex),
                        defender_resistance=status_profile.resistance_for(
                            status_name
                        ),
                        source_turn=battle_command3_high(command.command3),
                        per_offset=30,
                    ),
                    target_runtime.status,
                    damage_after_resolution=int(damage),
                    roll_1_100=status_application_rolls.get(
                        str(participant_id)
                    ),
                )
                if status_application.check.success:
                    poison_stat_sum=target_runtime.poison_stat_sum
                    if (
                        status_name == STATUS_POISON
                        and poison_stat_sum is None
                    ):
                        poison_stat_sum=(
                            int(status_profile.vital)
                            + int(status_profile.strength)
                            + int(status_profile.tough)
                            + int(status_profile.dex)
                        )
                    status_runtime[status_target_id]=replace(
                        target_runtime,
                        status=status_application.status_after,
                        poison_stat_sum=poison_stat_sum,
                    )
                    if status_application.command_cleared:
                        command_by_slot[status_target_slot]=BattleCommand(
                            BATTLE_COM_NONE
                        )
                        guarding.discard(status_target_slot)
        events.append(
            OrdinaryRoundEvent(
                participant_id,
                slot,
                attack_command_code,
                entry.action_value,
                result,
                original_target_slot=original_target,
                resolved_target_slot=resolved_damage_slot,
                retargeted=retargeted,
                critical=is_critical,
                damage=int(damage),
                target_hp_before=before,
                target_hp_after=after,
                status_application_resolution=status_application,
                guardian_redirected=guardian_redirected,
                guarded_target_slot=guarded_target_slot,
                guardian_slot=guardian_slot,
                damage_react_resolution=reaction_resolution,
            )
        )
        # BATTLE_Attack forces continuation FALSE whenever Guardian>=0.
        if (
            not guardian_redirected
            and not continuation_blocked_by_reaction
            and result != "critical"
            and counter_target_slot not in guarding
            and after > 0
        ):
            append_counter_chain(
                participant_id,
                slot,
                counter_target_slot,
            )

    return ResolvedOrdinaryRound(
        events=tuple(events),
        hp_by_participant_id=MappingProxyType(dict(hp_by_id)),
        hp_by_slot=MappingProxyType(dict(hp_by_slot)),
        action_order=tuple(
            entry.participant.participant_id
            for entry in prepared.ordered_entries
        ),
        base_status_runtime_by_participant_id=MappingProxyType(
            dict(status_runtime)
        ),
        base_damage_react_state_by_participant_id=MappingProxyType(
            dict(damage_react_state)
        ),
        exited_participant_ids=tuple(exited_ids),
        escaped_participant_ids=tuple(escaped_ids),
    )
