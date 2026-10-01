#!/usr/bin/env python3
"""Fixed-descendant AttackMagic footprint geometry and side-record selection."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cmp_to_key

TARGET_SIDE_0 = 20
TARGET_SIDE_1 = 21
TARGET_ALL = 22
TARGET_SIDE_1_B_ROW = 23
TARGET_SIDE_1_F_ROW = 24
TARGET_SIDE_0_F_ROW = 25
TARGET_SIDE_0_B_ROW = 26

CHAR_TABLE = (
    (13, 11, 10, 12, 14),
    (18, 16, 15, 17, 19),
    (8, 6, 5, 7, 9),
    (3, 1, 0, 2, 4),
)

SLOT_COORD = {
    slot: (row, col)
    for row, values in enumerate(CHAR_TABLE)
    for col, slot in enumerate(values)
}


def _sign(value: int) -> int:
    value = int(value)
    return (value > 0) - (value < 0)


def source_sort_compare(left: int, right: int) -> int:
    """Exact fixed-source SortLoc comparator, including its right-side typo."""
    left = int(left)
    right = int(right)
    if left not in SLOT_COORD or right not in SLOT_COORD:
        raise ValueError("battle slot must be 0..19")
    ly, lx = SLOT_COORD[left]
    ry, rx = SLOT_COORD[right]
    if left >= 10:
        if ly != ry:
            return ly - ry
        return lx - rx
    if ly != ry:
        return ry - ly
    # Source reads ele2basex - ele1basey here, not ele1basex.
    return rx - ly


def source_sort_is_portable(slots) -> bool:
    """Whether SortLoc defines a strict ordering over this concrete target set."""
    values = tuple(dict.fromkeys(int(x) for x in slots))
    if len(values) <= 1:
        return True
    for value in values:
        if value not in SLOT_COORD:
            raise ValueError("battle slot must be 0..19")
        if source_sort_compare(value, value) != 0:
            return False
    for left in values:
        for right in values:
            if left == right:
                continue
            if _sign(source_sort_compare(left, right)) != -_sign(
                source_sort_compare(right, left)
            ):
                return False
    for a in values:
        for b in values:
            for c in values:
                if source_sort_compare(a, b) < 0 and source_sort_compare(b, c) < 0:
                    if source_sort_compare(a, c) >= 0:
                        return False
    return True


def source_sorted_targets(slots):
    values = tuple(dict.fromkeys(int(x) for x in slots))
    if not source_sort_is_portable(values):
        return None
    return tuple(sorted(values, key=cmp_to_key(source_sort_compare)))


def record_index_for_attacker(*, magic_idx: int, attacker_slot: int) -> int:
    """BATTLE_MultiAttMagic picks odd record for side 0, even for side 1."""
    magic_idx = int(magic_idx)
    attacker_slot = int(attacker_slot)
    if magic_idx < 0:
        raise ValueError("magic_idx cannot be negative")
    if not 0 <= attacker_slot < 20:
        raise ValueError("attacker_slot must be 0..19")
    return magic_idx * 2 + (1 if attacker_slot < 10 else 0)


def matrix_from_attmagic_record(record):
    """Decode tagAttMagic.siField[3][5] from a 33-word record."""
    values = tuple(int(x) for x in record)
    if len(values) != 33:
        raise ValueError("attmagic record must contain 33 words")
    cells = values[18:33]
    return tuple(tuple(cells[row * 5 : row * 5 + 5]) for row in range(3))


def _side_slots(target: int):
    return range(0, 10) if int(target) < 10 else range(10, 20)


def normalize_attack_magic_selector(
    selector: int,
    *,
    alive_slots,
    retarget_rolls_0_9=(),
):
    """Reconstruct BATTLE_MultiList normalization relevant to AttackMagic."""
    selector = int(selector)
    alive = {int(x) for x in alive_slots if 0 <= int(x) < 20}

    if 0 <= selector < 20:
        candidates = tuple(slot for slot in _side_slots(selector) if slot in alive)
        if not candidates:
            return None
        if selector in alive:
            return selector
        for roll in (int(x) for x in retarget_rolls_0_9):
            if not 0 <= roll <= 9:
                raise ValueError("retarget roll must be 0..9")
            if roll < len(candidates):
                return candidates[roll]
        raise ValueError("dead single target requires a successful retarget roll")

    row_slots = {
        TARGET_SIDE_0_B_ROW: tuple(range(0, 5)),
        TARGET_SIDE_0_F_ROW: tuple(range(5, 10)),
        TARGET_SIDE_1_B_ROW: tuple(range(10, 15)),
        TARGET_SIDE_1_F_ROW: tuple(range(15, 20)),
    }
    fallback = {
        TARGET_SIDE_0_B_ROW: TARGET_SIDE_0_F_ROW,
        TARGET_SIDE_0_F_ROW: TARGET_SIDE_0_B_ROW,
        TARGET_SIDE_1_B_ROW: TARGET_SIDE_1_F_ROW,
        TARGET_SIDE_1_F_ROW: TARGET_SIDE_1_B_ROW,
    }
    if selector in row_slots:
        if any(slot in alive for slot in row_slots[selector]):
            return selector
        alternate = fallback[selector]
        if any(slot in alive for slot in row_slots[alternate]):
            return alternate
        return None

    return selector


def _matrix_enabled(matrix, row: int, col: int) -> bool:
    return bool(int(matrix[row][col]))


def _append_if_alive(out, slot, alive):
    if slot in alive:
        out.append(slot)


def footprint_target_set(*, selector: int, matrix, alive_slots):
    """Expand a normalized selector through tagAttMagic.siField[3][5]."""
    selector = int(selector)
    matrix = tuple(tuple(int(x) for x in row) for row in matrix)
    if len(matrix) != 3 or any(len(row) != 5 for row in matrix):
        raise ValueError("attack-magic field matrix must be 3x5")
    alive = {int(x) for x in alive_slots if 0 <= int(x) < 20}
    out = []

    if 0 <= selector < 20:
        base_y, base_x = SLOT_COORD[selector]
        for matrix_row, battle_row in enumerate(range(base_y - 1, base_y + 2)):
            if selector < 10:
                if battle_row < 2 or battle_row > 3:
                    continue
            else:
                if battle_row < 0 or battle_row > 1:
                    continue
            for matrix_col in range(5):
                x = base_x - 2 + matrix_col
                if not 0 <= x <= 4:
                    continue
                if _matrix_enabled(matrix, matrix_row, matrix_col):
                    _append_if_alive(out, CHAR_TABLE[battle_row][x], alive)

    elif selector == TARGET_SIDE_0:
        for matrix_row in range(2):
            battle_row = matrix_row + 2
            for col in range(5):
                if _matrix_enabled(matrix, matrix_row, col):
                    _append_if_alive(out, CHAR_TABLE[battle_row][col], alive)

    elif selector == TARGET_SIDE_1:
        for matrix_row in range(2):
            battle_row = matrix_row
            for col in range(5):
                if _matrix_enabled(matrix, matrix_row, col):
                    _append_if_alive(out, CHAR_TABLE[battle_row][col], alive)

    elif selector in {
        TARGET_SIDE_1_B_ROW,
        TARGET_SIDE_1_F_ROW,
        TARGET_SIDE_0_F_ROW,
        TARGET_SIDE_0_B_ROW,
    }:
        base_y = selector - TARGET_SIDE_1_B_ROW
        for matrix_row, battle_row in enumerate(range(base_y - 1, base_y + 2)):
            if selector in {TARGET_SIDE_0_F_ROW, TARGET_SIDE_0_B_ROW}:
                if battle_row < 2 or battle_row > 3:
                    continue
            else:
                if battle_row < 0 or battle_row > 1:
                    continue
            for col in range(5):
                if _matrix_enabled(matrix, matrix_row, col):
                    _append_if_alive(out, CHAR_TABLE[battle_row][col], alive)

    # TARGET_ALL (22) has no explicit branch in BATTLE_MultiAttMagic.
    return tuple(dict.fromkeys(out))


@dataclass(frozen=True)
class AttackMagicFootprint:
    magic_idx: int
    attacker_slot: int
    record_index: int
    requested_selector: int
    normalized_selector: int | None
    targets_in_source_build_order: tuple[int, ...]
    source_sort_portable: bool
    source_sorted_targets: tuple[int, ...] | None


def resolve_attack_magic_footprint(
    *,
    magic_idx: int,
    attacker_slot: int,
    selector: int,
    record,
    alive_slots,
    retarget_rolls_0_9=(),
) -> AttackMagicFootprint:
    record_index = record_index_for_attacker(
        magic_idx=magic_idx,
        attacker_slot=attacker_slot,
    )
    normalized = normalize_attack_magic_selector(
        selector,
        alive_slots=alive_slots,
        retarget_rolls_0_9=retarget_rolls_0_9,
    )
    if normalized is None:
        targets = ()
    else:
        targets = footprint_target_set(
            selector=normalized,
            matrix=matrix_from_attmagic_record(record),
            alive_slots=alive_slots,
        )
    portable = source_sort_is_portable(targets)
    ordered = source_sorted_targets(targets) if portable else None
    return AttackMagicFootprint(
        int(magic_idx),
        int(attacker_slot),
        record_index,
        int(selector),
        normalized,
        targets,
        portable,
        ordered,
    )
