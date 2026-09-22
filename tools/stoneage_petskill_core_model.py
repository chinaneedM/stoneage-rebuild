#!/usr/bin/env python3
"""Deterministic reference model for StoneAge's 15 stable common pet-skill callbacks.

The model separates skill-selection/command encoding from battle execution.
Random outcomes are injected or reduced to deterministic probability helpers.
It intentionally excludes the 50 active macro-gated pet-skill callbacks and
the four recovered callbacks absent from all three pinned source lineages.
"""

import re

from tools.stoneage_battle_status_model import (
    BASE_STATUS_NAME_BY_INDEX,
    BaseBattleStatusState,
    BasePhysicalOnHitStatusInputs,
    BaseStatusAttackInputs,
    base_status_attack_probability_value,
    resolve_base_physical_on_hit_status_application,
)


def _c_number(text, default=0, *, float_ok=False):
    pattern = r"\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))" if float_ok else r"\s*([+-]?\d+)"
    m = re.match(pattern, str(text))
    if not m:
        return float(default) if float_ok else int(default)
    return float(m.group(1)) if float_ok else int(m.group(1), 10)


def _after_marker(option, marker):
    text = str(option)
    pos = text.find(str(marker))
    if pos < 0:
        return None
    return text[pos + len(str(marker)) :]


def _percent_value(option, marker, default=None, *, as_float=False):
    tail = _after_marker(option, marker)
    if tail is None:
        return default
    return _c_number(tail, 0 if default is None else default, float_ok=as_float)


def _command(kind, target, **kwargs):
    out = {
        "accepted": True,
        "command": str(kind),
        "target": int(target),
        "mode": "C_OK",
    }
    out.update(kwargs)
    return out


def skill_none(target):
    return _command("NONE", target)


def skill_normal_attack(target):
    return _command("ATTACK", target)


def skill_normal_guard(target):
    return _command("GUARD", target)


def continuation_attack_command(target, option, *, prior_high=0):
    n = _c_number(option, 1)
    if n < 1 or n > 10:
        n = 1
    # CHAR_SETWORKINT_LOW preserves the previous high half.
    return _command("S_RENZOKU", target, low=n, high=int(prior_high))


def continuation_execution(*, count):
    n = int(count)
    return {
        "attack_max": n,
        "damage_divisor": n,
        "attack_loop": True,
    }


def charge_attack_command(target, option, *, attack_percent_marker="攻%"):
    n = _c_number(option, 1)
    if n < 1 or n > 10:
        n = 1
    per = _percent_value(option, attack_percent_marker, 0)
    return _command("S_CHARGE", target, low=n, high=int(per))


def charge_execution_step(
    *,
    remaining,
    attack_percent,
    fixed_attack,
    attack_modifier,
):
    """One BATTLE_Charge step.

    A positive low word is decremented and the pet does no action. When it is
    already <=0, attack power is rebuilt and command changes to CHARGE_OK.
    """
    remaining = int(remaining)
    if remaining > 0:
        return {
            "ready": False,
            "remaining": remaining - 1,
            "command": "S_CHARGE",
            "no_action": True,
            "attack_power": None,
        }
    power = int(fixed_attack)
    power += int(power * int(attack_percent) * 0.01)
    power += int(attack_modifier)
    return {
        "ready": True,
        "remaining": remaining,
        "command": "S_CHARGE_OK",
        "no_action": False,
        "attack_power": power,
    }


def _apply_fixed_percent(base, percent):
    return int(base) + int(int(base) * float(percent) / 100.0)


def power_balance_command(
    target,
    option,
    *,
    fixed_attack,
    fixed_defense,
    attack_percent_marker="攻%",
    defense_percent_marker="防%",
):
    """Command plus immediate attack/defense work-power mutations."""
    if option is None:
        return {
            "accepted": False,
            "command": "S_POWERBALANCE",
            "target": int(target),
            "mode": "C_OK",
            "attack_power": None,
            "defense_power": None,
        }
    attack = int(fixed_attack)
    defense = int(fixed_defense)
    ap = _percent_value(option, attack_percent_marker, None, as_float=True)
    dp = _percent_value(option, defense_percent_marker, None, as_float=True)
    if ap is not None:
        attack = _apply_fixed_percent(fixed_attack, ap)
    if dp is not None:
        defense = _apply_fixed_percent(fixed_defense, dp)
    return _command(
        "S_POWERBALANCE",
        target,
        attack_power=attack,
        defense_power=defense,
    )


