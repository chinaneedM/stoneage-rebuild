#!/usr/bin/env python3
"""Stable-descendant common enemy battle-AI decision model.

Evidence boundary:
- gavinlinasd/StoneAge@1f90cb6c gmsv/src/battle/battle_ai.c
- iriselia/StoneAge@9e6c8ce2 Source/gmsv/battle/battle_ai.c

This module reconstructs only the convergent common BATTLE_ai_normal subset.
All randomness is explicit input. The compile-gated _ENEMY_ATTACK_AI extension
(rn, leader/STR/DEX/attribute selectors), skill execution, and outer battle
state gates remain separate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ATTACK = "attack"
GUARD = "guard"
MAGIC = "magic"
ESCAPE = "escape"
SKILL = "skill"

TARGET_ALL = 1
TARGET_PLAYER = 2
TARGET_PET = 3

SELECT_RANDOM = 1
SELECT_HP_MAX = 2
SELECT_HP_MIN = 3


@dataclass(frozen=True)
class NormalEnemyAiOptions:
    attack_weight: int = 0
    target_scope: int = 0
    target_selection: int = 0
    guard_weight: int = 0
    magic_weight: int = 0
    escape_weight: int = 0
    skill_weights: tuple[int, ...] = (0, 0, 0, 0, 0, 0, 0)
    enemy_attack_ai_random_override: int | None = None

    def __post_init__(self) -> None:
        if len(self.skill_weights) != 7:
            raise ValueError("normal enemy AI requires seven skill-slot weights")
        weights = (
            self.attack_weight,
            self.guard_weight,
            self.magic_weight,
            self.escape_weight,
            *self.skill_weights,
        )
        if any(int(value) < 0 for value in weights):
            raise ValueError("enemy AI action weights cannot be negative")

    @property
    def total_weight(self) -> int:
        return sum(
            (
                int(self.attack_weight),
                int(self.guard_weight),
                int(self.magic_weight),
                int(self.escape_weight),
                *(int(value) for value in self.skill_weights),
            )
        )


@dataclass(frozen=True)
class EnemyAiTarget:
    """One opposing battle slot visible to the stable AI target scan."""

    slot: int
    participant_id: str
    kind: str
    hp: int
    alive: bool = True
    rescue_mode: bool = False

    def __post_init__(self) -> None:
        if not 0 <= int(self.slot) < 10:
            raise ValueError("enemy AI target slot must be in opposing-side 0..9")
        if self.kind not in {"player", "pet", "other"}:
            raise ValueError("enemy AI target kind must be player/pet/other")


@dataclass(frozen=True)
class EnemyAiDecision:
    kind: str
    target_slot: int | None = None
    skill_slot: int | None = None

    def __post_init__(self) -> None:
        if self.kind not in {ATTACK, GUARD, ESCAPE, SKILL}:
            raise ValueError(f"unsupported common enemy AI decision: {self.kind}")
        if self.kind in {ATTACK, SKILL}:
            if self.target_slot is None:
                raise ValueError(f"{self.kind} requires a target slot")
        elif self.target_slot is not None:
            raise ValueError(f"{self.kind} does not carry a target slot")
        if self.kind == SKILL:
            if self.skill_slot is None or not 0 <= int(self.skill_slot) < 7:
                raise ValueError("skill decision requires skill slot 0..6")
        elif self.skill_slot is not None:
            raise ValueError(f"{self.kind} does not carry a skill slot")


def _c_atoi(text: str) -> int:
    text = str(text).lstrip()
    if not text:
        return 0
    sign = 1
    if text[0] in "+-":
        if text[0] == "-":
            sign = -1
        text = text[1:]
    digits = []
    for char in text:
        if not char.isdigit():
            break
        digits.append(char)
    return sign * int("".join(digits), 10) if digits else 0


def _option_payload(option_text: str, search: str) -> str | None:
    """Mirror NPC_Util_GetStrFromStrWithDelim's first substring match."""
    for token in str(option_text).split("|"):
        if search not in token:
            continue
        parts = token.split(":")
        if len(parts) >= 2:
            return parts[1]
    return None


def _required_values(
    option_text: str,
    tag: str,
    count: int,
) -> tuple[int, ...] | None:
    payload = _option_payload(option_text, tag)
    if payload is None:
        return None
    parts = payload.split(";")
    if len(parts) < count:
        raise ValueError(
            f"enemy AI option {tag!r} lacks required suboptions: "
            f"expected {count}, got {len(parts)}"
        )
    return tuple(_c_atoi(parts[index]) for index in range(count))


