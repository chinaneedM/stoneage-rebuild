#!/usr/bin/env python3
"""Versioned StoneAge AttackMagic command/target/direct-use boundary.

This module intentionally stops at the MAGIC_DirectUse call boundary. It models
the fixed descendant command encoding and target-selector rewrite without
inventing recovered25 attack-magic damage semantics.
"""

from dataclasses import dataclass
import re

BATTLE_COM_S_ATTACK_MAGIC = 2002

ATTACK_MAGIC_TARGET_INDEX = {
    301: -1, 302: -1, 303: 26, 304: -1, 305: 20, 306: 20,
    307: -1, 308: -1, 309: -1, 310: -1, 311: 26, 312: 20,
    313: -1, 314: -1, 315: -1, 316: -1, 317: 26, 318: 20,
    319: -1, 320: -1, 321: 26, 322: -1, 323: 26, 324: 20, 325: 20,
}

PROFILE_GAVIN_IRIS = "GAVIN_IRIS_ITEM_HIGH"
PROFILE_BISMARCK = "BISMARCK_HIGH_RESIDUE"
PROFILE_RECOVERED25 = "RECOVERED25_EXPLICIT_ITEM"


def _parse_int_from(text, start):
    match = re.match(r"\s*([+-]?\d+)", text[int(start):])
    return None if match is None else int(match.group(1), 10)


def parse_source_shaped_option(option):
    """Parse the old handler's magic-then-item cursor shape.

    sizeof("magic")/sizeof("item") include the NUL byte, so the fixed C
    handler advances one extra byte past each marker before sscanf.
    """
    text = str(option)
    magic_pos = text.find("magic")
    if magic_pos < 0:
        return {
            "magic_marker": False,
            "magic": None,
            "item_marker_after_magic": False,
            "item": None,
        }
    magic_start = magic_pos + len("magic") + 1
    magic = _parse_int_from(text, magic_start)
    item_pos = text.find("item", magic_start)
    if item_pos < 0:
        return {
            "magic_marker": True,
            "magic": magic,
            "item_marker_after_magic": False,
            "item": None,
        }
    item_start = item_pos + len("item") + 1
    item = _parse_int_from(text, item_start)
    return {
        "magic_marker": True,
        "magic": magic,
        "item_marker_after_magic": True,
        "item": item,
    }


def pack_command3(low, high):
    return (int(low) & 0xFFFF) | ((int(high) & 0xFFFF) << 16)


def command3_low(value):
    return int(value) & 0xFFFF


def command3_high(value):
    return (int(value) >> 16) & 0xFFFF


@dataclass(frozen=True)
class AttackMagicCommand:
    command1: int
    command2: int
    command3: int
    magic_id: int
    item_index: int
    high_source: str


@dataclass(frozen=True)
class MagicDirectUseRequest:
    magic_id: int
    target: int
    item_index: int
    source_target: int
    target_area: int


def encode_attack_magic_command(
    target,
    option,
    *,
    profile=PROFILE_RECOVERED25,
    prior_high=0,
):
    parsed = parse_source_shaped_option(option)

    if profile == PROFILE_RECOVERED25:
        if not parsed["magic_marker"] or parsed["magic"] is None:
            raise ValueError(
                "recovered25 AttackMagic requires a numeric magic marker"
            )
        if (
            not parsed["item_marker_after_magic"]
            or parsed["item"] is None
        ):
            raise ValueError(
                "recovered25 AttackMagic requires a numeric item marker after magic"
            )
        magic = int(parsed["magic"])
        item = int(parsed["item"])
        if magic not in ATTACK_MAGIC_TARGET_INDEX:
            raise ValueError(
                "recovered25 AttackMagic magic id is outside 301..325"
            )
        high = item
        high_source = "explicit_item"

    elif profile == PROFILE_GAVIN_IRIS:
        # The early fixed handler reuses the pointer returned by strstr("magic")
        # in a second strstr(..., "item"). If magic is absent that pointer is
        # NULL, so do not sanitize the historical invalid/undefined cursor path.
        if not parsed["magic_marker"]:
            raise ValueError(
                "gavin/iris AttackMagic missing magic marker has invalid source cursor"
            )
        magic = 313 if parsed["magic"] is None else int(parsed["magic"])
        item = 19659 if parsed["item"] is None else int(parsed["item"])
        high = item
        high_source = "explicit_or_default_item"

    elif profile == PROFILE_BISMARCK:
        # This descendant removed the item parse/write; SETWORKINT_LOW preserves
        # the prior high half, which DirectUse later consumes as the item index.
        magic = 313 if parsed["magic"] is None else int(parsed["magic"])
        high = int(prior_high)
        item = high
        high_source = "preserved_residue"

    else:
        raise ValueError(f"unknown AttackMagic profile: {profile}")

    return AttackMagicCommand(
        command1=BATTLE_COM_S_ATTACK_MAGIC,
        command2=int(target),
        command3=pack_command3(magic, high),
        magic_id=int(magic),
        item_index=int(item),
        high_source=high_source,
    )


def remap_attack_magic_target(magic_id, target, *, open_e_petskill=False):
    """Apply the fixed 25-entry magic-id target selector table."""
    magic_id = int(magic_id)
    target = int(target)
    area = ATTACK_MAGIC_TARGET_INDEX.get(magic_id, -1)

    if area == 20:
        if open_e_petskill:
            return 21 if target >= 10 else 20
        return 20

    if area != -1:
        return area if 0 <= target <= 4 else area - 1

    return target


def build_magic_direct_use_request(command, *, open_e_petskill=False):
    """Project a command to the fixed battle executor's DirectUse arguments."""
    if int(command.command1) != BATTLE_COM_S_ATTACK_MAGIC:
        raise ValueError("not an AttackMagic battle command")
    target = remap_attack_magic_target(
        command.magic_id,
        command.command2,
        open_e_petskill=open_e_petskill,
    )
    return MagicDirectUseRequest(
        magic_id=int(command.magic_id),
        target=int(target),
        item_index=int(command.item_index),
        source_target=int(command.command2),
        target_area=int(ATTACK_MAGIC_TARGET_INDEX.get(command.magic_id, -1)),
    )
