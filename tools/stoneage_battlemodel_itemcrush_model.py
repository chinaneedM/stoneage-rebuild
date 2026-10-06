"""Declared empty-equipment ItemCrush chronology; equipped mutation excluded.

Source feature choices and raw rand range are explicit experiment inputs.
This does not select original build membership or certify a libc PRNG.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Mapping

SOURCE_DEFAULT_ITEMCRUSH_RATE = 400000
ITEMCRUSH_VARIANTS = frozenset({"legacy", "take_itemdamage", "take_itemdamage_fix",
                               "take_itemdamage_pet", "take_itemdamage_pet_fix"})


def _integer(value, name, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be integer in {low}..{high}")
    return value


@dataclass(frozen=True)
class EmptyEquipmentParticipant:
    participant_id: str
    kind: str
    level: int
    equipment_indices: tuple[int, ...]

    def __post_init__(self):
        if not isinstance(self.participant_id, str) or not self.participant_id:
            raise ValueError("equipment participant identity required")
        if self.kind not in {"player", "pet", "enemy"}:
            raise ValueError("bounded equipment participant kind required")
        _integer(self.level, "equipment level", 1, 2**31-1)
        if type(self.equipment_indices) is not tuple or len(self.equipment_indices) not in {5, 7}:
            raise ValueError("explicit five/seven equipment slots required")
        if any(type(v) is not int or v != -1 for v in self.equipment_indices):
            raise ValueError("only explicitly empty equipment indices are supported")


@dataclass(frozen=True)
class BattleModelItemCrushContext:
    source_profile: str
    variant: str
    global_rate: int
    raw_rand_max: int
    participants: Mapping[int, EmptyEquipmentParticipant]

    def __post_init__(self):
        if self.source_profile not in {"gavin", "iris", "bismarck"}:
            raise ValueError("explicit fixed source profile required")
        if self.variant not in ITEMCRUSH_VARIANTS:
            raise ValueError("explicit ItemCrush variant required")
        if self.source_profile != "bismarck" and self.variant not in {"legacy", "take_itemdamage"}:
            raise ValueError("FIX/pet-equipment variants only evidenced at bismarck")
        _integer(self.global_rate, "current ItemCrush rate", 1, 2**31-1)
        _integer(self.raw_rand_max, "declared raw rand maximum", 1, 2**31-1)
        copied = dict(self.participants)
        for slot, participant in copied.items():
            _integer(slot, "equipment slot", 0, 19)
            if not isinstance(participant, EmptyEquipmentParticipant):
                raise TypeError("typed empty equipment participants required")
            expected = 7 if participant.kind == "pet" and "pet" in self.variant else 5
            if len(participant.equipment_indices) != expected:
                raise ValueError("equipment slot count disagrees with declared variant")
        if len({p.participant_id for p in copied.values()}) != len(copied):
            raise ValueError("duplicate equipment participant identity")
        object.__setattr__(self, "participants", MappingProxyType(copied))

    def bind(self, entries, *, source_profile):
        if self.source_profile != source_profile:
            raise ValueError("ItemCrush source profile mismatches admission")
        if set(entries) != set(self.participants):
            raise ValueError("empty equipment must exactly cover mapped entries")
        for slot, entry in entries.items():
            _integer(slot, "bound equipment entry slot", 0, 19)
            p = self.participants[slot]
            if (p.participant_id, p.kind) != (entry.participant_id, entry.kind):
                raise ValueError("empty equipment participant identity/kind mismatch")


@dataclass(frozen=True)
class EmptyEquipmentItemCrushResolution:
    actual_defender_slot: int
    variant: str
    legacy_check_passed: bool = False
    legacy_roll: int | None = None
    raw_rand_value: int | None = None
    raw_rand_modulus: int | None = None
    defender_lookup_slots: tuple[int, ...] = ()
    attacker_weapon_looked_up: bool = False
    crushed: bool = False


def resolve_empty_equipment_itemcrush(
    context: BattleModelItemCrushContext, *, actor_slot: int, defender_slot: int,
    take: Callable[[str, int, int], int],
) -> EmptyEquipmentItemCrushResolution:
    """A surviving helper calls this even for DODGE/MISS/ALLGUARD/damage0.

    Caller owns survival, actual Guardian routing and ordering before status.
    Empty equipment prevents mutations, not the source checks/random draws.
    """
    if not isinstance(context, BattleModelItemCrushContext):
        raise TypeError("typed ItemCrush context required")
    _integer(actor_slot, "ItemCrush actor slot", 10, 19)
    _integer(defender_slot, "ItemCrush defender slot", 0, 9)
    if actor_slot not in context.participants or defender_slot not in context.participants:
        raise ValueError("ItemCrush endpoints require mapped equipment")
    defender = context.participants[defender_slot]
    if context.variant == "legacy":
        if defender.kind != "player":
            return EmptyEquipmentItemCrushResolution(defender_slot, context.variant)
        roll = _integer(take("itemcrush_check", 1, context.global_rate),
                        "ItemCrush check draw", 1, context.global_rate)
        passed = roll < defender.level
        # Original ItemCrush scans items, returns FALSE at j==0 before RAND.
        return EmptyEquipmentItemCrushResolution(defender_slot, context.variant,
            legacy_check_passed=passed, legacy_roll=roll,
            defender_lookup_slots=tuple(range(5)) if passed else ())
    raw = _integer(take("itemcrush_raw_rand", 0, context.raw_rand_max),
                   "ItemCrush raw rand draw", 0, context.raw_rand_max)
    count = len(defender.equipment_indices)
    modulus = count if "fix" in context.variant else 100
    reduced = raw % modulus
    start = reduced if "fix" in context.variant else (
        1 if reduced < 50 else 0 if reduced < 67 else 3 if reduced < 84 else 4)
    lookups = []
    for _ in range(count):
        lookups.append(start)
        # Source retains literal %5 even in the seven-slot pet variant.
        start = (start + 1) % 5
    return EmptyEquipmentItemCrushResolution(defender_slot, context.variant,
        raw_rand_value=raw, raw_rand_modulus=modulus,
        defender_lookup_slots=tuple(lookups), attacker_weapon_looked_up=True)
