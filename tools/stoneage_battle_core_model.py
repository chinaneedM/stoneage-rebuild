#!/usr/bin/env python3
"""Independently written model of the stable StoneAge descendant battle core.

This is an archaeology/reference model, not a claim that the 1999 JSS server
used every value here. Later profession/pet-skill/private-server extensions
are deliberately excluded.
"""

import math

PLAYER="player"
PET="pet"
ENEMY="enemy"
OTHER="other"

DAMAGE_RATE=2.0
D_16=1.0/16.0
D_8=1.0/8.0
KAWASHI_MAX_RATE=75
KAWASHI_PARA=0.02
CRITICAL_PARA=0.09
COUNTER_PARA=0.08


def _c_int(value):
    """C-style truncation toward zero for the positive values used here."""
    return int(value)


def early_action_value(quick, random_subtract, ride_quick=None):
    """Older convergent ordinary-command initiative profile.

    work = QUICK + 20
    dex = work - RAND(0, work * 0.30)
    non-positive values clamp to 1.
    """
    work=(ride_quick if ride_quick is not None else quick)+20
    max_sub=_c_int(work*0.30)
    if random_subtract < 0 or random_subtract > max_sub:
        raise ValueError("random_subtract outside older 30% initiative range")
    return max(1,work-random_subtract)


def early_item_action_value(quick, random_subtract):
    """Older convergent item-use initiative profile."""
    work=quick+20
    max_sub=_c_int(work*0.30)
    if random_subtract < 0 or random_subtract > max_sub:
        raise ValueError("random_subtract outside older 30% initiative range")
    return max(1,_c_int(work-random_subtract+work*0.15))


def initiative_total(dex,sequence=0,use_sequence=False):
    """Sort larger totals first."""
    return dex+(sequence if use_sequence else 0)


def effective_defense_newpower(defence_power,stone=False):
    value=defence_power*0.70
    if stone:
        value*=2.0
    return value


def effective_defense_preserved_old(defence_power,quick,fixed_vital,stone=False):
    value=defence_power*0.45+quick*0.20+fixed_vital*0.10
    if stone:
        value*=2.0
    return value


def physical_base_damage(attack,effective_defense,random_value):
    """Piecewise pre-element physical damage using a supplied RAND result."""
    if effective_defense > attack:
        if random_value not in (0,1):
            raise ValueError("random_value must be 0 or 1 below defense")
        return random_value

    if attack < effective_defense*(8.0/7.0):
        max_roll=_c_int(attack*D_16)
        if not 0 <= random_value <= max_roll:
            raise ValueError("random_value outside near-defense range")
        return random_value

    max_roll=_c_int(attack*D_8)
    if not 0 <= random_value <= max_roll:
        raise ValueError("random_value outside high-attack range")
    k0=random_value-attack*D_16
    return _c_int((attack-effective_defense)*DAMAGE_RATE+k0)


def guard_multiplier(roll_1_100):
    if not 1 <= roll_1_100 <= 100:
        raise ValueError("guard roll must be 1..100")
    if roll_1_100 <= 25:return 0.0
    if roll_1_100 <= 50:return 0.1
    if roll_1_100 <= 70:return 0.2
    if roll_1_100 <= 85:return 0.3
    if roll_1_100 <= 95:return 0.4
    return 0.5


def guard_damage(damage,roll_1_100):
    return _c_int(damage*guard_multiplier(roll_1_100))


def _relation_dex(attacker_dex,defender_dex,attacker_type,defender_type):
    at=int(attacker_dex);df=int(defender_dex)
    if attacker_type==ENEMY and defender_type==PET:
        at=_c_int(at*0.8)
    elif attacker_type!=ENEMY and defender_type==PET:
        df=_c_int(df*0.8)
    elif attacker_type!=PLAYER and defender_type==PLAYER:
        at=_c_int(at*0.6)
    elif attacker_type==PLAYER and defender_type!=PLAYER:
        df=_c_int(df*0.6)
    return at,df


def dodge_per_10000(attacker_dex,defender_dex,defender_luck=0,
                    attacker_type=PLAYER,defender_type=ENEMY,
                    battle_modifier=0,extra_percent_points=0,
                    kawashi_para=KAWASHI_PARA):
    """Stable minimal dodge core, excluding divergent bow/later-skill modifiers."""
    at,df=_relation_dex(attacker_dex,defender_dex,attacker_type,defender_type)
    if df>=at:
        big,small,wari=df,at,1.0
    else:
        big,small=at,df
        wari=0.0 if big<=0 else small/big
    work=(big-small)/kawashi_para
    if work<=0:work=0.0
    per=math.sqrt(work)*wari+defender_luck+battle_modifier+extra_percent_points
    per*=100.0
    per=min(per,KAWASHI_MAX_RATE*100)
    if per<=0:per=1
    return int(per)


def _critical_relation(attacker_dex,defender_dex,attacker_type,defender_type):
    at=int(attacker_dex);df=int(defender_dex)
    root=True;divisor=CRITICAL_PARA
    if attacker_type==PET and defender_type==ENEMY:
        df=_c_int(df*0.8)
    elif attacker_type==ENEMY and defender_type==PET:
        divisor=10.0;root=False
    elif attacker_type!=PLAYER and defender_type==PLAYER:
        divisor=10.0;root=False
    elif attacker_type==PLAYER and defender_type!=PLAYER:
        df=_c_int(df*0.6)
    return at,df,root,divisor


def critical_per_10000(attacker_dex,defender_dex,attacker_luck=0,
                       weapon_critical=0,attacker_type=PLAYER,
                       defender_type=ENEMY):
    at,df,root,divisor=_critical_relation(
        attacker_dex,defender_dex,attacker_type,defender_type)
    if at>=df:
        big,small,wari=at,df,1.0
    else:
        big,small=df,at
        wari=0.0 if big<=0 else small/big
    work=(big-small)/divisor
    if work<=0:work=0.0
    base=math.sqrt(work) if root else work
    per=(base+weapon_critical*0.5)*wari+attacker_luck
    per*=100.0
    if per<0:per=1
    if per>10000:per=10000
    return int(per)


def critical_bonus(defence_power,attacker_level,defender_level):
    if defender_level<=0:
        raise ValueError("defender_level must be positive")
    return _c_int(defence_power*(float(attacker_level)/float(defender_level))*0.5)


def raw_counter_basis(attacker_dex,defender_dex,
                      attacker_type=PLAYER,defender_type=ENEMY):
    """DEX-derived counter basis before weapon matchup/luck are applied."""
    at=int(attacker_dex);df=int(defender_dex)
    root=True;divisor=COUNTER_PARA
    if attacker_type==ENEMY and defender_type==PET:
        divisor=10.0;root=False
    elif attacker_type==PET and defender_type==ENEMY:
        df=_c_int(df*0.8)
    elif attacker_type!=PLAYER and defender_type==PLAYER:
        divisor=10.0;root=False
    elif attacker_type==PLAYER and defender_type!=PLAYER:
        df=_c_int(df*0.6)

    if at>=df:
        big,small,wari=at,df,1.0
    else:
        big,small=df,at
        wari=0.0 if big<=0 else small/big
    work=(big-small)/divisor
    if work<=0:work=0.0
    base=math.sqrt(work) if root else work
    return int(base*wari)
