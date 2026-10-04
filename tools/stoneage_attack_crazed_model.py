"""Pinned descendant AttackCrazed reference; no historical COM1 is assigned.

This is a reference boundary, not ordered-round runtime admission. Targets are
chosen at list construction time. In the non-bow dispatch, the first attack
uses ordinary TargetAdjust on the submitted target; list element zero is not
the first executed target. Later elements are rechecked by TargetAdjust.
"""
from dataclasses import dataclass
import re
from typing import Callable, Iterable

CALLBACK_NAME = "PETSKILL_AttackCrazed"
COMMAND_NAME = "BATTLE_COM_S_ATTCRAZED"
FEATURE_NAME = "_BATTLE_ATTCRAZED"
SOURCE_PETSKILL_SYMBOL_NAME = "PETSKILL_AttCrazed"


def parse_attack_crazed_option(raw: bytes) -> int:
    """C atoi prefix semantics, gated before signed packing/buffer overflow.

The native list has 20 entries and writes a terminator at index n. A positive
count below 20 is the admitted reference domain. Non-numeric/zero/negative
and larger values stay OPEN rather than receiving invented semantics.
    """
    if not isinstance(raw, bytes) or b"\0" in raw:
        raise ValueError("OPTION must be non-NUL bytes")
    match = re.match(rb"[\t\n\v\f\r ]*([+-]?[0-9]+)", raw)
    count = int(match.group(1)) if match else 0
    if not 1 <= count <= 19:
        raise ValueError("AttackCrazed count is outside the safe 1..19 domain")
    return count


@dataclass(frozen=True)
class AttackCrazedSetup:
    command_symbol: str
    submitted_target: int
    attack_power: int
    defense_power: int
    skill_array: int
    attack_count: int


def attack_crazed_callback_setup(*, actor_kind: str, fixed_strength: int,
                                fixed_toughness: int, skill_array: int,
                                submitted_target: int, option: bytes):
    if actor_kind not in {"pet", "enemy"}:
        raise ValueError("AttackCrazed rejects PLAYER/unknown actors")
    if not 0 <= int(skill_array) <= 65535:
        raise ValueError("skill array does not fit LOW(COM3)")
    if not 0 <= int(fixed_strength) <= 2147483647 or not 0 <= int(fixed_toughness) <= 2147483647:
        raise ValueError("fixed work stats outside admitted nonnegative C int domain")
    return AttackCrazedSetup(
        COMMAND_NAME, int(submitted_target), int(int(fixed_strength) * 0.8),
        int(int(fixed_toughness) * 0.7), int(skill_array),
        parse_attack_crazed_option(option),
    )


@dataclass(frozen=True)
class AttackCrazedTargetList:
    slots: tuple[int, ...]
    candidates: tuple[int, ...]
    selection_draws: int
    reason: str


def resolve_attack_crazed_target_list(*, actor_slot: int, submitted_target: int,
                                     attack_count: int, live_slots: Iterable[int],
                                     rand_index: Callable[[int, int], int],
                                     shootchestnut_enabled: bool):
    """Model the specialized TargetListSet branch, including its off-by-one.

No-candidate returns the initial target-filled native buffer without a
terminator. Return those 20 entries explicitly; do not invent a no-action.
Same-side rejection depends on _SHOOTCHESTNUT, not on _BATTLE_ATTCRAZED.
    """
    actor = int(actor_slot); target = int(submitted_target); n = int(attack_count)
    if not 0 <= actor <= 19 or not 1 <= n <= 19:
        raise ValueError("invalid actor/count domain")
    live = {int(slot) for slot in live_slots}
    if any(not 0 <= slot <= 19 for slot in live):
        raise ValueError("live slot outside battle domain")
    initial = (target,) * 20
    if shootchestnut_enabled and 0 <= target <= 19 and actor // 10 == target // 10:
        return AttackCrazedTargetList(initial, (), 0, "same_side_command_none")
    if not 0 <= target <= 19:
        return AttackCrazedTargetList((target, -1) + initial[2:], (), 0, "invalid_target")
    start = (target // 10) * 10
    candidates = tuple(slot for slot in range(start, start + 9) if slot in live)
    if not candidates:
        return AttackCrazedTargetList(initial, (), 0, "no_candidates_initial_buffer")
    picked = []
    for _ in range(n):
        index = int(rand_index(0, len(candidates) - 1))
        if not 0 <= index < len(candidates):
            raise ValueError("selection RNG outside requested interval")
        picked.append(candidates[index])
    return AttackCrazedTargetList(tuple(picked) + (-1,) + initial[n+1:], candidates, n, "selected")
