"""Bounded source-faithful BattleModel reference primitives.

The model captures BattleModel-specific setup and target scheduling. Common
AttackSeq/DamageSub arithmetic remains delegated to the already reconstructed
battle core; this module records only the BattleModel-specific contract around
that shared path.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import re
import struct

CALLBACK_NAME="PETSKILL_BattleModel"
COMMAND_NAME="BATTLE_COM_S_BATTLE_MODEL"
FEATURE_NAME="_PETSKILL_BATTLE_MODEL"

PROFILE_BIG5="big5_literals"
PROFILE_UTF8="utf8_literals"
CHARSETS={PROFILE_BIG5:"big5",PROFILE_UTF8:"utf-8"}

TYPE_COVER_ALL_BIT=0x00000001
TYPE_PHYSICAL_BIT=0x00000004


def _i32(value:int,name:str="value")->int:
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise ValueError(name+" must be a signed int32 witness")
    return value


def _f32(value:float)->float:
    value=struct.unpack("f",struct.pack("f",float(value)))[0]
    if not math.isfinite(value):
        raise ValueError("finite float32 domain required")
    return value


def _raw_option(raw:bytes)->bytes:
    if not isinstance(raw,bytes) or b"\0" in raw:
        raise ValueError("BattleModel OPTION must be non-NUL bytes")
    return raw


def _field(raw:bytes,index:int)->bytes|None:
    parts=raw.split(b"|")
    return parts[index-1] if 1 <= index <= len(parts) else None


def _c_atoi(raw:bytes)->int:
    match=re.match(rb"\s*([+-]?[0-9]+)",raw)
    if not match:
        return 0
    return _i32(int(match.group(1)),"atoi result")


def _scanf_float(raw:bytes)->float|None:
    match=re.match(
        rb"\s*([+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)",
        raw,
    )
    if not match:
        return None
    return _f32(float(match.group(1)))


def _pack_com2(attack_type:int,object_count:int)->int:
    attack_type=_i32(attack_type,"attack_type")
    object_count=_i32(object_count,"object_count")
    packed=(attack_type & 0xffff) | ((object_count & 0xffff) << 16)
    return packed-(1<<32) if packed >= 1<<31 else packed


@dataclass(frozen=True)
class BattleModelOptionShape:
    type_value:int
    configured_object_count:int
    status_token_bytes:int
    status_token_sha256:str
    turn_value:int|None
    hit_value:int|None
    action_numbers:tuple[int,...]
    field6_bytes:int
    field6_sha256:str
    field7_present:bool


def inspect_battlemodel_option(raw:bytes)->BattleModelOptionShape:
    """Return derived-only OPTION structure without retaining textual payload."""
    raw=_raw_option(raw)
    f1=_field(raw,1)
    f2=_field(raw,2)
    if f1 is None or f2 is None:
        raise ValueError("BattleModel OPTION requires fields 1 and 2")
    f3=_field(raw,3) or b""
    f4=_field(raw,4)
    f5=_field(raw,5)
    f6=_field(raw,6) or b""
    f7=_field(raw,7)
    actions=()
    if f7 is not None:
        tokens=f7.split(b" ")
        actions=tuple(_c_atoi(token) for token in tokens[:4] if token != b"")
    return BattleModelOptionShape(
        type_value=_c_atoi(f1),
        configured_object_count=_c_atoi(f2),
        status_token_bytes=len(f3),
        status_token_sha256=hashlib.sha256(f3).hexdigest(),
        turn_value=None if f4 is None else _c_atoi(f4),
        hit_value=None if f5 is None else _c_atoi(f5),
        action_numbers=actions,
        field6_bytes=len(f6),
        field6_sha256=hashlib.sha256(f6).hexdigest(),
        field7_present=f7 is not None,
    )


@dataclass(frozen=True)
class BattleModelSetup:
    accepted:bool
    attack_type:int
    object_count:int
    packed_com2:int
    skill_array:int
    powers:tuple[int,int,int]
    rng_draws:int
    command_written:bool
    mode_written:bool
    com2_written:bool
    com3_written:bool
    command_name:str=COMMAND_NAME


def _apply_stat_field(
    field6:bytes,
    *,
    profile:str,
    powers:tuple[int,int,int],
)->tuple[int,int,int]:
    """Reproduce the callback's positional attack-baseline stat quirk.

    The historical code reads CHAR_WORKATTACKPOWER before every axis. Because
    axis 0 can already rewrite attack power, later defence/quick percentage
    tokens observe that rewritten attack baseline.

    Source offsets +3 (percent) / +2 (absolute) are byte offsets designed for a
    two-byte Big5-family Han character. If an explicit profile reaches a
    matching token but the fixed offset cannot produce a defined float witness,
    this bounded model fails closed rather than inventing an uninitialised C
    float value.
    """
    if profile not in CHARSETS:
        raise ValueError("explicit BattleModel literal charset profile required")
    if len(powers)!=3:
        raise ValueError("attack/defence/quick work powers required")
    result=[_i32(int(v),"power") for v in powers]
    tokens=field6.split(b" ") if field6 else ()
    fper=None
    for axis,char in enumerate(("攻","防","敏")):
        if axis >= len(tokens):
            break
        token=tokens[axis]
        marker=char.encode(CHARSETS[profile])
        if marker not in token:
            continue
        value=result[0]
        if b"%" in token:
            scanned=_scanf_float(token[3:])
            if scanned is not None:
                fper=scanned
            if fper is None:
                raise ValueError(
                    "undefined fixed-byte percent scan in selected charset profile"
                )
            fper=_f32(fper/_f32(100.0))
            delta=int(_f32(_f32(value)*fper))
            result[axis]=_i32(value+delta,"adjusted power")
        else:
            scanned=_scanf_float(token[2:])
            if scanned is not None:
                fper=scanned
            if fper is None:
                raise ValueError(
                    "undefined fixed-byte absolute scan in selected charset profile"
                )
            result[axis]=_i32(int(fper),"absolute power")
    return tuple(result)


def resolve_battlemodel_setup(
    raw:bytes,
    *,
    profile:str,
    skill_array:int,
    powers_before:tuple[int,int,int],
    object_count_roll:int|None,
)->BattleModelSetup:
    """Model callback OPTION fields 1/2/6 plus COM/mode writes."""
    raw=_raw_option(raw)
    skill_array=_i32(skill_array,"skill_array")
    f1=_field(raw,1)
    f2=_field(raw,2)
    if f1 is None or f2 is None:
        return BattleModelSetup(
            False,0,0,0,skill_array,
            tuple(_i32(int(v),"power") for v in powers_before),
            0,False,False,False,False,
        )
    attack_type=_c_atoi(f1)
    configured=_c_atoi(f2)
    if configured <= 0:
        if type(object_count_roll) is not int or not 1 <= object_count_roll <= 10:
            raise ValueError("nonpositive BattleModel object count requires RAND(1,10)")
        object_count=object_count_roll
        rng_draws=1
    else:
        if object_count_roll is not None:
            raise ValueError("positive BattleModel object count owns no callback RNG")
        object_count=min(configured,10)
        rng_draws=0
    f6=_field(raw,6)
    powers=tuple(_i32(int(v),"power") for v in powers_before)
    if f6 is not None:
        powers=_apply_stat_field(f6,profile=profile,powers=powers)
    return BattleModelSetup(
        True,attack_type,object_count,_pack_com2(attack_type,object_count),
        skill_array,powers,rng_draws,True,True,True,True,
    )


@dataclass(frozen=True)
class BattleModelAttackObject:
    object_index:int
    target_slot:int
    action_number:int


@dataclass(frozen=True)
class BattleModelTargetPlan:
    attack_type:int
    object_count:int
    live_target_count:int
    attacks:tuple[BattleModelAttackObject,...]
    target_rng_draws:int
    covers_all_targets:bool


def resolve_battlemodel_target_plan(
    *,
    attack_type:int,
    object_count:int,
    living_opposing_slots:tuple[int,...],
    action_numbers:tuple[int,...],
    excess_target_rolls:tuple[int,...]=(),
)->BattleModelTargetPlan:
    """Reproduce BattleModel's unique attack-object to target scheduling.

    living_opposing_slots is the already-built BATTLE_MultiList order. R1
    deliberately does not claim that the old qsort/SortLoc presentation order
    is portable across libc implementations.
    """
    attack_type=_i32(attack_type,"attack_type")
    object_count=_i32(object_count,"object_count")
    if not 1 <= object_count <= 10:
        raise ValueError("BattleModel object_count must be 1..10 after callback")
    living=tuple(int(slot) for slot in living_opposing_slots)
    if not living:
        raise ValueError(
            "no-live-target source path reaches RAND(0,-1); R1 fails closed"
        )
    if len(living)>10 or len(set(living))!=len(living):
        raise ValueError("BattleModel living side must contain <=10 unique slots")
    for slot in living:
        _i32(slot,"target slot")
    actions=tuple(_i32(int(v),"action number") for v in action_numbers[:4])
    def action_for(index:int)->int:
        return actions[index % len(actions)] if actions else -1

    planned=[]
    n=len(living)
    first=min(object_count,n)
    for i in range(first):
        planned.append(BattleModelAttackObject(i,living[i],action_for(i)))

    rng_draws=0
    if object_count >= n:
        needed=object_count-n
        if len(excess_target_rolls)!=needed:
            raise ValueError(
                "one explicit RAND(0,living_count-1) witness required per excess object"
            )
        for offset,raw_roll in enumerate(excess_target_rolls):
            roll=int(raw_roll)
            if not 0 <= roll < n:
                raise ValueError("BattleModel excess target roll outside living list")
            obj=n+offset
            planned.append(BattleModelAttackObject(
                obj,living[roll],action_for(obj)
            ))
        rng_draws=needed
    else:
        if excess_target_rolls:
            raise ValueError("fewer-object BattleModel path owns no target RNG")
        if attack_type & TYPE_COVER_ALL_BIT:
            remaining=living[object_count:]
            for offset,target in enumerate(remaining):
                obj=offset % object_count
                planned.append(BattleModelAttackObject(
                    obj,target,action_for(obj)
                ))

    touched={item.target_slot for item in planned}
    return BattleModelTargetPlan(
        attack_type,object_count,n,tuple(planned),rng_draws,
        touched==set(living),
    )


@dataclass(frozen=True)
class BattleModelAttackContract:
    physical:bool
    guardian_redirect_enabled:bool
    damage_sub_marker_written:bool=True
    reflect_return_damage_suppressed:bool=True
    trap_return_damage_suppressed:bool=True
    acupuncture_return_damage_suppressed:bool=True


def resolve_battlemodel_attack_contract(attack_type:int)->BattleModelAttackContract:
    attack_type=_i32(attack_type,"attack_type")
    physical=bool(attack_type & TYPE_PHYSICAL_BIT)
    return BattleModelAttackContract(
        physical=physical,
        guardian_redirect_enabled=physical,
    )
