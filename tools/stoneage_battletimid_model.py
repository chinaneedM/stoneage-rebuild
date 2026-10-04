"""Bounded PETSKILL_BattleTimid descendant reference model.

The model preserves only facts shared by the fixed later-source profiles.
Recovered25 population/data identity and ordered runtime admission are separate.
"""
from __future__ import annotations

from dataclasses import dataclass

CALLBACK_NAME = "PETSKILL_BattleTimid"
COMMAND_NAME = "BATTLE_COM_S_TIMID"
FEATURE_NAME = "_PETSKILL_TIMID"
SAFE_RUNTIME_TARGET_DOMAIN = "opposite_side_only"


class BattleTimidSourceDomain(ValueError):
    """Input is outside the bounded common descendant reference domain."""


def _int32(value: int) -> int:
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise BattleTimidSourceDomain("requires signed int32 witness")
    return value


def _trunc_ratio(value: int, numerator: int, denominator: int = 10) -> int:
    value = _int32(value)
    product = value * numerator
    result = product // denominator if product >= 0 else -((-product) // denominator)
    return _int32(result)


def _pack_low(before: int, low: int) -> int:
    before = _int32(before)
    low = _int32(low)
    unsigned = ((before & 0xFFFFFFFF) & 0xFFFF0000) | (low & 0xFFFF)
    return unsigned - 2**32 if unsigned >= 2**31 else unsigned


@dataclass(frozen=True)
class BattleTimidSetup:
    accepted: bool
    target_slot: int
    packed_com3: int
    attack_power: int
    defence_power: int
    quick: int
    rejected_player: bool
    command_name: str = COMMAND_NAME
    mode_name: str = "BATTLE_CHARMODE_C_OK"


def resolve_battletimid_setup(
    *,
    actor_is_player: bool,
    target_slot: int,
    skill_array: int,
    packed_com3_before: int,
    fixed_str: int,
    fixed_tough: int,
    fixed_dex: int,
) -> BattleTimidSetup:
    """Reproduce the callback's fixed 70%/40%/80% work-power writes."""
    for value in (
        target_slot, skill_array, packed_com3_before,
        fixed_str, fixed_tough, fixed_dex,
    ):
        _int32(value)
    if actor_is_player:
        return BattleTimidSetup(
            False,target_slot,packed_com3_before,
            0,0,0,True,
        )
    return BattleTimidSetup(
        True,
        target_slot,
        _pack_low(packed_com3_before,skill_array),
        _trunc_ratio(fixed_str,7),
        _trunc_ratio(fixed_tough,4),
        _trunc_ratio(fixed_dex,8),
        False,
    )


@dataclass(frozen=True)
class BattleTimidExitResolution:
    draw: int
    damage: int
    forced_exit: bool
    target_is_pet: bool
    pet_default_exit: bool
    owner_default_pet_cleared: bool
    player_battle_exit: bool
    party_discharged: bool
    rng_draws_consumed: int = 1


def resolve_battletimid_post_damage(
    *,
    draw: int,
    damage: int,
    target_is_pet: bool,
) -> BattleTimidExitResolution:
    """Model the BATTLE_S_AttackDamage TIMID branch after damage is known.

    Source consumes rand()%100 before testing damage, so every admitted call
    consumes one draw.  R1 supplies the reduced draw explicitly rather than
    pretending Python's RNG reproduces libc rand().
    """
    if type(draw) is not int or not 0 <= draw <= 99:
        raise BattleTimidSourceDomain("draw must be the observed rand()%100 value")
    damage = _int32(damage)
    forced = draw < 15 and damage > 1
    return BattleTimidExitResolution(
        draw=draw,
        damage=damage,
        forced_exit=forced,
        target_is_pet=bool(target_is_pet),
        pet_default_exit=forced and bool(target_is_pet),
        owner_default_pet_cleared=forced and bool(target_is_pet),
        player_battle_exit=forced and not bool(target_is_pet),
        party_discharged=forced and not bool(target_is_pet),
    )


def validate_common_runtime_domain(*, opposite_side: bool) -> None:
    """Keep the gavin/iris vs Bismarck same-side compile-profile split open."""
    if not opposite_side:
        raise BattleTimidSourceDomain(
            "same-side targeting differs across pinned compile profiles"
        )