def guardian_command(
    target,
    option,
    *,
    fixed_attack,
    fixed_defense,
    battle_slot,
    battle_side,
    attack_percent_marker="攻%",
    defense_percent_marker="防%",
    defensive_marker="COM:",
    guard_word="防御",
):
    """Build guardian command and its same-turn guardian registration."""
    text = str(option)
    attack = int(fixed_attack)
    defense = int(fixed_defense)
    ap = _percent_value(text, attack_percent_marker, None, as_float=True)
    dp = _percent_value(text, defense_percent_marker, None, as_float=True)
    if ap is not None:
        attack = _apply_fixed_percent(fixed_attack, ap)
    if dp is not None:
        defense = _apply_fixed_percent(fixed_defense, dp)

    command = "S_GUARDIAN_ATTACK"
    guarded_slot = None
    tail = _after_marker(text, defensive_marker)
    if tail is not None and guard_word in tail:
        command = "GUARD"
        side = 1 if int(target) >= 10 else 0
        ownerpos = int(target) - side * 10
        if 0 <= ownerpos < 10:
            guarded_slot = int(target)
    else:
        ownerpos = int(battle_slot) - 5 - int(battle_side) * 10
        if 0 <= ownerpos <= 19:
            guarded_slot = int(battle_side) * 10 + ownerpos

    return _command(
        command,
        target,
        attack_power=attack,
        defense_power=defense,
        guardian_flag=True,
        guardian_for_slot=guarded_slot,
        guardian_slot=int(battle_slot),
    )


def guardian_redirect_allowed(
    *,
    guardian_exists,
    guardian_slot,
    defender_slot,
    guardian_alive,
    guardian_flag,
    guardian_sleep=0,
    guardian_confusion=0,
    guardian_paralysis=0,
    guardian_stone=0,
    guardian_barrier=0,
    guardian_is_attacker=False,
    attacker_uses_throw_weapon=False,
):
    if not guardian_exists:
        return False
    if int(guardian_slot) == int(defender_slot):
        return False
    if not guardian_alive or not guardian_flag:
        return False
    if any(
        int(x) > 0
        for x in (
            guardian_sleep,
            guardian_confusion,
            guardian_paralysis,
            guardian_stone,
            guardian_barrier,
        )
    ):
        return False
    if guardian_is_attacker or attacker_uses_throw_weapon:
        return False
    return True


def mighty_command(
    target,
    option,
    *,
    multiplier_marker="倍",
    dodge_marker="避",
):
    """Preserve old missing-marker quirk: encoded multiplier stays zero."""
    text = str(option)
    encoded_multiplier = 0
    tail = _after_marker(text, multiplier_marker)
    if tail is not None:
        encoded_multiplier = int(_c_number(tail, 2.0, float_ok=True) * 100)
    dodge = _percent_value(text, dodge_marker, 0)
    return _command(
        "S_MIGHTY",
        target,
        low=encoded_multiplier,
        high=int(dodge),
    )


def mighty_execution(*, encoded_multiplier, dodge_modifier):
    return {
        "damage_multiplier": int(encoded_multiplier) * 0.01,
        "dodge_modifier": int(dodge_modifier),
    }


def parse_status_skill(
    option,
    status_tokens,
    *,
    turn_marker="turn",
    attack_percent_marker="攻%",
    defense_percent_marker="防%",
):
    text = str(option)
    status = -1
    status_pos = None
    for i in range(1, len(status_tokens)):
        p = text.find(str(status_tokens[i]))
        if p >= 0 and (status_pos is None or p < status_pos):
            status = i
            status_pos = p
    turn = 3
    tail = _after_marker(text, turn_marker)
    if tail is not None:
        turn = _c_number(tail, 3)
    ap = _percent_value(text, attack_percent_marker, None, as_float=True)
    dp = _percent_value(text, defense_percent_marker, None, as_float=True)
    # The old handler stores loop variable i, not 'status'. If no token is
    # found, i has reached BATTLE_ST_END; the later status checker rejects it.
    encoded_status = status if status >= 0 else len(status_tokens)
    return {
        "status": encoded_status,
        "matched": status >= 0,
        "turn": int(turn),
        "attack_percent": ap,
        "defense_percent": dp,
    }


def status_change_command(
    target,
    option,
    status_tokens,
    *,
    fixed_attack,
    fixed_defense,
):
    parsed = parse_status_skill(option, status_tokens)
    attack = int(fixed_attack)
    defense = int(fixed_defense)
    if parsed["attack_percent"] is not None:
        attack = _apply_fixed_percent(fixed_attack, parsed["attack_percent"])
    if parsed["defense_percent"] is not None:
        defense = _apply_fixed_percent(fixed_defense, parsed["defense_percent"])
    return _command(
        "S_STATUSCHANGE",
        target,
        low=parsed["status"],
        high=parsed["turn"],
        attack_power=attack,
        defense_power=defense,
    )


