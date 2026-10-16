#!/usr/bin/env python3
"""RULES-01: source-bounded successful shop-to-owned-item reference join.

This is a modern deterministic evidence adapter for the recovered25 scenario,
NOT a claim about Taiwan-v1/JSS1999 shop inventories, original quest rewards,
or original commercial-server durability. The historical normal buy function
has non-atomic abnormal allocation failures; this adapter deliberately covers
only complete normal success and the two pre-mutation rejection cases.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from types import MappingProxyType
from typing import Any, Mapping

from tools.stoneage_item_shop_model import simulate_purchase
from tools.stoneage_local_runtime_core import LocalRuntimeSessionState
from tools.stoneage_singleplayer_domain import (
    InventoryItem, InventorySlot, ItemTemplateId, PlayerState,
)
from tools.stoneage_singleplayer_persistence import (
    decode_persistent_state, encode_persistent_state,
)


@dataclass(frozen=True)
class BoundedOrdinaryShopOffer:
    """All concrete values are caller-supplied; no historical IDs are guessed."""

    source_profile: str
    evidence_role: str
    source_receipt: str
    offered_item_id: int
    selected_item_id: int
    item_view: Mapping[str, Any]
    base_cost: int
    buy_rate: float
    usable_slot_count: int
    override_cost: int | None = None

    def __post_init__(self) -> None:
        if self.source_profile != "recovered25" or self.evidence_role != "LATER_RECOVERED":
            raise ValueError("ordinary shop join requires explicit later recovered25 provenance")
        if not str(self.source_receipt).strip():
            raise ValueError("source receipt or explicitly labeled test fixture is required")
        if int(self.offered_item_id) != int(self.selected_item_id):
            raise ValueError("chosen item must match the supplied shop offer")
        if int(self.selected_item_id) < 0:
            raise ValueError("item id must be nonnegative")
        if int(self.base_cost) < 0 or (
            self.override_cost is not None and int(self.override_cost) < 0
        ):
            raise ValueError("shop cost must be nonnegative")
        rate = float(self.buy_rate)
        if not math.isfinite(rate) or rate < 0:
            raise ValueError("buy rate must be finite and nonnegative")
        capacity = int(self.usable_slot_count)
        if capacity < 1 or capacity > 20:
            raise ValueError("usable inventory capacity must be explicitly within 1..20")
        if not isinstance(self.item_view, Mapping):
            raise ValueError("item client-view values must be supplied as a mapping")
        try:
            json.dumps(dict(self.item_view), allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError("item client view must be JSON-serializable") from exc


@dataclass(frozen=True)
class BoundedPurchaseResult:
    session: LocalRuntimeSessionState
    purchased: bool
    reason: str
    inventory_slot: int | None
    source_profile: str = "recovered25"
    evidence_role: str = "LATER_RECOVERED"
    original_commercial_save_proven: bool = False
    original_quest_award_proven: bool = False


def apply_normal_single_item_purchase(
    session: LocalRuntimeSessionState, offer: BoundedOrdinaryShopOffer
) -> BoundedPurchaseResult:
    """Join source-shaped normal buy outcome to modern persistent item ownership.

    The exact item, shop rate, capacity, item view and source/fixture identity
    must be supplied. No implicit reward, warp, fee payment or server save occurs.
    """
    if session.world_profile != offer.source_profile:
        raise ValueError("purchase source profile differs from current world")
    persistent = session.player_state
    if persistent.character is None or "gold" not in persistent.character.fields:
        raise ValueError("current authoritative Stone/gold state is unavailable")
    gold = int(persistent.character.fields["gold"])
    if gold < 0:
        raise ValueError("negative current Stone/gold cannot be a valid purchase input")
    used = set()
    for slot, item in persistent.inventory.items():
        index = int(slot.value)
        if not 0 <= index < offer.usable_slot_count or slot != item.slot:
            raise ValueError("inventory contains an invalid occupied source slot")
        used.add(index)
    free = [i for i in range(offer.usable_slot_count) if i not in used]
    outcome = simulate_purchase(
        gold=gold,
        base_cost=int(offer.base_cost),
        requested_quantity=1,
        empty_inventory_slots=len(free),
        buy_rate=float(offer.buy_rate),
        override_cost=(
            None if offer.override_cost is None else int(offer.override_cost)
        ),
    )
    if not outcome["success"]:
        return BoundedPurchaseResult(
            session=session, purchased=False, reason=outcome["reason"], inventory_slot=None
        )
    if outcome["quantity"] != 1 or outcome["items_added"] != 1 or not free:
        raise AssertionError("normal single-item purchase invariant violated")

    # Clone before any mutation: an old-server partial-create case is not
    # representable as a successful modern inventory mutation.
    from dataclasses import replace

    state = decode_persistent_state(encode_persistent_state(persistent))
    slot = InventorySlot(free[0])
    state.inventory[slot] = InventoryItem(
        slot=slot,
        template_id=ItemTemplateId(int(offer.selected_item_id)),
        view=MappingProxyType(dict(offer.item_view)),
    )
    values = dict(state.character.fields)
    values["gold"] = int(outcome["gold_after"])
    state.character = PlayerState(MappingProxyType(values))
    return BoundedPurchaseResult(
        session=replace(session, player_state=state),
        purchased=True,
        reason="normal_purchase_complete",
        inventory_slot=slot.value,
    )
