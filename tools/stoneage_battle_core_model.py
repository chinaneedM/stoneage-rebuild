#!/usr/bin/env python3
"""Independently written model of the stable StoneAge descendant battle core.

This is an archaeology/reference model, not a claim that the 1999 JSS server
used every value here. Later profession/pet-skill/private-server extensions
are deliberately excluded.
"""

import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

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
ATTR_MAX=100
AJ_SAME=1.0
AJ_UP=1.5
AJ_DOWN=0.6
D_ATTR=1.0/(ATTR_MAX*ATTR_MAX)


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



def elemental_vector(earth,water,fire,wind):
    """Return stable BATTLE_GetAttr order: earth, water, fire, wind, none."""
    values=[max(0,int(x)) for x in (earth,water,fire,wind)]
    none=max(0,ATTR_MAX-sum(values))
    return (*values,none)


def attribute_core_damage(damage,attacker_elements,defender_elements):
    """Stable BATTLE_AttrCalc without later field/property extensions.

    Elements are supplied in earth, water, fire, wind order. The source uses
    integer lvalues around floating coefficients, so each elemental subtotal
    and the final return are truncated toward zero.
    """
    if int(damage)<0:
        raise ValueError("damage must be non-negative")
    ae=elemental_vector(*attacker_elements)
    de=elemental_vector(*defender_elements)
    earth,water,fire,wind,none=ae
    dearth,dwater,dfire,dwind,dnone=de
    # BATTLE_AttrAdjust multiplies attacker element weights by base damage
    # before entering BATTLE_AttrCalc.
    fire*=int(damage)
    water*=int(damage)
    earth*=int(damage)
    wind*=int(damage)
    none*=int(damage)

    fire=_c_int(
        fire*dnone*AJ_UP + fire*dfire*AJ_SAME
        + fire*dwater*AJ_DOWN + fire*dearth*AJ_SAME
        + fire*dwind*AJ_UP
    )
    water=_c_int(
        water*dnone*AJ_UP + water*dfire*AJ_UP
        + water*dwater*AJ_SAME + water*dearth*AJ_DOWN
        + water*dwind*AJ_SAME
    )
    earth=_c_int(
        earth*dnone*AJ_UP + earth*dfire*AJ_SAME
        + earth*dwater*AJ_UP + earth*dearth*AJ_SAME
        + earth*dwind*AJ_DOWN
    )
    wind=_c_int(
        wind*dnone*AJ_UP + wind*dfire*AJ_DOWN
        + wind*dwater*AJ_SAME + wind*dearth*AJ_UP
        + wind*dwind*AJ_SAME
    )
    none=_c_int(
        none*dnone*AJ_SAME + none*dfire*AJ_DOWN
        + none*dwater*AJ_DOWN + none*dearth*AJ_DOWN
        + none*dwind*AJ_DOWN
    )
    return _c_int((fire+water+earth+wind+none)*D_ATTR)


def field_attribute_power(elements,field_attr="none",field_power=0):
    """Stable BATTLE_FieldAttAdjust scalar for one participant."""
    earth,water,fire,wind,_none=elemental_vector(*elements)
    field_power=float(field_power)
    selected={
        "earth":earth,
        "water":water,
        "fire":fire,
        "wind":wind,
    }.get(str(field_attr))
    if selected is None:
        if str(field_attr)!="none":
            raise ValueError(f"unknown field attribute: {field_attr}")
        return 0.5
    return 0.5 + selected*field_power*0.01*0.01*0.5


def attribute_adjusted_damage(
    damage,
    attacker_elements,
    defender_elements,
    *,
    field_attr="none",
    field_power=0,
):
    """Stable four-attribute adjustment with explicit battlefield attribute."""
    core=attribute_core_damage(damage,attacker_elements,defender_elements)
    at=field_attribute_power(attacker_elements,field_attr,field_power)
    df=field_attribute_power(defender_elements,field_attr,field_power)
    return _c_int(core*(at/df))


def critical_damage(
    normal_attribute_damage,
    defence_power,
    attacker_level,
    defender_level,
):
    """Stable non-bow critical additive term after normal damage calculation."""
    return int(normal_attribute_damage)+critical_bonus(
        defence_power,attacker_level,defender_level
    )


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
    """DEX-derived counter basis before weapon matchup/luck are applied.

    Stable descendants store Work in an int before sqrt/linear evaluation, so
    the division result truncates toward zero before the final wari scaling.
    """
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
    work=_c_int((big-small)/divisor)
    if work<=0:work=0
    base=math.sqrt(work) if root else work
    return int(base*wari)


COUNTER_WEAPON_FIST="fist"
COUNTER_WEAPON_AXE="axe"
COUNTER_WEAPON_CLUB="club"
COUNTER_WEAPON_SPEAR="spear"
COUNTER_WEAPON_BOW="bow"
COUNTER_WEAPON_BOOMERANG="boomerang"
COUNTER_WEAPON_BOUNDTHROW="boundthrow"
COUNTER_WEAPON_BREAKTHROW="breakthrow"
COUNTER_WEAPON_OTHER="other"

