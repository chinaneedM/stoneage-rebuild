#!/usr/bin/env python3
"""Deterministic reference model for the convergent StoneAge Charm NPC core."""

RATE = 10
CHARM_HEAL = 5
WARU = 3
MAX_CHARM = 100


def charm_cost(*, level, charm, transmigration):
    level = int(level)
    charm = int(charm)
    transmigration = int(transmigration)

    if charm >= MAX_CHARM:
        return -1
    if charm <= 1:
        charm = WARU

    return level * RATE * (charm // WARU) * (transmigration + 1)


def charm_upgrade(*, level, charm, transmigration, gold):
    """Mirror raw NPC_CharmUp, including stale-callback cost=-1 arithmetic."""
    cost = charm_cost(level=level, charm=charm, transmigration=transmigration)
    gold = int(gold)
    charm = int(charm)

    if cost > gold:
        return {
            "success": False,
            "reason": "insufficient_gold",
            "cost": cost,
            "gold_after": gold,
            "charm_after": charm,
            "player_parameters_recomputed": False,
            "pet_parameters_recomputed": False,
        }

    gold_after = gold - cost
    charm_after = (
        MAX_CHARM if charm + CHARM_HEAL >= MAX_CHARM else charm + CHARM_HEAL
    )

    return {
        "success": True,
        "reason": "upgraded",
        "cost": cost,
        "gold_after": gold_after,
        "charm_after": charm_after,
        "player_parameters_recomputed": True,
        "pet_parameters_recomputed": True,
    }


def normal_confirmation_available(*, level, charm, transmigration):
    return charm_cost(
        level=level, charm=charm, transmigration=transmigration
    ) != -1


def normal_yes_flow(*, level, charm, transmigration, gold):
    """Model normal UI flow after Yes, excluding forged/stale max-charm callbacks."""
    if not normal_confirmation_available(
        level=level, charm=charm, transmigration=transmigration
    ):
        return {
            "success": False,
            "reason": "already_max_charm",
            "cost": -1,
            "gold_after": int(gold),
            "charm_after": int(charm),
        }
    return charm_upgrade(
        level=level,
        charm=charm,
        transmigration=transmigration,
        gold=gold,
    )
