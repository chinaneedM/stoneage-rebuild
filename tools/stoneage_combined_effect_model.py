"""Bounded positive PETSKILL_Combined target/effect state seams.

This module composes already accepted common battle models. It is deliberately
not the ordered round/coordinator integration: initiative, callback selection,
DirectUse MP gating and command scheduling remain separate layers.
"""
from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
    active_base_status_names,
)
from tools.stoneage_combined_status_magic_model import (
    EXPECTED_IRIS_CP950_STATUS,
)
from tools.stoneage_magic_effect_model import (
    att_reverse_cast_transition,
    battle_recovery_gain,
    common_magic_status_change_transition,
    recovery_rate,
)
from tools.stoneage_nocast_model import resolve_nocast_multilist
from tools.stoneage_nocast_runtime_state import NocastParticipantRuntime
from tools.stoneage_refresh_model import resolve_refresh_recovery
from tools.stoneage_refresh_runtime_state import (
    apply_refresh_cleared_status,
    refresh_status_vector,
)

RECOVERY_MAGIC_ID = 21
RECOVERY_POWER = 100
STATUS_RECOVERY_MAGIC_ID = 61
STATUS_CHANGE_MAGIC_IDS = (139,159,169,179,189)
ATT_REVERSE_MAGIC_ID = 240


class CombinedEffectDomain(ValueError):
    """Required state is absent or outside the bounded Combined effect seam."""


@dataclass(frozen=True)
class CombinedResolvedTarget:
    source_target_slot: int
    resolved_target_slot: int
    retarget_draws_consumed: int

    @property
    def retargeted(self) -> bool:
        return self.source_target_slot != self.resolved_target_slot


def resolve_combined_single_target(
    source_target_slot: int,
    *,
    alive_slots,
    retarget_draws_0_9=(),
) -> CombinedResolvedTarget:
    """Resolve the audited iris __ATTACK_MAGIC BATTLE_MultiList single path."""
    source_target_slot=int(source_target_slot)
    if not 0 <= source_target_slot < 20:
        raise CombinedEffectDomain("Combined positive runtime requires single slot target")
    result=resolve_nocast_multilist(
        source_target_slot,
        alive_slots=alive_slots,
        retarget_draws_0_9=retarget_draws_0_9,
    )
    if len(result.slots)!=1:
        raise CombinedEffectDomain("Combined single target did not resolve exactly one slot")
    return CombinedResolvedTarget(
        source_target_slot=source_target_slot,
        resolved_target_slot=int(result.slots[0]),
        retarget_draws_consumed=int(result.retarget_draws_consumed),
    )


@dataclass(frozen=True)
class CombinedRecoveryEffect:
    target: CombinedResolvedTarget
    hp_before: int
    hp_after: int
    rolled_power: int
    raw_gain: int
    effect_rng_draws_consumed: int = 1


def resolve_combined_recovery21_effect(
    *,
    source_target_slot: int,
    alive_slots,
    retarget_draws_0_9=(),
    current_hp: int,
    max_hp: int,
    target_vital: int,
    target_is_player: bool,
    rolled_power: int,
    riding: bool,
) -> CombinedRecoveryEffect:
    """Bounded non-riding ID-21 HP recovery after DirectUse accepted."""
    if type(riding) is not bool or riding:
        raise CombinedEffectDomain("Combined Recovery riding split remains outside R1 seam")
    current_hp=int(current_hp); max_hp=int(max_hp); rolled_power=int(rolled_power)
    if max_hp < 0 or current_hp < 0 or current_hp > max_hp:
        raise CombinedEffectDomain("invalid bounded HP witness")
    if not 90 <= rolled_power <= 110:
        raise CombinedEffectDomain("Recovery 21 RAND witness must lie in 90..110")
    target=resolve_combined_single_target(
        source_target_slot,alive_slots=alive_slots,
        retarget_draws_0_9=retarget_draws_0_9,
    )
    rate=recovery_rate(vital=int(target_vital),is_player=bool(target_is_player))
    gain=battle_recovery_gain(
        power=RECOVERY_POWER,percent=False,max_hp=max_hp,rate=rate,
        rolled_power=rolled_power,
    )
    return CombinedRecoveryEffect(
        target=target,hp_before=current_hp,
        hp_after=min(max_hp,current_hp+int(gain)),
        rolled_power=rolled_power,raw_gain=int(gain),
    )


@dataclass(frozen=True)
class CombinedStatusChangeEffect:
    magic_id: int
    target: CombinedResolvedTarget
    status_index: int
    turn: int
    success_offset: int
    status_before: BaseBattleStatusState
    status_after: BaseBattleStatusState
    status_rng_draws_consumed: int
    command_cleared: bool


