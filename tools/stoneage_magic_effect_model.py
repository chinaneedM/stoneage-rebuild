#!/usr/bin/env python3
"""Reference model for the convergent StoneAge ordinary magic-effect core.

Scope is the old/common unguarded magic family:
Recovery, OtherRecovery, FieldAttChange, StatusChange, MagicDef,
StatusRecovery, Ressurect, AttReverse and ResAndDef.

Later macro-controlled magic families are intentionally excluded.
"""

import re

COMMON_MAGIC_EFFECTS = (
    "recovery",
    "other_recovery",
    "field_att_change",
    "status_change",
    "magic_def",
    "status_recovery",
    "ressurect",
    "att_reverse",
    "res_and_def",
)

BATTLE_ONLY_EFFECTS = frozenset(
    {
        "field_att_change",
        "status_change",
        "magic_def",
        "status_recovery",
        "ressurect",
        "att_reverse",
        "res_and_def",
    }
)

FIELD_CAPABLE_EFFECTS = frozenset({"recovery", "other_recovery"})



SIDE_OFFSET = 10
TARGET_SIDE_0 = 20
TARGET_SIDE_1 = 21
TARGET_ALL = 22


def common_alive_target_list(to_no, alive_slots, *, side_offset=SIDE_OFFSET):
    """Logical target expansion from the old non-attack-magic BATTLE_MultiList path.

    Slots 0..9 are side 0; 10..19 are side 1. Single-target requests include
    the target only when BATTLE_TargetCheck succeeds. Side/all selectors include
    only valid living targets. Unknown selectors fall through to one raw slot,
    matching the legacy fallback branch.
    """
    to_no = int(to_no)
    alive = {int(x) for x in alive_slots}
    if 0 <= to_no < side_offset * 2:
        return (to_no,) if to_no in alive else ()
    if to_no == TARGET_SIDE_0:
        return tuple(i for i in range(0, side_offset) if i in alive)
    if to_no == TARGET_SIDE_1:
        return tuple(i for i in range(side_offset, side_offset * 2) if i in alive)
    if to_no == TARGET_ALL:
        return tuple(i for i in range(0, side_offset * 2) if i in alive)
    return (to_no,)


def common_dead_target_list(to_no, dead_slots, *, side_offset=SIDE_OFFSET):
    """Logical target expansion from BATTLE_MultiListDead."""
    to_no = int(to_no)
    dead = {int(x) for x in dead_slots}
    if 0 <= to_no < side_offset * 2:
        return (to_no,) if to_no in dead else ()
    if to_no == TARGET_SIDE_0:
        return tuple(i for i in range(0, side_offset) if i in dead)
    if to_no == TARGET_SIDE_1:
        return tuple(i for i in range(side_offset, side_offset * 2) if i in dead)
    if to_no == TARGET_ALL:
        return tuple(i for i in range(0, side_offset * 2) if i in dead)
    return (to_no,)


def recovery_target_allowed(*, magic_target, caster_battle_no, to_no):
    """Packet-side recovery target guard from MAGIC_Recovery_Battle.

    MAGIC_TARGET 0 is self-only. MAGIC_TARGET 1 is single-target only and
    rejects aggregate selectors (20+). Other target modes are delegated to
    BATTLE_MultiList.
    """
    magic_target = int(magic_target)
    caster_battle_no = int(caster_battle_no)
    to_no = int(to_no)
    if magic_target == 0:
        return to_no == caster_battle_no
    if magic_target == 1:
        return to_no < TARGET_SIDE_0
    return True

def recovery_wrapper_target_allowed(effect, *, to_no, battling):
    """Top-level wrapper quirk around ordinary recovery targeting.

    MAGIC_Recovery contains an explicit battle-time rejection for TARGET_ALL
    (22), added as an old whole-target bug fix. MAGIC_OtherRecovery does not
    contain that exact wrapper rejection.
    """
    if not battling:
        return True
    if str(effect) == "recovery" and int(to_no) == TARGET_ALL:
        return False
    return True


def c_atoi(value):
    """Small C-atoi model: leading whitespace/sign/digits; no digits => 0."""
    text = str(value)
    m = re.match(r"\s*([+-]?\d+)", text)
    return int(m.group(1), 10) if m else 0


def recovery_rate(*, vital, is_player):
    """Observed GetRecoveryRate multiplier."""
    factor = 0.00010 if is_player else 0.00005
    return 1.0 + factor * int(vital)


