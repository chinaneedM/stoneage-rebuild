#!/usr/bin/env python3
"""Reference model for the convergent StoneAge descendant pet-growth core."""

from dataclasses import dataclass
from typing import Mapping, Sequence

from tools.stoneage_player_growth_model import resolve_player_exp_transition

VARIABLE_AI_LEVELUP_DELTA=500
VARIABLE_AI_MIN=-10000
VARIABLE_AI_MAX=10000


@dataclass(frozen=True)
class PetLevelGrowthRolls:
    allocation_rolls: tuple[int, ...]
    rank_roll: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "allocation_rolls", tuple(int(x) for x in self.allocation_rolls)
        )
        object.__setattr__(self, "rank_roll", int(self.rank_roll))


@dataclass(frozen=True)
class PetGrowthTransition:
    start_internal_stats: tuple[int, int, int, int]
    end_internal_stats: tuple[int, int, int, int]
    per_level_increments: tuple[tuple[int, int, int, int], ...]
    start_variable_ai: int
    end_variable_ai: int
    levels_gained: int

@dataclass(frozen=True)
class PetExpGrowthTransition:
    profile: str
    start_level: int
    start_exp: int
    award_exp: int
    end_level: int
    end_exp: int
    next_max_exp: int
    levels_gained: int
    growth: PetGrowthTransition

RANK_THRESHOLDS=((100,0),(95,1),(90,2),(85,3),(80,4),(0,5))
RANK_ROLL_RANGES=((450,500),(470,520),(490,540),(510,560),(530,580),(550,600))


def pet_rank_from_template_base(vital,strength,toughness,dexterity):
    total=int(vital)+int(strength)+int(toughness)+int(dexterity)
    for threshold,rank in RANK_THRESHOLDS:
        if total>=threshold:
            return rank
    raise AssertionError("unreachable rank")


def pack_growth_base(vital,strength,toughness,dexterity):
    vals=(vital,strength,toughness,dexterity)
    if any(not 0<=int(v)<=255 for v in vals):
        raise ValueError("growth-base components must fit one unsigned byte")
    return (
        (int(vital)<<24)
        | (int(strength)<<16)
        | (int(toughness)<<8)
        | int(dexterity)
    )


def unpack_growth_base(packed):
    packed=int(packed)
    return (
        (packed>>24)&0xff,
        (packed>>16)&0xff,
        (packed>>8)&0xff,
        packed&0xff,
    )


def individualize_growth_base(template_base,offsets):
    if len(template_base)!=4 or len(offsets)!=4:
        raise ValueError("expected four growth components and four offsets")
    if any(int(x)<-2 or int(x)>2 for x in offsets):
        raise ValueError("birth offsets must be in -2..2")
    vals=tuple(int(v)+int(o) for v,o in zip(template_base,offsets))
    if any(v<0 or v>255 for v in vals):
        raise ValueError("individualized growth base no longer fits a byte")
    return vals


def allocation_counts(allocation_rolls):
    if len(allocation_rolls)!=10:
        raise ValueError("pet level-up requires exactly ten allocation rolls")
    counts=[0,0,0,0]
    for roll in allocation_rolls:
        roll=int(roll)
        if not 0<=roll<=3:
            raise ValueError("allocation rolls must be in 0..3")
        counts[roll]+=1
    return tuple(counts)


def adjust_pet_variable_ai(current_variable_ai,delta):
    current=int(current_variable_ai)
    if not VARIABLE_AI_MIN<=current<=VARIABLE_AI_MAX:
        raise ValueError('current_variable_ai outside stable range')
    return min(
        VARIABLE_AI_MAX,
        max(VARIABLE_AI_MIN,current+int(delta)),
    )