def resolve_combined_status_change_effect(
    *,
    magic_id: int,
    source_target_slot: int,
    alive_slots,
    retarget_draws_0_9=(),
    current_status: BaseBattleStatusState,
    late_status_domain_clear: bool,
    roll_1_100: int | None,
    attacker_level: int,
    defender_level: int,
    pvp: bool,
    attacker_fixed_luck: int,
    defender_vital: int,
    defender_str: int,
    defender_tough: int,
    defender_dex: int,
    defender_resistance: int,
) -> CombinedStatusChangeEffect:
    """Conditional iris-CP950 StatusChange -> common StatusAttackCheck seam."""
    magic_id=int(magic_id)
    if magic_id not in STATUS_CHANGE_MAGIC_IDS:
        raise CombinedEffectDomain("magic is not a positive Combined StatusChange choice")
    if type(late_status_domain_clear) is not bool or not late_status_domain_clear:
        raise CombinedEffectDomain("late/unmodeled status interaction requires ordered audit")
    if not isinstance(current_status,BaseBattleStatusState):
        raise TypeError("current_status must be BaseBattleStatusState")
    active=active_base_status_names(current_status)
    if active and roll_1_100 is not None:
        raise CombinedEffectDomain("existing status blocks StatusAttackCheck RNG")
    if not active and roll_1_100 is None:
        raise CombinedEffectDomain("eligible StatusAttackCheck requires explicit RNG")
    target=resolve_combined_single_target(
        source_target_slot,alive_slots=alive_slots,
        retarget_draws_0_9=retarget_draws_0_9,
    )
    status_index=int(EXPECTED_IRIS_CP950_STATUS[magic_id])
    transition=common_magic_status_change_transition(
        current_status=current_status,status_index=status_index,turn=5,
        success_offset=15,attacker_level=attacker_level,
        defender_level=defender_level,pvp=pvp,
        attacker_fixed_luck=attacker_fixed_luck,defender_vital=defender_vital,
        defender_str=defender_str,defender_tough=defender_tough,
        defender_dex=defender_dex,defender_resistance=defender_resistance,
        roll_1_100=roll_1_100,
    )
    return CombinedStatusChangeEffect(
        magic_id=magic_id,target=target,status_index=status_index,turn=5,
        success_offset=15,status_before=current_status,
        status_after=transition["status"],
        status_rng_draws_consumed=int(transition["check"].rng_consumed),
        command_cleared=bool(transition["command_cleared"]),
    )


@dataclass(frozen=True)
class CombinedStatusRecoveryEffect:
    target: CombinedResolvedTarget
    cleared_status: int | None
    base_runtime: BaseBattleStatusRuntime
    late_runtime: NocastParticipantRuntime


def resolve_combined_status_recovery61_effect(
    *,
    source_target_slot: int,
    alive_slots,
    retarget_draws_0_9=(),
    base_runtime: BaseBattleStatusRuntime,
    late_runtime: NocastParticipantRuntime,
) -> CombinedStatusRecoveryEffect:
    """Conditional iris-CP950 wildcard: clear one highest modeled active status."""
    target=resolve_combined_single_target(
        source_target_slot,alive_slots=alive_slots,
        retarget_draws_0_9=retarget_draws_0_9,
    )
    vector=refresh_status_vector(base_runtime,late_runtime,require_complete=True)
    result=resolve_refresh_recovery(
        0,profile="iris",actor_counters=(0,)*44,target_counters=(vector,),
    )
    cleared=result.cleared_statuses[0]
    base_after,late_after=apply_refresh_cleared_status(
        base_runtime,late_runtime,cleared
    )
    return CombinedStatusRecoveryEffect(
        target=target,cleared_status=cleared,
        base_runtime=base_after,late_runtime=late_after,
    )


@dataclass(frozen=True)
class CombinedAttReverseEffect:
    target: CombinedResolvedTarget
    battle_flags: int
    earth: int
    water: int
    fire: int
    wind: int


def resolve_combined_att_reverse240_effect(
    *,
    source_target_slot: int,
    alive_slots,
    retarget_draws_0_9=(),
    battle_flags: int,
    reverse_bit: int,
    earth: int,
    water: int,
    fire: int,
    wind: int,
) -> CombinedAttReverseEffect:
    """Toggle persistent reverse flag and apply the immediate attribute swap."""
    target=resolve_combined_single_target(
        source_target_slot,alive_slots=alive_slots,
        retarget_draws_0_9=retarget_draws_0_9,
    )
    out=att_reverse_cast_transition(
        battle_flags=battle_flags,reverse_bit=reverse_bit,
        earth=earth,water=water,fire=fire,wind=wind,
    )
    attrs=out["attributes"]
    return CombinedAttReverseEffect(
        target=target,battle_flags=int(out["battle_flags"]),
        earth=int(attrs["earth"]),water=int(attrs["water"]),
        fire=int(attrs["fire"]),wind=int(attrs["wind"]),
    )