_COUNTER_WEAPON_TYPES=frozenset({
    COUNTER_WEAPON_FIST,
    COUNTER_WEAPON_AXE,
    COUNTER_WEAPON_CLUB,
    COUNTER_WEAPON_SPEAR,
    COUNTER_WEAPON_BOW,
    COUNTER_WEAPON_BOOMERANG,
    COUNTER_WEAPON_BOUNDTHROW,
    COUNTER_WEAPON_BREAKTHROW,
    COUNTER_WEAPON_OTHER,
})
_COUNTER_THROWING_WEAPONS=frozenset({
    COUNTER_WEAPON_BOW,
    COUNTER_WEAPON_BOOMERANG,
    COUNTER_WEAPON_BOUNDTHROW,
    COUNTER_WEAPON_BREAKTHROW,
})
# BATTLE_ItemType2ItemMap() in both pinned stable descendants deliberately
# omits ITEM_SPEAR despite retaining BATTLE_C_SPEAR in the enum/table. Preserve
# that source behavior: spear and unrecognized/other categories fall to NONE.
_COUNTER_WEAPON_CATEGORY=MappingProxyType({
    COUNTER_WEAPON_FIST:1,
    COUNTER_WEAPON_AXE:2,
    COUNTER_WEAPON_CLUB:3,
    COUNTER_WEAPON_SPEAR:0,
    COUNTER_WEAPON_BOW:5,
    COUNTER_WEAPON_BOOMERANG:6,
    COUNTER_WEAPON_BOUNDTHROW:6,
    COUNTER_WEAPON_BREAKTHROW:6,
    COUNTER_WEAPON_OTHER:0,
})
# Literal seven rows present in the pinned source. Category 7 (OTHER) is never
# returned by the source mapper and is therefore not invented here.
_COUNTER_WEAPON_MATCHUP=(
    (10,9,8,8,5,0,0,0),
    (10,9,7,7,6,0,0,0),
    (9,8,10,10,7,0,0,0),
    (8,8,10,10,7,0,0,0),
    (6,6,8,8,9,0,0,0),
    (0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0),
)


def _counter_weapon_type(value):
    weapon=str(value).lower()
    if weapon not in _COUNTER_WEAPON_TYPES:
        raise ValueError(f"unknown counter weapon type: {value}")
    return weapon


def counter_weapon_category(weapon_type):
    """Stable BATTLE_ItemType2ItemMap category, including the spear omission."""
    return int(_COUNTER_WEAPON_CATEGORY[_counter_weapon_type(weapon_type)])


def counter_weapon_matchup(attacker_weapon_type,defender_weapon_type):
    """Return the literal CounterTbl multiplier for two source weapon types."""
    at=counter_weapon_category(attacker_weapon_type)
    df=counter_weapon_category(defender_weapon_type)
    return int(_COUNTER_WEAPON_MATCHUP[at][df])


def counter_weapon_blocks_counter(weapon_type):
    """BATTLE_IsThrowWepon gate used by both counter-check branches."""
    return _counter_weapon_type(weapon_type) in _COUNTER_THROWING_WEAPONS


@dataclass(frozen=True)
class BattleCounterCheckInputs:
    """Stable base inputs consumed by BATTLE_CounterCheck."""

    attacker_kind: str
    defender_kind: str
    attacker_fixed_dex: int
    defender_fixed_dex: int
    attacker_fixed_luck: int = 0
    attacker_weapon_type: str = COUNTER_WEAPON_FIST
    defender_weapon_type: str = COUNTER_WEAPON_FIST

    def __post_init__(self) -> None:
        attacker_kind=str(self.attacker_kind)
        defender_kind=str(self.defender_kind)
        valid_kinds={PLAYER,PET,ENEMY,OTHER}
        if attacker_kind not in valid_kinds or defender_kind not in valid_kinds:
            raise ValueError("counter actor kind must be player/pet/enemy/other")
        object.__setattr__(self,"attacker_kind",attacker_kind)
        object.__setattr__(self,"defender_kind",defender_kind)
        object.__setattr__(self,"attacker_fixed_dex",int(self.attacker_fixed_dex))
        object.__setattr__(self,"defender_fixed_dex",int(self.defender_fixed_dex))
        object.__setattr__(self,"attacker_fixed_luck",int(self.attacker_fixed_luck))
        object.__setattr__(
            self,"attacker_weapon_type",
            _counter_weapon_type(self.attacker_weapon_type),
        )
        object.__setattr__(
            self,"defender_weapon_type",
            _counter_weapon_type(self.defender_weapon_type),
        )


@dataclass(frozen=True)
class BattleCounterCheckResolution:
    raw_basis: int
    weapon_matchup: int | None
    source_reported_percent: float
    comparison_threshold: float
    comparison: str
    rng_consumed: bool
    success: bool
    blocked_by_throwing_weapon: bool = False


def resolve_battle_counter_check(
    inputs: BattleCounterCheckInputs,
    *,
    roll_1_10000: int | None,
):
    """Mirror the stable base BATTLE_CounterCheck RNG boundary.

    Player counter actors use the source weapon matchup table plus FIXLUCK and
    the strict comparison RAND(1,10000) < threshold. Non-player actors use only
    the raw counter basis, cap it at 100 percent, and use <=. Throwing weapons
    on either side reject the counter before RNG.
    """
    if not isinstance(inputs,BattleCounterCheckInputs):
        raise TypeError("inputs must be BattleCounterCheckInputs")

    basis=raw_counter_basis(
        inputs.attacker_fixed_dex,
        inputs.defender_fixed_dex,
        attacker_type=inputs.attacker_kind,
        defender_type=inputs.defender_kind,
    )

    if (
        counter_weapon_blocks_counter(inputs.attacker_weapon_type)
        or counter_weapon_blocks_counter(inputs.defender_weapon_type)
    ):
        return BattleCounterCheckResolution(
            raw_basis=basis,
            weapon_matchup=None,
            source_reported_percent=0.0,
            comparison_threshold=0.0,
            comparison="blocked",
            rng_consumed=False,
            success=False,
            blocked_by_throwing_weapon=True,
        )

    if roll_1_10000 is None:
        raise ValueError("counter roll is required when weapon gate permits RNG")
    roll=int(roll_1_10000)
    if not 1 <= roll <= 10000:
        raise ValueError("counter roll must be 1..10000")

    if inputs.attacker_kind==PLAYER:
        matchup=counter_weapon_matchup(
            inputs.attacker_weapon_type,
            inputs.defender_weapon_type,
        )
        percent=(
            float(basis)*float(matchup)*0.1
            + float(inputs.attacker_fixed_luck)
        )
        reported=percent
        threshold=percent*100.0
        if threshold <= 0:
            threshold=1.0
            reported=0.0
        return BattleCounterCheckResolution(
            raw_basis=basis,
            weapon_matchup=matchup,
            source_reported_percent=reported,
            comparison_threshold=threshold,
            comparison="<",
            rng_consumed=True,
            success=roll < threshold,
        )

    percent=min(100.0,float(basis))
    reported=percent
    threshold=percent*100.0
    if threshold <= 0:
        threshold=1.0
        # Literal BATTLE_CounterCheckPet writes the post-threshold value back
        # through pPer, producing this odd one-at-10000 floor.
        reported=1.0
    return BattleCounterCheckResolution(
        raw_basis=basis,
        weapon_matchup=None,
        source_reported_percent=reported,
        comparison_threshold=threshold,
        comparison="<=",
        rng_consumed=True,
        success=roll <= threshold,
    )


