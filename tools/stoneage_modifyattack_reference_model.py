"""Bounded Modifyattack helper reference, not ordered-runtime admission.

Damage enters after AttackSeq, before DamageSub. The caller owns reaction
demotion and the positive-damage gate. Native float32/int truncation and the
integer division of the random remainder are preserved explicitly.
"""
from dataclasses import dataclass
import re
import struct

CALLBACK_NAME = "PETSKILL_Modifyattack"
COMMAND_NAME = "BATTLE_COM_S_MODIFYATT"
FEATURE_NAME = "_PSKILL_MODIFY"
ELEMENT_CODES = (b"EA", b"WA", b"FI", b"WI")


def _f32(value):
    return struct.unpack("f", struct.pack("f", value))[0]


@dataclass(frozen=True)
class ModifyAttackOption:
    element_index: int | None
    percent: int


def parse_modifyattack_option(raw: bytes) -> ModifyAttackOption | None:
    if not isinstance(raw, bytes) or b"\0" in raw or not raw.isascii():
        raise ValueError("reference requires non-NUL ASCII OPTION")
    fields = raw.split(b"|")
    if len(fields) < 2:
        return None
    first, second = fields[0][:255], fields[1][:255]
    match = re.match(rb"[\t\n\v\f\r ]*([+-]?[0-9]+)", second)
    percent = int(match.group(1)) if match else 0
    if not -(2**31) <= percent < 2**31:
        raise ValueError("atoi outside defined signed-int domain")
    kind = ELEMENT_CODES.index(first) if first in ELEMENT_CODES else None
    return ModifyAttackOption(kind, percent)


def modifyattack_helper_damage(damage, option, defender_elements, *, raw_rand=None):
    """Return (damage, helper_rand_draws); no fabricated PRNG state."""
    if type(damage) is not int or not 0 <= damage < 2**31:
        raise ValueError("nonnegative signed-int damage required")
    attrs = tuple(defender_elements)
    if len(attrs) != 4 or any(type(x) is not int or not 0 <= x <= 100 for x in attrs):
        raise ValueError("bounded elemental attributes must be 0..100")
    if option is not None and not isinstance(option, ModifyAttackOption):
        raise ValueError("typed bounded OPTION required")
    if option is None or option.element_index is None:
        if raw_rand is not None:
            raise ValueError("no helper RNG owned by this input")
        return damage, 0
    if not isinstance(option, ModifyAttackOption) or option.element_index not in range(4):
        raise ValueError("typed bounded OPTION required")
    modnum = attrs[option.element_index]
    if modnum <= 0:
        if raw_rand is not None:
            raise ValueError("zero matched attribute owns no helper RNG")
        return damage, 0
    if type(raw_rand) is not int or not 0 <= raw_rand < 2**31:
        raise ValueError("one explicit nonnegative signed-int rand result required")
    base = _f32(_f32(option.percent) / _f32(100))
    # Source casts AFTER integer division: remainders below 100 add zero.
    fraction = _f32(base + _f32((raw_rand % (modnum + 5)) // 100))
    result = _f32(_f32(damage) + _f32(_f32(damage) * fraction))
    if not -(2**31) <= result < 2**31:
        raise ValueError("float-to-int damage conversion outside defined domain")
    return int(result), 1
