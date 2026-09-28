#!/usr/bin/env python3
"""Engine-neutral versioned NPC spawn catalogue.

This promotes recovered create-block placement geometry into a runtime-facing
catalogue without importing NPC names, template behavior, dialogue, arguments,
or functionset semantics.

The catalogue preserves recovered25/LATER_RECOVERED provenance. It records
create-layer spawn controls only:
- placement identity and floor;
- inclusive birth and movement rectangles;
- simultaneous population cap (createnum);
- raw direction plus the descendant VALIDATEDIR modulo-8 projection;
- respawn delay in milliseconds;
- boundary and invincible-area spawn controls.

No row is promoted to Taiwan-v1 historical membership.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_versioned_world_geometry import (
    VersionedNpcPlacementGeometry,
    VersionedWorldGeometryManifest,
)


SEMANTIC_SOURCE_VERSION = "recovered25"

ISSUE_BIRTH_OUTSIDE_STABLE_MAP = "BIRTH_OUTSIDE_STABLE_MAP"
ISSUE_NON_OCTANT_RAW_DIRECTION = "NON_OCTANT_RAW_DIRECTION"
ISSUE_GENERATION_DISABLED = "GENERATION_DISABLED"


def _normalized_rect(
    rect: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    values = tuple(int(value) for value in rect)
    if len(values) != 4:
        raise ValueError("NPC spawn rectangle requires four values")
    x1, y1, x2, y2 = values
    if x1 > x2 or y1 > y2:
        raise ValueError("NPC spawn rectangle is not normalized")
    return values


@dataclass(frozen=True)
class VersionedNpcSpawnPlacement:
    """Recovered create-block placement semantics, separate from NPC template."""

    floor_id: int
    placement_id: int
    birth_rect: tuple[int, int, int, int]
    move_rect: tuple[int, int, int, int]
    population_cap: int
    raw_direction: int
    respawn_delay_ms: int
    boundary_enabled: bool
    ignore_invincible_area: bool
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "placement_id", int(self.placement_id))
        object.__setattr__(self, "birth_rect", _normalized_rect(self.birth_rect))
        object.__setattr__(self, "move_rect", _normalized_rect(self.move_rect))
        object.__setattr__(self, "population_cap", int(self.population_cap))
        object.__setattr__(self, "raw_direction", int(self.raw_direction))
        object.__setattr__(
            self, "respawn_delay_ms", int(self.respawn_delay_ms)
        )
        object.__setattr__(
            self, "boundary_enabled", bool(self.boundary_enabled)
        )
        object.__setattr__(
            self,
            "ignore_invincible_area",
            bool(self.ignore_invincible_area),
        )
        if not str(self.source_version):
            raise ValueError("NPC spawn placement requires source_version")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered NPC spawn placement must remain LATER_RECOVERED"
            )

    @property
    def normalized_direction(self) -> int:
        """Descendant VALIDATEDIR(x): ((x % 8) + 8) % 8."""
        return ((self.raw_direction % 8) + 8) % 8

    @property
    def raw_direction_is_octant(self) -> bool:
        return 0 <= self.raw_direction < 8

    @property
    def generation_enabled(self) -> bool:
        """Matches create-loop gates: cap must be positive; negative time disables."""
        return self.population_cap > 0 and self.respawn_delay_ms >= 0

    @property
    def birth_is_single_cell(self) -> bool:
        x1, y1, x2, y2 = self.birth_rect
        return x1 == x2 and y1 == y2

    def birth_rect_in_bounds(self, world: VersionedWorldGeometryManifest) -> bool:
        definition = world.world.topology.maps.get(self.floor_id)
        if definition is None:
            return False
        x1, y1, x2, y2 = self.birth_rect
        return (
            0 <= x1 <= x2 < definition.width
            and 0 <= y1 <= y2 < definition.height
        )

    def move_rect_fully_in_bounds(
        self, world: VersionedWorldGeometryManifest
    ) -> bool:
        definition = world.world.topology.maps.get(self.floor_id)
        if definition is None:
            return False
        x1, y1, x2, y2 = self.move_rect
        return (
            0 <= x1 <= x2 < definition.width
            and 0 <= y1 <= y2 < definition.height
        )

    def direct_projection_issues(
        self,
        world: VersionedWorldGeometryManifest,
    ) -> tuple[str, ...]:
        """Issues that block direct modern-runtime instantiation.

        Movement rectangles may intentionally extend outside a map and therefore
        are not a blocker here. Actual movement remains constrained by map
        collision/walkability at runtime.
        """
        issues: list[str] = []
        if not self.birth_rect_in_bounds(world):
            issues.append(ISSUE_BIRTH_OUTSIDE_STABLE_MAP)
        if not self.raw_direction_is_octant:
            issues.append(ISSUE_NON_OCTANT_RAW_DIRECTION)
        if not self.generation_enabled:
            issues.append(ISSUE_GENERATION_DISABLED)
        return tuple(issues)

    def direct_projection_eligible(
        self,
        world: VersionedWorldGeometryManifest,
    ) -> bool:
        return not self.direct_projection_issues(world)


@dataclass(frozen=True)
class VersionedNpcSpawnCatalogue:
    """Strict stable-world catalogue of recovered create-layer placements."""

    world_geometry: VersionedWorldGeometryManifest
    placements: tuple[VersionedNpcSpawnPlacement, ...]
    source_version: str = SEMANTIC_SOURCE_VERSION

    def __post_init__(self) -> None:
        placements = tuple(self.placements)
        if self.source_version != self.world_geometry.source_version:
            raise ValueError("NPC spawn catalogue source-version drift")

        by_id: dict[int, VersionedNpcSpawnPlacement] = {}
        for placement in placements:
            if placement.placement_id in by_id:
                raise ValueError(
                    f"duplicate NPC spawn placement ID {placement.placement_id}"
                )
            by_id[placement.placement_id] = placement
            if placement.source_version != self.source_version:
                raise ValueError("NPC spawn placement source-version drift")
            if placement.floor_id not in self.world_geometry.world.by_floor:
                raise ValueError(
                    f"NPC spawn floor {placement.floor_id} absent from world"
                )

        geometry_by_id = {
            row.placement_id: row for row in self.world_geometry.placements
        }
        if set(by_id) != set(geometry_by_id):
            missing = sorted(set(geometry_by_id) - set(by_id))
            extra = sorted(set(by_id) - set(geometry_by_id))
            raise ValueError(
                "NPC spawn catalogue/geometry identity mismatch; "
                f"missing={missing}, extra={extra}"
            )

        for placement_id, geometry in geometry_by_id.items():
            placement = by_id[placement_id]
            expected = (
                geometry.floor_id,
                geometry.birth_rect,
                geometry.move_rect,
                geometry.create_num,
                geometry.direction,
                geometry.respawn_time,
                bool(geometry.boundary),
                bool(geometry.ignore_invincible),
            )
            actual = (
                placement.floor_id,
                placement.birth_rect,
                placement.move_rect,
                placement.population_cap,
                placement.raw_direction,
                placement.respawn_delay_ms,
                placement.boundary_enabled,
                placement.ignore_invincible_area,
            )
            if actual != expected:
                raise ValueError(
                    f"NPC spawn placement {placement_id} drift from geometry"
                )

        object.__setattr__(self, "placements", placements)

    @property
    def by_id(self) -> Mapping[int, VersionedNpcSpawnPlacement]:
        return MappingProxyType({
            placement.placement_id: placement
            for placement in self.placements
        })

    @property
    def by_floor(self) -> Mapping[int, tuple[VersionedNpcSpawnPlacement, ...]]:
        grouped: dict[int, list[VersionedNpcSpawnPlacement]] = {}
        for placement in self.placements:
            grouped.setdefault(placement.floor_id, []).append(placement)
        return MappingProxyType({
            floor: tuple(rows)
            for floor, rows in grouped.items()
        })

    @property
    def direct_projection_eligible(self) -> tuple[VersionedNpcSpawnPlacement, ...]:
        return tuple(
            placement
            for placement in self.placements
            if placement.direct_projection_eligible(self.world_geometry)
        )

    @property
    def quarantined(self) -> tuple[VersionedNpcSpawnPlacement, ...]:
        return tuple(
            placement
            for placement in self.placements
            if not placement.direct_projection_eligible(self.world_geometry)
        )

    def issue_counts(self) -> Mapping[str, int]:
        counts: dict[str, int] = {}
        for placement in self.placements:
            for issue in placement.direct_projection_issues(self.world_geometry):
                counts[issue] = counts.get(issue, 0) + 1
        return MappingProxyType(counts)


def build_versioned_npc_spawn_catalogue(
    world_geometry: VersionedWorldGeometryManifest,
) -> VersionedNpcSpawnCatalogue:
    placements = tuple(
        VersionedNpcSpawnPlacement(
            floor_id=row.floor_id,
            placement_id=row.placement_id,
            birth_rect=row.birth_rect,
            move_rect=row.move_rect,
            population_cap=row.create_num,
            raw_direction=row.direction,
            respawn_delay_ms=row.respawn_time,
            boundary_enabled=bool(row.boundary),
            ignore_invincible_area=bool(row.ignore_invincible),
            source_version=row.source_version,
            evidence_role=row.evidence_role,
        )
        for row in world_geometry.placements
    )
    return VersionedNpcSpawnCatalogue(
        world_geometry=world_geometry,
        placements=placements,
        source_version=world_geometry.source_version,
    )