def parse_normal_enemy_ai_options(option_text: str) -> NormalEnemyAiOptions:
    """Parse the common fixed-descendant BATTLE_ai_normal profile."""
    attack = _required_values(option_text, "at", 3)
    guard = _required_values(option_text, "gu", 1)
    magic = _required_values(option_text, "ma", 1)
    escape = _required_values(option_text, "es", 1)

    wa_payload = _option_payload(option_text, "wa")
    wa_values = [0] * 7
    if wa_payload is not None:
        parts = wa_payload.split(";")
        for index in range(min(7, len(parts))):
            wa_values[index] = _c_atoi(parts[index])

    rn = _required_values(option_text, "rn", 1)
    return NormalEnemyAiOptions(
        attack_weight=0 if attack is None else attack[0],
        target_scope=0 if attack is None else attack[1],
        target_selection=0 if attack is None else attack[2],
        guard_weight=0 if guard is None else guard[0],
        magic_weight=0 if magic is None else magic[0],
        escape_weight=0 if escape is None else escape[0],
        skill_weights=tuple(wa_values),
        enemy_attack_ai_random_override=None if rn is None else rn[0],
    )


def _weighted_mode(
    options: NormalEnemyAiOptions,
    *,
    mode_roll: int,
) -> tuple[str, int | None] | None:
    total = options.total_weight
    if total <= 0:
        return None
    mode_roll = int(mode_roll)
    if not 0 <= mode_roll < total:
        raise ValueError(f"mode_roll must be in 0..{total - 1}")

    cursor = 0
    ordered = (
        (ATTACK, None, int(options.attack_weight)),
        (GUARD, None, int(options.guard_weight)),
        (MAGIC, None, int(options.magic_weight)),
        (ESCAPE, None, int(options.escape_weight)),
        *(
            (SKILL, index, int(weight))
            for index, weight in enumerate(options.skill_weights)
        ),
    )
    for kind, skill_slot, weight in ordered:
        cursor += weight
        if weight > 0 and mode_roll < cursor:
            return kind, skill_slot
    raise AssertionError("enemy AI weighted mode selection fell through")


def _target_candidates(
    targets: Iterable[EnemyAiTarget],
    *,
    scope: int,
) -> tuple[EnemyAiTarget, ...]:
    usable = tuple(
        sorted(
            (
                target
                for target in targets
                if bool(target.alive) and not bool(target.rescue_mode)
            ),
            key=lambda target: int(target.slot),
        )
    )

    def apply(current_scope: int) -> tuple[EnemyAiTarget, ...]:
        if current_scope == TARGET_PLAYER:
            return tuple(target for target in usable if target.kind == "player")
        if current_scope == TARGET_PET:
            return tuple(target for target in usable if target.kind == "pet")
        return usable

    candidates = apply(int(scope))
    if candidates:
        return candidates
    if int(scope) == TARGET_ALL:
        return ()
    return apply(TARGET_ALL)


def _select_target(
    options: NormalEnemyAiOptions,
    targets: Iterable[EnemyAiTarget],
    *,
    target_roll: int | None,
) -> int | None:
    candidates = _target_candidates(targets, scope=int(options.target_scope))
    if not candidates:
        return None

    selector = int(options.target_selection)
    if selector == SELECT_RANDOM:
        if target_roll is None:
            raise ValueError("random enemy AI target selection requires target_roll")
        target_roll = int(target_roll)
        if not 0 <= target_roll < len(candidates):
            raise ValueError(
                f"target_roll must be in 0..{len(candidates) - 1}"
            )
        return int(candidates[target_roll].slot)

    if selector == SELECT_HP_MAX:
        best = candidates[0]
        for target in candidates[1:]:
            if int(target.hp) > int(best.hp):
                best = target
        return int(best.slot)

    if selector == SELECT_HP_MIN:
        best = candidates[0]
        for target in candidates[1:]:
            if int(target.hp) < int(best.hp):
                best = target
        return int(best.slot)

    return None


def resolve_common_normal_enemy_ai(
    option_text: str,
    targets: Iterable[EnemyAiTarget],
    *,
    mode_roll: int,
    target_roll: int | None = None,
) -> EnemyAiDecision | None:
    """Resolve one common normal-AI decision using only explicit RNG.

    Returns None where the fixed source's normal selector returns FALSE, such
    as no configured action, invalid target selection, no legal target, or a
    selected ma mode (which has no terminal result branch in the inspected
    common function).

    Profiles carrying the compile-gated rn extension fail closed because
    recovered25 build-flag provenance is not yet established.
    """
    options = parse_normal_enemy_ai_options(option_text)
    if options.enemy_attack_ai_random_override is not None:
        raise ValueError(
            "enemy AI profile requires unresolved _ENEMY_ATTACK_AI extension"
        )

    selected = _weighted_mode(options, mode_roll=int(mode_roll))
    if selected is None:
        return None
    kind, skill_slot = selected

    if kind == GUARD:
        return EnemyAiDecision(GUARD)
    if kind == ESCAPE:
        return EnemyAiDecision(ESCAPE)
    if kind == MAGIC:
        return None

    target_slot = _select_target(
        options,
        targets,
        target_roll=target_roll,
    )
    if target_slot is None:
        return None
    if kind == ATTACK:
        return EnemyAiDecision(ATTACK, target_slot=target_slot)
    if kind == SKILL:
        return EnemyAiDecision(
            SKILL,
            target_slot=target_slot,
            skill_slot=int(skill_slot),
        )
    raise AssertionError(f"unhandled common enemy AI mode: {kind}")
