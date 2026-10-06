#!/usr/bin/env python3
"""Stable-descendant first battle-round command/order boundary.

This module reconstructs the command envelope and action-order seam without
inventing player input or enemy AI. Commands are explicit inputs. Later skills and profession systems remain outside this R1 boundary. Stable
base combo formation is reconstructed as an explicit opt-in rewrite after
action sorting; combo damage execution remains a separate seam.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from tools.stoneage_default_pet_exit_model import (
    DefaultPetExitAuthority, bind_exit_authorities, player_pet_exit_ids,
    pet_owner_id, clear_owner_selection, apply_selection_events,
)

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
from tools.stoneage_battlemodel_round_action import (
    BattleModelRoundAction, execute_current_battlemodel_round_action,
)
from tools.stoneage_battlemodel_hit_loop import BattleModelEntry, BattleModelHitLoopResolution
from tools.stoneage_enemy_ai_rehp_bridge import EnemyAiReHpSubmission
from tools.stoneage_enemy_ai_relife_bridge import EnemyAiReLifeSubmission
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
from tools.stoneage_enemy_ai_battletimid_bridge import (
    EnemyAiBattleTimidSubmission,
)
from tools.stoneage_battletimid_model import BattleTimidExitResolution
from tools.stoneage_enemy_ai_2battletimid_bridge import (
    EnemyAiTwoBattleTimidSubmission,
)
from tools.stoneage_2battletimid_reference_model import TwoBattleTimidPost
from tools.stoneage_enemy_ai_batfly_bridge import EnemyAiBatFlySubmission
from tools.stoneage_batfly_reference_model import (
    BatFlyExecutionGate,
    BatFlyResolution,
    BatFlyTarget,
    BatFlyTargetResolution,
)
from tools.stoneage_enemy_ai_lighttakeed_bridge import (
    EnemyAiLighttakeedSubmission,
)
from tools.stoneage_lighttakeed_model import (
    LighttakeedResolution,
    resolve_lighttakeed_reaction,
)
from tools.stoneage_enemy_ai_combined_bridge import EnemyAiCombinedSubmission
from tools.stoneage_enemy_ai_vary_bridge import EnemyAiVarySubmission
from tools.stoneage_combined_direct_magic_model import CombinedDirectMagicRoute
from tools.stoneage_combined_effect_model import (
    CombinedRecoveryEffect,
    CombinedStatusChangeEffect,
    CombinedStatusRecoveryEffect,
    CombinedAttReverseEffect,
    resolve_combined_single_target,
    resolve_combined_recovery21_effect,
    resolve_combined_status_change_effect,
    resolve_combined_status_recovery61_effect,
    resolve_combined_att_reverse240_effect,
)
from tools.stoneage_combined_runtime_state import (
    CombinedActionRolls,
    CombinedRuntimeOverlay,
)
from tools.stoneage_combined_status_magic_model import EXPECTED_IRIS_CP950_STATUS
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
from tools.stoneage_enemy_ai_weaken_bridge import EnemyAiWeakenSubmission
from tools.stoneage_weaken_runtime_state import WeakenActionRolls
from tools.stoneage_enemy_ai_refresh_bridge import EnemyAiRefreshSubmission
from tools.stoneage_refresh_runtime_state import (
    RefreshActionRolls,
    apply_refresh_cleared_status,
    refresh_status_vector,
)
from tools.stoneage_refresh_model import RefreshResolution, resolve_refresh_recovery
from tools.stoneage_enemy_ai_setmagicpet_bridge import EnemyAiSetMagicPetSubmission
from tools.stoneage_setmagicpet_runtime_state import (
    SetMagicPetActionRolls,
    SetMagicPetRoundOverlay,
    SetMagicPetTurnTick,
    apply_setmagicpet_option,
    tick_setmagicpet_runtime,
)
from tools.stoneage_weaken_model import (
    WeakenApplication, WeakenCheckInputs, resolve_weaken_target,
    resolve_weaken_multilist, resolve_weaken_self_tick,
)
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
from tools.stoneage_enemy_relife_model import (
    EnemyReLifeDeadEntry,
    EnemyReLifeResolution,
    EnemyReLifeRolls,
    resolve_enemy_relife_effect,
)
from tools.stoneage_recovered25_attack_magic_runtime import (
    Recovered25AttackMagicRuntime,
)

from tools.stoneage_enemy_ai_attack_crazed_bridge import EnemyAiAttackCrazedSubmission
from tools.stoneage_attack_crazed_model import resolve_attack_crazed_target_list
from tools.stoneage_enemy_ai_wildviolent_bridge import EnemyAiWildViolentSubmission
from tools.stoneage_wildviolent_model import (
    plan_wildviolent_nonbow_action,
    wildviolent_divided_damage,
)
from tools.stoneage_enemy_ai_modifyattack_bridge import EnemyAiModifyAttackSubmission
from tools.stoneage_modifyattack_reference_model import modifyattack_helper_damage
from tools.stoneage_enemy_ai_mdfyattack_bridge import EnemyAiMdfyAttackSubmission
from tools.stoneage_mdfyattack_model import mdfyattack_attribute_damage

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
    action_value_overrides_by_participant_id: Mapping[str,int] | None = None,
) -> PreparedBattleRound:
    """Calculate command-relative action values then sort descending.

    The fixed source uses qsort with comparator pC2->dex - pC1->dex. Its
    ordering for equal values is not a historical contract. If a tie occurs,
    callers must supply an explicit tie_break_order rather than having this
    reconstruction silently invent one.
    """
    entries = []
    seen_ids: set[str] = set()
    action_value_overrides={
        str(pid):int(value)
        for pid,value in (
            action_value_overrides_by_participant_id or {}
        ).items()
    }
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
                action_value=(
                    action_value_overrides[participant_id]
                    if participant_id in action_value_overrides
                    else command_action_value(
                        participant,
                        command,
                        random_subtract=initiative_random_subtracts[participant_id],
                    )
                ),
                source_order=source_order,
            )
        )

    unknown_action_overrides=sorted(set(action_value_overrides)-seen_ids)
    if unknown_action_overrides:
        raise ValueError(
            "action-value overrides reference unknown participants: "
            f"{unknown_action_overrides}"
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
    semantic_nonattack_ids: Sequence[str] = (),
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
    nonattack_ids={str(pid) for pid in semantic_nonattack_ids}
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
            and participant_id not in nonattack_ids
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
class AttackCrazedRolls:
    """Preselection indices consumed before any of the three physical hits.

    Zero indices are allowed only when the action-time candidate pool is empty.
    Per-hit retarget/dodge/critical/guard RNG stays in OrdinaryAttackRolls.
    """
    selection_indices: tuple[int, ...]
    hit_rolls: tuple[OrdinaryAttackRolls, ...]

    def __post_init__(self):
        indices=tuple(int(v) for v in self.selection_indices)
        hits=tuple(self.hit_rolls)
        if len(indices) not in (0,3) or any(v < 0 or v > 8 for v in indices):
            raise ValueError("AttackCrazed requires zero or three pool-index draws")
        if len(hits)!=3 or not all(isinstance(v,OrdinaryAttackRolls) for v in hits):
            raise ValueError("AttackCrazed requires three typed per-hit RNG bundles")
        object.__setattr__(self,"selection_indices",indices)
        object.__setattr__(self,"hit_rolls",hits)


@dataclass(frozen=True)
class WildViolentRolls:
    """Action-time RAND(3,10) plus exactly that many physical hit bundles."""

    count_roll_3_10: int
    hit_rolls: tuple[OrdinaryAttackRolls, ...]

    def __post_init__(self):
        count=int(self.count_roll_3_10)
        hits=tuple(self.hit_rolls)
        if not 3 <= count <= 10:
            raise ValueError("WildViolentAttack count roll must be 3..10")
        if len(hits)!=count or not all(
            isinstance(value,OrdinaryAttackRolls) for value in hits
        ):
            raise ValueError(
                "WildViolentAttack requires exactly count-roll typed hit bundles"
            )
        object.__setattr__(self,"count_roll_3_10",count)
        object.__setattr__(self,"hit_rolls",hits)


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
    # Source pet UltimateExtra clears the owner's selection before later deaths.
    default_pet_selection_cleared_owner_id: str | None = None
    # Exact round-local BENT_FLG_ULTIMATE write. Most paths leave these null
    # and the flag target is the resolved death target. Combo+DamageReact can
    # write the flag to a different entry after its quirky defindex rewrite.
    ultimate_flag_target_slot: int | None = None
    ultimate_flag_kind: int = 0
    attack_magic_target_resolution: AttackMagicTargetResolution | None = None
    enemy_rehp_resolution: EnemyReHpResolution | None = None
    enemy_relife_resolution: EnemyReLifeResolution | None = None
    damage_to_hp_recovery: DamageToHpRecovery | None = None
    mp_damage_resolution: MpDamageResolution | None = None
    fall_ground_resolution: FallGroundResolution | None = None
    battle_tear_augmentation: BattleTearAugmentation | None = None
    guard_break2_resolution: GuardBreak2DamageResolution | None = None
    battletimid_resolution: BattleTimidExitResolution | None = None
    battletimid_skill_id: int | None = None
    two_battletimid_resolution: TwoBattleTimidPost | None = None
    two_battletimid_skill_id: int | None = None
    two_battletimid_profile: str | None = None
    batfly_execution_gate: BatFlyExecutionGate | None = None
    batfly_target_resolution: BatFlyTargetResolution | None = None
    batfly_resolution: BatFlyResolution | None = None
    batfly_skill_id: int | None = None
    lighttakeed_resolution: LighttakeedResolution | None = None
    lighttakeed_skill_id: int | None = None
    lighttakeed_profile: str | None = None
    combined_skill_id: int | None = None
    combined_magic_id: int | None = None
    combined_direct_route: CombinedDirectMagicRoute | None = None
    combined_recovery_effect: CombinedRecoveryEffect | None = None
    combined_status_change_effect: CombinedStatusChangeEffect | None = None
    combined_status_recovery_effect: CombinedStatusRecoveryEffect | None = None
    combined_att_reverse_effect: CombinedAttReverseEffect | None = None
    vary_skill_id: int | None = None
    vary_visual_effect_enabled: bool | None = None
    modifyattack_skill_id: int | None = None
    modifyattack_damage_before: int | None = None
    modifyattack_helper_draws: int = 0
    modifyattack_event_marked: bool = False
    mdfyattack_skill_id: int | None = None
    mdfyattack_element: str | None = None
    mdfyattack_attack_vector: tuple[int, ...] = ()
    mdfyattack_event_marked: bool = False
    attack_crazed_skill_id: int | None = None
    attack_crazed_hit_index: int | None = None
    attack_crazed_target_list: tuple[int, ...] = ()
    attack_crazed_selection_draws: int = 0
    wildviolent_skill_id: int | None = None
    wildviolent_hit_index: int | None = None
    wildviolent_attack_count: int | None = None
    wildviolent_dodge_percent_points: int | None = None
    refresh_resolution: RefreshResolution | None = None
    refresh_skill_id: int | None = None
    refresh_status_index: int | None = None
    refresh_cleared_status: int | None = None
    setmagicpet_skill_id: int | None = None
    setmagicpet_kind: str | None = None
    setmagicpet_applied: bool | None = None
    setmagicpet_turn_tick: SetMagicPetTurnTick | None = None
    weaken_application: WeakenApplication | None = None
    weaken_tick_resolution: BarrierSelfTick | None = None
    weaken_skill_id: int | None = None
    barrier_application: BarrierApplication | None = None
    barrier_tick_resolution: BarrierSelfTick | None = None
    nocast_application: NocastApplication | None = None
    nocast_tick_resolution: NocastTick | None = None
    battlemodel_skill_id: int | None = None
    battlemodel_loop_resolution: BattleModelHitLoopResolution | None = None


PROFIT_BOUNDARY_ORDINARY_PER_HIT = "ordinary_per_hit"
PROFIT_BOUNDARY_COUNTER_CHAIN_CURRENT_DRIVER = "counter_chain_current_driver"
PROFIT_BOUNDARY_COMBO_COMMAND_TAIL = "combo_command_tail"
PROFIT_BOUNDARY_BATFLY_COMMAND_TAIL_CURRENT_DRIVER = "batfly_command_tail_current_driver"
PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL = "battlemodel_command_tail"

_PROFIT_BOUNDARY_KINDS = frozenset({
    PROFIT_BOUNDARY_ORDINARY_PER_HIT,
    PROFIT_BOUNDARY_COUNTER_CHAIN_CURRENT_DRIVER,
    PROFIT_BOUNDARY_COMBO_COMMAND_TAIL,
    PROFIT_BOUNDARY_BATFLY_COMMAND_TAIL_CURRENT_DRIVER,
    PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,
})


@dataclass(frozen=True)
class OrdinaryProfitBoundarySnapshot:
    """Immutable pre-AddProfit observation from the modern round driver.

    This is chronology evidence, not settlement authority. The persistent
    adapter must still run the accepted whole-scan model before charging any
    death/loyalty effects.
    """

    boundary_kind: str
    trigger_event_indexes: tuple[int, ...]
    hp_by_slot: Mapping[int, int]
    occupied_participant_id_by_slot: Mapping[int, str]
    ultimate_kind_by_slot: Mapping[int, int]
    prior_processed_death_ids: tuple[str, ...]
    default_pet_authorities_by_owner_id: Mapping[
        str, DefaultPetExitAuthority
    ]
    base_status_runtime_by_participant_id: Mapping[
        str, BaseBattleStatusRuntime
    ]
    nocast_overlay: NocastRoundOverlay | None

    def __post_init__(self) -> None:
        if self.boundary_kind not in _PROFIT_BOUNDARY_KINDS:
            raise ValueError("unknown profit boundary kind")
        indexes=tuple(self.trigger_event_indexes)
        if (
            not indexes
            or any(type(index) is not int or index < 0 for index in indexes)
            or tuple(sorted(set(indexes))) != indexes
        ):
            raise ValueError("profit boundary requires ordered unique event indexes")
        object.__setattr__(self, "trigger_event_indexes", indexes)

        hp={int(slot):int(value) for slot,value in self.hp_by_slot.items()}
        if any(not 0 <= slot < BATTLE_SLOT_COUNT for slot in hp):
            raise ValueError("profit boundary HP slot outside battle array")
        occupied={
            int(slot):str(participant_id)
            for slot,participant_id in self.occupied_participant_id_by_slot.items()
        }
        if set(occupied)-set(hp):
            raise ValueError("profit boundary occupancy lacks HP slot")
        if len(set(occupied.values())) != len(occupied):
            raise ValueError("profit boundary occupancy duplicates participant")
        ultimate={
            int(slot):int(kind)
            for slot,kind in self.ultimate_kind_by_slot.items()
        }
        if set(ultimate)-set(hp) or any(kind not in {1,2} for kind in ultimate.values()):
            raise ValueError("profit boundary ultimate flag drift")
        processed=tuple(str(pid) for pid in self.prior_processed_death_ids)
        if len(set(processed)) != len(processed):
            raise ValueError("profit boundary processed-death identities duplicate")
        authorities=dict(self.default_pet_authorities_by_owner_id)
        for owner_id,authority in authorities.items():
            if (
                not isinstance(authority,DefaultPetExitAuthority)
                or str(owner_id) != authority.owner_id
            ):
                raise ValueError("profit boundary default-pet authority drift")
        status=dict(self.base_status_runtime_by_participant_id)
        if any(not isinstance(value,BaseBattleStatusRuntime) for value in status.values()):
            raise TypeError("profit boundary requires typed base status runtime")
        if self.nocast_overlay is not None and not isinstance(
            self.nocast_overlay,NocastRoundOverlay
        ):
            raise TypeError("profit boundary late-status overlay has wrong type")
        object.__setattr__(self,"hp_by_slot",MappingProxyType(hp))
        object.__setattr__(
            self,"occupied_participant_id_by_slot",MappingProxyType(occupied)
        )
        object.__setattr__(
            self,"ultimate_kind_by_slot",MappingProxyType(ultimate)
        )
        object.__setattr__(self,"prior_processed_death_ids",processed)
        object.__setattr__(
            self,"default_pet_authorities_by_owner_id",
            MappingProxyType(authorities),
        )
        object.__setattr__(
            self,"base_status_runtime_by_participant_id",
            MappingProxyType(status),
        )


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
    setmagicpet_overlay: SetMagicPetRoundOverlay | None = None
    combined_overlay: CombinedRuntimeOverlay | None = None
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
    battlemodel_cleared_command_ids: tuple[str, ...] = ()
    profit_boundaries: tuple[OrdinaryProfitBoundarySnapshot, ...] = ()
    profit_processed_death_ids: tuple[str, ...] = ()


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
    semantic_noncounter_actor_ids: frozenset[str] = frozenset(),
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

        if actor_id in semantic_noncounter_actor_ids or command_by_slot[actor_slot].command1 not in {
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
    """Shared non-bow physical sequence witness; public RENZOKU API retained."""

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
    default_pet_exit_authorities: Mapping[str, DefaultPetExitAuthority] | None = None,
) -> ContinuationBaselineResolution:
    """Execute the stable non-bow ContinuationAttack public boundary."""
    return _resolve_nonbow_multihit_baseline(
        actor=actor,
        actor_slot=actor_slot,
        command=command,
        action_value=action_value,
        by_slot=by_slot,
        hp_by_slot=hp_by_slot,
        profiles=profiles,
        command_by_slot=command_by_slot,
        rolls=rolls,
        defense_profile=defense_profile,
        setup_effects_by_participant_id=setup_effects_by_participant_id,
        guardian_registrations_by_defender_slot=guardian_registrations_by_defender_slot,
        base_status_runtime_by_participant_id=base_status_runtime_by_participant_id,
        base_damage_react_state_by_participant_id=base_damage_react_state_by_participant_id,
        battle_abio_by_participant_id=battle_abio_by_participant_id,
        ultimate_overkill_by_participant_id=ultimate_overkill_by_participant_id,
        ride_pet_runtime=ride_pet_runtime,
        excluded_slots=excluded_slots,
        default_pet_exit_authorities=default_pet_exit_authorities,
        field_attr=field_attr,
        field_power=field_power,
    )


def _resolve_nonbow_multihit_baseline(
    *,
    actor: BattleParticipant,
    actor_slot: int,
    command: BattleCommand,
    action_value: int,
    by_slot: Mapping[int,BattleParticipant],
    hp_by_slot: Mapping[int,int],
    profiles: Mapping[str,BattleCombatProfile],
    command_by_slot: Mapping[int,BattleCommand],
    rolls: ContinuationAttackRolls | AttackCrazedRolls | WildViolentRolls,
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
    attack_crazed_submission: EnemyAiAttackCrazedSubmission | None = None,
    wildviolent_submission: EnemyAiWildViolentSubmission | None = None,
    field_attr: str = "none",
    field_power: int = 0,
    default_pet_exit_authorities: Mapping[str, DefaultPetExitAuthority] | None = None,
) -> ContinuationBaselineResolution:
    """Execute shared non-bow physical settlement under a typed hit plan.

    ContinuationAttack repeats its original target and divides damage;
    AttackCrazed consumes its preselection first and does not divide damage.
    This layer closes the fixed loop, per-hit original-target recheck,
    Guardian redirection, ordinary dodge/critical/guard damage, gDamageDiv,
    and the final BATTLE_Attack boolean used by the later counter chain.
    Damage-reaction, ride splitting, wakeup and ultimate/death handling are
    applied per hit because each can change later loop state, including actor
    death, petfall/unmount, target exit and the next retarget candidate set.
    ContinuationAttack itself adds no status-application payload.
    """

    crazed=attack_crazed_submission is not None
    wild=wildviolent_submission is not None
    if crazed and wild:
        raise ValueError("nonbow multihit semantic submissions overlap")
    semantic_carrier=bool(crazed or wild)
    expected_command=BATTLE_COM_ATTACK if semantic_carrier else BATTLE_COM_S_RENZOKU
    if int(command.command1) != expected_command:
        raise ValueError("nonbow multihit command/carrier mismatch")
    actor_slot=int(actor_slot)
    if by_slot.get(actor_slot) != actor:
        raise ValueError("continuation actor/slot mapping mismatch")
    actor_id=str(actor.participant_id)
    if actor_id not in profiles:
        raise KeyError(f"missing combat profile for {actor_id}")
    wild_plan=None
    if wild:
        if not isinstance(rolls,WildViolentRolls):
            raise TypeError("WildViolentAttack needs WildViolentRolls")
        wild_plan=plan_wildviolent_nonbow_action(
            count_roll_3_10=rolls.count_roll_3_10,
            packed_com3=command.command3,
            target_slot=command.command2,
        )
        count=int(wild_plan.attack_count)
    else:
        count=(
            attack_crazed_submission.attack_count
            if crazed else battle_command3_low(command.command3)
        )
    if not 1 <= count <= 10:
        raise ValueError("nonbow multihit count must be in 1..10")
    if len(rolls.hit_rolls) != count:
        raise ValueError("nonbow multihit RNG bundle count mismatch")

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
    default_authorities=bind_exit_authorities(default_pet_exit_authorities,by_slot)
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
    event_command=expected_command
    result_prefix=("wildviolent" if wild else ("attack_crazed" if crazed else "continuation"))
    hit_targets=(original_target,)*count
    selection_draws=0
    target_list=()
    if crazed:
        if not isinstance(rolls,AttackCrazedRolls):
            raise TypeError("AttackCrazed needs AttackCrazedRolls")
        if (actor.kind!="enemy" or actor.side!="enemy"
            or profiles[actor_id].counter_weapon_type!=COUNTER_WEAPON_FIST):
            raise ValueError("AttackCrazed currently admits enemy FIST actors only")
        if (attack_crazed_submission.participant_id!=actor_id
            or attack_crazed_submission.source_target_slot!=original_target):
            raise ValueError("AttackCrazed semantic carrier drift")
        draws=iter(rolls.selection_indices)
        consumed=[]
        def rand_index(low,high):
            try:value=next(draws)
            except StopIteration as exc:raise ValueError("missing AttackCrazed pool RNG") from exc
            consumed.append(value)
            return value
        listing=resolve_attack_crazed_target_list(
            actor_slot=actor_slot,submitted_target=original_target,attack_count=count,
            live_slots=(slot for slot in by_slot if slot not in excluded and hp[slot]>0),
            rand_index=rand_index,shootchestnut_enabled=True,
        )
        if len(consumed)!=len(rolls.selection_indices):
            raise ValueError("unused AttackCrazed pool RNG on empty candidate path")
        selection_draws=listing.selection_draws
        target_list=listing.slots[:count]
        hit_targets=(original_target,)+listing.slots[1:count]
    if wild:
        if (
            actor.kind!="enemy" or actor.side!="enemy"
            or profiles[actor_id].counter_weapon_type!=COUNTER_WEAPON_FIST
        ):
            raise ValueError("WildViolentAttack currently admits enemy FIST actors only")
        if (
            wildviolent_submission.participant_id!=actor_id
            or wildviolent_submission.source_target_slot!=original_target
            or int(wildviolent_submission.setup.packed_com3)!=int(command.command3)
        ):
            raise ValueError("WildViolentAttack semantic carrier/setup drift")
        if tuple(wild_plan.original_target_list)!=(original_target,)*20:
            raise ValueError("WildViolentAttack original-target list drift")
    actor_profile=profiles[actor_id]
    resolved: list[OrdinaryRoundEvent]=[]
    last_target: int | None=None
    last_continue=False
    wild_used_roll_fields=[set() for _ in rolls.hit_rolls] if wild else None

    for hit_index,hit_rolls in enumerate(rolls.hit_rolls):
        original_target=hit_targets[hit_index]
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
        if wild and retargeted:
            wild_used_roll_fields[hit_index].add("retarget_roll")
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
            if wild:
                wild_used_roll_fields[hit_index].add("dodge_roll_1_10000")
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
                extra_percent_points=(
                    (int(wild_plan.additive_dodge_percent_points) if wild else 0)
                    + _noguard_dodge_percent_modifier(
                        command_by_slot.get(target,BattleCommand(BATTLE_COM_NONE))
                    )
                ),
            )
            if dodge_roll <= dodge_probability:
                resolved.append(
                    OrdinaryRoundEvent(
                        actor_id,
                        actor_slot,
                        event_command,
                        int(action_value),
                        result_prefix+"_dodge",
                        attack_crazed_skill_id=613 if crazed else None,
                        attack_crazed_hit_index=hit_index if crazed else None,
                        attack_crazed_target_list=target_list,
                        attack_crazed_selection_draws=selection_draws,
                        wildviolent_skill_id=(wildviolent_submission.skill_id if wild else None),
                        wildviolent_hit_index=hit_index if wild else None,
                        wildviolent_attack_count=count if wild else None,
                        wildviolent_dodge_percent_points=(wild_plan.additive_dodge_percent_points if wild else None),
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

        if wild:
            wild_used_roll_fields[hit_index].update(("critical_roll_1_10000", "damage_roll"))
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
            if wild:
                wild_used_roll_fields[hit_index].add("guard_roll_1_100")
            guard_roll=_validated_roll(
                hit_rolls.guard_roll_1_100,
                1,100,
                "continuation guard_roll_1_100",
            )
            damage=guard_damage(damage,guard_roll)
        if damage < 1:
            if wild:
                wild_used_roll_fields[hit_index].add("minimum_damage_roll_0_1")
            damage=_validated_roll(
                hit_rolls.minimum_damage_roll_0_1,
                0,1,
                "continuation minimum_damage_roll_0_1",
            )

        # Fixed BATTLE_Attack applies gDamageDiv after AttackSeq (including
        # Guardian/critical/guard) and before BATTLE_DamageSub.
        if wild:
            damage=wildviolent_divided_damage(damage,count)
        elif not crazed:
            damage=continuation_divided_damage(damage,count)
        if damage == 0 and guardian_redirected:
            # AttackSeq's redirected zero-damage path is rendered as NORMAL/1.
            damage=1
            result=result_prefix+"_normal"
        elif damage == 0:
            result=(
                result_prefix+"_allguard"
                if damage_target_guarding
                else result_prefix+"_miss"
            )
        else:
            result=(
                result_prefix+"_critical"
                if is_critical
                else result_prefix+"_normal"
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
                if wild and needs_ultimate_roll:
                    wild_used_roll_fields[hit_index].add("ultimate_roll_1_100")
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
                event_command,
                int(action_value),
                result,
                attack_crazed_skill_id=613 if crazed else None,
                attack_crazed_hit_index=hit_index if crazed else None,
                attack_crazed_target_list=target_list,
                attack_crazed_selection_draws=selection_draws,
                wildviolent_skill_id=(wildviolent_submission.skill_id if wild else None),
                wildviolent_hit_index=hit_index if wild else None,
                wildviolent_attack_count=count if wild else None,
                wildviolent_dodge_percent_points=(wild_plan.additive_dodge_percent_points if wild else None),
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

                if exit_actor.kind == "pet":
                    owner_id=pet_owner_id(exit_id,default_authorities)
                    clear_owner_selection(default_authorities,owner_id)
                    resolved[-1]=replace(resolved[-1],
                        default_pet_selection_cleared_owner_id=owner_id)
                if exit_actor.kind == "player":
                    for pet_id in player_pet_exit_ids(exit_slot,exit_id,
                        default_authorities,by_slot,excluded):
                        pet_slot=default_authorities[exit_id].occupied_pet_slots[pet_id]
                        excluded.add(pet_slot)
                        if pet_id not in ultimate_exited_ids:
                            ultimate_exited_ids.append(pet_id)

                    hp[exit_slot]=1
                    status_runtime[exit_id]=BaseBattleStatusRuntime(
                        work_quick=int(exit_actor.quick)
                    )
                    for other_slot,other in by_slot.items():
                        if (
                            other.participant_id not in default_authorities[exit_id].owned_pet_ids
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

    if wild:
        for hit_index, (hit_rolls, used) in enumerate(zip(rolls.hit_rolls, wild_used_roll_fields)):
            unused=sorted(name for name, value in vars(hit_rolls).items()
                          if value is not None and name not in used)
            if unused:
                raise ValueError(f"unused WildViolentAttack hit RNG at hit {hit_index}: {unused}")

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
    mdfyattack_submissions_by_participant_id: Mapping[str,EnemyAiMdfyAttackSubmission] | None = None,
    modifyattack_submissions_by_participant_id: Mapping[str,EnemyAiModifyAttackSubmission] | None = None,
    modifyattack_rand_by_participant_id: Mapping[str,int | None] | None = None,
    attack_crazed_submissions_by_participant_id: Mapping[str,EnemyAiAttackCrazedSubmission] | None = None,
    attack_crazed_rolls_by_attack_id: Mapping[str,AttackCrazedRolls] | None = None,
    wildviolent_submissions_by_participant_id: Mapping[str,EnemyAiWildViolentSubmission] | None = None,
    wildviolent_rolls_by_attack_id: Mapping[str,WildViolentRolls] | None = None,
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
    enemy_relife_submissions_by_participant_id: Mapping[
        str,EnemyAiReLifeSubmission
    ] | None = None,
    enemy_relife_rolls_by_participant_id: Mapping[
        str,EnemyReLifeRolls
    ] | None = None,
    enemy_relife_retarget_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    revivable_dead_participant_ids: Sequence[str] = (),
    profit_processed_death_ids: Sequence[str] = (),
    passive_battle_entries_by_slot: Mapping[
        int,BattleParticipant
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
    battletimid_submissions_by_participant_id: Mapping[
        str,EnemyAiBattleTimidSubmission
    ] | None = None,
    battletimid_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    two_battletimid_submissions_by_participant_id: Mapping[
        str,EnemyAiTwoBattleTimidSubmission
    ] | None = None,
    two_battletimid_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    batfly_submissions_by_participant_id: Mapping[
        str,EnemyAiBatFlySubmission
    ] | None = None,
    batfly_retarget_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    two_battletimid_default_pet_slot_by_target_id: Mapping[
        str,int
    ] | None = None,
    two_battletimid_noreturn_by_target_id: Mapping[
        str,bool
    ] | None = None,
    lighttakeed_submissions_by_participant_id: Mapping[
        str,EnemyAiLighttakeedSubmission
    ] | None = None,
    combined_submissions_by_participant_id: Mapping[
        str,EnemyAiCombinedSubmission
    ] | None = None,
    combined_rolls_by_participant_id: Mapping[
        str,CombinedActionRolls
    ] | None = None,
    combined_overlay: CombinedRuntimeOverlay | None = None,
    vary_submissions_by_participant_id: Mapping[
        str,EnemyAiVarySubmission
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
    weaken_submissions_by_participant_id: Mapping[str,EnemyAiWeakenSubmission] | None = None,
    weaken_rolls_by_participant_id: Mapping[str,WeakenActionRolls] | None = None,
    refresh_submissions_by_participant_id: Mapping[str,EnemyAiRefreshSubmission] | None = None,
    refresh_rolls_by_participant_id: Mapping[str,RefreshActionRolls] | None = None,
    setmagicpet_submissions_by_participant_id: Mapping[str,EnemyAiSetMagicPetSubmission] | None = None,
    setmagicpet_rolls_by_participant_id: Mapping[str,SetMagicPetActionRolls] | None = None,
    barrier_submissions_by_participant_id: Mapping[
        str,EnemyAiBarrierSubmission
    ] | None = None,
    barrier_rolls_by_participant_id: Mapping[
        str,BarrierActionRolls
    ] | None = None,
    nocast_overlay: NocastRoundOverlay | None = None,
    setmagicpet_overlay: SetMagicPetRoundOverlay | None = None,
    ride_pet_source_slot: int | None = None,
    field_attr: str = "none",
    field_power: int = 0,
    battlemodel_actions_by_participant_id: Mapping[str, BattleModelRoundAction] | None = None,
    default_pet_exit_authorities: Mapping[str, DefaultPetExitAuthority] | None = None,
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
    passive_slots={}
    for raw_slot,participant in (
        passive_battle_entries_by_slot or {}
    ).items():
        slot=int(raw_slot)
        if not isinstance(participant,BattleParticipant):
            raise TypeError("passive battle entry has wrong type")
        participant_id=str(participant.participant_id)
        if not 0 <= slot < BATTLE_SLOT_COUNT:
            raise ValueError("passive battle entry slot must be in 0..19")
        expected_side="player" if slot < SIDE_OFFSET else "enemy"
        if participant.side != expected_side:
            raise ValueError("passive battle entry crossed battle sides")
        if int(participant.hp) > 0:
            raise ValueError("passive battle entry must be non-living")
        if slot in by_slot:
            raise ValueError("passive battle entry collides with active slot")
        if participant_id in slot_by_id:
            raise ValueError("passive battle entry duplicates participant")
        by_slot[slot]=participant
        slot_by_id[participant_id]=slot
        passive_slots[slot]=participant_id

    hp_by_slot = {
        slot: max(0, int(participant.hp))
        for slot, participant in by_slot.items()
    }
    hp_by_id = {
        participant.participant_id: hp_by_slot[slot]
        for slot, participant in by_slot.items()
    }
    initial_revivable_dead_ids={
        str(participant_id)
        for participant_id in revivable_dead_participant_ids
    }
    unknown_revivable=sorted(
        initial_revivable_dead_ids-set(slot_by_id)
    )
    if unknown_revivable:
        raise ValueError(
            "revivable-dead identities reference unknown battle entries: "
            f"{unknown_revivable}"
        )
    for participant_id in initial_revivable_dead_ids:
        slot=int(slot_by_id[participant_id])
        if int(slot) < SIDE_OFFSET:
            raise ValueError(
                "bounded ReLife revivable entry must be enemy-side"
            )
        if int(hp_by_slot[slot]) != 0:
            raise ValueError(
                "revivable-dead identity must currently have zero HP"
            )

    initial_profit_processed_death_ids=tuple(
        str(participant_id)
        for participant_id in profit_processed_death_ids
    )
    if len(initial_profit_processed_death_ids) != len(
        set(initial_profit_processed_death_ids)
    ):
        raise ValueError(
            "processed-death identities cannot contain duplicates"
        )

    for participant_id in slot_by_id:
        if participant_id not in profiles:
            raise KeyError(f"missing combat profile for {participant_id}")
    profiles=dict(profiles)

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

    # ReLife also uses ATTACK only as an initiative/COM2 carrier.  Its
    # resurrection target is selected independently from dead enemy entries.
    enemy_relife_submissions={
        str(participant_id):submission
        for participant_id,submission in (
            enemy_relife_submissions_by_participant_id or {}
        ).items()
    }
    enemy_relife_actor_ids=set(enemy_relife_submissions)
    unknown_relife_ids=sorted(enemy_relife_actor_ids-set(slot_by_id))
    if unknown_relife_ids:
        raise ValueError(
            "enemy ReLife submissions reference unknown actors: "
            f"{unknown_relife_ids}"
        )
    if enemy_relife_actor_ids & (
        enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("enemy ReLife overlaps another semantic skill")
    for participant_id,submission in enemy_relife_submissions.items():
        if not isinstance(submission,EnemyAiReLifeSubmission):
            raise TypeError(
                f"enemy ReLife submission for {participant_id} has wrong type"
            )
        if str(submission.participant_id) != participant_id:
            raise ValueError("enemy ReLife submission participant drift")
        entry=prepared_entry_by_id[participant_id]
        if entry.participant.side != "enemy" or entry.participant.kind != "enemy":
            raise ValueError("recovered25 ReLife admits enemy actors only")
        if (
            int(entry.command.command1) != BATTLE_COM_ATTACK
            or int(entry.command.command2)
            != int(submission.source_attack_target_slot)
        ):
            raise ValueError(
                "enemy ReLife ordering carrier must be ATTACK/source target"
            )
    enemy_relife_rolls={
        str(participant_id):rolls
        for participant_id,rolls in (
            enemy_relife_rolls_by_participant_id or {}
        ).items()
    }
    if set(enemy_relife_rolls) != enemy_relife_actor_ids:
        missing=sorted(enemy_relife_actor_ids-set(enemy_relife_rolls))
        extra=sorted(set(enemy_relife_rolls)-enemy_relife_actor_ids)
        raise ValueError(
            "enemy ReLife effect RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    for participant_id,rolls in enemy_relife_rolls.items():
        if not isinstance(rolls,EnemyReLifeRolls):
            raise TypeError(
                f"enemy ReLife effect RNG for {participant_id} has wrong type"
            )
    enemy_relife_retarget_rolls={
        str(participant_id):(
            None if value is None else int(value)
        )
        for participant_id,value in (
            enemy_relife_retarget_rolls_by_participant_id or {}
        ).items()
    }
    if set(enemy_relife_retarget_rolls) != enemy_relife_actor_ids:
        missing=sorted(
            enemy_relife_actor_ids-set(enemy_relife_retarget_rolls)
        )
        extra=sorted(
            set(enemy_relife_retarget_rolls)-enemy_relife_actor_ids
        )
        raise ValueError(
            "enemy ReLife TargetAdjust RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    attempted_enemy_relife_actor_ids=set()

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
        enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
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
        damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
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
        | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
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
        | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
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
        | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
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
        | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
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
        | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
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

    wildviolent_submissions=dict(wildviolent_submissions_by_participant_id or {})
    wildviolent_actor_ids=set(wildviolent_submissions)
    if wildviolent_actor_ids-set(slot_by_id):
        raise ValueError("WildViolentAttack references unknown actors")
    if wildviolent_actor_ids & (
        guard_break2_actor_ids | barrier_actor_ids | nocast_actor_ids
        | fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("WildViolentAttack semantic submissions overlap another skill")
    for pid,submission in wildviolent_submissions.items():
        if not isinstance(submission,EnemyAiWildViolentSubmission):
            raise TypeError("WildViolentAttack submission wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            submission.participant_id!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot
            or int(entry.command.command3)!=int(submission.setup.packed_com3)
        ):
            raise ValueError(
                "WildViolentAttack ordering carrier must be enemy ATTACK/source-target/setup COM3"
            )
        if profiles[pid].counter_weapon_type!=COUNTER_WEAPON_FIST:
            raise ValueError("WildViolentAttack currently admits enemy FIST actors only")
        effects=setup_effects.get(pid,BattleCommandSetupEffects())
        if (effects.attack_power,effects.defense_power)!=(
            submission.setup.attack_power,submission.setup.defense_power
        ):
            raise ValueError("WildViolentAttack callback work-power setup drift")
    wildviolent_rolls={
        str(pid):rolls for pid,rolls in (wildviolent_rolls_by_attack_id or {}).items()
    }
    if set(wildviolent_rolls)-wildviolent_actor_ids:
        raise ValueError("WildViolentAttack RNG references non-WildViolent actors")
    if any(not isinstance(value,WildViolentRolls) for value in wildviolent_rolls.values()):
        raise TypeError("WildViolentAttack RNG wrong type")
    consumed_wildviolent_roll_ids=set()

    attack_crazed_submissions=dict(attack_crazed_submissions_by_participant_id or {})
    attack_crazed_rolls=dict(attack_crazed_rolls_by_attack_id or {})
    if set(attack_crazed_submissions)-set(slot_by_id):
        raise ValueError("AttackCrazed references unknown actors")
    if set(attack_crazed_submissions) & (
        wildviolent_actor_ids | guard_break2_actor_ids | barrier_actor_ids | nocast_actor_ids
        | fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("AttackCrazed semantic submissions overlap another skill")
    if set(attack_crazed_rolls)!=set(attack_crazed_submissions):
        raise ValueError("AttackCrazed RNG actors mismatch")
    for pid,submission in attack_crazed_submissions.items():
        if not isinstance(submission,EnemyAiAttackCrazedSubmission) or not isinstance(attack_crazed_rolls[pid],AttackCrazedRolls):
            raise TypeError("AttackCrazed submission/RNG wrong type")
        entry=prepared_entry_by_id[pid]
        if (submission.participant_id!=pid or entry.participant.kind!="enemy" or entry.participant.side!="enemy"
            or entry.command.command1!=BATTLE_COM_ATTACK or entry.command.command2!=submission.source_target_slot):
            raise ValueError("AttackCrazed ordering carrier must be enemy ATTACK/source-target")
        if profiles[pid].counter_weapon_type!=COUNTER_WEAPON_FIST:
            raise ValueError("AttackCrazed currently admits enemy FIST actors only")
        expected=submission.callback_setup(fixed_strength=entry.participant.attack,fixed_toughness=entry.participant.defense)
        effects=setup_effects.get(pid,BattleCommandSetupEffects())
        if (effects.attack_power,effects.defense_power)!=(expected.attack_power,expected.defense_power):
            raise ValueError("AttackCrazed callback work-power setup drift")

    mdfyattack_submissions=dict(mdfyattack_submissions_by_participant_id or {})
    if set(mdfyattack_submissions)-set(slot_by_id):
        raise ValueError("Mdfyattack references unknown actors")
    if set(mdfyattack_submissions) & (
        wildviolent_actor_ids | set(attack_crazed_submissions) | guard_break2_actor_ids | barrier_actor_ids
        | nocast_actor_ids | fall_ground_actor_ids | battle_tear_actor_ids
        | mp_damage_actor_ids | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("Mdfyattack semantic submissions overlap another skill")
    for pid,submission in mdfyattack_submissions.items():
        if not isinstance(submission,EnemyAiMdfyAttackSubmission):
            raise TypeError("Mdfyattack submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (submission.participant_id!=pid or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy" or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot):
            raise ValueError("Mdfyattack ordering carrier must be enemy ATTACK/source-target")
        if profiles[pid].counter_weapon_type!=COUNTER_WEAPON_FIST:
            raise ValueError("Mdfyattack currently admits enemy FIST actors only")
    weaken_submissions=dict(weaken_submissions_by_participant_id or {})
    weaken_actor_ids=set(weaken_submissions)
    if weaken_actor_ids-set(slot_by_id):
        raise ValueError("Weaken references unknown actors")
    if weaken_actor_ids & (
        wildviolent_actor_ids | set(mdfyattack_submissions) | set(attack_crazed_submissions) | guard_break2_actor_ids
        | barrier_actor_ids | nocast_actor_ids | fall_ground_actor_ids | battle_tear_actor_ids
        | mp_damage_actor_ids | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    ):
        raise ValueError("Weaken semantic submissions overlap another skill")
    for pid,submission in weaken_submissions.items():
        if not isinstance(submission,EnemyAiWeakenSubmission):
            raise TypeError("Weaken submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (submission.participant_id!=pid or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy" or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot):
            raise ValueError("Weaken ordering carrier must be enemy ATTACK/source-target")
    weaken_rolls=dict(weaken_rolls_by_participant_id or {})
    if set(weaken_rolls)!=weaken_actor_ids:
        raise ValueError("Weaken RNG actors mismatch")
    if any(not isinstance(r,WeakenActionRolls) for r in weaken_rolls.values()):
        raise TypeError("Weaken RNG has wrong type")
    attempted_weaken_actor_ids=set()
    weaken_active_command_ids=set(weaken_actor_ids)

    refresh_submissions={
        str(pid):submission
        for pid,submission in (refresh_submissions_by_participant_id or {}).items()
    }
    refresh_actor_ids=set(refresh_submissions)
    if refresh_actor_ids-set(slot_by_id):
        raise ValueError("Refresh references unknown actors")
    refresh_overlap=(
        wildviolent_actor_ids | set(mdfyattack_submissions)
        | set(attack_crazed_submissions) | weaken_actor_ids
        | guard_break2_actor_ids | barrier_actor_ids | nocast_actor_ids
        | fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    )
    if refresh_actor_ids & refresh_overlap:
        raise ValueError("Refresh semantic submissions overlap another skill")
    for pid,submission in refresh_submissions.items():
        if not isinstance(submission,EnemyAiRefreshSubmission):
            raise TypeError("Refresh submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            submission.participant_id!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot
        ):
            raise ValueError("Refresh ordering carrier must be enemy ATTACK/source-target")
    refresh_rolls={
        str(pid):rolls
        for pid,rolls in (refresh_rolls_by_participant_id or {}).items()
    }
    if set(refresh_rolls)!=refresh_actor_ids:
        raise ValueError("Refresh RNG actors mismatch")
    if any(not isinstance(rolls,RefreshActionRolls) for rolls in refresh_rolls.values()):
        raise TypeError("Refresh RNG has wrong type")
    attempted_refresh_actor_ids=set()
    refresh_active_command_ids=set(refresh_actor_ids)

    setmagicpet_submissions={
        str(pid):submission
        for pid,submission in (
            setmagicpet_submissions_by_participant_id or {}
        ).items()
    }
    setmagicpet_actor_ids=set(setmagicpet_submissions)
    if setmagicpet_actor_ids-set(slot_by_id):
        raise ValueError("SetMagicPet references unknown actors")
    setmagicpet_overlap=(
        wildviolent_actor_ids | set(mdfyattack_submissions)
        | set(attack_crazed_submissions) | weaken_actor_ids
        | refresh_actor_ids | guard_break2_actor_ids | barrier_actor_ids
        | nocast_actor_ids | fall_ground_actor_ids | battle_tear_actor_ids
        | mp_damage_actor_ids | damage_to_hp_actor_ids
        | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    )
    if setmagicpet_actor_ids & setmagicpet_overlap:
        raise ValueError("SetMagicPet semantic submissions overlap another skill")
    for pid,submission in setmagicpet_submissions.items():
        if not isinstance(submission,EnemyAiSetMagicPetSubmission):
            raise TypeError("SetMagicPet submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            submission.participant_id!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot
        ):
            raise ValueError(
                "SetMagicPet ordering carrier must be enemy ATTACK/source-target"
            )
    setmagicpet_rolls={
        str(pid):rolls
        for pid,rolls in (
            setmagicpet_rolls_by_participant_id or {}
        ).items()
    }
    if set(setmagicpet_rolls)!=setmagicpet_actor_ids:
        raise ValueError("SetMagicPet RNG actors mismatch")
    if any(
        not isinstance(rolls,SetMagicPetActionRolls)
        for rolls in setmagicpet_rolls.values()
    ):
        raise TypeError("SetMagicPet RNG has wrong type")
    attempted_setmagicpet_actor_ids=set()
    setmagicpet_active_command_ids=set(setmagicpet_actor_ids)

    battletimid_submissions={
        str(pid):submission
        for pid,submission in (
            battletimid_submissions_by_participant_id or {}
        ).items()
    }
    battletimid_actor_ids=set(battletimid_submissions)
    if battletimid_actor_ids-set(slot_by_id):
        raise ValueError("BattleTimid references unknown actors")
    battletimid_overlap=(
        wildviolent_actor_ids | set(mdfyattack_submissions)
        | set(attack_crazed_submissions) | weaken_actor_ids
        | refresh_actor_ids | setmagicpet_actor_ids | guard_break2_actor_ids
        | barrier_actor_ids | nocast_actor_ids | fall_ground_actor_ids
        | battle_tear_actor_ids | mp_damage_actor_ids | damage_to_hp_actor_ids
        | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    )
    if battletimid_actor_ids & battletimid_overlap:
        raise ValueError("BattleTimid semantic submissions overlap another skill")
    for pid,submission in battletimid_submissions.items():
        if not isinstance(submission,EnemyAiBattleTimidSubmission):
            raise TypeError("BattleTimid submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            submission.participant_id!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot
        ):
            raise ValueError(
                "BattleTimid ordering carrier must be enemy ATTACK/source-target"
            )
        effects=setup_effects.get(pid,BattleCommandSetupEffects())
        if (
            effects.attack_power,
            effects.defense_power,
        ) != (
            submission.setup.attack_power,
            submission.setup.defence_power,
        ):
            raise ValueError("BattleTimid callback work-power setup drift")
    battletimid_rolls={
        str(pid):(None if draw is None else int(draw))
        for pid,draw in (battletimid_rolls_by_participant_id or {}).items()
    }
    if set(battletimid_rolls)!=battletimid_actor_ids:
        raise ValueError("BattleTimid RNG actors mismatch")
    if any(
        draw is not None and not 0 <= int(draw) <= 99
        for draw in battletimid_rolls.values()
    ):
        raise ValueError("BattleTimid reduced rand draw must be 0..99")
    attempted_battletimid_actor_ids=set()
    battletimid_active_command_ids=set(battletimid_actor_ids)

    two_battletimid_submissions={
        str(pid):submission
        for pid,submission in (
            two_battletimid_submissions_by_participant_id or {}
        ).items()
    }
    two_battletimid_actor_ids=set(two_battletimid_submissions)
    if two_battletimid_actor_ids-set(slot_by_id):
        raise ValueError("2BattleTimid references unknown actors")
    two_battletimid_overlap=(
        battletimid_actor_ids | wildviolent_actor_ids
        | set(mdfyattack_submissions) | set(attack_crazed_submissions)
        | weaken_actor_ids | refresh_actor_ids | setmagicpet_actor_ids
        | guard_break2_actor_ids | barrier_actor_ids | nocast_actor_ids
        | fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_relife_actor_ids
        | enemy_rehp_actor_ids | attack_magic_actor_ids
    )
    if two_battletimid_actor_ids & two_battletimid_overlap:
        raise ValueError("2BattleTimid semantic submissions overlap another skill")
    for pid,submission in two_battletimid_submissions.items():
        if not isinstance(submission,EnemyAiTwoBattleTimidSubmission):
            raise TypeError("2BattleTimid submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            submission.participant_id!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot
        ):
            raise ValueError(
                "2BattleTimid ordering carrier must be enemy ATTACK/source-target"
            )
        if int(entry.combo_id)!=0:
            raise ValueError("2BattleTimid cannot inherit ordinary combo rewriting")
        effects=setup_effects.get(pid,BattleCommandSetupEffects())
        if (
            effects.attack_power,
            effects.defense_power,
        ) != (
            int(submission.setup.powers[0]),
            int(submission.setup.powers[1]),
        ):
            raise ValueError("2BattleTimid callback work-power setup drift")
    two_battletimid_rolls={
        str(pid):(None if draw is None else int(draw))
        for pid,draw in (
            two_battletimid_rolls_by_participant_id or {}
        ).items()
    }
    if set(two_battletimid_rolls)!=two_battletimid_actor_ids:
        raise ValueError("2BattleTimid RNG actors mismatch")
    if any(
        draw is not None and not 0 <= int(draw) <= 99
        for draw in two_battletimid_rolls.values()
    ):
        raise ValueError("2BattleTimid reduced rand draw must be 0..99")
    two_battletimid_default_slots={
        str(pid):int(value)
        for pid,value in (
            two_battletimid_default_pet_slot_by_target_id or {}
        ).items()
    }
    two_battletimid_noreturn={
        str(pid):value
        for pid,value in (
            two_battletimid_noreturn_by_target_id or {}
        ).items()
    }
    if any(type(value) is not bool for value in two_battletimid_noreturn.values()):
        raise TypeError("2BattleTimid NORETURN witnesses must be booleans")
    consumed_two_battletimid_draw_ids=set()
    two_battletimid_active_command_ids=set(two_battletimid_actor_ids)

    lighttakeed_submissions={
        str(pid):submission
        for pid,submission in (
            lighttakeed_submissions_by_participant_id or {}
        ).items()
    }
    lighttakeed_actor_ids=set(lighttakeed_submissions)
    if lighttakeed_actor_ids-set(slot_by_id):
        raise ValueError("Lighttakeed submissions reference unknown actors")
    lighttakeed_overlap=(
        two_battletimid_actor_ids | battletimid_actor_ids | wildviolent_actor_ids
        | set(mdfyattack_submissions) | set(attack_crazed_submissions)
        | weaken_actor_ids | refresh_actor_ids | setmagicpet_actor_ids
        | guard_break2_actor_ids | barrier_actor_ids | nocast_actor_ids
        | fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_relife_actor_ids
        | enemy_rehp_actor_ids | attack_magic_actor_ids
    )
    if lighttakeed_actor_ids & lighttakeed_overlap:
        raise ValueError("Lighttakeed semantic submissions overlap another skill")
    for pid,submission in lighttakeed_submissions.items():
        if not isinstance(submission,EnemyAiLighttakeedSubmission):
            raise TypeError("Lighttakeed submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            str(submission.participant_id)!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or int(entry.command.command1)!=BATTLE_COM_ATTACK
            or int(entry.command.command2)!=int(submission.source_target_slot)
        ):
            raise ValueError(
                "Lighttakeed ordering carrier must be enemy ATTACK/source-target"
            )
        effects=setup_effects.get(pid,BattleCommandSetupEffects())
        if (
            effects.attack_power,
            effects.defense_power,
        ) != (
            int(submission.attack_power),
            int(submission.defense_power),
        ):
            raise ValueError("Lighttakeed callback work-power setup drift")
    lighttakeed_active_command_ids=set(lighttakeed_actor_ids)

    combined_submissions={
        str(pid):submission
        for pid,submission in (
            combined_submissions_by_participant_id or {}
        ).items()
    }
    combined_actor_ids=set(combined_submissions)
    if combined_actor_ids-set(slot_by_id):
        raise ValueError("Combined submissions reference unknown actors")
    combined_overlap=(
        lighttakeed_actor_ids | two_battletimid_actor_ids
        | battletimid_actor_ids | wildviolent_actor_ids
        | set(mdfyattack_submissions) | set(attack_crazed_submissions)
        | weaken_actor_ids | refresh_actor_ids | setmagicpet_actor_ids
        | guard_break2_actor_ids | barrier_actor_ids | nocast_actor_ids
        | fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    )
    if combined_actor_ids & combined_overlap:
        raise ValueError("Combined semantic submissions overlap another skill")
    for pid,submission in combined_submissions.items():
        if not isinstance(submission,EnemyAiCombinedSubmission):
            raise TypeError("Combined submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            str(submission.participant_id)!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or int(entry.command.command1)!=BATTLE_COM_ATTACK
            or int(entry.command.command2)!=int(submission.source_target_slot)
        ):
            raise ValueError(
                "Combined ordering carrier must be enemy ATTACK/source-target"
            )
    combined_rolls={
        str(pid):rolls
        for pid,rolls in (
            combined_rolls_by_participant_id or {}
        ).items()
    }
    if set(combined_rolls)!=combined_actor_ids:
        missing=sorted(combined_actor_ids-set(combined_rolls))
        extra=sorted(set(combined_rolls)-combined_actor_ids)
        raise ValueError(
            "Combined action RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    if any(
        not isinstance(rolls,CombinedActionRolls)
        for rolls in combined_rolls.values()
    ):
        raise TypeError("Combined action RNG has wrong type")
    if combined_actor_ids and combined_overlay is None:
        raise ValueError("Combined semantic action requires explicit runtime overlay")
    if combined_overlay is not None:
        if not isinstance(combined_overlay,CombinedRuntimeOverlay):
            raise TypeError("combined_overlay has wrong type")
        combined_overlay.validate_participants(slot_by_id)
    combined_working=combined_overlay
    attempted_combined_actor_ids=set()
    combined_active_command_ids=set(combined_actor_ids)
    combined_cleared_command_ids=set()

    vary_submissions={
        str(pid):submission
        for pid,submission in (
            vary_submissions_by_participant_id or {}
        ).items()
    }
    vary_actor_ids=set(vary_submissions)
    if vary_actor_ids-set(slot_by_id):
        raise ValueError("Vary submissions reference unknown actors")
    vary_overlap=(
        lighttakeed_actor_ids | combined_actor_ids | two_battletimid_actor_ids
        | battletimid_actor_ids
        | wildviolent_actor_ids
        | set(mdfyattack_submissions) | set(attack_crazed_submissions)
        | weaken_actor_ids | refresh_actor_ids | setmagicpet_actor_ids
        | guard_break2_actor_ids | barrier_actor_ids | nocast_actor_ids
        | fall_ground_actor_ids | battle_tear_actor_ids | mp_damage_actor_ids
        | damage_to_hp_actor_ids | enemy_relife_actor_ids | enemy_rehp_actor_ids | attack_magic_actor_ids
    )
    if vary_actor_ids & vary_overlap:
        raise ValueError("Vary semantic submissions overlap another skill")
    for pid,submission in vary_submissions.items():
        if not isinstance(submission,EnemyAiVarySubmission):
            raise TypeError("Vary submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            str(submission.participant_id)!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or int(entry.command.command1)!=BATTLE_COM_ATTACK
            or int(entry.command.command2)!=int(submission.source_target_carrier)
        ):
            raise ValueError(
                "Vary ordering carrier must be enemy ATTACK/source-target"
            )
    vary_active_command_ids=set(vary_actor_ids)

    modifyattack_submissions={str(pid):value for pid,value in (modifyattack_submissions_by_participant_id or {}).items()}
    modifyattack_actor_ids=set(modifyattack_submissions)
    if modifyattack_actor_ids-set(slot_by_id):
        raise ValueError("Modifyattack references unknown actors")
    if modifyattack_actor_ids & (vary_overlap | vary_actor_ids):
        raise ValueError("Modifyattack semantic submissions overlap another skill")
    for pid,submission in modifyattack_submissions.items():
        if not isinstance(submission,EnemyAiModifyAttackSubmission):
            raise TypeError("Modifyattack submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (submission.participant_id!=pid or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy" or entry.command.command1!=BATTLE_COM_ATTACK
            or entry.command.command2!=submission.source_target_slot):
            raise ValueError("Modifyattack ordering carrier must be enemy ATTACK/source-target")
        if profiles[pid].counter_weapon_type!=COUNTER_WEAPON_FIST:
            raise ValueError("Modifyattack currently admits enemy FIST actors only")
        if setup_effects.get(pid,BattleCommandSetupEffects())!=BattleCommandSetupEffects():
            raise ValueError("Modifyattack callback does not mutate work powers")
    modifyattack_rand={str(pid):value for pid,value in (modifyattack_rand_by_participant_id or {}).items()}
    if set(modifyattack_rand)!=modifyattack_actor_ids:
        raise ValueError("Modifyattack helper RNG actors mismatch")
    if any(value is not None and (type(value) is not int or not 0<=value<2**31) for value in modifyattack_rand.values()):
        raise ValueError("Modifyattack requires raw nonnegative signed-int rand result")
    modifyattack_active_command_ids=set(modifyattack_actor_ids)
    consumed_modifyattack_rand_ids=set()

    batfly_submissions={
        str(pid):submission
        for pid,submission in (
            batfly_submissions_by_participant_id or {}
        ).items()
    }
    batfly_actor_ids=set(batfly_submissions)
    if batfly_actor_ids-set(slot_by_id):
        raise ValueError("BatFly submissions reference unknown actors")
    batfly_overlap=(
        attack_magic_actor_ids | enemy_rehp_actor_ids | enemy_relife_actor_ids
        | damage_to_hp_actor_ids | mp_damage_actor_ids | fall_ground_actor_ids
        | battle_tear_actor_ids | nocast_actor_ids | guard_break2_actor_ids
        | barrier_actor_ids | weaken_actor_ids | refresh_actor_ids
        | setmagicpet_actor_ids | battletimid_actor_ids
        | two_battletimid_actor_ids | lighttakeed_actor_ids
        | combined_actor_ids | vary_actor_ids | modifyattack_actor_ids
        | set(mdfyattack_submissions) | set(attack_crazed_submissions)
        | wildviolent_actor_ids
    )
    if batfly_actor_ids & batfly_overlap:
        raise ValueError("BatFly semantic submissions overlap another skill")
    for pid,submission in batfly_submissions.items():
        if not isinstance(submission,EnemyAiBatFlySubmission):
            raise TypeError("BatFly submission has wrong type")
        entry=prepared_entry_by_id[pid]
        if (
            str(submission.participant_id)!=pid
            or entry.participant.kind!="enemy"
            or entry.participant.side!="enemy"
            or int(entry.command.command1)!=BATTLE_COM_ATTACK
            or int(entry.command.command2)!=int(submission.source_target_slot)
        ):
            raise ValueError(
                "BatFly ordering carrier must be enemy ATTACK/source-target"
            )
        if int(entry.combo_id)!=0:
            raise ValueError("BatFly cannot inherit ordinary combo rewriting")
        if setup_effects.get(pid,BattleCommandSetupEffects()) != BattleCommandSetupEffects():
            raise ValueError("BatFly callback does not mutate work powers")
    batfly_retarget_rolls={
        str(pid):(None if draw is None else int(draw))
        for pid,draw in (
            batfly_retarget_rolls_by_participant_id or {}
        ).items()
    }
    if set(batfly_retarget_rolls)!=batfly_actor_ids:
        missing=sorted(batfly_actor_ids-set(batfly_retarget_rolls))
        extra=sorted(set(batfly_retarget_rolls)-batfly_actor_ids)
        raise ValueError(
            "BatFly TargetAdjust RNG actors mismatch; "
            f"missing={missing}, extra={extra}"
        )
    if any(
        draw is not None and int(draw)<0
        for draw in batfly_retarget_rolls.values()
    ):
        raise ValueError("BatFly TargetAdjust draw cannot be negative")
    batfly_active_command_ids=set(batfly_actor_ids)

    # The scheduling carrier cannot confer native ATTACK counter eligibility.
    # Confusion later removes a rewritten actor from this symbolic-command set.
    mdfyattack_active_command_ids=set(mdfyattack_submissions)

    if (
        nocast_actor_ids or barrier_actor_ids or weaken_actor_ids
        or refresh_actor_ids or combined_actor_ids
    ) and nocast_overlay is None:
        raise ValueError(
            "Nocast/Barrier/Weaken/Refresh/Combined semantic action requires explicit round overlay"
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

    if setmagicpet_actor_ids and setmagicpet_overlay is None:
        raise ValueError(
            "SetMagicPet semantic action requires explicit round overlay"
        )
    if setmagicpet_overlay is not None and not isinstance(
        setmagicpet_overlay,SetMagicPetRoundOverlay
    ):
        raise TypeError("setmagicpet_overlay has wrong type")
    setmagicpet_working=(
        None
        if setmagicpet_overlay is None
        else dict(setmagicpet_overlay.runtime_by_participant_id)
    )
    if setmagicpet_working is not None:
        missing_magicpet_runtime=sorted(
            set(slot_by_id)-set(setmagicpet_working)
        )
        if missing_magicpet_runtime:
            raise ValueError(
                "SetMagicPet overlay lacks active participants: "
                + ",".join(missing_magicpet_runtime)
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

    def tick_setmagicpet_runtime_for_actor(
        participant_id: str,
        slot: int,
        command_code: int,
        action_value: int,
    ) -> SetMagicPetTurnTick | None:
        if setmagicpet_working is None:
            return None
        participant_id=str(participant_id)
        runtime=setmagicpet_working[participant_id]
        runtime,tick=tick_setmagicpet_runtime(runtime)
        setmagicpet_working[participant_id]=runtime
        if tick is None:
            return None
        events.append(
            OrdinaryRoundEvent(
                participant_id,
                int(slot),
                int(command_code),
                int(action_value),
                "setmagicpet_tick",
                original_target_slot=int(slot),
                resolved_target_slot=int(slot),
                setmagicpet_turn_tick=tick,
            )
        )
        return tick

    def tick_weaken_runtime(
        participant_id: str,
        slot: int,
        command_code: int,
        action_value: int,
    ) -> BarrierSelfTick | None:
        if nocast_working is None:
            return None
        participant_id=str(participant_id)
        runtime=nocast_working[participant_id]
        if int(runtime.weaken_counter) <= 0:
            return None
        tick=resolve_weaken_self_tick(
            int(runtime.weaken_counter),
            barrier_active_at_visit=bool(runtime.barrier_active_for_late_statuses),
        )
        nocast_working[participant_id]=runtime.after_weaken_tick(tick)
        events.append(
            OrdinaryRoundEvent(
                participant_id,
                int(slot),
                int(command_code),
                int(action_value),
                "weaken_tick",
                original_target_slot=int(slot),
                resolved_target_slot=int(slot),
                weaken_tick_resolution=tick,
            )
        )
        return tick

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
            weaken_active_at_visit=bool(runtime.weaken_active_for_late_statuses),
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
            weaken_active_at_visit=bool(runtime.weaken_active_for_late_statuses),
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
    revivable_dead_ids=set(initial_revivable_dead_ids)
    # Source ISDIE is independent from ReLife eligibility. Player/pet deaths
    # also need to survive across rounds so a later AddProfit scan cannot charge
    # them twice. The persistent caller supplies that explicit state.
    profit_processed_death_ids=set(initial_profit_processed_death_ids)
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

    battlemodel_actions=dict(battlemodel_actions_by_participant_id or {})
    battlemodel_actor_ids=set(battlemodel_actions)
    if battlemodel_actor_ids-set(prepared_entry_by_id):
        raise ValueError("BattleModel actions reference unknown prepared actors")
    if battlemodel_actions:
        other_semantics=(
            attack_magic_submissions or enemy_rehp_submissions or enemy_relife_submissions
            or damage_to_hp_submissions or mp_damage_submissions or battle_tear_submissions
            or guard_break2_submissions or battletimid_submissions or two_battletimid_submissions
            or batfly_submissions or lighttakeed_submissions or combined_submissions
            or vary_submissions or fall_ground_submissions or nocast_submissions
            or weaken_submissions or refresh_submissions or setmagicpet_submissions
            or barrier_submissions or attack_crazed_submissions or wildviolent_submissions
            or modifyattack_submissions or mdfyattack_submissions
        )
        if (other_semantics or ride_runtime is not None or nocast_overlay is not None
            or setmagicpet_overlay is not None or attack_magic_overlay is not None
            or combined_overlay is not None or counter_rolls_by_attack_id is not None):
            raise ValueError("BattleModel ordinary scope excludes other callbacks/overlays/ride/counter")
        if any(e.command.command1 not in {BATTLE_COM_ATTACK,BATTLE_COM_GUARD,BATTLE_COM_NONE,BATTLE_COM_WAIT}
               or e.combo_id for e in prepared.ordered_entries):
            raise ValueError("BattleModel ordinary scope requires noncombo base commands")
    for pid,action in battlemodel_actions.items():
        if not isinstance(action,BattleModelRoundAction):
            raise TypeError("typed BattleModel round actions required")
        entry=prepared_entry_by_id[pid]
        if (action.submission.participant_id != pid or entry.participant.kind != "enemy"
            or entry.participant.side != "enemy" or entry.command.command1 != BATTLE_COM_NONE
            or entry.command.command2 != action.submission.source_target_carrier):
            raise ValueError("BattleModel symbolic NONE/source-target carrier identity drift")
        context=action.physical_context
        if (set(context.profiles) != set(by_slot)
            or set(action.paralysis_resistance_by_slot) != set(by_slot)
            or set(action.opposing_slot_order) != {s for s in by_slot if s < SIDE_OFFSET}):
            raise ValueError("BattleModel current profile/resistance/opposing slot coverage mismatch")
        if context.defense_profile != defense_profile or (context.field_attr,context.field_power) != (field_attr,field_power):
            raise ValueError("BattleModel physical defense/field profile drift")
        if dict(context.guardians) != guardian_registrations:
            raise ValueError("BattleModel Guardian registrations drift")
        for s,p in by_slot.items():
            pp=context.profiles[s]
            combat=profiles[p.participant_id]
            quick=status_runtime[p.participant_id].work_quick
            if quick is None:
                quick=int(p.quick)
            if (pp.participant_id,pp.level,pp.fixed_dex,pp.fixed_luck,pp.defense_power,pp.quick,pp.elements,pp.fixed_vital) != (
                p.participant_id,int(p.level),int(combat.fixed_dex),int(combat.fixed_luck),
                _effective_defense_power(p,setup_effects),quick,combat.elements,p.fixed_vital):
                raise ValueError("BattleModel physical participant/current work drift")
            if pp.no_dodge or int(combat.weapon_critical) != 0 or combat.counter_weapon_type != COUNTER_WEAPON_FIST:
                raise ValueError("BattleModel ordinary scope requires no equipment critical/NO_DUCK/weapon feature")
        actor=entry.participant
        if (_effective_attack_power(actor,setup_effects),_effective_defense_power(actor,setup_effects),int(actor.quick)) != action.submission.setup.powers:
            raise ValueError("BattleModel callback post-setup work-power drift")
        bound_entries={s:BattleModelEntry(p.participant_id,p.kind,hp_by_slot[s],p.max_hp,
            action.paralysis_resistance_by_slot[s]) for s,p in by_slot.items()}
        action.itemcrush_context.bind(bound_entries,source_profile=action.submission.source_profile)
        if any(action.itemcrush_context.participants[s].level != context.profiles[s].level for s in by_slot):
            raise ValueError("BattleModel ItemCrush physical level drift")
    battlemodel_active_command_ids=set(battlemodel_actor_ids)
    battlemodel_cleared_command_ids=set()
    attempted_battlemodel_actor_ids=set()
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
    for passive_slot in passive_slots:
        command_by_slot.setdefault(
            int(passive_slot),
            BattleCommand(BATTLE_COM_NONE,input_complete=False),
        )
        action_value_by_slot.setdefault(int(passive_slot),0)
    escaped_ids: list[str] = []
    ultimate_exited_ids: list[str] = []
    # Source BENT_FLG_ULTIMATE is cleared at the start of each battle turn.
    # Keep it round-local; do not persist it across PersistentBattleState.
    ultimate_marked_slots: dict[int,int] = {}
    default_authorities=bind_exit_authorities(default_pet_exit_authorities,by_slot)

    def clear_player_exit_overlay(owner_id: str) -> None:
        if nocast_working is None:
            return
        if owner_id not in default_authorities:
            raise ValueError("player ultimate exit requires explicit default-pet authority")
        authority=default_authorities[owner_id]
        cleared=NocastRoundOverlay(nocast_working).after_player_exit(
            owner_id,authority.owned_pet_ids)
        nocast_working.clear()
        nocast_working.update(cleared.runtime_by_participant_id)

    profit_boundaries: list[OrdinaryProfitBoundarySnapshot] = []

    def capture_profit_boundary(
        new_events: Sequence[OrdinaryRoundEvent],
        *,
        boundary_kind: str,
    ) -> None:
        if not new_events:
            return
        start=len(events)-len(new_events)
        if start < 0 or any(
            events[start+offset] is not event
            for offset,event in enumerate(new_events)
        ):
            raise ValueError(
                "profit boundary events must be the current chronological tail"
            )
        profit_boundaries.append(
            OrdinaryProfitBoundarySnapshot(
                boundary_kind=boundary_kind,
                trigger_event_indexes=tuple(
                    range(start,start+len(new_events))
                ),
                hp_by_slot=MappingProxyType(dict(hp_by_slot)),
                occupied_participant_id_by_slot=MappingProxyType({
                    int(slot):str(participant.participant_id)
                    for slot,participant in by_slot.items()
                    if int(slot) not in exited_slots
                }),
                ultimate_kind_by_slot=MappingProxyType(
                    dict(ultimate_marked_slots)
                ),
                prior_processed_death_ids=tuple(
                    sorted(profit_processed_death_ids)
                ),
                default_pet_authorities_by_owner_id=MappingProxyType(
                    dict(default_authorities)
                ),
                base_status_runtime_by_participant_id=MappingProxyType(
                    dict(status_runtime)
                ),
                nocast_overlay=(
                    None
                    if nocast_working is None
                    else NocastRoundOverlay(nocast_working)
                ),
            )
        )

    def register_ultimate_exits(
        new_events: Sequence[OrdinaryRoundEvent],
        *,
        boundary_kind: str,
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

        capture_profit_boundary(
            new_events,
            boundary_kind=boundary_kind,
        )

        for event in new_events:
            if (
                event.target_hp_before is not None
                and event.target_hp_after is not None
                and int(event.target_hp_before) > 0
                and int(event.target_hp_after) == 0
                and event.resolved_target_slot is not None
            ):
                dead_slot=int(event.resolved_target_slot)
                if (
                    dead_slot in by_slot
                    and dead_slot >= SIDE_OFFSET
                    and by_slot[dead_slot].side == "enemy"
                    and int(ultimate_marked_slots.get(dead_slot,0)) <= 0
                ):
                    revivable_dead_ids.add(
                        str(by_slot[dead_slot].participant_id)
                    )

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

            revivable_dead_ids.discard(target_id)
            exited_slots.add(target_slot)
            ultimate_exited_ids.append(target_id)

            if target.kind == "pet":
                owner_id=pet_owner_id(target_id,default_authorities)
                clear_owner_selection(default_authorities,owner_id)
                for index,recorded in enumerate(events):
                    if recorded is event:
                        events[index]=replace(recorded,
                            default_pet_selection_cleared_owner_id=owner_id)
                        break
            if target.kind != "player":
                continue

            clear_player_exit_overlay(target_id)
            for pet_id in player_pet_exit_ids(target_slot,target_id,
                default_authorities,by_slot,exited_slots):
                pet_slot=default_authorities[target_id].occupied_pet_slots[pet_id]
                exited_slots.add(pet_slot)
                profit_processed_death_ids.discard(str(pet_id))
                if pet_id not in ultimate_exited_ids:
                    ultimate_exited_ids.append(pet_id)

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
                if other.participant_id not in default_authorities[target_id].owned_pet_ids:
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

        # Carry source-like ISDIE chronology to the next observed boundary.
        # Ultimate/Exit entries are no longer occupied; normal dead occupied
        # entries become processed. The persistent layer does not consume this
        # metadata yet.
        for observed_slot,observed in by_slot.items():
            observed_id=str(observed.participant_id)
            if int(observed_slot) in exited_slots:
                profit_processed_death_ids.discard(observed_id)
            elif int(hp_by_slot.get(observed_slot,0)) <= 0:
                profit_processed_death_ids.add(observed_id)
            else:
                profit_processed_death_ids.discard(observed_id)

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
            semantic_noncounter_actor_ids=frozenset(
                modifyattack_active_command_ids | mdfyattack_active_command_ids
                | weaken_active_command_ids
                | refresh_active_command_ids
                | setmagicpet_active_command_ids
                | battletimid_active_command_ids
                | two_battletimid_active_command_ids
                | batfly_active_command_ids
                | lighttakeed_active_command_ids
                | combined_active_command_ids
                | vary_active_command_ids
            ),
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
        register_ultimate_exits(
            counter_events,
            boundary_kind=PROFIT_BOUNDARY_COUNTER_CHAIN_CURRENT_DRIVER,
        )

    for entry in prepared.ordered_entries:
        apply_selection_events(default_authorities,events,by_slot)
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
        if str(participant_id) in combined_cleared_command_ids or str(participant_id) in battlemodel_cleared_command_ids:
            command=BattleCommand(
                BATTLE_COM_NONE,
                command2=entry.command.command2,
                command3=entry.command.command3,
                input_complete=entry.command.input_complete,
            )
            guarding.discard(slot)
            combined_active_command_ids.discard(str(participant_id))
            battlemodel_active_command_ids.discard(str(participant_id))
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
                        and late_runtime.weaken_active_for_late_statuses
                    ),
                    barrier_freeze_active=bool(
                        late_runtime is not None
                        and late_runtime.barrier_active_for_late_statuses
                    ),
                )
            )
            current_status_tick=tick
            if tick.confusion_rewrote_command:
                battlemodel_active_command_ids.discard(str(participant_id))
                modifyattack_active_command_ids.discard(str(participant_id))
                mdfyattack_active_command_ids.discard(str(participant_id))
                weaken_active_command_ids.discard(str(participant_id))
                refresh_active_command_ids.discard(str(participant_id))
                setmagicpet_active_command_ids.discard(str(participant_id))
                battletimid_active_command_ids.discard(str(participant_id))
                two_battletimid_active_command_ids.discard(str(participant_id))
                batfly_active_command_ids.discard(str(participant_id))
                lighttakeed_active_command_ids.discard(str(participant_id))
                combined_active_command_ids.discard(str(participant_id))
                vary_active_command_ids.discard(str(participant_id))
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
                battlemodel_active_command_ids.discard(str(participant_id))
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

        tick_setmagicpet_runtime_for_actor(
            str(participant_id),int(slot),
            int(entry.command.command1),int(entry.action_value)
        )
        tick_weaken_runtime(str(participant_id), int(slot),
                            int(entry.command.command1), int(entry.action_value))
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

        if str(participant_id) in battlemodel_active_command_ids:
            action=battlemodel_actions[str(participant_id)]
            battlemodel_event_start=len(events)
            before_hp=dict(hp_by_slot)
            loop=execute_current_battlemodel_round_action(action,actor_slot=slot,
                by_slot=by_slot,hp_by_slot=hp_by_slot,status_runtime=status_runtime,
                damage_react_state=damage_react_state,ultimate_overkill=ultimate_overkill,
                guarding_slots=frozenset(guarding),cleared_command_ids=battlemodel_cleared_command_ids,
                ultimate_marked_slots=ultimate_marked_slots,exited_slots=exited_slots,battle_abio=battle_abio)
            attempted_battlemodel_actor_ids.add(str(participant_id))
            if loop is None:
                events.append(OrdinaryRoundEvent(str(participant_id),slot,BATTLE_COM_NONE,
                    entry.action_value,"battlemodel_no_target",battlemodel_skill_id=638))
                register_ultimate_exits(
                    (events[-1],),
                    boundary_kind=PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,
                )
                continue
            for target_slot,work in loop.entries.items():
                target_id=work.participant_id
                hp_by_slot[target_slot]=work.hp
                hp_by_id[target_id]=work.hp
                status_runtime[target_id]=work.status_runtime
                damage_react_state[target_id]=work.reaction
                ultimate_overkill[target_id]=work.accumulated_overkill
            for cleared_slot in loop.cleared_command_slots:
                cleared_id=by_slot[cleared_slot].participant_id
                battlemodel_cleared_command_ids.add(cleared_id)
                command_by_slot[cleared_slot]=replace(command_by_slot[cleared_slot],command1=BATTLE_COM_NONE)
                guarding.discard(cleared_slot)
                battlemodel_active_command_ids.discard(cleared_id)
            for hit in loop.events:
                actual=hit.actual_defender_slot
                hp_before=before_hp[actual] if actual is not None else None
                hp_after=hp_before-hit.hp_loss if actual is not None else None
                if actual is not None:
                    before_hp[actual]=hp_after
                events.append(OrdinaryRoundEvent(str(participant_id),slot,BATTLE_COM_NONE,
                    entry.action_value,"battlemodel_"+hit.outcome,
                    original_target_slot=hit.attack.target_slot,resolved_target_slot=actual,
                    damage=hit.reported_damage,critical=hit.outcome=="critical",
                    target_hp_before=hp_before,target_hp_after=hp_after,
                    guardian_redirected=actual is not None and actual!=hit.attack.target_slot,
                    guardian_slot=actual if actual!=hit.attack.target_slot else None,
                    status_application_resolution=hit.status_application,
                    damage_react_resolution=hit.reaction,battlemodel_skill_id=638))
            events.append(OrdinaryRoundEvent(str(participant_id),slot,BATTLE_COM_NONE,
                entry.action_value,"battlemodel_action",battlemodel_skill_id=638,
                battlemodel_loop_resolution=loop))
            register_ultimate_exits(
                tuple(events[battlemodel_event_start:]),
                boundary_kind=PROFIT_BOUNDARY_BATTLEMODEL_COMMAND_TAIL,
            )
            continue

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
                                and candidate_late_runtime.weaken_active_for_late_statuses
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

                tick_weaken_runtime(candidate_id, candidate_slot,
                                    int(candidate.command.command1), int(candidate.action_value))
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
            register_ultimate_exits(
                combo_events,
                boundary_kind=PROFIT_BOUNDARY_COMBO_COMMAND_TAIL,
            )
            active_ride=bool(
                ride_runtime is not None and ride_runtime.mounted
            )
            processed_combo_ids.add(int(entry.combo_id))
            continue

        crazed_submission=attack_crazed_submissions.get(str(participant_id))
        wild_submission=wildviolent_submissions.get(str(participant_id))
        execute_crazed=bool(
            crazed_submission is not None and command.command1==BATTLE_COM_ATTACK
            and not (current_status_tick is not None and current_status_tick.confusion_rewrote_command)
        )
        execute_wild=bool(
            wild_submission is not None and command.command1==BATTLE_COM_ATTACK
            and not (current_status_tick is not None and current_status_tick.confusion_rewrote_command)
        )
        if execute_crazed and execute_wild:
            raise ValueError("multihit semantic execution overlap")
        if command.command1 == BATTLE_COM_S_RENZOKU or execute_crazed or execute_wild:
            continuation_id=str(participant_id)
            if (
                not execute_crazed and not execute_wild
                and continuation_id not in normalized_continuation_rolls
            ):
                raise KeyError(f"missing ContinuationAttack rolls for {continuation_id}")
            if execute_wild:
                if continuation_id not in wildviolent_rolls:
                    raise KeyError(
                        f"missing WildViolentAttack action-time rolls for {continuation_id}"
                    )
                consumed_wildviolent_roll_ids.add(continuation_id)
            continuation=_resolve_nonbow_multihit_baseline(
                actor=participant,
                actor_slot=int(slot),
                command=command,
                action_value=int(entry.action_value),
                by_slot=by_slot,
                default_pet_exit_authorities=default_authorities,
                hp_by_slot=hp_by_slot,
                profiles=profiles,
                command_by_slot=command_by_slot,
                rolls=(
                    attack_crazed_rolls[continuation_id]
                    if execute_crazed else (
                        wildviolent_rolls[continuation_id]
                        if execute_wild else normalized_continuation_rolls[continuation_id]
                    )
                ),
                attack_crazed_submission=crazed_submission if execute_crazed else None,
                wildviolent_submission=wild_submission if execute_wild else None,
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
            apply_selection_events(default_authorities,continuation_events,by_slot)
            for exit_id in continuation.ultimate_exited_participant_ids:
                exit_id=str(exit_id)
                exit_slot=slot_by_id.get(exit_id)
                if exit_slot is None:
                    exit_slot=next((a.occupied_pet_slots[exit_id]
                        for a in default_authorities.values()
                        if exit_id in a.occupied_pet_slots),None)
                if exit_slot is None:
                    raise ValueError("ContinuationAttack ultimate exit references unknown actor")
                exit_slot=int(exit_slot)
                exited_slots.add(exit_slot)
                if exit_id not in ultimate_exited_ids:
                    ultimate_exited_ids.append(exit_id)
                if exit_id in slot_by_id and by_slot[slot_by_id[exit_id]].kind == "player":
                    # The multihit resolver owns immediate HP/base clear. Bind
                    # its actual player Exit to the outer late-status overlay
                    # before any later prepared actor executes.
                    clear_player_exit_overlay(exit_id)
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
                command3=(
                    battle_command3_low(command.command3)
                    if execute_wild else command.command3
                ),
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

        batfly_actor_id=str(participant_id)
        if (
            batfly_actor_id in batfly_active_command_ids
            and int(command.command1) == BATTLE_COM_ATTACK
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=batfly_submissions[batfly_actor_id]
            if int(command.command2) != int(submission.source_target_slot):
                raise ValueError(
                    "BatFly ordering carrier target drift before execution"
                )
            living_opposing_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    _slot_side(other_slot)==0
                    and other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0))>0
                )
            )
            gate=submission.execution_gate(
                living_opposing_slots=living_opposing_slots,
                retarget_roll=batfly_retarget_rolls[batfly_actor_id],
            )
            if not gate.executable:
                events.append(
                    OrdinaryRoundEvent(
                        batfly_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "batfly_no_action",
                        original_target_slot=int(submission.source_target_slot),
                        resolved_target_slot=gate.adjusted_target_slot,
                        retargeted=bool(gate.retargeted),
                        batfly_execution_gate=gate,
                        batfly_skill_id=int(submission.skill_id),
                    )
                )
                continue

            target_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    _slot_side(other_slot)==0
                    and other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0))>0
                )
            )
            target_inputs=[]
            for target_slot in target_slots:
                target_actor=by_slot[int(target_slot)]
                target_id=str(target_actor.participant_id)
                ride_hp=None
                if (
                    target_actor.kind=="player"
                    and ride_runtime is not None
                    and str(ride_runtime.rider_id)==target_id
                    and bool(ride_runtime.mounted)
                ):
                    ride_hp=int(ride_runtime.hp)
                target_inputs.append(
                    BatFlyTarget(
                        character_hp=int(hp_by_slot[int(target_slot)]),
                        ride_pet_hp=ride_hp,
                    )
                )
            batfly_resolution=submission.effect(
                attacker_hp=int(hp_by_slot[int(slot)]),
                attacker_max_hp=int(participant.max_hp),
                targets=tuple(target_inputs),
            )
            batfly_events=[]
            for target_slot,target_resolution in zip(
                target_slots,batfly_resolution.targets
            ):
                target_actor=by_slot[int(target_slot)]
                target_id=str(target_actor.participant_id)
                before=int(hp_by_slot[int(target_slot)])
                after=int(target_resolution.character_hp_after)
                if before!=int(target_resolution.character_hp_before):
                    raise ValueError("BatFly target HP snapshot drift")
                hp_by_slot[int(target_slot)]=after
                hp_by_id[target_id]=after
                fell_rider_id=None
                if target_resolution.ride_pet_hp_before is not None:
                    if (
                        ride_runtime is None
                        or target_actor.kind!="player"
                        or str(ride_runtime.rider_id)!=target_id
                    ):
                        raise ValueError("BatFly ride target lost runtime identity")
                    if int(ride_runtime.hp)!=int(
                        target_resolution.ride_pet_hp_before
                    ):
                        raise ValueError("BatFly ride-pet HP snapshot drift")
                    ride_runtime=replace(
                        ride_runtime,
                        hp=int(target_resolution.ride_pet_hp_after),
                        mounted=(
                            False
                            if target_resolution.ride_pet_fell
                            else bool(ride_runtime.mounted)
                        ),
                        petfall=(
                            True
                            if target_resolution.ride_pet_fell
                            else bool(ride_runtime.petfall)
                        ),
                    )
                    if target_resolution.ride_pet_fell:
                        active_ride=False
                        fell_rider_id=target_id
                batfly_events.append(
                    OrdinaryRoundEvent(
                        batfly_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "batfly_drain",
                        original_target_slot=int(submission.source_target_slot),
                        resolved_target_slot=int(target_slot),
                        retargeted=bool(gate.retargeted),
                        damage=int(target_resolution.character_drain),
                        target_hp_before=before,
                        target_hp_after=after,
                        ride_pet_fell_rider_id=fell_rider_id,
                        batfly_execution_gate=gate,
                        batfly_target_resolution=target_resolution,
                        batfly_resolution=batfly_resolution,
                        batfly_skill_id=int(submission.skill_id),
                    )
                )
            hp_by_slot[int(slot)]=int(batfly_resolution.attacker_hp_after)
            hp_by_id[batfly_actor_id]=int(batfly_resolution.attacker_hp_after)
            events.extend(batfly_events)
            register_ultimate_exits(
                batfly_events,
                boundary_kind=PROFIT_BOUNDARY_BATFLY_COMMAND_TAIL_CURRENT_DRIVER,
            )
            continue

        vary_actor_id=str(participant_id)
        if (
            vary_actor_id in vary_submissions
            and vary_actor_id in vary_active_command_ids
            and int(command.command1) == BATTLE_COM_ATTACK
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=vary_submissions[vary_actor_id]
            if int(command.command2) != int(submission.source_target_carrier):
                raise ValueError(
                    "Vary ordering carrier target drift before execution"
                )
            events.append(
                OrdinaryRoundEvent(
                    vary_actor_id,
                    int(slot),
                    BATTLE_COM_ATTACK,
                    int(entry.action_value),
                    "vary_applied",
                    original_target_slot=int(submission.source_target_carrier),
                    vary_skill_id=int(submission.skill_id),
                    vary_visual_effect_enabled=bool(
                        submission.runtime_after_callback.visual_effect_enabled
                    ),
                )
            )
            continue

        combined_actor_id=str(participant_id)
        if (
            combined_actor_id in combined_submissions
            and combined_actor_id in combined_active_command_ids
            and int(command.command1) == BATTLE_COM_ATTACK
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=combined_submissions[combined_actor_id]
            if int(command.command2) != int(submission.source_target_slot):
                raise ValueError(
                    "Combined ordering carrier target drift before execution"
                )
            if combined_working is None:
                raise ValueError("Combined working overlay unexpectedly absent")
            if nocast_working is None:
                raise ValueError("Combined Nocast/status overlay unexpectedly absent")
            if combined_actor_id not in combined_working.mp_by_participant_id:
                raise ValueError(
                    "Combined actor lacks explicit current-MP witness"
                )
            action_rolls=combined_rolls[combined_actor_id]
            current_mp=int(
                combined_working.mp_by_participant_id[combined_actor_id]
            )
            route=submission.direct_magic_route(
                current_mp=current_mp,
                item_zero=combined_working.item_zero,
                nocast=int(nocast_working[combined_actor_id].counter),
                caster_valid=True,
                battle_mode_init=False,
                battling=True,
                function_present=True,
                battle_effect_return=True,
                family_index=0,
            )
            attempted_combined_actor_ids.add(combined_actor_id)
            if int(route.remaining_mp) != current_mp:
                combined_working=combined_working.with_mp(
                    combined_actor_id,int(route.remaining_mp)
                )
            if not route.accepted:
                if action_rolls != CombinedActionRolls():
                    raise ValueError(
                        "rejected Combined DirectUse cannot consume action RNG"
                    )
                events.append(
                    OrdinaryRoundEvent(
                        combined_actor_id,int(slot),BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "combined_direct_rejected_" + str(route.reason),
                        original_target_slot=int(submission.source_target_slot),
                        combined_skill_id=int(submission.skill_id),
                        combined_magic_id=int(submission.magic.magic_id),
                        combined_direct_route=route,
                    )
                )
                continue

            alive_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            target_resolution=resolve_combined_single_target(
                int(submission.source_target_slot),
                alive_slots=alive_slots,
                retarget_draws_0_9=action_rolls.retarget_draws_0_9,
            )
            target_slot=int(target_resolution.resolved_target_slot)
            if target_slot not in by_slot:
                raise ValueError(
                    "Combined target list resolved unoccupied slot"
                )
            defender=by_slot[target_slot]
            defender_id=str(defender.participant_id)
            magic_id=int(submission.magic.magic_id)
            recovery_effect=None
            status_change_effect=None
            status_recovery_effect=None
            att_reverse_effect=None
            result_name="combined_magic_applied"

            if magic_id == 21:
                if action_rolls.recovery_roll_90_110 is None:
                    raise ValueError(
                        "Combined Recovery 21 requires one RAND(90,110) witness"
                    )
                if action_rolls.status_roll_1_100 is not None:
                    raise ValueError(
                        "Combined Recovery 21 cannot consume status RNG"
                    )
                target_late=nocast_working[defender_id]
                riding_target=bool(
                    active_ride
                    and ride_runtime is not None
                    and str(ride_runtime.rider_id)==defender_id
                )
                recovery_effect=resolve_combined_recovery21_effect(
                    source_target_slot=int(submission.source_target_slot),
                    alive_slots=alive_slots,
                    current_hp=int(hp_by_slot[target_slot]),
                    max_hp=int(defender.max_hp),
                    target_vital=int(target_late.vital),
                    target_is_player=(defender.kind=="player"),
                    rolled_power=int(action_rolls.recovery_roll_90_110),
                    riding=riding_target,
                    resolved_target=target_resolution,
                )
                hp_by_slot[target_slot]=int(recovery_effect.hp_after)
                hp_by_id[defender_id]=int(recovery_effect.hp_after)
                result_name="combined_recovery"

            elif magic_id in {139,159,169,179,189}:
                if action_rolls.recovery_roll_90_110 is not None:
                    raise ValueError(
                        "Combined StatusChange cannot consume Recovery RNG"
                    )
                target_late=nocast_working[defender_id]
                if bool(target_late.unmodeled_status_active):
                    raise ValueError(
                        "Combined StatusChange with unmodeled active status "
                        "remains fail-closed"
                    )
                base_runtime=status_runtime[defender_id]
                base_active=any(
                    int(getattr(base_runtime.status,name))>0
                    for name in (
                        "poison","paralysis","sleep",
                        "stone","drunk","confusion",
                    )
                )
                modeled_late_active=target_late.has_any_status(
                    base_status_active=False
                )
                if modeled_late_active:
                    if action_rolls.status_roll_1_100 is not None:
                        raise ValueError(
                            "existing late status blocks Combined StatusAttackCheck RNG"
                        )
                    result_name="combined_status_change_blocked_existing_status"
                else:
                    if defender_id not in status_combat_profiles:
                        raise ValueError(
                            "Combined StatusChange target lacks explicit "
                            "status combat profile"
                        )
                    status_index=int(EXPECTED_IRIS_CP950_STATUS[magic_id])
                    status_name=BASE_STATUS_NAME_BY_INDEX[status_index]
                    status_profile=status_combat_profiles[defender_id]
                    status_change_effect=resolve_combined_status_change_effect(
                        magic_id=magic_id,
                        source_target_slot=int(submission.source_target_slot),
                        alive_slots=alive_slots,
                        current_status=base_runtime.status,
                        late_status_domain_clear=True,
                        roll_1_100=action_rolls.status_roll_1_100,
                        attacker_level=int(participant.level),
                        defender_level=int(defender.level),
                        pvp=False,
                        attacker_fixed_luck=int(
                            profiles[combined_actor_id].fixed_luck
                        ),
                        defender_vital=int(status_profile.vital),
                        defender_str=int(status_profile.strength),
                        defender_tough=int(status_profile.tough),
                        defender_dex=int(status_profile.dex),
                        defender_resistance=int(
                            status_profile.resistance_for(status_name)
                        ),
                        resolved_target=target_resolution,
                    )
                    poison_stat_sum=base_runtime.poison_stat_sum
                    if (
                        status_name == STATUS_POISON
                        and status_change_effect.status_after
                        != status_change_effect.status_before
                        and poison_stat_sum is None
                    ):
                        poison_stat_sum=(
                            int(status_profile.vital)
                            + int(status_profile.strength)
                            + int(status_profile.tough)
                            + int(status_profile.dex)
                        )
                    status_runtime[defender_id]=replace(
                        base_runtime,
                        status=status_change_effect.status_after,
                        poison_stat_sum=poison_stat_sum,
                    )
                    if status_change_effect.command_cleared:
                        combined_cleared_command_ids.add(defender_id)
                        command_by_slot[target_slot]=BattleCommand(
                            BATTLE_COM_NONE
                        )
                        guarding.discard(target_slot)
                    result_name=(
                        "combined_status_change_applied"
                        if status_change_effect.status_after
                        != status_change_effect.status_before
                        else "combined_status_change_blocked"
                    )

            elif magic_id == 61:
                if (
                    action_rolls.recovery_roll_90_110 is not None
                    or action_rolls.status_roll_1_100 is not None
                ):
                    raise ValueError(
                        "Combined StatusRecovery 61 owns no effect RNG"
                    )
                status_recovery_effect=resolve_combined_status_recovery61_effect(
                    source_target_slot=int(submission.source_target_slot),
                    alive_slots=alive_slots,
                    base_runtime=status_runtime[defender_id],
                    late_runtime=nocast_working[defender_id],
                    resolved_target=target_resolution,
                )
                status_runtime[defender_id]=status_recovery_effect.base_runtime
                nocast_working[defender_id]=status_recovery_effect.late_runtime
                result_name=(
                    "combined_status_recovery_cleared"
                    if status_recovery_effect.cleared_status is not None
                    else "combined_status_recovery_noop"
                )

            elif magic_id == 240:
                if (
                    action_rolls.recovery_roll_90_110 is not None
                    or action_rolls.status_roll_1_100 is not None
                ):
                    raise ValueError(
                        "Combined AttReverse 240 owns no effect RNG"
                    )
                was_reversed=bool(
                    combined_working.att_reverse_by_participant_id[defender_id]
                )
                current_profile=profiles[defender_id]
                att_reverse_effect=resolve_combined_att_reverse240_effect(
                    source_target_slot=int(submission.source_target_slot),
                    alive_slots=alive_slots,
                    battle_flags=1 if was_reversed else 0,
                    reverse_bit=1,
                    earth=int(current_profile.earth),
                    water=int(current_profile.water),
                    fire=int(current_profile.fire),
                    wind=int(current_profile.wind),
                    resolved_target=target_resolution,
                )
                next_overlay,attrs=combined_working.cast_att_reverse(
                    defender_id,current_profile
                )
                if (
                    int(attrs["earth"])!=int(att_reverse_effect.earth)
                    or int(attrs["water"])!=int(att_reverse_effect.water)
                    or int(attrs["fire"])!=int(att_reverse_effect.fire)
                    or int(attrs["wind"])!=int(att_reverse_effect.wind)
                ):
                    raise ValueError("Combined AttReverse state/effect drift")
                combined_working=next_overlay
                profiles[defender_id]=replace(
                    current_profile,
                    earth=int(attrs["earth"]),
                    water=int(attrs["water"]),
                    fire=int(attrs["fire"]),
                    wind=int(attrs["wind"]),
                )
                result_name="combined_att_reverse_toggled"
            else:
                raise ValueError(
                    "Combined selected magic escaped positive executable set"
                )

            events.append(
                OrdinaryRoundEvent(
                    combined_actor_id,int(slot),BATTLE_COM_ATTACK,
                    int(entry.action_value),result_name,
                    original_target_slot=int(submission.source_target_slot),
                    resolved_target_slot=target_slot,
                    retargeted=bool(target_resolution.retargeted),
                    target_hp_before=(
                        None if recovery_effect is None
                        else int(recovery_effect.hp_before)
                    ),
                    target_hp_after=(
                        None if recovery_effect is None
                        else int(recovery_effect.hp_after)
                    ),
                    combined_skill_id=int(submission.skill_id),
                    combined_magic_id=magic_id,
                    combined_direct_route=route,
                    combined_recovery_effect=recovery_effect,
                    combined_status_change_effect=status_change_effect,
                    combined_status_recovery_effect=status_recovery_effect,
                    combined_att_reverse_effect=att_reverse_effect,
                )
            )
            continue

        setmagicpet_actor_id=str(participant_id)
        if (
            setmagicpet_actor_id in setmagicpet_submissions
            and int(command.command1) == BATTLE_COM_ATTACK
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=setmagicpet_submissions[setmagicpet_actor_id]
            if int(command.command2) != int(submission.source_target_slot):
                raise ValueError(
                    "SetMagicPet ordering carrier target drift before execution"
                )
            if setmagicpet_working is None:
                raise ValueError(
                    "SetMagicPet working overlay unexpectedly absent"
                )
            alive_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            action_rolls=setmagicpet_rolls[setmagicpet_actor_id]
            target_list=resolve_nocast_multilist(
                int(submission.source_target_slot),
                alive_slots=alive_slots,
                retarget_draws_0_9=action_rolls.retarget_draws_0_9,
            )
            attempted_setmagicpet_actor_ids.add(setmagicpet_actor_id)
            for target_slot in target_list.slots:
                target_slot=int(target_slot)
                if target_slot not in by_slot:
                    raise ValueError(
                        "SetMagicPet target list resolved unoccupied slot"
                    )
                defender=by_slot[target_slot]
                defender_id=str(defender.participant_id)
                next_runtime,applied=apply_setmagicpet_option(
                    setmagicpet_working[defender_id],
                    submission.option,
                )
                setmagicpet_working[defender_id]=next_runtime
                events.append(
                    OrdinaryRoundEvent(
                        setmagicpet_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        (
                            "setmagicpet_applied"
                            if applied
                            else "setmagicpet_blocked_existing_buff"
                        ),
                        original_target_slot=int(
                            submission.source_target_slot
                        ),
                        resolved_target_slot=target_slot,
                        retargeted=bool(
                            target_list.slots
                            and int(target_list.slots[0])
                            != int(submission.source_target_slot)
                        ),
                        setmagicpet_skill_id=int(submission.skill_id),
                        setmagicpet_kind=submission.option.kind,
                        setmagicpet_applied=bool(applied),
                    )
                )
            continue

        refresh_actor_id=str(participant_id)
        if (
            refresh_actor_id in refresh_submissions
            and int(command.command1) == BATTLE_COM_ATTACK
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=refresh_submissions[refresh_actor_id]
            if int(command.command2) != int(submission.source_target_slot):
                raise ValueError(
                    "Refresh ordering carrier target drift before execution"
                )
            if nocast_working is None:
                raise ValueError("Refresh working overlay unexpectedly absent")
            alive_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            action_rolls=refresh_rolls[refresh_actor_id]
            target_list=resolve_nocast_multilist(
                int(submission.source_target_slot),
                alive_slots=alive_slots,
                retarget_draws_0_9=action_rolls.retarget_draws_0_9,
            )
            attempted_refresh_actor_ids.add(refresh_actor_id)
            actor_vector=refresh_status_vector(
                status_runtime[refresh_actor_id],
                nocast_working[refresh_actor_id],
                require_complete=False,
            )
            for target_slot in target_list.slots:
                target_slot=int(target_slot)
                if target_slot not in by_slot:
                    raise ValueError("Refresh target list resolved unoccupied slot")
                defender=by_slot[target_slot]
                defender_id=str(defender.participant_id)
                target_vector=refresh_status_vector(
                    status_runtime[defender_id],
                    nocast_working[defender_id],
                    require_complete=True,
                )
                resolution=resolve_refresh_recovery(
                    int(submission.status_index),
                    profile="iris",
                    actor_counters=actor_vector,
                    target_counters=(target_vector,),
                )
                cleared=resolution.cleared_statuses[0]
                next_base,next_late=apply_refresh_cleared_status(
                    status_runtime[defender_id],
                    nocast_working[defender_id],
                    cleared,
                )
                status_runtime[defender_id]=next_base
                nocast_working[defender_id]=next_late
                projected=refresh_status_vector(
                    next_base,
                    next_late,
                    require_complete=True,
                )
                if projected != resolution.target_counters[0]:
                    raise ValueError("Refresh modeled status mutation drifted from source recovery")
                events.append(
                    OrdinaryRoundEvent(
                        refresh_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "refresh_cleared" if cleared is not None else "refresh_noop",
                        original_target_slot=int(submission.source_target_slot),
                        resolved_target_slot=target_slot,
                        retargeted=bool(
                            target_list.slots
                            and int(target_list.slots[0])
                            != int(submission.source_target_slot)
                        ),
                        refresh_resolution=resolution,
                        refresh_skill_id=int(submission.skill_id),
                        refresh_status_index=int(submission.status_index),
                        refresh_cleared_status=(
                            None if cleared is None else int(cleared)
                        ),
                    )
                )
            continue

        weaken_actor_id=str(participant_id)
        if (
            weaken_actor_id in weaken_submissions
            and int(command.command1) == BATTLE_COM_ATTACK
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=weaken_submissions[weaken_actor_id]
            if int(command.command2) != int(submission.source_target_slot):
                raise ValueError(
                    "Weaken ordering carrier target drift before execution"
                )
            if nocast_working is None:
                raise ValueError("Weaken working overlay unexpectedly absent")

            alive_slots=tuple(
                other_slot
                for other_slot in sorted(by_slot)
                if (
                    other_slot not in exited_slots
                    and int(hp_by_slot.get(other_slot,0)) > 0
                )
            )
            action_rolls=weaken_rolls[weaken_actor_id]
            target_list=resolve_weaken_multilist(
                int(submission.source_target_slot),
                alive_slots=alive_slots,
                retarget_draws_0_9=action_rolls.retarget_draws_0_9,
            )
            attempted_weaken_actor_ids.add(weaken_actor_id)
            consumed_hit_roll_slots=set()
            for target_slot in target_list.slots:
                target_slot=int(target_slot)
                if target_slot not in by_slot:
                    raise ValueError(
                        "Weaken target list resolved unoccupied slot"
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
                application=resolve_weaken_target(
                    WeakenCheckInputs(
                        attacker_level=int(participant.level),
                        defender_level=int(defender.level),
                        pvp=False,
                        attacker_fixed_luck=int(
                            profiles[weaken_actor_id].fixed_luck
                        ),
                        defender_vital=int(target_runtime.vital),
                        defender_strength=int(target_runtime.strength),
                        defender_toughness=int(target_runtime.toughness),
                        defender_dexterity=int(target_runtime.dexterity),
                        defender_mod_weaken=int(target_runtime.mod_weaken),
                        defender_suit_resist=int(target_runtime.suit_resist),
                        any_existing_status=bool(any_status),
                        target_kind=str(defender.kind),
                    ),
                    submission.option,
                    roll_1_100=hit_roll,
                )
                if application.rng_consumed:
                    consumed_hit_roll_slots.add(target_slot)
                nocast_working[defender_id]=(
                    target_runtime.after_weaken_application(application)
                )
                result_name=(
                    "weaken_blocked_existing_status"
                    if application.probability_value is None
                    else (
                        "weaken_applied"
                        if application.counter_written is not None
                        else "weaken_missed"
                    )
                )
                events.append(
                    OrdinaryRoundEvent(
                        weaken_actor_id,
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
                        weaken_application=application,
                        weaken_skill_id=submission.skill_id,
                    )
                )
            supplied_hit_slots=set(action_rolls.hit_rolls_by_slot)
            if supplied_hit_slots != consumed_hit_roll_slots:
                missing=sorted(consumed_hit_roll_slots-supplied_hit_slots)
                extra=sorted(supplied_hit_slots-consumed_hit_roll_slots)
                raise ValueError(
                    "Weaken hit RNG slots mismatch; "
                    f"missing={missing}, extra={extra}"
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

        relife_actor_id=str(participant_id)
        if (
            relife_actor_id in enemy_relife_submissions
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            submission=enemy_relife_submissions[relife_actor_id]
            if (
                int(command.command1) != BATTLE_COM_ATTACK
                or int(command.command2)
                != int(submission.source_attack_target_slot)
            ):
                raise ValueError(
                    "enemy ReLife ordering carrier drift before execution"
                )

            original_relife_target=int(
                submission.source_attack_target_slot
            )
            adjusted_target=original_relife_target
            relife_retargeted=False
            adjusted_alive=(
                adjusted_target in by_slot
                and adjusted_target not in exited_slots
                and int(hp_by_slot.get(adjusted_target,0)) > 0
            )
            if (
                adjusted_alive
                and _slot_side(adjusted_target) == _slot_side(slot)
            ):
                raise ValueError(
                    "enemy ReLife fallback target crossed battle sides"
                )
            target_adjust_roll=enemy_relife_retarget_rolls[
                relife_actor_id
            ]
            if adjusted_alive:
                if target_adjust_roll is not None:
                    raise ValueError(
                        "enemy ReLife supplied unused TargetAdjust RNG"
                    )
            else:
                adjusted_target=_retarget_slot(
                    int(slot),
                    by_slot,
                    hp_by_slot,
                    target_adjust_roll,
                    excluded_slots=exited_slots,
                )
                relife_retargeted=True

            effect_rolls=enemy_relife_rolls[relife_actor_id]
            attempted_enemy_relife_actor_ids.add(relife_actor_id)
            if adjusted_target is None:
                if not effect_rolls.is_empty:
                    raise ValueError(
                        "enemy ReLife effect RNG supplied after no-target"
                    )
                if relife_actor_id in attack_rolls:
                    raise ValueError(
                        "enemy ReLife no-target supplied fallback attack RNG"
                    )
                events.append(
                    OrdinaryRoundEvent(
                        relife_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "enemy_relife_no_target",
                        original_target_slot=original_relife_target,
                        retargeted=relife_retargeted,
                    )
                )
                continue

            dead_entries={}
            for ally_slot in range(10,20):
                if ally_slot not in by_slot or ally_slot in exited_slots:
                    continue
                ally=by_slot[ally_slot]
                if ally.side != "enemy":
                    raise ValueError(
                        "enemy ReLife dead scan crossed battle sides"
                    )
                ally_id=str(ally.participant_id)
                is_revivable=ally_id in revivable_dead_ids
                dead_entries[ally_slot]=EnemyReLifeDeadEntry(
                    participant_id=ally_id,
                    slot=ally_slot,
                    hp=int(hp_by_slot.get(ally_slot,0)),
                    max_hp=int(ally.max_hp),
                    is_die=bool(is_revivable),
                    is_attacked=bool(is_revivable),
                    battle_mode_ready=True,
                    rescue_mode=False,
                    ultimate_exited=False,
                )

            relife_resolution=resolve_enemy_relife_effect(
                adjusted_attack_target_slot=int(adjusted_target),
                entries_by_slot=dead_entries,
                rolls=effect_rolls,
                caster_mode_ready=True,
            )
            if relife_resolution.success:
                if relife_actor_id in attack_rolls:
                    raise ValueError(
                        "successful enemy ReLife supplied fallback attack RNG"
                    )
                if relife_resolution.selected_slot is None:
                    raise ValueError(
                        "successful enemy ReLife lacks selected slot"
                    )
                revived_slot=int(relife_resolution.selected_slot)
                revived=by_slot[revived_slot]
                revived_id=str(revived.participant_id)
                hp_by_slot[revived_slot]=int(relife_resolution.hp_after)
                hp_by_id[revived_id]=int(relife_resolution.hp_after)
                revivable_dead_ids.discard(revived_id)
                profit_processed_death_ids.discard(revived_id)
                events.append(
                    OrdinaryRoundEvent(
                        relife_actor_id,
                        int(slot),
                        BATTLE_COM_ATTACK,
                        int(entry.action_value),
                        "enemy_relife",
                        original_target_slot=original_relife_target,
                        resolved_target_slot=revived_slot,
                        retargeted=relife_retargeted,
                        target_hp_before=int(relife_resolution.hp_before),
                        target_hp_after=int(relife_resolution.hp_after),
                        enemy_relife_resolution=relife_resolution,
                    )
                )
                continue

            if not relife_resolution.fallback_to_attack:
                raise ValueError(
                    "failed enemy ReLife did not request physical fallback"
                )
            events.append(
                OrdinaryRoundEvent(
                    relife_actor_id,
                    int(slot),
                    BATTLE_COM_ATTACK,
                    int(entry.action_value),
                    "enemy_relife_fallback",
                    original_target_slot=original_relife_target,
                    resolved_target_slot=int(adjusted_target),
                    retargeted=relife_retargeted,
                    enemy_relife_resolution=relife_resolution,
                )
            )
            rehp_fallback_active=True
            rehp_fallback_original_target=original_relife_target
            rehp_fallback_retargeted=relife_retargeted
            command=BattleCommand(
                BATTLE_COM_ATTACK,
                command2=int(adjusted_target),
                command3=command.command3,
                input_complete=command.input_complete,
            )
            command_by_slot[slot]=command

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
                "semantic fallback attack must not consume a second retarget RNG"
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
        modifyattack_submission=(modifyattack_submissions.get(str(participant_id))
            if str(participant_id) in modifyattack_active_command_ids else None)
        modifyattack_source_react_blocked=(modifyattack_submission is not None
            and base_damage_react_active(damage_react_state[str(defender_id)]))
        modifyattack_damage_before=None
        modifyattack_helper_draws=0
        mdfyattack_submission=(mdfyattack_submissions.get(str(participant_id))
            if str(participant_id) in mdfyattack_active_command_ids else None)
        mdfyattack_source_react_blocked=(mdfyattack_submission is not None
            and base_damage_react_active(damage_react_state[str(defender_id)]))
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

        lighttakeed_submission=None
        if (
            str(participant_id) in lighttakeed_active_command_ids
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            lighttakeed_submission=lighttakeed_submissions[str(participant_id)]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "Lighttakeed semantic action lost ATTACK ordering carrier"
                )

        two_battletimid_submission=None
        two_battletimid_draw=None
        if (
            str(participant_id) in two_battletimid_active_command_ids
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            two_battletimid_submission=two_battletimid_submissions[
                str(participant_id)
            ]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "2BattleTimid semantic action lost ATTACK ordering carrier"
                )
            if active_ride:
                raise ValueError(
                    "2BattleTimid with mounted ride runtime is outside R1"
                )
            if retargeted or int(target)!=int(
                two_battletimid_submission.source_target_slot
            ):
                raise ValueError(
                    "2BattleTimid substituted target is outside admitted R1"
                )
            if defender.kind=="pet":
                target_id=str(defender.participant_id)
                if target_id not in two_battletimid_default_slots:
                    raise ValueError(
                        "2BattleTimid pet target lacks authoritative default-pet slot"
                    )
                if target_id not in two_battletimid_noreturn:
                    raise ValueError(
                        "2BattleTimid pet target lacks authoritative NORETURN state"
                    )
            two_battletimid_draw=two_battletimid_rolls[str(participant_id)]

        battletimid_submission=None
        battletimid_draw=None
        if (
            str(participant_id) in battletimid_active_command_ids
            and not (
                current_status_tick is not None
                and current_status_tick.confusion_rewrote_command
            )
        ):
            battletimid_submission=battletimid_submissions[str(participant_id)]
            if int(command.command1) != BATTLE_COM_ATTACK:
                raise ValueError(
                    "BattleTimid semantic action lost ATTACK ordering carrier"
                )
            if base_damage_react_active(
                damage_react_state[str(defender_id)]
            ):
                raise ValueError(
                    "BattleTimid with active target DamageReact is outside R1"
                )
            if active_ride:
                raise ValueError(
                    "BattleTimid with mounted ride runtime is outside R1"
                )
            battletimid_draw=battletimid_rolls[str(participant_id)]
            if battletimid_draw is None:
                raise ValueError(
                    "BattleTimid execution requires one reduced rand draw"
                )
            attempted_battletimid_actor_ids.add(str(participant_id))

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
                lighttakeed_dodge_resolution=None
                if lighttakeed_submission is not None:
                    source_defender=by_slot[int(target)]
                    source_defender_id=str(source_defender.participant_id)
                    lighttakeed_dodge_resolution=resolve_lighttakeed_reaction(
                        profile=str(lighttakeed_submission.profile),
                        marker_kind=int(lighttakeed_submission.marker_kind),
                        attacker_state=damage_react_state[str(participant_id)],
                        defender_state=damage_react_state[source_defender_id],
                        raw_damage=0,
                        attacker_hp=int(hp_by_slot[slot]),
                        attacker_max_hp=int(participant.max_hp),
                        defender_hp=int(hp_by_slot[int(target)]),
                        defender_max_hp=int(source_defender.max_hp),
                        attacker_uses_throwing_weapon=counter_weapon_blocks_counter(
                            attacker_profile.counter_weapon_type
                        ),
                    )
                battletimid_resolution=(
                    None
                    if battletimid_submission is None
                    else battletimid_submission.post_damage(
                        draw=int(battletimid_draw),
                        damage=0,
                        target_is_pet=(defender.kind=="pet"),
                    )
                )
                two_battletimid_resolution=None
                if two_battletimid_submission is not None:
                    if two_battletimid_draw is not None:
                        raise ValueError(
                            "2BattleTimid dodge/zero-damage path owns no effect RNG"
                        )
                    target_id=str(defender.participant_id)
                    two_battletimid_resolution=(
                        two_battletimid_submission.post_damage(
                            draw=None,
                            damage=0,
                            target_is_pet=(defender.kind=="pet"),
                            source_target_slot=int(target),
                            default_pet_slot=two_battletimid_default_slots.get(
                                target_id,-1
                            ),
                            pet_noreturn=two_battletimid_noreturn.get(
                                target_id,False
                            ),
                        )
                    )
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
                        battletimid_resolution=battletimid_resolution,
                        battletimid_skill_id=(
                            None
                            if battletimid_submission is None
                            else int(battletimid_submission.skill_id)
                        ),
                        two_battletimid_resolution=two_battletimid_resolution,
                        two_battletimid_skill_id=(
                            None
                            if two_battletimid_submission is None
                            else int(two_battletimid_submission.skill_id)
                        ),
                        two_battletimid_profile=(
                            None
                            if two_battletimid_submission is None
                            else str(two_battletimid_submission.profile)
                        ),
                        modifyattack_skill_id=(None if modifyattack_submission is None else modifyattack_submission.skill_id),
                        lighttakeed_resolution=lighttakeed_dodge_resolution,
                        lighttakeed_skill_id=(
                            None
                            if lighttakeed_submission is None
                            else int(lighttakeed_submission.skill_id)
                        ),
                        lighttakeed_profile=(
                            None
                            if lighttakeed_submission is None
                            else str(lighttakeed_submission.profile)
                        ),
                    )
                )
                if (
                    modifyattack_submission is None
                    and mdfyattack_submission is None
                    and two_battletimid_submission is None
                    and not continuation_blocked_by_reaction
                ):
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
        if mdfyattack_submission is not None:
            damage = mdfyattack_attribute_damage(
                base_damage, mdfyattack_submission.option, defender_profile.elements,
                field_attr=field_attr, field_power=field_power,
            )
        else:
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

        if modifyattack_submission is not None and not modifyattack_source_react_blocked and int(damage)>0:
            original_modify_target=by_slot[int(target)]
            modifyattack_damage_before=int(damage)
            original_elements=profiles[str(original_modify_target.participant_id)].elements
            owns_rand=original_elements[modifyattack_submission.option.element_index]>0
            supplied_rand=modifyattack_rand[str(participant_id)]
            damage,modifyattack_helper_draws=modifyattack_helper_damage(
                int(damage),modifyattack_submission.option,original_elements,
                raw_rand=supplied_rand if owns_rand else None,
            )
            if modifyattack_helper_draws:
                consumed_modifyattack_rand_ids.add(str(participant_id))

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
            or battletimid_submission is not None
            or two_battletimid_submission is not None
            or lighttakeed_submission is not None
            or modifyattack_submission is not None
            or mdfyattack_submission is not None
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

        lighttakeed_resolution=None
        if lighttakeed_submission is not None:
            lighttakeed_resolution=resolve_lighttakeed_reaction(
                profile=str(lighttakeed_submission.profile),
                marker_kind=int(lighttakeed_submission.marker_kind),
                attacker_state=damage_react_state[str(participant_id)],
                defender_state=damage_react_state[reaction_defender_id],
                raw_damage=int(damage),
                attacker_hp=int(hp_by_slot[slot]),
                attacker_max_hp=int(participant.max_hp),
                defender_hp=int(hp_by_slot[reaction_target_slot]),
                defender_max_hp=int(reaction_defender.max_hp),
                attacker_uses_throwing_weapon=counter_weapon_blocks_counter(
                    attacker_profile.counter_weapon_type
                ),
            )
            reaction_resolution=lighttakeed_resolution.damage_react_resolution
            damage_react_state[str(participant_id)]=(
                lighttakeed_resolution.attacker_state_after
            )
            damage_react_state[reaction_defender_id]=(
                lighttakeed_resolution.defender_state_after
            )
        else:
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

        battletimid_resolution=None
        if battletimid_submission is not None:
            battletimid_resolution=battletimid_submission.post_damage(
                draw=int(battletimid_draw),
                damage=int(event_damage),
                target_is_pet=(reaction_defender.kind=="pet"),
            )
            if battletimid_resolution.forced_exit:
                if int(after) <= 0:
                    raise ValueError(
                        "BattleTimid lethal-damage forced-exit overlap is outside R1"
                    )
                exit_slot=int(reaction_target_slot)
                exit_id=str(reaction_defender_id)
                exited_slots.add(exit_slot)
                if exit_id not in exited_ids:
                    exited_ids.append(exit_id)

        two_battletimid_resolution=None
        if two_battletimid_submission is not None:
            if guardian_redirected:
                raise ValueError(
                    "2BattleTimid Guardian redirect composition is outside R1"
                )
            source_reaction_active=base_damage_react_active(
                reaction_resolution.state_before
            )
            owns_effect_draw=bool(
                int(event_damage)>0 and not source_reaction_active
            )
            if owns_effect_draw:
                if two_battletimid_draw is None:
                    raise ValueError(
                        "2BattleTimid positive undemoted event requires one draw"
                    )
                consumed_two_battletimid_draw_ids.add(str(participant_id))
            elif two_battletimid_draw is not None:
                raise ValueError(
                    "2BattleTimid reaction/zero-damage path owns no effect RNG"
                )
            target_id=str(reaction_defender_id)
            two_battletimid_resolution=two_battletimid_submission.post_damage(
                draw=(
                    int(two_battletimid_draw)
                    if owns_effect_draw
                    else None
                ),
                damage=int(event_damage),
                target_is_pet=(reaction_defender.kind=="pet"),
                source_target_slot=int(reaction_target_slot),
                default_pet_slot=two_battletimid_default_slots.get(
                    target_id,-1
                ),
                pet_noreturn=two_battletimid_noreturn.get(
                    target_id,False
                ),
                active_original_reaction=source_reaction_active,
            )
            if two_battletimid_resolution.pet_withdrawn:
                if int(after)<=0:
                    raise ValueError(
                        "2BattleTimid lethal recall/death overlap is outside R1"
                    )
                exit_slot=int(reaction_target_slot)
                exit_id=str(reaction_defender_id)
                exited_slots.add(exit_slot)
                if exit_id not in exited_ids:
                    exited_ids.append(exit_id)

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
                battletimid_resolution=battletimid_resolution,
                battletimid_skill_id=(
                    None
                    if battletimid_submission is None
                    else int(battletimid_submission.skill_id)
                ),
                two_battletimid_resolution=two_battletimid_resolution,
                two_battletimid_skill_id=(
                    None
                    if two_battletimid_submission is None
                    else int(two_battletimid_submission.skill_id)
                ),
                two_battletimid_profile=(
                    None
                    if two_battletimid_submission is None
                    else str(two_battletimid_submission.profile)
                ),
                lighttakeed_resolution=lighttakeed_resolution,
                lighttakeed_skill_id=(
                    None
                    if lighttakeed_submission is None
                    else int(lighttakeed_submission.skill_id)
                ),
                lighttakeed_profile=(
                    None
                    if lighttakeed_submission is None
                    else str(lighttakeed_submission.profile)
                ),
                modifyattack_skill_id=(None if modifyattack_submission is None else modifyattack_submission.skill_id),
                modifyattack_damage_before=modifyattack_damage_before,
                modifyattack_helper_draws=modifyattack_helper_draws,
                modifyattack_event_marked=(modifyattack_submission is not None
                    and not modifyattack_source_react_blocked and int(event_damage)>0),
                mdfyattack_skill_id=(None if mdfyattack_submission is None else mdfyattack_submission.skill_id),
                mdfyattack_element=(None if mdfyattack_submission is None else mdfyattack_submission.option.element),
                mdfyattack_attack_vector=(() if mdfyattack_submission is None else mdfyattack_submission.option.attack_vector),
                mdfyattack_event_marked=(mdfyattack_submission is not None
                    and not mdfyattack_source_react_blocked and int(event_damage)>0),
                ride_damage_split=ride_split,
                ride_hp_resolution=ride_hp_resolution,
                ride_pet_fell_rider_id=ride_pet_fell_rider_id,
                ultimate_damage_resolution=ultimate_damage_resolution,
                death_ultimate_resolution=death_ultimate_resolution,
                ultimate_kind=int(ultimate_kind),
            )
        )
        register_ultimate_exits(
            (events[-1],),
            boundary_kind=PROFIT_BOUNDARY_ORDINARY_PER_HIT,
        )
        # Generic BATTLE_S_AttackDamage forces continuation FALSE on
        # Guardian/DamageReact. Dedicated BATTLE_S_FallGround does not: its
        # iRet is controlled by AttackSeq result, the post-react defindex's
        # GUARD state and death. Preserve that difference here.
        if (
            modifyattack_submission is None
            and mdfyattack_submission is None
            and two_battletimid_submission is None
            and not (
                battletimid_resolution is not None
                and battletimid_resolution.forced_exit
            )
            and _battle_attack_continuation_allowed(
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
            )
        ):
            append_counter_chain(
                participant_id,
                slot,
                counter_target_slot,
            )

    for participant_id in sorted(
        combined_actor_ids-attempted_combined_actor_ids
    ):
        if combined_rolls[participant_id] != CombinedActionRolls():
            raise ValueError(
                "Combined RNG supplied for status/death-suppressed semantic action: "
                + participant_id
            )

    for participant_id in sorted(modifyattack_actor_ids-consumed_modifyattack_rand_ids):
        if modifyattack_rand[participant_id] is not None:
            raise ValueError("Modifyattack unowned helper RNG supplied: "+participant_id)

    for participant_id in sorted(
        battletimid_actor_ids-attempted_battletimid_actor_ids
    ):
        if battletimid_rolls[participant_id] is not None:
            raise ValueError(
                "BattleTimid RNG supplied for status/no-target-suppressed "
                "semantic action: " + participant_id
            )

    for participant_id in sorted(two_battletimid_actor_ids):
        draw=two_battletimid_rolls[participant_id]
        if (
            draw is not None
            and participant_id not in consumed_two_battletimid_draw_ids
        ):
            raise ValueError(
                "2BattleTimid unowned RNG supplied for suppressed/demoted "
                "semantic action: " + participant_id
            )

    for participant_id in sorted(
        enemy_relife_actor_ids-attempted_enemy_relife_actor_ids
    ):
        if (
            not enemy_relife_rolls[participant_id].is_empty
            or enemy_relife_retarget_rolls[participant_id] is not None
        ):
            raise ValueError(
                "enemy ReLife RNG supplied for status-suppressed semantic action: "
                + participant_id
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

    for participant_id in sorted(
        weaken_actor_ids-attempted_weaken_actor_ids
    ):
        if not weaken_rolls[participant_id].is_empty:
            raise ValueError(
                "Weaken RNG supplied for status-suppressed semantic action: "
                + participant_id
            )

    for participant_id in sorted(
        refresh_actor_ids-attempted_refresh_actor_ids
    ):
        if not refresh_rolls[participant_id].is_empty:
            raise ValueError(
                "Refresh RNG supplied for status-suppressed semantic action: "
                + participant_id
            )

    for participant_id in sorted(
        setmagicpet_actor_ids-attempted_setmagicpet_actor_ids
    ):
        if not setmagicpet_rolls[participant_id].is_empty:
            raise ValueError(
                "SetMagicPet RNG supplied for status-suppressed semantic action: "
                + participant_id
            )

    unused_wildviolent_roll_ids=sorted(
        set(wildviolent_rolls)-consumed_wildviolent_roll_ids
    )
    if unused_wildviolent_roll_ids:
        raise ValueError(
            "unused WildViolentAttack action RNG supplied for status/death-suppressed actors: "
            f"{unused_wildviolent_roll_ids}"
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
    if battlemodel_actions and (ultimate_marked_slots or any(
        e.target_hp_before is not None and e.target_hp_before > 0
        and e.target_hp_after == 0 for e in events
    )):
        raise ValueError("BattleModel nonlethal round excludes all death/ultimate exit/profit compositions")
    for pid in battlemodel_actor_ids-attempted_battlemodel_actor_ids:
        if battlemodel_actions[pid].draws:
            raise ValueError("unused BattleModel RNG supplied for status/death/incomplete-suppressed actor: "+pid)
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
        setmagicpet_overlay=(
            None
            if setmagicpet_working is None
            else SetMagicPetRoundOverlay(setmagicpet_working)
        ),
        combined_overlay=combined_working,
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
        battlemodel_cleared_command_ids=tuple(sorted(battlemodel_cleared_command_ids)),
        profit_boundaries=tuple(profit_boundaries),
        profit_processed_death_ids=tuple(
            sorted(profit_processed_death_ids)
        ),
    )