EXP_FULL_LEVEL_ADVANTAGE=5
EXP_DECAY_WINDOW=15

PET_KILL_VARIABLE_AI_DELTA=1
PET_HIGHER_ENEMY_KILL_VARIABLE_AI_DELTA=20


@dataclass(frozen=True)
class KillProfitRecipient:
    participant_id: str
    level: int
    kind: str
    ride_pet_id: str | None = None
    ride_pet_level: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self,'participant_id',str(self.participant_id))
        object.__setattr__(self,'level',int(self.level))
        if (self.ride_pet_id is None) != (self.ride_pet_level is None):
            raise ValueError('ride pet id and level must be supplied together')
        if self.ride_pet_id is not None:
            object.__setattr__(self,'ride_pet_id',str(self.ride_pet_id))
            object.__setattr__(self,'ride_pet_level',int(self.ride_pet_level))


@dataclass(frozen=True)
class BattleKillProfit:
    direct_exp_by_participant_id: Mapping[str,int]
    ride_exp_by_participant_id: Mapping[str,int]
    pet_variable_ai_delta_by_participant_id: Mapping[str,int]
    kill_count_delta_by_participant_id: Mapping[str,int]


@dataclass(frozen=True)
class KillProfitScanEnemy:
    """One battle entry as seen by BATTLE_AddExpItem()'s death scan."""

    enemy_id: str
    level: int
    reward_exp: int
    hp: int
    is_die: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self,'enemy_id',str(self.enemy_id))
        object.__setattr__(self,'level',int(self.level))
        object.__setattr__(self,'reward_exp',int(self.reward_exp))
        object.__setattr__(self,'hp',int(self.hp))
        object.__setattr__(self,'is_die',bool(self.is_die))
        if self.reward_exp < 0:
            raise ValueError('reward_exp must be non-negative')


@dataclass(frozen=True)
class BattleKillProfitScan:
    """Aggregated EXP/loyalty result of one source-shaped profit scan."""

    claimed_enemy_ids: tuple[str,...]
    direct_exp_by_participant_id: Mapping[str,int]
    ride_exp_by_participant_id: Mapping[str,int]
    pet_variable_ai_delta_by_participant_id: Mapping[str,int]
    kill_count_delta_by_participant_id: Mapping[str,int]



def battle_exp_from_enemy(base_exp,receiver_level,enemy_level):
    """Stable descendant per-enemy EXP award before later bonus systems.

    A receiver at most 5 levels above the enemy receives full enemy EXP.
    From +6 through +19 the award declines linearly across a 15-level window.
    At +20 or more the minimum award is 1.
    """
    if base_exp < 0:
        raise ValueError("base_exp must be non-negative")
    diff=int(receiver_level)-int(enemy_level)
    if diff <= EXP_FULL_LEVEL_ADVANTAGE:
        return int(base_exp)

    factor=EXP_FULL_LEVEL_ADVANTAGE+EXP_DECAY_WINDOW-diff
    if factor > EXP_DECAY_WINDOW:
        factor=EXP_DECAY_WINDOW
    if factor <= 0:
        return 1
    award=(int(base_exp)*factor)//EXP_DECAY_WINDOW
    return max(1,award)


def ride_pet_exp_from_enemy(base_exp,ride_pet_level,enemy_level):
    """Ride-pet award: same level-gap rule, then 60% with C-style truncation.

    The source applies the 60% after the minimum-1 base calculation and does
    not re-apply the minimum, so a far-overlevel ride pet can receive 0.
    """
    award=battle_exp_from_enemy(base_exp,ride_pet_level,enemy_level)
    return int(award*0.60)


def battle_kill_profit(
    base_exp,
    enemy_level,
    attack_list: Sequence[KillProfitRecipient],
    *,
    norisk=False,
):
    '''Mirror the stable BATTLE_AddExpItem() reward loop for one newly dead enemy.

    Every entry in the attack list receives its own full level-adjusted EXP.
    A valid ride pet receives a separate award using the ride pet's own level,
    then 60% truncation. Direct pet attackers also receive the normal-risk
    VARIABLEAI kill adjustment. Item drops and later dead-extra hooks remain
    outside this pure allocation model.
    '''
    recipients=tuple(attack_list)
    if not recipients:
        raise ValueError('attack_list must contain at least one recipient')

    direct={}
    ride={}
    variable_ai={}
    kill_count={}

    def add(mapping,key,value):
        mapping[key]=mapping.get(key,0)+int(value)

    for raw in recipients:
        recipient=(
            raw
            if isinstance(raw,KillProfitRecipient)
            else KillProfitRecipient(*raw)
        )
        pid=recipient.participant_id
        add(
            direct,
            pid,
            battle_exp_from_enemy(base_exp,recipient.level,enemy_level),
        )
        add(kill_count,pid,1)

        if recipient.ride_pet_id is not None:
            add(
                ride,
                recipient.ride_pet_id,
                ride_pet_exp_from_enemy(
                    base_exp,
                    recipient.ride_pet_level,
                    enemy_level,
                ),
            )
            add(kill_count,recipient.ride_pet_id,1)

        if recipient.kind==PET and not norisk:
            delta=(
                PET_HIGHER_ENEMY_KILL_VARIABLE_AI_DELTA
                if int(enemy_level)>recipient.level
                else PET_KILL_VARIABLE_AI_DELTA
            )
            add(variable_ai,pid,delta)

    return BattleKillProfit(
        direct_exp_by_participant_id=MappingProxyType(direct),
        ride_exp_by_participant_id=MappingProxyType(ride),
        pet_variable_ai_delta_by_participant_id=MappingProxyType(variable_ai),
        kill_count_delta_by_participant_id=MappingProxyType(kill_count),
    )


