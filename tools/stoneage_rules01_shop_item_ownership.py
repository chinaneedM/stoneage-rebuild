#!/usr/bin/env python3
"""A bounded DESIGN composition: descendant shop purchase -> persistent item.

This module deliberately DOES NOT recover a historical shop inventory, a
commercial-server save format, or an original quest reward. All source fields
must be explicitly supplied. It applies only the successful, single-item
ordinary shop path from the separately qualified descendant model.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from math import isfinite
from types import MappingProxyType
from typing import Any, Mapping

from tools.stoneage_item_shop_model import simulate_purchase
from tools.stoneage_local_runtime_core import LocalRuntimeSessionState
from tools.stoneage_singleplayer_domain import (
    InventoryItem, InventorySlot, ItemTemplateId, PersistentPlayerState, PlayerState,
)


@dataclass(frozen=True)
class ReferencePurchaseResult:
    session: LocalRuntimeSessionState
    purchased: bool
    reason: str
    item_slot: int | None
    total_price: int | None
    source_profile: str
    evidence_role: str


def apply_reference_normal_shop_purchase(
    session: LocalRuntimeSessionState,
    *,
    item_template_id: int,
    item_view: Mapping[str, Any],
    base_cost: int,
    buy_rate: float,
    inventory_capacity: int,
    source_ref: str,
    source_profile: str,
    evidence_role: str,
) -> ReferencePurchaseResult:
    """Compose one successful ordinary shop purchase with owned character data.

    The shop's exact item, cost, rate, slot capacity and evidence identity are
    mandatory inputs from a matching versioned source. A failed normal
    precondition is an unchanged state. This narrow adapter does not emulate
    allocator failure, bulk buy, partial legacy transaction side effects, item
    acquisition outside a shop, or a quest reward/consumption.
    """
    if not isinstance(session, LocalRuntimeSessionState):
        raise TypeError("reference purchase requires a local session")
    if (
        session.world_profile != "recovered25"
        or str(source_profile) != "recovered25"
        or str(evidence_role) != "LATER_RECOVERED"
    ):
        raise ValueError("reference shop purchase requires recovered25 LATER_RECOVERED scope")
    if not str(source_ref).strip():
        raise ValueError("shop source identity is required; no generic item source fallback")
    if not isinstance(item_view, Mapping):
        raise TypeError("item view must be provided as an explicit mapping")
    item_id = int(item_template_id)
    price_base = int(base_cost)
    rate = float(buy_rate)
    capacity = int(inventory_capacity)
    if item_id < 0 or price_base < 0 or not isfinite(rate) or rate < 0:
        raise ValueError("item/cost/rate input is invalid")
    if not 1 <= capacity <= 20:
        raise ValueError("inventory capacity must be explicit and within reference slot bounds")

    persistent = session.player_state
    if persistent.character is None or "gold" not in persistent.character.fields:
        raise ValueError("source-aligned current Stone/gold is required")
    gold = int(persistent.character.fields["gold"])
    if gold < 0:
        raise ValueError("current Stone cannot be negative")
    inventory = dict(persistent.inventory)
    if any(
        not isinstance(slot, InventorySlot)
        or not 0 <= slot.value < capacity
        or item.slot != slot
        for slot, item in inventory.items()
    ):
        raise ValueError("inventory slot identity/capacity drift")
    free_slots = [InventorySlot(i) for i in range(capacity) if InventorySlot(i) not in inventory]
    outcome = simulate_purchase(
        gold=gold,
        base_cost=price_base,
        requested_quantity=1,
        empty_inventory_slots=len(free_slots),
        buy_rate=rate,
    )
    if not outcome["success"]:
        return ReferencePurchaseResult(
            session, False, str(outcome["reason"]), None,
            outcome.get("total_price"), "recovered25", "LATER_RECOVERED",
        )

    if outcome["items_added"] != 1 or outcome["quantity"] != 1 or not free_slots:
        raise ValueError("single-item reference purchase cardinality drift")
    slot = free_slots[0]
    new_inventory = dict(inventory)
    new_inventory[slot] = InventoryItem(
        slot=slot,
        template_id=ItemTemplateId(item_id),
        view=MappingProxyType(dict(item_view)),
    )
    fields = dict(persistent.character.fields)
    fields["gold"] = int(outcome["gold_after"])
    updated_player = PersistentPlayerState(
        character=PlayerState(MappingProxyType(fields)),
        inventory=new_inventory,
        pets=dict(persistent.pets),
        dead_pet_count=persistent.dead_pet_count,
        default_pet_slot=persistent.default_pet_slot,
    )
    return ReferencePurchaseResult(
        replace(session, player_state=updated_player), True, "purchased", slot.value,
        int(outcome["total_price"]), "recovered25", "LATER_RECOVERED",
    )
