#!/usr/bin/env python3
"""Guarded fixed-source model for PETSKILL_Barrier.

The model keeps source status-index and work-enum domains separate. In the
pinned descendants BATTLE_ST_BARRIER is a small StatusTbl index while
CHAR_WORKBARRIER is a work-field enum, so nominal status==CHAR_WORKBARRIER
equipment-specific branches are not assumed to execute.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import struct


CALLBACK_NAME="PETSKILL_Barrier"
COMMAND_NAME="BATTLE_COM_S_BARRIER"
FEATURE_NAME="_SKILL_BARRIER"
MAGIC_FEATURE_NAME="_MAGIC_BARRIER"
SOURCE_PETSKILL_SYMBOL_NAME="PETSKILL_BARRIER"
SUCCESS_MARKER="成"


class BarrierUndefinedSourceDomain(ValueError):
    """The pinned C path is undefined/uninitialized for this input."""


def _scanf_int(text:str) -> int | None:
    match=re.match(r"^[\t\n\v\f\r ]*([+-]?[0-9]+)",text)
    if match is None:
        return None
    value=int(match.group(1))
    if not -(2**31) <= value < 2**31:
        raise BarrierUndefinedSourceDomain(
            "sscanf integer is outside signed int32"
        )
    return value


@dataclass(frozen=True)
class BarrierOption:
    turn: int
    success_offset: int


def parse_barrier_option(option:bytes,*,encoding:str) -> BarrierOption:
    """Mirror sequential strstr/sizeof/sscanf used by BATTLE_S_Barrier."""
    if encoding not in {"cp950","big5","utf-8"}:
        raise ValueError("explicit supported source text encoding is required")
    raw=bytes(option).split(b"\0",1)[0]
    raw.decode(encoding,"strict")
    start=raw.find(b"turn")
    if start < 0:
        raise BarrierUndefinedSourceDomain(
            "missing turn makes the later strstr use NULL"
        )
    offset=start+len(b"turn")+1
    if offset > len(raw):
        raise BarrierUndefinedSourceDomain(
            "turn pointer advances beyond string NUL"
        )
    tail=raw[offset:]
    turn=_scanf_int(tail.decode(encoding,"strict"))
    if turn is None:
        raise BarrierUndefinedSourceDomain(
            "turn is uninitialized after failed sscanf"
        )
    success=0
    marker=SUCCESS_MARKER.encode(encoding)
    found=tail.find(marker)
    if found >= 0:
        success_offset=found+len(marker)+1
        if success_offset > len(tail):
            raise BarrierUndefinedSourceDomain(
                "success pointer advances beyond string NUL"
            )
        parsed=_scanf_int(tail[success_offset:].decode(encoding,"strict"))
        if parsed is not None:
            success=parsed
    return BarrierOption(turn=turn,success_offset=success)


def _f32(value:float|int) -> float:
    return struct.unpack("=f",struct.pack("=f",value))[0]


@dataclass(frozen=True)
class BarrierCheckInputs:
    attacker_level: int
    defender_level: int
    pvp: bool
    attacker_fixed_luck: int
    defender_vital: int
    defender_strength: int
    defender_toughness: int
    defender_dexterity: int
    defender_mod_barrier: int
    defender_suit_resist: int
    any_existing_status: bool


def barrier_probability_value(
    inputs:BarrierCheckInputs,
    success_offset:int,
) -> int:
    """Pinned BATTLE_StatusAttackCheck(status=BARRIER, Range=30, Bai=1)."""
    attrs=tuple(int(x) for x in (
        inputs.defender_vital,
        inputs.defender_strength,
        inputs.defender_toughness,
        inputs.defender_dexterity,
    ))
    total=sum(attrs)
    if total <= 0 or total >= 2**31 or any(x < 0 for x in attrs):
        raise BarrierUndefinedSourceDomain(
            "requires nonnegative stats and positive int32 sum"
        )
    share=_f32(_f32(attrs[0])/_f32(total))
    vital_penalty=_f32(_f32(share/0.25)*10.0)
    level=0 if inputs.pvp else max(
        -30,
        min(30,int(inputs.attacker_level)-int(inputs.defender_level)),
    )
    subtotal=(
        int(success_offset)
        + level
        + int(inputs.attacker_fixed_luck)
        - int(inputs.defender_mod_barrier)
    )
    if not -(2**31) <= subtotal < 2**31:
        raise BarrierUndefinedSourceDomain(
            "probability integer subtotal overflows int32"
        )
    per_float=_f32(
        _f32(_f32(subtotal)-vital_penalty)
        - _f32(int(inputs.defender_suit_resist))
    )
    if not -(2**31) <= per_float < 2**31:
        raise BarrierUndefinedSourceDomain(
            "probability float cannot convert to int32"
        )
    return min(80,int(per_float))


@dataclass(frozen=True)
class BarrierApplication:
    probability_value: int | None
    rng_consumed: bool
    hit_check_succeeded: bool
    counter_written: int | None
    source_return_value: bool = False


def resolve_barrier_target(
    inputs:BarrierCheckInputs,
    option:BarrierOption,
    *,
    roll_1_100:int|None,
) -> BarrierApplication:
    if inputs.any_existing_status:
        if roll_1_100 is not None:
            raise ValueError(
                "existing status blocks Barrier before RNG; roll is unused"
            )
        return BarrierApplication(None,False,False,None)
    per=barrier_probability_value(inputs,option.success_offset)
    if roll_1_100 is None or not 1 <= int(roll_1_100) <= 100:
        raise ValueError("eligible Barrier check requires RAND(1,100)")
    hit=int(roll_1_100) < per
    return BarrierApplication(
        probability_value=per,
        rng_consumed=True,
        hit_check_succeeded=hit,
        counter_written=(int(option.turn)+1 if hit else None),
    )


@dataclass(frozen=True)
class BarrierSelfTick:
    counter_before: int
    decremented_local_counter: int
    counter_after: int
    expired: bool
    self_freeze_restored_storage: bool


def resolve_barrier_self_tick(
    counter:int,
    *,
    weaken_active_at_visit:bool=False,
) -> BarrierSelfTick:
    """Mirror Barrier's own StatusTbl[9] visit.

    StatusSeq decrements local cnt first. Active WEAKEN may immediately write
    cnt+1 back; then active BARRIER may do the same. Expiry still tests the
    decremented local cnt, so counter=1 with WEAKEN active can report expiry
    while storage is restored to 1. Without WEAKEN, any counter above one
    self-freezes indefinitely while counter=1 reaches stored zero.
    """
    before=int(counter)
    if before <= 0:
        return BarrierSelfTick(before,before,before,False,False)
    decremented=before-1
    restored=bool(weaken_active_at_visit) or decremented > 0
    after=before if restored else decremented
    return BarrierSelfTick(
        counter_before=before,
        decremented_local_counter=decremented,
        counter_after=after,
        expired=(decremented <= 0),
        self_freeze_restored_storage=restored,
    )


def barrier_blocks_action(counter:int) -> bool:
    return int(counter) > 0


@dataclass(frozen=True)
class BarrierTargetList:
    slots: tuple[int,...]
    retarget_draws_consumed: int


def resolve_barrier_multilist(
    selector:int,
    *,
    alive_slots,
    retarget_draws_0_9=(),
) -> BarrierTargetList:
    """Pinned BATTLE_MultiList closed single/side/row domain."""
    selector=int(selector)
    alive=tuple(sorted(set(int(x) for x in alive_slots)))
    if any(not 0 <= x < 20 for x in alive):
        raise ValueError("alive slots must lie in 0..19")
    draws=tuple(int(x) for x in retarget_draws_0_9)
    if any(not 0 <= x < 10 for x in draws):
        raise ValueError("retarget draws must lie in 0..9")
    if 0 <= selector < 20:
        candidates=tuple(x for x in alive if x//10==selector//10)
        if not candidates:
            raise BarrierUndefinedSourceDomain(
                "empty single-side MultiList leaves ToList uninitialized"
            )
        if selector in alive:
            if draws:
                raise ValueError(
                    "live single target does not consume retarget draws"
                )
            return BarrierTargetList((selector,),0)
        for index,draw in enumerate(draws):
            if draw < len(candidates):
                if index+1 != len(draws):
                    raise ValueError(
                        "retarget draws remain after first successful draw"
                    )
                return BarrierTargetList((candidates[draw],),index+1)
        raise ValueError(
            "dead single target requires successful explicit rand()%10 draw"
        )
    if draws:
        raise ValueError("area selector does not consume retarget draws")
    if selector in {20,21}:
        return BarrierTargetList(
            tuple(x for x in alive if x//10==selector-20),
            0,
        )
    rows={23:(10,15),24:(15,20),25:(5,10),26:(0,5)}
    if selector in rows:
        lo,hi=rows[selector]
        targets=tuple(x for x in alive if lo <= x < hi)
        if not targets:
            targets=tuple(x for x in alive if x//10==lo//10)
        return BarrierTargetList(targets,0)
    raise BarrierUndefinedSourceDomain(
        "selector outside closed single/side/row domain"
    )
