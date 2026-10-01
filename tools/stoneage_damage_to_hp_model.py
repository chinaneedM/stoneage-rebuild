#!/usr/bin/env python3
"""Fixed-descendant PETSKILL_DamageToHp reference boundary.

This is the older _SKILL_DAMAGETOHP callback, not the later
PETSKILL_DamageToHp2 variant.  The guarded numeric COM1 is intentionally not
assigned to recovered25 here.

Two source quirks are preserved exactly:
- callback setup computes `atoi(token1) / 100` as C integer division before
  assigning it to float;
- post-hit recovery uses floating division for token2 and converts
  `damage * ratio` back to int with C truncation toward zero.
"""

from __future__ import annotations

from dataclasses import dataclass


CALLBACK_NAME = "PETSKILL_DamageToHp"
COMMAND_NAME = "BATTLE_COM_S_DAMAGETOHP"


def c_atoi(text: str) -> int:
    """Small source-compatible atoi subset for recovered ASCII OPTION tokens."""

    s=str(text)
    i=0
    while i < len(s) and s[i].isspace():
        i+=1
    sign=1
    if i < len(s) and s[i] in "+-":
        if s[i] == "-":
            sign=-1
        i+=1
    start=i
    value=0
    while i < len(s) and "0" <= s[i] <= "9":
        value=value*10+(ord(s[i])-48)
        i+=1
    if i == start:
        return 0
    return sign*value


def c_int_div(numerator: int, denominator: int) -> int:
    """C99 integer division truncating toward zero."""

    numerator=int(numerator)
    denominator=int(denominator)
    if denominator == 0:
        raise ZeroDivisionError("C integer division by zero")
    quotient=abs(numerator)//abs(denominator)
    return -quotient if (numerator < 0) != (denominator < 0) else quotient


@dataclass(frozen=True)
class DamageToHpOption:
    attack_adjust_token: int
    recovery_percent: int
    token_count: int

    @property
    def callback_integer_ratio(self) -> int:
        # Fixed callback: def = (atoi(buf1) / 100); both operands are int.
        return c_int_div(self.attack_adjust_token,100)


def parse_damage_to_hp_option(option: str) -> DamageToHpOption:
    """Parse only the two delimiter positions consumed by fixed source."""

    text=str(option)
    tokens=text.split("|")
    if len(tokens) < 2:
        raise ValueError("DamageToHp OPTION requires at least two pipe fields")
    return DamageToHpOption(
        attack_adjust_token=c_atoi(tokens[0]),
        recovery_percent=c_atoi(tokens[1]),
        token_count=len(tokens),
    )


def damage_to_hp_attack_power(
    fixed_strength: int,
    option: DamageToHpOption,
) -> int:
    """Mirror callback WORKATTACKPOWER rewrite, including integer-division bug."""

    fixed_strength=int(fixed_strength)
    ratio=int(option.callback_integer_ratio)
    return fixed_strength-int(fixed_strength*float(ratio))


@dataclass(frozen=True)
class DamageToHpRecovery:
    attempted: bool
    target_damage_react_blocked: bool
    damage_basis: int
    recovery_percent: int
    reported_recovery: int
    effective_hp_delta: int
    attacker_hp_before: int
    attacker_hp_after: int


def resolve_damage_to_hp_recovery(
    *,
    damage: int,
    petdamage: int,
    attacker_hp: int,
    attacker_max_hp: int,
    target_damage_react: int,
    option: DamageToHpOption,
) -> DamageToHpRecovery:
    """Mirror BATTLE_S_DamageToHp after BATTLE_S_AttackDamage settlement.

    The fixed caller passes damage + petdamage as the recovery basis.  Damage
    reaction blocks conversion whenever BATTLE_GetDamageReact(defindex) > 0.
    """

    damage_basis=int(damage)+int(petdamage)
    hp=int(attacker_hp)
    max_hp=int(attacker_max_hp)
    react=int(target_damage_react)
    if max_hp < 0:
        raise ValueError("DamageToHp attacker max HP cannot be negative")
    if hp > max_hp:
        raise ValueError("DamageToHp attacker HP cannot exceed max HP")

    if damage_basis < 1 or react > 0:
        return DamageToHpRecovery(
            attempted=False,
            target_damage_react_blocked=react>0,
            damage_basis=damage_basis,
            recovery_percent=int(option.recovery_percent),
            reported_recovery=0,
            effective_hp_delta=0,
            attacker_hp_before=hp,
            attacker_hp_after=hp,
        )

    # Fixed source: def=((float)defi)/100; A_HP=(int)(Damage*def).
    reported=int(damage_basis*(float(option.recovery_percent)/100.0))
    if reported+hp > max_hp:
        reported=max_hp-hp
    after=min(hp+reported,max_hp)
    return DamageToHpRecovery(
        attempted=True,
        target_damage_react_blocked=False,
        damage_basis=damage_basis,
        recovery_percent=int(option.recovery_percent),
        reported_recovery=int(reported),
        effective_hp_delta=int(after-hp),
        attacker_hp_before=hp,
        attacker_hp_after=int(after),
    )
