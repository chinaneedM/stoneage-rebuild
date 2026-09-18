#!/usr/bin/env python3
"""Reference model for StoneAge common item effect semantics.

This module models the convergent, unguarded descendant behavior around the
ordinary recovery/status/defense/parameter/field/reverse/resurrection/capture
item effects. Random rolls are injected by callers/tests.
"""

import re

from tools.stoneage_magic_effect_model import (
    att_reverse_cast_transition,
    common_alive_target_list,
    common_dead_target_list,
    magic_def_transition,
    parse_after_marker,
    parse_field_attribute_option,
    recovery_rate,
    resurrection_gain,
    status_recovery_transition,
)


BATTLE_ONLY_ITEM_EFFECTS = frozenset(
    {
        "status_change",
        "status_recovery",
        "magic_def",
        "param_change",
        "field_change",
        "att_reverse",
        "ressurect",
        "capture_up",
    }
)


def item_use_route(effect, *, caster_valid, battle_mode_init, battling):
    """Top-level item wrapper routing before the concrete effect function."""
    effect = str(effect)
    if not caster_valid:
        return {"accepted": False, "route": "reject_invalid_caster"}
    if battle_mode_init:
        return {"accepted": False, "route": "reject_battle_init"}
    if effect == "recovery":
        return {"accepted": True, "route": "battle" if battling else "field"}
    if effect in BATTLE_ONLY_ITEM_EFFECTS:
        if not battling:
            return {"accepted": False, "route": "reject_not_battling"}
        return {"accepted": True, "route": "battle"}
    raise ValueError("effect is outside the modeled common item core")


def _find_token(text, tokens, start=0):
    text = str(text)
    best = None
    for index in range(int(start), len(tokens)):
        token = str(tokens[index])
        pos = text.find(token)
        if pos < 0:
            continue
        candidate = (pos, index, token)
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    if best is None:
        return None
    pos, index, token = best
    return {
        "index": index,
        "token": token,
        "tail": text[pos + len(token) :],
    }


def _scan_item_value_tail(tail, default):
    """Model token match + old for-loop's extra one-byte pointer increment."""
    tail = str(tail)
    if tail:
        tail = tail[1:]
    m = re.match(r"\s*([+-]?\d+)", tail)
    if m:
        return int(m.group(1), 10)
    return None if default is None else int(default)


def parse_battle_recovery_option(option, *, hp_token, mp_token):
    """Parse the unguarded HP/MP branches of ITEM_useRecovery_Battle.

    HP is checked before MP. The common branch never sets percentage mode.
    """
    text = str(option)
    pos_hp = text.find(str(hp_token))
    if pos_hp >= 0:
        tail = text[pos_hp + len(str(hp_token)) :]
        return {
            "kind": "hp",
            "power": _scan_item_value_tail(tail, 0),
            "percent": False,
        }
    pos_mp = text.find(str(mp_token))
    if pos_mp >= 0:
        tail = text[pos_mp + len(str(mp_token)) :]
        return {
            "kind": "mp",
            "power": _scan_item_value_tail(tail, 0),
            "percent": False,
        }
    return None


def battle_item_recovery_gain(*, kind, rolled_power, vital=0, is_player=True):
    """Shared BATTLE_MultiRecovery arithmetic for unguarded item HP/MP use."""
    amount = float(rolled_power)
    if str(kind) == "hp":
        amount *= recovery_rate(vital=vital, is_player=is_player)
    elif str(kind) != "mp":
        raise ValueError("kind must be hp or mp")
    return int(amount)


def parse_status_change_option(option, status_tokens):
    """Item status change defaults to turn=0 and success=15."""
    found = _find_token(option, status_tokens, start=0)
    if found is None:
        return None
    return {
        "status": found["index"],
        "turn": parse_after_marker(option, "turn", 0),
        "success": parse_after_marker(option, "成", 15),
    }


def parse_status_recovery_option(option, status_tokens):
    found = _find_token(option, status_tokens, start=0)
    return None if found is None else {"status": found["index"]}


def parse_magic_def_option(option, defense_tokens):
    """Item magic-defense duration defaults to zero, unlike magic's 3."""
    found = _find_token(option, defense_tokens, start=1)
    if found is None:
        return None
    return {
        "kind": found["index"],
        "turn": parse_after_marker(option, "turn", 0),
    }


def parse_param_change_option(option, param_tokens):
    """Parse parameter kind, percent flag, and power (default 30)."""
    found = _find_token(option, param_tokens, start=1)
    if found is None:
        return None
    power = _scan_item_value_tail(found["tail"], 30)
    return {
        "kind": found["index"],
        "power": power,
        "percent": "%" in found["tail"],
    }


