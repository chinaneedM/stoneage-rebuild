#!/usr/bin/env python3
"""Guarded gavin/iriselia Nocast reference; not a recovered25 round executor.

No historical numeric command is emitted. Caller supplies all work resistance
and active-status state; unavailable state is never inferred as zero.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import struct

CALLBACK_NAME = "PETSKILL_Nocast"
COMMAND_NAME = "BATTLE_COM_S_NOCAST"
SUCCESS_MARKER = "成"


class NocastUndefinedSourceDomain(ValueError):
    """The fixed C path has undefined/uninitialized behavior in this domain."""


def _scanf_int(text: str) -> int | None:
    match = re.match(r"^[\t\n\v\f\r ]*([+-]?[0-9]+)", text)
    if match is None:
        return None
    value = int(match.group(1))
    if not -(2**31) <= value < 2**31:
        raise NocastUndefinedSourceDomain("sscanf integer is outside signed int32")
    return value


@dataclass(frozen=True)
class NocastOption:
    turn: int
    success_offset: int


def parse_nocast_option(option: bytes, *, encoding: str) -> NocastOption:
    """Mirror sequential strstr + sizeof(marker) + sscanf, including skip byte.

    sizeof includes the NUL, so the source skips one byte AFTER each marker.
    The success search starts at the advanced turn pointer, not OPTION start.
    Missing/invalid turn leaves C NULL/uninitialized state and is rejected.
    A missing/invalid success field retains the source's initialized zero.
    """
    if encoding not in {"cp950", "big5", "utf-8"}:
        raise ValueError("explicit supported source text encoding is required")
    raw = bytes(option).split(b"\0", 1)[0]
    raw.decode(encoding, "strict")
    start = raw.find(b"turn")
    if start < 0:
        raise NocastUndefinedSourceDomain("missing turn makes second strstr use NULL")
    tail = raw[start + len(b"turn") + 1:]
    if start + len(b"turn") + 1 > len(raw):
        raise NocastUndefinedSourceDomain("turn pointer advances beyond string NUL")
    # sscanf reads the initial ASCII number; trailing multibyte text is immaterial.
    turn = _scanf_int(tail.decode(encoding, "strict"))
    if turn is None:
        raise NocastUndefinedSourceDomain("turn is uninitialized after failed sscanf")
    marker = SUCCESS_MARKER.encode(encoding)
    found = tail.find(marker)
    success = 0
    if found >= 0:
        offset = found + len(marker) + 1
        if offset > len(tail):
            raise NocastUndefinedSourceDomain("success pointer advances beyond string NUL")
        parsed = _scanf_int(tail[offset:].decode(encoding, "strict"))
        if parsed is not None:
            success = parsed
    return NocastOption(turn, success)


def _f32(value: float | int) -> float:
    return struct.unpack("=f", struct.pack("=f", value))[0]


@dataclass(frozen=True)
class NocastCheckInputs:
    attacker_level: int
    defender_level: int
    pvp: bool
    attacker_fixed_luck: int
    defender_vital: int
    defender_strength: int
    defender_toughness: int
    defender_dexterity: int
    defender_mod_nocast: int
    defender_suit_resist: int
    # Must cover the entire compiled StatusTbl, including later statuses.
    any_existing_status: bool
    target_kind: str


def nocast_probability_value(inputs: NocastCheckInputs, success_offset: int) -> int:
    """Active gavin/iris StatusAttackCheck(status=10, Range=30, Bai=1).

    Float locals round at their C assignment boundaries. Equipment/suit-part3
    NOCAST additions do not execute: source compares status index 10 against
    work-enum IDs 51/53/54, not StatusTbl[10]. The general suit resist DOES apply.
    """
    attrs = tuple(int(x) for x in (
        inputs.defender_vital, inputs.defender_strength,
        inputs.defender_toughness, inputs.defender_dexterity,
    ))
    total = sum(attrs)
    if total <= 0 or total >= 2**31 or any(x < 0 for x in attrs):
        raise NocastUndefinedSourceDomain("requires nonnegative stats and positive int32 sum")
    share = _f32(_f32(attrs[0]) / _f32(total))
    vital_penalty = _f32(_f32(share / 0.25) * 10.0)
    level = 0 if inputs.pvp else max(-30, min(30,
        int(inputs.attacker_level) - int(inputs.defender_level)))
    subtotal = (int(success_offset) + level + int(inputs.attacker_fixed_luck)
                - int(inputs.defender_mod_nocast))
    if not -(2**31) <= subtotal < 2**31:
        raise NocastUndefinedSourceDomain("probability integer subtotal overflows int32")
    per_float = _f32(_f32(_f32(subtotal) - vital_penalty)
                     - _f32(int(inputs.defender_suit_resist)))
    if not -(2**31) <= per_float < 2**31:
        raise NocastUndefinedSourceDomain("probability float cannot convert to int32")
    return min(80, int(per_float))


@dataclass(frozen=True)
class NocastApplication:
    probability_value: int | None
    rng_consumed: bool
    hit_check_succeeded: bool
    pet_excluded: bool
    turn_written: int | None
    nc_flag: int | None
    source_return_value: bool = False


def resolve_nocast_target(inputs: NocastCheckInputs, option: NocastOption,
                          *, roll_1_100: int | None) -> NocastApplication:
    if inputs.target_kind not in {"player", "pet", "enemy", "other"}:
        raise ValueError("unknown Nocast target kind")
    if inputs.any_existing_status:
        if roll_1_100 is not None:
            raise ValueError("existing status blocks before RNG; supplied roll is unused")
        return NocastApplication(None, False, False, False, None, None)
    per = nocast_probability_value(inputs, option.success_offset)
    if roll_1_100 is None or not 1 <= int(roll_1_100) <= 100:
        raise ValueError("eligible Nocast check requires RAND(1,100)")
    hit = int(roll_1_100) < per
    excluded = hit and inputs.target_kind == "pet"
    applied = hit and not excluded
    return NocastApplication(per, True, hit, excluded,
                            option.turn if applied else None,
                            1 if applied else None)


@dataclass(frozen=True)
class NocastTick:
    counter_after: int
    nc_flag: int | None
    expired: bool


def resolve_nocast_tick(counter: int, *, weaken_active_at_visit: bool,
                        barrier_active_at_visit: bool) -> NocastTick:
    """Isolated StatusTbl[10] visit, after all earlier status visits.

    Freeze writes cnt+1 to storage but expiry still tests decremented local cnt.
    This intentionally preserves stored counter=1 plus NC(0) on that edge.
    """
    before = int(counter)
    if before <= 0:
        return NocastTick(before, None, False)
    decremented = before - 1
    after = before if (weaken_active_at_visit or barrier_active_at_visit) else decremented
    expired = decremented <= 0
    return NocastTick(after, 0 if expired else 1, expired)


def nocast_blocks_direct_magic(counter: int) -> bool:
    """MAGIC_DirectUse rejects positive WORKNOCAST before item/MP handling."""
    return int(counter) > 0


@dataclass(frozen=True)
class NocastTargetList:
    slots: tuple[int, ...]
    retarget_draws_consumed: int


def resolve_nocast_multilist(selector: int, *, alive_slots,
                             retarget_draws_0_9=()) -> NocastTargetList:
    """Gavin/iris __ATTACK_MAGIC MultiList; no preceding TargetAdjust.

    Explicit rand()%10 draws preserve the dead-single rejection loop. TARGET_ALL
    is excluded because the fixed source writes its terminator at the wrong
    index; no invented dense target list is substituted for uninitialized data.
    """
    selector = int(selector)
    alive = tuple(sorted(set(int(x) for x in alive_slots)))
    if any(not 0 <= x < 20 for x in alive):
        raise ValueError("alive slots must lie in 0..19")
    draws = tuple(int(x) for x in retarget_draws_0_9)
    if any(not 0 <= x < 10 for x in draws):
        raise ValueError("retarget draws must lie in 0..9")
    if 0 <= selector < 20:
        candidates = tuple(x for x in alive if x // 10 == selector // 10)
        if not candidates:
            raise NocastUndefinedSourceDomain("empty single-side MultiList leaves ToList uninitialized")
        if selector in alive:
            if draws:
                raise ValueError("live single target does not consume retarget draws")
            return NocastTargetList((selector,), 0)
        for index, draw in enumerate(draws):
            if draw < len(candidates):
                if index + 1 != len(draws):
                    raise ValueError("retarget draws remain after first successful draw")
                return NocastTargetList((candidates[draw],), index + 1)
        raise ValueError("dead single target requires successful explicit rand()%10 draw")
    if draws:
        raise ValueError("area selector does not consume retarget draws")
    if selector in {20, 21}:
        return NocastTargetList(tuple(x for x in alive if x // 10 == selector - 20), 0)
    rows = {23: (10, 15), 24: (15, 20), 25: (5, 10), 26: (0, 5)}
    if selector in rows:
        lo, hi = rows[selector]
        targets = tuple(x for x in alive if lo <= x < hi)
        if not targets:
            targets = tuple(x for x in alive if x // 10 == lo // 10)
        return NocastTargetList(targets, 0)
    raise NocastUndefinedSourceDomain("selector outside closed single/side/row domain")
