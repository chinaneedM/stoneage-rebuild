"""Explicit PETSKILL_Combined descendant initiative profiles.

The fixed descendant sources disagree on the BATTLE_COM_JYUJYUTU initiative
range. R1 therefore requires an explicit profile witness instead of choosing
one descendant as historical truth.
"""
from __future__ import annotations

from dataclasses import dataclass

PROFILE_GAVIN_IRIS_30PCT = "gavin_iris_scaled_30pct"
PROFILE_BISMARCK_FIXED15 = "bismarck_fixed_15"
ADMITTED_PROFILES = (
    PROFILE_GAVIN_IRIS_30PCT,
    PROFILE_BISMARCK_FIXED15,
)


class CombinedInitiativeDomain(ValueError):
    """Input is outside the audited Combined initiative witness domain."""


def _int32(value: int) -> int:
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise CombinedInitiativeDomain("requires signed int32 witness")
    return value


@dataclass(frozen=True)
class CombinedInitiativeResolution:
    profile: str
    work_quick: int
    base_work: int
    max_random_subtract: int
    random_subtract: int
    action_value: int
    rng_draws_consumed: int = 1


def resolve_combined_initiative(
    *,
    profile: str,
    work_quick: int,
    random_subtract: int,
) -> CombinedInitiativeResolution:
    """Resolve the audited BATTLE_DexCalc branch from an explicit RAND witness.

    gavin/iris:
        work = WORKQUICK + 20
        dex = work - RAND(0, work * 0.3)

    fixed Bismarck:
        work = WORKQUICK + 20
        dex = work - RAND(0, 15)

    The source final dex<=1 clamp is commented out at the fixed Bismarck pin,
    so this model does not silently apply the older common-core clamp. It owns
    one already-reduced RAND result and no callback-selection RNG.
    """
    profile = str(profile)
    if profile not in ADMITTED_PROFILES:
        raise CombinedInitiativeDomain(
            "Combined initiative profile must be explicit"
        )
    work_quick = _int32(work_quick)
    random_subtract = _int32(random_subtract)
    base_work = work_quick + 20
    _int32(base_work)

    if profile == PROFILE_GAVIN_IRIS_30PCT:
        max_subtract = int(base_work * 0.30)
        if max_subtract < 0:
            raise CombinedInitiativeDomain(
                "negative scaled RAND upper bound is outside admitted domain"
            )
    else:
        max_subtract = 15

    if not 0 <= random_subtract <= max_subtract:
        raise CombinedInitiativeDomain(
            "Combined initiative RAND witness outside profile range"
        )
    action_value = base_work - random_subtract
    _int32(action_value)
    return CombinedInitiativeResolution(
        profile=profile,
        work_quick=work_quick,
        base_work=base_work,
        max_random_subtract=max_subtract,
        random_subtract=random_subtract,
        action_value=action_value,
    )