def param_modifier_delta(
    kind,
    *,
    power,
    percent,
    fixed_attack=0,
    fixed_defense=0,
    fixed_quick=0,
    fixed_charm=0,
):
    """Return exact work-array delta used by BATTLE_MultiParamChange.

    Kinds follow source order:
      1 attack, 2 defense, 3 quick, 4 charm, 5 capture.

    Attack/defense/quick work modifiers are stored in x100 scale. In percent
    mode the old code multiplies the fixed x100 base directly by 'power';
    otherwise it stores power*100. Charm and capture use ordinary units.
    """
    kind = int(kind)
    power = int(power)
    percent = bool(percent)

    if kind == 1:
        return int(fixed_attack) * power if percent else power * 100
    if kind == 2:
        return int(fixed_defense) * power if percent else power * 100
    if kind == 3:
        return int(fixed_quick) * power if percent else power * 100
    if kind == 4:
        return int(int(fixed_charm) * power * 0.01) if percent else power
    if kind == 5:
        return power
    raise ValueError("unsupported parameter-change kind")


def apply_param_modifier(current_modifier, delta):
    return int(current_modifier) + int(delta)


def parse_field_change_option(option, attribute_tokens):
    """Item field change delegates to the same BATTLE_FieldAttChange parser."""
    return parse_field_attribute_option(option, attribute_tokens)


def parse_resurrection_option(option):
    text = str(option)
    m = re.match(r"\s*([+-]?\d+)", text)
    power = int(m.group(1), 10) if m else 0
    return {"power": power, "percent": "%" in text}


def resurrection_target_transition(
    *,
    is_dead,
    is_pvp_player,
    current_hp,
    max_hp,
    power,
    percent,
    rolled_power=None,
):
    """Shared BATTLE_MultiRessurect semantics used by item resurrection."""
    if not is_dead or is_pvp_player:
        return {
            "changed": False,
            "is_dead": bool(is_dead),
            "hp": int(current_hp),
        }
    gain = resurrection_gain(
        power=power,
        percent=percent,
        max_hp=max_hp,
        rolled_power=rolled_power,
    )
    return {
        "changed": True,
        "is_dead": False,
        "hp": min(int(current_hp) + gain, int(max_hp)),
    }


def parse_capture_up_option(option):
    m = re.match(r"\s*([+-]?\d+)", str(option))
    return int(m.group(1), 10) if m else 5


def capture_up_transition(
    *,
    is_player,
    is_dead,
    current_capture_modifier,
    rolled_power,
):
    """BATTLE_MultiCaptureUp changes only living player targets."""
    if not is_player or is_dead:
        return {
            "changed": False,
            "capture_modifier": int(current_capture_modifier),
        }
    return {
        "changed": True,
        "capture_modifier": int(current_capture_modifier) + int(rolled_power),
    }


def parse_field_recovery_option(
    option,
    *,
    target_type,
    all_token,
    hp_token,
    mp_token,
    charm_token,
    loyalty_token,
):
    """Parse unguarded ITEM_useRecovery_Field request components.

    Values parsed from explicit HP/MP/charm/loyalty keys are RNG inputs in the
    source. A parse failure uses literal 1 without RNG. Loyalty is stored x100.
    """
    text = str(option)
    target_type = str(target_type)
    requests = {}

    if str(all_token) in text:
        requests["hp"] = {"full_marker": True, "base": 10_000_000, "randomized": False}
        if target_type != "pet":
            requests["mp"] = {"full_marker": True, "base": 100, "randomized": False}

    specs = (
        ("hp", hp_token, True),
        ("mp", mp_token, target_type == "player"),
        ("loyalty", loyalty_token, target_type == "pet"),
        ("charm", charm_token, target_type == "player"),
    )
    for key, token, applicable in specs:
        if not applicable:
            continue
        pos = text.find(str(token))
        if pos < 0:
            continue
        tail = text[pos + len(str(token)) :]
        scanned = _scan_item_value_tail(tail, None)
        if scanned is None:
            requests[key] = {"base": 1, "randomized": False}
        else:
            requests[key] = {"base": scanned, "randomized": True}

    return requests


def _clamp(value, lo, hi):
    # Source order is min(value, max) followed by max(value, min).
    return max(min(int(value), int(hi)), int(lo))


