#!/usr/bin/env python3
"""Reference model for the convergent StoneAge direct player-trade core."""

from dataclasses import dataclass, replace
from math import floor

TRADE_FREE = 0
TRADE_SENDING = 1
TRADE_TRADING = 2
TRADE_LOCK = 3

MAX_TRADE_ITEMS = 15
MAX_TRADE_PETS = 5

PROTOCOL_OLD = "old"
PROTOCOL_TRADESYSTEM2 = "tradesystem2"


@dataclass(frozen=True)
class TradeSide:
    mode: int = TRADE_FREE
    confirmed: bool = False
    locked: bool = False


@dataclass(frozen=True)
class ItemOffer:
    slot: int
    quantity: int
    stack_count: int
    valid: bool = True


@dataclass(frozen=True)
class PetOffer:
    slot: int
    level: int
    valid: bool = True
    family_guardian: bool = False


@dataclass(frozen=True)
class Offer:
    items: tuple = ()
    pets: tuple = ()
    gold: int = 0


def begin_trade():
    """Fixed active descendants enter TRADING directly; SENDING is dormant."""
    return (
        TradeSide(mode=TRADE_TRADING, confirmed=False, locked=False),
        TradeSide(mode=TRADE_TRADING, confirmed=False, locked=False),
    )


def can_search_trade(*, mode, in_party, in_battle):
    """Stable initiator gates in TRADE_Search."""
    return (
        int(mode) not in (TRADE_TRADING, TRADE_LOCK)
        and not bool(in_party)
        and not bool(in_battle)
    )


def target_trade_eligible(
    *,
    is_player,
    is_self,
    in_party,
    in_battle,
    trade_enabled,
    mode,
):
    return (
        bool(is_player)
        and not bool(is_self)
        and not bool(in_party)
        and not bool(in_battle)
        and bool(trade_enabled)
        and int(mode) == TRADE_FREE
    )


def can_modify_offer(side):
    """Once this side confirms, item/pet/gold handlers reject further edits."""
    return side.mode == TRADE_TRADING and not side.confirmed


def confirm(side):
    if side.mode != TRADE_TRADING or side.confirmed:
        return side
    return replace(side, confirmed=True)


def request_final_lock(side, other, protocol=PROTOCOL_TRADESYSTEM2):
    """Model the two preserved finalization variants.

    New TRADESYSTEM2:
      - both must already be confirmed;
      - each side separately enters LOCK;
      - execute only when both modes are LOCK.

    Older/simplified branch:
      - if this side is not yet confirmed, the K action confirms it;
      - after both confirms are true, the next K locks the sender and executes
        without requiring the peer's mode to be LOCK.
    """
    if protocol not in (PROTOCOL_OLD, PROTOCOL_TRADESYSTEM2):
        raise ValueError("unknown protocol")

    if protocol == PROTOCOL_OLD:
        if not side.confirmed:
            return replace(side, confirmed=True), False
        if not other.confirmed:
            return side, False
        if side.mode == TRADE_LOCK:
            return side, False
        return replace(side, mode=TRADE_LOCK, locked=True), True

    if not side.confirmed or not other.confirmed:
        return side, False
    if side.mode == TRADE_LOCK:
        return side, False
    side = replace(side, mode=TRADE_LOCK, locked=True)
    execute = other.mode == TRADE_LOCK
    return side, execute


def cancel_trade():
    """Close/cancel resets both logical sides and their confirmation state."""
    free = TradeSide(mode=TRADE_FREE, confirmed=False, locked=False)
    return free, free


def validate_gold_offer(offered, carried):
    offered = int(offered)
    carried = int(carried)
    return 0 <= offered <= carried


def validate_pet_offer(
    pet,
    *,
    receiver_level,
    receiver_transmigration=0,
    receiver_pick_all_pet=False,
    max_level_delta=5,
):
    """Common older care gate; Bismarck later changed the delta to +20."""
    if not pet.valid or pet.family_guardian:
        return False
    if receiver_pick_all_pet:
        return True
    if int(receiver_transmigration) > 0:
        return True
    return int(pet.level) <= int(receiver_level) + int(max_level_delta)


