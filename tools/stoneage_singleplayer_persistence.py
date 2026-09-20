#!/usr/bin/env python3
"""Versioned local persistence for the single-player historical domain.

This is a reconstruction DESIGN boundary, not a recovered historical save or
account format. It serializes only persistent player-owned state. Static master
data, transient world objects, active interaction sessions, battle sessions and
network/account-server concepts are intentionally excluded.
"""

from __future__ import annotations

import json
from types import MappingProxyType
from typing import Any, Mapping

from tools.stoneage_singleplayer_domain import (
    EnemyVariantId,
    InventoryItem,
    InventorySlot,
    ItemTemplateId,
    PetActor,
    PetSkill,
    PetSlot,
    PetTemplateId,
    PersistentPlayerState,
    PlayerState,
    SinglePlayerHistoricalDomain,
)


PERSISTENCE_SCHEMA = "stoneage.singleplayer.persistence.r1"
_TOP_LEVEL_KEYS = {"schema", "character", "inventory", "pets"}


def _plain_mapping(value: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    out = dict(value)
    try:
        json.dumps(out, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} contains non-JSON state") from exc
    return out


def dump_persistent_state(
    state: PersistentPlayerState,
) -> dict[str, Any]:
    character = None
    if state.character is not None:
        character = _plain_mapping(state.character.fields, label="character")

    inventory = []
    for slot, item in sorted(state.inventory.items()):
        if slot != item.slot:
            raise ValueError("inventory dictionary key does not match item slot")
        inventory.append(
            {
                "slot": slot.value,
                "template_id": item.template_id.value,
                "view": _plain_mapping(item.view, label=f"inventory slot {slot.value}"),
            }
        )

    pets = []
    for slot, pet in sorted(state.pets.items()):
        if slot != pet.slot:
            raise ValueError("pet dictionary key does not match pet slot")
        pets.append(
            {
                "slot": slot.value,
                "variant_id": pet.variant_id.value,
                "template_id": pet.template_id.value,
                "state": _plain_mapping(pet.state, label=f"pet slot {slot.value}"),
                "skills": [
                    {
                        "template_id": int(skill.template_id),
                        "view": _plain_mapping(
                            skill.view,
                            label=f"pet slot {slot.value} skill {skill.template_id}",
                        ),
                    }
                    for skill in pet.skills
                ],
            }
        )

    return {
        "schema": PERSISTENCE_SCHEMA,
        "character": character,
        "inventory": inventory,
        "pets": pets,
    }


def _require_exact_top_level(payload: Mapping[str, Any]) -> None:
    keys = set(payload)
    missing = _TOP_LEVEL_KEYS - keys
    extra = keys - _TOP_LEVEL_KEYS
    if missing:
        raise ValueError(f"persistent payload missing keys: {sorted(missing)}")
    if extra:
        raise ValueError(f"persistent payload has unknown keys: {sorted(extra)}")


def load_persistent_state(payload: Mapping[str, Any]) -> PersistentPlayerState:
    _require_exact_top_level(payload)
    if payload["schema"] != PERSISTENCE_SCHEMA:
        raise ValueError(f"unsupported persistence schema: {payload['schema']}")

    state = PersistentPlayerState()

    character = payload["character"]
    if character is not None:
        if not isinstance(character, Mapping):
            raise ValueError("character payload must be an object or null")
        state.character = PlayerState(MappingProxyType(dict(character)))

    seen_inventory: set[int] = set()
    inventory = payload["inventory"]
    if not isinstance(inventory, list):
        raise ValueError("inventory payload must be a list")
    for row in inventory:
        if not isinstance(row, Mapping):
            raise ValueError("inventory entry must be an object")
        if set(row) != {"slot", "template_id", "view"}:
            raise ValueError("inventory entry has unexpected shape")
        slot = InventorySlot(int(row["slot"]))
        if slot.value in seen_inventory:
            raise ValueError(f"duplicate inventory slot {slot.value}")
        seen_inventory.add(slot.value)
        if not isinstance(row["view"], Mapping):
            raise ValueError("inventory view must be an object")
        item = InventoryItem(
            slot=slot,
            template_id=ItemTemplateId(int(row["template_id"])),
            view=MappingProxyType(dict(row["view"])),
        )
        state.inventory[slot] = item

    seen_pets: set[int] = set()
    pets = payload["pets"]
    if not isinstance(pets, list):
        raise ValueError("pets payload must be a list")
    for row in pets:
        if not isinstance(row, Mapping):
            raise ValueError("pet entry must be an object")
        if set(row) != {
            "slot",
            "variant_id",
            "template_id",
            "state",
            "skills",
        }:
            raise ValueError("pet entry has unexpected shape")
        slot = PetSlot(int(row["slot"]))
        if slot.value in seen_pets:
            raise ValueError(f"duplicate pet slot {slot.value}")
        seen_pets.add(slot.value)
        if not isinstance(row["state"], Mapping):
            raise ValueError("pet state must be an object")
        if not isinstance(row["skills"], list):
            raise ValueError("pet skills must be a list")

        skills = []
        for skill_row in row["skills"]:
            if not isinstance(skill_row, Mapping):
                raise ValueError("pet skill entry must be an object")
            if set(skill_row) != {"template_id", "view"}:
                raise ValueError("pet skill entry has unexpected shape")
            if not isinstance(skill_row["view"], Mapping):
                raise ValueError("pet skill view must be an object")
            skills.append(
                PetSkill(
                    template_id=int(skill_row["template_id"]),
                    view=MappingProxyType(dict(skill_row["view"])),
                )
            )

        pet = PetActor(
            slot=slot,
            variant_id=EnemyVariantId(int(row["variant_id"])),
            template_id=PetTemplateId(int(row["template_id"])),
            runtime_object_id=None,
            state=MappingProxyType(dict(row["state"])),
            skills=tuple(skills),
        )
        state.pets[slot] = pet

    return state


def encode_persistent_state(state: PersistentPlayerState) -> str:
    return json.dumps(
        dump_persistent_state(state),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def decode_persistent_state(data: str) -> PersistentPlayerState:
    try:
        payload = json.loads(str(data))
    except json.JSONDecodeError as exc:
        raise ValueError("invalid persistence JSON") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("persistent payload root must be an object")
    return load_persistent_state(payload)


def restore_domain_persistent_state(
    domain: SinglePlayerHistoricalDomain,
    payload: Mapping[str, Any],
) -> PersistentPlayerState:
    restored = load_persistent_state(payload)
    domain.persistent = restored
    return restored
