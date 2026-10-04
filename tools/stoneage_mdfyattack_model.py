"""Guarded Mdfyattack reference, distinct from Modifyattack.

No historical recovered25 command number or ordered-round admission is
assigned here. Only non-null ASCII OPTION and defined signed-C arithmetic
are admitted. Native failure paths can leave partial work writes; refusing
those inputs here does not model them as an atomic native rollback.
"""
from dataclasses import dataclass
import re
import struct

from tools.stoneage_battle_core_model import elemental_vector

CALLBACK_NAME = "PETSKILL_Mdfyattack"
COMMAND_NAME = "BATTLE_COM_S_MDFYATTACK"
FEATURE_NAME = "_PSKILL_MDFYATTACK"
ELEMENT_CODES = (b"EA", b"WA", b"FI", b"WI")
ELEMENT_NAMES = ("earth", "water", "fire", "wind")
INT_MAX = 2147483647


@dataclass(frozen=True)
class MdfyAttackOption:
    element_index: int
    amount: int

    def __post_init__(self):
        if type(self.element_index) is not int or not 0 <= self.element_index < 4:
            raise ValueError("Mdfyattack element must be EA/WA/FI/WI")
        # HIGH uses a signed left shift by 16. Negative or >=32768 is not
        # a defined signed-C packing domain; do not normalize wrapped values.
        if type(self.amount) is not int or not 0 <= self.amount <= 32767:
            raise ValueError("Mdfyattack amount outside defined HIGH(COM4) packing")

    @property
    def element(self):
        return ELEMENT_NAMES[self.element_index]

    @property
    def packed_com4(self):
        return (self.amount << 16) | self.element_index

    @property
    def attack_vector(self):
        result = [0] * 5
        result[self.element_index] = self.amount
        return tuple(result)


def parse_mdfyattack_option(raw: bytes) -> MdfyAttackOption:
    if not isinstance(raw, bytes) or b"\0" in raw:
        raise ValueError("Mdfyattack reference requires non-NUL OPTION bytes")
    try:
        raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("non-ASCII delimiter scanning remains outside reference") from exc
    fields = raw.split(b"|")
    # The native helper copies at most 255 bytes into each 256-byte buffer.
    token = fields[0][:255]
    if token not in ELEMENT_CODES or len(fields) < 2:
        raise ValueError("Mdfyattack requires exact first code and second field")
    number = fields[1][:255]
    match = re.match(rb"[\t\n\v\f\r ]*([+-]?[0-9]+)", number)
    amount = int(match.group(1)) if match else 0
    return MdfyAttackOption(ELEMENT_CODES.index(token), amount)


@dataclass(frozen=True)
class MdfyAttackSetup:
    command_symbol: str
    submitted_target: int
    skill_array: int
    option: MdfyAttackOption


def mdfyattack_callback_setup(*, submitted_target: int, skill_array: int,
                            option: bytes) -> MdfyAttackSetup:
    if type(submitted_target) is not int or not -2147483648 <= submitted_target <= INT_MAX:
        raise ValueError("submitted target outside C int")
    if type(skill_array) is not int or not 0 <= skill_array <= 65535:
        raise ValueError("skill array outside explicit LOW(COM3) domain")
    # No PLAYER rejection or attack/defense work-power mutation in this callback.
    return MdfyAttackSetup(COMMAND_NAME, submitted_target, skill_array,
                          parse_mdfyattack_option(option))


def _f32(value):
    return struct.unpack("f", struct.pack("f", value))[0]


def mdfyattack_attribute_damage(damage: int, option: MdfyAttackOption,
                               defender_elements, *, field_attr="none",
                               field_power=0, property_hooks_active=False):
    """Attribute-stage reference with no property/suit/profession extensions.

    Input damage is the physical pre-attribute value. This function is not a
    complete AttackSeq, critical, guard, Guardian or damageReact settlement.
    In particular, the attack vector's fifth component remains zero even
    for an amount below 100; the ordinary elemental_vector helper must not
    fill a neutral remainder for this attacker.
    """
    if not isinstance(option, MdfyAttackOption):
        raise ValueError("typed Mdfyattack OPTION required")
    if property_hooks_active:
        raise ValueError("property hooks require a separately evidenced execution profile")
    if type(damage) is not int or not 0 <= damage <= INT_MAX:
        raise ValueError("damage outside nonnegative C int")
    values = tuple(defender_elements)
    if len(values) != 4 or any(type(x) is not int or not 0 <= x <= 100 for x in values):
        raise ValueError("defender elements outside guarded 0..100 domain")
    if type(field_power) is not int or not 0 <= field_power <= 100:
        raise ValueError("field power outside guarded 0..100 domain")
    if field_attr not in ("none", *ELEMENT_NAMES):
        raise ValueError("unknown field attribute")
    defense = elemental_vector(*values)
    scaled = damage * option.amount
    # Native element*damage and element*defender products precede the
    # floating coefficients. Reject signed overflow rather than emulating it.
    if scaled > INT_MAX or any(scaled * weight > INT_MAX for weight in defense):
        raise ValueError("Mdfyattack attribute product would overflow C int")
    # Earth -> water -> fire -> wind -> earth dominance cycle. Preserve
    # term order and the int assignment before final D_ATTR truncation.
    coefficients = (
        (1.0, 1.5, 1.0, 0.6, 1.5),
        (0.6, 1.0, 1.5, 1.0, 1.5),
        (1.0, 0.6, 1.0, 1.5, 1.5),
        (1.5, 1.0, 0.6, 1.0, 1.5),
    )[option.element_index]
    # C expression order is neutral, fire, water, earth, wind.
    order = (4, 2, 1, 0, 3)
    subtotal = int(sum(scaled * defense[i] * coefficients[i] for i in order))
    if subtotal > INT_MAX:
        raise ValueError("Mdfyattack attribute subtotal would overflow C int")
    core = int(subtotal * (1.0 / 10000))
    selected = ELEMENT_NAMES.index(field_attr) if field_attr != "none" else None
    def power(vector):
        if selected is None:
            return 0.5
        return _f32(0.5 + vector[selected] * _f32(field_power) * 0.01 * 0.01 * 0.5)
    ratio = _f32(power(option.attack_vector) / power(defense))
    adjusted = _f32(_f32(core) * ratio)
    if adjusted > INT_MAX:
        raise ValueError("field adjustment outside C int")
    return int(adjusted)
