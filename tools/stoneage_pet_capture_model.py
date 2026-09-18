#!/usr/bin/env python3
"""Reference model for the convergent StoneAge pet-capture core."""

import math

MAX_PETS = 5
NOMINAL_CAPTURE_MPDOWN_ARGUMENT = 20
ACTIVE_CAPTURE_MP_COST = 0

COMMON_CAPTURE_COPY_FIELDS = (
    "base_image",
    "hp",
    "mp",
    "max_mp",
    "vital",
    "strength",
    "toughness",
    "dexterity",
    "luck",
    "fire",
    "water",
    "earth",
    "wind",
    "skill_slots",
    "mod_ai",
    "level",
    "poison",
    "paralysis",
    "sleep",
    "stone",
    "drunk",
    "confusion",
    "rare",
    "pet_rank",
    "pet_id",
    "critical",
    "counter",
    "pet_skills",
    "alloc_point",
    "name",
)


def capture_basic_gate(
    *,
    target_is_enemy,
    target_pet_flag,
    attacker_level,
    target_level,
    pick_all_pet=False,
):
    """Mirror the stable target/type/level gate in BATTLE_CaptureCheck."""
    if not target_is_enemy:
        return False, "target_not_enemy"
    if int(target_pet_flag) == 0:
        return False, "target_not_capturable"
    if not pick_all_pet and int(attacker_level) + 5 < int(target_level):
        return False, "target_level_too_high"
    return True, "ok"


def required_items_satisfied(required_item_ids, inventory_item_ids):
    """Model the stable logical requirement without hardcoding versioned tables."""
    inventory = tuple(int(v) for v in inventory_item_ids)
    return all(int(required) in inventory for required in required_item_ids)


def consume_required_items_on_success(required_item_ids, inventory_item_ids):
    """Mirror the descendant success path: delete all matching condition items."""
    required = {int(v) for v in required_item_ids}
    inventory = tuple(int(v) for v in inventory_item_ids)
    consumed = tuple(v for v in inventory if v in required)
    remaining = tuple(v for v in inventory if v not in required)
    return remaining, consumed


def capture_score(
    *,
    attacker_charm,
    attacker_level,
    attacker_dex,
    attacker_luck,
    target_level,
    target_dex,
    target_capture_default,
    target_hp,
    target_max_hp,
    temp_capture_mod=0,
    target_sleep=0,
):
    """Compute the preserved BATTLE_CaptureCheck WorkGet value literally."""
    max_hp = float(target_max_hp)
    if max_hp <= 0:
        max_hp = 1.0

    hp = float(target_hp)
    hp_term = 10.0 - (hp * hp) / max_hp
    level_term = float(attacker_level) / 2.0 - float(target_level) / 2.0
    dex_term = float(attacker_dex) / 15.0 - float(target_dex) / 15.0

    score = (
        hp_term
        + level_term
        + dex_term
        + float(target_capture_default)
        + float(attacker_luck)
    ) * float(attacker_charm) / 50.0

    score += float(temp_capture_mod)
    if float(target_sleep) > 0:
        score += 15.0

    if score > 99.0:
        score = 99.0
    return score


def capture_roll_success(score, roll):
    """Mirror RAND(1,100) < WorkGet."""
    roll = int(roll)
    if roll < 1 or roll > 100:
        raise ValueError("roll must be an integer in 1..100")
    return float(roll) < float(score)


def effective_success_roll_count(score):
    """Number of integer RAND(1,100) outcomes that satisfy roll < score."""
    score = float(score)
    return max(0, min(100, math.ceil(score) - 1))


def first_empty_pet_slot(pet_slots):
    """Return the first ordinary carried-pet slot, or -1 when all five are full."""
    slots = tuple(pet_slots)
    if len(slots) != MAX_PETS:
        raise ValueError("ordinary pet roster must contain exactly five slots")
    for index, value in enumerate(slots):
        if value is None or int(value) == -1:
            return index
    return -1


def captured_pet_state(enemy_state, owner_getpetcount, pet_slot):
    """Build the stable common enemy->pet state transfer at successful capture."""
    pet_slot = int(pet_slot)
    if pet_slot < 0 or pet_slot >= MAX_PETS:
        raise ValueError("pet_slot must be in 0..4")

    missing = [field for field in COMMON_CAPTURE_COPY_FIELDS if field not in enemy_state]
    if missing:
        raise ValueError("enemy_state missing fields: " + ", ".join(missing))

    pet = {field: enemy_state[field] for field in COMMON_CAPTURE_COPY_FIELDS}
    pet.update(
        {
            "which_type": "pet",
            "pet_get_level": int(enemy_state["level"]),
            "owner_pet_slot": pet_slot,
            "owner_getpetcount": int(owner_getpetcount) + 1,
            "enemy_exits_battle": True,
            "exp_copied_from_enemy": False,
            "max_exp_recomputed_from_level": True,
            "variable_ai": 0,
        }
    )
    return pet


def resolve_capture_attempt(
    *,
    target_is_enemy,
    target_pet_flag,
    attacker_level,
    target_level,
    attacker_charm,
    attacker_dex,
    attacker_luck,
    target_dex,
    target_capture_default,
    target_hp,
    target_max_hp,
    target_sleep,
    temp_capture_mod,
    pick_all_pet,
    required_item_ids,
    inventory_item_ids,
    pet_slots,
    roll,
):
    """Resolve the stable top-level capture sequence through pet-slot creation.

    Required-item tables themselves remain version-specific inputs.
    """
    base = {
        "success": False,
        "temp_capture_mod_after": 0,
        "inventory_after": tuple(int(v) for v in inventory_item_ids),
        "consumed_items": (),
        "pet_slot": -1,
    }

    if not required_items_satisfied(required_item_ids, inventory_item_ids):
        return {**base, "reason": "missing_required_items", "score": None}

    eligible, reason = capture_basic_gate(
        target_is_enemy=target_is_enemy,
        target_pet_flag=target_pet_flag,
        attacker_level=attacker_level,
        target_level=target_level,
        pick_all_pet=pick_all_pet,
    )
    if not eligible:
        return {**base, "reason": reason, "score": 0.0}

    score = capture_score(
        attacker_charm=attacker_charm,
        attacker_level=attacker_level,
        attacker_dex=attacker_dex,
        attacker_luck=attacker_luck,
        target_level=target_level,
        target_dex=target_dex,
        target_capture_default=target_capture_default,
        target_hp=target_hp,
        target_max_hp=target_max_hp,
        temp_capture_mod=temp_capture_mod,
        target_sleep=target_sleep,
    )
    if not capture_roll_success(score, roll):
        return {**base, "reason": "roll_failed", "score": score}

    slot = first_empty_pet_slot(pet_slots)
    if slot < 0:
        return {**base, "reason": "pet_slots_full", "score": score}

    remaining, consumed = consume_required_items_on_success(
        required_item_ids, inventory_item_ids
    )
    return {
        **base,
        "success": True,
        "reason": "captured",
        "score": score,
        "pet_slot": slot,
        "inventory_after": remaining,
        "consumed_items": consumed,
    }