def status_attack_probability(
    *,
    status,
    defender_vital,
    defender_str,
    defender_tough,
    defender_dex,
    attacker_luck,
    attacker_level,
    defender_level,
    pvp,
    status_specific_resist=0,
    per_offset=30,
    level_range=40,
    level_multiplier=2.0,
):
    """Delegate pet status-attack probability to the common status core."""
    status=int(status)
    status_name=BASE_STATUS_NAME_BY_INDEX.get(status)
    if status_name is None:
        return 0
    return base_status_attack_probability_value(
        BaseStatusAttackInputs(
            status=status_name,
            attacker_level=attacker_level,
            defender_level=defender_level,
            pvp=pvp,
            attacker_fixed_luck=attacker_luck,
            defender_vital=defender_vital,
            defender_str=defender_str,
            defender_tough=defender_tough,
            defender_dex=defender_dex,
            defender_resistance=status_specific_resist,
            per_offset=per_offset,
            level_range=level_range,
            level_scale=level_multiplier,
        )
    )


def status_attack_application(
    *,
    current_status,
    damage,
    status,
    turn,
    defender_vital,
    defender_str,
    defender_tough,
    defender_dex,
    attacker_luck,
    attacker_level,
    defender_level,
    pvp,
    status_specific_resist=0,
    roll_1_to_100=None,
    per_offset=30,
):
    """Authoritative stable pet StatusChange physical application seam.

    The handler supplies status + turn in COM3; BATTLE_Attack supplies the
    positive-damage gate and the common 30/40/2 status-check profile.
    """
    if not isinstance(current_status,BaseBattleStatusState):
        raise TypeError("current_status must be BaseBattleStatusState")
    status=int(status)
    status_name=BASE_STATUS_NAME_BY_INDEX.get(status)
    if status_name is None:
        return {
            "valid_status":False,
            "application":None,
        }
    application=resolve_base_physical_on_hit_status_application(
        BasePhysicalOnHitStatusInputs(
            status=status_name,
            attacker_level=attacker_level,
            defender_level=defender_level,
            pvp=pvp,
            attacker_fixed_luck=attacker_luck,
            defender_vital=defender_vital,
            defender_str=defender_str,
            defender_tough=defender_tough,
            defender_dex=defender_dex,
            defender_resistance=status_specific_resist,
            source_turn=turn,
            per_offset=per_offset,
        ),
        current_status,
        damage_after_resolution=damage,
        roll_1_100=roll_1_to_100,
    )
    return {
        "valid_status":True,
        "application":application,
    }


def status_attack_transition(
    *,
    damage,
    status,
    turn,
    already_has_ordinary_status,
    probability,
    rolled_1_to_100,
    immobilizing_statuses=(2, 3, 4, 9),
):
    if int(damage) <= 0 or int(status) <= 0 or already_has_ordinary_status:
        return {"applied": False, "timer": 0, "clear_command": False}
    if int(rolled_1_to_100) >= int(probability):
        return {"applied": False, "timer": 0, "clear_command": False}
    # Source writes gBattleStausTurn + 1, then physical DRUNK is halved.
    timer=int(turn)+1
    if int(status)==5:
        timer//=2
    return {
        "applied": True,
        "timer": timer,
        "clear_command": int(status) in set(immobilizing_statuses),
    }


def earth_round_command(
    target,
    option,
    *,
    attack_percent_marker="攻%",
    prior_com3=0,
):
    tail = _after_marker(option, attack_percent_marker)
    # Unlike most handlers, EarthRound writes the whole COM3 only when the
    # marker exists. Without it, old COM3 survives and later becomes the
    # EarthRound0 damage percentage.
    com3 = int(prior_com3)
    if tail is not None:
        com3 = int(_c_number(tail, 0, float_ok=True))
    return _command("S_EARTHROUND1", target, com3=com3)


def earth_round_hide_transition():
    return {
        "is_attacked_flag": False,
        "next_command": "S_EARTHROUND0",
        "result": False,
    }


def earth_round_attack_transition(*, attack_percent):
    return {
        "damage_multiplier": 1.0 + 0.01 * int(attack_percent),
        "reset_command_after_attack": True,
    }


def guard_break_command(
    target,
    option,
    *,
    fixed_attack,
    attack_percent_marker="攻%",
):
    attack = int(fixed_attack)
    ap = _percent_value(option, attack_percent_marker, None, as_float=True)
    if ap is not None:
        attack = _apply_fixed_percent(fixed_attack, ap)
    return _command("S_GBREAK", target, attack_power=attack)


