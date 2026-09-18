#!/usr/bin/env python3
"""Reference model for the convergent StoneAge descendant player-growth core."""

POINTS_PER_LEVEL=3
INTERNAL_PER_DISPLAY_POINT=100


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
