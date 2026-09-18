#!/usr/bin/env python3
"""Deterministic reference model for StoneAge ordinary item/pet pool storage.

This models the fixed-descendant server behavior at the state-transition level.
It deliberately keeps later account-shared Depot warehouses separate.
"""

DEFAULT_ITEM_POOL_MAX = 20
DEFAULT_PET_POOL_MAX = 10
CARRIED_PET_MAX = 5
DEFAULT_ITEM_POOL_COST = 200


def pet_pool_capacity(transmigration, max_slots=DEFAULT_PET_POOL_MAX):
    """Fixed-source usable ordinary pet-pool slots: 5 + 2 per transmigration."""
    return min(int(max_slots), int(transmigration) * 2 + 5)


def item_pool_capacity(transmigration, max_slots=DEFAULT_ITEM_POOL_MAX):
    """Fixed-source usable ordinary item-pool slots: 10 + 4 per transmigration."""
    return min(int(max_slots), int(transmigration) * 4 + 10)


def pet_pool_cost(level):
    """NPC_GETPOOLCOST in the inspected fixed pet-shop descendants."""
    return 50 + int(level) * 4


def first_empty(slots, limit=None):
    if limit is None:
        limit = len(slots)
    limit = min(int(limit), len(slots))
    for i in range(limit):
        if slots[i] is None:
            return i
    return -1


def compact(slots):
    occupied = [value for value in slots if value is not None]
    return occupied + [None] * (len(slots) - len(occupied))


def item_ui_marks_nonpoolable(*, drop_at_logout, vanish_at_drop, can_petmail):
    """The ordinary pool-item UI marks these items as unavailable."""
    return bool(drop_at_logout) or bool(vanish_at_drop) or not bool(can_petmail)


def deposit_item_pool_handler(
    *,
    carried,
    pool,
    selected_slot,
    transmigration,
    gold,
    cost=DEFAULT_ITEM_POOL_COST,
):
    """Mirror the authoritative ordinary pool-item handler.

    Historical quirk: CHAR_DelGold's return value is ignored. If gold is
    insufficient the item is still moved after the failed debit.
    """
    carried = list(carried)
    pool = list(pool)
    selected_slot = int(selected_slot)
    if selected_slot < 0 or selected_slot >= len(carried):
        return {"ok": False, "reason": "invalid_carried_slot"}
    item = carried[selected_slot]
    if item is None:
        return {"ok": False, "reason": "invalid_item"}

    empty = first_empty(pool, item_pool_capacity(transmigration, len(pool)))
    if empty == -1:
        return {"ok": False, "reason": "pool_full"}

    gold = int(gold)
    cost = int(cost)
    payment_succeeded = gold >= cost
    if payment_succeeded:
        gold -= cost

    pool[empty] = item
    carried[selected_slot] = None
    return {
        "ok": True,
        "reason": "stored",
        "carried": tuple(carried),
        "pool": tuple(pool),
        "gold": gold,
        "payment_succeeded": payment_succeeded,
        "historical_unpaid_move": not payment_succeeded,
        "stored_slot": empty,
    }


def withdraw_item_pool(*, carried, pool, selected_pool_slot):
    carried = list(carried)
    pool = list(pool)
    selected_pool_slot = int(selected_pool_slot)

    empty = first_empty(carried)
    if empty == -1:
        return {"ok": False, "reason": "carried_full"}
    if selected_pool_slot < 0 or selected_pool_slot >= len(pool):
        return {"ok": False, "reason": "invalid_pool_slot"}
    item = pool[selected_pool_slot]
    if item is None:
        return {"ok": False, "reason": "invalid_item"}

    carried[empty] = item
    pool[selected_pool_slot] = None
    pool = compact(pool)
    return {
        "ok": True,
        "reason": "withdrawn",
        "carried": tuple(carried),
        "pool": tuple(pool),
        "carried_slot": empty,
    }


def deposit_pet_pool(
    *,
    carried,
    pool,
    selected_slot,
    transmigration,
    level,
    gold,
    default_pet_slot=-1,
    ride_pet_slot=-1,
    pool_enabled=True,
):
    """Model the ordinary pet-shop deposit path including its WN preflight."""
    carried = list(carried)
    pool = list(pool)
    selected_slot = int(selected_slot)

    if not pool_enabled:
        return {"ok": False, "reason": "pool_disabled"}
    if selected_slot < 0 or selected_slot >= len(carried):
        return {"ok": False, "reason": "invalid_carried_slot"}
    pet = carried[selected_slot]
    if pet is None:
        return {"ok": False, "reason": "invalid_pet"}
    if selected_slot == int(ride_pet_slot):
        return {"ok": False, "reason": "riding_pet"}

    cost = pet_pool_cost(level)
    if int(gold) < cost:
        return {"ok": False, "reason": "insufficient_gold", "cost": cost}

    empty = first_empty(pool, pet_pool_capacity(transmigration, len(pool)))
    if empty == -1:
        return {"ok": False, "reason": "pool_full", "cost": cost}

    carried[selected_slot] = None
    pool[empty] = pet
    default_pet_slot = -1 if int(default_pet_slot) == selected_slot else int(default_pet_slot)
    return {
        "ok": True,
        "reason": "stored",
        "carried": tuple(carried),
        "pool": tuple(pool),
        "gold": int(gold) - cost,
        "cost": cost,
        "default_pet_slot": default_pet_slot,
        "stored_slot": empty,
    }


def withdraw_pet_pool(*, carried, pool, selected_pool_slot):
    carried = list(carried)
    pool = list(pool)
    selected_pool_slot = int(selected_pool_slot)

    empty = first_empty(carried, CARRIED_PET_MAX)
    if empty == -1:
        return {"ok": False, "reason": "carried_full"}
    if selected_pool_slot < 0 or selected_pool_slot >= len(pool):
        return {"ok": False, "reason": "invalid_pool_slot"}
    pet = pool[selected_pool_slot]
    if pet is None:
        return {"ok": False, "reason": "invalid_pet"}

    carried[empty] = pet
    pool[selected_pool_slot] = None
    pool = compact(pool)
    return {
        "ok": True,
        "reason": "withdrawn",
        "carried": tuple(carried),
        "pool": tuple(pool),
        "carried_slot": empty,
    }


def later_depot_item_deposit_allowed(
    *,
    drop_at_logout,
    vanish_at_drop,
    can_petmail,
    enough_gold,
):
    """Later shared Depot path rechecks restrictions and payment server-side."""
    if item_ui_marks_nonpoolable(
        drop_at_logout=drop_at_logout,
        vanish_at_drop=vanish_at_drop,
        can_petmail=can_petmail,
    ):
        return False
    return bool(enough_gold)


def persistence_domains():
    """Separate ordinary character-inline pools from later shared Depot data."""
    return {
        "character_inline": ("pool_items", "pool_pets"),
        "later_shared_depot": ("depot_items", "depot_pets"),
    }
