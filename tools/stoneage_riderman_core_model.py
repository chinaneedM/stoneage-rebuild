#!/usr/bin/env python3
"""Deterministic reference model for the StoneAge Riderman core."""

RECOVERED_TUITION = {
    6: 5000,
    7: 10000,
    8: 15000,
    9: 20000,
}

TARGET_LEVEL = {
    6: 40,
    7: 80,
    8: 120,
    9: 200,
}

PREREQ_LEVEL = {
    6: 0,
    7: 40,
    8: 80,
    9: 120,
}


def _c_div(a, b):
    a = int(a)
    b = int(b)
    if b == 0:
        raise ZeroDivisionError
    q = abs(a) // abs(b)
    return -q if (a < 0) ^ (b < 0) else q


def family_revenue_share(tuition):
    """Common post-success extension: one fifth, C integer division."""
    return _c_div(tuition, 5)


def trainer_gate(learnride, action, lineage="gavin"):
    learnride = int(learnride)
    action = int(action)
    if action not in TARGET_LEVEL:
        return {"allowed": False, "reason": "not_training_action"}

    target = TARGET_LEVEL[action]
    prereq = PREREQ_LEVEL[action]

    if action in (6, 7, 8):
        if learnride >= target:
            return {"allowed": False, "reason": "already_learned"}
        if learnride < prereq:
            return {"allowed": False, "reason": "missing_prerequisite"}
        return {"allowed": True, "reason": "eligible"}

    # Special class diverges by fixed descendant.
    if lineage in ("gavin", "iriselia"):
        if learnride > 120:
            return {"allowed": False, "reason": "already_learned"}
        if learnride < 120:
            return {"allowed": False, "reason": "missing_prerequisite"}
        return {"allowed": True, "reason": "eligible"}

    if lineage == "bismarck":
        if learnride > 200:
            return {"allowed": False, "reason": "already_learned"}
        if learnride < 120:
            return {"allowed": False, "reason": "missing_prerequisite"}
        return {"allowed": True, "reason": "eligible"}

    raise ValueError("lineage must be gavin, iriselia, or bismarck")


def trainer_transaction(
    *,
    learnride,
    gold,
    action,
    tuition,
    lineage="gavin",
    matching_village_family=False,
):
    gate = trainer_gate(learnride, action, lineage)
    if not gate["allowed"]:
        return {
            "success": False,
            "reason": gate["reason"],
            "learnride_after": int(learnride),
            "gold_after": int(gold),
            "family_credit": 0,
        }

    tuition = int(tuition)
    gold = int(gold)
    if gold < tuition:
        return {
            "success": False,
            "reason": "insufficient_stone",
            "learnride_after": int(learnride),
            "gold_after": gold,
            "family_credit": 0,
        }

    return {
        "success": True,
        "reason": "trained",
        "learnride_after": TARGET_LEVEL[int(action)],
        "gold_after": gold - tuition,
        "family_credit": (
            family_revenue_share(tuition)
            if matching_village_family else 0
        ),
        "events": (
            "deduct_stone",
            "set_learnride",
            "refresh_gold_status",
            "refresh_learnride_status",
            "optional_family_revenue",
        ),
    }


def common_mount_gate(
    *,
    valid_character,
    battle_free,
    valid_pet,
    already_riding,
    learnride,
    pet_level,
    pet_loyalty,
    player_level,
    direct_mapping_exists,
):
    """Intersection of the fixed descendant native riding gates.

    Versioned gates such as pet-transmigration limits, NEW_RIDEPETS fallback,
    default-pet treatment, trade-mode checks and other fork extensions are
    intentionally outside this common gate.
    """
    if not valid_character:
        return {"allowed": False, "reason": "invalid_character"}
    if not battle_free:
        return {"allowed": False, "reason": "in_battle"}
    if not valid_pet:
        return {"allowed": False, "reason": "invalid_pet"}
    if already_riding:
        return {"allowed": False, "reason": "already_riding"}
    if int(learnride) < int(pet_level):
        return {"allowed": False, "reason": "training_limit"}
    if int(pet_loyalty) < 100:
        return {"allowed": False, "reason": "loyalty"}
    if int(player_level) + 5 < int(pet_level):
        return {"allowed": False, "reason": "player_level_gap"}
    if not direct_mapping_exists:
        return {"allowed": False, "reason": "no_ride_mapping"}
    return {"allowed": True, "reason": "eligible"}


def mount_apply(*, pet_slot, ride_graphic):
    return {
        "ridepet_after": int(pet_slot),
        "base_image_after": int(ride_graphic),
        "recompute_parameters": True,
        "broadcast_character": True,
        "refresh_ride_status": True,
    }


def dismount_apply(*, base_base_image):
    return {
        "ridepet_after": -1,
        "base_image_after": int(base_base_image),
        "recompute_parameters": True,
        "broadcast_character": True,
        "refresh_ride_status": True,
    }


def transmigration_preserves_learnride():
    """The fixed descendant transmigration path leaves reset commented out."""
    return True
