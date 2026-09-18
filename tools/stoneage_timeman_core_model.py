#!/usr/bin/env python3
"""Deterministic reference model for the StoneAge TimeMan core."""

LSTIME_SECONDS_PER_DAY = 5400
LSTIME_HOURS_PER_DAY = 1024

TIME_TABLE = (
    ("ALLNIGHT", 301, 700),
    ("ALLNOON", 701, 300),
    ("AM", 501, 125),
    ("PM", 126, 500),
    ("FORE", 701, 125),
    ("AFTER", 126, 300),
    ("EVNING", 301, 500),
    ("MORNING", 501, 700),
    ("FREE", 0, 1024),
)


def resolve_time_rule(value):
    if value is None:
        return None
    text = str(value)
    for name, born, dead in TIME_TABLE:
        if name in text:
            return (name, born, dead)
    return None


def alternate_graphic(change_no):
    """Missing or any value containing CLS maps to hidden graphic 9999."""
    if change_no is None:
        return 9999
    text = str(change_no)
    if "CLS" in text:
        return 9999
    try:
        return int(text.strip())
    except ValueError:
        return 0


def active_at_hour(born, dead, hour):
    """Mirror NPC_TimeManWatch's strict endpoint comparisons."""
    born = int(born)
    dead = int(dead)
    hour = int(hour)

    if born < dead:
        return born < hour and dead > hour

    return (
        (born < hour and LSTIME_HOURS_PER_DAY > hour)
        or (0 < hour and dead > hour)
    )


def state_for_hour(*, original_graphic, alternate, born, dead, hour):
    active = active_at_hour(born, dead, hour)
    if active:
        return {
            "mode": 0,
            "graphic": int(original_graphic),
            "message_key": "main_msg",
            "active": True,
        }
    return {
        "mode": 1,
        "graphic": int(alternate),
        "message_key": "change_msg",
        "active": False,
    }


def watch_transition(
    *,
    current_now_graphic,
    original_graphic,
    alternate,
    born,
    dead,
    hour,
):
    target = state_for_hour(
        original_graphic=original_graphic,
        alternate=alternate,
        born=born,
        dead=dead,
        hour=hour,
    )
    if int(current_now_graphic) == int(target["graphic"]):
        return {
            **target,
            "changed": False,
            "broadcast": False,
        }
    return {
        **target,
        "changed": True,
        "broadcast": True,
        "now_graphic_after": target["graphic"],
    }


def can_talk(*, base_graphic, is_player, face_or_near, in_front):
    if int(base_graphic) == 9999:
        return False
    if not is_player:
        return False
    if not face_or_near:
        return False
    if not in_front:
        return False
    return True


def message_key_for_mode(mode):
    return "main_msg" if int(mode) == 0 else "change_msg"


def choose_message_variant(message, pick=0):
    parts = str(message).split(",")
    if not parts:
        return ""
    return parts[int(pick) % len(parts)]


def scaled_hour_from_day_seconds(day_seconds):
    """Equivalent 1024-unit LS hour for a position in the 5400-second day."""
    seconds = int(day_seconds) % LSTIME_SECONDS_PER_DAY
    return seconds * LSTIME_HOURS_PER_DAY // LSTIME_SECONDS_PER_DAY


def init_model(*, base_graphic, time_value, change_no=None):
    resolved = resolve_time_rule(time_value)
    if resolved is None:
        return {"success": False, "reason": "unknown_time"}
    name, born, dead = resolved
    return {
        "success": True,
        "time_rule": name,
        "born": born,
        "dead": dead,
        "original_graphic": int(base_graphic),
        "alternate_graphic": alternate_graphic(change_no),
        "mode_explicitly_initialized": False,
        "now_graphic_explicitly_initialized": False,
        "first_time_state_change_requires_watch": True,
    }
