#!/usr/bin/env python3
"""Strict reconstruction bridge for the recovered 2.5 encounter data chain.

This models the descendant server-side chain:
floor/coordinate -> encount -> group -> enemy variant -> enemybase template.

It is a bridge/validation layer, not Taiwan v1.0 server provenance. Unlike the
old C runtime, unresolved positive references raise explicit errors instead of
allowing negative array indexing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from tools.stoneage_tw10_gameplay_model import TemplateRef


def _int(row: Mapping[str, Any], key: str, default: int | None = None) -> int:
    if key not in row:
        if default is None:
            raise KeyError(f"missing encounter source field: {key}")
        return int(default)
    value = row[key]
    if value is None or value == "":
        if default is None:
            raise ValueError(f"empty encounter source field: {key}")
        return int(default)
    return int(value)


def _slots(
    row: Mapping[str, Any],
    id_prefix: str,
    weight_prefix: str,
    count: int = 10,
) -> tuple[tuple[int, int], ...]:
    out = []
    for n in range(1, count + 1):
        identity = _int(row, f"{id_prefix}{n}", -1)
        weight = _int(row, f"{weight_prefix}{n}", -1)
        out.append((identity, weight))
    return tuple(out)


def weighted_choice(entries: Sequence[tuple[Any, int]], roll: int) -> Any:
    """Choose by the old cumulative positive-weight convention.

    The roll is explicit to keep reconstruction tests deterministic.
    """
    usable = [(value, int(weight)) for value, weight in entries if int(weight) > 0]
    total = sum(weight for _, weight in usable)
    if total <= 0:
        raise ValueError("weighted choice has no positive weights")
    roll = int(roll)
    if not 0 <= roll < total:
        raise ValueError(f"roll must be in 0..{total - 1}")
    cumulative = 0
    for value, weight in usable:
        cumulative += weight
        if roll < cumulative:
            return value
    raise AssertionError("weighted choice fell through")


@dataclass(frozen=True)
class EnemyVariantBridge:
    enemy_id: int
    tempno: int
    level_min: int
    level_max: int
    create_max: int
    create_min_declared: int
    tactics: int
    exp_override: int
    duel_point: int
    style: int
    capturable: bool

    @classmethod
    def from_enemy(cls, row: Mapping[str, Any]) -> "EnemyVariantBridge":
        lv_min = _int(row, "LV_MIN")
        lv_max = _int(row, "LV_MAX")
        if lv_min == 0:
            lv_min = lv_max
        lo, hi = min(lv_min, lv_max), max(lv_min, lv_max)
        return cls(
            enemy_id=_int(row, "ID"),
            tempno=_int(row, "TEMPNO"),
            level_min=lo,
            level_max=hi,
            create_max=_int(row, "CREATEMAXNUM"),
            create_min_declared=_int(row, "CREATEMINNUM"),
            tactics=_int(row, "TACTICS"),
            exp_override=_int(row, "EXP"),
            duel_point=_int(row, "DUELPOINT"),
            style=_int(row, "STYLE"),
            capturable=bool(_int(row, "PETFLG")),
        )

    @property
    def variant_ref(self) -> TemplateRef:
        return TemplateRef("enemy.ID", self.enemy_id)

    @property
    def pet_template_ref(self) -> TemplateRef:
        return TemplateRef("enemybase.TEMPNO", self.tempno)

    def choose_level(self, level_roll: int) -> int:
        level_roll = int(level_roll)
        width = self.level_max - self.level_min + 1
        if not 0 <= level_roll < width:
            raise ValueError(f"level_roll must be in 0..{width - 1}")
        return self.level_min + level_roll


@dataclass(frozen=True)
class GroupBridge:
    group_id: int
    appear_by_item_id: int
    not_appear_by_item_id: int
    enemy_slots: tuple[tuple[int, int], ...]

    @classmethod
    def from_group(cls, row: Mapping[str, Any]) -> "GroupBridge":
        return cls(
            group_id=_int(row, "GROUP_ID"),
            appear_by_item_id=_int(row, "APPEAR_BY_ITEM_ID", -1),
            not_appear_by_item_id=_int(row, "NOT_APPEAR_BY_ITEM_ID", -1),
            enemy_slots=_slots(row, "ENEMY_ID", "CREATEPROB"),
        )

    def is_eligible(self, inventory_template_ids: Iterable[int]) -> bool:
        inventory = {int(x) for x in inventory_template_ids}
        if self.appear_by_item_id != -1 and self.appear_by_item_id not in inventory:
            return False
        if (
            self.not_appear_by_item_id != -1
            and self.not_appear_by_item_id in inventory
        ):
            return False
        return True

    def resolved_enemy_choices(
        self,
        enemies: Mapping[int, EnemyVariantBridge],
    ) -> tuple[tuple[EnemyVariantBridge, int], ...]:
        result = []
        seen: set[int] = set()
        for enemy_id, weight in self.enemy_slots:
            if enemy_id == -1:
                continue
            if enemy_id in seen:
                raise ValueError(f"group {self.group_id} duplicates enemy ID {enemy_id}")
            seen.add(enemy_id)
            if enemy_id not in enemies:
                raise KeyError(
                    f"group {self.group_id} references unresolved enemy ID {enemy_id}"
                )
            result.append((enemies[enemy_id], weight))
        if not result:
            raise ValueError(f"group {self.group_id} has no resolved enemies")
        return tuple(result)


@dataclass(frozen=True)
class EncounterAreaBridge:
    index: int
    floor: int
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    probability_min: int
    probability_max: int
    enemy_max_num: int
    zorder: int
    group_slots: tuple[tuple[int, int], ...]

    @classmethod
    def from_encount(cls, row: Mapping[str, Any]) -> "EncounterAreaBridge":
        x1, x2 = _int(row, "X1"), _int(row, "X2")
        y1, y2 = _int(row, "Y1"), _int(row, "Y2")
        p1, p2 = _int(row, "ENCOUNT_PROB_MIN"), _int(row, "ENCOUNT_PROB_MAX")
        enemy_max = _int(row, "ENEMY_MAX_NUM")
        if not 1 <= enemy_max <= 10:
            raise ValueError("ENEMY_MAX_NUM must be in 1..10")
        return cls(
            index=_int(row, "INDEX"),
            floor=_int(row, "FLOOR"),
            min_x=min(x1, x2),
            min_y=min(y1, y2),
            max_x=max(x1, x2),
            max_y=max(y1, y2),
            probability_min=min(p1, p2),
            probability_max=max(p1, p2),
            enemy_max_num=enemy_max,
            zorder=_int(row, "ZORDER"),
            group_slots=_slots(row, "GROUP_ID", "GROUP_PROB"),
        )

    def contains(self, floor: int, x: int, y: int) -> bool:
        return (
            self.zorder > 0
            and self.floor == int(floor)
            and self.min_x <= int(x) <= self.max_x
            and self.min_y <= int(y) <= self.max_y
        )

    def resolved_group_choices(
        self,
        groups: Mapping[int, GroupBridge],
        inventory_template_ids: Iterable[int],
    ) -> tuple[tuple[GroupBridge, int], ...]:
        result = []
        for group_id, weight in self.group_slots:
            if group_id == -1:
                continue
            if group_id not in groups:
                if weight > 0:
                    raise KeyError(
                        f"encount {self.index} has positive weight for unresolved group {group_id}"
                    )
                continue
            group = groups[group_id]
            if group.is_eligible(inventory_template_ids):
                result.append((group, weight))
        return tuple(result)


def active_encounter_area(
    areas: Iterable[EncounterAreaBridge],
    *,
    floor: int,
    x: int,
    y: int,
) -> EncounterAreaBridge | None:
    matches = [area for area in areas if area.contains(floor, x, y)]
    if not matches:
        return None
    return max(matches, key=lambda area: area.zorder)


def choose_group(
    area: EncounterAreaBridge,
    groups: Mapping[int, GroupBridge],
    *,
    inventory_template_ids: Iterable[int] = (),
    roll: int,
) -> GroupBridge:
    choices = area.resolved_group_choices(groups, inventory_template_ids)
    return weighted_choice(choices, roll)


def choose_enemy(
    group: GroupBridge,
    enemies: Mapping[int, EnemyVariantBridge],
    *,
    roll: int,
) -> EnemyVariantBridge:
    return weighted_choice(group.resolved_enemy_choices(enemies), roll)


def effective_enemy_count_limit(
    area: EncounterAreaBridge,
    choices: Sequence[EnemyVariantBridge],
) -> int:
    """Historical upper bound before random target-count selection."""
    possible = sum(max(0, int(enemy.create_max)) for enemy in choices)
    return min(area.enemy_max_num, possible)
