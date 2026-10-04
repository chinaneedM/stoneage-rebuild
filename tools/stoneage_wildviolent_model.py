"""Explicit-charset WildViolentAttack reference; no recovered numeric command.

This is a callback/action-plan seam, not an ordered battle executor. Original
compiler execution charset is unknown. Undefined signed shifts and scanf
overflow remain outside admission, even when a later x86 build happens to run.
"""
from dataclasses import dataclass
from fractions import Fraction
import math
import re
import struct

from tools.stoneage_nocast_model import _f32, _scanf_int

CALLBACK_NAME = "PETSKILL_WildViolentAttack"
COMMAND_NAME = "BATTLE_COM_S_WILDVIOLENTATTACK"
FEATURE_NAME = "_SKILL_WILDVIOLENT_ATT"
SOURCE_PETSKILL_SYMBOL_NAME = "PETSKILL_WILDVIOLENTATTACK"


class WildViolentUndefinedSourceDomain(ValueError):
    """Input outside the explicitly defined native reference domain."""


def _int32(value):
    if not isinstance(value, int) or not -(2**31) <= value < 2**31:
        raise WildViolentUndefinedSourceDomain("requires signed int32")
    return value


def _float32(value):
    try:
        result = _f32(value)
    except (OverflowError, ValueError) as exc:
        raise WildViolentUndefinedSourceDomain("float32 overflow") from exc
    if not math.isfinite(result):
        raise WildViolentUndefinedSourceDomain("nonfinite float32")
    return result


