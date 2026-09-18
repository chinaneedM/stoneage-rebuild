#!/usr/bin/env python3
"""Reference model for the convergent StoneAge player death/revival core."""

CLEAR_ON_DEATH = (
    "paralysis",
    "sleep",
    "stone",
    "drunk",
    "confusion",
    "poison",
)


def death_transition(gold, equipped_slots, attacker_class, dead_count=0):
    """Model the stable core_Dying state transition.

    attacker_class:
      - "enemy": valid CHAR_TYPEENEMY attacker
      - "non_enemy": valid non-enemy character attacker
      - "unknown": sentinel/invalid/no resolvable attacker

    World placement of dropped objects is intentionally represented as a
    request because CHAR_DropItem/CHAR_DropMoney can fail for map/object
    placement reasons. The final carried-gold state is still zero in core_Dying.
    """
    gold = int(gold)
    dead_count = int(dead_count)
    if gold < 0:
        raise ValueError("gold must be non-negative")
    if dead_count < 0:
        raise ValueError("dead_count must be non-negative")
    if attacker_class not in {"enemy", "non_enemy", "unknown"}:
        raise ValueError("attacker_class must be enemy/non_enemy/unknown")

    equipped = tuple(int(slot) for slot in equipped_slots)
    if len(set(equipped)) != len(equipped):
        raise ValueError("equipped_slots must not contain duplicates")

    if attacker_class in {"enemy", "unknown"}:
        drop_mode = "all_equipped"
        requested_item_drop_slots = equipped
        random_item_drop_candidates = ()
    else:
        drop_mode = "one_random_equipped"
        requested_item_drop_slots = ()
        random_item_drop_candidates = equipped

    return {
        "party_discharged": True,
        "item_drop_mode": drop_mode,
        "requested_item_drop_slots": requested_item_drop_slots,
        "random_item_drop_candidates": random_item_drop_candidates,
        "random_item_drop_count": 1 if equipped and attacker_class == "non_enemy" else 0,
        "requested_ground_gold": gold // 2,
        "final_carried_gold": 0,
        "dead_count": dead_count + 1,
        "cleared_statuses": CLEAR_ON_DEATH,
        "is_dead": True,
        "is_attacked": False,
    }


def resurrect_transition(requested_hp, max_hp):
    """Mirror CHAR_playerresurrect for a normal positive MAXHP character."""
    requested_hp = int(requested_hp)
    max_hp = int(max_hp)
    if max_hp <= 0:
        raise ValueError("max_hp must be positive")
    if requested_hp >= max_hp:
        hp = max_hp
    elif requested_hp <= 0:
        hp = 1
    else:
        hp = requested_hp
    return {
        "base_image_restored": True,
        "is_dead": False,
        "is_attacked": True,
        "is_overed": False,
        "hp": hp,
        "mp_unchanged": True,
        "location_unchanged": True,
    }


def login_sanitize(is_dead, hp):
    """Model the preserved player-load cleanup relevant to death state."""
    hp = int(hp)
    return {
        "is_dead": False if bool(is_dead) else False,
        "hp": 1 if hp <= 0 else hp,
    }
