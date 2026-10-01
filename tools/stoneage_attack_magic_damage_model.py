#!/usr/bin/env python3
"""Deterministic fixed-descendant StoneAge AttackMagic damage core.

This is a guarded/versioned layer. It reconstructs the convergent
_FIX_MAGICDAMAGE path from the three pinned descendants and keeps all RNG
values injected by the caller. It does not itself select attmagic footprints
or admit AttackMagic into recovered25 enemy-AI runtime.
"""

from __future__ import annotations

from dataclasses import dataclass


def c_int_div(numerator: int, denominator: int) -> int:
    """C-style signed integer division truncated toward zero."""
    numerator = int(numerator)
    denominator = int(denominator)
    if denominator == 0:
        raise ZeroDivisionError("integer division by zero")
    sign = -1 if (numerator < 0) ^ (denominator < 0) else 1
    return sign * (abs(numerator) // abs(denominator))


@dataclass(frozen=True)
class ElementAttrs:
    """Element order is earth=0, water=1, fire=2, wind=3, plus none."""

    earth: int
    water: int
    fire: int
    wind: int
    none: int = 0

    def __post_init__(self) -> None:
        for name in ("earth", "water", "fire", "wind", "none"):
            object.__setattr__(self, name, int(getattr(self, name)))

    def element(self, index: int) -> int:
        index = int(index)
        if index not in range(4):
            raise ValueError("element index must be 0..3")
        return (self.earth, self.water, self.fire, self.wind)[index]


def attacker_magic_proficiency(
    *,
    actor_kind: str,
    level: int,
    stored_proficiency: int,
) -> tuple[int, bool]:
    """Return fixed-source proficiency plus whether attacker training applies."""
    if str(actor_kind) == "enemy":
        return int(int(level) * 0.9), False
    # _FIX_MAGICDAMAGE marks the non-player/non-enemy branch as trainable and
    # reads stored CHAR_EARTH_EXP+n values (the source comment calls it PET).
    return int(stored_proficiency), True


def effective_magic_resistance(
    *,
    actor_kind: str,
    level: int,
    stored_resistance: int,
    equipment_resistance: int = 0,
    magic_defense_percent: int | None = None,
) -> int:
    """Reconstruct DEF_MAGIC_NUM resistance input before damage power."""
    kind = str(actor_kind)
    if kind == "player":
        value = int(stored_resistance) + int(equipment_resistance)
    elif kind == "enemy":
        value = int(int(level) * 0.5)
    else:
        value = int(stored_resistance)

    if magic_defense_percent is not None and value > 0:
        value = int(value + value * (int(magic_defense_percent) / 100.0))
    return value


def true_magic_success(*, proficiency: int, roll_0_99: int) -> bool:
    """One source rand()%100 proficiency check performed once per cast."""
    roll = int(roll_0_99)
    if not 0 <= roll <= 99:
        raise ValueError("true-magic roll must be 0..99")
    return roll <= int(proficiency)


def magic_dodge_threshold(
    *,
    actor_kind: str,
    level: int,
    luck: int = 0,
    base_resistance: int = 0,
    equipment_quimagic: int = 0,
) -> int:
    """Integer threshold consumed by BATTLE_MagicDodge."""
    if str(actor_kind) == "player":
        raw = (
            float(int(luck)) * 3.0
            + float(int(base_resistance)) * 0.15
            + float(int(equipment_quimagic)) * 0.9
        )
    else:
        raw = min(float(int(level)) * 0.2, 30.0)
    return int(raw)


def magic_dodges(
    *,
    actor_kind: str,
    level: int,
    roll_1_100: int,
    luck: int = 0,
    base_resistance: int = 0,
    equipment_quimagic: int = 0,
) -> bool:
    roll = int(roll_1_100)
    if not 1 <= roll <= 100:
        raise ValueError("magic-dodge roll must be 1..100")
    return roll <= magic_dodge_threshold(
        actor_kind=actor_kind,
        level=level,
        luck=luck,
        base_resistance=base_resistance,
        equipment_quimagic=equipment_quimagic,
    )


def fixed_magic_base_power(
    *,
    power: int,
    magic_level: int,
    attacker_proficiency: int,
    defender_resistance: int,
    random_0_19: int,
) -> int:
    """Kmagic/Mmagic/Amagic branch before elemental/field adjustment."""
    random_0_19 = int(random_0_19)
    if not 0 <= random_0_19 <= 19:
        raise ValueError("damage random must be 0..19")

    kmagic = (
        float(int(attacker_proficiency)) * 1.4
        - float(int(defender_resistance))
    )
    mmagic = float(int(attacker_proficiency))
    if kmagic < 0:
        kmagic = 0.0
    if mmagic < 1:
        mmagic = 1.0

    amagic = (kmagic * kmagic) / (mmagic * mmagic)
    amagic += float(random_0_19) / 100.0
    return int(
        int(power)
        * (1.0 + float(int(magic_level)) / 10.0)
        * amagic
    )


def field_attribute_power(
    *,
    field_element: int | None,
    field_power: int,
    attrs: ElementAttrs,
) -> float:
    """BATTLE_FieldAttAdjust with AJ_BOTTOM=AJ_PLUS=0.5."""
    if field_element is None or int(field_element) not in range(4):
        return 0.5
    value = attrs.element(int(field_element))
    return (
        0.5
        + float(value)
        * float(int(field_power))
        * 0.01
        * 0.01
        * 0.5
    )


def attr_calc(attacker: ElementAttrs, defender: ElementAttrs) -> int:
    """Four-element BATTLE_AttrCalc including assignment truncation."""
    fire = int(
        attacker.fire * defender.none * 1.5
        + attacker.fire * defender.fire * 1.0
        + attacker.fire * defender.water * 0.6
        + attacker.fire * defender.earth * 1.0
        + attacker.fire * defender.wind * 1.5
    )
    water = int(
        attacker.water * defender.none * 1.5
        + attacker.water * defender.fire * 1.5
        + attacker.water * defender.water * 1.0
        + attacker.water * defender.earth * 0.6
        + attacker.water * defender.wind * 1.0
    )
    earth = int(
        attacker.earth * defender.none * 1.5
        + attacker.earth * defender.fire * 1.0
        + attacker.earth * defender.water * 1.5
        + attacker.earth * defender.earth * 1.0
        + attacker.earth * defender.wind * 0.6
    )
    wind = int(
        attacker.wind * defender.none * 1.5
        + attacker.wind * defender.fire * 0.6
        + attacker.wind * defender.water * 1.0
        + attacker.wind * defender.earth * 1.5
        + attacker.wind * defender.wind * 1.0
    )
    none = int(
        attacker.none * defender.none * 1.0
        + attacker.none * defender.fire * 0.6
        + attacker.none * defender.water * 0.6
        + attacker.none * defender.earth * 0.6
        + attacker.none * defender.wind * 0.6
    )
    return int((fire + water + earth + wind + none) * 0.0001)


def magic_attribute_adjust(
    *,
    damage: int,
    magic_level: int,
    element: int,
    attacker_attrs: ElementAttrs,
    defender_attrs: ElementAttrs,
    field_element: int | None,
    field_power: int,
) -> int:
    """BATTLE_getMagicAdjustInt, preserving integer attr/50 traction."""
    element = int(element)
    if element not in range(4):
        raise ValueError("element index must be 0..3")

    magic10 = int(magic_level) * 10
    original = attacker_attrs.element(element)
    pulled = magic10 + magic10 * c_int_div(original, 50)

    values = [0, 0, 0, 0]
    values[element] = pulled
    # The source zeroes the other four elemental slots but leaves At_none
    # untouched; preserve that non-obvious behavior exactly.
    dragged = ElementAttrs(
        values[0],
        values[1],
        values[2],
        values[3],
        attacker_attrs.none,
    )
    at_field = field_attribute_power(
        field_element=field_element,
        field_power=field_power,
        attrs=dragged,
    )
    df_field = field_attribute_power(
        field_element=field_element,
        field_power=field_power,
        attrs=defender_attrs,
    )

    damage = int(damage)
    scaled = ElementAttrs(
        dragged.earth * damage,
        dragged.water * damage,
        dragged.fire * damage,
        dragged.wind * damage,
        dragged.none * damage,
    )
    adjusted = attr_calc(scaled, defender_attrs)
    return int(adjusted * (at_field / df_field))


def apply_true_magic_penalty(damage: int, *, success: bool) -> int:
    """Failed proficiency check applies source int *= 0.7."""
    return int(damage) if success else int(int(damage) * 0.7)


@dataclass(frozen=True)
class FixedMagicHitDamage:
    base_power: int
    attribute_adjusted: int
    true_magic_success: bool
    final_damage: int


def resolve_fixed_magic_hit_damage(
    *,
    power: int,
    magic_level: int,
    element: int,
    attacker_proficiency: int,
    defender_resistance: int,
    attacker_attrs: ElementAttrs,
    defender_attrs: ElementAttrs,
    field_element: int | None,
    field_power: int,
    damage_random_0_19: int,
    true_magic: bool,
) -> FixedMagicHitDamage:
    """Non-dodged hit: base power -> attr/field adjust -> 0.7 penalty."""
    base = fixed_magic_base_power(
        power=power,
        magic_level=magic_level,
        attacker_proficiency=attacker_proficiency,
        defender_resistance=defender_resistance,
        random_0_19=damage_random_0_19,
    )
    adjusted = magic_attribute_adjust(
        damage=base,
        magic_level=magic_level,
        element=element,
        attacker_attrs=attacker_attrs,
        defender_attrs=defender_attrs,
        field_element=field_element,
        field_power=field_power,
    )
    final = apply_true_magic_penalty(adjusted, success=true_magic)
    return FixedMagicHitDamage(base, adjusted, bool(true_magic), final)


def attack_magic_effect_value(
    *,
    positive_attr: int,
    negative_attr: int,
) -> int:
    """BATTLE_CalAttMagicEffect, including signed C integer division."""
    value = c_int_div(
        100 * int(positive_attr) - 100 * int(negative_attr),
        1000,
    )
    return max(-10, min(10, value))


def attack_magic_ride_ratio(
    *,
    element: int,
    rider_attrs: ElementAttrs,
    pet_attrs: ElementAttrs,
) -> int:
    """BATTLE_CalcCharaRatio; returned rider share is clamped to 2..8/10."""
    element = int(element)
    if element not in range(4):
        return 5

    positive = (element + 1) % 4
    rider_weight = 20 + attack_magic_effect_value(
        positive_attr=rider_attrs.element(positive),
        negative_attr=rider_attrs.element(element),
    )
    pet_weight = 20 + attack_magic_effect_value(
        positive_attr=pet_attrs.element(positive),
        negative_attr=pet_attrs.element(element),
    )
    ratio = c_int_div(
        10 * rider_weight,
        rider_weight + pet_weight,
    )
    return max(2, min(8, ratio))


@dataclass(frozen=True)
class AttackMagicHpResult:
    rider_hp: int
    pet_hp: int | None
    reported_rider_damage: int
    pet_damage: int
    unmounted: bool


def apply_attack_magic_hp(
    *,
    damage: int,
    rider_hp: int,
    ride_pet_hp: int | None = None,
    ride_ratio: int = 10,
) -> AttackMagicHpResult:
    """Apply the dedicated AttackMagic rider/pet HP branch.

    This intentionally preserves two source quirks:
    - rider overkill assigns the already-negative HP value back into the
      temporary rider share before computing pet damage, which can make pet
      damage exceed raw damage;
    - a ride pet that lands on exactly 0 HP is not unmounted here because the
      source tests the post-subtraction value with < 0 rather than <= 0.
    """
    damage = int(damage)
    rider_hp = int(rider_hp)

    if ride_pet_hp is None:
        return AttackMagicHpResult(
            max(0, rider_hp - damage),
            None,
            damage,
            0,
            False,
        )

    pet_hp = int(ride_pet_hp)
    if pet_hp <= 0:
        return AttackMagicHpResult(
            max(0, rider_hp - damage),
            pet_hp,
            damage,
            0,
            False,
        )

    intended_rider_damage = c_int_div(
        damage * int(ride_ratio),
        10,
    )
    reported_rider_damage = intended_rider_damage

    rider_after = rider_hp - intended_rider_damage
    source_rider_share = intended_rider_damage
    if rider_after < 0:
        source_rider_share = rider_after
        rider_after = 0

    pet_damage = damage - source_rider_share
    pet_after = pet_hp - pet_damage
    unmounted = pet_after < 0
    if unmounted:
        pet_after = 0

    return AttackMagicHpResult(
        rider_after,
        pet_after,
        reported_rider_damage,
        pet_damage,
        unmounted,
    )


@dataclass(frozen=True)
class MagicExpState:
    level: int
    exp: int
    opposed_level: int
    opposed_exp: int


def attack_magic_training(
    state: MagicExpState,
    *,
    magic_level: int,
    target_count: int,
) -> MagicExpState:
    """Magic_ComputeAttExp; caller gates this to failed trainable casts."""
    target_count = int(target_count)
    if target_count < 0:
        raise ValueError("target_count cannot be negative")

    level = int(state.level)
    exp = int(state.exp)
    opposed_level = int(state.opposed_level)
    opposed_exp = int(state.opposed_exp)
    add_exp = int(magic_level) * 3 * target_count

    exp += add_exp
    if exp > 100:
        exp = 0
        if level < 100:
            level += 1
    exp = max(exp, 0)
    level = max(0, min(100, level))

    if opposed_level > 1:
        opposed_exp = int(opposed_exp - add_exp * 0.5)
        if opposed_exp < 0:
            opposed_exp = 0
            opposed_level -= 1
            if opposed_level < 0:
                opposed_level = 0

    return MagicExpState(
        level,
        exp,
        opposed_level,
        opposed_exp,
    )


def defense_magic_training(
    state: MagicExpState,
    *,
    magic_level: int,
    damage: int,
) -> MagicExpState:
    """Magic_ComputeDefExp; source ignores hits below 200 final damage."""
    if int(damage) < 200:
        return state

    level = int(state.level)
    exp = int(state.exp)
    opposed_level = int(state.opposed_level)
    opposed_exp = int(state.opposed_exp)

    add_exp = c_int_div(int(damage), 20) * (int(magic_level) * 2)
    exp += add_exp
    if level < 0:
        level = 0
    if exp > 100:
        exp = 0
        if level < 100:
            level += 1
        level = max(0, min(100, level))
    exp = max(exp, 0)

    if opposed_level > 1:
        opposed_exp -= 2
        if opposed_exp < 0:
            opposed_exp = 90
            opposed_level -= 1
            if opposed_level < 0:
                opposed_level = 0

    return MagicExpState(
        level,
        exp,
        opposed_level,
        opposed_exp,
    )


def attacker_training_applies(
    *,
    training_actor: bool,
    true_magic: bool,
) -> bool:
    return bool(training_actor) and not bool(true_magic)


def attack_magic_hit_clears_sleep(*, dodged: bool) -> bool:
    """Only non-dodged targets enter def_be_hit and later lose SLEEP."""
    return not bool(dodged)
