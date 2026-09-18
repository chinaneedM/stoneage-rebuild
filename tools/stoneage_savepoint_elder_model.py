#!/usr/bin/env python3
"""Reference model for StoneAge elder/save-point/return-point core semantics.

The model intentionally separates convergent state transitions from source-version
interaction/save-call differences. It does not copy NPC content payloads.
"""

from copy import deepcopy

MAX_ELDERS = 128
ELDER_INDEX_START = 4

# Fixed descendants share these ordinary built-in elder slots.
BUILTIN_ELDERS = {
    0: (1006, 15, 22),
    1: (2006, 20, 16),
    2: (3006, 21, 16),
    3: (4006, 14, 20),
    4: (7770, 9, 10),
}


def new_elder_registry():
    """Return the server elder-position array as a Python list.

    C static storage zero-initializes unspecified slots, so this model keeps
    (0, 0, 0) in every unregistered slot instead of using None.
    """
    registry = [(0, 0, 0) for _ in range(MAX_ELDERS)]
    for elder_id, pos in BUILTIN_ELDERS.items():
        registry[elder_id] = pos
    return registry


def register_dynamic_elder(
    registry,
    *,
    elder_id,
    floor,
    x,
    y,
    coordinate_valid=True,
):
    """Mirror SavePointInit + CHAR_ElderSetPosition's convergent gate."""
    elder_id = int(elder_id)
    if not coordinate_valid:
        return False
    if elder_id < ELDER_INDEX_START or elder_id >= MAX_ELDERS:
        return False
    registry[elder_id] = (int(floor), int(x), int(y))
    return True


def get_elder_position(registry, elder_id):
    """Mirror CHAR_getElderPosition's range check only."""
    elder_id = int(elder_id)
    if elder_id < 0 or elder_id >= len(registry):
        return None
    return tuple(registry[elder_id])


def ordinary_birth_state(hometown, savepoint_mask=0):
    """Ordinary four-hometown initialization shared by the fixed descendants."""
    hometown = int(hometown)
    if hometown < 0 or hometown > 3:
        return None
    return {
        "position": BUILTIN_ELDERS[hometown],
        "last_talk_elder": hometown,
        "savepoint_mask": int(savepoint_mask) | (1 << hometown),
    }


def signed_shift_is_portable(shiftbit, int_bits=32):
    """Whether signed C expression (1 << shiftbit) is safely representable.

    The descendants do not perform this guard. This helper documents the
    representation mismatch between a 128-slot elder registry and one signed
    integer save-point bit field; it is not an inferred historical clamp.
    """
    shiftbit = int(shiftbit)
    int_bits = int(int_bits)
    return 0 <= shiftbit < int_bits - 1


def source_set_savepoint_flag(mask, elder_id):
    """Mathematical equivalent of point | (1 << elder_id).

    Callers can use signed_shift_is_portable() to distinguish source operations
    whose behavior is not portable for an ordinary 32-bit signed C int.
    """
    return int(mask) | (1 << int(elder_id))


def source_savepoint_flag_is_set(mask, elder_id):
    bit = 1 << int(elder_id)
    return (int(mask) & bit) == bit


def legacy_interaction_allowed(*, in_front, dead, same_cell):
    """gavinlinasd/iriselia save-point talk gate.

    The source's same-cell exception bypasses both the facing failure and the
    death check. The model preserves that quirk rather than silently fixing it.
    """
    if (not bool(in_front)) or bool(dead):
        return bool(same_cell)
    return True


def bismarck_interaction_allowed(*, distance, dead, range_limit=2):
    """Later Bismarck gate: dead is always rejected; facing is not required."""
    return (not bool(dead)) and int(distance) <= int(range_limit)