def battle_kill_profit_scan(
    enemies: Sequence[KillProfitScanEnemy],
    attack_list: Sequence[KillProfitRecipient],
    *,
    norisk=False,
):
    """Mirror BATTLE_AddExpItem() scanning all unprocessed dead entries.

    The stable source does not ask which action caused each death. At every
    BATTLE_AddProfit() call it scans all battle entries and claims every entry
    with HP <= 0 and ISDIE == false for the *current* attack list, then marks
    that entry dead. This means a deferred status death can be collected by a
    later unrelated profit trigger; no original DoT/status owner is retained by
    this reward routine.

    Callers supply only reward-bearing enemy entries here. Player/PvP death,
    drops, ultimate hooks and dead-count mutation stay outside this pure EXP
    allocation model.
    """
    recipients=tuple(attack_list)
    if not recipients:
        raise ValueError('attack_list must contain at least one recipient')

    direct={}
    ride={}
    variable_ai={}
    kill_count={}
    claimed=[]
    seen=set()

    def add_all(target,source):
        for key,value in source.items():
            target[key]=target.get(key,0)+int(value)

    for raw_enemy in tuple(enemies):
        enemy=(
            raw_enemy
            if isinstance(raw_enemy,KillProfitScanEnemy)
            else KillProfitScanEnemy(*raw_enemy)
        )
        if enemy.enemy_id in seen:
            raise ValueError(f'duplicate profit-scan enemy id {enemy.enemy_id}')
        seen.add(enemy.enemy_id)
        if enemy.hp > 0 or enemy.is_die:
            continue

        profit=battle_kill_profit(
            enemy.reward_exp,
            enemy.level,
            recipients,
            norisk=norisk,
        )
        claimed.append(enemy.enemy_id)
        add_all(direct,profit.direct_exp_by_participant_id)
        add_all(ride,profit.ride_exp_by_participant_id)
        add_all(variable_ai,profit.pet_variable_ai_delta_by_participant_id)
        add_all(kill_count,profit.kill_count_delta_by_participant_id)

    return BattleKillProfitScan(
        claimed_enemy_ids=tuple(claimed),
        direct_exp_by_participant_id=MappingProxyType(direct),
        ride_exp_by_participant_id=MappingProxyType(ride),
        pet_variable_ai_delta_by_participant_id=MappingProxyType(variable_ai),
        kill_count_delta_by_participant_id=MappingProxyType(kill_count),
    )


# Stable descendant battle-drop constants.
ENEMY_DROP_SLOT_COUNT=10
BATTLE_PENDING_DROP_MAX=3
ITEMPROB_FIXED_SCALE=1000
ITEMPROB_LEGACY_SCALE=100


@dataclass(frozen=True)
class BattleDropItem:
    """Identity of an already-instantiated enemy-held item."""
    instance_id: str
    template_id: int
    view: Mapping[str,object] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self,'instance_id',str(self.instance_id))
        object.__setattr__(self,'template_id',int(self.template_id))
        object.__setattr__(
            self,
            'view',
            MappingProxyType(dict(self.view or {})),
        )
        if not self.instance_id:
            raise ValueError('drop item instance_id must not be empty')


@dataclass(frozen=True)
class DropRecipientTicket:
    """One attack-list ticket and the player entry that receives its loot."""
    participant_id: str
    player_entry_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self,'participant_id',str(self.participant_id))
        object.__setattr__(self,'player_entry_id',str(self.player_entry_id))
        if not self.participant_id or not self.player_entry_id:
            raise ValueError('drop recipient ids must not be empty')


@dataclass(frozen=True)
class DropAllocationRoll:
    """Explicit RNG consumed for one enemy-held item during profit scanning."""
    recipient_index: int
    replace_when_full: bool | None = None
    replacement_slot: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self,'recipient_index',int(self.recipient_index))
        if self.replacement_slot is not None:
            object.__setattr__(self,'replacement_slot',int(self.replacement_slot))


@dataclass(frozen=True)
class BattleDropAllocation:
    pending_by_player_entry_id: Mapping[str,tuple[BattleDropItem,...]]
    destroyed_items: tuple[BattleDropItem,...]


@dataclass(frozen=True)
class BattleDropSettlement:
    inventory_additions_by_slot: Mapping[int,BattleDropItem]
    destroyed_items: tuple[BattleDropItem,...]


def enemy_item_probability_hit(probability,roll,*,fixed_itemprob=True):
    """Resolve ITEMPROB using the selected preserved descendant branch."""
    scale=ITEMPROB_FIXED_SCALE if fixed_itemprob else ITEMPROB_LEGACY_SCALE
    probability=int(probability)
    if probability < 0 or probability > scale:
        raise ValueError(f'item probability must be in 0..{scale}')
    if probability == 0:
        if roll is not None:
            raise ValueError('zero item probability consumes no RNG roll')
        return False
    if roll is None:
        raise ValueError('non-zero item probability requires an RNG roll')
    roll=int(roll)
    if not 0 <= roll < scale:
        raise ValueError(f'item probability roll must be in 0..{scale-1}')
    return roll < probability


