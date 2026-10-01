#!/usr/bin/env python3
"""Fixed-descendant PETSKILL_MpDamage reference boundary.

The guarded numeric COM1 is intentionally not assigned to recovered25.
The callback shares DamageToHp's C integer-division attack-power quirk, while
its post-hit effect removes a percentage of the target's *current* MP.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_damage_to_hp_model import c_atoi, c_int_div


CALLBACK_NAME = "PETSKILL_MpDamage"
COMMAND_NAME = "BATTLE_COM_S_MPDAMAGE"


@dataclass(frozen=True)
class MpDamageOption:
    attack_adjust_token: int
    mp_percent: int
    token_count: int

    @property
    def callback_integer_ratio(self) -> int:
        return c_int_div(self.attack_adjust_token,100)


def parse_mp_damage_option(option: str) -> MpDamageOption:
    tokens=str(option).split("|")
    if len(tokens) < 2:
        raise ValueError("MpDamage OPTION requires at least two pipe fields")
    return MpDamageOption(
        attack_adjust_token=c_atoi(tokens[0]),
        mp_percent=c_atoi(tokens[1]),
        token_count=len(tokens),
    )


def mp_damage_attack_power(
    fixed_strength: int,
    option: MpDamageOption,
) -> int:
    fixed_strength=int(fixed_strength)
    ratio=int(option.callback_integer_ratio)
    return fixed_strength-int(fixed_strength*float(ratio))


@dataclass(frozen=True)
class MpDamageResolution:
    attempted: bool
    physical_damage: int
    target_kind: str
    target_damage_react_blocked: bool
    mp_percent: int
    mp_damage: int
    mp_before: int
    mp_after: int


def resolve_mp_damage(
    *,
    physical_damage: int,
    target_kind: str,
    target_mp: int,
    target_damage_react: int,
    option: MpDamageOption,
) -> MpDamageResolution:
    """Mirror fixed BATTLE_S_MpDamage after physical DamageSub.

    The helper does not scale MP loss from physical damage. Physical damage is
    only a >0 gate. Enemy/pet targets are excluded, and active DamageReact
    blocks the effect. The percentage is applied to current MP.
    """

    damage=int(physical_damage)
    kind=str(target_kind)
    mp=int(target_mp)
    react=int(target_damage_react)
    if mp < 0:
        raise ValueError("MpDamage target MP cannot be negative")

    blocked=react>0
    if damage < 1 or blocked or kind in {"enemy","pet"} or mp <= 0:
        return MpDamageResolution(
            attempted=False,
            physical_damage=damage,
            target_kind=kind,
            target_damage_react_blocked=blocked,
            mp_percent=int(option.mp_percent),
            mp_damage=0,
            mp_before=mp,
            mp_after=mp,
        )

    amount=int(mp*(float(option.mp_percent)/100.0))
    return MpDamageResolution(
        attempted=True,
        physical_damage=damage,
        target_kind=kind,
        target_damage_react_blocked=False,
        mp_percent=int(option.mp_percent),
        mp_damage=int(amount),
        mp_before=mp,
        mp_after=mp-int(amount),
    )