def _scanf_decimal_float(raw):
    text = raw.decode("latin-1").lstrip("\t\n\v\f\r ")
    if re.match(r"[+-]?(?:inf|nan|0[xX])", text, re.I):
        raise WildViolentUndefinedSourceDomain("nondecimal float outside admission")
    # Deliberately exclude incomplete exponents: glibc scanf consumes them in
    # a way not specified by this decimal-prefix reference.
    match = re.match(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", text)
    if match is None:
        return None
    if text[match.end():].startswith(("e", "E")):
        raise WildViolentUndefinedSourceDomain("incomplete float exponent")
    token = match.group(0)
    if len(token) > 128 or ("e" in token.lower() and
                           abs(int(token.lower().split("e")[1])) > 100):
        raise WildViolentUndefinedSourceDomain("decimal outside bounded scanner domain")
    # scanf %f rounds directly to binary32. Avoid binary64 double rounding by
    # comparing exact rational distances to the candidate and its neighbours.
    exact = Fraction(token)
    candidate = _float32(abs(float(token)))
    bits = struct.unpack("=I", struct.pack("=f", candidate))[0]
    neighbours = []
    for n in (bits - 1, bits, bits + 1):
        if 0 <= n < 0x7f800000:
            value = struct.unpack("=f", struct.pack("=I", n))[0]
            neighbours.append((abs(Fraction(value) - abs(exact)), n & 1, value))
    value = min(neighbours)[2]
    return -value if token.startswith("-") else value


@dataclass(frozen=True)
class WildViolentOption:
    attack_delta_fraction: float | None
    defense_delta_fraction: float | None
    additive_dodge_percent_points: int


def parse_wildviolent_option(option: bytes, *, execution_charset: str) -> WildViolentOption:
    if execution_charset not in {"utf-8", "cp950", "big5"}:
        raise ValueError("explicit supported execution charset required")
    raw = bytes(option)
    if b"\0" in raw:
        raise WildViolentUndefinedSourceDomain("embedded NUL outside admission")
    # OPTION is a C byte string. Its encoding need not equal the compiled
    # literal encoding: the UTF-8-source/CP950-data mismatch is meaningful.
    per = _float32(0.01)
    fractions = []
    for marker in ("攻%", "防%"):
        pos = raw.find(marker.encode(execution_charset))
        if pos < 0:
            fractions.append(None)
            continue
        value = _scanf_decimal_float(raw[pos + 3:])
        if value is not None:
            per = value
        per = _float32(per / _float32(100))
        fractions.append(per)
    pos = raw.find("避".encode(execution_charset))
    try:
        duck = _scanf_int(raw[pos + 2:].decode("latin-1")) if pos >= 0 else None
    except ValueError as exc:
        raise WildViolentUndefinedSourceDomain("dodge scanf overflows int32") from exc
    return WildViolentOption(*fractions, 0 if duck is None else duck)


def _power(fixed, fraction, before):
    if fraction is None:
        return before
    product = _float32(_float32(fixed) * fraction)
    if not -(2**31) <= product < 2**31:
        raise WildViolentUndefinedSourceDomain("float-to-int32 power delta overflow")
    return _int32(fixed + int(product))


@dataclass(frozen=True)
class WildViolentSetup:
    source_return_value: bool
    command_name: str
    target_slot: int
    mode_name: str
    attack_power: int
    defense_power: int
    packed_com3: int
    option: WildViolentOption | None


def resolve_wildviolent_setup(*, option: bytes | None, execution_charset: str,
                             profile: str, target_slot: int, fixed_strength: int,
                             fixed_toughness: int, attack_power_before: int,
                             defense_power_before: int, packed_com3_before: int):
    if profile not in {"gavin", "iris", "bismarck"}:
        raise ValueError("unknown pinned profile")
    if execution_charset not in {"utf-8", "cp950", "big5"}:
        raise ValueError("explicit supported execution charset required")
    for value in (target_slot, fixed_strength, fixed_toughness,
                  attack_power_before, defense_power_before, packed_com3_before):
        _int32(value)
    if option is None and profile == "bismarck":
        raise WildViolentUndefinedSourceDomain("strcmp NULL dereference")
    failed = option is None or (profile == "bismarck" and option == b"")
    parsed = None if failed else parse_wildviolent_option(
        option, execution_charset=execution_charset)
    packed = packed_com3_before
    attack, defense = attack_power_before, defense_power_before
    if parsed is not None:
        duck = parsed.additive_dodge_percent_points
        if not 0 <= duck <= 32767:
            raise WildViolentUndefinedSourceDomain("HIGH macro has undefined signed left shift")
        attack = _power(fixed_strength, parsed.attack_delta_fraction, attack)
        defense = _power(fixed_toughness, parsed.defense_delta_fraction, defense)
        packed = (duck << 16) | (packed & 65535)
    # Command/target/mode are written even before an OPTION failure.
    return WildViolentSetup(not failed, COMMAND_NAME, target_slot,
                           "BATTLE_CHARMODE_C_OK", attack, defense, packed, parsed)


@dataclass(frozen=True)
class WildViolentActionPlan:
    attack_count: int
    damage_divisor: int
    additive_dodge_percent_points: int
    original_target_list: tuple[int, ...]


def plan_wildviolent_nonbow_action(*, count_roll_3_10: int, packed_com3: int,
                                  target_slot: int):
    """Count RNG precedes TargetListSet/initial TargetAdjust at action time.

    Opposite-side, non-bow domain only. This does not consume physical hit or
    retarget RNG, settle HP, perform status visits, or simulate suppression.
    """
    if not isinstance(count_roll_3_10, int) or not 3 <= count_roll_3_10 <= 10:
        raise ValueError("requires explicit RAND(3,10) witness")
    _int32(packed_com3)
    _int32(target_slot)
    return WildViolentActionPlan(count_roll_3_10, count_roll_3_10,
                                packed_com3 >> 16, (target_slot,) * 20)


def wildviolent_divided_damage(damage: int, attack_count: int) -> int:
    """Actual float gDamageDiv seam AFTER AttackSeq, BEFORE DamageSub."""
    _int32(damage)
    if not isinstance(attack_count, int) or not 3 <= attack_count <= 10:
        raise ValueError("requires count in native RAND(3,10) range")
    if damage <= 0:
        return damage
    divided = int(_float32(_float32(damage) / _float32(attack_count)))
    return max(1, divided)