def allocate_battle_drop_items(
    items: Sequence[BattleDropItem],
    attack_list: Sequence[DropRecipientTicket],
    rolls: Sequence[DropAllocationRoll],
    *,
    pending_by_player_entry_id: Mapping[str,Sequence[BattleDropItem]] | None = None,
):
    """Allocate instantiated enemy items at the three-slot battle buffer seam."""
    items=tuple(
        item if isinstance(item,BattleDropItem) else BattleDropItem(*item)
        for item in items
    )
    tickets=tuple(
        ticket if isinstance(ticket,DropRecipientTicket)
        else DropRecipientTicket(*ticket)
        for ticket in attack_list
    )
    rolls=tuple(
        roll if isinstance(roll,DropAllocationRoll)
        else DropAllocationRoll(*roll)
        for roll in rolls
    )
    if not tickets:
        raise ValueError('drop attack_list must contain at least one ticket')
    if len(items) != len(rolls):
        raise ValueError('one drop allocation roll is required per item')

    pools={
        str(owner):[
            item if isinstance(item,BattleDropItem) else BattleDropItem(*item)
            for item in values
        ]
        for owner,values in (pending_by_player_entry_id or {}).items()
    }
    for owner,pool in pools.items():
        if len(pool) > BATTLE_PENDING_DROP_MAX:
            raise ValueError(
                f'pending drop pool for {owner} exceeds {BATTLE_PENDING_DROP_MAX}'
            )

    seen=set()
    for pool in pools.values():
        for item in pool:
            if item.instance_id in seen:
                raise ValueError(f'duplicate drop item instance {item.instance_id}')
            seen.add(item.instance_id)
    for item in items:
        if item.instance_id in seen:
            raise ValueError(f'duplicate drop item instance {item.instance_id}')
        seen.add(item.instance_id)

    destroyed=[]
    for item,roll in zip(items,rolls):
        if not 0 <= roll.recipient_index < len(tickets):
            raise ValueError('drop recipient_index outside attack-list range')
        owner=tickets[roll.recipient_index].player_entry_id
        pool=pools.setdefault(owner,[])
        if len(pool) < BATTLE_PENDING_DROP_MAX:
            if roll.replace_when_full is not None or roll.replacement_slot is not None:
                raise ValueError('non-full drop pool consumes no replacement RNG')
            pool.append(item)
            continue
        if roll.replace_when_full is None:
            raise ValueError('full drop pool requires RAND(0,1) replacement decision')
        if not bool(roll.replace_when_full):
            if roll.replacement_slot is not None:
                raise ValueError('discard branch consumes no replacement-slot RNG')
            destroyed.append(item)
            continue
        if roll.replacement_slot is None:
            raise ValueError('replacement branch requires RAND(0,2) slot')
        slot=int(roll.replacement_slot)
        if not 0 <= slot < BATTLE_PENDING_DROP_MAX:
            raise ValueError('replacement slot must be in 0..2')
        destroyed.append(pool[slot])
        pool[slot]=item

    return BattleDropAllocation(
        pending_by_player_entry_id=MappingProxyType(
            {owner:tuple(pool) for owner,pool in pools.items()}
        ),
        destroyed_items=tuple(destroyed),
    )


def settle_player_battle_drops(
    pending_items: Sequence[BattleDropItem],
    occupied_inventory_slots: Sequence[int],
    *,
    player_alive=True,
    inventory_slot_count=20,
):
    """Settle pending drops to first empty bag slots; destroy non-fitting items."""
    items=tuple(
        item if isinstance(item,BattleDropItem) else BattleDropItem(*item)
        for item in pending_items
    )
    if len(items) > BATTLE_PENDING_DROP_MAX:
        raise ValueError('pending battle drops exceed three-slot source buffer')
    inventory_slot_count=int(inventory_slot_count)
    if inventory_slot_count <= 0:
        raise ValueError('inventory_slot_count must be positive')
    occupied={int(slot) for slot in occupied_inventory_slots}
    if any(slot < 0 or slot >= inventory_slot_count for slot in occupied):
        raise ValueError('occupied inventory slot outside bag range')
    if not bool(player_alive):
        return BattleDropSettlement(
            inventory_additions_by_slot=MappingProxyType({}),
            destroyed_items=items,
        )

    additions={}
    destroyed=[]
    for item in items:
        empty=next(
            (slot for slot in range(inventory_slot_count) if slot not in occupied),
            None,
        )
        if empty is None:
            destroyed.append(item)
            continue
        occupied.add(empty)
        additions[empty]=item

    return BattleDropSettlement(
        inventory_additions_by_slot=MappingProxyType(additions),
        destroyed_items=tuple(destroyed),
    )


# Stable descendant capture seam.
PET_SLOT_COUNT=5


@dataclass(frozen=True)
class BattleCaptureInputs:
    """Explicit values consumed by BATTLE_CaptureCheck/PET_createPetFromCharaIndex."""
    attacker_level: int
    attacker_charm: int
    attacker_fixed_dex: int
    attacker_fixed_luck: int
    target_level: int
    target_hp: int
    target_max_hp: int
    target_fixed_dex: int
    target_capture_default: int
    target_is_enemy: bool = True
    target_capturable: bool = True
    pick_all_pet: bool = False
    temporary_capture_modifier: int = 0
    target_sleep: int = 0
    required_items_present: bool = True
    occupied_pet_slots: tuple[int,...] = ()

    def __post_init__(self) -> None:
        for name in (
            'attacker_level','attacker_charm','attacker_fixed_dex',
            'attacker_fixed_luck','target_level','target_hp','target_max_hp',
            'target_fixed_dex','target_capture_default',
            'temporary_capture_modifier','target_sleep',
        ):
            object.__setattr__(self,name,int(getattr(self,name)))
        slots=tuple(int(slot) for slot in self.occupied_pet_slots)
        if len(set(slots)) != len(slots):
            raise ValueError('occupied pet slots must be unique')
        if any(slot < 0 or slot >= PET_SLOT_COUNT for slot in slots):
            raise ValueError('occupied pet slot must be in 0..4')
        object.__setattr__(self,'occupied_pet_slots',slots)


@dataclass(frozen=True)
class BattleCaptureResolution:
    success: bool
    failure_reason: str | None
    displayed_probability: float | None
    rng_consumed: bool
    assigned_pet_slot: int | None
    capture_modifier_after: int = 0