def apply_field_recovery(
    requests,
    *,
    target_type,
    current_hp,
    max_hp,
    current_mp=0,
    max_mp=0,
    current_charm=0,
    current_loyalty=0,
    vital=0,
    rolls=None,
):
    """Apply parsed field-recovery requests.

    'rolls' maps request key to already-rolled RAND(base*0.9, base*1.1).
    """
    rolls = dict(rolls or {})
    if not requests:
        return {
            "changed": False,
            "consume": False,
            "hp": int(current_hp),
            "mp": int(current_mp),
            "charm": int(current_charm),
            "loyalty": int(current_loyalty),
        }

    hp = int(current_hp)
    mp = int(current_mp)
    charm = int(current_charm)
    loyalty = int(current_loyalty)
    target_type = str(target_type)

    for key, spec in requests.items():
        amount = spec["base"]
        if spec.get("randomized"):
            if key not in rolls:
                raise ValueError(f"missing injected roll for {key}")
            amount = rolls[key]

        if key == "hp":
            amount = int(
                float(amount)
                * recovery_rate(vital=vital, is_player=(target_type == "player"))
            )
            hp = _clamp(hp + amount, 1, max_hp)
        elif key == "mp":
            mp = _clamp(mp + int(amount), 1, max_mp)
        elif key == "charm":
            charm = _clamp(charm + int(amount), 0, 100)
        elif key == "loyalty":
            loyalty = _clamp(loyalty + int(amount) * 100, -10000, 10000)

    return {
        "changed": True,
        "consume": True,
        "hp": hp,
        "mp": mp,
        "charm": charm,
        "loyalty": loyalty,
    }


def battle_effect_consumption(*, item_valid, argument_valid, parser_succeeded):
    """Common concrete battle item functions consume only after parser success.

    Once the concrete primitive is called, item deletion follows regardless of
    whether any selected target ultimately changes.
    """
    return bool(item_valid and argument_valid and parser_succeeded)


def field_change_consumption(*, item_valid, argument_valid):
    """ITEM_useFieldChange_Battle ignores BATTLE_FieldAttChange's return value."""
    return bool(item_valid and argument_valid)


def living_targets(to_no, alive_slots):
    return common_alive_target_list(to_no, alive_slots)


def dead_targets(to_no, dead_slots):
    return common_dead_target_list(to_no, dead_slots)


def reverse_target_transition(**kwargs):
    return att_reverse_cast_transition(**kwargs)


def recover_statuses(active_statuses, *, requested_status, confusion_index):
    return status_recovery_transition(
        active_statuses,
        requested_status=requested_status,
        confusion_index=confusion_index,
    )


def set_magic_defense(current_turns, *, kind, turn):
    return magic_def_transition(
        current_turns=current_turns,
        kind=kind,
        turn=turn,
    )


def parse_warp_argument(option):
    """Parse ITEM_useWarp's four-integer argument: flag floor x y."""
    m = re.match(
        r"\s*([+-]?\d+)\s+([+-]?\d+)\s+([+-]?\d+)\s+([+-]?\d+)",
        str(option),
    )
    if not m:
        return None
    flag, floor, x, y = (int(x, 10) for x in m.groups())
    return {"flag": flag, "floor": floor, "x": x, "y": y}


def warp_item_transition(
    *,
    parsed_argument,
    battle_mode_none,
    current_floor,
    party_mode,
    caster_id,
    valid_party_members=(),
):
    """Stable ITEM_WarpForAny control flow around the shared warp primitive.

    floor 117 is blocked in both observed compile branches. Additional blocked
    floors remain version/macro layers.
    """
    if parsed_argument is None:
        return {"accepted": False, "consume": False, "targets": (), "reason": "bad_argument"}
    if not battle_mode_none:
        return {"accepted": False, "consume": False, "targets": (), "reason": "in_battle"}
    if int(current_floor) == 117:
        return {"accepted": False, "consume": False, "targets": (), "reason": "blocked_floor"}

    mode = str(party_mode)
    if mode == "leader":
        if int(parsed_argument["flag"]) == 0:
            return {
                "accepted": False,
                "consume": False,
                "targets": (),
                "reason": "leader_single_only_rejected",
            }
        return {
            "accepted": True,
            "consume": True,
            "targets": tuple(valid_party_members),
            "reason": "party_warp",
        }
    if mode == "client":
        return {"accepted": False, "consume": False, "targets": (), "reason": "party_client"}
    if mode == "none":
        return {
            "accepted": True,
            "consume": True,
            "targets": (caster_id,),
            "reason": "solo_warp",
        }

    # Legacy helper reaches TRUE without an explicit warp for an unexpected mode.
    return {"accepted": True, "consume": True, "targets": (), "reason": "unknown_mode"}


