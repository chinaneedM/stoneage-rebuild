#!/usr/bin/env python3
"""Deterministic reference model for the StoneAge Windowman routing core."""

BUTTON_OK = 0
BUTTON_CANCEL = 1
BUTTON_YES = 2
BUTTON_NO = 3
BUTTON_PREV = 4
BUTTON_NEXT = 5


def button_index(*, window_is_select, data=None, select_flags=0):
    """Mirror Windowman button decoding.

    For SELECT windows, atoi(data)+5 maps the first selection to button 6.
    For ordinary windows, the source checks bit flags in OK/CANCEL/YES/NO/
    PREV/NEXT order.
    """
    if window_is_select:
        try:
            button = int(str(data).strip()) + 5
        except (TypeError, ValueError):
            button = 5
        if button > 12:
            return None
        return button

    flags = int(select_flags)
    mapping = (
        (1, BUTTON_OK),
        (2, BUTTON_CANCEL),
        (4, BUTTON_YES),
        (8, BUTTON_NO),
        (16, BUTTON_PREV),
        (32, BUTTON_NEXT),
    )
    for bit, button in mapping:
        if flags & bit:
            return button
    return None


def has_item(item_ids, wanted):
    wanted = int(wanted)
    return any(int(item) == wanted for item in item_ids)


def route_button(
    *,
    button_used,
    gotowin=-1,
    checkhaveitem=-1,
    haveitemgotowin=-1,
    checkdonthaveitem=-1,
    donthaveitemgotowin=-1,
    item_ids=(),
):
    """Return the Windowman routing result without inventing mutations.

    Both item conditions run in source order. If both are configured and pass,
    the don't-have target overwrites the have-item target.
    """
    if not button_used:
        return {
            "routed": False,
            "reason": "button_unused",
            "target": None,
            "state_mutation": False,
        }

    newwin = -1

    if int(checkhaveitem) != -1:
        if not has_item(item_ids, checkhaveitem):
            return {
                "routed": False,
                "reason": "required_item_missing",
                "target": None,
                "state_mutation": False,
            }
        newwin = int(haveitemgotowin)

    if int(checkdonthaveitem) != -1:
        if has_item(item_ids, checkdonthaveitem):
            return {
                "routed": False,
                "reason": "forbidden_item_present",
                "target": None,
                "state_mutation": False,
            }
        newwin = int(donthaveitemgotowin)

    if newwin == -1:
        newwin = int(gotowin)

    return {
        "routed": True,
        "reason": "route",
        "target": newwin,
        "state_mutation": False,
        "next_action": "read_target_window_and_send",
    }


def validate_button_definition(
    *,
    gotowin=-1,
    checkhaveitem=-1,
    haveitemgotowin=-1,
    checkdonthaveitem=-1,
    donthaveitemgotowin=-1,
):
    """Mirror endbutton's structural validation."""
    if int(gotowin) != -1:
        return True

    have_complete = (
        int(checkhaveitem) != -1 and int(haveitemgotowin) != -1
    )
    dont_complete = (
        int(checkdonthaveitem) != -1 and int(donthaveitemgotowin) != -1
    )
    return have_complete or dont_complete


def parsed_but_inert_fields():
    """Fields read into Windowman state but never applied by the callback."""
    return ("takeitem", "giveitem")


def unparsed_placeholder_fields():
    """Fields present in buttonproc but lacking fixed-source config parsing."""
    return ("warp", "battle")


def recovered_25_active_control_fields():
    """Measured active control surface of the 13 resolved 2.5 conff files."""
    return ("gotowin",)


def interaction_allowed(*, is_player, in_front_one, callback_distance=None):
    if not is_player:
        return False
    if not in_front_one:
        return False
    if callback_distance is not None and int(callback_distance) > 1:
        return False
    return True
