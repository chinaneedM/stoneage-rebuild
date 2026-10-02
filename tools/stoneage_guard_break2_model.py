#!/usr/bin/env python3
"""Guarded fixed-source model for PETSKILL_GuardBreak2.

This module models only source behavior that converges across the pinned
gavin/iriselia/Bismarck profiles. It deliberately does not assign a historical
numeric COM1 to recovered25 data and does not treat the source pet-skill symbol
number as a recovered25 row ID.
"""

from __future__ import annotations

from dataclasses import dataclass

CALLBACK_NAME = "PETSKILL_GuardBreak2"
COMMAND_NAME = "BATTLE_COM_S_GBREAK2"
FEATURE_NAME = "_SKILL_GUARDBREAK2"
SOURCE_PETSKILL_SYMBOL_NAME = "PETSKILL_GUARDBREAK2"
SOURCE_GUARD_MULTIPLIER = 1.3
SOURCE_NONGUARD_MULTIPLIER = 0.7
INT32_MAX = 2**31 - 1


class GuardBreak2UndefinedSourceDomain(ValueError):
    """Input would leave the fixed C int conversion outside the closed domain."""


@dataclass(frozen=True)
class GuardBreak2DamageResolution:
    damage_before: int
    defender_command_is_guard: bool
    multiplier: float
    damage_after_multiplier: int
    guard_adjust_applies_after_multiplier: bool


def _checked_damage(value: int) -> int:
    value = int(value)
    if not 0 <= value <= INT32_MAX:
        raise GuardBreak2UndefinedSourceDomain(
            "GuardBreak2 damage requires a nonnegative signed-int32 input"
        )
    return value


def resolve_guard_break2_damage_step(
    damage: int,
    *,
    defender_command_is_guard: bool,
    defender_confusion_counter: int = 0,
) -> GuardBreak2DamageResolution:
    """Mirror the GBreak2 branch inside fixed-source BATTLE_AttackSeq.

    The branch tests only defender COM1 when selecting 1.3 versus 0.7.
    Afterwards the ordinary GuardAdjust path still runs only when COM1 is GUARD
    and WORKCONFUSION <= 0. The caller owns that GuardAdjust RNG/mechanics.

    C evaluates int * double then assigns back to int, truncating toward zero.
    """
    before = _checked_damage(damage)
    command_guard = bool(defender_command_is_guard)
    confusion = int(defender_confusion_counter)
    multiplier = (
        SOURCE_GUARD_MULTIPLIER
        if command_guard
        else SOURCE_NONGUARD_MULTIPLIER
    )
    scaled_float = before * multiplier
    if not 0 <= scaled_float <= INT32_MAX:
        raise GuardBreak2UndefinedSourceDomain(
            "GuardBreak2 scaled damage cannot convert to signed int32"
        )
    after = int(scaled_float)
    return GuardBreak2DamageResolution(
        damage_before=before,
        defender_command_is_guard=command_guard,
        multiplier=multiplier,
        damage_after_multiplier=after,
        guard_adjust_applies_after_multiplier=(
            command_guard and confusion <= 0
        ),
    )
