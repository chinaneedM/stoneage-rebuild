"""Conditional byte-accurate 2BattleTimid reference; no original build selected."""
from dataclasses import dataclass
import math
import re
import struct

CALLBACK_NAME='PETSKILL_2BattleTimid'
COMMAND_NAME='BATTLE_COM_S_2TIMID'
FEATURE_NAME='_PETSKILL_2TIMID'
PROFILE_UTF8='utf8_literals'
PROFILE_BIG5='big5_literals'
CHARSETS={PROFILE_UTF8:'utf-8',PROFILE_BIG5:'big5'}


def _int32(value):
    if type(value) is not int or not -(2**31)<=value<2**31:
        raise ValueError('signed int32 witness required')
    return value


def _f32(value):
    result=struct.unpack('f',struct.pack('f',value))[0]
    if not math.isfinite(result):raise ValueError('finite float32 domain required')
    return result


def _raw(raw,profile):
    if profile not in CHARSETS:raise ValueError('explicit execution charset profile required')
    if not isinstance(raw,bytes) or b'\0' in raw:raise ValueError('nonnull non-NUL raw OPTION required')
    return raw,CHARSETS[profile]


def _scan(raw,integer=False):
    expr=rb'\s*([+-]?[0-9]+)' if integer else rb'\s*([+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)'
    match=re.match(expr,raw)
    if not match:return None
    return _int32(int(match.group(1))) if integer else _f32(float(match.group(1)))


@dataclass(frozen=True)
class TwoBattleTimidSetup:
    accepted:bool
    target_slot:int
    packed_com3:int
    powers:tuple[int,int,int]
    command_written:bool
    skill_written:bool
    command_name:str=COMMAND_NAME


def resolve_2battletimid_setup(raw,*,profile,target_slot,skill_array,packed_com3_before,
                              fixed_powers,powers_before,valid_actor=True):
    raw,charset=_raw(raw,profile)
    for value in (target_slot,skill_array,packed_com3_before,*fixed_powers,*powers_before):_int32(value)
    if len(fixed_powers)!=3 or len(powers_before)!=3:raise ValueError('three fixed and work powers required')
    if not valid_actor:return TwoBattleTimidSetup(False,target_slot,packed_com3_before,tuple(powers_before),False,False)
    powers=list(powers_before)
    fraction=_f32(0)
    # All six source ifs are independent. Plus overwrites minus from the same
    # fixed baseline. Failed sscanf retains the previous (already scaled) float.
    for axis,char in enumerate(('攻','防','敏')):
        for sign in ('-','+'):
            marker=(sign+char+'%').encode(charset)
            at=raw.find(marker)
            if at<0:continue
            scanned=_scan(raw[at+4:])
            if scanned is not None:fraction=scanned
            fraction=_f32(fraction/_f32(100))
            product=_f32(_f32(fixed_powers[axis])*fraction)
            result=product if sign=='-' else _f32(_f32(fixed_powers[axis])+product)
            if not -(2**31)<=result<2**31:raise ValueError('float-to-int conversion outside defined domain')
            powers[axis]=int(result)
    packed=(packed_com3_before & 0xffff0000)|(skill_array & 0xffff)
    if packed>=2**31:packed-=2**32
    return TwoBattleTimidSetup(True,target_slot,packed,tuple(powers),True,True)


def parse_2battletimid_chance(raw,*,profile):
    raw,charset=_raw(raw,profile)
    at=raw.find('命%'.encode(charset))
    if at<0:return 0
    scanned=_scan(raw[at+3:],integer=True)
    return 0 if scanned is None else scanned


@dataclass(frozen=True)
class TwoBattleTimidPost:
    chance:int
    rng_draws:int
    pet_recall_requested:bool
    pet_withdrawn:bool
    owner_default_pet_after:int
    owner_slot:int|None
    status_notifications:int
    bs_frames:int
    be_frames:int=0
    player_battle_exit:bool=False


def resolve_2battletimid_post_damage(raw,*,profile,damage,draw,target_is_pet,
                                    source_target_slot=5,default_pet_slot=2,
                                    pet_noreturn=False,active_original_reaction=False):
    _raw(raw,profile);_int32(damage);_int32(default_pet_slot)
    if damage<0:raise ValueError('nonnegative post-damage domain required')
    if active_original_reaction or damage==0:
        if draw is not None:raise ValueError('demoted event owns no 2Timid draw')
        return TwoBattleTimidPost(0,0,False,False,default_pet_slot,None,0,0)
    if type(draw) is not int or not 0<=draw<100:raise ValueError('one explicit rand()%100 witness required')
    chance=parse_2battletimid_chance(raw,profile=profile)
    requested=draw<chance and damage>1 and bool(target_is_pet)
    if requested and (type(source_target_slot) is not int or source_target_slot not in (*range(5,10),*range(15,20))):
        raise ValueError('pet target requires owner-aligned battle slot')
    withdrawn=requested and not bool(pet_noreturn)
    return TwoBattleTimidPost(chance,1,requested,withdrawn,
        -1 if withdrawn else default_pet_slot,source_target_slot-5 if requested else None,
        2 if requested else 0,1 if withdrawn else 0)