def first_empty_pet_slot(occupied_pet_slots: Sequence[int],*,slot_count=PET_SLOT_COUNT):
    """Mirror CHAR_getCharPetElement(): ascending first-free slot or -1."""
    slot_count=int(slot_count)
    if slot_count <= 0:
        raise ValueError('pet slot count must be positive')
    occupied={int(slot) for slot in occupied_pet_slots}
    if any(slot < 0 or slot >= slot_count for slot in occupied):
        raise ValueError('occupied pet slot outside pet array')
    for slot in range(slot_count):
        if slot not in occupied:
            return slot
    return -1


def battle_capture_probability(inputs: BattleCaptureInputs) -> float:
    """Mirror stable BATTLE_CaptureCheck arithmetic without gates or RNG."""
    if not isinstance(inputs,BattleCaptureInputs):
        inputs=BattleCaptureInputs(**dict(inputs))
    max_hp=float(inputs.target_max_hp)
    if max_hp <= 0:
        max_hp=1.0
    hp=float(inputs.target_hp)
    hp_term=10.0-(hp*hp)/max_hp
    level_term=float(inputs.attacker_level)/2.0-float(inputs.target_level)/2.0
    dex_term=float(inputs.attacker_fixed_dex)/15.0-float(inputs.target_fixed_dex)/15.0
    work=(
        hp_term+level_term+dex_term
        +float(inputs.target_capture_default+inputs.attacker_fixed_luck)
    )*float(inputs.attacker_charm)/50.0
    work+=float(inputs.temporary_capture_modifier)
    if inputs.target_sleep > 0:
        work+=15.0
    if work > 99.0:
        work=99.0
    return work


def resolve_battle_capture_attempt(
    inputs: BattleCaptureInputs,
    *,
    roll_1_100: int | None,
) -> BattleCaptureResolution:
    """Resolve capture gates, RNG order and the later five-slot capacity check."""
    if not isinstance(inputs,BattleCaptureInputs):
        inputs=BattleCaptureInputs(**dict(inputs))

    def failed(reason,probability=None,rng=False):
        return BattleCaptureResolution(
            False,reason,probability,rng,None,0
        )

    if not inputs.required_items_present:
        if roll_1_100 is not None:
            raise ValueError('missing required capture item consumes no capture RNG')
        return failed('missing_required_items')
    if not inputs.target_is_enemy:
        if roll_1_100 is not None:
            raise ValueError('non-enemy capture target consumes no capture RNG')
        return failed('target_not_enemy',0.0)
    if not inputs.target_capturable:
        if roll_1_100 is not None:
            raise ValueError('PETFLG=0 capture target consumes no capture RNG')
        return failed('target_not_capturable',0.0)
    if not inputs.pick_all_pet and inputs.attacker_level+5 < inputs.target_level:
        if roll_1_100 is not None:
            raise ValueError('level-gated capture consumes no capture RNG')
        return failed('target_level_too_high',0.0)

    probability=battle_capture_probability(inputs)
    if roll_1_100 is None:
        raise ValueError('eligible capture attempt requires RAND(1,100) result')
    roll=int(roll_1_100)
    if not 1 <= roll <= 100:
        raise ValueError('capture roll must be in 1..100')
    if not roll < probability:
        return failed('capture_roll_failed',probability,True)

    slot=first_empty_pet_slot(inputs.occupied_pet_slots)
    if slot < 0:
        return failed('pet_slots_full',probability,True)
    return BattleCaptureResolution(True,None,probability,True,slot,0)


@dataclass(frozen=True)
class BattleEscapeInputs:
    """Explicit values consumed by stable BATTLE_Escape/BATTLE_EscapeCheck."""
    actor_level: int
    actor_kind: str
    actor_fixed_luck: int = 1
    actor_rare: int = 0
    stored_escape_count_before: int = 0
    opponent_levels: tuple[int,...] = ()
    opponent_abio_flags: tuple[bool,...] = ()
    pvp: bool = False
    forced_exit: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self,'actor_level',int(self.actor_level))
        object.__setattr__(self,'actor_kind',str(self.actor_kind))
        object.__setattr__(self,'actor_fixed_luck',int(self.actor_fixed_luck))
        object.__setattr__(self,'actor_rare',int(self.actor_rare))
        count=int(self.stored_escape_count_before)
        if count < 0:
            raise ValueError('stored escape count cannot be negative')
        object.__setattr__(self,'stored_escape_count_before',count)
        levels=tuple(int(value) for value in self.opponent_levels)
        flags=tuple(bool(value) for value in self.opponent_abio_flags)
        if flags and len(flags) != len(levels):
            raise ValueError('opponent ABIO flags must match opponent levels')
        if not flags:
            flags=(False,)*len(levels)
        object.__setattr__(self,'opponent_levels',levels)
        object.__setattr__(self,'opponent_abio_flags',flags)
        if self.actor_kind not in {'player','enemy'}:
            raise ValueError('ordinary escape actor must be player or enemy')


@dataclass(frozen=True)
class BattleEscapeResolution:
    check_success: bool
    exits_battle: bool
    probability: int | None
    rng_consumed: bool
    stored_escape_count_after: int
    effective_escape_count: int
    effective_luck: int | None
    average_opponent_level: int | None


def _c_trunc_div(numerator: int,denominator: int) -> int:
    """C99-style integer division truncating toward zero."""
    if int(denominator) == 0:
        raise ZeroDivisionError('integer division by zero')
    return int(int(numerator)/int(denominator))


