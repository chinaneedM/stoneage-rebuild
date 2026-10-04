"""Bounded PETSKILL_Combined descendant reference model.

Only the source-safe, well-formed OPTION domain is modeled.  Malformed OPTION
behavior in the pinned descendants remains historical UB and is never repaired
silently here.
"""
from __future__ import annotations

from dataclasses import dataclass

CALLBACK_NAME="PETSKILL_Combined"
COMMAND_NAME="BATTLE_COM_JYUJYUTU"
FEATURE_NAME="_PETSKILL_COMBINED"
COMMAND_VALUE=2000
MAX_MAGIC_CHOICES=10


class CombinedSourceDomain(ValueError):
    """Input is outside the bounded well-formed descendant source domain."""


def _int32(value:int)->int:
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise CombinedSourceDomain("requires signed int32 witness")
    return value


def normalize_declared_count(raw_count:int)->int:
    raw_count=_int32(raw_count)
    if raw_count <= 0:
        raise CombinedSourceDomain(
            "Combined source has no safe count<=0 path"
        )
    return min(raw_count,MAX_MAGIC_CHOICES)


@dataclass(frozen=True)
class CombinedSelection:
    target_slot:int
    declared_count:int
    effective_count:int
    magic_ids:tuple[int,...]
    draw_index:int
    selected_magic_id:int
    packed_com3:int
    rng_draws_consumed:int=1
    command_name:str=COMMAND_NAME
    command_value:int=COMMAND_VALUE
    mode_name:str="BATTLE_CHARMODE_C_OK"


def resolve_combined_selection(
    *,
    target_slot:int,
    declared_count:int,
    magic_ids:tuple[int,...],
    draw_index:int,
)->CombinedSelection:
    """Model the callback after its localized marker branch is known valid.

    The C source clamps declared counts above ten, fills up to that many
    kill[] entries, consumes one raw rand()%count draw, writes the chosen
    magic ID into LOW(COM3), and then clears HIGH(COM3) to zero.
    """
    target_slot=_int32(target_slot)
    effective=normalize_declared_count(declared_count)
    ids=tuple(_int32(int(value)) for value in magic_ids)
    if len(ids) < effective:
        raise CombinedSourceDomain(
            "missing magic tokens are historical uninitialized-read UB"
        )
    ids=ids[:effective]
    if type(draw_index) is not int or not 0 <= draw_index < effective:
        raise CombinedSourceDomain(
            "draw_index must be the observed rand()%effective_count value"
        )
    selected=ids[draw_index]
    packed=selected & 0xFFFF
    return CombinedSelection(
        target_slot=target_slot,
        declared_count=int(declared_count),
        effective_count=effective,
        magic_ids=ids,
        draw_index=draw_index,
        selected_magic_id=selected,
        packed_com3=packed,
    )
