#!/usr/bin/env python3
"""Deterministic model of the common StoneAge ExChangeMan condition/config core.

This intentionally preserves observed fixed-descendant quirks instead of
normalizing the old C implementation into a cleaner expression language.
"""

from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple


@dataclass(frozen=True)
class ItemState:
    item_id: int
    pile: int = 0
    carried: bool = True


@dataclass(frozen=True)
class PetState:
    pet_id: int
    level: int
    endevent: int = 0
    use_name: str = ""


@dataclass(frozen=True)
class ExchangeState:
    level: int = 1
    items: Tuple[ItemState, ...] = field(default_factory=tuple)
    pets: Tuple[PetState, ...] = field(default_factory=tuple)
    end_flags: frozenset[int] = field(default_factory=frozenset)
    now_flags: frozenset[int] = field(default_factory=frozenset)
    savepoint_bits: int = 0
    image: int = 0
    lstime: int = 0


def c_atoi(value: str) -> int:
    """Small atoi-compatible parser for the ASCII forms used by NPC config."""
    s = value.lstrip()
    if not s:
        return 0
    sign = 1
    if s[0] in "+-":
        sign = -1 if s[0] == "-" else 1
        s = s[1:]
    n = 0
    found = False
    for ch in s:
        if not ch.isdigit():
            break
        found = True
        n = n * 10 + ord(ch) - ord("0")
    return sign * n if found else 0


def get_arg_field(argstr: str, key: str) -> Optional[str]:
    """Mirror NPC_Util_GetStrFromStrWithDelim's substring-based key lookup."""
    for token in argstr.split("|"):
        if key in token:
            parts = token.split(":")
            if len(parts) >= 2:
                return parts[1]
    return None


def merge_arg_file_lines(lines: Iterable[str]) -> str:
    """Model NPC_Util_MargeStrFromArgFile: strip line endings and join with '|'."""
    merged = ""
    for raw in lines:
        line = raw.rstrip("\r\n")
        if merged and not merged.endswith("|"):
            merged += "|"
        merged += line
    return merged


def compare_source(point1: int, mypoint: int, flag: int) -> bool:
    """Mirror NPC_EventBigSmallLastCheck."""
    if flag == 0:
        return point1 == mypoint
    if flag == 1:
        return mypoint < point1
    if flag == 2:
        return mypoint > point1
    if flag == 3:
        return point1 != mypoint
    return False


def _operator(term: str) -> tuple[Optional[str], int]:
    if "<" in term:
        return "<", 1
    if ">" in term:
        return ">", 2
    if "!=" in term:
        return "!=", 3
    if "=" in term:
        return "=", 0
    return None, -1


def _carried_item_check(state: ExchangeState, item_no: int, flag: int) -> bool:
    for item in state.items:
        if not item.carried:
            continue
        if compare_source(item_no, item.item_id, flag):
            if flag == 0:
                return True
            continue
        if flag == 0:
            continue
        return False
    if flag == 3:
        return True
    return False


def _quantity_item_check(state: ExchangeState, item_no: int, required: int) -> bool:
    count = 0
    for item in state.items:
        if item.item_id != item_no:
            continue
        count += item.pile if item.pile else 1
        if count >= required:
            return True
    return False


def _level_check(state: ExchangeState, level: int, flag: int) -> bool:
    result = compare_source(level, state.level, flag)
    if result:
        if flag == 3:
            return False
        return True
    if flag == 3:
        return True
    return False


def _flag_check(flags: frozenset[int], shiftbit: int, flag: int, *, now: bool) -> bool:
    present = shiftbit in flags
    if now:
        if present:
            return True
        if flag == 3:
            return True
        return False
    if present:
        if flag == 3:
            return False
        return True
    if flag == 3:
        return True
    return False


def _savepoint_check(bits: int, shiftbit: int, flag: int) -> bool:
    present = (bits & (1 << shiftbit)) == (1 << shiftbit)
    if present:
        if flag == 3:
            return False
        return True
    if flag == 3:
        return True
    return False


