#!/usr/bin/env python3
"""Reference model for the convergent StoneAge descendant player-creation core."""

BASE_STAT_TOTAL=20
BASE_STAT_MAX=20
ELEMENT_POINT_TOTAL=10
ELEMENT_POINT_MAX=10
INTERNAL_PER_DISPLAY_STAT=100
INTERNAL_PER_ELEMENT_POINT=10

DEFAULT_LEVEL=1
DEFAULT_EXP=0
DEFAULT_FREE_STAT_POINTS=0
DEFAULT_CHARM=60
DEFAULT_MP=100


def validate_base_stats(vital,strength,toughness,dexterity):
    """Validate the ordinary new-character VITAL/STR/TOUGH/DEX allocation."""
    values=tuple(int(v) for v in (vital,strength,toughness,dexterity))
    if any(v<0 or v>BASE_STAT_MAX for v in values):
        raise ValueError("each base stat must be between 0 and 20")
    if sum(values)!=BASE_STAT_TOTAL:
        raise ValueError("base stat allocation must total 20")
    return values


def validate_element_points(earth,water,fire,wind):
    """Validate the ordinary new-character elemental allocation."""
    values=tuple(int(v) for v in (earth,water,fire,wind))
    if any(v<0 or v>ELEMENT_POINT_MAX for v in values):
        raise ValueError("each element point value must be between 0 and 10")
    if sum(values)!=ELEMENT_POINT_TOTAL:
        raise ValueError("element allocation must total 10")
    if sum(v>0 for v in values)>2:
        raise ValueError("element points may occupy at most two elements")
    if earth>0 and fire>0:
        raise ValueError("earth and fire cannot both be allocated")
    if water>0 and wind>0:
        raise ValueError("water and wind cannot both be allocated")
    return values


def build_creation_state(
    vital,strength,toughness,dexterity,
    earth,water,fire,wind,
):
    """Build the stable ordinary creation state before derived/equipment work.

    Later test-server/new-player configuration overrides are intentionally
    excluded from this baseline model.
    """
    stats=validate_base_stats(vital,strength,toughness,dexterity)
    elements=validate_element_points(earth,water,fire,wind)
    return {
        "level":DEFAULT_LEVEL,
        "exp":DEFAULT_EXP,
        "free_stat_points":DEFAULT_FREE_STAT_POINTS,
        "charm":DEFAULT_CHARM,
        "mp":DEFAULT_MP,
        "max_mp":DEFAULT_MP,
        "vital":stats[0]*INTERNAL_PER_DISPLAY_STAT,
        "strength":stats[1]*INTERNAL_PER_DISPLAY_STAT,
        "toughness":stats[2]*INTERNAL_PER_DISPLAY_STAT,
        "dexterity":stats[3]*INTERNAL_PER_DISPLAY_STAT,
        "earth":elements[0]*INTERNAL_PER_ELEMENT_POINT,
        "water":elements[1]*INTERNAL_PER_ELEMENT_POINT,
        "fire":elements[2]*INTERNAL_PER_ELEMENT_POINT,
        "wind":elements[3]*INTERNAL_PER_ELEMENT_POINT,
    }
