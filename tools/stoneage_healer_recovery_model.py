#!/usr/bin/env python3
"""Reference model for the convergent StoneAge healer/recovery core."""

PARTY_NONE = 0
PARTY_LEADER = 1
PARTY_CLIENT = 2

WINDOW_MODE_PET_ONLY = 0
WINDOW_MODE_HP = 1
WINDOW_MODE_MP = 2
WINDOW_MODE_ALL = 3

DEFAULT_HP_RATE_UNITS = 500   # RATE=1000 -> 0.5 * level
DEFAULT_MP_RATE_UNITS = 2000  # RATE=1000 -> 2.0 * level
RATE_SCALE = 1000


def healer_targets(talker_id, party_mode, leader_slots=None):
    """Ordinary NPC healer target semantics.

    Standalone players and clients heal only themselves. A leader heals every
    valid entry in the leader-owned party roster.
    """
    talker_id = int(talker_id)
    party_mode = int(party_mode)
    if party_mode in (PARTY_NONE, PARTY_CLIENT):
        return (talker_id,)
    if party_mode != PARTY_LEADER:
        raise ValueError("unknown party mode")
    if leader_slots is None:
        raise ValueError("leader_slots required for party leader")
    return tuple(int(v) for v in leader_slots if v is not None and int(v) >= 0)


def _heal_pet(pet):
    if pet is None:
        return None
    out = dict(pet)
    out["dead"] = False
    out["hp"] = int(out["max_hp"])
    out["mp"] = int(out["max_mp"])
    out["parameters_recomputed"] = True
    return out


def free_healer_all_heal(player, pets):
    """Mirror NPC_HealerAllHeal.

    Player HP/MP are filled. Player death/status flags are intentionally not
    altered. Every valid carried pet is revived and filled to max HP/MP.
    """
    out_player = dict(player)
    out_player["hp"] = int(out_player["max_hp"])
    out_player["mp"] = int(out_player["max_mp"])

    out_pets = tuple(_heal_pet(p) for p in pets)
    return {
        "player": out_player,
        "pets": out_pets,
        "player_death_flag_unchanged": True,
        "player_abnormal_statuses_unchanged": True,
    }


def window_healer_level_is_free(player_level, free_below_level):
    """Source rule: configured_level > player_level means free."""
    return int(free_below_level) > int(player_level)


def hp_cost(player_level, hp_rate_units=DEFAULT_HP_RATE_UNITS):
    """Mirror NPC_WindowCostCheck exactly for ordinary positive config."""
    cost = int(int(player_level) * (int(hp_rate_units) / RATE_SCALE))
    if cost < 1:
        cost = 1
    return cost


def mp_cost(player_level, mp_rate_units=DEFAULT_MP_RATE_UNITS):
    """Mirror NPC_WindowCostCheckMp's asymmetric minimum rule."""
    cost = int(int(player_level) * (int(mp_rate_units) / RATE_SCALE))
    if cost == 0:
        cost = 1
    return cost


def window_healer_cost(
    *,
    player_level,
    free_below_level,
    mode,
    hp,
    max_hp,
    mp,
    max_mp,
    hp_rate_units=DEFAULT_HP_RATE_UNITS,
    mp_rate_units=DEFAULT_MP_RATE_UNITS,
):
    """Return the charge requested before healing."""
    mode = int(mode)
    if window_healer_level_is_free(player_level, free_below_level):
        return 0

    if mode == WINDOW_MODE_HP:
        return hp_cost(player_level, hp_rate_units)
    if mode == WINDOW_MODE_MP:
        return mp_cost(player_level, mp_rate_units)
    if mode == WINDOW_MODE_ALL:
        total = 0
        if int(hp) < int(max_hp):
            total += hp_cost(player_level, hp_rate_units)
        if int(mp) < int(max_mp):
            total += mp_cost(player_level, mp_rate_units)
        return total
    if mode == WINDOW_MODE_PET_ONLY:
        return 0
    raise ValueError("mode must be 0..3")


def pet_healer_check(pets):
    """Mirror NPC_PetHealerCheck: only HP deficit is inspected."""
    for pet in pets:
        if pet is None:
            continue
        if int(pet["hp"]) != int(pet["max_hp"]):
            return True
    return False


def window_healer_apply(player, pets, mode):
    """Apply NPC_WindowHealerAllHeal after payment succeeds."""
    mode = int(mode)
    if mode not in (
        WINDOW_MODE_PET_ONLY,
        WINDOW_MODE_HP,
        WINDOW_MODE_MP,
        WINDOW_MODE_ALL,
    ):
        raise ValueError("mode must be 0..3")

    out_player = dict(player)
    if mode == WINDOW_MODE_HP:
        out_player["hp"] = int(out_player["max_hp"])
    elif mode == WINDOW_MODE_MP:
        out_player["mp"] = int(out_player["max_mp"])
    elif mode == WINDOW_MODE_ALL:
        out_player["hp"] = int(out_player["max_hp"])
        out_player["mp"] = int(out_player["max_mp"])

    out_pets = tuple(_heal_pet(p) for p in pets)
    return {
        "player": out_player,
        "pets": out_pets,
        "player_death_flag_unchanged": True,
        "player_abnormal_statuses_unchanged": True,
    }


def window_healer_transaction(
    *,
    player,
    pets,
    mode,
    free_below_level,
    gold,
    hp_rate_units=DEFAULT_HP_RATE_UNITS,
    mp_rate_units=DEFAULT_MP_RATE_UNITS,
):
    """Charge first, then heal; insufficient gold leaves state unchanged."""
    charge = window_healer_cost(
        player_level=player["level"],
        free_below_level=free_below_level,
        mode=mode,
        hp=player["hp"],
        max_hp=player["max_hp"],
        mp=player["mp"],
        max_mp=player["max_mp"],
        hp_rate_units=hp_rate_units,
        mp_rate_units=mp_rate_units,
    )
    gold = int(gold)
    if gold < charge:
        return {
            "success": False,
            "reason": "not_enough_gold",
            "charge": charge,
            "gold_after": gold,
            "player": dict(player),
            "pets": tuple(None if p is None else dict(p) for p in pets),
        }

    healed = window_healer_apply(player, pets, mode)
    return {
        "success": True,
        "reason": "healed",
        "charge": charge,
        "gold_after": gold - charge,
        **healed,
    }
