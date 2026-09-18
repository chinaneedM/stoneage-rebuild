#!/usr/bin/env python3
"""Reference model for the convergent pre-sixth-transmigration player core."""

CORE_MAX_TRANSMIGRATIONS=5
CORE_MIN_LEVEL=80
CORE_EVENT_FLAGS=(39,40,42,46)
CORE_REQUIRED_PETS=(693,694,695,696)
ACCUMULATED_LEVEL_CAP=130
FREE_POINTS_PER_TRANSMIGRATION=10


def core_eligibility(level,transmigrations,event_flags,pet_ids,free_points=0):
    """Return (eligible, reason) for the stable five-transmigration gate."""
    level=int(level)
    transmigrations=int(transmigrations)
    flags=set(int(v) for v in event_flags)
    pets=list(int(v) for v in pet_ids)
    if transmigrations>=CORE_MAX_TRANSMIGRATIONS:
        return False,"max_transmigrations"
    if level<CORE_MIN_LEVEL:
        return False,"level"
    if int(free_points)>0:
        return False,"unspent_points"
    if not set(CORE_EVENT_FLAGS).issubset(flags):
        return False,"event_flags"
    if transmigrations<4:
        if CORE_REQUIRED_PETS[transmigrations] not in pets:
            return False,"required_pet"
    elif not set(CORE_REQUIRED_PETS).issubset(set(pets)):
        return False,"required_pets"
    return True,"ok"


def source_rounding(value,num=1):
    """Mirror the preserved C helper literally, including its unusual semantics."""
    value=float(value)
    num=int(num)
    if num<0:
        return value
    num-=1
    p=float(10**num)
    return (value*p+0.5)/p


def inherited_total_points(
    stats_internal,new_transmigrations,accumulated_quests,accumulated_levels
):
    total_internal=sum(int(v) for v in stats_internal)
    if total_internal<=0:
        raise ValueError("total internal stats must be positive")
    displayed_total=float(total_internal)/100.0
    ans=(
        displayed_total/12.0
        + float(accumulated_quests)/4.0
        + (float(accumulated_levels)-int(new_transmigrations)*85.0)/4.0
    )
    return int(ans)


def apply_core_transmigration(
    stats_internal,
    level,
    quest_count,
    old_transmigrations,
    accumulated_quests=0,
    accumulated_levels=0,
):
    """Apply stable status/reset math for the ordinary 1st..5th transmigration."""
    stats=tuple(int(v) for v in stats_internal)
    if len(stats)!=4:
        raise ValueError("stats_internal must contain VITAL/STR/TOUGH/DEX")
    old_transmigrations=int(old_transmigrations)
    if not 0<=old_transmigrations<CORE_MAX_TRANSMIGRATIONS:
        raise ValueError("old_transmigrations must be 0..4 for the core model")
    new_transmigrations=old_transmigrations+1
    new_quests=int(accumulated_quests)+int(quest_count)
    new_levels=int(accumulated_levels)+min(int(level),ACCUMULATED_LEVEL_CAP)
    total_internal=sum(stats)
    if total_internal<=0:
        raise ValueError("total internal stats must be positive")

    inherited_total=inherited_total_points(
        stats,new_transmigrations,new_quests,new_levels
    )
    inherited_stats=[]
    for stat in stats:
        share=float(stat)/float(total_internal)*inherited_total
        internal=int(source_rounding(share,1)*100)
        inherited_stats.append(max(0,internal))

    return {
        "transmigrations":new_transmigrations,
        "level":1,
        "exp":0,
        "free_stat_points":new_transmigrations*FREE_POINTS_PER_TRANSMIGRATION,
        "accumulated_quests":new_quests,
        "accumulated_levels":new_levels,
        "trans_equation":(new_quests<<16)+new_levels,
        "inherited_total_formula_result":inherited_total,
        "vital":inherited_stats[0],
        "strength":inherited_stats[1],
        "toughness":inherited_stats[2],
        "dexterity":inherited_stats[3],
    }
