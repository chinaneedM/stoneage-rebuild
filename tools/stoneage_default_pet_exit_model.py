"""Explicit owner/default selection/occupancy for the reduced battle layout.

No owned == selected == active inference. Source-shaped selected helper exit
and the separate player Entry[i+5] cleanup return independently bound identities.
"""
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class DefaultPetExitAuthority:
    owner_id: str
    selected_pet_id: str | None
    owned_pet_ids: tuple[str, ...]
    occupied_pet_slots: Mapping[str, int]

    def __post_init__(self):
        if type(self.owner_id) is not str or not self.owner_id:
            raise ValueError("explicit owner identity required")
        pets = self.owned_pet_ids
        if type(pets) is not tuple or any(type(p) is not str or not p for p in pets):
            raise ValueError("explicit owned pet identity tuple required")
        if len(set(pets)) != len(pets) or self.owner_id in pets:
            raise ValueError("duplicate/conflicting owned pet identity")
        if self.selected_pet_id is not None and self.selected_pet_id not in pets:
            raise ValueError("selected pet must belong to authoritative roster")
        slots = dict(self.occupied_pet_slots)
        if set(slots)-set(pets) or len(set(slots.values())) != len(slots):
            raise ValueError("pet occupancy ownership/slot drift")
        if any(type(s) is not int or not 0 <= s < 20 for s in slots.values()):
            raise ValueError("explicit reduced battle slot required")
        object.__setattr__(self, "occupied_pet_slots", MappingProxyType(slots))


def bind_exit_authorities(values, by_slot):
    authorities = dict(values or {})
    owned = set()
    occupied = set()
    for owner_id, authority in authorities.items():
        if not isinstance(authority, DefaultPetExitAuthority) or authority.owner_id != owner_id:
            raise ValueError("typed default-pet owner authority required")
        if owned.intersection(authority.owned_pet_ids):
            raise ValueError("pet cannot belong to multiple owners")
        owned.update(authority.owned_pet_ids)
        owner = next((p for p in by_slot.values() if p.participant_id == owner_id), None)
        if owner is not None and owner.kind != "player":
            raise ValueError("default-pet owner must be a player")
        for pet_id, slot in authority.occupied_pet_slots.items():
            if slot in occupied:
                raise ValueError("conflicting pet occupancy authorities")
            occupied.add(slot)
            p = by_slot.get(slot)
            if p is not None and (p.participant_id != pet_id or p.kind != "pet"
                                  or (owner is not None and p.side != owner.side)):
                raise ValueError("default-pet battle occupancy identity drift")
        for slot, p in by_slot.items():
            if p.participant_id in authority.owned_pet_ids:
                if authority.occupied_pet_slots.get(p.participant_id) != slot:
                    raise ValueError("active owned pet lacks matching occupancy authority")
    return authorities


def pet_owner_id(pet_id, authorities):
    owners = [pid for pid, a in authorities.items() if pet_id in a.owned_pet_ids]
    if len(owners) != 1:
        raise ValueError("pet ultimate exit requires explicit unique owner authority")
    return owners[0]


def clear_owner_selection(authorities, owner_id):
    if owner_id not in authorities:
        raise ValueError("selection clear requires explicit owner authority")
    authorities[owner_id] = replace(authorities[owner_id], selected_pet_id=None)


def player_pet_exit_ids(owner_slot, owner_id, authorities, by_slot, excluded_slots):
    if owner_id not in authorities:
        raise ValueError("player ultimate exit requires explicit default-pet authority")
    authority = authorities[owner_id]
    # Selection may resolve to an owned pet absent from battle. The helper's
    # failed Exit must not select some other available pet.
    selected = authority.selected_pet_id
    selected_slot = authority.occupied_pet_slots.get(selected)
    result = []
    if selected_slot is not None and selected_slot not in excluded_slots:
        result.append(selected)
    # This separate occupancy cleanup occurs even when DEFAULTPET is -1.
    if type(owner_slot) is not int or not 0 <= owner_slot < 20 or not owner_slot % 10 < 5:
        raise ValueError("player exit requires an evidenced reduced owner slot")
    paired_slot = owner_slot + 5
    paired = next((pid for pid, s in authority.occupied_pet_slots.items() if s == paired_slot), None)
    actual = by_slot.get(paired_slot)
    if paired_slot not in excluded_slots and actual is not None:
        if actual.kind != "pet" or actual.participant_id != paired:
            raise ValueError("player paired occupancy conflicts with owner authority")
    if paired is not None and paired_slot not in excluded_slots and paired not in result:
        result.append(paired)
    return tuple(result)


def apply_selection_events(authorities, events, by_slot):
    """Apply semantic selection transitions in event order, without HP inference."""
    for event in events:
        if event.default_pet_selection_cleared_owner_id is not None:
            clear_owner_selection(authorities, event.default_pet_selection_cleared_owner_id)
        recall = (event.two_battletimid_resolution is not None and
                  event.two_battletimid_resolution.pet_withdrawn)
        timid = (event.battletimid_resolution is not None and
                 event.battletimid_resolution.owner_default_pet_cleared)
        if (recall or timid) and authorities:
            target = by_slot.get(event.resolved_target_slot)
            if target is None:
                raise ValueError("selection event has no bound pet target")
            clear_owner_selection(authorities, pet_owner_id(target.participant_id, authorities))
