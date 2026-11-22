#!/usr/bin/env python3
"""2016 descendant classic-PC baseline pet panel, never original TW1 stats."""
from dataclasses import dataclass
from struct import pack, unpack


@dataclass(frozen=True)
class PetSourceBasePanel:
    """Unmodified CHAR_initcharWorkInt work fields, not the actual client UI."""

    max_hp: int
    attack: int
    defense: int
    quick: int


def _c_float32(value):
    """One C float storage round; the HP local is float, not double."""
    return unpack("<f", pack("<f", float(value)))[0]


def project_pet_source_base_panel(internal_stats):
    """Source-bounded 2016 PC char.c CHAR_initcharWorkInt baseline.

    Reproduces double arithmetic for STR/TOUGH/DEX and intermediate float
    storage for hp, with C truncation to int. Caller must separately consider
    ITEM_equipEffect, Other_DefcharWorkInt, HP clamps, and status/network
    serialization. No executable original retail server is implied.
    """
    if len(internal_stats) != 4:
        raise ValueError("expected four internal pet stats")
    vital, strength, toughness, dexterity = tuple(int(x) for x in internal_stats)
    if min(vital, strength, toughness, dexterity) < 0:
        raise ValueError("internal pet stats must be non-negative")
    hp = _c_float32((4*vital + strength + toughness + dexterity) * 0.01)
    attack = (
        strength * 0.01 * 1.0
        + toughness * 0.01 * 0.1
        + vital * 0.01 * 0.1
        + dexterity * 0.01 * 0.05
    )
    defense = (
        toughness * 0.01 * 1.0
        + strength * 0.01 * 0.1
        + vital * 0.01 * 0.1
        + dexterity * 0.01 * 0.05
    )
    return PetSourceBasePanel(
        max_hp=int(hp), attack=int(attack),
        defense=int(defense), quick=int(dexterity * 0.01),
    )