def resolve_battle_escape_attempt(
    inputs: BattleEscapeInputs,
    *,
    roll_1_100: int | None,
) -> BattleEscapeResolution:
    """Mirror stable BATTLE_Escape() then BATTLE_EscapeCheck() ordering.

    The source increments entry.escape first, then EscapeCheck uses escape+1.
    Since battle-entry initialization sets escape=0, an ordinary first attempt
    therefore uses an effective multiplier of 2. This apparently redundant
    increment is preserved rather than normalized away.
    """
    if not isinstance(inputs,BattleEscapeInputs):
        inputs=BattleEscapeInputs(**dict(inputs))

    stored_after=inputs.stored_escape_count_before+1
    effective_count=stored_after+1

    if inputs.pvp:
        if roll_1_100 is not None:
            raise ValueError('PvP escape check returns before consuming RNG')
        return BattleEscapeResolution(
            check_success=True,
            exits_battle=True,
            probability=None,
            rng_consumed=False,
            stored_escape_count_after=stored_after,
            effective_escape_count=effective_count,
            effective_luck=None,
            average_opponent_level=None,
        )

    if inputs.actor_kind == 'enemy':
        if inputs.actor_rare == 0:
            luck=1
        elif inputs.actor_rare == 1:
            luck=3
        else:
            luck=5
    else:
        luck=min(5,max(1,int(inputs.actor_fixed_luck)))

    if not inputs.opponent_levels:
        average=0
        chance=100
    else:
        total=0
        for level,abio in zip(
            inputs.opponent_levels,
            inputs.opponent_abio_flags,
        ):
            if abio:
                total-=100
            total+=int(level)
        average=_c_trunc_div(total,len(inputs.opponent_levels))
        if luck >= 5:
            chance=95*effective_count
        else:
            base={4:60,3:50,2:40,1:30}[luck]
            chance=base*effective_count-2*(average-inputs.actor_level)
    if chance < 1:
        chance=1

    if roll_1_100 is None:
        raise ValueError('non-PvP escape check requires RAND(1,100) result')
    roll=int(roll_1_100)
    if not 1 <= roll <= 100:
        raise ValueError('escape roll must be in 1..100')
    check_success=roll < chance
    return BattleEscapeResolution(
        check_success=check_success,
        exits_battle=(check_success or bool(inputs.forced_exit)),
        probability=int(chance),
        rng_consumed=True,
        stored_escape_count_after=stored_after,
        effective_escape_count=effective_count,
        effective_luck=luck,
        average_opponent_level=average,
    )


CH_FIX_PLAYERDEAD=-2
AI_FIX_PLAYERDEAD=-100
AI_FIX_PETDEAD=-500

CH_FIX_PLAYERULTIMATE=-4
AI_FIX_PLAYERULTIMATE=-1000
AI_FIX_PETULTIMATE=-1000


@dataclass(frozen=True)
class BattleUltimateDamageInputs:
    """Stable BATTLE_DamageSub/BATTLE_DamageSub2 ultimate accumulator inputs.

    damage_for_threshold is the source's pre-HP-settlement damage value.
    hp_damage_applied is the actual HP subtraction applied to the resolved
    damage target (for ride splitting / reflection these can differ).
    """

    damage_for_threshold: int
    hp_damage_applied: int
    target_hp_before: int
    target_max_hp: int
    accumulated_overkill_before: int = 0

    def __post_init__(self) -> None:
        for name in (
            "damage_for_threshold",
            "hp_damage_applied",
            "target_hp_before",
            "target_max_hp",
            "accumulated_overkill_before",
        ):
            value=int(getattr(self,name))
            if value < 0:
                raise ValueError(f"{name} cannot be negative")
            object.__setattr__(self,name,value)
        if self.target_max_hp <= 0:
            raise ValueError("target_max_hp must be positive")
        if self.target_hp_before > self.target_max_hp:
            raise ValueError("target_hp_before cannot exceed target_max_hp")


@dataclass(frozen=True)
class BattleUltimateDamageResolution:
    ultimate_kind: int
    threshold_times_five: int
    overkill_damage: int
    accumulated_overkill_after: int

    def __post_init__(self) -> None:
        if int(self.ultimate_kind) not in {0,1,2}:
            raise ValueError("ultimate_kind must be 0, 1 or 2")


def resolve_battle_ultimate_damage(
    inputs: BattleUltimateDamageInputs,
) -> BattleUltimateDamageResolution:
    """Mirror stable maxHP*1.2+20 threshold and WORKULTIMATE accumulation."""

    if not isinstance(inputs,BattleUltimateDamageInputs):
        inputs=BattleUltimateDamageInputs(**dict(inputs))

    threshold5=int(inputs.target_max_hp)*6+100
    overkill=max(
        0,
        int(inputs.hp_damage_applied)-int(inputs.target_hp_before),
    )

    if int(inputs.damage_for_threshold)*5 >= threshold5:
        return BattleUltimateDamageResolution(
            ultimate_kind=2,
            threshold_times_five=threshold5,
            overkill_damage=overkill,
            accumulated_overkill_after=0,
        )

    accumulated=int(inputs.accumulated_overkill_before)
    if overkill > 0:
        accumulated+=overkill
        if accumulated*5 >= threshold5:
            return BattleUltimateDamageResolution(
                ultimate_kind=1,
                threshold_times_five=threshold5,
                overkill_damage=overkill,
                accumulated_overkill_after=0,
            )

    return BattleUltimateDamageResolution(
        ultimate_kind=0,
        threshold_times_five=threshold5,
        overkill_damage=overkill,
        accumulated_overkill_after=accumulated,
    )


@dataclass(frozen=True)
class BattleDeathUltimateInputs:
    """Post-damage dead-target override from the ordinary Attack path."""

    base_ultimate_kind: int
    victim_kind: str
    abio: bool = False
    critical: bool = False

    def __post_init__(self) -> None:
        kind=int(self.base_ultimate_kind)
        if kind not in {0,1,2}:
            raise ValueError("base_ultimate_kind must be 0, 1 or 2")
        object.__setattr__(self,"base_ultimate_kind",kind)
        object.__setattr__(self,"victim_kind",str(self.victim_kind))
        object.__setattr__(self,"abio",bool(self.abio))
        object.__setattr__(self,"critical",bool(self.critical))


@dataclass(frozen=True)
class BattleDeathUltimateResolution:
    ultimate_kind: int
    critical_roll_consumed: bool = False


