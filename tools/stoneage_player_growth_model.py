#!/usr/bin/env python3
"""Reference model for the convergent StoneAge descendant player-growth core."""

from dataclasses import dataclass
from typing import Mapping

POINTS_PER_LEVEL=3
INTERNAL_PER_DISPLAY_POINT=100

LEGACY_CUMULATIVE_EXP='legacy_cumulative'
PER_LEVEL_EXP='per_level'
PLAYER_LEVELUP_CHARM_DELTA=2

EXP_PROFILES=frozenset({LEGACY_CUMULATIVE_EXP,PER_LEVEL_EXP})


@dataclass(frozen=True)
class PlayerExpTransition:
    profile: str
    start_level: int
    start_exp: int
    award_exp: int
    end_level: int
    end_exp: int
    next_max_exp: int
    levels_gained: int
    free_stat_points_delta: int
    charm_delta: int
    duel_point_delta: int


def resolve_player_exp_transition(
    current_level,
    current_exp,
    award_exp,
    current_max_exp,
    *,
    profile,
    next_max_exp_by_level: Mapping[int,int] | None = None,
):
    '''Resolve one explicitly selected descendant EXP transition regime.

    current_max_exp is the max/next EXP exposed for the current level.
    After a crossing, next_max_exp_by_level[new_level] supplies the next
    exposed value. Threshold data remains caller-supplied so later mixed
    server tables are never silently promoted to an early JSS baseline.
    '''
    level=int(current_level)
    exp=int(current_exp)
    award=int(award_exp)
    max_exp=int(current_max_exp)
    profile=str(profile)
    future={} if next_max_exp_by_level is None else {
        int(k):int(v) for k,v in next_max_exp_by_level.items()
    }

    if profile not in EXP_PROFILES:
        raise ValueError(f'unknown EXP profile: {profile}')
    if level < 1:
        raise ValueError('current_level must be >= 1')
    if exp < 0 or award < 0:
        raise ValueError('EXP values must be non-negative')
    if max_exp <= 0:
        raise ValueError('current_max_exp must be positive')
    if exp >= max_exp:
        raise ValueError('starting EXP must be below current max EXP')

    start_level=level
    start_exp=exp
    work_exp=exp+award
    levels_gained=0
    duel_point_delta=0

    while work_exp >= max_exp:
        crossed=max_exp
        if profile == PER_LEVEL_EXP:
            work_exp-=crossed

        level+=1
        levels_gained+=1
        duel_point_delta+=level*10

        if level not in future:
            raise ValueError(f'missing next max EXP for new level {level}')
        next_max=int(future[level])
        if next_max <= 0:
            raise ValueError('next max EXP must be positive')
        if profile == LEGACY_CUMULATIVE_EXP and next_max <= crossed:
            raise ValueError(
                'legacy cumulative max EXP must increase after level-up'
            )
        max_exp=next_max

    return PlayerExpTransition(
        profile=profile,
        start_level=start_level,
        start_exp=start_exp,
        award_exp=award,
        end_level=level,
        end_exp=work_exp,
        next_max_exp=max_exp,
        levels_gained=levels_gained,
        free_stat_points_delta=levels_gained*POINTS_PER_LEVEL,
        charm_delta=PLAYER_LEVELUP_CHARM_DELTA if levels_gained else 0,
        duel_point_delta=duel_point_delta,
    )


def displayed_stat(internal_value):
    """Protocol/UI representation of an internal base stat."""
    return int(internal_value)//INTERNAL_PER_DISPLAY_POINT


def award_free_points(current_points,levels_gained,points_per_level=POINTS_PER_LEVEL):
    levels_gained=int(levels_gained)
    if levels_gained<0:
        raise ValueError("levels_gained must be non-negative")
    return int(current_points)+levels_gained*int(points_per_level)


def spend_free_point(vital,strength,toughness,dexterity,free_points,stat_index):
    """Spend one player free point on VITAL/STR/TOUGH/DEX (0..3)."""
    values=[int(vital),int(strength),int(toughness),int(dexterity)]
    free_points=int(free_points)
    stat_index=int(stat_index)
    if free_points<=0:
        raise ValueError("no free stat points available")
    if not 0<=stat_index<4:
        raise ValueError("stat_index must be 0..3")
    values[stat_index]+=INTERNAL_PER_DISPLAY_POINT
    return (*values,free_points-1)


def base_derived_stats(vital,strength,toughness,dexterity):
    """Return stable pre-equipment work stats.

    Inputs use the server's x100 persistent representation.
    Positive float-to-int conversions match C truncation.
    """
    v=int(vital)
    s=int(strength)
    t=int(toughness)
    d=int(dexterity)

    fix_vital=int(v*0.01)
    fix_dex=int(d*0.01)
    fix_str=int(
        s*0.01*1.0
        + t*0.01*0.10
        + v*0.01*0.10
        + d*0.01*0.05
    )
    fix_tough=int(
        t*0.01*1.0
        + s*0.01*0.10
        + v*0.01*0.10
        + d*0.01*0.05
    )
    max_hp=int((v*4+s+t+d)*0.01)

    return {
        "fix_vital":fix_vital,
        "fix_str":fix_str,
        "fix_tough":fix_tough,
        "fix_dex":fix_dex,
        "attack_power":fix_str,
        "defence_power":fix_tough,
        "quick":fix_dex,
        "max_hp":max_hp,
    }
