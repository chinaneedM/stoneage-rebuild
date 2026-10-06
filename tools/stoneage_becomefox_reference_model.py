"""Bounded BecomeFox post-attack and FOXROUND semantic reference.

This module models only behavior already closed by the exact recovered25
source/data reference plus pinned descendant source structure. It deliberately
keeps source-profile divergences explicit and does not infer original executable
identity.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

FOX_IMAGE = 101749
NO_FOX_ROUND = -1

BLOCKING_RESULTS = frozenset({"MISS", "DODGE", "ALLGUARD"})


@dataclass(frozen=True)
class FoxState:
    base_image: int
    base_base_image: int
    attack_power: int
    defence_power: int
    quick: int
    fix_str: int
    fix_tough: int
    fix_dex: int
    fox_round: int = NO_FOX_ROUND
    ride_pet: int = -1
    petfall: int = 0


@dataclass(frozen=True)
class TransformDecision:
    target_check_consumed: bool
    draw_consumed: bool
    transformed: bool
    magic_effect: bool
    ride_image_changed: bool
    state: FoxState


@dataclass(frozen=True)
class RoundRecovery:
    recovered: bool
    notify_owner_slot: int | None
    state: FoxState


@dataclass(frozen=True)
class PetInReset:
    reset_applied: bool
    no_return_blocked_after_reset: bool
    ordinary_int_marker_after: int
    work_int_marker_after: int
    state: FoxState


def _c_trunc_08(value: int) -> int:
    # All bounded recovered values are nonnegative. int(float) matches C's
    # truncation toward zero for these inputs.
    return int(int(value) * 0.8)


def resolve_postattack_transform(
    state: FoxState,
    *,
    command_is_becomefox: bool,
    attack_result: str,
    target_alive: bool,
    draw_mod_100: int | None,
    target_is_player: bool,
    target_petflag: int,
    attacker_pig_marker: int = -1,
    arrange_guard_active: bool = True,
    pig_guard_active: bool = True,
    current_turn: int,
) -> TransformDecision:
    """Resolve the exact short-circuit order of the descendant post-hit block.

    The source owns exactly one rand()%100 draw only after command/result/alive
    gates pass. Type/PETFLG/pig eligibility is checked *after* that draw.
    """
    if not command_is_becomefox:
        return TransformDecision(False, False, False, False, False, state)
    if attack_result in BLOCKING_RESULTS:
        return TransformDecision(False, False, False, False, False, state)
    if arrange_guard_active and attack_result == "ARRANGE":
        return TransformDecision(False, False, False, False, False, state)

    # BATTLE_TargetCheck is evaluated before the RNG.
    target_checked = True
    if not target_alive:
        return TransformDecision(target_checked, False, False, False, False, state)

    if draw_mod_100 is None or not 0 <= int(draw_mod_100) <= 99:
        raise ValueError("draw_mod_100 must be supplied in [0,99] once RNG is reached")
    draw = int(draw_mod_100)
    if draw >= 31:
        return TransformDecision(target_checked, True, False, False, False, state)

    # These eligibility checks occur after the draw and therefore still consume
    # it on an ineligible target.
    if target_is_player:
        return TransformDecision(target_checked, True, False, False, False, state)
    if int(target_petflag) == 0:
        return TransformDecision(target_checked, True, False, False, False, state)
    if pig_guard_active and int(attacker_pig_marker) != -1:
        return TransformDecision(target_checked, True, False, False, False, state)

    ride_changed = state.ride_pet != -1
    next_state = replace(
        state,
        fox_round=int(current_turn),
        base_image=FOX_IMAGE,
        ride_pet=-1 if ride_changed else state.ride_pet,
        petfall=1 if ride_changed else state.petfall,
    )
    return TransformDecision(
        target_checked,
        True,
        True,
        True,
        ride_changed,
        next_state,
    )


def apply_active_fox_action_powers(state: FoxState) -> FoxState:
    """Apply the source's pre-action power rewrite while FOXROUND is active."""
    if state.fox_round == NO_FOX_ROUND:
        return state
    return replace(
        state,
        attack_power=_c_trunc_08(state.fix_str),
        defence_power=_c_trunc_08(state.fix_tough),
        quick=_c_trunc_08(state.fix_dex),
    )


def resolve_round_recovery(
    state: FoxState,
    *,
    current_turn: int,
    battle_slot: int,
) -> RoundRecovery:
    """Apply the pinned source's >2 turn recovery boundary."""
    if state.fox_round == NO_FOX_ROUND:
        return RoundRecovery(False, None, state)

    # The source first re-enforces the fox image whenever the marker is active.
    working = replace(state, base_image=FOX_IMAGE)
    if int(current_turn) - int(state.fox_round) <= 2:
        return RoundRecovery(False, None, working)

    restored = replace(
        working,
        base_image=working.base_base_image,
        attack_power=working.fix_str,
        defence_power=working.fix_tough,
        quick=working.fix_dex,
        fox_round=NO_FOX_ROUND,
    )
    return RoundRecovery(True, int(battle_slot) - 5, restored)


def resolve_battle_exit(state: FoxState) -> FoxState:
    """Exit restores image/marker only; it does not itself restore powers."""
    if state.base_image != FOX_IMAGE and state.fox_round == NO_FOX_ROUND:
        return state
    return replace(
        state,
        base_image=state.base_base_image,
        fox_round=NO_FOX_ROUND,
    )


def resolve_petin_reset(
    state: FoxState,
    *,
    accessor_profile: str,
    ordinary_int_marker: int,
    work_int_marker: int,
    no_return: bool,
) -> PetInReset:
    """Preserve the gavin/iris vs Bismarck FOXROUND accessor split.

    All pinned profiles execute this reset before checking NORETURN. The reset
    restores image, attack and quick but not defence.
    """
    if accessor_profile not in {"ordinary_int", "work_int"}:
        raise ValueError("unknown accessor_profile")
    marker = (
        int(ordinary_int_marker)
        if accessor_profile == "ordinary_int"
        else int(work_int_marker)
    )
    should_reset = marker != NO_FOX_ROUND or state.base_image == FOX_IMAGE
    oi = int(ordinary_int_marker)
    wi = int(work_int_marker)
    working = state
    if should_reset:
        working = replace(
            state,
            base_image=state.base_base_image,
            attack_power=state.fix_str,
            quick=state.fix_dex,
        )
        if accessor_profile == "ordinary_int":
            oi = NO_FOX_ROUND
        else:
            wi = NO_FOX_ROUND
    return PetInReset(
        reset_applied=should_reset,
        no_return_blocked_after_reset=bool(no_return),
        ordinary_int_marker_after=oi,
        work_int_marker_after=wi,
        state=working,
    )


def dexcalc_source_order_fact(profile: str) -> dict:
    """Record the audited control-flow fact, not a synthetic initiative rule."""
    if profile not in {"gavin", "iris", "bismarck"}:
        raise ValueError("unknown profile")
    return {
        "fox_pre_switch_assignment": "(quick+20)*0.8",
        "ordinary_allowed_commands_fall_to_default": True,
        "default_overwrites_fox_dex": True,
        "default_rand_upper_fraction": 0.1 if profile == "bismarck" else 0.3,
        "effective_extra_fox_20pct_initiative_penalty_accepted": False,
    }
