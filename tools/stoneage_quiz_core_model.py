#!/usr/bin/env python3
"""Deterministic reference model for the fixed-descendant StoneAge Quiz NPC."""

from dataclasses import dataclass

MEPLAYER = 8
OLDNO = 100


@dataclass(frozen=True)
class QuestionMeta:
    q_type: int
    level: int
    answer_type: int
    answer_no: int


def normalized_mask(value):
    value = int(value)
    return 0xFFFF if value <= 0 else value


def question_matches(question, *, type_mask=0, answer_mask=0, level_mask=0):
    """Match the fixed NPC_GetQuestion bit-mask filters."""
    type_mask = normalized_mask(type_mask)
    answer_mask = normalized_mask(answer_mask)
    level_mask = normalized_mask(level_mask)

    type_bit = 1 << (int(question.q_type) - 1)
    return (
        (type_mask & type_bit) == type_bit
        and (answer_mask & int(question.answer_type)) == int(question.answer_type)
        and (level_mask & int(question.level)) == int(question.level)
    )


def question_row_status(field_count, answer_type, answer_no):
    """Model the loader's nine-field requirement and hard semantic rejects."""
    if int(field_count) < 9:
        return "skip_short_row"
    if int(answer_type) == 1 and int(answer_no) == 3:
        return "fatal_two_choice_answer_3"
    if int(answer_type) == 4 and int(answer_no) != 1:
        return "fatal_free_text_answer_not_1"
    return "loaded"


def threshold_value(score, pairs):
    """Return the first configured value whose threshold is met.

    The source scans pairs in configuration order; it does not sort thresholds.
    """
    score = int(score)
    for threshold, value in pairs:
        if score >= int(threshold):
            return value
    return None


def free_text_correct(submitted_text, configured_answer):
    """Fixed source accepts a free-text response when answer text is a substring."""
    return str(configured_answer) in str(submitted_text)


def choice_correct(submitted_value, displayed_answer_index):
    """A zero/invalid numeric selection is ignored by the fixed callback."""
    try:
        value = int(submitted_value)
    except (TypeError, ValueError):
        value = 0
    if value == 0:
        return None
    return value == int(displayed_answer_index)


def party_gate(in_party):
    """Party membership is warned about but does not stop Quiz progression."""
    return "warn_and_continue" if bool(in_party) else "continue"


def parse_requirements(requirements):
    """Requirements are abstract (item_token, count-or-None) pairs."""
    out = []
    for item, count in requirements:
        out.append((item, None if count is None else int(count)))
    return out


def item_requirements_satisfied(inventory, requirements):
    """Validation rechecks the original inventory for every token."""
    inv = list(inventory)
    for item, count in parse_requirements(requirements):
        have = sum(1 for x in inv if x == item)
        need = 1 if count is None else count
        if have < need:
            return False
    return True


def delete_entry_items(inventory, requirements):
    """Model Quiz/Janken deletion quirks after a successful validation pass.

    Plain tokens delete every matching copy. Starred tokens delete up to count.
    Duplicate tokens are processed sequentially and can therefore under-delete
    relative to the earlier validation, while still reporting success.
    """
    inv = list(inventory)
    for item, count in parse_requirements(requirements):
        if count is None:
            inv = [x for x in inv if x != item]
            continue

        remaining = count
        kept = []
        for x in inv:
            if x == item and remaining > 0:
                remaining -= 1
            else:
                kept.append(x)
        inv = kept
    return inv


def item_full_gate(*, has_empty_item_slot, inventory, entry_requirements):
    """Full inventory is accepted only if configured entry items are present.

    The source assumes consuming EntryItem will free reward capacity.
    """
    if bool(has_empty_item_slot):
        return True
    requirements = parse_requirements(entry_requirements)
    if not requirements:
        return False
    return item_requirements_satisfied(inventory, requirements)


def entry_stone_check(gold, cost):
    return int(cost) <= int(gold)


def delete_entry_stone(gold, cost):
    """Literal source mutation; negative cost therefore increases Gold."""
    gold = int(gold)
    cost = int(cost)
    if gold - cost < 0:
        return 0
    return gold - cost


def can_allocate_player_slot(active_slots):
    return int(active_slots) < MEPLAYER


def can_record_question_history(answered_count):
    """The fixed oldno array has 100 entries and no protective bounds check."""
    return int(answered_count) < OLDNO


def persistence_boundary():
    """Quiz mutates ordinary character state but does not synchronously save it."""
    return "deferred_standard_character_save"
