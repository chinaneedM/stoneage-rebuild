#!/usr/bin/env python3
"""Reference model for the convergent StoneAge save/logout persistence core."""

PERSISTED_SURFACES = (
    "char_data_ints",
    "char_data_strings",
    "character_flags",
    "skills",
    "items",
    "titles",
    "address_book",
    "carried_pets",
)

RUNTIME_ONLY_SURFACES = (
    "work_ints",
    "battle_runtime",
    "party_runtime",
    "channel_runtime",
    "connection_state",
)


def periodic_save_sweep_due(now_sec, last_sweep_sec):
    """The global sweep runs only when now > last_sweep + 10."""
    return int(now_sec) > int(last_sweep_sec) + 10


def periodic_character_save_due(
    *,
    connected,
    login_state,
    now_sec,
    last_save_sec,
    interval_sec,
):
    """Mirror chardatasavecheck's per-connection gate."""
    return (
        bool(connected)
        and str(login_state) == "LOGIN"
        and int(now_sec) - int(last_save_sec) > int(interval_sec)
    )


def save_request(*, trigger):
    """Return whether the save request asks SAAC to unlock the account."""
    trigger = str(trigger)
    if trigger in {"periodic", "savepoint", "manual"}:
        return {"unlock": False, "wait_for_ack_before_return": False}
    if trigger == "logout":
        return {"unlock": True, "wait_for_ack_before_return": False}
    raise ValueError("unknown save trigger")


def serialization_surface(*, include_pool_item=False, include_pool_pet=False):
    """Core character string persists data fields, not WORK/runtime fields."""
    persisted = list(PERSISTED_SURFACES)
    if include_pool_item:
        persisted.append("pool_items")
    if include_pool_pet:
        persisted.append("pool_pets")
    return {
        "persisted": tuple(persisted),
        "runtime_only": RUNTIME_ONLY_SURFACES,
    }


def logout_drop_items(items):
    """Delete every concrete item whose DROPATLOGOUT flag is true.

    This happens before final logout serialization, so those items are absent
    from the saved character snapshot.
    """
    kept = []
    deleted = []
    for item in items:
        if item is None:
            kept.append(None)
            continue
        if bool(item.get("drop_at_logout", False)):
            deleted.append(item)
            kept.append(None)
        else:
            kept.append(dict(item))
    return {
        "items_after_cleanup": tuple(kept),
        "deleted": tuple(deleted),
    }


def logout_sequence(*, in_battle, save=True):
    """Stable high-level ordering before runtime object destruction."""
    steps = []
    if in_battle:
        steps.extend(
            (
                "battle_escape_dp",
                "apply_pending_duelpoint_delta",
                "battle_exit",
            )
        )
    steps.extend(
        (
            "delete_drop_at_logout_items",
            "discharge_party",
            "cleanup_runtime_memberships",
            "pickup_follow_pet",
            "set_last_leave_time",
        )
    )
    if save:
        steps.append("send_async_save_unlock_true")
    steps.extend(
        (
            "notify_logout",
            "delete_runtime_pets",
            "delete_runtime_character",
        )
    )
    return tuple(steps)


def saac_save_sequence(*, unlock):
    """SAAC's old ordering: unlock occurs before serialization envelope/disk write."""
    steps = []
    if unlock:
        steps.append("unlock_account")
    steps.extend(
        (
            "build_save_envelope",
            "resolve_character_slot",
            "write_character_file",
            "send_save_result",
        )
    )
    return tuple(steps)


def save_send_return_value(*, serialization_ok=True):
    """GMSV returns after sending, not after receiving SAAC durability success."""
    return bool(serialization_ok)


def logout_ack_result(success):
    """Normal logout reply handling has no retry/recovery branch."""
    return {
        "client_message": "success" if success else "Cannot save",
        "connection_state_after": "NOTLOGIN",
        "character_index_after": -1,
        "retry": False,
        "rollback_runtime_character": False,
    }


def failed_logout_save_data_loss_risk():
    """Runtime object is already destroyed before asynchronous save ACK arrives."""
    return True


def normal_logout_uses_save():
    """All fixed ordinary disconnect/logout call sites observed pass TRUE."""
    return True


def observed_normal_save_false_callsite():
    """No normal fixed logout/disconnect call site with save=FALSE was found."""
    return False