def _pet_check(
    state: ExchangeState,
    term: str,
    required_name: Optional[str] = None,
) -> bool:
    if "-" not in term:
        return False
    level_part, pet_part = term.split("-", 1)
    if "*" in pet_part:
        pet_id_s, required_s = pet_part.split("*", 1)
        pet_id = c_atoi(pet_id_s)
        required = c_atoi(required_s)
    else:
        pet_id = c_atoi(pet_part)
        required = 1

    if required == 0:
        return True

    if "<" in level_part:
        threshold = c_atoi(level_part.split("<", 1)[1])
        flag = 1
    elif ">" in level_part:
        threshold = c_atoi(level_part.split(">", 1)[1])
        flag = 2
    elif "=" in level_part:
        threshold = c_atoi(level_part.split("=", 1)[1])
        flag = 0
    else:
        return False

    mode = 1 if "EV" in term else 0
    count = 0
    for pet in state.pets:
        if count == required:
            return True
        if pet.pet_id != pet_id or pet.endevent != mode:
            continue
        if not compare_source(threshold, pet.level, flag):
            continue
        if required_name is not None and pet.use_name != required_name:
            continue
        count += 1
    return count == required


def evaluate_term(
    term: str,
    state: ExchangeState,
    *,
    required_pet_name: Optional[str] = None,
) -> bool:
    """Evaluate one ExChangeMan EVENT term using the fixed-source behavior."""
    if "PET" in term:
        return _pet_check(state, term, required_pet_name)

    op, flag = _operator(term)
    if op is None:
        return False
    left, right = term.split(op, 1)
    value = c_atoi(right)

    if op == "=" and "*" in term:
        item_s, count_s = right.split("*", 1)
        return _quantity_item_check(state, c_atoi(item_s), c_atoi(count_s))

    if left == "LV":
        return _level_check(state, value, flag)
    if left == "ITEM":
        return _carried_item_check(state, value, flag)
    if left == "ENDEV":
        return _flag_check(state.end_flags, value, flag, now=False)
    if left == "NOWEV":
        return _flag_check(state.now_flags, value, flag, now=True)
    if left == "SP":
        return _savepoint_check(state.savepoint_bits, value, flag)
    if left == "TIME":
        return compare_source(value, state.lstime, flag)
    if left == "IMAGE":
        return compare_source(state.image, value, flag)
    return False


def evaluate_event_expression(
    expression: str,
    state: ExchangeState,
    *,
    required_pet_name: Optional[str] = None,
) -> int:
    """Return the one-based first satisfied comma branch, or -1."""
    for index, branch in enumerate(expression.split(","), start=1):
        if "&" in branch:
            terms = branch.split("&")
            if all(evaluate_term(t, state, required_pet_name=required_pet_name) for t in terms):
                return index
        elif evaluate_term(branch, state, required_pet_name=required_pet_name):
            return index
    return -1


def event_cost(arg: str, level: int) -> int:
    """Mirror NPC_EventGetCost."""
    if "LV" in arg:
        mult = arg.split("*", 1)[1] if "*" in arg else ""
        return level * c_atoi(mult)
    return c_atoi(arg)


def event_warp_step(spec: str, counter: int = 1) -> tuple[int, Optional[tuple[int, int, int]]]:
    """Mirror NPC_EventWarpNpc's NPC-local round-robin destination selector."""
    entries = spec.split(",") if spec else []
    if len(entries) + 1 <= counter:
        counter = 1
    original = counter
    pos = counter
    while 1 <= pos <= len(entries):
        entry = entries[pos - 1]
        pos += 1
        parts = entry.split(".")
        if len(parts) < 3:
            continue
        dest = (c_atoi(parts[0]), c_atoi(parts[1]), c_atoi(parts[2]))
        return pos, dest
    return original, None