def advance_pet_growth(
    growth_base,
    rank,
    current_internal_stats,
    current_variable_ai,
    level_rolls: Sequence[PetLevelGrowthRolls],
):
    '''Apply one explicit stable-descendant growth draw set per gained level.

    CHAR_ALLOCPOINT/growth_base and PETRANK are persistent identity inputs and
    are not mutated by level-up. Each level consumes ten allocation draws and
    one rank-band multiplier draw, then adds +500 to hidden VARIABLEAI with
    the stable -10000..10000 clamp.
    '''
    if len(growth_base)!=4 or len(current_internal_stats)!=4:
        raise ValueError('growth and current stat vectors must have four components')
    start=tuple(int(x) for x in current_internal_stats)
    if any(x<0 for x in start):
        raise ValueError('current internal pet stats must be non-negative')
    variable_ai=int(current_variable_ai)
    if not VARIABLE_AI_MIN<=variable_ai<=VARIABLE_AI_MAX:
        raise ValueError('current_variable_ai outside stable range')

    current=list(start)
    increments=[]
    for raw_rolls in tuple(level_rolls):
        rolls=(
            raw_rolls
            if isinstance(raw_rolls,PetLevelGrowthRolls)
            else PetLevelGrowthRolls(*raw_rolls)
        )
        inc=pet_level_increments(
            growth_base,
            rank,
            rolls.allocation_rolls,
            rolls.rank_roll,
        )
        current=[value+delta for value,delta in zip(current,inc)]
        increments.append(tuple(inc))
        variable_ai=adjust_pet_variable_ai(
            variable_ai,
            VARIABLE_AI_LEVELUP_DELTA,
        )

    return PetGrowthTransition(
        start_internal_stats=start,
        end_internal_stats=tuple(current),
        per_level_increments=tuple(increments),
        start_variable_ai=int(current_variable_ai),
        end_variable_ai=variable_ai,
        levels_gained=len(increments),
    )

def resolve_pet_exp_growth_transition(
    current_level,
    current_exp,
    award_exp,
    current_max_exp,
    *,
    profile,
    next_max_exp_by_level: Mapping[int,int] | None,
    growth_base,
    rank,
    current_internal_stats,
    current_variable_ai,
    level_rolls: Sequence[PetLevelGrowthRolls],
):
    '''Resolve EXP thresholds and exactly one explicit growth draw bundle per level.

    Pet EXP follows the same versioned CHAR_LevelUpCheck threshold regimes as
    player EXP. Unlike players, each crossed level additionally invokes
    CHAR_PetLevelUp() and CHAR_PetAddVariableAi(), so the caller must provide
    exactly one deterministic PetLevelGrowthRolls bundle for every level gained.
    '''
    exp_transition=resolve_player_exp_transition(
        current_level,
        current_exp,
        award_exp,
        current_max_exp,
        profile=profile,
        next_max_exp_by_level=next_max_exp_by_level,
    )
    rolls=tuple(level_rolls)
    if len(rolls)!=exp_transition.levels_gained:
        raise ValueError(
            'pet level-up requires exactly one growth roll bundle per gained level'
        )
    growth=advance_pet_growth(
        growth_base=growth_base,
        rank=rank,
        current_internal_stats=current_internal_stats,
        current_variable_ai=current_variable_ai,
        level_rolls=rolls,
    )
    return PetExpGrowthTransition(
        profile=exp_transition.profile,
        start_level=exp_transition.start_level,
        start_exp=exp_transition.start_exp,
        award_exp=exp_transition.award_exp,
        end_level=exp_transition.end_level,
        end_exp=exp_transition.end_exp,
        next_max_exp=exp_transition.next_max_exp,
        levels_gained=exp_transition.levels_gained,
        growth=growth,
    )


def pet_level_increments(growth_base,rank,allocation_rolls,rank_roll):
    """Return (vital, strength, toughness, dexterity) increments."""
    if len(growth_base)!=4:
        raise ValueError("growth_base must have four components")
    rank=int(rank)
    if not 0<=rank<len(RANK_ROLL_RANGES):
        rank=0
    lo,hi=RANK_ROLL_RANGES[rank]
    rank_roll=int(rank_roll)
    if not lo<=rank_roll<=hi:
        raise ValueError("rank_roll outside PETRANK range")
    counts=allocation_counts(allocation_rolls)
    multiplier=rank_roll*0.01
    return tuple(int((int(base)+bonus)*multiplier) for base,bonus in zip(growth_base,counts))
