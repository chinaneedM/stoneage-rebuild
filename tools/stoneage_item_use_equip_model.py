#!/usr/bin/env python3
"""Reference model for the convergent StoneAge item use/equip core."""

ITEM_OTHER = "other"
ITEM_DISH = "dish"

HEAD = 0
BODY = 1
ARM = 2
DECORATION1 = 3
DECORATION2 = 4
BASE_EQUIP_SLOTS = 5


def item_use_route(item_type):
    """Mirror CHAR_ItemUse's stable top-level type split."""
    return "use_callback" if item_type in {ITEM_OTHER, ITEM_DISH} else "equip"


def direct_move_packet_allowed(in_battle):
    """Direct client equip/inventory move packets are rejected during battle."""
    return not bool(in_battle)


def resolve_use_request(*, alive, item_valid, item_type, usefunc_present=True):
    """Return the stable high-level CHAR_ItemUse route."""
    if not alive:
        return {"accepted": False, "route": "none", "reason": "dead"}
    if not item_valid:
        return {"accepted": False, "route": "none", "reason": "invalid_item"}

    route = item_use_route(item_type)
    if route == "equip":
        return {
            "accepted": True,
            "route": "equip",
            "calls_usefunc": False,
            "reason": "equipment_type",
        }

    return {
        "accepted": True,
        "route": "use_callback" if usefunc_present else "nothing_happens",
        "calls_usefunc": bool(usefunc_present),
        "reason": "callback" if usefunc_present else "no_usefunc",
    }


def choose_use_equip_slot(item_equip_place, item_type, equipment):
    """Mirror the stable CHAR_ItemUse auto-slot choice.

    For non-decoration equipment the item's declared equip place is used.
    For decoration-class items, either decoration slot may be chosen, but the
    same ITEM_TYPE may not occupy both decoration slots.
    """
    equipment = tuple(equipment)
    if len(equipment) != BASE_EQUIP_SLOTS:
        raise ValueError("baseline equipment must contain five slots")

    item_equip_place = int(item_equip_place)
    if item_equip_place < 0:
        return -1

    if item_equip_place != DECORATION1:
        return item_equip_place

    left = equipment[DECORATION1]
    right = equipment[DECORATION2]

    def typ(value):
        if value is None:
            return None
        return value.get("type")

    if left is None and right is not None and item_type != typ(right):
        return DECORATION1
    if right is None and left is not None and item_type != typ(left):
        return DECORATION2

    if item_type != typ(right):
        return DECORATION1
    if item_type != typ(left):
        return DECORATION2
    return DECORATION1


def _equip_target_valid(item, to_slot, equipment):
    declared = int(item.get("equip_place", -1))
    if declared < 0:
        return False, "not_equippable"

    if declared == DECORATION1:
        if to_slot not in (DECORATION1, DECORATION2):
            return False, "wrong_slot"
        other_slot = DECORATION2 if to_slot == DECORATION1 else DECORATION1
        other = equipment[other_slot]
        if other is not None and other.get("type") == item.get("type"):
            return False, "duplicate_decoration_type"
        return True, "ok"

    if to_slot != declared:
        return False, "wrong_slot"
    return True, "ok"


def equip_level_gate(item_level, player_level, transmigration=0):
    """Common old gate: un-reborn characters must meet ITEM_LEVEL."""
    if int(transmigration) <= 0 and int(item_level) > int(player_level):
        return False
    return True


def move_bag_to_equip(
    *,
    equipment,
    bag,
    bag_index,
    equip_slot,
    player_level,
    transmigration=0,
):
    """Model the convergent bag->equip move including displacement.

    Optional later strength/dex/profession/rookie/token checks are deliberately
    outside this common model.
    """
    equipment = list(equipment)
    bag = list(bag)
    if len(equipment) != BASE_EQUIP_SLOTS:
        raise ValueError("baseline equipment must contain five slots")
    if bag_index < 0 or bag_index >= len(bag):
        raise ValueError("bag index out of range")
    if equip_slot < 0 or equip_slot >= BASE_EQUIP_SLOTS:
        raise ValueError("equip slot out of range")

    incoming = bag[bag_index]
    if incoming is None:
        return {
            "moved": False,
            "reason": "empty_source",
            "equipment": tuple(equipment),
            "bag": tuple(bag),
            "events": (),
            "recompute_parameters": True,
        }

    if not equip_level_gate(
        incoming.get("level", 0), player_level, transmigration
    ):
        return {
            "moved": False,
            "reason": "level_too_low",
            "equipment": tuple(equipment),
            "bag": tuple(bag),
            "events": (),
            "recompute_parameters": True,
        }

    valid, reason = _equip_target_valid(incoming, equip_slot, equipment)
    if not valid:
        return {
            "moved": False,
            "reason": reason,
            "equipment": tuple(equipment),
            "bag": tuple(bag),
            "events": (),
            "recompute_parameters": True,
        }

    displaced = equipment[equip_slot]
    equipment[equip_slot] = incoming
    bag[bag_index] = displaced

    events = []
    if displaced is not None:
        events.append(("detach", displaced.get("id")))
    events.append(("attach", incoming.get("id")))

    return {
        "moved": True,
        "reason": "equipped",
        "equipment": tuple(equipment),
        "bag": tuple(bag),
        "events": tuple(events),
        "recompute_parameters": True,
        "status_refresh": True,
    }


def move_equip_to_bag(
    *,
    equipment,
    bag,
    equip_slot,
    bag_index,
    player_level,
    transmigration=0,
):
    """Model equip->bag.

    If the target bag slot is occupied, the source does not simply overwrite it:
    the occupied bag item is instead attempted as an equip replacement in the
    source slot, reproducing the recursive exchange path.
    """
    equipment = list(equipment)
    bag = list(bag)
    if len(equipment) != BASE_EQUIP_SLOTS:
        raise ValueError("baseline equipment must contain five slots")
    if equip_slot < 0 or equip_slot >= BASE_EQUIP_SLOTS:
        raise ValueError("equip slot out of range")
    if bag_index < 0 or bag_index >= len(bag):
        raise ValueError("bag index out of range")

    outgoing = equipment[equip_slot]
    if outgoing is None:
        return {
            "moved": False,
            "reason": "empty_source",
            "equipment": tuple(equipment),
            "bag": tuple(bag),
            "events": (),
            "recompute_parameters": True,
        }

    if bag[bag_index] is None:
        equipment[equip_slot] = None
        bag[bag_index] = outgoing
        return {
            "moved": True,
            "reason": "unequipped",
            "equipment": tuple(equipment),
            "bag": tuple(bag),
            "events": (("detach", outgoing.get("id")),),
            "recompute_parameters": True,
            "status_refresh": True,
        }

    return move_bag_to_equip(
        equipment=equipment,
        bag=bag,
        bag_index=bag_index,
        equip_slot=equip_slot,
        player_level=player_level,
        transmigration=transmigration,
    )


def move_bag_to_bag(bag, from_index, to_index):
    """Baseline item-box behavior is a direct swap (stacking is optional later)."""
    bag = list(bag)
    if from_index < 0 or from_index >= len(bag):
        raise ValueError("from index out of range")
    if to_index < 0 or to_index >= len(bag):
        raise ValueError("to index out of range")
    if from_index == to_index or bag[from_index] is None:
        return {"moved": False, "bag": tuple(bag)}
    bag[from_index], bag[to_index] = bag[to_index], bag[from_index]
    return {"moved": True, "bag": tuple(bag)}


def direct_equip_to_equip_allowed():
    """CHAR_moveEquipItem rejects direct equipment-slot to equipment-slot moves."""
    return False