def common_cast_route(
    effect,
    *,
    caster_valid,
    battle_mode_init,
    current_mp,
    mp_cost,
    battling,
    target_valid=True,
):
    """Model common top-level gating and the historically important MP order.

    Most battle-only effects deduct MP before discovering that the cast was
    attempted outside battle. Recovery effects can route to field behavior.
    Field recovery validates the target only after MP has been deducted.
    """
    effect = str(effect)
    if effect not in COMMON_MAGIC_EFFECTS:
        raise ValueError("effect is outside the ordinary common magic core")

    current_mp = int(current_mp)
    mp_cost = int(mp_cost)

    if not caster_valid:
        return {
            "accepted": False,
            "remaining_mp": current_mp,
            "mp_spent": 0,
            "route": "reject_invalid_caster",
        }
    if battle_mode_init:
        return {
            "accepted": False,
            "remaining_mp": current_mp,
            "mp_spent": 0,
            "route": "reject_battle_init",
        }
    if current_mp < mp_cost:
        return {
            "accepted": False,
            "remaining_mp": current_mp,
            "mp_spent": 0,
            "route": "reject_insufficient_mp",
        }

    remaining = current_mp - mp_cost

    if effect in BATTLE_ONLY_EFFECTS:
        if not battling:
            return {
                "accepted": False,
                "remaining_mp": remaining,
                "mp_spent": mp_cost,
                "route": "reject_not_battling_after_mp",
            }
        return {
            "accepted": True,
            "remaining_mp": remaining,
            "mp_spent": mp_cost,
            "route": "battle",
        }

    # Recovery and OtherRecovery.
    if battling:
        return {
            "accepted": True,
            "remaining_mp": remaining,
            "mp_spent": mp_cost,
            "route": "battle",
        }
    if not target_valid:
        return {
            "accepted": False,
            "remaining_mp": remaining,
            "mp_spent": mp_cost,
            "route": "reject_invalid_field_target_after_mp",
        }
    return {
        "accepted": True,
        "remaining_mp": remaining,
        "mp_spent": mp_cost,
        "route": "field",
    }


def parse_recovery_option(option):
    """Battle recovery uses atoi(option), plus '%' as a percentage flag."""
    text = str(option)
    return {"power": c_atoi(text), "percent": "%" in text}


def battle_recovery_gain(*, power, percent, max_hp, rate, rolled_power):
    """Ordinary non-riding battle recovery after RAND has produced rolled_power."""
    amount = float(rolled_power)
    if percent:
        amount *= int(max_hp) * 0.01
    amount *= float(rate)
    return int(amount)


def field_recovery_gain(*, rate, rolled_power):
    """Field recovery has no '%' branch; it scales the RAND result by rate."""
    return int(float(rolled_power) * float(rate))


def parse_after_marker(text, marker, default):
    """Mirror the source's marker + exactly one separator convention.

    The C code advances by sizeof(marker-array), not strlen(marker). Because
    sizeof includes the terminating NUL, the runtime pointer skips the marker
    plus one additional byte from the option string. The preserved data syntax
    therefore needs one separator byte such as '=' before the integer.
    """
    pos = str(text).find(str(marker))
    if pos < 0:
        return int(default)
    tail = str(text)[pos + len(str(marker)) :]
    if not tail:
        return int(default)
    tail = tail[1:]
    m = re.match(r"\s*([+-]?\d+)", tail)
    return int(m.group(1), 10) if m else int(default)


def _find_first_token(text, tokens):
    """Return (index, token, tail-after-token) by earliest textual occurrence."""
    text = str(text)
    hits = []
    for index, token in enumerate(tokens):
        pos = text.find(str(token))
        if pos >= 0:
            hits.append((pos, index, str(token)))
    if not hits:
        return None
    pos, index, token = min(hits, key=lambda x: (x[0], x[1]))
    return index, token, text[pos + len(token) :]


def parse_field_attribute_option(option, attr_tokens):
    """Parse the stable field-attribute option semantics.

    attr_tokens should follow source order: NONE, EARTH, WATER, FIRE, WIND.
    """
    found = _find_first_token(option, attr_tokens)
    if found is None:
        return None
    attr, _token, tail = found
    m = re.match(r"\s*([+-]?\d+)", tail)
    power = int(m.group(1), 10) if m else 30
    if power < 0 or power > 100:
        power = 30
    turn = parse_after_marker(tail, "turn", 3)
    return {"attribute": attr, "power": power, "turn": turn}


def parse_status_change_option(option, status_tokens):
    """Parse ordinary status magic: status + optional turn + success."""
    found = _find_first_token(option, status_tokens)
    if found is None:
        return None
    status, _token, tail = found
    return {
        "status": status,
        "turn": parse_after_marker(tail, "turn", 3),
        "success": parse_after_marker(tail, "成", 15),
    }


