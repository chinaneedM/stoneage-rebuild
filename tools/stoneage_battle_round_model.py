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

from tools.stoneage_attack_magic_action_model import (
    AttackMagicDefenderState,
    AttackMagicRideTargetState,
    AttackMagicTargetResolution,
    EnemyAttackMagicActionRolls,
    EnemyAttackMagicCasterState,
    resolve_enemy_attack_magic_action,
)
from tools.stoneage_attack_magic_damage_model import ElementAttrs
from tools.stoneage_attack_magic_model import BATTLE_COM_S_ATTACK_MAGIC
from tools.stoneage_attack_magic_state_model import (
    AttackMagicRoundOverlay,
    attack_magic_field_element,
)
from tools.stoneage_enemy_ai_attack_magic_bridge import (
    EnemyAiAttackMagicSubmission,
)
from tools.stoneage_enemy_ai_rehp_bridge import EnemyAiReHpSubmission
from tools.stoneage_enemy_ai_damage_to_hp_bridge import (
    EnemyAiDamageToHpSubmission,
)
from tools.stoneage_enemy_ai_mp_damage_bridge import EnemyAiMpDamageSubmission
from tools.stoneage_enemy_ai_fall_ground_bridge import (
    EnemyAiFallGroundSubmission,
)
from tools.stoneage_enemy_ai_battle_tear_bridge import (
    EnemyAiBattleTearSubmission,
)
from tools.stoneage_enemy_ai_nocast_bridge import EnemyAiNocastSubmission
from tools.stoneage_enemy_ai_barrier_bridge import EnemyAiBarrierSubmission
from tools.stoneage_enemy_ai_guard_break2_bridge import (
    EnemyAiGuardBreak2Submission,
)
from tools.stoneage_guard_break2_model import (
    GuardBreak2DamageResolution,
    resolve_guard_break2_damage_step,
)
from tools.stoneage_barrier_model import (
    BarrierApplication,
    BarrierCheckInputs,
    BarrierSelfTick,
    resolve_barrier_multilist,
    resolve_barrier_self_tick,
    resolve_barrier_target,
)
from tools.stoneage_barrier_runtime_state import BarrierActionRolls
from tools.stoneage_nocast_model import (
    NocastApplication,
    NocastCheckInputs,
    NocastTick,
    resolve_nocast_multilist,
    resolve_nocast_target,
    resolve_nocast_tick,
)
from tools.stoneage_nocast_runtime_state import (
    NocastActionRolls,
    NocastRoundOverlay,
)
from tools.stoneage_battle_tear_damage_model import (
    BattleTearAugmentation,
    resolve_battle_tear_pre_damage_sub,
)
from tools.stoneage_fall_ground_model import (
    FallGroundResolution,
    resolve_fall_ground,
)
from tools.stoneage_mp_damage_model import (
    MpDamageResolution,
    resolve_mp_damage,
)
from tools.stoneage_damage_to_hp_model import (
    DamageToHpRecovery,
    resolve_damage_to_hp_recovery,
)
from tools.stoneage_enemy_rehp_model import (
    EnemyReHpAllyState,
    EnemyReHpResolution,
    EnemyReHpRolls,
    resolve_enemy_rehp_effect,
)
from tools.stoneage_recovered25_attack_magic_runtime import (
    Recovered25AttackMagicRuntime,
)

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
    BattleUltimateDamageInputs,
    BattleUltimateDamageResolution,
    BattleDeathUltimateInputs,
    BattleDeathUltimateResolution,
    COUNTER_WEAPON_FIST,
    attribute_adjusted_damage,
    critical_damage,
    critical_per_10000,
    continuation_divided_damage,
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
    resolve_battle_ultimate_damage,
    resolve_battle_death_ultimate_override,
)
from tools.stoneage_battle_damage_react_model import (
    DAMAGE_REACT_ABSROB,
    DAMAGE_REACT_REFLEC,
    DAMAGE_REACT_VANISH,
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
from tools.stoneage_battle_ride_damage_model import (
    RideDamageSplit,
    RideHpResolution,
    RidePetRuntime,
    apply_ride_damage,
    apply_ride_heal,
    combo_ride_damage_split,
    immediate_reaction_ride_split,
    ordinary_ride_damage_split,
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
from tools.stoneage_petskill_core_model import (
    abduct_probability,
    abduct_transition,
    earth_round_attack_transition,
    steal_transition,
)


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
BATTLE_COM_S_RENZOKU = 1001
BATTLE_COM_S_GBREAK = 1002
BATTLE_COM_S_GUARDIAN_ATTACK = 1003
BATTLE_COM_S_GUARDIAN_GUARD = 1004  # enum-only in pinned common Guardian handler
BATTLE_COM_S_CHARGE = 1005
BATTLE_COM_S_MIGHTY = 1006
BATTLE_COM_S_POWERBALANCE = 1007
BATTLE_COM_S_STATUSCHANGE = 1008
# Fixed battle.h sequence: EARTHROUND0=1009, EARTHROUND1=1010,
# LOSTESCAPE=1011, ABDUCT=1012, STEAL=1013.
BATTLE_COM_S_EARTHROUND0 = 1009
BATTLE_COM_S_EARTHROUND1 = 1010
BATTLE_COM_S_ABDUCT = 1012
BATTLE_COM_S_STEAL = 1013
BATTLE_COM_S_NOGUARD = 1014
BATTLE_COM_S_CHARGE_OK = 1015


def battle_command3_low(value: int) -> int:
    return int(value) & 0xFFFF


def battle_command3_high(value: int) -> int:
    return int(value) >> 16


def pack_battle_command3(*, low: int, high: int) -> int:
    """Mirror CHAR_SETWORKINT_LOW/HIGH for the common positive COM3 payloads."""
    return (int(high) << 16) | (int(low) & 0xFFFF)


def _noguard_counter_percent_modifier(command: "BattleCommand") -> int:
    """Decode the active fixed-source upper-byte NoGuard counter modifier."""

    if int(command.command1) != BATTLE_COM_S_NOGUARD:
        return 0
    value=(battle_command3_low(command.command3) >> 8) & 0xFF
    if value > 127:
        value *= -1
    return int(value)


def _noguard_dodge_percent_modifier(command: "BattleCommand") -> int:
    if int(command.command1) != BATTLE_COM_S_NOGUARD:
        return 0
    return int(battle_command3_high(command.command3))


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
        BATTLE_COM_S_ATTACK_MAGIC,
        BATTLE_COM_S_RENZOKU,
        BATTLE_COM_S_GBREAK,
        BATTLE_COM_S_GUARDIAN_ATTACK,
        BATTLE_COM_S_GUARDIAN_GUARD,
        BATTLE_COM_S_CHARGE,
        BATTLE_COM_S_MIGHTY,
        BATTLE_COM_S_POWERBALANCE,
        BATTLE_COM_S_STATUSCHANGE,
        BATTLE_COM_S_EARTHROUND0,
        BATTLE_COM_S_EARTHROUND1,
        BATTLE_COM_S_ABDUCT,
        BATTLE_COM_S_STEAL,
        BATTLE_COM_S_NOGUARD,
        BATTLE_COM_S_CHARGE_OK,
    }
)

NO_ACTION_COMMANDS = frozenset({
    BATTLE_COM_NONE,
    BATTLE_COM_WAIT,
    BATTLE_COM_S_NOGUARD,
})


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
    # Latent fixed-source ChargeAttack ready power. It is not applied while
    # S_CHARGE waits; LOW(COM3)==0 promotes it for S_CHARGE_OK.
    charge_ready_attack_power: int | None = None
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
        BATTLE_COM_NONE,
        BATTLE_COM_ATTACK,
        BATTLE_COM_GUARD,
        BATTLE_COM_CAPTURE,
        BATTLE_COM_ESCAPE,
        BATTLE_COM_COMBO,
        BATTLE_COM_WAIT,
        BATTLE_COM_S_ATTACK_MAGIC,
        BATTLE_COM_S_RENZOKU,
        BATTLE_COM_S_GBREAK,
        BATTLE_COM_S_GUARDIAN_ATTACK,
        BATTLE_COM_S_CHARGE,
        BATTLE_COM_S_MIGHTY,
        BATTLE_COM_S_POWERBALANCE,
        BATTLE_COM_S_STATUSCHANGE,
        BATTLE_COM_S_EARTHROUND0,
        BATTLE_COM_S_EARTHROUND1,
        BATTLE_COM_S_ABDUCT,
        BATTLE_COM_S_STEAL,
        BATTLE_COM_S_NOGUARD,
        BATTLE_COM_S_CHARGE_OK,
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
    ultimate_roll_1_100: int | None = None


@dataclass(frozen=True)
class CounterAttemptRolls:
    """Explicit RNG consumed by one BATTLE_Counter() attempt."""

    counter_check_roll_1_10000: int | None
    attack_rolls: OrdinaryAttackRolls | None = None


@dataclass(frozen=True)
class ContinuationAttackRolls:
    """Explicit per-hit RNG for one stable S_RENZOKU execution.

    Each hit carries its own OrdinaryAttackRolls bundle.  retarget_roll inside
    that bundle is consumed only when the source resets COM2 to the original
    target and BATTLE_TargetAdjust finds that original target dead/invalid.
    """

    hit_rolls: tuple[OrdinaryAttackRolls, ...]

    def __post_init__(self) -> None:
        rolls=tuple(self.hit_rolls)
        if not 1 <= len(rolls) <= 10:
            raise ValueError("ContinuationAttack requires 1..10 hit-roll bundles")
        object.__setattr__(self,"hit_rolls",rolls)


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
class OrdinaryAbductRolls:
    """Explicit RNG consumed by TargetAdjust + BATTLE_Abduct."""

    abduct_roll_1_100: int | None = None
    retarget_roll: int | None = None


@dataclass(frozen=True)
class OrdinaryStealRolls:
    """Explicit RAND inputs consumed by TargetAdjust + BATTLE_Steal."""

    success_roll_1_100: int | None = None
    mode_roll_1_100: int | None = None
    gold_percent_roll_8_12: int | None = None
    chosen_item_ordinal: int | None = None
    retarget_roll: int | None = None


@dataclass(frozen=True)
class OrdinaryStealResolution:
    success: bool
    mode: str | None
    attacker_exits: bool
    defender_gold_loss: int = 0
    destroyed_item_slot: int | None = None


@dataclass(frozen=True)
class OrdinaryAbductContext:
    """Recovered command identity plus fixed battle-global context."""

    skill_array: int
    ai_threshold: int
    has_win_func: bool = False

    def __post_init__(self) -> None:
        array=int(self.skill_array)
        if array < 0:
            raise ValueError("Abduct skill array must be non-negative")
        object.__setattr__(self,"skill_array",array)
        object.__setattr__(self,"ai_threshold",int(self.ai_threshold))
        object.__setattr__(self,"has_win_func",bool(self.has_win_func))


@dataclass(frozen=True)
class OrdinaryAbductResolution:
    attempted: bool
    success: bool
    probability: int
    attacker_exits: bool
    defender_exits: bool


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
    abduct_resolution: OrdinaryAbductResolution | None = None
    steal_resolution: OrdinaryStealResolution | None = None
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
    ride_damage_split: RideDamageSplit | None = None
    ride_hp_resolution: RideHpResolution | None = None
    ride_pet_fell_rider_id: str | None = None
    ultimate_damage_resolution: BattleUltimateDamageResolution | None = None
    death_ultimate_resolution: BattleDeathUltimateResolution | None = None
    ultimate_kind: int = 0
    # Exact round-local BENT_FLG_ULTIMATE write. Most paths leave these null
    # and the flag target is the resolved death target. Combo+DamageReact can
    # write the flag to a different entry after its quirky defindex rewrite.
    ultimate_flag_target_slot: int | None = None
    ultimate_flag_kind: int = 0
    attack_magic_target_resolution: AttackMagicTargetResolution | None = None
    enemy_rehp_resolution: EnemyReHpResolution | None = None
    damage_to_hp_recovery: DamageToHpRecovery | None = None
    mp_damage_resolution: MpDamageResolution | None = None
    fall_ground_resolution: FallGroundResolution | None = None
    battle_tear_augmentation: BattleTearAugmentation | None = None
    guard_break2_resolution: GuardBreak2DamageResolution | None = None
    barrier_application: BarrierApplication | None = None
    barrier_tick_resolution: BarrierSelfTick | None = None
    nocast_application: NocastApplication | None = None
    nocast_tick_resolution: NocastTick | None = None


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
    ride_pet_runtime: RidePetRuntime | None = None
    attack_magic_overlay: AttackMagicRoundOverlay | None = None
    nocast_overlay: NocastRoundOverlay | None = None
    ultimate_overkill_by_participant_id: Mapping[str,int] | None = None
    ultimate_exited_participant_ids: tuple[str, ...] = ()
    exited_participant_ids: tuple[str, ...] = ()
    escaped_participant_ids: tuple[str, ...] = ()
    carried_commands_by_participant_id: Mapping[str,BattleCommand] | None = None
    carried_setup_effects_by_participant_id: Mapping[
        str,BattleCommandSetupEffects
    ] | None = None
    steal_gold_by_player_id: Mapping[str,int] | None = None
    steal_item_slots_by_player_id: Mapping[str,tuple[int,...]] | None = None
    mp_by_participant_id: Mapping[str,int] | None = None


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