def begin_savepoint_talk(
    *,
    savepoint_mask,
    last_talk_elder,
    elder_id,
    noitem=False,
    requirement_available=False,
):
    """Model the state decision made by the ordinary talk callback.

    Requirement parsing/deletion is kept outside this function because the
    concrete GetItem expression is content data. requirement_available
    represents NPC_UsedCheck(..., flg=0).

    Returns an immutable-style result with the new persistent state and the
    next UI/action stage.
    """
    elder_id = int(elder_id)
    mask = int(savepoint_mask)

    # NOITEM sets the unlock bit before the code checks the bit.
    if noitem:
        mask = source_set_savepoint_flag(mask, elder_id)

    if source_savepoint_flag_is_set(mask, elder_id):
        return {
            "savepoint_mask": mask,
            "last_talk_elder": elder_id,
            "stage": "activated",
            "needs_confirmation": False,
        }

    if requirement_available:
        return {
            "savepoint_mask": mask,
            "last_talk_elder": int(last_talk_elder),
            "stage": "confirmation",
            "needs_confirmation": True,
        }

    return {
        "savepoint_mask": mask,
        "last_talk_elder": int(last_talk_elder),
        "stage": "requirements_missing",
        "needs_confirmation": False,
    }


def confirm_savepoint_unlock(
    *,
    savepoint_mask,
    last_talk_elder,
    elder_id,
    confirmed,
    requirement_consume_success,
):
    """Model the YES-window path after a locked save point offered activation."""
    if not confirmed:
        return {
            "savepoint_mask": int(savepoint_mask),
            "last_talk_elder": int(last_talk_elder),
            "activated": False,
        }
    if not requirement_consume_success:
        return {
            "savepoint_mask": int(savepoint_mask),
            "last_talk_elder": int(last_talk_elder),
            "activated": False,
        }

    elder_id = int(elder_id)
    return {
        "savepoint_mask": source_set_savepoint_flag(savepoint_mask, elder_id),
        "last_talk_elder": elder_id,
        "activated": True,
    }


def return_point_resolution(registry, *, last_talk_elder):
    """Resolve the position consumed by record-point return callers.

    CHAR_getElderPosition validates only the array index. An in-range slot that
    was never registered therefore resolves to the C static-zero tuple.
    """
    pos = get_elder_position(registry, last_talk_elder)
    return {
        "lookup_ok": pos is not None,
        "position": pos,
        "registered_nonzero": bool(pos and pos != (0, 0, 0)),
    }


def old_login_appear_return(
    registry,
    *,
    saved_position,
    last_talk_elder,
    appear_floor_member,
):
    """Model the observed older login policy without fabricating fallback data.

    If the saved floor is not an appear-table member, it is retained.
    If it is a member, the caller asks for LASTTALKELDER and uses that position.
    We expose lookup failure instead of simulating C uninitialized locals.
    """
    saved = tuple(saved_position)
    if not appear_floor_member:
        return {
            "position": saved,
            "redirected": False,
            "lookup_ok": True,
        }

    resolved = get_elder_position(registry, last_talk_elder)
    if resolved is None:
        return {
            "position": None,
            "redirected": True,
            "lookup_ok": False,
        }
    return {
        "position": resolved,
        "redirected": True,
        "lookup_ok": True,
    }


def savepoint_persistence_policy(lineage, *, char_is_save=True):
    """Expose observed fixed-lineage immediate-save differences.

    All returned save requests use unlock=False. This only describes the
    save-point callback path, not periodic or logout persistence.
    """
    lineage = str(lineage)
    if lineage in {"gavinlinasd", "iriselia"}:
        return {
            "immediate_save_on_activation": True,
            "unlock": False,
            "duplicate_save_on_revisit_observed": True,
        }
    if lineage == "bismarck":
        return {
            "immediate_save_on_activation": False,
            "conditional_revisit_save": bool(char_is_save),
            "unlock": False,
            "duplicate_save_on_revisit_observed": False,
        }
    raise ValueError("unknown lineage")


def copy_state(state):
    """Tiny helper for consumers that want mutation-isolated dictionaries."""
    return deepcopy(state)
