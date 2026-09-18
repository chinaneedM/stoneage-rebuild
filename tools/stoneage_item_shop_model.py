#!/usr/bin/env python3
"""Reference model for the convergent StoneAge NPC item-shop core."""

from dataclasses import dataclass


ACCESSORY_TYPES = frozenset(range(8, 16))
OFFENCE_TYPES = frozenset((*range(0, 5), *range(17, 20)))
DEFENCE_TYPES = frozenset(range(5, 8))


@dataclass(frozen=True)
class ShopItem:
    item_id: int
    item_type: int
    base_cost: int
    stack_count: int = 1


def buy_unit_price(base_cost, buy_rate=1.0, override_cost=None):
    """Source semantics: choose base/override cost, multiply, truncate to int."""
    cost = int(base_cost) if override_cost is None else int(override_cost)
    return int(cost * float(buy_rate))


def clamp_purchase_quantity(requested, empty_inventory_slots):
    """NPC_SetNewItem silently reduces requested count to current empty slots."""
    requested = int(requested)
    empty_inventory_slots = int(empty_inventory_slots)
    if requested <= 0 or empty_inventory_slots <= 0:
        return 0
    return min(requested, empty_inventory_slots)


def purchase_total(base_cost, quantity, buy_rate=1.0, override_cost=None):
    unit = buy_unit_price(base_cost, buy_rate, override_cost)
    return unit * int(quantity)


def can_afford_purchase(gold, total_price):
    return int(gold) >= int(total_price)


def simulate_purchase(
    *,
    gold,
    base_cost,
    requested_quantity,
    empty_inventory_slots,
    buy_rate=1.0,
    override_cost=None,
    fail_create_at=None,
    fail_add_at=None,
):
    """Model NPC_SetNewItem + NPC_AddItemBuy ordering.

    fail_create_at/fail_add_at are zero-based failure-injection points used to
    expose the old server's lack of rollback. Gold is deducted only after every
    requested item has been created and inserted successfully.
    """
    quantity = clamp_purchase_quantity(requested_quantity, empty_inventory_slots)
    if quantity <= 0:
        return {
            "success": False,
            "reason": "no_capacity_or_invalid_quantity",
            "quantity": 0,
            "items_added": 0,
            "gold_after": int(gold),
        }

    total = purchase_total(base_cost, quantity, buy_rate, override_cost)
    if not can_afford_purchase(gold, total):
        return {
            "success": False,
            "reason": "not_enough_gold",
            "quantity": quantity,
            "items_added": 0,
            "gold_after": int(gold),
            "total_price": total,
        }

    added = 0
    for i in range(quantity):
        if fail_create_at is not None and i == int(fail_create_at):
            return {
                "success": False,
                "reason": "item_creation_failed",
                "quantity": quantity,
                "items_added": added,
                "gold_after": int(gold),
                "total_price": total,
            }
        if fail_add_at is not None and i == int(fail_add_at):
            return {
                "success": False,
                "reason": "inventory_insert_failed",
                "quantity": quantity,
                "items_added": added,
                "gold_after": int(gold),
                "total_price": total,
            }
        added += 1

    return {
        "success": True,
        "reason": "purchased",
        "quantity": quantity,
        "items_added": added,
        "gold_after": int(gold) - total,
        "total_price": total,
    }


def _id_in_specs(item_id, specs):
    """Match exact IDs or inclusive (start,end) ranges."""
    item_id = int(item_id)
    for spec in specs:
        if isinstance(spec, int):
            if item_id == spec:
                return True
        else:
            start, end = map(int, spec)
            if start > end:
                start, end = end, start
            if start <= item_id <= end:
                return True
    return False


def _type_matches_label(item_type, label):
    item_type = int(item_type)
    label = str(label).upper()
    if label == "ACCESSORY":
        return item_type in ACCESSORY_TYPES
    if label == "OFFENCE":
        return item_type in OFFENCE_TYPES
    if label == "DEFENCE":
        return item_type in DEFENCE_TYPES
    return False


def sell_whitelisted(
    item,
    *,
    limit_item_types=(),
    exact_type_labels=None,
    limit_item_ids=(),
):
    """Model the whitelist role of LimitItemType / LimitItemNo.

    exact_type_labels maps symbolic shop labels (e.g. AXE/RING) to numeric
    ITEM_TYPE values supplied by the version's TypeTable.
    """
    exact_type_labels = exact_type_labels or {}
    for label in limit_item_types:
        label_u = str(label).upper()
        if _type_matches_label(item.item_type, label_u):
            return True
        if label_u in exact_type_labels and int(item.item_type) == int(
            exact_type_labels[label_u]
        ):
            return True
    return _id_in_specs(item.item_id, limit_item_ids)


def sell_unit_price(
    item_cost,
    *,
    normal_sell_rate=None,
    is_special_item=False,
    special_rate=None,
):
    """Return sale price, or None when no applicable price rule exists.

    A matched special_item defaults to 1.2 when special_rate is absent.
    Ordinary items require an explicit sell_rate in the NPC configuration.
    """
    if is_special_item:
        rate = 1.2 if special_rate is None else float(special_rate)
        return int(int(item_cost) * rate)
    if normal_sell_rate is None:
        return None
    return int(int(item_cost) * float(normal_sell_rate))


def can_receive_sale_gold(current_gold, proceeds, max_gold):
    """NPC_SellNewItem rejects >= MAX, so exact-cap sales are rejected."""
    return int(current_gold) + int(proceeds) < int(max_gold)


def simulate_sale(
    *,
    item,
    sell_quantity,
    current_gold,
    max_gold,
    whitelisted,
    normal_sell_rate=None,
    is_special_item=False,
    special_rate=None,
):
    """Model the stable sell path: validate -> delete/decrement -> add gold."""
    sell_quantity = int(sell_quantity)
    if sell_quantity <= 0 or sell_quantity > int(item.stack_count):
        return {
            "success": False,
            "reason": "invalid_quantity",
            "gold_after": int(current_gold),
            "stack_after": int(item.stack_count),
        }
    if not bool(whitelisted):
        return {
            "success": False,
            "reason": "not_whitelisted",
            "gold_after": int(current_gold),
            "stack_after": int(item.stack_count),
        }

    unit = sell_unit_price(
        item.base_cost,
        normal_sell_rate=normal_sell_rate,
        is_special_item=is_special_item,
        special_rate=special_rate,
    )
    if unit is None:
        return {
            "success": False,
            "reason": "no_sell_rate",
            "gold_after": int(current_gold),
            "stack_after": int(item.stack_count),
        }

    proceeds = unit * sell_quantity
    if not can_receive_sale_gold(current_gold, proceeds, max_gold):
        return {
            "success": False,
            "reason": "gold_cap",
            "gold_after": int(current_gold),
            "stack_after": int(item.stack_count),
            "proceeds": proceeds,
        }

    stack_after = int(item.stack_count) - sell_quantity
    return {
        "success": True,
        "reason": "sold",
        "unit_price": unit,
        "proceeds": proceeds,
        "gold_after": int(current_gold) + proceeds,
        "stack_after": stack_after,
        "item_instance_deleted": stack_after <= 0,
        "mutation_order": ("delete_or_decrement_item", "add_gold"),
    }


def buy_mutation_order():
    return ("create_and_insert_each_item", "deduct_total_gold")


def sell_mutation_order():
    return ("delete_or_decrement_item", "add_gold")


def buy_is_transactionally_atomic():
    return False