def pet_follow_item_transition(
    *,
    existing_follow_valid,
    target_valid,
    item_valid,
    follow_level,
    target_level,
    target_in_first_five_pet_slots,
    drop_follow_success,
):
    """Common ITEM_petFollow eligibility.

    The visible loyalty <80 check has its rejection commented out, and the
    function does not delete the item after a successful follow operation.
    """
    if existing_follow_valid:
        return {"accepted": False, "consume": False, "reason": "existing_follow"}
    if not target_valid:
        return {"accepted": False, "consume": False, "reason": "invalid_target"}
    if not item_valid:
        return {"accepted": False, "consume": False, "reason": "invalid_item"}
    if int(target_level) > int(follow_level):
        return {"accepted": False, "consume": False, "reason": "level_too_high"}
    if not target_in_first_five_pet_slots:
        return {"accepted": False, "consume": False, "reason": "not_owned_slot"}
    if not drop_follow_success:
        return {"accepted": False, "consume": False, "reason": "drop_follow_failed"}
    return {"accepted": True, "consume": False, "reason": "follow_started"}


def skillup_point_item_transition(*, item_valid, current_points):
    if not item_valid:
        return {"changed": False, "consume": False, "points": int(current_points)}
    return {"changed": True, "consume": True, "points": int(current_points) + 1}


def noenemy_item_transition(*, item_valid):
    return {
        "changed": bool(item_valid),
        "consume": bool(item_valid),
        "noenemy": bool(item_valid),
    }


def encounter_item_transition(*, item_valid):
    return {
        "changed": bool(item_valid),
        "consume": bool(item_valid),
        "stay_encounter": bool(item_valid),
    }


def microphone_item_transition(*, caster_valid, battle_mode_none, current_enabled):
    """ITEM_useMic toggles runtime mic mode only outside battle and is not consumed."""
    if not caster_valid:
        return {"changed": False, "consume": False, "enabled": bool(current_enabled)}
    if not battle_mode_none:
        return {"changed": False, "consume": False, "enabled": bool(current_enabled)}
    return {
        "changed": True,
        "consume": False,
        "enabled": not bool(current_enabled),
    }


def change_pet_owner_item_transition(
    *,
    caster_valid,
    target_valid,
    item_valid,
    target_is_pet,
    pet_owner_marker,
    player_account_marker,
):
    """Model ITEM_changePetOwner's rename-lock release behavior."""
    if not caster_valid or not target_valid or not item_valid:
        return {
            "changed": False,
            "consume": False,
            "pet_owner_marker": str(pet_owner_marker),
        }
    if not target_is_pet:
        return {
            "changed": False,
            "consume": False,
            "pet_owner_marker": str(pet_owner_marker),
        }
    marker = str(pet_owner_marker)
    if marker == "" or marker == str(player_account_marker):
        return {"changed": False, "consume": False, "pet_owner_marker": marker}
    return {"changed": True, "consume": True, "pet_owner_marker": ""}


def tohelos_item_transition(
    *,
    item_valid,
    option,
    caster_party_mode,
    caster_id,
    party_leader_id=None,
):
    """Model ITEM_useEffectTohelos's destructive parse/mutation order.

    The item is detached from inventory before either argument field is parsed.
    Any parse failure still destroys the item instance.
    """
    if not item_valid:
        return {
            "changed": False,
            "consume": False,
            "target_id": None,
            "cutrate": None,
            "limitcount": None,
        }
    parts = str(option).split("|")
    target = party_leader_id if str(caster_party_mode) == "client" else caster_id
    if len(parts) < 1 or parts[0] == "":
        return {
            "changed": False,
            "consume": True,
            "target_id": target,
            "cutrate": None,
            "limitcount": None,
        }
    cutrate = max(0, int(parts[0]) if re.match(r"\s*[+-]?\d+", parts[0]) else 0)
    if len(parts) < 2 or parts[1] == "":
        return {
            "changed": False,
            "consume": True,
            "target_id": target,
            "cutrate": cutrate,
            "limitcount": None,
        }
    limitcount = max(0, int(parts[1]) if re.match(r"\s*[+-]?\d+", parts[1]) else 0)
    return {
        "changed": True,
        "consume": True,
        "target_id": target,
        "cutrate": cutrate,
        "limitcount": limitcount,
    }


def equipment_noenemy_level(evade_level):
    """ITEM_equipNoenemy quantizes positive argument levels into four bands."""
    value = int(evade_level)
    if value >= 200:
        return 200
    if value >= 120:
        return 120
    if value >= 80:
        return 80
    if value >= 40:
        return 40
    return 0


def remove_equipment_noenemy():
    """ITEM_remNoenemy always clears the connection-level equipment value."""
    return 0
