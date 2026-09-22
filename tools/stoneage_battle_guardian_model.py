#!/usr/bin/env python3
"""Stable descendant guardian eligibility seam.

Guardian registration is created by the pet Guardian skill during command
setup. Physical AttackSeq consults that registration after dodge but before
critical/damage. The check itself consumes no RNG.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardianRegistration:
    guardian_slot: int
    guardian_flag: bool = True
    guardian_barrier: int = 0

    def __post_init__(self) -> None:
        slot=int(self.guardian_slot)
        if not 0 <= slot <= 19:
            raise ValueError("guardian_slot must be in 0..19")
        barrier=int(self.guardian_barrier)
        if barrier < 0:
            raise ValueError("guardian_barrier cannot be negative")
        object.__setattr__(self,"guardian_slot",slot)
        object.__setattr__(self,"guardian_flag",bool(self.guardian_flag))
        object.__setattr__(self,"guardian_barrier",barrier)


def guardian_redirect_allowed(
    *,
    guardian_exists,
    guardian_slot,
    defender_slot,
    guardian_alive,
    guardian_flag,
    guardian_sleep=0,
    guardian_confusion=0,
    guardian_paralysis=0,
    guardian_stone=0,
    guardian_barrier=0,
    guardian_is_attacker=False,
    attacker_uses_throw_weapon=False,
):
    """Mirror the common BATTLE_GuardianCheck gates."""
    if not guardian_exists:
        return False
    if int(guardian_slot) == int(defender_slot):
        return False
    if not guardian_alive or not guardian_flag:
        return False
    if any(
        int(value)>0
        for value in (
            guardian_sleep,
            guardian_confusion,
            guardian_paralysis,
            guardian_stone,
            guardian_barrier,
        )
    ):
        return False
    if guardian_is_attacker or attacker_uses_throw_weapon:
        return False
    return True
