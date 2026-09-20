#!/usr/bin/env python3
"""Deterministic stable-descendant enemy spawn/birth orchestration.

This reconstructs the fixed ENEMY_getEnemy composition boundary after an
encounter group has been selected. It intentionally keeps all random outcomes
explicit and preserves the observed fact that CREATEMINNUM is loaded but not
enforced by this core generation path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from tools.stoneage_singleplayer_battle import (
    BattleParticipant,
    enemy_participant_from_spawn_state,
)
from tools.stoneage_tw10_25_bridge_model import (
    PetBirthBridgeState,
    PetTemplateBridge,
    build_pet_birth_bridge,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


SIZE_NORMAL = 0
SIZE_BIG = 1
SOURCE_LOOP_LIMIT = 100


@dataclass(frozen=True)
class EnemyBirthRolls:
    level_roll: int
    birth_offsets: tuple[int, int, int, int]
    spawn_allocation_rolls: tuple[int, ...]

    def __post_init__(self) -> None:
        offsets = tuple(int(x) for x in self.birth_offsets)
        allocations = tuple(int(x) for x in self.spawn_allocation_rolls)
        if len(offsets) != 4 or any(x < -2 or x > 2 for x in offsets):
            raise ValueError("birth_offsets must contain four values in -2..2")
        if len(allocations) != 10 or any(x < 0 or x > 3 for x in allocations):
            raise ValueError(
                "spawn_allocation_rolls must contain ten values in 0..3"
            )
        object.__setattr__(self, "level_roll", int(self.level_roll))
        object.__setattr__(self, "birth_offsets", offsets)
        object.__setattr__(self, "spawn_allocation_rolls", allocations)


@dataclass(frozen=True)
class EnemySpawnPlan:
    group_id: int
    initial_target_count: int
    final_target_count: int
    variants: tuple[EnemyVariantBridge, ...]
    selection_attempts: int
    loop_limit_reached: bool
    create_min_enforced: bool = False

    @property
    def actual_count(self) -> int:
        return len(self.variants)


@dataclass(frozen=True)
class SpawnedEnemy:
    spawn_index: int
    variant: EnemyVariantBridge
    template: PetTemplateBridge
    birth: PetBirthBridgeState
    participant: BattleParticipant


def _resolved_group_slots(
    group: GroupBridge,
    enemies: Mapping[int, EnemyVariantBridge],
) -> tuple[tuple[EnemyVariantBridge, int], ...]:
    slots = []
    for enemy_id, weight in group.enemy_slots:
        if enemy_id == -1:
            continue
        if enemy_id not in enemies:
            raise KeyError(
                f"group {group.group_id} references unresolved enemy ID {enemy_id}"
            )
        slots.append((enemies[enemy_id], int(weight)))
    if not slots:
        raise ValueError(f"group {group.group_id} has no enemy slots")
    if sum(max(0, weight) for _, weight in slots) <= 0:
        raise ValueError(f"group {group.group_id} has no positive CREATEPROB")
    return tuple(slots)


def _weighted_slot(
    slots: Sequence[tuple[EnemyVariantBridge, int]],
    roll: int,
) -> EnemyVariantBridge:
    total = sum(max(0, int(weight)) for _, weight in slots)
    roll = int(roll)
    if not 0 <= roll < total:
        raise ValueError(f"selection roll must be in 0..{total - 1}")
    cumulative = 0
    for variant, weight in slots:
        weight = max(0, int(weight))
        cumulative += weight
        if weight > 0 and roll < cumulative:
            return variant
    raise AssertionError("weighted enemy slot selection fell through")


def _template_for_variant(
    variant: EnemyVariantBridge,
    templates: Mapping[int, PetTemplateBridge],
) -> PetTemplateBridge:
    if variant.tempno not in templates:
        raise KeyError(
            f"enemy ID {variant.enemy_id} references unresolved TEMPNO {variant.tempno}"
        )
    template = templates[variant.tempno]
    if template.tempno != variant.tempno:
        raise ValueError(
            f"template key/identity mismatch for TEMPNO {variant.tempno}"
        )
    if template.size_class is None:
        raise ValueError(
            f"enemybase TEMPNO {template.tempno} lacks SIZE for spawn layout"
        )
    if template.size_class not in (SIZE_NORMAL, SIZE_BIG):
        raise ValueError(
            f"enemybase TEMPNO {template.tempno} has unsupported SIZE "
            f"{template.size_class}"
        )
    return template


def effective_spawn_capacity(
    area: EncounterAreaBridge,
    group: GroupBridge,
    enemies: Mapping[int, EnemyVariantBridge],
) -> int:
    """Area ENEMY_MAX_NUM capped by the sum of per-slot CREATEMAXNUM.

    Duplicate group slots intentionally contribute capacity repeatedly, exactly
    as the fixed source later multiplies the selected variant limit by the
    number of equal slots.
    """
    slots = _resolved_group_slots(group, enemies)
    declared = 0
    for variant, _ in slots:
        if variant.create_max < 0:
            raise ValueError(
                f"enemy ID {variant.enemy_id} has negative CREATEMAXNUM"
            )
        declared += variant.create_max
    return min(int(area.enemy_max_num), declared)


def plan_enemy_spawns(
    area: EncounterAreaBridge,
    group: GroupBridge,
    enemies: Mapping[int, EnemyVariantBridge],
    templates: Mapping[int, PetTemplateBridge],
    *,
    entry_count_roll: int,
    selection_rolls: Sequence[int],
) -> EnemySpawnPlan:
    """Reproduce the fixed ENEMY_getEnemy count/selection loop.

    entry_count_roll is the explicit result of RAND(1, effective_capacity).
    selection_rolls are explicit RAND(0, sum(CREATEPROB)-1) results and include
    rolls consumed by rejected capacity/size attempts.
    """
    slots = _resolved_group_slots(group, enemies)
    capacity = effective_spawn_capacity(area, group, enemies)
    if capacity < 1:
        raise ValueError("encounter has no spawn capacity")

    initial_target = int(entry_count_roll)
    if not 1 <= initial_target <= capacity:
        raise ValueError(
            f"entry_count_roll must be in 1..{capacity}"
        )

    # Resolve all template size classes up front. This prevents the modern
    # reconstruction from silently treating an unknown historical SIZE as normal.
    template_by_enemy = {
        variant.enemy_id: _template_for_variant(variant, templates)
        for variant, _ in slots
    }

    selected: list[EnemyVariantBridge] = []
    big_count = 0
    target = initial_target
    attempts = 0
    rolls = tuple(int(x) for x in selection_rolls)

    for roll in rolls:
        if len(selected) >= target or attempts >= SOURCE_LOOP_LIMIT:
            break
        attempts += 1
        variant = _weighted_slot(slots, roll)

        duplicate_slot_count = sum(
            1 for candidate, _ in slots
            if candidate.enemy_id == variant.enemy_id
        )
        current_count = sum(
            1 for candidate in selected
            if candidate.enemy_id == variant.enemy_id
        )
        max_for_variant = int(variant.create_max) * duplicate_slot_count
        if current_count >= max_for_variant:
            continue

        template = template_by_enemy[variant.enemy_id]
        if template.size_class == SIZE_BIG:
            if big_count >= 5:
                target -= 1
                continue

            if len(selected) > 4:
                normal_index = None
                for index in range(5):
                    prior = selected[index]
                    prior_template = template_by_enemy[prior.enemy_id]
                    if prior_template.size_class == SIZE_NORMAL:
                        normal_index = index
                        break
                if normal_index is None:
                    continue
                displaced = selected[normal_index]
                selected[normal_index] = variant
                selected.append(displaced)
            else:
                selected.append(variant)
            big_count += 1
        else:
            selected.append(variant)

    loop_limit_reached = attempts >= SOURCE_LOOP_LIMIT and len(selected) < target
    if len(selected) < target and not loop_limit_reached:
        raise ValueError(
            "selection_rolls exhausted before source spawn loop terminated"
        )

    return EnemySpawnPlan(
        group_id=group.group_id,
        initial_target_count=initial_target,
        final_target_count=target,
        variants=tuple(selected),
        selection_attempts=attempts,
        loop_limit_reached=loop_limit_reached,
        create_min_enforced=False,
    )


def materialize_spawn_plan(
    plan: EnemySpawnPlan,
    templates: Mapping[int, PetTemplateBridge],
    *,
    birth_rolls: Sequence[EnemyBirthRolls],
) -> tuple[SpawnedEnemy, ...]:
    if len(birth_rolls) != len(plan.variants):
        raise ValueError(
            "birth_rolls count must equal planned enemy count"
        )

    spawned = []
    for index, (variant, rolls) in enumerate(zip(plan.variants, birth_rolls)):
        template = _template_for_variant(variant, templates)
        level = variant.choose_level(rolls.level_roll)
        birth = build_pet_birth_bridge(
            template,
            level=level,
            birth_offsets=rolls.birth_offsets,
            spawn_allocation_rolls=rolls.spawn_allocation_rolls,
        )
        participant = enemy_participant_from_spawn_state(
            variant,
            template,
            birth,
            spawn_index=index,
        )
        spawned.append(
            SpawnedEnemy(
                spawn_index=index,
                variant=variant,
                template=template,
                birth=birth,
                participant=participant,
            )
        )
    return tuple(spawned)
