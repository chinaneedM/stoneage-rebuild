"""Safe, version-tagged PETSKILL_Weaken reference, without numeric COM1.

Only the leading WEAKEN-marker domain is admitted. Arbitrary status scans and
unverified descendant encoding/build identities remain outside this reference.
"""
from dataclasses import dataclass

from tools.stoneage_nocast_model import (
    NocastCheckInputs, _scanf_int, _f32, nocast_probability_value,
    resolve_nocast_multilist,
)
from tools.stoneage_barrier_model import resolve_barrier_self_tick

CALLBACK_NAME = "PETSKILL_Weaken"
COMMAND_NAME = "BATTLE_COM_S_WEAKEN"


class WeakenUndefinedSourceDomain(ValueError):
    """Unverified or undefined fixed-source input."""


@dataclass(frozen=True)
class WeakenOption:
    turn: int
    success_offset: int
    status_index: int = 7


def parse_weaken_option(option: bytes, *, encoding: str,
                        simplified_utf8: bool = False) -> WeakenOption:
    if encoding not in {"cp950", "big5", "utf-8"}:
        raise ValueError("explicit supported encoding is required")
    if simplified_utf8 and encoding != "utf-8":
        raise ValueError("simplified profile is admitted only for UTF-8 source")
    raw = bytes(option)
    if b"\0" in raw:
        raise WeakenUndefinedSourceDomain("embedded NUL is outside admitted OPTION")
    raw.decode(encoding, "strict")
    marker = ("虚" if simplified_utf8 else "虛").encode(encoding)
    # The C scanner compares TWO bytes, adds two, then the for-loop adds one.
    # This consumes the UTF-8 character, or a Big5 character plus one byte.
    if not raw.startswith(marker):
        raise WeakenUndefinedSourceDomain("requires leading verified WEAKEN marker")
    tail = raw[3:]
    found = tail.find(b"turn")
    if found < 0:
        raise WeakenUndefinedSourceDomain("missing turn makes second strstr use NULL")
    offset = found + 5
    if offset > len(tail):
        raise WeakenUndefinedSourceDomain("turn pointer advances beyond string NUL")
    # Unlike Nocast/Barrier, Weaken initializes turn=3 before sscanf.
    turn = _scanf_int(tail[offset:].decode("latin-1"))
    if turn is None:
        turn = 3
    success = 0
    remaining = tail[offset:]
    success_marker = "成".encode(encoding)
    found = remaining.find(success_marker)
    if found >= 0:
        offset = found + len(success_marker) + 1
        if offset > len(remaining):
            raise WeakenUndefinedSourceDomain("success pointer advances beyond string NUL")
        value = _scanf_int(remaining[offset:].decode("latin-1"))
        if value is not None:
            success = value
    if not -(2**31) <= turn < 2**31 - 1:
        raise WeakenUndefinedSourceDomain("turn+1 would overflow signed int32")
    return WeakenOption(turn, success)


@dataclass(frozen=True)
class WeakenCheckInputs:
    attacker_level: int
    defender_level: int
    pvp: bool
    attacker_fixed_luck: int
    defender_vital: int
    defender_strength: int
    defender_toughness: int
    defender_dexterity: int
    defender_mod_weaken: int
    defender_suit_resist: int
    any_existing_status: bool
    target_kind: str


