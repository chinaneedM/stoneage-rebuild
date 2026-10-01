#!/usr/bin/env python3
"""Exact-order enemy AttackMagic action composer for the recovered25 path.

This composes only already-closed layers:
- Recovered25EnemyAttackMagicPlan (target membership/order + magic parameters)
- fixed _FIX_MAGICDAMAGE arithmetic
- explicit target magic state and explicit RNG

It deliberately does not register command 2002 in the ordinary battle-round
resolver. Profit, player death flags and round-event integration remain a
separate adapter seam.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_attack_magic_damage_model import (
    AttackMagicHpResult,
    ElementAttrs,
    FixedMagicHitDamage,
    MagicExpState,
    apply_attack_magic_hp,
    attack_magic_ride_ratio,
    attacker_magic_proficiency,
    defense_magic_training,
    effective_magic_resistance,
    magic_dodges,
    resolve_fixed_magic_hit_damage,
    true_magic_success,
)
from tools.stoneage_recovered25_attack_magic_runtime import (
    Recovered25EnemyAttackMagicPlan,
)


def _pure_attrs(attrs: ElementAttrs) -> ElementAttrs:
    earth=max(0,int(attrs.earth))
    water=max(0,int(attrs.water))
    fire=max(0,int(attrs.fire))
    wind=max(0,int(attrs.wind))
    return ElementAttrs(
        earth,
        water,
        fire,
        wind,
        max(0,100-earth-water-fire-wind),
    )


def source_battle_attrs(
    actor_attrs: ElementAttrs,
    *,
    ride_pet_attrs: ElementAttrs | None = None,
) -> ElementAttrs:
    """Reconstruct battle_magic.c BATTLE_GetAttr.

    With a resolved ride pet, each fixed elemental attribute is integer-averaged
    between rider and pet before clamping. The no-element component is then
    recomputed as max(0, 100 - four-element sum).
    """
    actor=_pure_attrs(actor_attrs)
    if ride_pet_attrs is None:
        return actor
    pet=_pure_attrs(ride_pet_attrs)
    earth=(int(actor.earth)+int(pet.earth))//2
    water=(int(actor.water)+int(pet.water))//2
    fire=(int(actor.fire)+int(pet.fire))//2
    wind=(int(actor.wind)+int(pet.wind))//2
    return ElementAttrs(
        earth,
        water,
        fire,
        wind,
        max(0,100-earth-water-fire-wind),
    )


@dataclass(frozen=True)
class AttackMagicRideTargetState:
    pet_id: str
    hp: int
    max_hp: int
    pure_attrs: ElementAttrs
    mounted: bool = True
    petfall: bool = False

    def __post_init__(self) -> None:
        pet_id=str(self.pet_id)
        if not pet_id:
            raise ValueError("AttackMagic ride state requires pet_id")
        hp=int(self.hp)
        max_hp=int(self.max_hp)
        if max_hp < 0 or not 0 <= hp <= max_hp:
            raise ValueError("AttackMagic ride-pet hp must be within max_hp")
        mounted=bool(self.mounted)
        petfall=bool(self.petfall)
        if mounted and petfall:
            raise ValueError("mounted AttackMagic ride pet cannot carry PETFALL")
        object.__setattr__(self,"pet_id",pet_id)
        object.__setattr__(self,"hp",hp)
        object.__setattr__(self,"max_hp",max_hp)
        object.__setattr__(self,"pure_attrs",_pure_attrs(self.pure_attrs))
        object.__setattr__(self,"mounted",mounted)
        object.__setattr__(self,"petfall",petfall)


@dataclass(frozen=True)
class EnemyAttackMagicCasterState:
    participant_id: str
    level: int
    pure_attrs: ElementAttrs

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        if not participant_id:
            raise ValueError("AttackMagic caster requires participant_id")
        level=int(self.level)
        if level < 0:
            raise ValueError("AttackMagic caster level cannot be negative")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"level",level)
        object.__setattr__(self,"pure_attrs",_pure_attrs(self.pure_attrs))


@dataclass(frozen=True)
class AttackMagicDefenderState:
    participant_id: str
    kind: str
    level: int
    hp: int
    max_hp: int
    pure_attrs: ElementAttrs
    resistance: MagicExpState
    luck: int = 0
    equipment_resistance: int = 0
    equipment_quimagic: int = 0
    magic_defense_percent: int | None = None
    sleep_turns: int = 0
    ride: AttackMagicRideTargetState | None = None

    def __post_init__(self) -> None:
        participant_id=str(self.participant_id)
        kind=str(self.kind)
        if not participant_id:
            raise ValueError("AttackMagic defender requires participant_id")
        if kind not in {"player","pet","enemy","other"}:
            raise ValueError("unknown AttackMagic defender kind")
        level=int(self.level)
        hp=int(self.hp)
        max_hp=int(self.max_hp)
        if level < 0:
            raise ValueError("AttackMagic defender level cannot be negative")
        if max_hp < 0 or not 0 <= hp <= max_hp:
            raise ValueError("AttackMagic defender hp must be within max_hp")
        if self.ride is not None and kind != "player":
            raise ValueError("recovered ride-pet AttackMagic target must be player")
        object.__setattr__(self,"participant_id",participant_id)
        object.__setattr__(self,"kind",kind)
        object.__setattr__(self,"level",level)
        object.__setattr__(self,"hp",hp)
        object.__setattr__(self,"max_hp",max_hp)
        object.__setattr__(self,"pure_attrs",_pure_attrs(self.pure_attrs))
        object.__setattr__(self,"luck",int(self.luck))
        object.__setattr__(
            self,"equipment_resistance",int(self.equipment_resistance)
        )
        object.__setattr__(
            self,"equipment_quimagic",int(self.equipment_quimagic)
        )
        if self.magic_defense_percent is not None:
            object.__setattr__(
                self,
                "magic_defense_percent",
                int(self.magic_defense_percent),
            )
        object.__setattr__(self,"sleep_turns",max(0,int(self.sleep_turns)))


@dataclass(frozen=True)
class AttackMagicTargetRolls:
    dodge_roll_1_100: int
    damage_random_0_19: int | None = None

    def __post_init__(self) -> None:
        dodge=int(self.dodge_roll_1_100)
        if not 1 <= dodge <= 100:
            raise ValueError("AttackMagic dodge roll must be 1..100")
        object.__setattr__(self,"dodge_roll_1_100",dodge)
        if self.damage_random_0_19 is not None:
            damage=int(self.damage_random_0_19)
            if not 0 <= damage <= 19:
                raise ValueError("AttackMagic damage random must be 0..19")
            object.__setattr__(self,"damage_random_0_19",damage)


@dataclass(frozen=True)
class EnemyAttackMagicActionRolls:
    true_magic_roll_0_99: int
    target_rolls_by_slot: Mapping[int, AttackMagicTargetRolls]

    def __post_init__(self) -> None:
        cast=int(self.true_magic_roll_0_99)
        if not 0 <= cast <= 99:
            raise ValueError("AttackMagic cast roll must be 0..99")
        normalized={}
        for slot,value in self.target_rolls_by_slot.items():
            slot=int(slot)
            if not 0 <= slot < 20:
                raise ValueError("AttackMagic target-roll slot must be 0..19")
            if not isinstance(value,AttackMagicTargetRolls):
                raise TypeError("AttackMagic target rolls have wrong type")
            normalized[slot]=value
        object.__setattr__(self,"true_magic_roll_0_99",cast)
        object.__setattr__(
            self,"target_rolls_by_slot",MappingProxyType(normalized)
        )


@dataclass(frozen=True)
class AttackMagicTargetResolution:
    slot: int
    participant_id: str
    dodged: bool
    true_magic_success: bool
    raw_magic_damage: int
    reported_rider_damage: int
    ride_pet_damage: int
    hp_before: int
    hp_after: int
    ride_pet_hp_before: int | None
    ride_pet_hp_after: int | None
    ride_pet_unmounted: bool
    sleep_cleared: bool
    resistance_before: MagicExpState
    resistance_after: MagicExpState
    damage_detail: FixedMagicHitDamage | None = None


@dataclass(frozen=True)
class EnemyAttackMagicActionResolution:
    plan: Recovered25EnemyAttackMagicPlan
    attacker_proficiency: int
    true_magic_success: bool
    target_order: tuple[int, ...]
    targets: tuple[AttackMagicTargetResolution, ...]
    defenders_after: Mapping[int, AttackMagicDefenderState]
    attacker_training_applied: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "defenders_after",
            MappingProxyType(
                {int(slot):state for slot,state in self.defenders_after.items()}
            ),
        )


def _target_battle_attrs(state: AttackMagicDefenderState) -> ElementAttrs:
    ride=state.ride
    return source_battle_attrs(
        state.pure_attrs,
        ride_pet_attrs=(
            ride.pure_attrs
            if ride is not None and ride.mounted
            else None
        ),
    )


def resolve_enemy_attack_magic_action(
    *,
    plan: Recovered25EnemyAttackMagicPlan,
    caster: EnemyAttackMagicCasterState,
    defenders_by_slot: Mapping[int, AttackMagicDefenderState],
    rolls: EnemyAttackMagicActionRolls,
    field_element: int | None = None,
    field_power: int = 0,
) -> EnemyAttackMagicActionResolution:
    """Compose an exact-order enemy AttackMagic action.

    RNG consumption is source-shaped:
    1) one true-magic roll per cast;
    2) one dodge roll per sorted target;
    3) one damage random only for a non-dodged target.
    """
    if not isinstance(plan,Recovered25EnemyAttackMagicPlan):
        raise TypeError("AttackMagic action requires recovered25 runtime plan")
    if not plan.source_sort_portable or plan.source_target_order is None:
        raise ValueError(
            "AttackMagic action requires exact portable historical target order"
        )
    target_order=tuple(int(slot) for slot in plan.source_target_order)
    if tuple(plan.target_membership) and set(target_order) != set(
        int(slot) for slot in plan.target_membership
    ):
        raise ValueError("AttackMagic plan order/membership drift")
    if field_element is not None and int(field_element) not in range(4):
        raise ValueError("AttackMagic field element must be 0..3 or null")

    defenders={int(slot):state for slot,state in defenders_by_slot.items()}
    for slot in target_order:
        if slot not in defenders:
            raise KeyError(f"missing AttackMagic defender state for slot {slot}")
        if slot not in rolls.target_rolls_by_slot:
            raise KeyError(f"missing AttackMagic target rolls for slot {slot}")

    proficiency,training_actor=attacker_magic_proficiency(
        actor_kind="enemy",
        level=caster.level,
        stored_proficiency=0,
    )
    if training_actor:
        raise ValueError("enemy AttackMagic caster unexpectedly trainable")
    cast_success=true_magic_success(
        proficiency=proficiency,
        roll_0_99=rolls.true_magic_roll_0_99,
    )
    attacker_attrs=source_battle_attrs(caster.pure_attrs)

    results=[]
    working=dict(defenders)
    for slot in target_order:
        state=working[slot]
        target_rolls=rolls.target_rolls_by_slot[slot]
        dodge=magic_dodges(
            actor_kind=state.kind,
            level=state.level,
            roll_1_100=target_rolls.dodge_roll_1_100,
            luck=state.luck,
            base_resistance=state.resistance.level,
            equipment_quimagic=state.equipment_quimagic,
        )
        ride_before=(
            int(state.ride.hp)
            if state.ride is not None
            else None
        )
        if dodge:
            results.append(
                AttackMagicTargetResolution(
                    slot=slot,
                    participant_id=state.participant_id,
                    dodged=True,
                    true_magic_success=cast_success,
                    raw_magic_damage=0,
                    reported_rider_damage=0,
                    ride_pet_damage=0,
                    hp_before=state.hp,
                    hp_after=state.hp,
                    ride_pet_hp_before=ride_before,
                    ride_pet_hp_after=ride_before,
                    ride_pet_unmounted=False,
                    sleep_cleared=False,
                    resistance_before=state.resistance,
                    resistance_after=state.resistance,
                    damage_detail=None,
                )
            )
            continue

        if target_rolls.damage_random_0_19 is None:
            raise KeyError(
                f"non-dodged AttackMagic target {slot} requires damage random"
            )

        effective_resistance=effective_magic_resistance(
            actor_kind=state.kind,
            level=state.level,
            stored_resistance=state.resistance.level,
            equipment_resistance=state.equipment_resistance,
            magic_defense_percent=state.magic_defense_percent,
        )
        detail=resolve_fixed_magic_hit_damage(
            power=plan.power,
            magic_level=plan.magic_level,
            element=plan.element,
            attacker_proficiency=proficiency,
            defender_resistance=effective_resistance,
            attacker_attrs=attacker_attrs,
            defender_attrs=_target_battle_attrs(state),
            field_element=field_element,
            field_power=int(field_power),
            damage_random_0_19=target_rolls.damage_random_0_19,
            true_magic=cast_success,
        )
        raw_damage=int(detail.final_damage)
        resistance_after=(
            defense_magic_training(
                state.resistance,
                magic_level=plan.magic_level,
                damage=raw_damage,
            )
            if state.kind in {"player","pet"}
            else state.resistance
        )

        ride=state.ride
        active_ride=(
            ride is not None
            and ride.mounted
            and int(ride.hp) > 0
        )
        if active_ride:
            ratio=attack_magic_ride_ratio(
                element=plan.element,
                rider_attrs=state.pure_attrs,
                pet_attrs=ride.pure_attrs,
            )
            hp_result=apply_attack_magic_hp(
                damage=raw_damage,
                rider_hp=state.hp,
                ride_pet_hp=ride.hp,
                ride_ratio=ratio,
            )
            ride_after=replace(
                ride,
                hp=int(hp_result.pet_hp),
                mounted=(
                    False if hp_result.unmounted else ride.mounted
                ),
                petfall=bool(ride.petfall or hp_result.unmounted),
            )
        else:
            hp_result=apply_attack_magic_hp(
                damage=raw_damage,
                rider_hp=state.hp,
            )
            ride_after=ride

        sleep_cleared=state.sleep_turns > 0
        next_state=replace(
            state,
            hp=int(hp_result.rider_hp),
            resistance=resistance_after,
            sleep_turns=0,
            ride=ride_after,
        )
        working[slot]=next_state
        results.append(
            AttackMagicTargetResolution(
                slot=slot,
                participant_id=state.participant_id,
                dodged=False,
                true_magic_success=cast_success,
                raw_magic_damage=raw_damage,
                reported_rider_damage=int(hp_result.reported_rider_damage),
                ride_pet_damage=int(hp_result.pet_damage),
                hp_before=state.hp,
                hp_after=next_state.hp,
                ride_pet_hp_before=ride_before,
                ride_pet_hp_after=(
                    None
                    if next_state.ride is None
                    else int(next_state.ride.hp)
                ),
                ride_pet_unmounted=bool(hp_result.unmounted),
                sleep_cleared=sleep_cleared,
                resistance_before=state.resistance,
                resistance_after=resistance_after,
                damage_detail=detail,
            )
        )

    return EnemyAttackMagicActionResolution(
        plan=plan,
        attacker_proficiency=proficiency,
        true_magic_success=cast_success,
        target_order=target_order,
        targets=tuple(results),
        defenders_after=working,
        attacker_training_applied=False,
    )