def _attack_magic_exact_retarget_rolls(
    selector: int,
    *,
    alive_slots: Sequence[int],
    rolls_0_9: Sequence[int],
) -> tuple[int,...]:
    """Reject unused AttackMagic BATTLE_MultiList retarget RNG."""
    selector=int(selector)
    rolls=tuple(int(x) for x in rolls_0_9)
    if any(not 0 <= value <= 9 for value in rolls):
        raise ValueError("AttackMagic retarget roll must be 0..9")

    alive={int(x) for x in alive_slots}
    if not 0 <= selector < 20:
        if rolls:
            raise ValueError(
                "AttackMagic row/side selector cannot consume retarget RNG"
            )
        return rolls

    side=0 if selector < 10 else 1
    candidates=tuple(
        slot
        for slot in range(side*10,side*10+10)
        if slot in alive
    )
    if not candidates or selector in alive:
        if rolls:
            raise ValueError(
                "AttackMagic live/no-target selector cannot consume retarget RNG"
            )
        return rolls

    success_index=None
    for index,value in enumerate(rolls):
        if value < len(candidates):
            success_index=index
            break
    if success_index is None:
        return rolls
    if success_index != len(rolls)-1:
        raise ValueError("AttackMagic retarget RNG contains unused trailing rolls")
    return rolls


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
    ultimate_overkill_by_participant_id: dict[str,int],
    defense_profile: str,
    field_attr: str,
    field_power: int,
    ride_pet_runtime: RidePetRuntime | None = None,
) -> tuple[tuple[OrdinaryRoundEvent, ...], RidePetRuntime | None]:
    """Execute the stable base alternating BATTLE_Counter() loop.

    This is deliberately limited to the already-recovered status-free,
    no-guardian/no-reaction ordinary physical seam. Ride-pet sharing is part
    of the same source BATTLE_DamageSub call used here. The source permits at most
    five alternating attempts after a main attack's continuation flag remains
    true. Each successful counter uses BATTLE_AttackSeq-style dodge/critical/
    damage resolution, then scales positive damage to 75 percent.
    """
    supplied=tuple(counter_rolls)
    if len(supplied) > 5:
        raise ValueError("stable counter chain accepts at most five attempts")

    resolved: list[OrdinaryRoundEvent] = []
    ride_runtime=ride_pet_runtime
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

        if command_by_slot[actor_slot].command1 not in {
            BATTLE_COM_ATTACK,
            BATTLE_COM_S_NOGUARD,
        }:
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
                nonplayer_percent_modifier=_noguard_counter_percent_modifier(
                    command_by_slot[actor_slot]
                ),
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
                extra_percent_points=_noguard_dodge_percent_modifier(
                    command_by_slot[target_slot]
                ),
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

        ride_split=None
        ride_hp_resolution=None
        ride_pet_fell_rider_id=None
        event_damage=int(damage)
        if (
            int(damage)>0
            and ride_runtime is not None
            and ride_runtime.mounted
            and str(ride_runtime.rider_id)==target_id
        ):
            ride_split=ordinary_ride_damage_split(
                int(damage),
                rider_defense_power=int(target_defense),
                pet_defense_power=int(ride_runtime.defense_power),
                pet_hp=int(ride_runtime.hp),
            )
            ride_hp_resolution=apply_ride_damage(
                ride_split,
                rider_hp=int(before),
                rider_max_hp=int(target.max_hp),
                pet_hp=int(ride_runtime.hp),
                pet_max_hp=int(ride_runtime.max_hp),
            )
            after=int(ride_hp_resolution.rider_hp_after)
            event_damage=int(ride_split.rider_amount)
            if ride_hp_resolution.unmounted:
                ride_pet_fell_rider_id=str(ride_runtime.rider_id)
            ride_runtime=replace(
                ride_runtime,
                hp=int(ride_hp_resolution.pet_hp_after),
                mounted=(
                    False
                    if ride_hp_resolution.unmounted
                    else ride_runtime.mounted
                ),
                petfall=bool(
                    ride_runtime.petfall or ride_hp_resolution.petfall
                ),
            )
        else:
            after=max(0,before-int(damage))
        hp_by_slot[target_slot]=after
        hp_by_id[target_id]=after

        ultimate_damage_resolution=None
        death_ultimate_resolution=None
        ultimate_kind=0
        if int(damage)>0:
            ultimate_damage_resolution=resolve_battle_ultimate_damage(
                BattleUltimateDamageInputs(
                    damage_for_threshold=int(damage),
                    hp_damage_applied=max(0,int(before)-int(after)),
                    target_hp_before=int(before),
                    target_max_hp=int(target.max_hp),
                    accumulated_overkill_before=int(
                        ultimate_overkill_by_participant_id[target_id]
                    ),
                )
            )
            ultimate_overkill_by_participant_id[target_id]=int(
                ultimate_damage_resolution.accumulated_overkill_after
            )
            ultimate_kind=int(
                ultimate_damage_resolution.ultimate_kind
            )
            if int(before)>0 and int(after)<=0:
                victim_abio=bool(
                    counter_abio_by_participant_id.get(target_id,False)
                )
                victim_kind=_participant_battle_kind(target)
                needs_ultimate_roll=bool(
                    (not victim_abio)
                    and victim_kind != PLAYER
                    and is_critical
                )
                if (
                    rolls.ultimate_roll_1_100 is not None
                    and not needs_ultimate_roll
                ):
                    raise ValueError(
                        "counter ultimate_roll_1_100 supplied on unused "
                        "death path"
                    )
                death_ultimate_resolution=(
                    resolve_battle_death_ultimate_override(
                        BattleDeathUltimateInputs(
                            base_ultimate_kind=ultimate_kind,
                            victim_kind=victim_kind,
                            abio=victim_abio,
                            critical=bool(is_critical),
                        ),
                        critical_roll_1_100=(
                            rolls.ultimate_roll_1_100
                            if needs_ultimate_roll
                            else None
                        ),
                    )
                )
                ultimate_kind=int(
                    death_ultimate_resolution.ultimate_kind
                )
            elif rolls.ultimate_roll_1_100 is not None:
                raise ValueError(
                    "counter ultimate_roll_1_100 supplied without "
                    "non-player critical death"
                )
        elif rolls.ultimate_roll_1_100 is not None:
            raise ValueError(
                "counter ultimate_roll_1_100 supplied on zero-damage path"
            )

        if int(event_damage)>0:
            target_runtime=status_runtime_by_participant_id[target_id]
            wake=resolve_base_damage_wakeup(
                target_runtime.status,
                damage_count_before=target_runtime.damage_count,
                damage=int(event_damage),
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
                damage=int(event_damage),
                target_hp_before=before,
                target_hp_after=after,
                is_counter=True,
                counter_attempt=attempt_index + 1,
                counter_check_resolution=check,
                ride_damage_split=ride_split,
                ride_hp_resolution=ride_hp_resolution,
                ride_pet_fell_rider_id=ride_pet_fell_rider_id,
                ultimate_damage_resolution=ultimate_damage_resolution,
                death_ultimate_resolution=death_ultimate_resolution,
                ultimate_kind=int(ultimate_kind),
            )
        )

        if attack_seq_result in {"counter_miss","counter_critical"} or after <= 0:
            break

    return tuple(resolved),ride_runtime


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
    ride_pet_runtime: RidePetRuntime | None = None,
    ultimate_overkill_by_participant_id: dict[str,int] | None = None,
    battle_abio_by_participant_id: Mapping[str,bool] | None = None,
) -> tuple[tuple[OrdinaryRoundEvent, ...], RidePetRuntime | None]:
    """Execute the stable per-member Combo DamageReact path."""
    group=tuple(members)
    if ultimate_overkill_by_participant_id is None:
        ultimate_overkill_by_participant_id={
            str(participant.participant_id):0
            for participant in by_slot.values()
        }
    battle_abio_by_participant_id=dict(
        battle_abio_by_participant_id or {}
    )
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
    actor_ids=tuple(str(x.participant.participant_id) for x in group)
    slot_by_id={
        str(participant.participant_id):int(slot)
        for slot,participant in by_slot.items()
    }
    ride_runtime=ride_pet_runtime
    target_ride_active=bool(
        ride_runtime is not None
        and ride_runtime.mounted
        and target_id == ride_runtime.rider_id
    )

    resolved=[]
    accumulated=0
    accumulated_rider=0
    accumulated_pet=0
    accumulated_shared=False
    last_react=None
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
        last_react=react

        ride_split=None
        ride_hp_resolution=None
        ride_pet_fell_rider_id=None
        event_damage=contribution
        if ride_runtime is not None and ride_runtime.mounted:
            if (
                react.effective_kind == DAMAGE_REACT_ABSROB
                and target_id == ride_runtime.rider_id
            ):
                ride_split=immediate_reaction_ride_split(
                    contribution,
                    rider_defense_power=int(target.defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_heal(
                    ride_split,
                    rider_hp=int(react.defender_hp_before),
                    rider_max_hp=int(target.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                react=replace(
                    react,
                    defender_hp_after=int(ride_hp_resolution.rider_hp_after),
                )
                event_damage=int(ride_split.rider_amount)
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                )
            elif (
                react.effective_kind == DAMAGE_REACT_REFLEC
                and actor_id == ride_runtime.rider_id
            ):
                ride_split=immediate_reaction_ride_split(
                    contribution,
                    rider_defense_power=int(actor.defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_damage(
                    ride_split,
                    rider_hp=int(react.attacker_hp_before),
                    rider_max_hp=int(actor.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                react=replace(
                    react,
                    attacker_hp_after=int(ride_hp_resolution.rider_hp_after),
                )
                event_damage=int(ride_split.rider_amount)
                if ride_hp_resolution.unmounted:
                    ride_pet_fell_rider_id=ride_runtime.rider_id
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                    mounted=(
                        False
                        if ride_hp_resolution.unmounted
                        else ride_runtime.mounted
                    ),
                    petfall=bool(
                        ride_runtime.petfall or ride_hp_resolution.petfall
                    ),
                )

        if int(react.accumulated_damage)>0:
            deferred=int(react.accumulated_damage)
            accumulated+=deferred
            if target_ride_active and ride_runtime is not None:
                ride_split=combo_ride_damage_split(
                    deferred,
                    rider_defense_power=int(target.defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                accumulated_rider+=int(ride_split.rider_amount)
                accumulated_pet+=int(ride_split.pet_amount)
                accumulated_shared=bool(
                    accumulated_shared or ride_split.shared
                )
                event_damage=int(ride_split.rider_amount)
            else:
                accumulated_rider+=deferred

        hp_by_slot[actor_slot]=int(react.attacker_hp_after)
        hp_by_id[actor_id]=int(react.attacker_hp_after)
        hp_by_slot[int(target_slot)]=int(react.defender_hp_after)
        hp_by_id[target_id]=int(react.defender_hp_after)

        # The immediate BATTLE_DamageSub return is discarded by BATTLE_Combo,
        # but its internal WORKULTIMATE mutation still occurs. Preserve that
        # accumulator/reset side effect without turning the return into an
        # entry ultimate flag.
        immediate_ultimate_resolution=None
        immediate_damage_sub_called=bool(
            (
                react.selected_kind == DAMAGE_REACT_REFLEC
                and not react.reflect_blocked_by_throwing_weapon
            )
            or react.selected_kind in {
                DAMAGE_REACT_ABSROB,
                DAMAGE_REACT_VANISH,
            }
        )
        if immediate_damage_sub_called:
            if react.selected_kind == DAMAGE_REACT_REFLEC:
                immediate_target_id=actor_id
                immediate_before=int(react.attacker_hp_before)
                immediate_after=int(react.attacker_hp_after)
                immediate_max_hp=int(actor.max_hp)
            else:
                immediate_target_id=target_id
                immediate_before=int(react.defender_hp_before)
                immediate_after=int(react.defender_hp_after)
                immediate_max_hp=int(target.max_hp)
            immediate_ultimate_resolution=resolve_battle_ultimate_damage(
                BattleUltimateDamageInputs(
                    damage_for_threshold=int(contribution),
                    hp_damage_applied=max(
                        0,
                        immediate_before-immediate_after,
                    ),
                    target_hp_before=int(immediate_before),
                    target_max_hp=int(immediate_max_hp),
                    accumulated_overkill_before=int(
                        ultimate_overkill_by_participant_id[
                            immediate_target_id
                        ]
                    ),
                )
            )
            ultimate_overkill_by_participant_id[
                immediate_target_id
            ]=int(
                immediate_ultimate_resolution.accumulated_overkill_after
            )

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
                damage=int(event_damage),
                target_hp_before=event_before,
                target_hp_after=event_after,
                is_combo=True,
                combo_id=int(combo_id),
                combo_member_index=int(member_index),
                combo_damage_react_resolution=react,
                ride_damage_split=ride_split,
                ride_hp_resolution=ride_hp_resolution,
                ride_pet_fell_rider_id=ride_pet_fell_rider_id,
                ultimate_damage_resolution=immediate_ultimate_resolution,
            )
        )

    # BATTLE_DamageSub2 is assigned to the local ultimate variable only after
    # the final member. It receives reactions disabled (refrect=-1), so only
    # deferred/non-reacted Combo damage participates in this returned value.
    last=group[-1]
    last_id=str(last.participant.participant_id)
    last_slot=int(slot_by_id[last_id])
    last_roll=member_rolls[-1]
    last_is_critical=bool(resolved[-1].critical)
    if last_react is None:
        raise AssertionError("combo reaction execution produced no last reaction")

    settlement_ultimate_resolution=None
    settlement_death_ultimate_resolution=None
    settlement_ultimate_kind=0
    settlement_event_index=None

    if accumulated > 0:
        before=int(hp_by_slot[int(target_slot)])
        settlement_split=None
        settlement_hp=None
        ride_pet_fell_rider_id=None
        if target_ride_active and ride_runtime is not None:
            settlement_split=RideDamageSplit(
                int(accumulated),
                int(accumulated_rider),
                int(accumulated_pet),
                bool(accumulated_shared),
            )
            settlement_hp=apply_ride_damage(
                settlement_split,
                rider_hp=before,
                rider_max_hp=int(target.max_hp),
                pet_hp=int(ride_runtime.hp),
                pet_max_hp=int(ride_runtime.max_hp),
            )
            after=int(settlement_hp.rider_hp_after)
            if settlement_hp.unmounted:
                ride_pet_fell_rider_id=ride_runtime.rider_id
            ride_runtime=replace(
                ride_runtime,
                hp=int(settlement_hp.pet_hp_after),
                mounted=(
                    False
                    if settlement_hp.unmounted
                    else ride_runtime.mounted
                ),
                petfall=bool(
                    ride_runtime.petfall or settlement_hp.petfall
                ),
            )
            settlement_damage=int(settlement_split.rider_amount)
        else:
            after=max(0,before-int(accumulated))
            settlement_damage=int(accumulated)

        hp_by_slot[int(target_slot)]=after
        hp_by_id[target_id]=after
        settlement_ultimate_resolution=resolve_battle_ultimate_damage(
            BattleUltimateDamageInputs(
                damage_for_threshold=int(accumulated_rider),
                hp_damage_applied=max(0,int(before)-int(after)),
                target_hp_before=int(before),
                target_max_hp=int(target.max_hp),
                accumulated_overkill_before=int(
                    ultimate_overkill_by_participant_id[target_id]
                ),
            )
        )
        ultimate_overkill_by_participant_id[target_id]=int(
            settlement_ultimate_resolution.accumulated_overkill_after
        )
        settlement_ultimate_kind=int(
            settlement_ultimate_resolution.ultimate_kind
        )

        resolved.append(
            OrdinaryRoundEvent(
                last_id,
                last_slot,
                BATTLE_COM_COMBO,
                int(last.action_value),
                "combo_settlement",
                original_target_slot=int(original_target_slot),
                resolved_target_slot=int(target_slot),
                retargeted=bool(retargeted),
                damage=int(settlement_damage),
                target_hp_before=before,
                target_hp_after=after,
                is_combo=True,
                combo_id=int(combo_id),
                combo_settlement=True,
                profit_participant_ids=actor_ids,
                ride_damage_split=settlement_split,
                ride_hp_resolution=settlement_hp,
                ride_pet_fell_rider_id=ride_pet_fell_rider_id,
                ultimate_damage_resolution=settlement_ultimate_resolution,
            )
        )
        settlement_event_index=len(resolved)-1

    # Historical quirk: after DamageSub2 has already computed ultimate against
    # the original defender, stale REFLEC rewrites defindex=attackindex. The
    # death check and eventual BENT_FLG_ULTIMATE write then use that rewritten
    # entry. Throwing-weapon reflect bypass still leaves react==REFLEC here.
    death_check_slot=(
        last_slot
        if last_react.selected_kind == DAMAGE_REACT_REFLEC
        else int(target_slot)
    )
    death_check_target=by_slot[death_check_slot]
    death_check_id=str(death_check_target.participant_id)
    if int(hp_by_slot[death_check_slot]) <= 0:
        victim_abio=bool(
            battle_abio_by_participant_id.get(death_check_id,False)
        )
        needs_ultimate_roll=bool(
            (not victim_abio)
            and _participant_battle_kind(death_check_target) == ENEMY
            and last_is_critical
        )
        if (
            last_roll.ultimate_roll_1_100 is not None
            and not needs_ultimate_roll
        ):
            raise ValueError(
                "combo DamageReact ultimate_roll_1_100 supplied on unused "
                "death path"
            )
        settlement_death_ultimate_resolution=(
            resolve_battle_death_ultimate_override(
                BattleDeathUltimateInputs(
                    base_ultimate_kind=settlement_ultimate_kind,
                    victim_kind=_participant_battle_kind(death_check_target),
                    abio=victim_abio,
                    critical=last_is_critical,
                    critical_scope="enemy_only",
                ),
                critical_roll_1_100=(
                    last_roll.ultimate_roll_1_100
                    if needs_ultimate_roll
                    else None
                ),
            )
        )
        settlement_ultimate_kind=int(
            settlement_death_ultimate_resolution.ultimate_kind
        )
    elif last_roll.ultimate_roll_1_100 is not None:
        raise ValueError(
            "combo DamageReact ultimate_roll_1_100 supplied without "
            "enemy critical death"
        )

    flag_slot=(
        death_check_slot if settlement_ultimate_kind>0 else None
    )
    flag_kind=(
        int(settlement_ultimate_kind)
        if settlement_ultimate_kind>0
        else 0
    )
    if settlement_event_index is None:
        # DamageSub2(0) returns 0 and emits no distinct HP transaction in this
        # model. Attach the source final death-check/flag metadata to the last
        # member event so AddProfit can still observe the round-local flag.
        resolved[-1]=replace(
            resolved[-1],
            death_ultimate_resolution=settlement_death_ultimate_resolution,
            ultimate_kind=int(settlement_ultimate_kind),
            ultimate_flag_target_slot=flag_slot,
            ultimate_flag_kind=flag_kind,
        )
    else:
        resolved[settlement_event_index]=replace(
            resolved[settlement_event_index],
            death_ultimate_resolution=settlement_death_ultimate_resolution,
            ultimate_kind=int(settlement_ultimate_kind),
            ultimate_flag_target_slot=flag_slot,
            ultimate_flag_kind=flag_kind,
        )

    return tuple(resolved),ride_runtime


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
    ride_pet_runtime: RidePetRuntime | None = None,
    ultimate_overkill_by_participant_id: dict[str,int] | None = None,
    battle_abio_by_participant_id: Mapping[str,bool] | None = None,
) -> tuple[tuple[OrdinaryRoundEvent, ...], RidePetRuntime | None]:
    """Execute the status-free stable combo damage seam."""
    group=tuple(members)
    if ultimate_overkill_by_participant_id is None:
        ultimate_overkill_by_participant_id={
            str(entry.participant.participant_id):0
            for entry in group
        }
        target_pid=str(by_slot[int(target_slot)].participant_id)
        ultimate_overkill_by_participant_id.setdefault(target_pid,0)
    battle_abio_by_participant_id=dict(
        battle_abio_by_participant_id or {}
    )
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
            ride_pet_runtime=ride_pet_runtime,
            ultimate_overkill_by_participant_id=(
                ultimate_overkill_by_participant_id
            ),
            battle_abio_by_participant_id=battle_abio_by_participant_id,
        )
    actor_ids=tuple(
        str(entry.participant.participant_id) for entry in group
    )
    slot_by_actor_id={
        str(participant.participant_id):int(slot)
        for slot,participant in by_slot.items()
    }
    ride_runtime=ride_pet_runtime
    target_ride_active=bool(
        ride_runtime is not None
        and ride_runtime.mounted
        and target_id == ride_runtime.rider_id
    )

    rows=[]
    total_damage=0
    rider_damage=0
    pet_damage=0
    any_shared=False
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
        member_split=None
        event_damage=contribution
        if target_ride_active and ride_runtime is not None:
            member_split=combo_ride_damage_split(
                contribution,
                rider_defense_power=int(target.defense),
                pet_defense_power=int(ride_runtime.defense_power),
                pet_hp=int(ride_runtime.hp),
            )
            rider_damage+=int(member_split.rider_amount)
            pet_damage+=int(member_split.pet_amount)
            any_shared=bool(any_shared or member_split.shared)
            event_damage=int(member_split.rider_amount)
        else:
            rider_damage+=contribution

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
                event_damage,
                member_index,
                member_split,
            )
        )

    settlement_hp=None
    ride_pet_fell_rider_id=None
    if target_ride_active and ride_runtime is not None:
        aggregate=RideDamageSplit(
            int(total_damage),
            int(rider_damage),
            int(pet_damage),
            bool(any_shared),
        )
        settlement_hp=apply_ride_damage(
            aggregate,
            rider_hp=before,
            rider_max_hp=int(target.max_hp),
            pet_hp=int(ride_runtime.hp),
            pet_max_hp=int(ride_runtime.max_hp),
        )
        after=int(settlement_hp.rider_hp_after)
        if settlement_hp.unmounted:
            ride_pet_fell_rider_id=ride_runtime.rider_id
        ride_runtime=replace(
            ride_runtime,
            hp=int(settlement_hp.pet_hp_after),
            mounted=(
                False
                if settlement_hp.unmounted
                else ride_runtime.mounted
            ),
            petfall=bool(
                ride_runtime.petfall or settlement_hp.petfall
            ),
        )
    else:
        after=max(0,before-int(total_damage))
    hp_by_slot[int(target_slot)]=after
    hp_by_id[target_id]=after

    last_entry=group[-1]
    last_roll=member_rolls[-1]
    last_is_critical=bool(rows[-1][3])
    settlement_damage_for_ultimate=int(rider_damage)
    ultimate_damage_resolution=resolve_battle_ultimate_damage(
        BattleUltimateDamageInputs(
            damage_for_threshold=settlement_damage_for_ultimate,
            hp_damage_applied=max(0,int(before)-int(after)),
            target_hp_before=int(before),
            target_max_hp=int(target.max_hp),
            accumulated_overkill_before=int(
                ultimate_overkill_by_participant_id[target_id]
            ),
        )
    )
    ultimate_overkill_by_participant_id[target_id]=int(
        ultimate_damage_resolution.accumulated_overkill_after
    )
    ultimate_kind=int(ultimate_damage_resolution.ultimate_kind)
    death_ultimate_resolution=None
    if int(before) > 0 and int(after) <= 0:
        victim_abio=bool(
            battle_abio_by_participant_id.get(target_id,False)
        )
        needs_ultimate_roll=bool(
            (not victim_abio)
            and _participant_battle_kind(target) == ENEMY
            and last_is_critical
        )
        if (
            last_roll.ultimate_roll_1_100 is not None
            and not needs_ultimate_roll
        ):
            raise ValueError(
                "combo ultimate_roll_1_100 supplied on unused death path"
            )
        death_ultimate_resolution=resolve_battle_death_ultimate_override(
            BattleDeathUltimateInputs(
                base_ultimate_kind=ultimate_kind,
                victim_kind=_participant_battle_kind(target),
                abio=victim_abio,
                critical=last_is_critical,
                critical_scope="enemy_only",
            ),
            critical_roll_1_100=(
                last_roll.ultimate_roll_1_100
                if needs_ultimate_roll
                else None
            ),
        )
        ultimate_kind=int(death_ultimate_resolution.ultimate_kind)
    elif last_roll.ultimate_roll_1_100 is not None:
        raise ValueError(
            "combo ultimate_roll_1_100 supplied without enemy critical death"
        )

    resolved=[]
    for row_index,(
        entry,
        actor_slot,
        result,
        is_critical,
        event_damage,
        member_index,
        member_split,
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
                damage=int(event_damage),
                target_hp_before=before,
                target_hp_after=(after if is_last else before),
                is_combo=True,
                combo_id=int(combo_id),
                combo_member_index=int(member_index),
                profit_participant_ids=actor_ids,
                ride_damage_split=member_split,
                ride_hp_resolution=(settlement_hp if is_last else None),
                ride_pet_fell_rider_id=(
                    ride_pet_fell_rider_id if is_last else None
                ),
                ultimate_damage_resolution=(
                    ultimate_damage_resolution if is_last else None
                ),
                death_ultimate_resolution=(
                    death_ultimate_resolution if is_last else None
                ),
                ultimate_kind=(
                    int(ultimate_kind) if is_last else 0
                ),
            )
        )
    return tuple(resolved),ride_runtime


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


def _continuation_nonbow_target_for_hit(
    *,
    actor_slot: int,
    original_target_slot: int,
    by_slot: Mapping[int, BattleParticipant],
    hp_by_slot: Mapping[int, int],
    retarget_roll: int | None,
    excluded_slots: Sequence[int] = (),
) -> tuple[int | None,bool]:
    """Mirror non-bow S_RENZOKU's repeated original-target adjustment.

    BATTLE_TargetListSet fills every non-bow list entry with the originally
    submitted COM2.  Before every later hit battle.c writes that list entry
    back to COM2 and calls BATTLE_TargetAdjust.  Therefore once the original
    target dies, each remaining hit independently runs BATTLE_DefaultAttacker
    instead of sticking to the previous hit's retarget.
    """

    original=int(original_target_slot)
    excluded={int(slot) for slot in excluded_slots}
    original_alive=bool(
        original in by_slot
        and original not in excluded
        and int(hp_by_slot.get(original,0)) > 0
    )
    if original_alive:
        return original,False
    return (
        _retarget_slot(
            int(actor_slot),
            by_slot,
            hp_by_slot,
            retarget_roll,
            excluded_slots=excluded_slots,
        ),
        True,
    )


def _battle_attack_continuation_allowed(
    *,
    guardian_redirected: bool,
    damage_reaction_active: bool,
    critical: bool,
    target_guarding: bool,
    target_hp_after: int,
) -> bool:
    """Mirror the stable BATTLE_Attack boolean used to enter counter chaining."""

    return bool(
        not bool(guardian_redirected)
        and not bool(damage_reaction_active)
        and not bool(critical)
        and not bool(target_guarding)
        and int(target_hp_after) > 0
    )


@dataclass(frozen=True)
class ContinuationBaselineResolution:
    """Evidence-closed non-bow S_RENZOKU execution witness."""

    events: tuple[OrdinaryRoundEvent, ...]
    hp_by_slot: Mapping[int,int]
    last_target_slot: int | None
    counter_continuation_allowed: bool
    ride_pet_runtime: RidePetRuntime | None = None
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None
    base_damage_react_state_by_participant_id: Mapping[
        str,BaseDamageReactState
    ] | None = None
    ultimate_overkill_by_participant_id: Mapping[str,int] | None = None
    ultimate_exited_participant_ids: tuple[str, ...] = ()


def resolve_continuation_nonbow_baseline(
    *,
    actor: BattleParticipant,
    actor_slot: int,
    command: BattleCommand,
    action_value: int,
    by_slot: Mapping[int,BattleParticipant],
    hp_by_slot: Mapping[int,int],
    profiles: Mapping[str,BattleCombatProfile],
    command_by_slot: Mapping[int,BattleCommand],
    rolls: ContinuationAttackRolls,
    defense_profile: str,
    setup_effects_by_participant_id: Mapping[
        str,BattleCommandSetupEffects
    ] | None = None,
    guardian_registrations_by_defender_slot: Mapping[
        int,GuardianRegistration
    ] | None = None,
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None,
    base_damage_react_state_by_participant_id: Mapping[
        str,BaseDamageReactState
    ] | None = None,
    battle_abio_by_participant_id: Mapping[str,bool] | None = None,
    ultimate_overkill_by_participant_id: Mapping[str,int] | None = None,
    ride_pet_runtime: RidePetRuntime | None = None,
    excluded_slots: Sequence[int] = (),
    field_attr: str = "none",
    field_power: int = 0,
) -> ContinuationBaselineResolution:
    """Execute the evidence-closed non-bow S_RENZOKU baseline.

    This layer closes the fixed loop, per-hit original-target recheck,
    Guardian redirection, ordinary dodge/critical/guard damage, gDamageDiv,
    and the final BATTLE_Attack boolean used by the later counter chain.
    Damage-reaction, ride splitting, wakeup and ultimate/death handling are
    applied per hit because each can change later loop state, including actor
    death, petfall/unmount, target exit and the next retarget candidate set.
    ContinuationAttack itself adds no status-application payload.
    """

    if int(command.command1) != BATTLE_COM_S_RENZOKU:
        raise ValueError("continuation baseline requires S_RENZOKU command")
    actor_slot=int(actor_slot)
    if by_slot.get(actor_slot) != actor:
        raise ValueError("continuation actor/slot mapping mismatch")
    actor_id=str(actor.participant_id)
    if actor_id not in profiles:
        raise KeyError(f"missing combat profile for {actor_id}")
    count=battle_command3_low(command.command3)
    if not 1 <= count <= 10:
        raise ValueError("S_RENZOKU LOW(COM3) must be in 1..10")
    if len(rolls.hit_rolls) != count:
        raise ValueError(
            "ContinuationAttack requires exactly LOW(COM3) hit-roll bundles"
        )

    hp={int(slot):max(0,int(value)) for slot,value in hp_by_slot.items()}
    for slot,participant in by_slot.items():
        hp.setdefault(int(slot),max(0,int(participant.hp)))
    setup_effects=dict(setup_effects_by_participant_id or {})
    guardian_registrations={
        int(slot):registration
        for slot,registration in (
            guardian_registrations_by_defender_slot or {}
        ).items()
    }
    supplied_status_runtime={
        str(participant_id):runtime
        for participant_id,runtime in (
            base_status_runtime_by_participant_id or {}
        ).items()
    }
    status_runtime={
        str(participant.participant_id):supplied_status_runtime.get(
            str(participant.participant_id),
            BaseBattleStatusRuntime(),
        )
        for participant in by_slot.values()
    }
    damage_react_state={
        str(participant.participant_id):(
            base_damage_react_state_by_participant_id or {}
        ).get(
            str(participant.participant_id),
            BaseDamageReactState(),
        )
        for participant in by_slot.values()
    }
    battle_abio={
        str(participant_id):bool(value)
        for participant_id,value in (
            battle_abio_by_participant_id or {}
        ).items()
    }
    if ultimate_overkill_by_participant_id is None:
        ultimate_overkill={
            str(participant.participant_id):0
            for participant in by_slot.values()
        }
    else:
        ultimate_overkill={
            str(participant_id):int(value)
            for participant_id,value in (
                ultimate_overkill_by_participant_id or {}
            ).items()
        }
        expected_ids={
            str(participant.participant_id)
            for participant in by_slot.values()
        }
        if set(ultimate_overkill) != expected_ids:
            raise ValueError(
                "ContinuationAttack ultimate accumulator participants mismatch"
            )
        if any(value < 0 for value in ultimate_overkill.values()):
            raise ValueError("ultimate accumulator cannot be negative")
    ultimate_exited_ids: list[str]=[]
    excluded={int(slot) for slot in excluded_slots}
    ride_runtime=ride_pet_runtime
    active_ride=False
    if ride_runtime is not None:
        if not isinstance(ride_runtime,RidePetRuntime):
            raise TypeError("ride_pet_runtime must be RidePetRuntime or null")
        rider_id=str(ride_runtime.rider_id)
        rider_slot=next(
            (
                int(slot)
                for slot,participant in by_slot.items()
                if str(participant.participant_id)==rider_id
            ),
            None,
        )
        if rider_slot is None:
            raise ValueError("ride runtime rider is not an active battle entry")
        active_ride=bool(
            ride_runtime.mounted
            and int(hp.get(rider_slot,0)) > 0
            and int(ride_runtime.hp) > 0
        )
    original_target=int(command.command2)
    actor_profile=profiles[actor_id]
    resolved: list[OrdinaryRoundEvent]=[]
    last_target: int | None=None
    last_continue=False

    for hit_rolls in rolls.hit_rolls:
        if int(hp.get(actor_slot,0)) <= 0:
            last_continue=False
            break

        target,retargeted=_continuation_nonbow_target_for_hit(
            actor_slot=actor_slot,
            original_target_slot=original_target,
            by_slot=by_slot,
            hp_by_slot=hp,
            retarget_roll=hit_rolls.retarget_roll,
            excluded_slots=excluded,
        )
        if target is None:
            last_target=None
            last_continue=False
            break
        target=int(target)
        if _slot_side(target)==_slot_side(actor_slot):
            raise ValueError("ContinuationAttack retarget crossed battle sides")

        original_defender=by_slot[target]
        original_defender_id=str(original_defender.participant_id)
        if original_defender_id not in profiles:
            raise KeyError(
                f"missing combat profile for {original_defender_id}"
            )
        original_defender_profile=profiles[original_defender_id]
        original_before=int(hp[target])
        original_guarding=bool(
            target in command_by_slot
            and int(command_by_slot[target].command1)==BATTLE_COM_GUARD
        )
        continuation_blocked_by_reaction=(
            base_damage_react_blocks_main_continuation(
                damage_react_state[actor_id],
                damage_react_state[original_defender_id],
            )
        )

        # BATTLE_AttackSeq performs dodge against the original/adjusted target
        # before BATTLE_GuardianCheck may redirect the damage calculation.
        if not original_guarding:
            dodge_roll=_validated_roll(
                hit_rolls.dodge_roll_1_10000,
                1,10000,
                "continuation dodge_roll_1_10000",
            )
            dodge_probability=dodge_per_10000(
                actor_profile.fixed_dex,
                original_defender_profile.fixed_dex,
                defender_luck=_source_luck(
                    original_defender,
                    original_defender_profile,
                ),
                attacker_type=_participant_battle_kind(actor),
                defender_type=_participant_battle_kind(original_defender),
                extra_percent_points=_noguard_dodge_percent_modifier(
                    command_by_slot.get(
                        target,
                        BattleCommand(BATTLE_COM_NONE),
                    )
                ),
            )
            if dodge_roll <= dodge_probability:
                resolved.append(
                    OrdinaryRoundEvent(
                        actor_id,
                        actor_slot,
                        BATTLE_COM_S_RENZOKU,
                        int(action_value),
                        "continuation_dodge",
                        original_target_slot=original_target,
                        resolved_target_slot=target,
                        retargeted=bool(retargeted),
                        target_hp_before=original_before,
                        target_hp_after=original_before,
                    )
                )
                last_target=target
                last_continue=not continuation_blocked_by_reaction
                continue

        counter_target=target
        damage_target=target
        guardian_redirected=False
        guarded_target_slot=None
        guardian_slot=None
        registration=guardian_registrations.get(target)
        if registration is not None:
            candidate_slot=int(registration.guardian_slot)
            candidate=by_slot.get(candidate_slot)
            candidate_runtime=(
                None
                if candidate is None
                else status_runtime.get(
                    str(candidate.participant_id),
                    BaseBattleStatusRuntime(),
                )
            )
            if guardian_redirect_allowed(
                guardian_exists=(
                    candidate is not None
                    and candidate_slot not in excluded
                ),
                guardian_slot=candidate_slot,
                defender_slot=target,
                guardian_alive=(
                    candidate is not None
                    and candidate_slot not in excluded
                    and int(hp.get(candidate_slot,0)) > 0
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
                guardian_is_attacker=(candidate_slot==actor_slot),
                attacker_uses_throw_weapon=counter_weapon_blocks_counter(
                    actor_profile.counter_weapon_type
                ),
            ):
                guardian_redirected=True
                guarded_target_slot=target
                guardian_slot=candidate_slot
                damage_target=candidate_slot

        defender=by_slot[damage_target]
        defender_id=str(defender.participant_id)
        if defender_id not in profiles:
            raise KeyError(f"missing combat profile for {defender_id}")
        defender_profile=profiles[defender_id]
        before=int(hp[damage_target])
        damage_target_guarding=bool(
            damage_target in command_by_slot
            and int(command_by_slot[damage_target].command1)==BATTLE_COM_GUARD
        )

        critical_roll=_validated_roll(
            hit_rolls.critical_roll_1_10000,
            1,10000,
            "continuation critical_roll_1_10000",
        )
        critical_probability=critical_per_10000(
            actor_profile.fixed_dex,
            defender_profile.fixed_dex,
            attacker_luck=_source_luck(actor,actor_profile),
            weapon_critical=int(actor_profile.weapon_critical),
            attacker_type=_participant_battle_kind(actor),
            defender_type=_participant_battle_kind(defender),
        )
        is_critical=critical_roll < critical_probability

        defender_work_defense=_effective_defense_power(defender,setup_effects)
        base_damage=physical_base_damage(
            _effective_attack_power(actor,setup_effects),
            _effective_defense_for_round(
                defender,
                defense_profile,
                stone=False,
                work_defense=defender_work_defense,
            ),
            int(hit_rolls.damage_roll),
        )
        damage=attribute_adjusted_damage(
            base_damage,
            actor_profile.elements,
            defender_profile.elements,
            field_attr=field_attr,
            field_power=field_power,
        )
        if is_critical:
            damage=critical_damage(
                damage,
                defender_work_defense,
                actor.level,
                defender.level,
            )
        if damage_target_guarding:
            guard_roll=_validated_roll(
                hit_rolls.guard_roll_1_100,
                1,100,
                "continuation guard_roll_1_100",
            )
            damage=guard_damage(damage,guard_roll)
        if damage < 1:
            damage=_validated_roll(
                hit_rolls.minimum_damage_roll_0_1,
                0,1,
                "continuation minimum_damage_roll_0_1",
            )

        # Fixed BATTLE_Attack applies gDamageDiv after AttackSeq (including
        # Guardian/critical/guard) and before BATTLE_DamageSub.
        damage=continuation_divided_damage(damage,count)
        if damage == 0 and guardian_redirected:
            # AttackSeq's redirected zero-damage path is rendered as NORMAL/1.
            damage=1
            result="continuation_normal"
        elif damage == 0:
            result=(
                "continuation_allguard"
                if damage_target_guarding
                else "continuation_miss"
            )
        else:
            result=(
                "continuation_critical"
                if is_critical
                else "continuation_normal"
            )

        reaction_resolution=resolve_base_damage_react(
            damage_react_state[defender_id],
            raw_damage=int(damage),
            attacker_hp=int(hp[actor_slot]),
            attacker_max_hp=int(actor.max_hp),
            defender_hp=int(hp[damage_target]),
            defender_max_hp=int(defender.max_hp),
            attacker_uses_throwing_weapon=counter_weapon_blocks_counter(
                actor_profile.counter_weapon_type
            ),
        )
        damage_react_state[defender_id]=reaction_resolution.state_after

        ride_split=None
        ride_hp_resolution=None
        ride_pet_fell_rider_id=None
        event_damage=int(damage)
        if active_ride and ride_runtime is not None:
            rider_id=str(ride_runtime.rider_id)
            if (
                reaction_resolution.effective_kind == DAMAGE_REACT_ABSROB
                and defender_id == rider_id
            ):
                ride_split=immediate_reaction_ride_split(
                    int(damage),
                    rider_defense_power=int(defender_work_defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_heal(
                    ride_split,
                    rider_hp=int(reaction_resolution.defender_hp_before),
                    rider_max_hp=int(defender.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                reaction_resolution=replace(
                    reaction_resolution,
                    defender_hp_after=int(
                        ride_hp_resolution.rider_hp_after
                    ),
                )
                event_damage=int(ride_split.rider_amount)
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                )
            elif (
                reaction_resolution.effective_kind == DAMAGE_REACT_REFLEC
                and actor_id == rider_id
            ):
                actor_work_defense=_effective_defense_power(
                    actor,setup_effects
                )
                ride_split=immediate_reaction_ride_split(
                    int(damage),
                    rider_defense_power=int(actor_work_defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_damage(
                    ride_split,
                    rider_hp=int(reaction_resolution.attacker_hp_before),
                    rider_max_hp=int(actor.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                reaction_resolution=replace(
                    reaction_resolution,
                    attacker_hp_after=int(
                        ride_hp_resolution.rider_hp_after
                    ),
                )
                event_damage=int(ride_split.rider_amount)
                if ride_hp_resolution.unmounted:
                    ride_pet_fell_rider_id=ride_runtime.rider_id
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                    mounted=(
                        False
                        if ride_hp_resolution.unmounted
                        else ride_runtime.mounted
                    ),
                    petfall=bool(
                        ride_runtime.petfall or ride_hp_resolution.petfall
                    ),
                )
                active_ride=bool(ride_runtime.mounted)
            elif (
                reaction_resolution.damage_target == "defender"
                and defender_id == rider_id
            ):
                ride_split=ordinary_ride_damage_split(
                    int(damage),
                    rider_defense_power=int(defender_work_defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_damage(
                    ride_split,
                    rider_hp=int(reaction_resolution.defender_hp_before),
                    rider_max_hp=int(defender.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                reaction_resolution=replace(
                    reaction_resolution,
                    defender_hp_after=int(
                        ride_hp_resolution.rider_hp_after
                    ),
                )
                event_damage=int(ride_split.rider_amount)
                if ride_hp_resolution.unmounted:
                    ride_pet_fell_rider_id=ride_runtime.rider_id
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                    mounted=(
                        False
                        if ride_hp_resolution.unmounted
                        else ride_runtime.mounted
                    ),
                    petfall=bool(
                        ride_runtime.petfall or ride_hp_resolution.petfall
                    ),
                )
                active_ride=bool(ride_runtime.mounted)

        hp[actor_slot]=int(reaction_resolution.attacker_hp_after)
        hp[damage_target]=int(reaction_resolution.defender_hp_after)

        if reaction_resolution.effective_kind == DAMAGE_REACT_REFLEC:
            resolved_damage_slot=actor_slot
            event_before=int(reaction_resolution.attacker_hp_before)
            event_after=int(reaction_resolution.attacker_hp_after)
        else:
            resolved_damage_slot=damage_target
            event_before=int(reaction_resolution.defender_hp_before)
            event_after=int(reaction_resolution.defender_hp_after)

        resolved_damage_id=str(
            by_slot[resolved_damage_slot].participant_id
        )
        ultimate_damage_resolution=None
        death_ultimate_resolution=None
        ultimate_kind=0
        if int(damage) > 0:
            hp_damage_applied=max(0,int(event_before)-int(event_after))
            ultimate_damage_resolution=resolve_battle_ultimate_damage(
                BattleUltimateDamageInputs(
                    damage_for_threshold=int(damage),
                    hp_damage_applied=int(hp_damage_applied),
                    target_hp_before=int(event_before),
                    target_max_hp=int(
                        by_slot[resolved_damage_slot].max_hp
                    ),
                    accumulated_overkill_before=int(
                        ultimate_overkill[resolved_damage_id]
                    ),
                )
            )
            ultimate_overkill[resolved_damage_id]=int(
                ultimate_damage_resolution.accumulated_overkill_after
            )
            ultimate_kind=int(
                ultimate_damage_resolution.ultimate_kind
            )
            if int(event_before) > 0 and int(event_after) <= 0:
                victim=by_slot[resolved_damage_slot]
                victim_kind=_participant_battle_kind(victim)
                victim_abio=bool(
                    battle_abio.get(resolved_damage_id,False)
                )
                needs_ultimate_roll=bool(
                    (not victim_abio)
                    and victim_kind != PLAYER
                    and is_critical
                )
                if (
                    hit_rolls.ultimate_roll_1_100 is not None
                    and not needs_ultimate_roll
                ):
                    raise ValueError(
                        "continuation ultimate_roll_1_100 supplied "
                        "on unused death path"
                    )
                death_ultimate_resolution=(
                    resolve_battle_death_ultimate_override(
                        BattleDeathUltimateInputs(
                            base_ultimate_kind=ultimate_kind,
                            victim_kind=victim_kind,
                            abio=victim_abio,
                            critical=bool(is_critical),
                        ),
                        critical_roll_1_100=(
                            hit_rolls.ultimate_roll_1_100
                            if needs_ultimate_roll
                            else None
                        ),
                    )
                )
                ultimate_kind=int(
                    death_ultimate_resolution.ultimate_kind
                )
            elif hit_rolls.ultimate_roll_1_100 is not None:
                raise ValueError(
                    "continuation ultimate_roll_1_100 supplied "
                    "when no non-player critical death consumed it"
                )
        elif hit_rolls.ultimate_roll_1_100 is not None:
            raise ValueError(
                "continuation ultimate_roll_1_100 supplied on zero-damage path"
            )

        if (
            int(damage) > 0
            and reaction_resolution.wakeup_target is not None
        ):
            wake_target_id=(
                actor_id
                if reaction_resolution.wakeup_target == "attacker"
                else defender_id
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

        resolved.append(
            OrdinaryRoundEvent(
                actor_id,
                actor_slot,
                BATTLE_COM_S_RENZOKU,
                int(action_value),
                result,
                original_target_slot=original_target,
                resolved_target_slot=resolved_damage_slot,
                retargeted=bool(retargeted),
                critical=bool(is_critical),
                damage=int(event_damage),
                target_hp_before=event_before,
                target_hp_after=event_after,
                guardian_redirected=guardian_redirected,
                guarded_target_slot=guarded_target_slot,
                guardian_slot=guardian_slot,
                damage_react_resolution=reaction_resolution,
                ride_damage_split=ride_split,
                ride_hp_resolution=ride_hp_resolution,
                ride_pet_fell_rider_id=ride_pet_fell_rider_id,
                ultimate_damage_resolution=ultimate_damage_resolution,
                death_ultimate_resolution=death_ultimate_resolution,
                ultimate_kind=int(ultimate_kind),
            )
        )
        counter_target_hp_after_attack=int(hp.get(counter_target,0))
        last_target=counter_target
        last_continue=_battle_attack_continuation_allowed(
            guardian_redirected=guardian_redirected,
            damage_reaction_active=continuation_blocked_by_reaction,
            critical=bool(is_critical),
            target_guarding=original_guarding,
            target_hp_after=counter_target_hp_after_attack,
        )

        if (
            int(event_before) > 0
            and int(event_after) <= 0
            and int(ultimate_kind) > 0
        ):
            exit_slot=int(resolved_damage_slot)
            exit_actor=by_slot[exit_slot]
            exit_id=str(exit_actor.participant_id)
            if exit_id not in ultimate_exited_ids:
                excluded.add(exit_slot)
                ultimate_exited_ids.append(exit_id)

                if exit_actor.kind == "player":
                    active_allied=[
                        (other_slot,other)
                        for other_slot,other in by_slot.items()
                        if (
                            other.side == exit_actor.side
                            and other.kind == "pet"
                            and str(other.participant_id)
                            not in ultimate_exited_ids
                            and int(other_slot) not in excluded
                        )
                    ]
                    if len(active_allied) > 1:
                        raise ValueError(
                            "player ultimate exit requires a unique "
                            "active/default pet"
                        )
                    if active_allied:
                        pet_slot,pet=active_allied[0]
                        excluded.add(int(pet_slot))
                        ultimate_exited_ids.append(
                            str(pet.participant_id)
                        )

                    hp[exit_slot]=1
                    status_runtime[exit_id]=BaseBattleStatusRuntime(
                        work_quick=int(exit_actor.quick)
                    )
                    for other_slot,other in by_slot.items():
                        if (
                            other.side != exit_actor.side
                            or other.kind != "pet"
                        ):
                            continue
                        other_id=str(other.participant_id)
                        if int(hp.get(int(other_slot),0)) <= 0:
                            hp[int(other_slot)]=1
                        status_runtime[other_id]=BaseBattleStatusRuntime(
                            work_quick=int(other.quick)
                        )

                    if (
                        ride_runtime is not None
                        and str(ride_runtime.rider_id)==exit_id
                        and ride_runtime.petfall
                    ):
                        ride_runtime=replace(
                            ride_runtime,
                            mounted=False,
                            petfall=False,
                        )
                        active_ride=False

    return ContinuationBaselineResolution(
        events=tuple(resolved),
        hp_by_slot=MappingProxyType(dict(hp)),
        last_target_slot=last_target,
        counter_continuation_allowed=bool(last_continue),
        ride_pet_runtime=ride_runtime,
        base_status_runtime_by_participant_id=MappingProxyType(
            dict(status_runtime)
        ),
        base_damage_react_state_by_participant_id=MappingProxyType(
            dict(damage_react_state)
        ),
        ultimate_overkill_by_participant_id=MappingProxyType(
            dict(ultimate_overkill)
        ),
        ultimate_exited_participant_ids=tuple(ultimate_exited_ids),
    )


def resolve_ordinary_round(
    prepared: PreparedBattleRound,
    *,
    slots: Mapping[str, int],
    profiles: Mapping[str, BattleCombatProfile],
    attack_rolls: Mapping[str, OrdinaryAttackRolls],
    defense_profile: str,
    capture_contexts: Mapping[str, OrdinaryCaptureContext] | None = None,
    capture_rolls: Mapping[str, OrdinaryCaptureRolls] | None = None,
    abduct_contexts: Mapping[str, OrdinaryAbductContext] | None = None,
    abduct_rolls: Mapping[str, OrdinaryAbductRolls] | None = None,
    steal_rolls: Mapping[str, OrdinaryStealRolls] | None = None,
    steal_player_gold_by_participant_id: Mapping[str,int] | None = None,
    steal_player_item_slots_by_participant_id: Mapping[
        str,Sequence[int]
    ] | None = None,
    escape_contexts: Mapping[str, OrdinaryEscapeContext] | None = None,
    escape_rolls: Mapping[str, OrdinaryEscapeRolls] | None = None,
    counter_rolls_by_attack_id: Mapping[
        str,Sequence[CounterAttemptRolls]
    ] | None = None,
    counter_abio_by_participant_id: Mapping[str,bool] | None = None,
    battle_abio_by_participant_id: Mapping[str,bool] | None = None,
    ultimate_overkill_by_participant_id: Mapping[str,int] | None = None,
    combo_rolls_by_starter_id: Mapping[
        str,ComboExecutionRolls
    ] | None = None,
    continuation_rolls_by_attack_id: Mapping[
        str,ContinuationAttackRolls
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
    ride_pet_runtime: RidePetRuntime | None = None,
    attack_magic_runtime: Recovered25AttackMagicRuntime | None = None,
    attack_magic_submissions_by_participant_id: Mapping[
        str,EnemyAiAttackMagicSubmission
    ] | None = None,
    attack_magic_rolls_by_participant_id: Mapping[
        str,EnemyAttackMagicActionRolls
    ] | None = None,
    attack_magic_overlay: AttackMagicRoundOverlay | None = None,
    attack_magic_retarget_rolls_by_participant_id: Mapping[
        str,Sequence[int]
    ] | None = None,
    enemy_rehp_submissions_by_participant_id: Mapping[
        str,EnemyAiReHpSubmission
    ] | None = None,
    enemy_rehp_rolls_by_participant_id: Mapping[
        str,EnemyReHpRolls
    ] | None = None,
    enemy_rehp_retarget_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    damage_to_hp_submissions_by_participant_id: Mapping[
        str,EnemyAiDamageToHpSubmission
    ] | None = None,
    mp_damage_submissions_by_participant_id: Mapping[
        str,EnemyAiMpDamageSubmission
    ] | None = None,
    mp_by_participant_id: Mapping[str,int] | None = None,
    battle_tear_submissions_by_participant_id: Mapping[
        str,EnemyAiBattleTearSubmission
    ] | None = None,
    guard_break2_submissions_by_participant_id: Mapping[
        str,EnemyAiGuardBreak2Submission
    ] | None = None,
    fall_ground_submissions_by_participant_id: Mapping[
        str,EnemyAiFallGroundSubmission
    ] | None = None,
    fall_ground_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    fall_ground_equipment_resistance_by_participant_id: Mapping[
        str,int
    ] | None = None,
    nocast_submissions_by_participant_id: Mapping[
        str,EnemyAiNocastSubmission
    ] | None = None,
    nocast_rolls_by_participant_id: Mapping[
        str,NocastActionRolls
    ] | None = None,
    barrier_submissions_by_participant_id: Mapping[
        str,EnemyAiBarrierSubmission
    ] | None = None,
    barrier_rolls_by_participant_id: Mapping[
        str,BarrierActionRolls
    ] | None = None,
    nocast_overlay: NocastRoundOverlay | None = None,
    ride_pet_source_slot: int | None = None,
    field_attr: str = "none",
    field_power: int = 0,
) -> ResolvedOrdinaryRound:
    """Execute the status-free base battle seam.

    Passing counter_rolls_by_attack_id enables the recovered base counter loop.
    Prepared COMBO groups additionally require combo_rolls_by_starter_id;
    S_RENZOKU requires continuation_rolls_by_attack_id. Guard
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

    attack_magic_actor_ids={
        str(entry.participant.participant_id)
        for entry in prepared.ordered_entries
        if int(entry.command.command1) == BATTLE_COM_S_ATTACK_MAGIC
    }
    attack_magic_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            attack_magic_submissions_by_participant_id or {}
        ).items()
    }
    if set(attack_magic_submissions) != attack_magic_actor_ids:
        missing=sorted(attack_magic_actor_ids-set(attack_magic_submissions))
        extra=sorted(set(attack_magic_submissions)-attack_magic_actor_ids)
        raise ValueError(
            "AttackMagic submissions must match command-2002 actors; "
            f"missing={missing}, extra={extra}"
        )
    for participant_id,submission in attack_magic_submissions.items():
        if not isinstance(submission,EnemyAiAttackMagicSubmission):
            raise TypeError(
                f"AttackMagic submission for {participant_id} has wrong type"
            )
    if attack_magic_actor_ids and attack_magic_runtime is None:
        raise ValueError("command 2002 requires recovered25 AttackMagic runtime")
    if (
        attack_magic_runtime is not None
        and not isinstance(attack_magic_runtime,Recovered25AttackMagicRuntime)
    ):
        raise TypeError("attack_magic_runtime has wrong type")
    if attack_magic_actor_ids and attack_magic_overlay is None:
        raise ValueError("command 2002 requires AttackMagic round overlay")
    if (
        attack_magic_overlay is not None
        and not isinstance(attack_magic_overlay,AttackMagicRoundOverlay)
    ):
        raise TypeError("attack_magic_overlay has wrong type")
    attack_magic_working=(
        None
        if attack_magic_overlay is None
        else dict(attack_magic_overlay.resistance_by_participant_id)
    )
    attack_magic_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            attack_magic_rolls_by_participant_id or {}
        ).items()
    }
    unknown_attack_magic_roll_ids=sorted(
        set(attack_magic_rolls)-attack_magic_actor_ids
    )
    if unknown_attack_magic_roll_ids:
        raise ValueError(
            "AttackMagic RNG references non-2002 actors: "
            f"{unknown_attack_magic_roll_ids}"
        )
    for participant_id,magic_rolls in attack_magic_rolls.items():
        if not isinstance(magic_rolls,EnemyAttackMagicActionRolls):
            raise TypeError(
                f"AttackMagic RNG for {participant_id} has wrong type"
            )
    attack_magic_retarget_rolls={
        str(participant_id):tuple(int(x) for x in values)
        for participant_id,values in (
            attack_magic_retarget_rolls_by_participant_id or {}
        ).items()
    }
    unknown_attack_magic_retarget_ids=sorted(
        set(attack_magic_retarget_rolls)-attack_magic_actor_ids
    )
    if unknown_attack_magic_retarget_ids:
        raise ValueError(
            "AttackMagic retarget RNG references non-2002 actors: "
            f"{unknown_attack_magic_retarget_ids}"
        )
    consumed_attack_magic_roll_ids=set()

    # ReHP uses a typed semantic submission because the recovered25 guarded
    # numeric COM1 is unproven. Its BattleCommand is ordinary ATTACK only as
    # an internal initiative/ordering carrier; execution is intercepted below.
    enemy_rehp_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            enemy_rehp_submissions_by_participant_id or {}
        ).items()
    }
    enemy_rehp_actor_ids=set(enemy_rehp_submissions)
    unknown_rehp_ids=sorted(enemy_rehp_actor_ids-set(slot_by_id))
    if unknown_rehp_ids:
        raise ValueError(
            f"enemy ReHP submissions reference unknown actors: {unknown_rehp_ids}"
        )
    if enemy_rehp_actor_ids & attack_magic_actor_ids:
        raise ValueError("enemy ReHP and AttackMagic submissions overlap")
    prepared_entry_by_id={
        str(entry.participant.participant_id):entry
        for entry in prepared.ordered_entries
    }
    for participant_id,submission in enemy_rehp_submissions.items():
        if not isinstance(submission,EnemyAiReHpSubmission):
            raise TypeError(
                f"enemy ReHP submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("enemy ReHP submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError("reconstructed ReHP currently admits enemy actors only")
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "enemy ReHP ordering carrier must be ATTACK with source target"
            )

    enemy_rehp_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            enemy_rehp_rolls_by_participant_id or {}
        ).items()
    }
    if set(enemy_rehp_rolls) != enemy_rehp_actor_ids:
        missing=sorted(enemy_rehp_actor_ids-set(enemy_rehp_rolls))
        extra=sorted(set(enemy_rehp_rolls)-enemy_rehp_actor_ids)
        raise ValueError(
            "enemy ReHP effect RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    for participant_id,rolls in enemy_rehp_rolls.items():
        if not isinstance(rolls,EnemyReHpRolls):
            raise TypeError(
                f"enemy ReHP effect RNG for {participant_id} has wrong type"
            )
    enemy_rehp_retarget_rolls={
        str(participant_id):(
            None if value is None else int(value)
        )
        for participant_id,value in (
            enemy_rehp_retarget_rolls_by_participant_id or {}
        ).items()
    }
    if set(enemy_rehp_retarget_rolls) != enemy_rehp_actor_ids:
        missing=sorted(enemy_rehp_actor_ids-set(enemy_rehp_retarget_rolls))
        extra=sorted(set(enemy_rehp_retarget_rolls)-enemy_rehp_actor_ids)
        raise ValueError(
            "enemy ReHP TargetAdjust RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    attempted_enemy_rehp_actor_ids=set()

    damage_to_hp_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            damage_to_hp_submissions_by_participant_id or {}
        ).items()
    }
    damage_to_hp_actor_ids=set(damage_to_hp_submissions)
    unknown_damage_to_hp_ids=sorted(damage_to_hp_actor_ids-set(slot_by_id))
    if unknown_damage_to_hp_ids:
        raise ValueError(
            "DamageToHp submissions reference unknown actors: "
            f"{unknown_damage_to_hp_ids}"
        )
    if damage_to_hp_actor_ids & (
        enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("DamageToHp semantic submissions overlap another skill")
    for participant_id,submission in damage_to_hp_submissions.items():
        if not isinstance(submission,EnemyAiDamageToHpSubmission):
            raise TypeError(
                f"DamageToHp submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("DamageToHp submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError(
                "recovered25 DamageToHp currently admits enemy actors only"
            )
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "DamageToHp ordering carrier must be ATTACK/source-target"
            )

    mp_damage_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            mp_damage_submissions_by_participant_id or {}
        ).items()
    }
    mp_damage_actor_ids=set(mp_damage_submissions)
    unknown_mp_damage_ids=sorted(mp_damage_actor_ids-set(slot_by_id))
    if unknown_mp_damage_ids:
        raise ValueError(
            f"MpDamage submissions reference unknown actors: {unknown_mp_damage_ids}"
        )
    if mp_damage_actor_ids & (
        damage_to_hp_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("MpDamage semantic submissions overlap another skill")
    for participant_id,submission in mp_damage_submissions.items():
        if not isinstance(submission,EnemyAiMpDamageSubmission):
            raise TypeError(
                f"MpDamage submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("MpDamage submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError("recovered25 MpDamage currently admits enemy actors only")
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "MpDamage ordering carrier must be ATTACK/source-target"
            )

    mp_working={
        str(participant_id):int(value)
        for participant_id,value in (mp_by_participant_id or {}).items()
    }
    unknown_mp_state=sorted(set(mp_working)-set(slot_by_id))
    if unknown_mp_state:
        raise ValueError(
            f"MpDamage MP state references unknown actors: {unknown_mp_state}"
        )
    if any(value < 0 for value in mp_working.values()):
        raise ValueError("MpDamage MP state cannot be negative")

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

    battle_tear_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            battle_tear_submissions_by_participant_id or {}
        ).items()
    }
    battle_tear_actor_ids=set(battle_tear_submissions)
    unknown_battle_tear_ids=sorted(battle_tear_actor_ids-set(slot_by_id))
    if unknown_battle_tear_ids:
        raise ValueError(
            "BattleTear submissions reference unknown actors: "
            f"{unknown_battle_tear_ids}"
        )
    if battle_tear_actor_ids & (
        mp_damage_actor_ids | damage_to_hp_actor_ids
        | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("BattleTear semantic submissions overlap another skill")
    for participant_id,submission in battle_tear_submissions.items():
        if not isinstance(submission,EnemyAiBattleTearSubmission):
            raise TypeError(
                f"BattleTear submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("BattleTear submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError(
                "recovered25 BattleTear currently admits enemy actors only"
            )
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "BattleTear ordering carrier must be ATTACK/source-target"
            )
        expected_setup=submission.callback_setup(
            fixed_strength=int(entry.participant.attack),
            fixed_toughness=int(entry.participant.defense),
        )
        effects=setup_effects.get(participant_id,BattleCommandSetupEffects())
        if (
            effects.attack_power is None
            or int(effects.attack_power) != int(expected_setup.attack_power)
            or effects.defense_power is None
            or int(effects.defense_power) != int(expected_setup.defense_power)
        ):
            raise ValueError(
                "BattleTear callback attack/defense setup effect drift"
            )

    fall_ground_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            fall_ground_submissions_by_participant_id or {}
        ).items()
    }
    fall_ground_actor_ids=set(fall_ground_submissions)
    unknown_fall_ground_ids=sorted(fall_ground_actor_ids-set(slot_by_id))
    if unknown_fall_ground_ids:
        raise ValueError(
            "FallGround submissions reference unknown actors: "
            f"{unknown_fall_ground_ids}"
        )
    if fall_ground_actor_ids & (
        battle_tear_actor_ids | mp_damage_actor_ids | damage_to_hp_actor_ids
        | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("FallGround semantic submissions overlap another skill")
    for participant_id,submission in fall_ground_submissions.items():
        if not isinstance(submission,EnemyAiFallGroundSubmission):
            raise TypeError(
                f"FallGround submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("FallGround submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError(
                "recovered25 FallGround currently admits enemy actors only"
            )
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "FallGround ordering carrier must be ATTACK/source-target"
            )
        expected_attack=submission.callback_attack_power(
            int(entry.participant.attack)
        )
        effects=setup_effects.get(
            participant_id,
            BattleCommandSetupEffects(),
        )
        if effects.attack_power is None or int(effects.attack_power) != expected_attack:
            raise ValueError(
                "FallGround callback attack-power setup effect drift"
            )

    fall_ground_rolls={
        str(participant_id):(
            None if value is None else int(value)
        )
        for participant_id,value in (
            fall_ground_rolls_by_participant_id or {}
        ).items()
    }
    if set(fall_ground_rolls) != fall_ground_actor_ids:
        missing=sorted(fall_ground_actor_ids-set(fall_ground_rolls))
        extra=sorted(set(fall_ground_rolls)-fall_ground_actor_ids)
        raise ValueError(
            "FallGround RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    for participant_id,value in fall_ground_rolls.items():
        if value is not None and not 0 <= value <= 100:
            raise ValueError(
                f"FallGround RNG for {participant_id} must be 0..100 or None"
            )

    fall_ground_resistance={
        str(participant_id):int(value)
        for participant_id,value in (
            fall_ground_equipment_resistance_by_participant_id or {}
        ).items()
    }
    expected_fall_targets={
        str(entry.participant.participant_id)
        for entry in prepared.ordered_entries
        if entry.participant.side=="player"
    } if fall_ground_actor_ids else set()
    if set(fall_ground_resistance) != expected_fall_targets:
        missing=sorted(expected_fall_targets-set(fall_ground_resistance))
        extra=sorted(set(fall_ground_resistance)-expected_fall_targets)
        raise ValueError(
            "FallGround equipment-resistance state must cover exactly "
            f"player-side targets; missing={missing}, extra={extra}"
        )
    nonzero_fall_resistance={
        pid:value for pid,value in fall_ground_resistance.items()
        if int(value) != 0
    }
    if nonzero_fall_resistance:
        raise ValueError(
            "FallGround nonzero equipment resistance is outside the "
            "cross-descendant recovered25 admission domain"
        )

    attempted_fall_ground_actor_ids=set()

    nocast_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            nocast_submissions_by_participant_id or {}
        ).items()
    }
    nocast_actor_ids=set(nocast_submissions)
    unknown_nocast_ids=sorted(nocast_actor_ids-set(slot_by_id))
    if unknown_nocast_ids:
        raise ValueError(
            f"Nocast submissions reference unknown actors: {unknown_nocast_ids}"
        )
    if nocast_actor_ids & (
        fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("Nocast semantic submissions overlap another skill")
    for participant_id,submission in nocast_submissions.items():
        if not isinstance(submission,EnemyAiNocastSubmission):
            raise TypeError(
                f"Nocast submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("Nocast submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError("recovered25 Nocast currently admits enemy actors only")
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "Nocast ordering carrier must be ATTACK/source-target"
            )

    barrier_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            barrier_submissions_by_participant_id or {}
        ).items()
    }
    barrier_actor_ids=set(barrier_submissions)
    unknown_barrier_ids=sorted(barrier_actor_ids-set(slot_by_id))
    if unknown_barrier_ids:
        raise ValueError(
            f"Barrier submissions reference unknown actors: {unknown_barrier_ids}"
        )
    if barrier_actor_ids & (
        nocast_actor_ids | fall_ground_actor_ids | battle_tear_actor_ids
        | mp_damage_actor_ids | damage_to_hp_actor_ids
        | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("Barrier semantic submissions overlap another skill")
    for participant_id,submission in barrier_submissions.items():
        if not isinstance(submission,EnemyAiBarrierSubmission):
            raise TypeError(
                f"Barrier submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("Barrier submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError(
                "recovered25 Barrier currently admits enemy actors only"
            )
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "Barrier ordering carrier must be ATTACK/source-target"
            )

    guard_break2_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            guard_break2_submissions_by_participant_id or {}
        ).items()
    }
    guard_break2_actor_ids=set(guard_break2_submissions)
    unknown_guard_break2_ids=sorted(
        guard_break2_actor_ids-set(slot_by_id)
    )
    if unknown_guard_break2_ids:
        raise ValueError(
            "GuardBreak2 submissions reference unknown actors: "
            f"{unknown_guard_break2_ids}"
        )
    if guard_break2_actor_ids & (
        nocast_actor_ids | fall_ground_actor_ids | battle_tear_actor_ids
        | mp_damage_actor_ids | damage_to_hp_actor_ids
        | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError(
            "GuardBreak2 semantic submissions overlap another skill"
        )
    for participant_id,submission in guard_break2_submissions.items():
        if not isinstance(submission,EnemyAiGuardBreak2Submission):
            raise TypeError(
                f"GuardBreak2 submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("GuardBreak2 submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError(
                "recovered25 GuardBreak2 currently admits enemy actors only"
            )
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2) != int(submission.source_target_slot)
        ):
            raise ValueError(
                "GuardBreak2 ordering carrier must be ATTACK/source-target"
            )

    if (nocast_actor_ids or barrier_actor_ids) and nocast_overlay is None:
        raise ValueError(
            "Nocast/Barrier semantic action requires explicit round overlay"
        )
    if nocast_overlay is not None and not isinstance(
        nocast_overlay,NocastRoundOverlay
    ):
        raise TypeError("nocast_overlay has wrong type")
    nocast_working=(
        None
        if nocast_overlay is None
        else dict(nocast_overlay.runtime_by_participant_id)
    )
    if nocast_working is not None:
        missing_nocast_runtime=sorted(set(slot_by_id)-set(nocast_working))
        if missing_nocast_runtime:
            raise ValueError(
                "Nocast overlay lacks active participants: "
                + ",".join(missing_nocast_runtime)
            )

    nocast_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            nocast_rolls_by_participant_id or {}
        ).items()
    }
    if set(nocast_rolls) != nocast_actor_ids:
        missing=sorted(nocast_actor_ids-set(nocast_rolls))
        extra=sorted(set(nocast_rolls)-nocast_actor_ids)
        raise ValueError(
            "Nocast RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    for participant_id,rolls in nocast_rolls.items():
        if not isinstance(rolls,NocastActionRolls):
            raise TypeError(f"Nocast RNG for {participant_id} has wrong type")
    attempted_nocast_actor_ids=set()

    barrier_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            barrier_rolls_by_participant_id or {}
        ).items()
    }
    if set(barrier_rolls) != barrier_actor_ids:
        missing=sorted(barrier_actor_ids-set(barrier_rolls))
        extra=sorted(set(barrier_rolls)-barrier_actor_ids)
        raise ValueError(
            "Barrier RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    for participant_id,rolls in barrier_rolls.items():
        if not isinstance(rolls,BarrierActionRolls):
            raise TypeError(
                f"Barrier RNG for {participant_id} has wrong type"
            )
    attempted_barrier_actor_ids=set()

    guarding = {
        slot_by_id[entry.participant.participant_id]
        for entry in prepared.ordered_entries
        if entry.command.command1 == BATTLE_COM_GUARD
        and int(entry.participant.hp) > 0
        and entry.command.input_complete
    }

    events: list[OrdinaryRoundEvent] = []

    def tick_barrier_runtime(
        participant_id: str,
        slot: int,
        command_code: int,
        action_value: int,
    ) -> BarrierSelfTick | None:
        if nocast_working is None:
            return None
        participant_id=str(participant_id)
        runtime=nocast_working[participant_id]
        if int(runtime.barrier_counter) <= 0:
            return None
        tick=resolve_barrier_self_tick(
            int(runtime.barrier_counter),
            weaken_active_at_visit=bool(runtime.weaken_active_at_visit),
        )
        nocast_working[participant_id]=runtime.after_barrier_tick(tick)
        events.append(
            OrdinaryRoundEvent(
                participant_id,
                int(slot),
                int(command_code),
                int(action_value),
                "barrier_tick",
                original_target_slot=int(slot),
                resolved_target_slot=int(slot),
                barrier_tick_resolution=tick,
            )
        )
        return tick

    def tick_nocast_runtime(
        participant_id: str,
        slot: int,
        command_code: int,
        action_value: int,
    ) -> None:
        if nocast_working is None:
            return
        participant_id=str(participant_id)
        runtime=nocast_working[participant_id]
        if int(runtime.counter) <= 0:
            return
        tick=resolve_nocast_tick(
            int(runtime.counter),
            weaken_active_at_visit=bool(runtime.weaken_active_at_visit),
            barrier_active_at_visit=bool(
                runtime.barrier_active_for_late_statuses
            ),
        )
        nocast_working[participant_id]=runtime.after_tick(tick)
        events.append(
            OrdinaryRoundEvent(
                participant_id,
                int(slot),
                int(command_code),
                int(action_value),
                "nocast_tick",
                original_target_slot=int(slot),
                resolved_target_slot=int(slot),
                nocast_tick_resolution=tick,
            )
        )

    exited_slots: set[int] = set()
    exited_ids: list[str] = []
    capture_contexts=dict(capture_contexts or {})
    capture_rolls=dict(capture_rolls or {})
    abduct_contexts=dict(abduct_contexts or {})
    abduct_rolls=dict(abduct_rolls or {})
    steal_rolls=dict(steal_rolls or {})
    steal_gold={
        str(pid):int(value)
        for pid,value in (steal_player_gold_by_participant_id or {}).items()
    }
    if any(value < 0 for value in steal_gold.values()):
        raise ValueError("Steal player gold cannot be negative")
    steal_items={
        str(pid):tuple(sorted(int(slot) for slot in slots))
        for pid,slots in (
            steal_player_item_slots_by_participant_id or {}
        ).items()
    }
    for pid,slots in steal_items.items():
        if len(slots) != len(set(slots)):
            raise ValueError(f"Steal item slots contain duplicates for {pid}")
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
    battle_abio={
        str(participant_id):bool(value)
        for participant_id,value in (
            battle_abio_by_participant_id or {}
        ).items()
    }
    unknown_abio_ids=sorted(set(battle_abio)-set(slot_by_id))
    if unknown_abio_ids:
        raise ValueError(
            f"battle ABIO references unknown actors: {unknown_abio_ids}"
        )
    if ultimate_overkill_by_participant_id is None:
        ultimate_overkill={pid:0 for pid in slot_by_id}
    else:
        ultimate_overkill={
            str(pid):int(value)
            for pid,value in ultimate_overkill_by_participant_id.items()
        }
        if set(ultimate_overkill) != set(slot_by_id):
            missing=sorted(set(slot_by_id)-set(ultimate_overkill))
            extra=sorted(set(ultimate_overkill)-set(slot_by_id))
            raise ValueError(
                f"ultimate accumulator participants mismatch; "
                f"missing={missing}, extra={extra}"
            )
        if any(value < 0 for value in ultimate_overkill.values()):
            raise ValueError("ultimate accumulator cannot be negative")
    normalized_combo_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            combo_rolls_by_starter_id or {}
        ).items()
    }
    normalized_continuation_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            continuation_rolls_by_attack_id or {}
        ).items()
    }
    unknown_continuation_ids=sorted(
        set(normalized_continuation_rolls)-set(slot_by_id)
    )
    if unknown_continuation_ids:
        raise ValueError(
            "ContinuationAttack RNG references unknown actors: "
            f"{unknown_continuation_ids}"
        )
    for participant_id,rolls in normalized_continuation_rolls.items():
        if not isinstance(rolls,ContinuationAttackRolls):
            raise TypeError(
                f"ContinuationAttack RNG for {participant_id} has wrong type"
            )
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

    ride_runtime=ride_pet_runtime
    active_ride=False
    if ride_runtime is not None:
        if not isinstance(ride_runtime,RidePetRuntime):
            raise TypeError("ride_pet_runtime must be RidePetRuntime or null")
        if ride_runtime.rider_id not in slot_by_id:
            raise ValueError("ride runtime rider is not an active battle entry")
        rider=by_slot[slot_by_id[ride_runtime.rider_id]]
        if rider.kind != "player":
            raise ValueError("common ride runtime rider must be a player")
        if ride_runtime.pet_id in slot_by_id:
            raise ValueError(
                "non-entry ride pet cannot also occupy an active battle slot"
            )
        active_ride=bool(ride_runtime.mounted)

    if fall_ground_actor_ids:
        if ride_runtime is None:
            if ride_pet_source_slot is not None:
                raise ValueError(
                    "FallGround ride-pet source slot supplied without ride runtime"
                )
        else:
            if ride_pet_source_slot is None:
                raise ValueError(
                    "FallGround ride runtime requires source pet slot provenance"
                )
            ride_pet_source_slot=int(ride_pet_source_slot)
            if not 0 <= ride_pet_source_slot <= 4:
                raise ValueError(
                    "FallGround ride-pet source slot must be in 0..4"
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
    ultimate_exited_ids: list[str] = []
    # Source BENT_FLG_ULTIMATE is cleared at the start of each battle turn.
    # Keep it round-local; do not persist it across PersistentBattleState.
    ultimate_marked_slots: dict[int,int] = {}

    def register_ultimate_exits(
        new_events: Sequence[OrdinaryRoundEvent],
    ) -> None:
        """Apply immediate BATTLE_UltimateExtra/BATTLE_Exit entry effects.

        Profit itself remains represented by the death event and is settled by
        the persistent layer after the round.  Entry removal must be immediate
        because the stable command loop calls BATTLE_AddProfit after each
        attack/counter before later actors execute.
        """
        nonlocal ride_runtime,active_ride

        # BATTLE_Combo returns before BATTLE_AddProfit scans deaths.
        # Collect every entry-flag write first so a later Combo write can affect
        # an earlier reflected death in the same Combo call.
        for event in new_events:
            if event.ultimate_flag_target_slot is not None:
                flag_slot=int(event.ultimate_flag_target_slot)
                if flag_slot not in by_slot:
                    raise ValueError(
                        "ultimate flag write resolved to an unknown battle slot"
                    )
                flag_kind=int(event.ultimate_flag_kind)
                if flag_kind not in {1,2}:
                    raise ValueError(
                        "explicit ultimate flag write requires kind 1 or 2"
                    )
                ultimate_marked_slots[flag_slot]=flag_kind
            elif (
                int(event.ultimate_kind)>0
                and event.resolved_target_slot is not None
            ):
                flag_slot=int(event.resolved_target_slot)
                if flag_slot not in by_slot:
                    raise ValueError(
                        "ultimate death resolved to an unknown battle slot"
                    )
                ultimate_marked_slots[flag_slot]=int(event.ultimate_kind)

        for event in new_events:
            if (
                event.target_hp_before is None
                or event.target_hp_after is None
                or int(event.target_hp_before) <= 0
                or int(event.target_hp_after) > 0
                or event.resolved_target_slot is None
            ):
                continue

            target_slot=int(event.resolved_target_slot)
            if target_slot not in by_slot:
                raise ValueError(
                    "death resolved to an unknown battle slot"
                )
            if int(ultimate_marked_slots.get(target_slot,0)) <= 0:
                continue
            target=by_slot[target_slot]
            target_id=str(target.participant_id)
            if target_id in ultimate_exited_ids:
                continue

            exited_slots.add(target_slot)
            ultimate_exited_ids.append(target_id)

            if target.kind != "player":
                continue

            # BATTLE_UltimateExtra(player) first calls
            # BATTLE_PetDefaultExit(), then BATTLE_Exit(player).  The current
            # single-player battle session has no independent DEFAULTPET
            # selector, so at most one active allied pet can be projected
            # without inventing ownership/selection.
            active_allied=[
                (other_slot,other)
                for other_slot,other in by_slot.items()
                if (
                    other.side==target.side
                    and other.kind=="pet"
                    and str(other.participant_id)
                    not in ultimate_exited_ids
                    and other_slot not in exited_slots
                )
            ]
            if len(active_allied) > 1:
                raise ValueError(
                    "player ultimate exit requires a unique active/default pet"
                )
            if active_allied:
                pet_slot,pet=active_allied[0]
                exited_slots.add(int(pet_slot))
                ultimate_exited_ids.append(str(pet.participant_id))

            # AddProfit marks ISDIE before UltimateExtra. BATTLE_Exit(player)
            # clears ISDIE and restores the dead player to HP=1.
            hp_by_slot[target_slot]=1
            hp_by_id[target_id]=1

            # The player BATTLE_Exit path clears base battle statuses for the
            # player and every carried pet and restores dead carried pets to 1.
            status_runtime[target_id]=BaseBattleStatusRuntime(
                work_quick=int(target.quick)
            )
            for other_slot,other in by_slot.items():
                if other.side!=target.side or other.kind!="pet":
                    continue
                other_id=str(other.participant_id)
                if int(hp_by_slot.get(other_slot,0)) <= 0:
                    hp_by_slot[other_slot]=1
                    hp_by_id[other_id]=1
                status_runtime[other_id]=BaseBattleStatusRuntime(
                    work_quick=int(other.quick)
                )

            # BATTLE_Exit clears WORKPETFALL after converting the ride state
            # to unmounted.  No fall flag is allowed to leak past exit.
            if (
                ride_runtime is not None
                and str(ride_runtime.rider_id)==target_id
                and ride_runtime.petfall
            ):
                ride_runtime=replace(
                    ride_runtime,
                    mounted=False,
                    petfall=False,
                )
                active_ride=False

    def append_counter_chain(
        main_actor_id: str,
        main_actor_slot: int,
        target_slot: int,
    ) -> None:
        if normalized_counter_rolls is None:
            return
        nonlocal ride_runtime,active_ride
        counter_events,ride_runtime=_resolve_counter_chain(
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
            ultimate_overkill_by_participant_id=ultimate_overkill,
            defense_profile=defense_profile,
            field_attr=field_attr,
            field_power=field_power,
            ride_pet_runtime=ride_runtime,
        )
        active_ride=bool(
            ride_runtime is not None and ride_runtime.mounted
        )
        events.extend(counter_events)
        register_ultimate_exits(counter_events)

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
        late_runtime=(
            None
            if nocast_working is None
            else nocast_working[str(participant_id)]
        )
        barrier_blocked_before=bool(
            late_runtime is not None
            and int(late_runtime.barrier_counter) > 0
        )
        if barrier_blocked_before:
            command=BattleCommand(
                BATTLE_COM_NONE,
                command2=entry.command.command2,
                command3=entry.command.command3,
                input_complete=entry.command.input_complete,
            )
            guarding.discard(slot)
        runtime=status_runtime[str(participant_id)]
        status_before=runtime.status
        base_status_was_active=any(
            int(getattr(status_before,name))>0 for name in (
                "poison","paralysis","sleep","stone","drunk","confusion"
            )
        )
        if base_status_was_active:
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
                    weaken_freeze_active=bool(
                        late_runtime is not None
                        and late_runtime.weaken_active_at_visit
                    ),
                    barrier_freeze_active=bool(
                        late_runtime is not None
                        and late_runtime.barrier_active_for_late_statuses
                    ),
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

        barrier_tick=tick_barrier_runtime(
            str(participant_id),
            int(slot),
            int(entry.command.command1),
            int(entry.action_value),
        )
        if (
            barrier_tick is not None
            and int(barrier_tick.counter_after) > 0
        ):
            command=BattleCommand(
                BATTLE_COM_NONE,
                command2=entry.command.command2,
                command3=entry.command.command3,
                input_complete=entry.command.input_complete,
            )
            command_by_slot[slot]=command
            guarding.discard(slot)

        tick_nocast_runtime(
            str(participant_id),
            int(slot),
            int(entry.command.command1),
            int(entry.action_value),
        )

        if command.command1 == BATTLE_COM_S_EARTHROUND1:
            next_earthround=BattleCommand(
                BATTLE_COM_S_EARTHROUND0,
                command2=command.command2,
                command3=command.command3,
                input_complete=command.input_complete,
            )
            command_by_slot[slot]=next_earthround
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_S_EARTHROUND1,
                    entry.action_value,
                    "earthround_hide",
                    original_target_slot=int(command.command2),
                )
            )
            continue

        if command.command1 == BATTLE_COM_S_CHARGE:
            remaining=battle_command3_low(command.command3)
            attack_percent=battle_command3_high(command.command3)
            charge_effects=setup_effects.get(str(participant_id))
            if (
                charge_effects is None
                or charge_effects.charge_ready_attack_power is None
            ):
                raise ValueError(
                    "S_CHARGE requires explicit latent ready attack power"
                )
            if remaining > 0:
                next_charge=BattleCommand(
                    BATTLE_COM_S_CHARGE,
                    command2=command.command2,
                    command3=pack_battle_command3(
                        low=remaining-1,
                        high=attack_percent,
                    ),
                    input_complete=command.input_complete,
                )
                command_by_slot[slot]=next_charge
                events.append(
                    OrdinaryRoundEvent(
                        participant_id,
                        slot,
                        BATTLE_COM_S_CHARGE,
                        entry.action_value,
                        "charge_wait",
                        original_target_slot=int(command.command2),
                    )
                )
                continue
            command=BattleCommand(
                BATTLE_COM_S_CHARGE_OK,
                command2=command.command2,
                command3=command.command3,
                input_complete=command.input_complete,
            )
            setup_effects[str(participant_id)]=replace(
                charge_effects,
                attack_power=int(
                    charge_effects.charge_ready_attack_power
                ),
            )
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

        if command.command1 == BATTLE_COM_S_NOGUARD:
            # Fixed battle.c calls BATTLE_NoAction but leaves COM1/COM3 intact;
            # later attackers/counters in this same round still consume them.
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_S_NOGUARD,
                    entry.action_value,
                    "noguard_no_action",
                )
            )
            continue

        if command.command1 == BATTLE_COM_S_ATTACK_MAGIC:
            caster_id=str(participant_id)
            if participant.kind != "enemy" or participant.side != "enemy":
                raise ValueError(
                    "reconstructed command 2002 currently admits enemy casters only"
                )
            submission=attack_magic_submissions[caster_id]
            if str(submission.participant_id) != caster_id:
                raise ValueError("AttackMagic submission/caster identity drift")
            if (
                int(submission.command.command1) != int(command.command1)
                or int(submission.command.command2) != int(command.command2)
                or int(submission.command.command3) != int(command.command3)
            ):
                raise ValueError("AttackMagic BattleCommand/submission payload drift")
            if attack_magic_runtime is None or attack_magic_working is None:
                raise ValueError("AttackMagic execution state unexpectedly absent")

            alive_player_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    _slot_side(other_slot) == 0
                    and other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            retarget_values=_attack_magic_exact_retarget_rolls(
                int(submission.direct_use_request.target),
                alive_slots=alive_player_slots,
                rolls_0_9=attack_magic_retarget_rolls.get(caster_id,()),
            )
            plan=attack_magic_runtime.resolve_enemy_footprint(
                skill_id=int(submission.skill_id),
                actor_slot=int(slot),
                target_slot=int(submission.direct_use_request.source_target),
                alive_player_slots=alive_player_slots,
                retarget_rolls_0_9=retarget_values,
                require_exact_source_order=True,
            )
            if int(plan.magic_id) != int(submission.command.magic_id):
                raise ValueError("AttackMagic round plan/submission magic-id drift")

            caster_profile=profiles[caster_id]
            caster=EnemyAttackMagicCasterState(
                participant_id=caster_id,
                level=int(participant.level),
                pure_attrs=ElementAttrs(*caster_profile.elements),
            )
            defenders={}
            for target_slot in plan.source_target_order or ():
                target_slot=int(target_slot)
                if target_slot not in by_slot:
                    raise ValueError(
                        f"AttackMagic target slot {target_slot} is not occupied"
                    )
                defender=by_slot[target_slot]
                defender_id=str(defender.participant_id)
                if defender.side != "player":
                    raise ValueError("enemy AttackMagic target crossed battle sides")
                if defender_id not in attack_magic_working:
                    raise KeyError(
                        f"missing AttackMagic resistance runtime for {defender_id}"
                    )
                defender_profile=profiles[defender_id]
                resistance_runtime=attack_magic_working[defender_id]

                ride_state=None
                if (
                    defender.kind == "player"
                    and ride_runtime is not None
                    and str(ride_runtime.rider_id) == defender_id
                    and bool(ride_runtime.mounted)
                ):
                    ride_id=str(ride_runtime.pet_id)
                    if ride_id not in profiles:
                        raise KeyError(
                            f"missing AttackMagic ride-pet profile for {ride_id}"
                        )
                    ride_profile=profiles[ride_id]
                    if not isinstance(ride_profile,BattleCombatProfile):
                        raise TypeError(
                            f"AttackMagic ride profile for {ride_id} has wrong type"
                        )
                    ride_state=AttackMagicRideTargetState(
                        pet_id=ride_id,
                        hp=int(ride_runtime.hp),
                        max_hp=int(ride_runtime.max_hp),
                        pure_attrs=ElementAttrs(*ride_profile.elements),
                        mounted=bool(ride_runtime.mounted),
                        petfall=bool(ride_runtime.petfall),
                    )

                defender_runtime=status_runtime[defender_id]
                defenders[target_slot]=AttackMagicDefenderState(
                    participant_id=defender_id,
                    kind=str(defender.kind),
                    level=int(defender.level),
                    hp=int(hp_by_slot[target_slot]),
                    max_hp=int(defender.max_hp),
                    pure_attrs=ElementAttrs(*defender_profile.elements),
                    resistance=resistance_runtime.state_for(plan.element),
                    luck=int(defender_profile.fixed_luck),
                    equipment_resistance=int(
                        resistance_runtime.equipment_resistance[plan.element]
                    ),
                    equipment_quimagic=int(
                        resistance_runtime.equipment_quimagic
                    ),
                    magic_defense_percent=(
                        resistance_runtime.magic_defense_percent
                    ),
                    sleep_turns=int(defender_runtime.status.sleep),
                    ride=ride_state,
                )

            magic_rolls=attack_magic_rolls.get(caster_id)
            if plan.normalized_selector is None and magic_rolls is None:
                magic_rolls=EnemyAttackMagicActionRolls(None,{})
            elif magic_rolls is None:
                raise KeyError(
                    f"missing AttackMagic action RNG for {caster_id}"
                )
            else:
                consumed_attack_magic_roll_ids.add(caster_id)

            expected_target_roll_slots=set(
                int(x) for x in (plan.source_target_order or ())
            )
            actual_target_roll_slots=set(
                int(x) for x in magic_rolls.target_rolls_by_slot
            )
            if actual_target_roll_slots != expected_target_roll_slots:
                missing=sorted(
                    expected_target_roll_slots-actual_target_roll_slots
                )
                extra=sorted(
                    actual_target_roll_slots-expected_target_roll_slots
                )
                raise ValueError(
                    "AttackMagic action RNG target slots mismatch; "
                    f"missing={missing}, extra={extra}"
                )

            action=resolve_enemy_attack_magic_action(
                plan=plan,
                caster=caster,
                defenders_by_slot=defenders,
                rolls=magic_rolls,
                field_element=attack_magic_field_element(field_attr),
                field_power=int(field_power),
            )
            if not action.targets:
                events.append(
                    OrdinaryRoundEvent(
                        caster_id,
                        int(slot),
                        BATTLE_COM_S_ATTACK_MAGIC,
                        int(entry.action_value),
                        (
                            "attackmagic_no_target"
                            if plan.normalized_selector is None
                            else "attackmagic_empty_footprint"
                        ),
                        original_target_slot=int(
                            submission.direct_use_request.source_target
                        ),
                        retargeted=bool(
                            plan.normalized_selector != plan.source_selector
                        ),
                    )
                )
                continue

            for hit in action.targets:
                target_slot=int(hit.slot)
                defender=by_slot[target_slot]
                defender_id=str(defender.participant_id)
                before=int(hp_by_slot[target_slot])
                if before != int(hit.hp_before):
                    raise ValueError(
                        "AttackMagic action/local target HP pre-state drift"
                    )
                hp_by_slot[target_slot]=int(hit.hp_after)
                hp_by_id[defender_id]=int(hit.hp_after)

                defender_after=action.defenders_after[target_slot]
                defender_runtime=status_runtime[defender_id]
                status_runtime[defender_id]=replace(
                    defender_runtime,
                    status=replace(
                        defender_runtime.status,
                        sleep=int(defender_after.sleep_turns),
                    ),
                )
                attack_magic_working[defender_id]=attack_magic_working[
                    defender_id
                ].with_state(
                    plan.element,
                    defender_after.resistance,
                )

                ride_fell_id=None
                if (
                    defender.kind == "player"
                    and ride_runtime is not None
                    and str(ride_runtime.rider_id) == defender_id
                    and defender_after.ride is not None
                ):
                    ride_after=defender_after.ride
                    if str(ride_after.pet_id) != str(ride_runtime.pet_id):
                        raise ValueError("AttackMagic ride identity drift")
                    if int(ride_after.max_hp) != int(ride_runtime.max_hp):
                        raise ValueError("AttackMagic ride max-HP drift")
                    if bool(hit.ride_pet_unmounted):
                        ride_fell_id=defender_id
                    ride_runtime=replace(
                        ride_runtime,
                        hp=int(ride_after.hp),
                        mounted=bool(ride_after.mounted),
                        petfall=bool(ride_after.petfall),
                    )
                    active_ride=bool(ride_runtime.mounted)

                events.append(
                    OrdinaryRoundEvent(
                        caster_id,
                        int(slot),
                        BATTLE_COM_S_ATTACK_MAGIC,
                        int(entry.action_value),
                        (
                            "attackmagic_dodge"
                            if hit.dodged
                            else "attackmagic_hit"
                        ),
                        original_target_slot=int(
                            submission.direct_use_request.source_target
                        ),
                        resolved_target_slot=target_slot,
                        retargeted=bool(
                            plan.normalized_selector != plan.source_selector
                        ),
                        damage=int(hit.reported_rider_damage),
                        target_hp_before=int(hit.hp_before),
                        target_hp_after=int(hit.hp_after),
                        ride_pet_fell_rider_id=ride_fell_id,
                        attack_magic_target_resolution=hit,
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

        if command.command1 == BATTLE_COM_S_ABDUCT:
            original_target=int(command.command2)
            target=original_target
            retargeted=False
            target_alive=(
                target in by_slot
                and target not in exited_slots
                and int(hp_by_slot.get(target,0))>0
                and _slot_side(target) != _slot_side(slot)
            )
            actor_rolls=abduct_rolls.get(
                participant_id,
                OrdinaryAbductRolls(),
            )
            if not isinstance(actor_rolls,OrdinaryAbductRolls):
                raise TypeError(
                    f"Abduct rolls for {participant_id} have wrong type"
                )
            if not target_alive:
                target=_retarget_slot(
                    slot,
                    by_slot,
                    hp_by_slot,
                    actor_rolls.retarget_roll,
                    excluded_slots=exited_slots,
                )
                retargeted=True
            if target is None:
                events.append(
                    OrdinaryRoundEvent(
                        participant_id,
                        slot,
                        BATTLE_COM_S_ABDUCT,
                        entry.action_value,
                        "abduct_no_target",
                        original_target_slot=original_target,
                        retargeted=True,
                    )
                )
                continue
            if participant_id not in abduct_contexts:
                raise KeyError(f"missing Abduct context for {participant_id}")
            context=abduct_contexts[participant_id]
            if not isinstance(context,OrdinaryAbductContext):
                raise TypeError(
                    f"Abduct context for {participant_id} has wrong type"
                )
            if battle_command3_low(command.command3) != int(context.skill_array):
                raise ValueError("Abduct COM3 skill-array identity drift")

            defender=by_slot[target]
            defender_id=str(defender.participant_id)
            probability=abduct_probability(
                attacker_level=int(participant.level),
                defender_level=int(defender.level),
                defender_type=str(defender.kind),
                has_win_func=bool(context.has_win_func),
                ai_threshold=int(context.ai_threshold),
                defender_fixed_ai=defender.fixed_ai,
            )
            if defender.kind=="player":
                resolution=OrdinaryAbductResolution(
                    attempted=False,
                    success=False,
                    probability=int(probability),
                    attacker_exits=False,
                    defender_exits=False,
                )
                result_name="abduct_rejected_player"
            elif participant.kind not in {"pet","enemy"}:
                resolution=OrdinaryAbductResolution(
                    attempted=False,
                    success=False,
                    probability=int(probability),
                    attacker_exits=False,
                    defender_exits=False,
                )
                result_name="abduct_ineligible_attacker"
            else:
                roll=_validated_roll(
                    actor_rolls.abduct_roll_1_100,
                    1,
                    100,
                    "abduct_roll_1_100",
                )
                transition=abduct_transition(
                    attacker_type=str(participant.kind),
                    defender_type=str(defender.kind),
                    probability=int(probability),
                    rolled_1_to_100=roll,
                )
                resolution=OrdinaryAbductResolution(
                    attempted=bool(transition["attempted"]),
                    success=bool(transition["success"]),
                    probability=int(probability),
                    attacker_exits=bool(transition["attacker_exits"]),
                    defender_exits=bool(transition.get("defender_exits",False)),
                )
                result_name=(
                    "abduct_success"
                    if resolution.success
                    else "abduct_failed"
                )
                if resolution.attacker_exits and slot not in exited_slots:
                    exited_slots.add(slot)
                    if str(participant_id) not in exited_ids:
                        exited_ids.append(str(participant_id))
                if resolution.defender_exits and target not in exited_slots:
                    exited_slots.add(target)
                    if defender_id not in exited_ids:
                        exited_ids.append(defender_id)

            before=int(hp_by_slot[target])
            events.append(
                OrdinaryRoundEvent(
                    participant_id,
                    slot,
                    BATTLE_COM_S_ABDUCT,
                    entry.action_value,
                    result_name,
                    original_target_slot=original_target,
                    resolved_target_slot=target,
                    retargeted=retargeted,
                    target_hp_before=before,
                    target_hp_after=before,
                    abduct_resolution=resolution,
                )
            )
            continue

        if command.command1 == BATTLE_COM_S_STEAL:
            original_target=int(command.command2)
            target=original_target
            retargeted=False
            target_alive=(
                target in by_slot
                and target not in exited_slots
                and int(hp_by_slot.get(target,0)) > 0
                and _slot_side(target) != _slot_side(slot)
            )
            actor_rolls=steal_rolls.get(
                str(participant_id),
                OrdinaryStealRolls(),
            )
            if not isinstance(actor_rolls,OrdinaryStealRolls):
                raise TypeError(
                    f"Steal rolls for {participant_id} have wrong type"
                )
            if not target_alive:
                target=_retarget_slot(
                    slot,
                    by_slot,
                    hp_by_slot,
                    actor_rolls.retarget_roll,
                    excluded_slots=exited_slots,
                )
                retargeted=True
            if target is None:
                events.append(
                    OrdinaryRoundEvent(
                        str(participant_id),
                        int(slot),
                        BATTLE_COM_S_STEAL,
                        int(entry.action_value),
                        "steal_no_target",
                        original_target_slot=original_target,
                        retargeted=True,
                    )
                )
                continue
            if participant.kind not in {"pet","enemy"}:
                raise ValueError("S_STEAL requires PET or ENEMY attacker")

            defender=by_slot[target]
            defender_id=str(defender.participant_id)
            success_roll=_validated_roll(
                actor_rolls.success_roll_1_100,
                1,
                100,
                "steal_success_roll_1_100",
            )
            transition_kwargs={
                "defender_type":str(defender.kind),
                "success_roll_1_to_100":success_roll,
            }
            if defender.kind=="player" and success_roll < 50:
                if defender_id not in steal_gold:
                    raise KeyError(
                        f"missing Steal gold state for {defender_id}"
                    )
                if defender_id not in steal_items:
                    raise KeyError(
                        f"missing Steal item state for {defender_id}"
                    )
                mode_roll=_validated_roll(
                    actor_rolls.mode_roll_1_100,
                    1,
                    100,
                    "steal_mode_roll_1_100",
                )
                transition_kwargs["mode_roll_1_to_100"]=mode_roll
                transition_kwargs["defender_gold"]=int(
                    steal_gold[defender_id]
                )
                current_items=tuple(steal_items[defender_id])
                transition_kwargs["carried_item_slots"]=current_items
                if mode_roll < 50:
                    transition_kwargs["gold_percent_roll"]=_validated_roll(
                        actor_rolls.gold_percent_roll_8_12,
                        8,
                        12,
                        "steal_gold_percent_roll_8_12",
                    )
                elif current_items:
                    transition_kwargs["chosen_item_ordinal"]=_validated_roll(
                        actor_rolls.chosen_item_ordinal,
                        0,
                        len(current_items)-1,
                        "steal_chosen_item_ordinal",
                    )

            transition=steal_transition(**transition_kwargs)
            resolution=OrdinaryStealResolution(
                success=bool(transition["success"]),
                mode=(
                    None
                    if transition.get("mode") is None
                    else str(transition["mode"])
                ),
                attacker_exits=bool(
                    transition.get("attacker_exits",False)
                ),
                defender_gold_loss=int(
                    transition.get("defender_gold_loss",0)
                ),
                destroyed_item_slot=(
                    None
                    if transition.get("destroyed_item_slot") is None
                    else int(transition["destroyed_item_slot"])
                ),
            )
            if resolution.success and defender.kind=="player":
                if resolution.mode=="gold":
                    steal_gold[defender_id]=(
                        int(steal_gold[defender_id])
                        - int(resolution.defender_gold_loss)
                    )
                elif resolution.mode=="item":
                    destroyed=int(resolution.destroyed_item_slot)
                    steal_items[defender_id]=tuple(
                        item_slot
                        for item_slot in steal_items[defender_id]
                        if int(item_slot) != destroyed
                    )
            if resolution.attacker_exits and slot not in exited_slots:
                exited_slots.add(slot)
                if str(participant_id) not in exited_ids:
                    exited_ids.append(str(participant_id))

            before=int(hp_by_slot[target])
            events.append(
                OrdinaryRoundEvent(
                    str(participant_id),
                    int(slot),
                    BATTLE_COM_S_STEAL,
                    int(entry.action_value),
                    (
                        f"steal_success_{resolution.mode}"
                        if resolution.success
                        else "steal_failed"
                    ),
                    original_target_slot=original_target,
                    resolved_target_slot=int(target),
                    retargeted=retargeted,
                    target_hp_before=before,
                    target_hp_after=before,
                    steal_resolution=resolution,
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

                candidate_late_runtime=(
                    None
                    if nocast_working is None
                    else nocast_working[candidate_id]
                )
                candidate_barrier_blocked_before=bool(
                    candidate_late_runtime is not None
                    and int(candidate_late_runtime.barrier_counter) > 0
                )
                if candidate_barrier_blocked_before:
                    command_by_slot[candidate_slot]=BattleCommand(
                        BATTLE_COM_NONE,
                        command2=candidate.command.command2,
                        command3=candidate.command.command3,
                        input_complete=candidate.command.input_complete,
                    )
                    guarding.discard(candidate_slot)

                candidate_runtime=status_runtime[candidate_id]
                candidate_status=candidate_runtime.status
                candidate_base_status_was_active=any(
                    int(getattr(candidate_status,name))>0
                    for name in (
                        "poison","paralysis","sleep",
                        "stone","drunk","confusion",
                    )
                )
                if candidate_base_status_was_active:
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
                            weaken_freeze_active=bool(
                                candidate_late_runtime is not None
                                and candidate_late_runtime.weaken_active_at_visit
                            ),
                            barrier_freeze_active=bool(
                                candidate_late_runtime is not None
                                and candidate_late_runtime.barrier_active_for_late_statuses
                            ),
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

                    candidate_base_can_move=bool(tick.can_move_after_tick)
                else:
                    candidate_base_can_move=True

                candidate_barrier_tick=tick_barrier_runtime(
                    candidate_id,
                    candidate_slot,
                    int(candidate.command.command1),
                    int(candidate.action_value),
                )
                candidate_barrier_after=bool(
                    nocast_working is not None
                    and int(
                        nocast_working[candidate_id].barrier_counter
                    ) > 0
                )
                if candidate_barrier_after:
                    command_by_slot[candidate_slot]=BattleCommand(
                        BATTLE_COM_NONE,
                        command2=candidate.command.command2,
                        command3=candidate.command.command3,
                        input_complete=candidate.command.input_complete,
                    )
                    guarding.discard(candidate_slot)

                tick_nocast_runtime(
                    candidate_id,
                    candidate_slot,
                    int(candidate.command.command1),
                    int(candidate.action_value),
                )

                if not candidate_base_can_move or candidate_barrier_after:
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
            combo_events,ride_runtime=_resolve_combo_group(
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
                ride_pet_runtime=ride_runtime,
                ultimate_overkill_by_participant_id=ultimate_overkill,
                battle_abio_by_participant_id=battle_abio,
            )
            events.extend(combo_events)
            register_ultimate_exits(combo_events)
            active_ride=bool(
                ride_runtime is not None and ride_runtime.mounted
            )
            processed_combo_ids.add(int(entry.combo_id))
            continue

        if command.command1 == BATTLE_COM_S_RENZOKU:
            continuation_id=str(participant_id)
            if continuation_id not in normalized_continuation_rolls:
                raise KeyError(
                    f"missing ContinuationAttack rolls for {continuation_id}"
                )
            continuation=resolve_continuation_nonbow_baseline(
                actor=participant,
                actor_slot=int(slot),
                command=command,
                action_value=int(entry.action_value),
                by_slot=by_slot,
                hp_by_slot=hp_by_slot,
                profiles=profiles,
                command_by_slot=command_by_slot,
                rolls=normalized_continuation_rolls[continuation_id],
                defense_profile=defense_profile,
                setup_effects_by_participant_id=setup_effects,
                guardian_registrations_by_defender_slot=guardian_registrations,
                base_status_runtime_by_participant_id=status_runtime,
                base_damage_react_state_by_participant_id=damage_react_state,
                battle_abio_by_participant_id=battle_abio,
                ultimate_overkill_by_participant_id=ultimate_overkill,
                ride_pet_runtime=ride_runtime,
                excluded_slots=exited_slots,
                field_attr=field_attr,
                field_power=field_power,
            )

            hp_by_slot.clear()
            hp_by_slot.update({
                int(k):int(v)
                for k,v in continuation.hp_by_slot.items()
            })
            hp_by_id.clear()
            hp_by_id.update({
                str(by_slot[int(k)].participant_id):int(v)
                for k,v in hp_by_slot.items()
                if int(k) in by_slot
            })
            if continuation.base_status_runtime_by_participant_id is not None:
                status_runtime.clear()
                status_runtime.update(
                    continuation.base_status_runtime_by_participant_id
                )
            if (
                continuation.base_damage_react_state_by_participant_id
                is not None
            ):
                damage_react_state.clear()
                damage_react_state.update(
                    continuation.base_damage_react_state_by_participant_id
                )
            if continuation.ultimate_overkill_by_participant_id is not None:
                ultimate_overkill.clear()
                ultimate_overkill.update(
                    continuation.ultimate_overkill_by_participant_id
                )
            ride_runtime=continuation.ride_pet_runtime
            active_ride=bool(
                ride_runtime is not None and ride_runtime.mounted
            )

            continuation_events=tuple(continuation.events)
            events.extend(continuation_events)
            for exit_id in continuation.ultimate_exited_participant_ids:
                exit_id=str(exit_id)
                if exit_id not in slot_by_id:
                    raise ValueError(
                        "ContinuationAttack ultimate exit references "
                        f"unknown actor {exit_id}"
                    )
                exit_slot=int(slot_by_id[exit_id])
                exited_slots.add(exit_slot)
                if exit_id not in ultimate_exited_ids:
                    ultimate_exited_ids.append(exit_id)
            for event in continuation_events:
                if (
                    int(event.ultimate_kind)>0
                    and event.resolved_target_slot is not None
                ):
                    ultimate_marked_slots[
                        int(event.resolved_target_slot)
                    ]=int(event.ultimate_kind)

            command_by_slot[slot]=BattleCommand(
                BATTLE_COM_ATTACK,
                command2=(
                    -1
                    if continuation.last_target_slot is None
                    else int(continuation.last_target_slot)
                ),
                command3=command.command3,
                input_complete=command.input_complete,
            )

            if (
                continuation.counter_continuation_allowed
                and continuation.last_target_slot is not None
            ):
                append_counter_chain(
                    continuation_id,
                    int(slot),
                    int(continuation.last_target_slot),
                )
            continue

        barrier_actor_id=str(participant_id)
        if (
            barrier_actor_id in barrier_submissions
            and int(command.command1) == BATTLE_COM_ATTACK
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=barrier_submissions[barrier_actor_id]
            if int(command.command2) != int(submission.source_target_slot):
                raise ValueError(
                    "Barrier ordering carrier target drift before execution"
                )
            if nocast_working is None:
                raise ValueError("Barrier working overlay unexpectedly absent")

            alive_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            action_rolls=barrier_rolls[barrier_actor_id]
            target_list=resolve_barrier_multilist(
                int(submission.source_target_slot),
                alive_slots=alive_slots,
                retarget_draws_0_9=action_rolls.retarget_draws_0_9,
            )
            attempted_barrier_actor_ids.add(barrier_actor_id)
            consumed_hit_roll_slots=set()
            for target_slot in target_list.slots:
                target_slot=int(target_slot)
                if target_slot not in by_slot:
                    raise ValueError(
                        "Barrier target list resolved unoccupied slot"
                    )
                defender=by_slot[target_slot]
                defender_id=str(defender.participant_id)
                target_runtime=nocast_working[defender_id]
                base_runtime=status_runtime[defender_id]
                base_status_active=any(
                    int(getattr(base_runtime.status,name))>0
                    for name in (
                        "poison","paralysis","sleep",
                        "stone","drunk","confusion",
                    )
                )
                any_status=target_runtime.has_any_status(
                    base_status_active=base_status_active
                )
                hit_roll=action_rolls.hit_rolls_by_slot.get(target_slot)
                application=resolve_barrier_target(
                    BarrierCheckInputs(
                        attacker_level=int(participant.level),
                        defender_level=int(defender.level),
                        pvp=False,
                        attacker_fixed_luck=int(
                            profiles[barrier_actor_id].fixed_luck
                        ),
                        defender_vital=int(target_runtime.vital),
                        defender_strength=int(target_runtime.strength),
                        defender_toughness=int(target_runtime.toughness),
                        defender_dexterity=int(target_runtime.dexterity),
                        defender_mod_barrier=int(target_runtime.mod_barrier),
                        defender_suit_resist=int(target_runtime.suit_resist),
                        any_existing_status=bool(any_status),
                    ),
                    submission.option,
                    roll_1_100=hit_roll,
                )
                if application.rng_consumed:
                    consumed_hit_roll_slots.add(target_slot)
                nocast_working[defender_id]=(
                    target_runtime.after_barrier_application(application)
                )
                result_name=(
                    "barrier_blocked_existing_status"
                    if application.probability_value is None
                    else (
                        "barrier_applied"
                        if application.counter_written is not None
                        else "barrier_missed"
                    )
                )
                events.append(
                    OrdinaryRoundEvent(
                        barrier_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        result_name,
                        original_target_slot=int(
                            submission.source_target_slot
                        ),
                        resolved_target_slot=target_slot,
                        retargeted=bool(
                            target_list.slots
                            and int(target_list.slots[0])
                            != int(submission.source_target_slot)
                        ),
                        barrier_application=application,
                    )
                )
            supplied_hit_slots=set(action_rolls.hit_rolls_by_slot)
            if supplied_hit_slots != consumed_hit_roll_slots:
                missing=sorted(consumed_hit_roll_slots-supplied_hit_slots)
                extra=sorted(supplied_hit_slots-consumed_hit_roll_slots)
                raise ValueError(
                    "Barrier hit RNG slots mismatch; "
                    f"missing={missing}, extra={extra}"
                )
            continue

        nocast_actor_id=str(participant_id)
        if (
            nocast_actor_id in nocast_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=nocast_submissions[nocast_actor_id]
            if (
                int(command.command1) != BATTLE_COM_ATTACK
                or int(command.command2) != int(submission.source_target_slot)
            ):
                raise ValueError("Nocast ordering carrier drift before execution")
            if nocast_working is None:
                raise ValueError("Nocast working overlay unexpectedly absent")

            alive_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            action_rolls=nocast_rolls[nocast_actor_id]
            target_list=resolve_nocast_multilist(
                int(submission.source_target_slot),
                alive_slots=alive_slots,
                retarget_draws_0_9=action_rolls.retarget_draws_0_9,
            )
            attempted_nocast_actor_ids.add(nocast_actor_id)
            consumed_hit_roll_slots=set()
            for target_slot in target_list.slots:
                target_slot=int(target_slot)
                if target_slot not in by_slot:
                    raise ValueError("Nocast target list resolved unoccupied slot")
                defender=by_slot[target_slot]
                defender_id=str(defender.participant_id)
                target_runtime=nocast_working[defender_id]
                base_runtime=status_runtime[defender_id]
                base_status_active=any(
                    int(getattr(base_runtime.status,name))>0
                    for name in (
                        "poison","paralysis","sleep",
                        "stone","drunk","confusion",
                    )
                )
                any_status=target_runtime.has_any_status(
                    base_status_active=base_status_active
                )
                hit_roll=action_rolls.hit_rolls_by_slot.get(target_slot)
                application=resolve_nocast_target(
                    NocastCheckInputs(
                        attacker_level=int(participant.level),
                        defender_level=int(defender.level),
                        pvp=False,
                        attacker_fixed_luck=int(
                            profiles[nocast_actor_id].fixed_luck
                        ),
                        defender_vital=int(target_runtime.vital),
                        defender_strength=int(target_runtime.strength),
                        defender_toughness=int(target_runtime.toughness),
                        defender_dexterity=int(target_runtime.dexterity),
                        defender_mod_nocast=int(target_runtime.mod_nocast),
                        defender_suit_resist=int(target_runtime.suit_resist),
                        any_existing_status=bool(any_status),
                        target_kind=(
                            str(defender.kind)
                            if str(defender.kind) in {
                                "player","pet","enemy","other"
                            }
                            else "other"
                        ),
                    ),
                    submission.option,
                    roll_1_100=hit_roll,
                )
                if application.rng_consumed:
                    consumed_hit_roll_slots.add(target_slot)
                nocast_working[defender_id]=target_runtime.after_application(
                    application
                )
                result_name=(
                    "nocast_blocked_existing_status"
                    if application.probability_value is None
                    else (
                        "nocast_pet_excluded"
                        if application.pet_excluded
                        else (
                            "nocast_applied"
                            if application.turn_written is not None
                            else "nocast_missed"
                        )
                    )
                )
                events.append(
                    OrdinaryRoundEvent(
                        nocast_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        result_name,
                        original_target_slot=int(
                            submission.source_target_slot
                        ),
                        resolved_target_slot=target_slot,
                        retargeted=bool(
                            target_list.slots
                            and int(target_list.slots[0])
                            != int(submission.source_target_slot)
                        ),
                        nocast_application=application,
                    )
                )
            supplied_hit_slots=set(action_rolls.hit_rolls_by_slot)
            if supplied_hit_slots != consumed_hit_roll_slots:
                missing=sorted(consumed_hit_roll_slots-supplied_hit_slots)
                extra=sorted(supplied_hit_slots-consumed_hit_roll_slots)
                raise ValueError(
                    "Nocast hit RNG slots mismatch; "
                    f"missing={missing}, extra={extra}"
                )
            continue

        rehp_fallback_active=False
        rehp_fallback_original_target=None
        rehp_fallback_retargeted=False
        rehp_actor_id=str(participant_id)
        if (
            rehp_actor_id in enemy_rehp_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=enemy_rehp_submissions[rehp_actor_id]
            if (
                int(command.command1) != BATTLE_COM_ATTACK
                or int(command.command2) != int(submission.source_target_slot)
            ):
                raise ValueError("enemy ReHP ordering carrier drift before execution")

            original_rehp_target=int(submission.source_target_slot)
            adjusted_target=original_rehp_target
            rehp_retargeted=False
            adjusted_alive=(
                adjusted_target in by_slot
                and adjusted_target not in exited_slots
                and int(hp_by_slot.get(adjusted_target,0)) > 0
            )
            if adjusted_alive and _slot_side(adjusted_target) == _slot_side(slot):
                raise ValueError("enemy ReHP source target crossed battle sides")

            target_adjust_roll=enemy_rehp_retarget_rolls[rehp_actor_id]
            if adjusted_alive:
                if target_adjust_roll is not None:
                    raise ValueError(
                        "enemy ReHP supplied unused TargetAdjust RNG for live target"
                    )
            else:
                adjusted_target=_retarget_slot(
                    int(slot),
                    by_slot,
                    hp_by_slot,
                    target_adjust_roll,
                    excluded_slots=exited_slots,
                )
                rehp_retargeted=True

            effect_rolls=enemy_rehp_rolls[rehp_actor_id]
            attempted_enemy_rehp_actor_ids.add(rehp_actor_id)
            if adjusted_target is None:
                if not effect_rolls.is_empty:
                    raise ValueError(
                        "enemy ReHP effect RNG supplied after TargetAdjust no-target"
                    )
                if rehp_actor_id in attack_rolls:
                    raise ValueError(
                        "enemy ReHP no-target path supplied unused fallback attack RNG"
                    )
                events.append(
                    OrdinaryRoundEvent(
                        rehp_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "enemy_rehp_no_target",
                        original_target_slot=original_rehp_target,
                        retargeted=rehp_retargeted,
                    )
                )
                continue

            allies={}
            for ally_slot in range(10,20):
                if ally_slot not in by_slot or ally_slot in exited_slots:
                    continue
                ally=by_slot[ally_slot]
                if ally.side != "enemy":
                    raise ValueError("enemy ReHP ally scan crossed battle sides")
                allies[ally_slot]=EnemyReHpAllyState(
                    participant_id=str(ally.participant_id),
                    slot=ally_slot,
                    hp=int(hp_by_slot.get(ally_slot,0)),
                    max_hp=int(ally.max_hp),
                )

            rehp_resolution=resolve_enemy_rehp_effect(
                adjusted_attack_target_slot=int(adjusted_target),
                allies_by_slot=allies,
                rolls=effect_rolls,
                caster_mode_ready=True,
            )
            if rehp_resolution.success:
                if rehp_actor_id in attack_rolls:
                    raise ValueError(
                        "successful enemy ReHP supplied unused fallback attack RNG"
                    )
                if rehp_resolution.healed_slot is None:
                    raise ValueError("successful enemy ReHP lacks healed slot")
                healed_slot=int(rehp_resolution.healed_slot)
                healed=by_slot[healed_slot]
                healed_id=str(healed.participant_id)
                hp_by_slot[healed_slot]=int(rehp_resolution.hp_after)
                hp_by_id[healed_id]=int(rehp_resolution.hp_after)
                events.append(
                    OrdinaryRoundEvent(
                        rehp_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "enemy_rehp",
                        original_target_slot=original_rehp_target,
                        resolved_target_slot=healed_slot,
                        retargeted=rehp_retargeted,
                        target_hp_before=int(rehp_resolution.hp_before),
                        target_hp_after=int(rehp_resolution.hp_after),
                        enemy_rehp_resolution=rehp_resolution,
                    )
                )
                continue

            if not rehp_resolution.fallback_to_attack:
                raise ValueError("failed enemy ReHP did not request physical fallback")
            events.append(
                OrdinaryRoundEvent(
                    rehp_actor_id,
                    int(slot),
                    BATTLE_COM_ATTACK,
                    int(entry.action_value),
                    "enemy_rehp_fallback",
                    original_target_slot=original_rehp_target,
                    resolved_target_slot=int(adjusted_target),
                    retargeted=rehp_retargeted,
                    enemy_rehp_resolution=rehp_resolution,
                )
            )
            rehp_fallback_active=True
            rehp_fallback_original_target=original_rehp_target
            rehp_fallback_retargeted=rehp_retargeted
            command=BattleCommand(
                BATTLE_COM_ATTACK,
                command2=int(adjusted_target),
                command3=command.command3,
                input_complete=command.input_complete,
            )
            command_by_slot[slot]=command

        rolls = attack_rolls.get(participant_id)
        if rolls is None:
            raise KeyError(f"missing ordinary attack rolls for {participant_id}")
        if rehp_fallback_active and rolls.retarget_roll is not None:
            raise ValueError(
                "enemy ReHP fallback attack must not consume a second retarget RNG"
            )
        attack_command_code=int(command.command1)
        if attack_command_code in {
            BATTLE_COM_S_CHARGE_OK,
            BATTLE_COM_S_EARTHROUND0,
        }:
            # Fixed battle.c clears CHARGE_OK/EARTHROUND0 to NONE before
            # entering their physical attack loops.
            command_by_slot[slot]=BattleCommand(BATTLE_COM_NONE)
        elif attack_command_code in {
            BATTLE_COM_S_GBREAK,
            BATTLE_COM_S_GUARDIAN_ATTACK,
            BATTLE_COM_S_MIGHTY,
            BATTLE_COM_S_POWERBALANCE,
            BATTLE_COM_S_STATUSCHANGE,
        }:
            command_by_slot[slot]=BattleCommand(
                BATTLE_COM_ATTACK,
                command2=command.command2,
                command3=command.command3,
                input_complete=command.input_complete,
            )

        if rehp_fallback_active:
            original_target=int(rehp_fallback_original_target)
            target=int(command.command2)
            retargeted=bool(rehp_fallback_retargeted)
        else:
            original_target=int(command.command2)
            target=original_target
            retargeted=False

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
        guardbreak_eligible=bool(
            attack_command_code == BATTLE_COM_S_GBREAK
            and int(target) in guarding
            and int(
                status_runtime[str(defender_id)].status.confusion
            ) <= 0
        )
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
                extra_percent_points=(
                    (
                        battle_command3_high(command.command3)
                        if attack_command_code == BATTLE_COM_S_MIGHTY
                        else 0
                    )
                    + _noguard_dodge_percent_modifier(
                        command_by_slot[target]
                    )
                ),
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

        damage_to_hp_submission=None
        damage_to_hp_source_react_blocked=False
        if (
            str(participant_id) in damage_to_hp_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            damage_to_hp_submission=damage_to_hp_submissions[
                str(participant_id)
            ]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "DamageToHp semantic action lost ATTACK ordering carrier"
                )
            source_defender=by_slot[int(target)]
            source_defender_id=str(source_defender.participant_id)
            damage_to_hp_source_react_blocked=base_damage_react_active(
                damage_react_state[source_defender_id]
            )

        fall_ground_submission=None
        fall_ground_source_react_blocked=False
        if (
            str(participant_id) in fall_ground_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            fall_ground_submission=fall_ground_submissions[str(participant_id)]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "FallGround semantic action lost ATTACK ordering carrier"
                )
            source_defender=by_slot[int(target)]
            source_defender_id=str(source_defender.participant_id)
            fall_ground_source_react_blocked=base_damage_react_active(
                damage_react_state[source_defender_id]
            )

        mp_damage_submission=None
        mp_damage_source_react_blocked=False
        if (
            str(participant_id) in mp_damage_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            mp_damage_submission=mp_damage_submissions[str(participant_id)]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "MpDamage semantic action lost ATTACK ordering carrier"
                )
            source_defender=by_slot[int(target)]
            source_defender_id=str(source_defender.participant_id)
            mp_damage_source_react_blocked=base_damage_react_active(
                damage_react_state[source_defender_id]
            )

        guard_break2_submission=None
        if (
            str(participant_id) in guard_break2_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            guard_break2_submission=guard_break2_submissions[
                str(participant_id)
            ]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "GuardBreak2 semantic action lost ATTACK ordering carrier"
                )

        battle_tear_submission=None
        battle_tear_source_react_blocked=False
        if (
            str(participant_id) in battle_tear_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            battle_tear_submission=battle_tear_submissions[str(participant_id)]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "BattleTear semantic action lost ATTACK ordering carrier"
                )
            source_defender=by_slot[int(target)]
            source_defender_id=str(source_defender.participant_id)
            battle_tear_source_react_blocked=base_damage_react_active(
                damage_react_state[source_defender_id]
            )

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

        guard_break2_resolution=None
        if guard_break2_submission is not None:
            guard_break2_resolution=resolve_guard_break2_damage_step(
                int(damage),
                defender_command_is_guard=(
                    int(damage_target_slot) in guarding
                ),
                defender_confusion_counter=int(
                    status_runtime[str(defender_id)].status.confusion
                ),
            )
            damage=int(guard_break2_resolution.damage_after_multiplier)
            if guard_break2_resolution.guard_adjust_applies_after_multiplier:
                guard_roll=_validated_roll(
                    rolls.guard_roll_1_100,
                    1,
                    100,
                    "guard_roll_1_100",
                )
                damage=guard_damage(damage,guard_roll)
        elif (
            damage_target_slot in guarding
            and attack_command_code != BATTLE_COM_S_GBREAK
        ):
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

        if attack_command_code == BATTLE_COM_S_MIGHTY:
            damage = int(
                int(damage)
                * (battle_command3_low(command.command3) * 0.01)
            )
        elif attack_command_code == BATTLE_COM_S_EARTHROUND0:
            earth_transition=earth_round_attack_transition(
                attack_percent=int(command.command3)
            )
            damage=int(
                int(damage)
                * float(earth_transition["damage_multiplier"])
            )

        battle_tear_augmentation=None
        if battle_tear_submission is not None:
            original_tear_target=by_slot[int(target)]
            original_tear_target_id=str(original_tear_target.participant_id)
            tear_ride_hp=None
            tear_ride_max_hp=None
            if (
                original_tear_target.kind=="player"
                and active_ride
                and ride_runtime is not None
                and str(ride_runtime.rider_id)==original_tear_target_id
            ):
                tear_ride_hp=int(ride_runtime.hp)
                tear_ride_max_hp=int(ride_runtime.max_hp)
            battle_tear_augmentation=resolve_battle_tear_pre_damage_sub(
                option_text=str(battle_tear_submission.wound_percent),
                attack_seq_damage=int(damage),
                attack_seq_result=str(result),
                damage_react_active=bool(battle_tear_source_react_blocked),
                same_side=(_slot_side(int(slot))==_slot_side(int(target))),
                prevent_same_side=True,
                target_hp=int(hp_by_slot[int(target)]),
                target_max_hp=int(original_tear_target.max_hp),
                target_kind=str(original_tear_target.kind),
                ride_pet_hp=tear_ride_hp,
                ride_pet_max_hp=tear_ride_max_hp,
            )
            damage=int(battle_tear_augmentation.damage_after)

        reaction_target_slot=int(damage_target_slot)
        reaction_defender=defender
        reaction_defender_id=str(defender_id)
        reaction_defender_work_defense=int(defender_work_defense)
        if (
            damage_to_hp_submission is not None
            or mp_damage_submission is not None
            or fall_ground_submission is not None
            or battle_tear_submission is not None
            or guard_break2_submission is not None
        ):
            # Fixed specialized BATTLE_S_AttackDamage lets AttackSeq calculate
            # against a Guardian but passes its original defindex to DamageSub.
            reaction_target_slot=int(target)
            reaction_defender=by_slot[reaction_target_slot]
            reaction_defender_id=str(reaction_defender.participant_id)
            reaction_defender_work_defense=_effective_defense_power(
                reaction_defender,setup_effects
            )
        if attack_command_code == BATTLE_COM_S_GBREAK:
            if not guardbreak_eligible:
                damage=0
                result="miss"
            # Fixed BATTLE_S_GBreak passes the original defindex into
            # BATTLE_DamageSub even when BATTLE_AttackSeq used Guardian
            # as its local damage-calculation defender.
            reaction_target_slot=int(target)
            reaction_defender=by_slot[reaction_target_slot]
            reaction_defender_id=str(reaction_defender.participant_id)
            reaction_defender_work_defense=_effective_defense_power(
                reaction_defender,setup_effects
            )

        reaction_resolution=resolve_base_damage_react(
            damage_react_state[reaction_defender_id],
            raw_damage=int(damage),
            attacker_hp=int(hp_by_slot[slot]),
            attacker_max_hp=int(participant.max_hp),
            defender_hp=int(hp_by_slot[reaction_target_slot]),
            defender_max_hp=int(reaction_defender.max_hp),
            attacker_uses_throwing_weapon=counter_weapon_blocks_counter(
                attacker_profile.counter_weapon_type
            ),
        )
        damage_react_state[reaction_defender_id]=reaction_resolution.state_after

        ride_split=None
        ride_hp_resolution=None
        ride_pet_fell_rider_id=None
        event_damage=int(damage)
        if active_ride and ride_runtime is not None:
            rider_id=str(ride_runtime.rider_id)
            if (
                reaction_resolution.effective_kind == DAMAGE_REACT_ABSROB
                and reaction_defender_id == rider_id
            ):
                ride_split=immediate_reaction_ride_split(
                    int(damage),
                    rider_defense_power=int(reaction_defender_work_defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_heal(
                    ride_split,
                    rider_hp=int(reaction_resolution.defender_hp_before),
                    rider_max_hp=int(reaction_defender.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                reaction_resolution=replace(
                    reaction_resolution,
                    defender_hp_after=int(
                        ride_hp_resolution.rider_hp_after
                    ),
                )
                event_damage=int(ride_split.rider_amount)
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                )
            elif (
                reaction_resolution.effective_kind == DAMAGE_REACT_REFLEC
                and str(participant_id) == rider_id
            ):
                attacker_work_defense=_effective_defense_power(
                    participant,setup_effects
                )
                ride_split=immediate_reaction_ride_split(
                    int(damage),
                    rider_defense_power=int(attacker_work_defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_damage(
                    ride_split,
                    rider_hp=int(reaction_resolution.attacker_hp_before),
                    rider_max_hp=int(participant.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                reaction_resolution=replace(
                    reaction_resolution,
                    attacker_hp_after=int(
                        ride_hp_resolution.rider_hp_after
                    ),
                )
                event_damage=int(ride_split.rider_amount)
                if ride_hp_resolution.unmounted:
                    ride_pet_fell_rider_id=ride_runtime.rider_id
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                    mounted=(
                        False
                        if ride_hp_resolution.unmounted
                        else ride_runtime.mounted
                    ),
                    petfall=bool(
                        ride_runtime.petfall or ride_hp_resolution.petfall
                    ),
                )
                active_ride=bool(ride_runtime.mounted)
            elif (
                reaction_resolution.damage_target == "defender"
                and reaction_defender_id == rider_id
            ):
                ride_split=ordinary_ride_damage_split(
                    int(damage),
                    rider_defense_power=int(reaction_defender_work_defense),
                    pet_defense_power=int(ride_runtime.defense_power),
                    pet_hp=int(ride_runtime.hp),
                )
                ride_hp_resolution=apply_ride_damage(
                    ride_split,
                    rider_hp=int(reaction_resolution.defender_hp_before),
                    rider_max_hp=int(reaction_defender.max_hp),
                    pet_hp=int(ride_runtime.hp),
                    pet_max_hp=int(ride_runtime.max_hp),
                )
                reaction_resolution=replace(
                    reaction_resolution,
                    defender_hp_after=int(
                        ride_hp_resolution.rider_hp_after
                    ),
                )
                event_damage=int(ride_split.rider_amount)
                if ride_hp_resolution.unmounted:
                    ride_pet_fell_rider_id=ride_runtime.rider_id
                ride_runtime=replace(
                    ride_runtime,
                    hp=int(ride_hp_resolution.pet_hp_after),
                    mounted=(
                        False
                        if ride_hp_resolution.unmounted
                        else ride_runtime.mounted
                    ),
                    petfall=bool(
                        ride_runtime.petfall or ride_hp_resolution.petfall
                    ),
                )
                active_ride=bool(ride_runtime.mounted)

        hp_by_slot[slot]=int(reaction_resolution.attacker_hp_after)
        hp_by_id[str(participant_id)]=int(
            reaction_resolution.attacker_hp_after
        )
        hp_by_slot[reaction_target_slot]=int(
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
            resolved_damage_slot=int(reaction_target_slot)
            resolved_damage_id=reaction_defender_id
            before=int(reaction_resolution.defender_hp_before)
            after=int(reaction_resolution.defender_hp_after)
            status_target_slot=int(reaction_target_slot)

        fall_ground_resolution=None
        if fall_ground_submission is not None:
            attempted_fall_ground_actor_ids.add(str(participant_id))
            fall_target=by_slot[int(reaction_target_slot)]
            fall_target_id=str(fall_target.participant_id)
            source_ride_slot=None
            if (
                fall_target.kind=="player"
                and ride_runtime is not None
                and ride_runtime.mounted
                and str(ride_runtime.rider_id)==fall_target_id
            ):
                source_ride_slot=ride_pet_source_slot
            fall_ground_resolution=resolve_fall_ground(
                post_damage_player_damage=int(event_damage),
                damage_react=(
                    1 if fall_ground_source_react_blocked else 0
                ),
                same_side=(
                    _slot_side(int(slot))
                    == _slot_side(int(reaction_target_slot))
                ),
                target_kind=str(fall_target.kind),
                ride_pet_slot=source_ride_slot,
                fall_roll_0_100=fall_ground_rolls[str(participant_id)],
                equipment_fall_resistance=int(
                    fall_ground_resistance[fall_target_id]
                ),
                # Only the cross-descendant zero-resistance intersection is
                # admitted. With explicit zero state both pinned branches agree.
                use_equipment_resistance=True,
                prevent_same_side=True,
                fix_petfall=False,
            )
            if fall_ground_resolution.fell:
                if ride_runtime is None or not ride_runtime.mounted:
                    raise ValueError(
                        "FallGround resolved fall without mounted ride runtime"
                    )
                ride_runtime=replace(
                    ride_runtime,
                    mounted=False,
                    petfall=True,
                )
                active_ride=False
                ride_pet_fell_rider_id=str(ride_runtime.rider_id)

        damage_to_hp_recovery=None
        if (
            damage_to_hp_submission is not None
            and not damage_to_hp_source_react_blocked
            and int(damage) > 0
        ):
            damage_basis_player=int(damage)
            damage_basis_pet=0
            if ride_split is not None:
                damage_basis_player=int(ride_split.rider_amount)
                damage_basis_pet=int(ride_split.pet_amount)
            damage_to_hp_recovery=resolve_damage_to_hp_recovery(
                damage=damage_basis_player,
                petdamage=damage_basis_pet,
                attacker_hp=int(hp_by_slot[slot]),
                attacker_max_hp=int(participant.max_hp),
                target_damage_react=0,
                option=damage_to_hp_submission.option,
            )
            hp_by_slot[slot]=int(damage_to_hp_recovery.attacker_hp_after)
            hp_by_id[str(participant_id)]=int(
                damage_to_hp_recovery.attacker_hp_after
            )

        mp_damage_resolution=None
        if (
            mp_damage_submission is not None
            and not mp_damage_source_react_blocked
        ):
            mp_target=by_slot[int(target)]
            mp_target_id=str(mp_target.participant_id)
            if mp_target.kind == "player":
                if mp_target_id not in mp_working:
                    raise KeyError(
                        f"missing MpDamage current MP for {mp_target_id}"
                    )
                target_mp=int(mp_working[mp_target_id])
            else:
                # Fixed helper rejects enemy/pet before reading MP.
                target_mp=0
            mp_damage_resolution=resolve_mp_damage(
                # BATTLE_DamageSub writes playerdamage back through pDamage;
                # on a mounted target this is the rider portion only.
                physical_damage=int(event_damage),
                target_kind=str(mp_target.kind),
                target_mp=target_mp,
                target_damage_react=0,
                option=mp_damage_submission.option,
            )
            if mp_target.kind == "player":
                mp_working[mp_target_id]=int(
                    mp_damage_resolution.mp_after
                )

        ultimate_damage_resolution=None
        death_ultimate_resolution=None
        ultimate_kind=0
        if int(damage) > 0:
            hp_damage_applied=max(0,int(before)-int(after))
            ultimate_damage_resolution=resolve_battle_ultimate_damage(
                BattleUltimateDamageInputs(
                    damage_for_threshold=int(damage),
                    hp_damage_applied=int(hp_damage_applied),
                    target_hp_before=int(before),
                    target_max_hp=int(
                        by_slot[resolved_damage_slot].max_hp
                    ),
                    accumulated_overkill_before=int(
                        ultimate_overkill[resolved_damage_id]
                    ),
                )
            )
            ultimate_overkill[resolved_damage_id]=int(
                ultimate_damage_resolution.accumulated_overkill_after
            )
            ultimate_kind=int(
                ultimate_damage_resolution.ultimate_kind
            )
            if int(before) > 0 and int(after) <= 0:
                victim_kind=_participant_battle_kind(
                    by_slot[resolved_damage_slot]
                )
                victim_abio=bool(
                    battle_abio.get(resolved_damage_id,False)
                )
                needs_ultimate_roll=bool(
                    (not victim_abio)
                    and victim_kind != PLAYER
                    and is_critical
                )
                if (
                    rolls.ultimate_roll_1_100 is not None
                    and not needs_ultimate_roll
                ):
                    raise ValueError(
                        "ultimate_roll_1_100 supplied on unused death path"
                    )
                death_ultimate_resolution=(
                    resolve_battle_death_ultimate_override(
                        BattleDeathUltimateInputs(
                            base_ultimate_kind=ultimate_kind,
                            victim_kind=victim_kind,
                            abio=victim_abio,
                            critical=bool(is_critical),
                        ),
                        critical_roll_1_100=(
                            rolls.ultimate_roll_1_100
                            if needs_ultimate_roll
                            else None
                        ),
                    )
                )
                ultimate_kind=int(
                    death_ultimate_resolution.ultimate_kind
                )
            elif rolls.ultimate_roll_1_100 is not None:
                raise ValueError(
                    "ultimate_roll_1_100 supplied when no "
                    "non-player critical death consumed it"
                )
        elif rolls.ultimate_roll_1_100 is not None:
            raise ValueError(
                "ultimate_roll_1_100 supplied on zero-damage path"
            )

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
            int(event_damage) > 0
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
                    damage_after_resolution=int(event_damage),
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
                damage=int(event_damage),
                target_hp_before=before,
                target_hp_after=after,
                status_application_resolution=status_application,
                guardian_redirected=guardian_redirected,
                guarded_target_slot=guarded_target_slot,
                guardian_slot=guardian_slot,
                damage_react_resolution=reaction_resolution,
                damage_to_hp_recovery=damage_to_hp_recovery,
                mp_damage_resolution=mp_damage_resolution,
                fall_ground_resolution=fall_ground_resolution,
                battle_tear_augmentation=battle_tear_augmentation,
                guard_break2_resolution=guard_break2_resolution,
                ride_damage_split=ride_split,
                ride_hp_resolution=ride_hp_resolution,
                ride_pet_fell_rider_id=ride_pet_fell_rider_id,
                ultimate_damage_resolution=ultimate_damage_resolution,
                death_ultimate_resolution=death_ultimate_resolution,
                ultimate_kind=int(ultimate_kind),
            )
        )
        register_ultimate_exits((events[-1],))
        # Generic BATTLE_S_AttackDamage forces continuation FALSE on
        # Guardian/DamageReact. Dedicated BATTLE_S_FallGround does not: its
        # iRet is controlled by AttackSeq result, the post-react defindex's
        # GUARD state and death. Preserve that difference here.
        if _battle_attack_continuation_allowed(
            guardian_redirected=(
                False
                if (
                    fall_ground_submission is not None
                    or guard_break2_submission is not None
                )
                else guardian_redirected
            ),
            damage_reaction_active=(
                False
                if (
                    fall_ground_submission is not None
                    or guard_break2_submission is not None
                )
                else continuation_blocked_by_reaction
            ),
            critical=(result == "critical"),
            target_guarding=(
                (resolved_damage_slot in guarding)
                if fall_ground_submission is not None
                else (
                    (counter_target_slot in guarding)
                    if guard_break2_submission is not None
                    else (counter_target_slot in guarding)
                )
            ),
            target_hp_after=after,
        ):
            append_counter_chain(
                participant_id,
                slot,
                counter_target_slot,
            )

    for participant_id in sorted(
        enemy_rehp_actor_ids-attempted_enemy_rehp_actor_ids
    ):
        if (
            not enemy_rehp_rolls[participant_id].is_empty
            or enemy_rehp_retarget_rolls[participant_id] is not None
        ):
            raise ValueError(
                "enemy ReHP RNG supplied for status-suppressed semantic action: "
                + participant_id
            )

    for participant_id in sorted(
        fall_ground_actor_ids-attempted_fall_ground_actor_ids
    ):
        if fall_ground_rolls[participant_id] is not None:
            raise ValueError(
                "FallGround RNG supplied for status/no-target/dodge-suppressed "
                "semantic action: " + participant_id
            )

    for participant_id in sorted(
        nocast_actor_ids-attempted_nocast_actor_ids
    ):
        if not nocast_rolls[participant_id].is_empty:
            raise ValueError(
                "Nocast RNG supplied for status-suppressed semantic action: "
                + participant_id
            )

    for participant_id in sorted(
        barrier_actor_ids-attempted_barrier_actor_ids
    ):
        if not barrier_rolls[participant_id].is_empty:
            raise ValueError(
                "Barrier RNG supplied for status-suppressed semantic action: "
                + participant_id
            )

    unused_attack_magic_roll_ids=sorted(
        set(attack_magic_rolls)-consumed_attack_magic_roll_ids
    )
    if unused_attack_magic_roll_ids:
        raise ValueError(
            "unused AttackMagic action RNG supplied for actors: "
            f"{unused_attack_magic_roll_ids}"
        )

    carried_commands={}
    carried_effects={}
    for carried_slot,carried_command in command_by_slot.items():
        if int(carried_command.command1) not in {
            BATTLE_COM_S_CHARGE,
            BATTLE_COM_S_EARTHROUND0,
        }:
            continue
        if (
            carried_slot in exited_slots
            or int(hp_by_slot.get(carried_slot,0)) <= 0
        ):
            continue
        carried_id=str(by_slot[carried_slot].participant_id)
        carried_commands[carried_id]=carried_command
        effects=setup_effects.get(
            carried_id,
            BattleCommandSetupEffects(),
        )
        if (
            int(carried_command.command1) == BATTLE_COM_S_CHARGE
            and effects.charge_ready_attack_power is None
        ):
            raise ValueError(
                f"carried S_CHARGE lacks ready attack power: {carried_id}"
            )
        carried_effects[carried_id]=effects

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
        ride_pet_runtime=ride_runtime,
        attack_magic_overlay=(
            None
            if attack_magic_working is None
            else AttackMagicRoundOverlay(attack_magic_working)
        ),
        nocast_overlay=(
            None
            if nocast_working is None
            else NocastRoundOverlay(nocast_working)
        ),
        ultimate_overkill_by_participant_id=MappingProxyType(
            dict(ultimate_overkill)
        ),
        ultimate_exited_participant_ids=tuple(ultimate_exited_ids),
        exited_participant_ids=tuple(exited_ids),
        escaped_participant_ids=tuple(escaped_ids),
        carried_commands_by_participant_id=MappingProxyType(
            dict(carried_commands)
        ),
        carried_setup_effects_by_participant_id=MappingProxyType(
            dict(carried_effects)
        ),
        steal_gold_by_player_id=MappingProxyType(dict(steal_gold)),
        steal_item_slots_by_player_id=MappingProxyType(
            dict(steal_items)
        ),
        mp_by_participant_id=MappingProxyType(dict(mp_working)),
    )