def weaken_probability_value(inputs: WeakenCheckInputs, success_offset: int) -> int:
    for value in (success_offset, inputs.attacker_level, inputs.defender_level,
                  inputs.attacker_fixed_luck, inputs.defender_mod_weaken,
                  inputs.defender_suit_resist):
        if not -(2**31) <= int(value) < 2**31:
            raise WeakenUndefinedSourceDomain("requires signed int32 inputs")
    delta = inputs.attacker_level - inputs.defender_level
    if not inputs.pvp and not -(2**31) <= delta < 2**31:
        raise WeakenUndefinedSourceDomain("level subtraction overflows signed int32")
    if not inputs.pvp and not -(2**31) <= _f32(delta) < 2**31:
        raise WeakenUndefinedSourceDomain("level *= float Bai cannot convert to int32")
    level = 0 if inputs.pvp else max(-30, min(30, delta))
    subtotal = int(success_offset)
    for term in (level, inputs.attacker_fixed_luck, -inputs.defender_mod_weaken):
        subtotal += term
        if not -(2**31) <= subtotal < 2**31:
            raise WeakenUndefinedSourceDomain("probability intermediate overflows int32")
    # Status 7 follows the same closed, non-paralysis formula as status 10.
    # Status-specific equipment branches compare against WORK enums, not 7.
    return nocast_probability_value(NocastCheckInputs(
        inputs.attacker_level, inputs.defender_level, inputs.pvp,
        inputs.attacker_fixed_luck, inputs.defender_vital,
        inputs.defender_strength, inputs.defender_toughness,
        inputs.defender_dexterity, inputs.defender_mod_weaken,
        inputs.defender_suit_resist, inputs.any_existing_status,
        inputs.target_kind,
    ), success_offset)


@dataclass(frozen=True)
class WeakenApplication:
    probability_value: int | None
    rng_consumed: bool
    hit_check_succeeded: bool
    counter_written: int | None
    source_return_value: bool = False


def resolve_weaken_target(inputs: WeakenCheckInputs, option: WeakenOption,
                          *, roll_1_100: int | None) -> WeakenApplication:
    if inputs.target_kind not in {"player", "pet", "enemy", "other"}:
        raise ValueError("unknown target kind")
    if option.status_index != 7:
        raise WeakenUndefinedSourceDomain("only WEAKEN status index is admitted")
    if not -(2**31) <= option.turn < 2**31 - 1:
        raise WeakenUndefinedSourceDomain("turn+1 would overflow signed int32")
    if inputs.any_existing_status:
        if roll_1_100 is not None:
            raise ValueError("existing status blocks before RNG")
        return WeakenApplication(None, False, False, None)
    per = weaken_probability_value(inputs, option.success_offset)
    if roll_1_100 is None or not 1 <= roll_1_100 <= 100:
        raise ValueError("eligible check requires RAND(1,100)")
    hit = roll_1_100 < per
    # Shared MultiParamChangeTurn writes turn+1, including PET targets.
    return WeakenApplication(per, True, hit, option.turn + 1 if hit else None)


def resolve_weaken_self_tick(counter: int, *, barrier_active_at_visit: bool = False):
    """Same decrement/self-freeze/expiry primitive already used for Barrier.

    WEAKEN precedes BARRIER and NOCAST. A counter above one restores itself;
    one reaches zero unless BARRIER restores storage, even as local expiry fires.
    """
    return resolve_barrier_self_tick(counter,
                                   weaken_active_at_visit=barrier_active_at_visit)


resolve_weaken_multilist = resolve_nocast_multilist


@dataclass(frozen=True)
class WeakenRecalculation:
    strength: int
    toughness: int
    dexterity: int
    weaken_counter: int
    barrier_counter: int


def resolve_weaken_recalculation(strength: int, toughness: int, dexterity: int,
                                 *, weaken_counter: int, barrier_counter: int):
    """Other_DefcharWorkInt seam AFTER fresh base/equipment reconstruction.

    All other suit/profession/wolf/fear modifiers must be absent. This function
    is an explicit recalculation event, not an automatically invented round tick.
    C 0.8 is double; conversion back to int truncates toward zero. The final
    attack/defense/quick work fields equal these resulting fixed values.
    """
    values=(strength,toughness,dexterity,weaken_counter,barrier_counter)
    if any(not 0 <= int(x) < 2**31 for x in values):
        raise WeakenUndefinedSourceDomain("recalculation requires nonnegative int32 inputs")
    active=weaken_counter>0
    powers=tuple(int(x*0.8) if active else int(x) for x in (strength,toughness,dexterity))
    return WeakenRecalculation(*powers,
        weaken_counter-1 if active else weaken_counter,
        barrier_counter-1 if barrier_counter>0 else barrier_counter)
