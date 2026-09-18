#!/usr/bin/env python3
"""Lightweight deterministic model for StoneAge presentation-only NPCs."""


def signboard_can_open(*, is_player, distance):
    return bool(is_player) and int(distance) <= 1


def signboard_render_mode(argument):
    return (
        "manor_placeholder"
        if "%manorid:" in str(argument)
        else "plain"
    )


def townpeople_can_talk(*, is_player, in_front_three):
    return bool(is_player) and bool(in_front_three)


def townpeople_variant_count(argument):
    if argument is None:
        return None
    return str(argument).count(",") + 1


def townpeople_choose(argument, pick=0):
    if argument is None:
        return {
            "deterministic": False,
            "reason": "source_uses_uninitialized_buffer_when_arg_missing",
        }
    parts = str(argument).split(",")
    return {
        "deterministic": True,
        "message": parts[int(pick) % len(parts)],
    }


def mic_init_shape(argument):
    text = str(argument)
    tokens = text.split("|") if "|" in text else []
    return {
        "free": "FREE" in text,
        "wind": "WIND" in text,
        "pipe_scoped": bool(tokens),
        "token_count": len(tokens),
        "mode": 0 if tokens else 1,
    }


def mic_talker_allowed(*, is_player, free, face_to_face_one):
    if not is_player:
        return False
    if free:
        return True
    return bool(face_to_face_one)


def mic_recipient_allowed(
    *,
    same_floor,
    scoped_mode,
    inside_rectangle=True,
):
    if not same_floor:
        return False
    if scoped_mode:
        return bool(inside_rectangle)
    return True


def mic_delivery(*, wind, recipient_in_battle):
    """Normal chat is always sent to an eligible recipient.

    WIND adds a message window only when the recipient is not in battle.
    """
    return {
        "send_chat": True,
        "send_window": bool(wind) and not bool(recipient_in_battle),
    }


def mic_family_branch(*, family_flag_nonzero, family_role_matches):
    return bool(family_flag_nonzero) and bool(family_role_matches)


def presentation_classes_mutate_player_core_state():
    return False


def recovered_25_shape():
    return {
        "SignBoard": {
            "refs": 181,
            "resolved": 181,
            "manor_placeholder": 4,
            "plain": 177,
        },
        "TownPeople": {
            "refs": 445,
            "resolved_files": 389,
            "inline": 34,
            "missing_files": 15,
            "noarg": 7,
        },
        "Mic": {
            "refs": 4,
            "resolved_files": 4,
            "pipe_scoped": 4,
            "free": 1,
            "wind": 0,
            "family_flag_nonzero": 0,
        },
    }
