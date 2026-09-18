#!/usr/bin/env python3
"""Reference model for the convergent StoneAge descendant pet-growth core."""

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
