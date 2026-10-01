#!/usr/bin/env python3
"""Fixed-descendant PETSKILL_BattleTearDamage reference boundary."""

from __future__ import annotations

from dataclasses import dataclass
import re


CALLBACK_NAME="PETSKILL_BattleTearDamage"
COMMAND_NAME="BATTLE_COM_S_PETSKILLTEAR"


def c_atoi(text:str) -> int:
    """Small exact-enough model of the C atoi grammar used by this handler."""
    match=re.match(r"^[\t\n\v\f\r ]*([+-]?)(\d+)",str(text))
    if match is None:
        return 0
    value=int(match.group(2),10)
    return -value if match.group(1)=="-" else value


@dataclass(frozen=True)
class BattleTearSetup:
    attack_power:int
    defense_power:int
    skill_array:int


def battle_tear_callback_setup(
    *,
    fixed_strength:int,
    fixed_toughness:int,
    skill_array:int,
) -> BattleTearSetup:
    """Mirror the fixed callback's immediate work-power and LOW(COM3) writes."""
    # C converts the double products to int on CHAR_setWorkInt.
    return BattleTearSetup(
        attack_power=int(int(fixed_strength)*0.9),
        defense_power=int(int(fixed_toughness)*0.8),
        skill_array=int(skill_array),
    )


@dataclass(frozen=True)
class BattleTearAugmentation:
    option_percent:int
    missing_target_hp:int
    missing_ride_pet_hp:int
    wound_basis:int
    wound_damage:int
    damage_before:int
    damage_after:int
    applied:bool
    zeroed_physical_damage:bool


def resolve_battle_tear_pre_damage_sub(
    *,
    option_text:str,
    attack_seq_damage:int,
    attack_seq_result:str,
    damage_react_active:bool,
    same_side:bool,
    prevent_same_side:bool,
    target_hp:int,
    target_max_hp:int,
    target_kind:str,
    ride_pet_hp:int|None=None,
    ride_pet_max_hp:int|None=None,
) -> BattleTearAugmentation:
    """Mirror the TEAR switch immediately after BATTLE_AttackSeq.

    AttackSeq may already have calculated physical damage against a Guardian,
    but the fixed TEAR block reads missing HP from the original adjusted target
    (and its ride pet). DamageSub later also receives that original target.
    """
    damage=int(attack_seq_damage)
    hp=int(target_hp); max_hp=int(target_max_hp)
    if max_hp < 0 or not 0 <= hp <= max_hp:
        raise ValueError("target HP must be within max HP")

    ride_missing=0
    if ride_pet_hp is not None or ride_pet_max_hp is not None:
        if ride_pet_hp is None or ride_pet_max_hp is None:
            raise ValueError("ride-pet HP/max-HP must be supplied together")
        rhp=int(ride_pet_hp); rmax=int(ride_pet_max_hp)
        if rmax < 0 or not 0 <= rhp <= rmax:
            raise ValueError("ride-pet HP must be within max HP")
        if str(target_kind)=="player":
            ride_missing=rmax-rhp

    target_missing=max_hp-hp
    basis=target_missing+ride_missing
    percent=c_atoi(option_text)
    wound=int(basis*(float(percent)/100.0))

    blocked=(
        (bool(prevent_same_side) and bool(same_side))
        or str(attack_seq_result)=="dodge"
        or bool(damage_react_active)
    )
    if blocked:
        return BattleTearAugmentation(
            percent,target_missing,ride_missing,basis,wound,
            damage,damage,False,False,
        )

    if wound <= 0:
        return BattleTearAugmentation(
            percent,target_missing,ride_missing,basis,wound,
            damage,0,True,damage!=0,
        )
    return BattleTearAugmentation(
        percent,target_missing,ride_missing,basis,wound,
        damage,damage+wound,True,False,
    )
