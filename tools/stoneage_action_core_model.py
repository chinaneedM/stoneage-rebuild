#!/usr/bin/env python3
"""Deterministic routing model for the StoneAge Action NPC."""

ACTION_TO_KEY = {
    "attack": "attack",
    "damage": "damage",
    "down": "down",
    "sit": "sit",
    "hand": "hand",
    "pleasure": "pleasure",
    "angry": "angry",
    "sad": "sad",
    "guard": "guard",
    "nod": "nod",
    "throw": "throw",
}

RECOVERED_25_KEYS = (
    "normal",
    "attack",
    "damage",
    "down",
    "sit",
    "hand",
    "pleasure",
    "angry",
    "sad",
    "guard",
    "nod",
    "throw",
)


def talked_response_key(*, is_player, in_front_one, normal_configured):
    if not is_player:
        return None
    if not in_front_one:
        return None
    if not normal_configured:
        return None
    return "normal"


def watch_response_key(
    *,
    object_is_character,
    is_player,
    face_to_face_one,
    action,
    configured_keys,
):
    if not object_is_character:
        return None
    if not is_player:
        return None
    if not face_to_face_one:
        return None

    key = ACTION_TO_KEY.get(str(action))
    if key is None:
        return None
    if key not in set(configured_keys):
        return None
    return key


def action_has_state_mutation():
    return False


def normal_is_invalid_action_fallback():
    """Despite the source comment, Watch has no normal fallback."""
    return False


def msgcol_initialization_status(configured_msgcol=None):
    """Describe the literal fixed-source initialization defect.

    NPC_ActionInit passes an uninitialized local char array to
    NPC_Util_GetNumFromStrWithDelim instead of first calling GetArgStr.
    C therefore gives no deterministic configured/default color result.
    """
    return {
        "configured_value": configured_msgcol,
        "deterministic_from_fixed_source": False,
        "reason": "uninitialized_argstr_read",
    }


def recovered_25_surface():
    return {
        "refs": 8,
        "all_response_keys_present": RECOVERED_25_KEYS,
        "msgcol_configured_value": 1,
        "msgcol_blocks": 8,
    }
