#!/usr/bin/env python3
"""Stable common ride-pet physical damage-sharing seam."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RidePetRuntime:
    """Battle-local state for a non-entry pet currently selected as CHAR_RIDEPET."""

    rider_id: str
    pet_id: str
    hp: int
    max_hp: int
    defense_power: int
    mounted: bool = True
    petfall: bool = False

    def __post_init__(self) -> None:
        rider_id=str(self.rider_id)
        pet_id=str(self.pet_id)
        if not rider_id:
            raise ValueError("ride runtime requires rider_id")
        if not pet_id:
            raise ValueError("ride runtime requires pet_id")
        hp=int(self.hp)
        max_hp=int(self.max_hp)
        if max_hp < 0:
            raise ValueError("ride-pet max_hp cannot be negative")
        if not 0 <= hp <= max_hp:
            raise ValueError("ride-pet hp must be within max_hp")
        mounted=bool(self.mounted)
        petfall=bool(self.petfall)
        if mounted and petfall:
            raise ValueError("mounted ride pet cannot already carry PETFALL")
        object.__setattr__(self,"rider_id",rider_id)
        object.__setattr__(self,"pet_id",pet_id)
        object.__setattr__(self,"hp",hp)
        object.__setattr__(self,"max_hp",max_hp)
        object.__setattr__(self,"defense_power",int(self.defense_power))
        object.__setattr__(self,"mounted",mounted)
        object.__setattr__(self,"petfall",petfall)


@dataclass(frozen=True)
class RideDamageSplit:
    raw_damage: int
    rider_amount: int
    pet_amount: int
    shared: bool

    def __post_init__(self) -> None:
        for name in ("raw_damage","rider_amount","pet_amount"):
            value=int(getattr(self,name))
            if value < 0:
                raise ValueError(f"{name} cannot be negative")
            object.__setattr__(self,name,value)
        object.__setattr__(self,"shared",bool(self.shared))


@dataclass(frozen=True)
class RideHpResolution:
    rider_hp_before: int
    rider_hp_after: int
    pet_hp_before: int
    pet_hp_after: int
    unmounted: bool
    petfall: bool


def ride_pet_lookup_allowed(*, rider_kind: str) -> bool:
    """Common BATTLE_getRidePet resolves ordinary player characters only."""
    return str(rider_kind) == "player"


def ordinary_ride_damage_split(
    damage: int,
    *,
    rider_defense_power: int,
    pet_defense_power: int,
    pet_hp: int,
) -> RideDamageSplit:
    """Normal BATTLE_DamageSub split; both powers are clamped to at least 1."""
    damage=int(damage)
    pet_hp=int(pet_hp)
    if damage < 0:
        raise ValueError("damage cannot be negative")
    if damage == 0 or pet_hp <= 0:
        return RideDamageSplit(damage,damage,0,False)
    rider_power=max(int(rider_defense_power),1)
    pet_power=max(int(pet_defense_power),1)
    rider=(damage*pet_power)//(rider_power+pet_power)+1
    pet=damage-rider+1
    return RideDamageSplit(damage,rider,max(pet,0),True)


def immediate_reaction_ride_split(
    damage: int,
    *,
    rider_defense_power: int,
    pet_defense_power: int,
    pet_hp: int,
) -> RideDamageSplit:
    """ABSROB/REFLEC BATTLE_DamageSub split using raw work-defense powers."""
    damage=int(damage)
    pet_hp=int(pet_hp)
    if damage < 0:
        raise ValueError("damage cannot be negative")
    if damage == 0 or pet_hp <= 0:
        return RideDamageSplit(damage,damage,0,False)
    rider_power=int(rider_defense_power)
    pet_power=int(pet_defense_power)
    denominator=rider_power+pet_power
    if denominator <= 0:
        raise ValueError(
            "source immediate ride split requires positive defense-power sum"
        )
    rider=(damage*pet_power)//denominator+1
    pet=damage-rider+1
    return RideDamageSplit(damage,rider,max(pet,0),True)


def combo_ride_damage_split(
    damage: int,
    *,
    rider_defense_power: int,
    pet_defense_power: int,
    pet_hp: int,
) -> RideDamageSplit:
    """BATTLE_DamageSubCale split before Combo aggregate settlement."""
    damage=int(damage)
    pet_hp=int(pet_hp)
    if damage < 0:
        raise ValueError("damage cannot be negative")
    if damage == 0 or pet_hp <= 0:
        return RideDamageSplit(damage,damage,0,False)
    rider_power=max(int(rider_defense_power),1)
    pet_power=max(int(pet_defense_power),1)
    rider=(damage*pet_power)//(rider_power+pet_power)
    pet=damage-rider
    if damage > 0 and rider < 1:
        rider=1
    return RideDamageSplit(damage,rider,max(pet,0),True)


def apply_ride_damage(
    split: RideDamageSplit,
    *,
    rider_hp: int,
    rider_max_hp: int,
    pet_hp: int,
    pet_max_hp: int,
) -> RideHpResolution:
    """Apply physical damage and mirror ride-pet death unmount/PETFALL."""
    rider_hp=int(rider_hp); rider_max_hp=int(rider_max_hp)
    pet_hp=int(pet_hp); pet_max_hp=int(pet_max_hp)
    if not 0 <= rider_hp <= rider_max_hp:
        raise ValueError("rider HP must be within max HP")
    if not 0 <= pet_hp <= pet_max_hp:
        raise ValueError("ride-pet HP must be within max HP")
    rider_after=max(0,rider_hp-int(split.rider_amount))
    pet_after=max(0,pet_hp-int(split.pet_amount))
    # DamageSub's final defpet check unmounts whenever the selected ride pet
    # is at/below zero after application, even if it entered this call at zero.
    fell=bool(pet_after<=0)
    return RideHpResolution(
        rider_hp,rider_after,pet_hp,pet_after,fell,fell
    )


def apply_ride_heal(
    split: RideDamageSplit,
    *,
    rider_hp: int,
    rider_max_hp: int,
    pet_hp: int,
    pet_max_hp: int,
) -> RideHpResolution:
    """Apply ABSROB healing with separate rider/pet max-HP caps."""
    rider_hp=int(rider_hp); rider_max_hp=int(rider_max_hp)
    pet_hp=int(pet_hp); pet_max_hp=int(pet_max_hp)
    if not 0 <= rider_hp <= rider_max_hp:
        raise ValueError("rider HP must be within max HP")
    if not 0 <= pet_hp <= pet_max_hp:
        raise ValueError("ride-pet HP must be within max HP")
    return RideHpResolution(
        rider_hp,
        min(rider_max_hp,rider_hp+int(split.rider_amount)),
        pet_hp,
        min(pet_max_hp,pet_hp+int(split.pet_amount)),
        False,
        False,
    )
