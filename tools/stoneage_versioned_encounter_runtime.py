#!/usr/bin/env python3
"""Versioned encounter-runtime adapter for provenance-safe world content.

This adapter joins the later recovered encounter master-data bridge to the
already versioned world geometry. It does not reinterpret recovered-2.5 rows as
Taiwan-v1 facts and it does not repair specimen defects.

The existing strict encounter resolver remains authoritative. Positive-weight
references to missing groups are recorded here and still raise KeyError when a
runtime request reaches an affected encounter area.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_singleplayer_domain import HistoricalStaticData
from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)
from tools.stoneage_versioned_world_geometry import (
    VersionedEncounterAreaGeometry,
    VersionedWorldGeometryManifest,
)


SEMANTIC_SOURCE_VERSION = "recovered25"


@dataclass(frozen=True)
class UnresolvedPositiveGroupReference:
    area_index: int
    floor_id: int
    group_id: int
    weight: int
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        for name in ("area_index", "floor_id", "group_id", "weight"):
            object.__setattr__(self, name, int(getattr(self, name)))
        if self.weight <= 0:
            raise ValueError("unresolved group defect must have positive weight")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered encounter defect must remain LATER_RECOVERED"
            )


@dataclass(frozen=True)
class VersionedEncounterRuntimeAdapter:
    """Validated recovered-later encounter data for the stable world subset."""

    world_geometry: VersionedWorldGeometryManifest
    encounter_areas: tuple[EncounterAreaBridge, ...]
    groups: Mapping[int, GroupBridge]
    enemies: Mapping[int, EnemyVariantBridge]
    unresolved_positive_group_refs: tuple[
        UnresolvedPositiveGroupReference, ...
    ]
    source_version: str = SEMANTIC_SOURCE_VERSION

    def __post_init__(self) -> None:
        areas = tuple(self.encounter_areas)
        groups = {int(key): value for key, value in self.groups.items()}
        enemies = {int(key): value for key, value in self.enemies.items()}
        defects = tuple(self.unresolved_positive_group_refs)

        if self.source_version != self.world_geometry.source_version:
            raise ValueError("encounter adapter source-version drift")

        by_index: dict[int, EncounterAreaBridge] = {}
        for area in areas:
            if area.index in by_index:
                raise ValueError(
                    f"duplicate runtime encounter area index {area.index}"
                )
            by_index[area.index] = area

        geometry_by_index: dict[int, VersionedEncounterAreaGeometry] = {}
        for geometry in self.world_geometry.encounters:
            if geometry.index in geometry_by_index:
                raise ValueError(
                    f"duplicate versioned encounter geometry index {geometry.index}"
                )
            geometry_by_index[geometry.index] = geometry

        if set(by_index) != set(geometry_by_index):
            missing = sorted(set(geometry_by_index) - set(by_index))
            extra = sorted(set(by_index) - set(geometry_by_index))
            raise ValueError(
                "runtime encounter areas do not match versioned geometry; "
                f"missing={missing}, extra={extra}"
            )

        actual_defects: list[UnresolvedPositiveGroupReference] = []
        for index in sorted(geometry_by_index):
            geometry = geometry_by_index[index]
            area = by_index[index]
            _validate_area_matches_geometry(area, geometry)

            positive_group_slots = tuple(
                (int(group_id), int(weight))
                for group_id, weight in area.group_slots
                if int(group_id) >= 0 and int(weight) > 0
            )
            if len(positive_group_slots) != geometry.positive_group_ref_count:
                raise ValueError(
                    f"encounter {index} positive group-ref count drift"
                )
            for group_id, weight in positive_group_slots:
                if group_id not in groups:
                    actual_defects.append(
                        UnresolvedPositiveGroupReference(
                            area_index=area.index,
                            floor_id=area.floor,
                            group_id=group_id,
                            weight=weight,
                        )
                    )

        actual_key = tuple(
            (d.area_index, d.floor_id, d.group_id, d.weight)
            for d in actual_defects
        )
        supplied_key = tuple(
            (d.area_index, d.floor_id, d.group_id, d.weight)
            for d in defects
        )
        if actual_key != supplied_key:
            raise ValueError(
                "supplied unresolved-group defect inventory does not match "
                "the strict recovered encounter/group join"
            )

        for key, group in groups.items():
            if key != group.group_id:
                raise ValueError(
                    f"group mapping key {key} != GROUP_ID {group.group_id}"
                )
        for key, enemy in enemies.items():
            if key != enemy.enemy_id:
                raise ValueError(
                    f"enemy mapping key {key} != enemy.ID {enemy.enemy_id}"
                )

        object.__setattr__(self, "encounter_areas", areas)
        object.__setattr__(self, "groups", MappingProxyType(groups))
        object.__setattr__(self, "enemies", MappingProxyType(enemies))
        object.__setattr__(
            self, "unresolved_positive_group_refs", defects
        )

    @property
    def specimen_defect_area_indices(self) -> tuple[int, ...]:
        return tuple(
            sorted({defect.area_index for defect in self.unresolved_positive_group_refs})
        )

    @property
    def static_data(self) -> HistoricalStaticData:
        """Return the already-versioned stable-world subset for existing resolver."""
        return HistoricalStaticData(
            encounter_areas=self.encounter_areas,
            encounter_groups=self.groups,
            enemy_variants=self.enemies,
        )


def _validate_area_matches_geometry(
    area: EncounterAreaBridge,
    geometry: VersionedEncounterAreaGeometry,
) -> None:
    actual = (
        int(area.floor),
        int(area.min_x),
        int(area.min_y),
        int(area.max_x),
        int(area.max_y),
        int(area.probability_min),
        int(area.probability_max),
        int(area.enemy_max_num),
        int(area.zorder),
    )
    expected = (
        int(geometry.floor_id),
        int(geometry.rect[0]),
        int(geometry.rect[1]),
        int(geometry.rect[2]),
        int(geometry.rect[3]),
        int(geometry.probability_min),
        int(geometry.probability_max),
        int(geometry.enemy_max_num),
        int(geometry.zorder),
    )
    if actual != expected:
        raise ValueError(
            f"encounter area {area.index} geometry/master-data drift; "
            f"actual={actual}, expected={expected}"
        )


def build_versioned_encounter_runtime_adapter(
    *,
    world_geometry: VersionedWorldGeometryManifest,
    all_encounter_areas: Sequence[EncounterAreaBridge],
    groups: Mapping[int, GroupBridge],
    enemies: Mapping[int, EnemyVariantBridge],
) -> VersionedEncounterRuntimeAdapter:
    """Filter full recovered source to the stable-world geometry subset.

    Missing positive group references are retained as defects. Nothing is
    synthesized, removed from the area, or assigned a replacement weight.
    """
    geometry_indices = {
        geometry.index for geometry in world_geometry.encounters
    }
    selected = tuple(
        area for area in all_encounter_areas
        if area.index in geometry_indices
    )

    defects: list[UnresolvedPositiveGroupReference] = []
    normalized_groups = {int(key): value for key, value in groups.items()}
    for area in selected:
        for group_id, weight in area.group_slots:
            group_id = int(group_id)
            weight = int(weight)
            if group_id >= 0 and weight > 0 and group_id not in normalized_groups:
                defects.append(
                    UnresolvedPositiveGroupReference(
                        area_index=area.index,
                        floor_id=area.floor,
                        group_id=group_id,
                        weight=weight,
                    )
                )

    defects.sort(
        key=lambda d: (d.area_index, d.group_id, d.weight, d.floor_id)
    )
    return VersionedEncounterRuntimeAdapter(
        world_geometry=world_geometry,
        encounter_areas=tuple(sorted(selected, key=lambda area: area.index)),
        groups=groups,
        enemies=enemies,
        unresolved_positive_group_refs=tuple(defects),
    )