def parse_magic_def_option(option, defense_tokens):
    """Parse defense-kind and duration; duration defaults to 3 turns."""
    found = _find_first_token(option, defense_tokens)
    if found is None:
        return None
    kind, _token, tail = found
    return {"kind": kind, "turn": parse_after_marker(tail, "turn", 3)}


def parse_resurrection_option(option):
    text = str(option)
    return {"power": c_atoi(text), "percent": "%" in text}


def resurrection_gain(*, power, percent, max_hp, rolled_power=None):
    """Observed BATTLE_MultiRessurect HP gain.

    Important preserved quirk: for nonzero power the source calculates a
    percentage value first when '%' is present, then overwrites it with
    RAND(power*0.9, power*1.1). Thus percent has no effect on final HP gain.
    power==0 means full MAXHP.
    """
    power = int(power)
    if power == 0:
        return int(max_hp)
    if rolled_power is None:
        raise ValueError("rolled_power is required for nonzero resurrection power")
    return max(1, int(rolled_power))


def status_recovery_transition(active_statuses, *, requested_status, confusion_index):
    """Mirror the old single-status recovery selection quirk.

    The source scans all status slots and keeps the highest-index active status.
    It can clear that one status if explicitly requested, or if requested_status
    is zero and the selected status is within the ordinary bad-status range.
    """
    active = {int(x) for x in active_statuses if int(x) > 0}
    selected = max(active) if active else 0
    clear = (
        selected != 0
        and (
            int(requested_status) == selected
            or (
                int(requested_status) == 0
                and selected <= int(confusion_index)
            )
        )
    )
    if clear:
        active.remove(selected)
    return {
        "selected_status": selected,
        "cleared": clear,
        "active_statuses": tuple(sorted(active)),
    }


def magic_def_transition(*, current_turns, kind, turn):
    out = dict(current_turns)
    out[int(kind)] = int(turn)
    return out


def att_reverse_transition(*, battle_flags, reverse_bit):
    """BATTLE_MultiAttReverse toggles, rather than merely enabling, the flag."""
    return int(battle_flags) ^ int(reverse_bit)


def att_reverse_cast_transition(
    *,
    battle_flags,
    reverse_bit,
    earth,
    water,
    fire,
    wind,
):
    """Apply the immediate BATTLE_MultiAttReverse + BATTLE_AttReverse behavior.

    The XOR happens first. If the new reverse flag is on, fixed elemental
    values are swapped earth<->fire and water<->wind. If the new flag is off,
    BATTLE_AttReverse returns immediately, so the current fixed values remain
    unchanged until the next parameter refresh.
    """
    flags = att_reverse_transition(
        battle_flags=battle_flags,
        reverse_bit=reverse_bit,
    )
    attrs = {
        "earth": int(earth),
        "water": int(water),
        "fire": int(fire),
        "wind": int(wind),
    }
    if flags & int(reverse_bit):
        attrs = {
            "earth": int(fire),
            "water": int(wind),
            "fire": int(earth),
            "wind": int(water),
        }
    return {"battle_flags": flags, "attributes": attrs}


def att_reverse_precommand_refresh(
    *,
    battle_flags,
    reverse_bit,
    earth,
    water,
    fire,
    wind,
):
    """Model parameter refresh: rebuild normal fixed attrs, then reapply reverse."""
    attrs = {
        "earth": int(earth),
        "water": int(water),
        "fire": int(fire),
        "wind": int(wind),
    }
    if int(battle_flags) & int(reverse_bit):
        attrs = {
            "earth": int(fire),
            "water": int(wind),
            "fire": int(earth),
            "wind": int(water),
        }
    return attrs


def res_and_def_transition(
    *,
    is_dead,
    is_pvp_player,
    current_hp,
    max_hp,
    power,
    percent,
    rolled_power,
    magic_def_turns,
    magic_def_kind,
    turn,
):
    """Common combined resurrection + magic-defense target transition."""
    if is_pvp_player or not is_dead:
        return {
            "changed": False,
            "is_dead": bool(is_dead),
            "hp": int(current_hp),
            "magic_def_turns": dict(magic_def_turns),
        }

    gain = resurrection_gain(
        power=power,
        percent=percent,
        max_hp=max_hp,
        rolled_power=rolled_power,
    )
    hp = min(int(current_hp) + gain, int(max_hp))
    defenses = magic_def_transition(
        current_turns=magic_def_turns,
        kind=magic_def_kind,
        turn=turn,
    )
    return {
        "changed": True,
        "is_dead": False,
        "hp": hp,
        "magic_def_turns": defenses,
    }
