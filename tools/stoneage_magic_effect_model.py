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
    """Mirror the source's marker + one separator + integer convention.

    The old code advances by sizeof(marker-array), i.e. text length plus the
    terminating NUL. In the data syntax that effectively skips one separator
    byte after the marker. This helper accepts either one non-numeric separator
    or a directly adjacent integer to keep the semantic model encoding-neutral.
    """
    pos = str(text).find(str(marker))
    if pos < 0:
        return int(default)
    tail = str(text)[pos + len(str(marker)) :]
    if tail and tail[0] not in "+-0123456789":
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