def guard_break_gate(*, target_guarding, target_confused):
    """Old GBreak only resolves damage against a non-confused guarding target."""
    return bool(target_guarding and not target_confused)


def abduct_command(target, *, skill_array, prior_high=0):
    # CHAR_SETWORKINT_LOW preserves the previous high half.
    return _command("S_ABDUCT", target, low=int(skill_array), high=int(prior_high))


def abduct_probability(*, attacker_level, defender_level, defender_is_player, has_win_func):
    """Base unguarded BATTLE_Abduct probability before later ABDUCTII extension."""
    if defender_is_player or has_win_func:
        return 0
    per = int((int(defender_level) - int(attacker_level)) * 0.6 + 30)
    return max(per, 50)


def abduct_transition(
    *,
    attacker_type,
    defender_type,
    probability,
    rolled_1_to_100,
):
    """Outcome plus unconditional attacker exit behavior.

    Only PET/ENEMY attackers are eligible; PLAYER defenders are rejected.
    A valid attempt removes the attacker from battle whether success or failure.
    """
    if attacker_type not in ("pet", "enemy") or defender_type == "player":
        return {"attempted": False, "success": False, "attacker_exits": False}
    success = int(rolled_1_to_100) < int(probability)
    return {
        "attempted": True,
        "success": success,
        "attacker_exits": True,
        "defender_exits": success and defender_type in ("pet", "enemy"),
    }


def steal_command(target):
    return _command("S_STEAL", target)


def steal_transition(
    *,
    defender_type,
    success_roll_1_to_100,
    mode_roll_1_to_100=None,
    defender_gold=0,
    gold_percent_roll=None,
    carried_item_slots=(),
    chosen_item_ordinal=None,
):
    """Deterministic shell around old BATTLE_Steal.

    Old common steal has 50% chance only against PLAYER targets; non-players
    have probability zero. A successful theft removes the stealing pet from
    battle. Random sub-rolls are injected.
    """
    if defender_type != "player":
        return {"success": False, "mode": None, "attacker_exits": False}
    if int(success_roll_1_to_100) >= 50:
        return {"success": False, "mode": None, "attacker_exits": False}

    if mode_roll_1_to_100 is None:
        raise ValueError("mode roll required after steal success")
    if int(mode_roll_1_to_100) < 50:
        if gold_percent_roll is None:
            raise ValueError("gold percent roll required for gold steal")
        gold = int(float(int(defender_gold)) * int(gold_percent_roll) * 0.01)
        if gold <= 0:
            return {
            "success": False,
            "mode": "gold",
            "attacker_exits": False,
            "defender_gold_loss": 0,
            "attacker_gold_gain": 0,
        }
        return {
            "success": True,
            "mode": "gold",
            "attacker_exits": True,
            "defender_gold_loss": gold,
            "attacker_gold_gain": 0,
        }

    slots = tuple(int(x) for x in carried_item_slots)
    if not slots:
        return {
            "success": False,
            "mode": "item",
            "attacker_exits": False,
            "destroyed_item_slot": None,
            "attacker_item_gain": False,
        }
    if chosen_item_ordinal is None:
        raise ValueError("item ordinal required for item steal")
    idx = int(chosen_item_ordinal)
    if idx < 0 or idx >= len(slots):
        raise ValueError("item ordinal out of range")
    return {
        "success": True,
        "mode": "item",
        "attacker_exits": True,
        "destroyed_item_slot": slots[idx],
        "attacker_item_gain": False,
    }


def merge_transition(
    *,
    owner_battle_mode_none,
    merge_result,
):
    if not owner_battle_mode_none:
        return {"accepted": False, "result": False, "reason": "owner_in_battle"}
    return {"accepted": True, "result": bool(merge_result), "reason": "merge_called"}


def no_guard_command(
    target,
    option,
    *,
    dodge_marker="避%",
    counter_marker="击%",
    critical_marker="心%",
    prior_high=0,
):
    dodge_tail = _after_marker(option, dodge_marker)
    # HIGH is only written when the dodge marker exists.
    dodge = int(prior_high) if dodge_tail is None else int(_c_number(dodge_tail, 0))
    counter = int(_percent_value(option, counter_marker, 0))
    critical = int(_percent_value(option, critical_marker, 0))
    packed_low = (counter << 8) + critical
    return _command("S_NOGUARD", target, low=packed_low, high=dodge)


def no_guard_execution():
    """Fixed old battle switch consumes S_NOGUARD only as BATTLE_NoAction."""
    return {
        "no_action": True,
        "parsed_parameters_consumed": False,
    }