def validate_structured_offer(offer):
    if len(offer.items) > MAX_TRADE_ITEMS:
        return False
    if len(offer.pets) > MAX_TRADE_PETS:
        return False
    if int(offer.gold) < 0:
        return False
    for item in offer.items:
        if not item.valid or item.quantity <= 0 or item.quantity > item.stack_count:
            return False
    slots = [p.slot for p in offer.pets]
    if len(set(slots)) != len(slots):
        return False
    return all(p.valid for p in offer.pets)


def source_item_slots_freed(offer):
    """Only a fully offered stack frees its sender inventory slot."""
    return sum(
        1
        for item in offer.items
        if item.valid and int(item.quantity) == int(item.stack_count)
    )


def incoming_item_slots_needed_source(quantity, receiver_max_pile):
    """Mirror TRADE_CheckTradeList literally.

    Source code uses (quantity / maxPile) + 1 when quantity > maxPile.
    This over-counts exact multiples (e.g. 20 with maxPile 10 -> 3).
    """
    quantity = int(quantity)
    receiver_max_pile = int(receiver_max_pile)
    if quantity <= 0 or receiver_max_pile <= 0:
        raise ValueError("positive quantity/max pile required")
    if quantity > receiver_max_pile:
        return quantity // receiver_max_pile + 1
    return 1


def item_slots_needed_for_offer(offer, receiver_max_pile):
    return sum(
        incoming_item_slots_needed_source(item.quantity, receiver_max_pile)
        for item in offer.items
    )


def preflight_trade(
    *,
    left_offer,
    right_offer,
    left_empty_item_slots,
    right_empty_item_slots,
    left_max_pile,
    right_max_pile,
    left_empty_pet_slots,
    right_empty_pet_slots,
    left_gold,
    right_gold,
    left_max_gold,
    right_max_gold,
):
    """Mirror the structured trade preflight used before destructive transfer."""
    if not validate_structured_offer(left_offer):
        return False, "left_offer_invalid"
    if not validate_structured_offer(right_offer):
        return False, "right_offer_invalid"

    left_item_capacity = int(left_empty_item_slots) + source_item_slots_freed(left_offer)
    right_item_capacity = int(right_empty_item_slots) + source_item_slots_freed(right_offer)

    left_item_need = item_slots_needed_for_offer(right_offer, left_max_pile)
    right_item_need = item_slots_needed_for_offer(left_offer, right_max_pile)

    if left_item_capacity < left_item_need:
        return False, "left_item_full"
    if right_item_capacity < right_item_need:
        return False, "right_item_full"

    left_pet_capacity = int(left_empty_pet_slots) + len(left_offer.pets)
    right_pet_capacity = int(right_empty_pet_slots) + len(right_offer.pets)
    if left_pet_capacity < len(right_offer.pets):
        return False, "left_pet_full"
    if right_pet_capacity < len(left_offer.pets):
        return False, "right_pet_full"

    left_gold_room = int(left_max_gold) - int(left_gold) + int(left_offer.gold)
    right_gold_room = int(right_max_gold) - int(right_gold) + int(right_offer.gold)
    if left_gold_room < int(right_offer.gold):
        return False, "left_gold_overflow"
    if right_gold_room < int(left_offer.gold):
        return False, "right_gold_overflow"

    return True, "ok"


def final_gold_balances(
    left_gold, right_gold, left_offer_gold, right_offer_gold
):
    """Successful transfer is simultaneous in intent, netting each side's offers."""
    return (
        int(left_gold) - int(left_offer_gold) + int(right_offer_gold),
        int(right_gold) - int(right_offer_gold) + int(left_offer_gold),
    )


def structured_mutation_order():
    """Executed order in TRADE_HandleTrade; no rollback journal exists."""
    return (
        "remove_left_items",
        "remove_right_items",
        "remove_left_pets",
        "remove_right_pets",
        "subtract_left_gold",
        "subtract_right_gold",
        "add_items_to_left",
        "add_items_to_right",
        "add_pets_to_left",
        "add_pets_to_right",
        "add_gold_to_left",
        "add_gold_to_right",
    )


def is_transactionally_atomic():
    """Preflight reduces failure risk, but execution has no rollback transaction."""
    return False


def transfer_pet_owner(pet, new_owner_id, new_owner_cdkey, new_owner_name):
    out = dict(pet)
    out["player_index"] = int(new_owner_id)
    out["owner_cdkey"] = new_owner_cdkey
    out["owner_name"] = new_owner_name
    out["parameters_recomputed"] = True
    return out
