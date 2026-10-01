#!/usr/bin/env python3
"""Fixed-descendant PETSKILL_FallGround reference boundary.

This models the guarded _PSKILL_FALLGROUND callback plus the post-damage
fall decision.  It deliberately keeps compile-profile differences explicit:
gavin/iriselia enable equipment fall resistance and same-side prevention,
while pinned Bismarck does not.  None of the pinned descendants defines
_FIXPETFALL, so the historical player ride-slot test is strictly > 0.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


CALLBACK_NAME = "PETSKILL_FallGround"
COMMAND_NAME = "BATTLE_COM_S_FALLRIDE"
ATTACK_MARKER = "攻%"


@dataclass(frozen=True)
class FallGroundOption:
    attack_percent: float | None
    marker_present: bool


def parse_fall_ground_option(option: str) -> FallGroundOption:
    text=str(option)
    at=text.find(ATTACK_MARKER)
    if at < 0:
        return FallGroundOption(None,False)
    tail=text[at+len(ATTACK_MARKER):]
    match=re.match(
        r"[\t\n\v\f\r ]*"
        r"([+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))"
        r"(?:[eE][+-]?\d+)?)",
        tail,
    )
    if match is None:
        # sscanf("%f") would fail; fixed callback keeps fPer's initial 0.01
        # and still applies it because the marker itself was found.
        return FallGroundOption(None,True)
    return FallGroundOption(float(match.group(1)),True)


def fall_ground_attack_power(
    fixed_strength: int,
    option: FallGroundOption,
) -> int:
    """Mirror callback WORKATTACKPOWER mutation.

    If the marker is absent the callback leaves WORKATTACKPOWER untouched; this
    function therefore rejects that case because no prior work value is passed.
    If the marker exists but sscanf fails, fPer remains 0.01 then is divided by
    100, exactly as the fixed callback does.
    """

    fixed=int(fixed_strength)
    if not option.marker_present:
        raise ValueError("FallGround marker absent: prior WORKATTACKPOWER unknown")
    percent=0.01 if option.attack_percent is None else float(option.attack_percent)
    fraction=percent/100.0
    return fixed+int(fixed*fraction)


@dataclass(frozen=True)
class FallGroundResolution:
    rng_consumed: bool
    roll_0_100: int | None
    threshold: int | None
    roll_passed: bool
    target_kind: str
    ride_pet_slot_before: int | None
    fell: bool
    ride_pet_slot_after: int | None
    petfall_after: bool


def resolve_fall_ground(
    *,
    post_damage_player_damage: int,
    damage_react: int,
    same_side: bool,
    target_kind: str,
    ride_pet_slot: int | None,
    fall_roll_0_100: int | None,
    equipment_fall_resistance: int = 0,
    use_equipment_resistance: bool,
    prevent_same_side: bool,
    fix_petfall: bool = False,
) -> FallGroundResolution:
    """Resolve the fixed FallGround side effect after BATTLE_DamageSub.

    RAND(0,100) is consumed whenever the common gate passes, even if the target
    is not riding.  For PLAYER targets the pinned descendants all use the
    unfixed ride test (>0), because none defines _FIXPETFALL.
    """

    damage=int(post_damage_player_damage)
    react=int(damage_react)
    same=bool(same_side)
    kind=str(target_kind)
    resistance=int(equipment_fall_resistance)

    gate=damage > 0 and react == 0 and not (prevent_same_side and same)
    if not gate:
        if fall_roll_0_100 is not None:
            raise ValueError("FallGround RNG supplied on a gated-off path")
        return FallGroundResolution(
            False,None,None,False,kind,ride_pet_slot,False,ride_pet_slot,False
        )

    if fall_roll_0_100 is None:
        raise ValueError("FallGround RAND(0,100) is required")
    roll=int(fall_roll_0_100)
    if not 0 <= roll <= 100:
        raise ValueError("FallGround roll must be in 0..100")

    threshold=50+(resistance if use_equipment_resistance else 0)
    passed=roll > threshold
    fell=False
    after=ride_pet_slot
    petfall=False
    if passed and kind == "player" and ride_pet_slot is not None:
        slot=int(ride_pet_slot)
        mounted_test=slot >= 0 if fix_petfall else slot > 0
        if mounted_test:
            fell=True
            after=None
            petfall=True

    return FallGroundResolution(
        True,roll,threshold,passed,kind,ride_pet_slot,fell,after,petfall
    )
