"""Bounded SetMagicPet descendant reference model.

This preserves later-source quirks rather than normalizing them into a cleaner
game design.  Ordered enemy runtime admission remains separate.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import re

CALLBACK_NAME = "PETSKILL_SetMagicPet"
COMMAND_NAME = "BATTLE_COM_S_SETMAGICPET"
FEATURE_NAME = "_MAGICPET_SKILL"
SOURCE_PETSKILL_SYMBOL_NAME = "PETSKILL_SETMAGICPET"


class SetMagicPetSourceDomain(ValueError):
    """Unproved or unsafe SetMagicPet source/reference domain."""


def _int32(value: int) -> int:
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise SetMagicPetSourceDomain("requires signed int32 witness")
    return value


def _c_atoi(raw: bytes) -> int:
    if not isinstance(raw, bytes):
        raise SetMagicPetSourceDomain("atoi witness must be raw bytes")
    match = re.match(rb"[ \t\r\n\v\f]*([+-]?)([0-9]+)", raw)
    if not match:
        return 0
    magnitude = int(match.group(2), 10)
    value = -magnitude if match.group(1) == b"-" else magnitude
    return _int32(value)


@dataclass(frozen=True)
class SetMagicPetOption:
    turn: int
    amount: int
    kind: str | None
    third_field: bytes

    @property
    def safe_recognized_kind(self) -> bool:
        return self.kind in {"HP", "STR", "TGH", "DEX"}


def parse_setmagicpet_option(option: bytes | None) -> SetMagicPetOption:
    """Reproduce the three delimiter reads and substring dispatch priority."""
    if option is None:
        raise SetMagicPetSourceDomain("safe reference requires non-NULL OPTION")
    if not isinstance(option, bytes) or b"\0" in option:
        raise SetMagicPetSourceDomain("safe reference requires non-NUL OPTION bytes")
    parts = option.split(b"|")
    if len(parts) < 3:
        raise SetMagicPetSourceDomain("source requires three delimiter fields")
    turn = _c_atoi(parts[0])
    amount = _c_atoi(parts[1])
    field = bytes(parts[2])
    if b"HP" in field:
        kind = "HP"
    elif b"STR" in field:
        kind = "STR"
    elif b"TGH" in field:
        kind = "TGH"
    elif b"DEX" in field:
        kind = "DEX"
    else:
        kind = None
    return SetMagicPetOption(turn, amount, kind, field)


@dataclass(frozen=True)
class SetMagicPetSetup:
    accepted: bool
    target_slot: int
    packed_com3: int
    use_count_before: int
    use_count_after: int
    rejected_by_nominal_three_use_limit: bool
    command_name: str = COMMAND_NAME
    mode_name: str = "BATTLE_CHARMODE_C_OK"


def resolve_setmagicpet_setup(
    *,
    target_slot: int,
    skill_array: int,
    packed_com3_before: int,
    use_count: int,
) -> SetMagicPetSetup:
    """Preserve the later-source non-incrementing 'three-use' counter bug."""
    for value in (target_slot, skill_array, packed_com3_before, use_count):
        _int32(value)
    if use_count >= 3:
        return SetMagicPetSetup(
            False, target_slot, packed_com3_before, use_count, use_count, True
        )
    packed = (packed_com3_before & 0xFFFF0000) | (skill_array & 0xFFFF)
    if packed >= 2**31:
        packed -= 2**32
    # Source writes CHAR_MAGICPETMP back to nums unchanged.
    return SetMagicPetSetup(
        True, target_slot, packed, use_count, use_count, False
    )


@dataclass(frozen=True)
class SetMagicPetTargetState:
    duck_turn: int = 0
    str_turn: int = 0
    str_power: int = 0
    tgh_turn: int = 0
    tgh_power: int = 0
    dex_turn: int = 0
    dex_power: int = 0

    def __post_init__(self) -> None:
        for value in (
            self.duck_turn, self.str_turn, self.str_power,
            self.tgh_turn, self.tgh_power, self.dex_turn, self.dex_power,
        ):
            _int32(int(value))

    @property
    def blocks_new_magicpet_buff(self) -> bool:
        return any(
            int(value) > 0
            for value in (
                self.duck_turn, self.str_turn, self.tgh_turn, self.dex_turn
            )
        )


@dataclass(frozen=True)
class SetMagicPetBuffResolution:
    option: SetMagicPetOption
    targets: tuple[SetMagicPetTargetState, ...]
    applied: tuple[bool, ...]


def apply_setmagicpet_buff(
    option: SetMagicPetOption,
    target_states,
) -> SetMagicPetBuffResolution:
    if option.kind == "HP":
        raise SetMagicPetSourceDomain("HP branch uses MultiRecovery, not buff storage")
    outputs = []
    applied = []
    for raw_state in target_states:
        if not isinstance(raw_state, SetMagicPetTargetState):
            raise TypeError("SetMagicPet target state has wrong type")
        state = raw_state
        if state.blocks_new_magicpet_buff:
            outputs.append(state)
            applied.append(False)
            continue
        if option.kind == "STR":
            state = replace(state, str_turn=option.turn, str_power=option.amount)
            changed = True
        elif option.kind == "TGH":
            state = replace(state, tgh_turn=option.turn, tgh_power=option.amount)
            changed = True
        elif option.kind == "DEX":
            state = replace(state, dex_turn=option.turn, dex_power=option.amount)
            changed = True
        else:
            # The source still returns TRUE and formats a kind-0 display event.
            # Runtime admission must not silently treat this as a real buff.
            changed = False
        outputs.append(state)
        applied.append(changed)
    return SetMagicPetBuffResolution(option, tuple(outputs), tuple(applied))


def _c_div100(product: int) -> int:
    return product // 100 if product >= 0 else -((-product) // 100)


@dataclass(frozen=True)
class SetMagicPetFixedStats:
    fixed_str: int
    fixed_tough: int
    fixed_dex: int


def recalculate_setmagicpet_fixed_stats(
    *,
    fixed_str: int,
    fixed_tough: int,
    fixed_dex: int,
    pre_suit_tough: int,
    state: SetMagicPetTargetState,
) -> SetMagicPetFixedStats:
    """Preserve the shared mtgh basis bug in all three pinned descendants.

    R1 admits at most one active STR/TGH/DEX magic-pet state.  This matches the
    executor's own mutual-exclusion gate and avoids inventing overlap order.
    """
    values = (fixed_str, fixed_tough, fixed_dex, pre_suit_tough)
    for value in values:
        _int32(value)
    active = sum(int(x > 0) for x in (state.str_turn, state.tgh_turn, state.dex_turn))
    if active > 1:
        raise SetMagicPetSourceDomain(
            "multiple active STR/TGH/DEX states are outside bounded source domain"
        )
    out_str, out_tough, out_dex = values[:3]
    basis = pre_suit_tough
    if state.str_turn > 0:
        out_str = _int32(out_str + _c_div100(basis * state.str_power))
    elif state.tgh_turn > 0:
        out_tough = _int32(out_tough + _c_div100(basis * state.tgh_power))
    elif state.dex_turn > 0:
        out_dex = _int32(out_dex + _c_div100(basis * state.dex_power))
    return SetMagicPetFixedStats(out_str, out_tough, out_dex)


def tick_setmagicpet_turns(state: SetMagicPetTargetState) -> SetMagicPetTargetState:
    """BATTLE_StatusSeq decrements positive turn counters but leaves powers."""
    return replace(
        state,
        duck_turn=max(0, state.duck_turn - 1),
        str_turn=max(0, state.str_turn - 1),
        tgh_turn=max(0, state.tgh_turn - 1),
        dex_turn=max(0, state.dex_turn - 1),
    )