def resolve_battle_death_ultimate_override(
    inputs: BattleDeathUltimateInputs,
    *,
    critical_roll_1_100: int | None = None,
) -> BattleDeathUltimateResolution:
    """Apply dead-target ABIO / non-player critical ultimate override."""

    if not isinstance(inputs,BattleDeathUltimateInputs):
        inputs=BattleDeathUltimateInputs(**dict(inputs))

    if inputs.abio:
        if critical_roll_1_100 is not None:
            raise ValueError("ABIO ultimate override does not consume critical RNG")
        return BattleDeathUltimateResolution(1,False)

    if inputs.victim_kind != PLAYER and inputs.critical:
        if critical_roll_1_100 is None:
            raise ValueError("non-player critical death requires RAND(1,100)")
        roll=int(critical_roll_1_100)
        if not 1 <= roll <= 100:
            raise ValueError("critical death ultimate roll must be in 1..100")
        return BattleDeathUltimateResolution(
            1 if roll < 50 else int(inputs.base_ultimate_kind),
            True,
        )

    if critical_roll_1_100 is not None:
        raise ValueError("critical death ultimate RNG supplied on unused path")
    return BattleDeathUltimateResolution(int(inputs.base_ultimate_kind),False)


@dataclass(frozen=True)
class BattleUltimateDeathInputs:
    """Stable BATTLE_UltimateExtra PvE penalty subset."""

    victim_kind: str
    victim_level: int
    owner_level: int | None = None
    pve_battle: bool = True
    no_risk: bool = False
    default_pet_present: bool = False

    def __post_init__(self) -> None:
        kind=str(self.victim_kind)
        object.__setattr__(self,"victim_kind",kind)
        object.__setattr__(self,"victim_level",int(self.victim_level))
        if self.owner_level is not None:
            object.__setattr__(self,"owner_level",int(self.owner_level))
        if kind == PET and self.owner_level is None:
            raise ValueError("pet ultimate penalty requires owner_level")


@dataclass(frozen=True)
class BattleUltimateDeathResolution:
    player_charm_delta: int = 0
    default_pet_variable_ai_delta: int = 0
    victim_pet_variable_ai_delta: int = 0
    owner_dead_pet_count_delta: int = 0
    clears_owner_default_pet: bool = False
    exits_victim_battle: bool = True


def resolve_battle_ultimate_death_penalty(
    inputs: BattleUltimateDeathInputs,
) -> BattleUltimateDeathResolution:
    """Mirror base player/pet PvE penalties in BATTLE_UltimateExtra."""

    if not isinstance(inputs,BattleUltimateDeathInputs):
        inputs=BattleUltimateDeathInputs(**dict(inputs))

    if inputs.victim_kind == PLAYER:
        if not inputs.pve_battle or inputs.no_risk:
            return BattleUltimateDeathResolution()
        level_divisor=2 if int(inputs.victim_level) <= 10 else 1
        return BattleUltimateDeathResolution(
            player_charm_delta=int(CH_FIX_PLAYERULTIMATE/level_divisor),
            default_pet_variable_ai_delta=(
                int(AI_FIX_PLAYERULTIMATE/level_divisor)
                if inputs.default_pet_present
                else 0
            ),
        )

    if inputs.victim_kind == PET:
        level_divisor=2 if int(inputs.owner_level) <= 10 else 1
        if not inputs.pve_battle:
            return BattleUltimateDeathResolution(
                clears_owner_default_pet=True,
            )
        if inputs.no_risk:
            return BattleUltimateDeathResolution(
                owner_dead_pet_count_delta=1,
                clears_owner_default_pet=True,
            )
        return BattleUltimateDeathResolution(
            victim_pet_variable_ai_delta=int(
                AI_FIX_PETULTIMATE/level_divisor
            ),
            owner_dead_pet_count_delta=1,
            clears_owner_default_pet=True,
        )

    return BattleUltimateDeathResolution()

@dataclass(frozen=True)
class BattleNormalDeathInputs:
    """Stable BATTLE_NormalDeadExtra inputs kept separate from final defeat."""

    victim_kind: str
    victim_level: int
    owner_level: int | None = None
    pve_battle: bool = True
    no_risk: bool = False
    default_pet_present: bool = False

    def __post_init__(self) -> None:
        kind=str(self.victim_kind)
        object.__setattr__(self,"victim_kind",kind)
        object.__setattr__(self,"victim_level",int(self.victim_level))
        if self.owner_level is not None:
            object.__setattr__(self,"owner_level",int(self.owner_level))
        if kind == PET and self.owner_level is None:
            raise ValueError("pet normal-death penalty requires owner_level")


@dataclass(frozen=True)
class BattleNormalDeathResolution:
    player_charm_delta: int = 0
    default_pet_variable_ai_delta: int = 0
    victim_pet_variable_ai_delta: int = 0
    owner_dead_pet_count_delta: int = 0
    clears_victim_command: bool = False


def resolve_battle_normal_death_penalty(
    inputs: BattleNormalDeathInputs,
) -> BattleNormalDeathResolution:
    """Mirror the stable PvE/non-norisk BATTLE_NormalDeadExtra side effects."""

    if not isinstance(inputs,BattleNormalDeathInputs):
        inputs=BattleNormalDeathInputs(**dict(inputs))

    if not inputs.pve_battle or inputs.no_risk:
        return BattleNormalDeathResolution()

    if inputs.victim_kind == PLAYER:
        level_divisor=2 if int(inputs.victim_level) <= 10 else 1
        charm=int(CH_FIX_PLAYERDEAD/level_divisor)
        active_pet=(
            int(AI_FIX_PLAYERDEAD/level_divisor)
            if inputs.default_pet_present
            else 0
        )
        return BattleNormalDeathResolution(
            player_charm_delta=charm,
            default_pet_variable_ai_delta=active_pet,
            clears_victim_command=True,
        )

    if inputs.victim_kind == PET:
        level_divisor=2 if int(inputs.owner_level) <= 10 else 1
        return BattleNormalDeathResolution(
            victim_pet_variable_ai_delta=int(AI_FIX_PETDEAD/level_divisor),
            owner_dead_pet_count_delta=1,
            clears_victim_command=True,
        )

    return BattleNormalDeathResolution()
