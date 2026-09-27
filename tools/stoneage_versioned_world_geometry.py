#!/usr/bin/env python3
"""Engine-neutral reader for derived versioned StoneAge world geometry."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import (
    HistoricalWorldTopology,
    LATER_RECOVERED,
    LegacyWarpEdge,
)
from tools.stoneage_versioned_world_manifest import VersionedWorldManifest


WORLD_GEOMETRY_REPORT_REF = (
    "research/recovered/STONEAGE-25-STABLE-WORLD-GEOMETRY-R1.txt"
)
SEMANTIC_SOURCE_VERSION = "recovered25"


def _rect(value: str) -> tuple[int, int, int, int]:
    parts = str(value).split(",")
    if len(parts) != 4:
        raise ValueError(f"invalid rectangle: {value}")
    rect = tuple(int(part) for part in parts)
    if rect[0] > rect[2] or rect[1] > rect[3]:
        raise ValueError(f"unnormalized rectangle: {value}")
    return rect  # type: ignore[return-value]


def _point3(value: str) -> tuple[int, int, int]:
    parts = str(value).split(",")
    if len(parts) != 3:
        raise ValueError(f"invalid floor/x/y tuple: {value}")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} record")
    out: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        if not key or key in out:
            raise ValueError(f"duplicate/blank {prefix} field: {key}")
        out[key] = value
    return out


@dataclass(frozen=True)
class VersionedNpcPlacementGeometry:
    floor_id: int
    placement_id: int
    birth_rect: tuple[int, int, int, int]
    move_rect: tuple[int, int, int, int]
    direction: int
    create_num: int
    respawn_time: int
    boundary: int
    ignore_invincible: int
    resolved_template_refs: int
    classic_warp_refs: int
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("NPC placement geometry must remain LATER_RECOVERED")
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "placement_id", int(self.placement_id))


@dataclass(frozen=True)
class VersionedClassicWarpGeometry:
    source_floor: int
    placement_id: int
    source_rect: tuple[int, int, int, int]
    destination_floor: int
    destination_x: int
    destination_y: int
    conditional_time: bool
    destination_is_stable_candidate: bool
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("classic warp geometry must remain LATER_RECOVERED")
        object.__setattr__(self, "source_floor", int(self.source_floor))
        object.__setattr__(self, "placement_id", int(self.placement_id))
        object.__setattr__(self, "destination_floor", int(self.destination_floor))
        object.__setattr__(self, "destination_x", int(self.destination_x))
        object.__setattr__(self, "destination_y", int(self.destination_y))
        object.__setattr__(self, "conditional_time", bool(self.conditional_time))
        object.__setattr__(
            self,
            "destination_is_stable_candidate",
            bool(self.destination_is_stable_candidate),
        )

    @property
    def source_is_single_cell(self) -> bool:
        x1, y1, x2, y2 = self.source_rect
        return x1 == x2 and y1 == y2


@dataclass(frozen=True)
class VersionedEncounterAreaGeometry:
    index: int
    floor_id: int
    rect: tuple[int, int, int, int]
    probability_min: int
    probability_max: int
    enemy_max_num: int
    zorder: int
    positive_group_ref_count: int
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("encounter geometry must remain LATER_RECOVERED")
        for name in (
            "index",
            "floor_id",
            "probability_min",
            "probability_max",
            "enemy_max_num",
            "zorder",
            "positive_group_ref_count",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))


@dataclass(frozen=True)
class VersionedWorldGeometryManifest:
    world: VersionedWorldManifest
    placements: tuple[VersionedNpcPlacementGeometry, ...]
    classic_warps: tuple[VersionedClassicWarpGeometry, ...]
    encounters: tuple[VersionedEncounterAreaGeometry, ...]
    source_version: str = SEMANTIC_SOURCE_VERSION
    report_ref: str = WORLD_GEOMETRY_REPORT_REF

    def __post_init__(self) -> None:
        placements = tuple(self.placements)
        warps = tuple(self.classic_warps)
        encounters = tuple(self.encounters)
        if self.source_version != self.world.semantic_source_version:
            raise ValueError("world geometry semantic source version drift")

        world_ids = set(self.world.by_floor)
        for row in placements:
            if row.floor_id not in world_ids:
                raise ValueError(
                    f"NPC placement floor {row.floor_id} absent from world manifest"
                )
            if row.source_version != self.source_version:
                raise ValueError("NPC placement source-version drift")
        for row in warps:
            if row.source_floor not in world_ids:
                raise ValueError(
                    f"classic warp source floor {row.source_floor} absent from world"
                )
            if row.source_version != self.source_version:
                raise ValueError("classic warp source-version drift")
        for row in encounters:
            if row.floor_id not in world_ids:
                raise ValueError(
                    f"encounter floor {row.floor_id} absent from world manifest"
                )
            if row.source_version != self.source_version:
                raise ValueError("encounter source-version drift")

        placement_counts: dict[int, int] = {}
        for row in placements:
            placement_counts[row.floor_id] = placement_counts.get(row.floor_id, 0) + 1
        encounter_counts: dict[int, int] = {}
        for row in encounters:
            encounter_counts[row.floor_id] = encounter_counts.get(row.floor_id, 0) + 1

        for floor in self.world.floors:
            expected_npc = floor.semantic.npc_create_count
            actual_npc = placement_counts.get(floor.floor_id, 0)
            if actual_npc != expected_npc:
                raise ValueError(
                    f"NPC placement coverage drift on floor {floor.floor_id}: "
                    f"expected={expected_npc}, actual={actual_npc}"
                )
            expected_encounter = floor.semantic.encounter_row_count
            actual_encounter = encounter_counts.get(floor.floor_id, 0)
            if actual_encounter != expected_encounter:
                raise ValueError(
                    f"encounter coverage drift on floor {floor.floor_id}: "
                    f"expected={expected_encounter}, actual={actual_encounter}"
                )

        object.__setattr__(self, "placements", placements)
        object.__setattr__(self, "classic_warps", warps)
        object.__setattr__(self, "encounters", encounters)

    @property
    def placements_by_floor(self) -> Mapping[int, tuple[VersionedNpcPlacementGeometry, ...]]:
        grouped: dict[int, list[VersionedNpcPlacementGeometry]] = {}
        for row in self.placements:
            grouped.setdefault(row.floor_id, []).append(row)
        return MappingProxyType({
            floor: tuple(rows) for floor, rows in grouped.items()
        })

    @property
    def encounters_by_floor(self) -> Mapping[int, tuple[VersionedEncounterAreaGeometry, ...]]:
        grouped: dict[int, list[VersionedEncounterAreaGeometry]] = {}
        for row in self.encounters:
            grouped.setdefault(row.floor_id, []).append(row)
        return MappingProxyType({
            floor: tuple(rows) for floor, rows in grouped.items()
        })

    def projectable_legacy_warp_edges(self) -> tuple[LegacyWarpEdge, ...]:
        """Project only unambiguous classic overlap warps into executable topology."""
        topology = self.world.topology
        candidates: list[tuple[MapPosition, MapPosition]] = []
        source_counts: dict[MapPosition, int] = {}

        for row in self.classic_warps:
            if not row.source_is_single_cell:
                continue
            if row.conditional_time:
                continue
            if not row.destination_is_stable_candidate:
                continue
            x1, y1, _x2, _y2 = row.source_rect
            source = MapPosition(row.source_floor, x1, y1)
            destination = MapPosition(
                row.destination_floor,
                row.destination_x,
                row.destination_y,
            )
            if not topology.is_valid_position(source):
                continue
            if not topology.is_valid_position(destination):
                continue
            candidates.append((source, destination))
            source_counts[source] = source_counts.get(source, 0) + 1

        return tuple(
            LegacyWarpEdge(source=source, destination=destination)
            for source, destination in candidates
            if source_counts[source] == 1
        )

    def topology_with_projectable_legacy_warps(self) -> HistoricalWorldTopology:
        """Return strict topology with only safely projectable later warp edges."""
        return HistoricalWorldTopology.from_provenance_maps(
            self.world.topology.maps,
            legacy_warps=self.projectable_legacy_warp_edges(),
        )


def parse_versioned_world_geometry(
    *,
    world: VersionedWorldManifest,
    text: str,
) -> VersionedWorldGeometryManifest:
    source_version: str | None = None
    evidence_role: str | None = None
    counts: dict[str, int] = {}
    placements: list[VersionedNpcPlacementGeometry] = []
    warps: list[VersionedClassicWarpGeometry] = []
    encounters: list[VersionedEncounterAreaGeometry] = []
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SEMANTIC_SOURCE_VERSION|"):
            if source_version is not None:
                raise ValueError("duplicate semantic source version")
            source_version = line.split("|", 1)[1]
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            if evidence_role is not None:
                raise ValueError("duplicate geometry evidence role")
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed COUNT row: {line}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("NPC_PLACEMENT|"):
            fields = _fields(line, "NPC_PLACEMENT")
            placements.append(
                VersionedNpcPlacementGeometry(
                    floor_id=int(fields["floor"]),
                    placement_id=int(fields["placement"]),
                    birth_rect=_rect(fields["birth"]),
                    move_rect=_rect(fields["move"]),
                    direction=int(fields["dir"]),
                    create_num=int(fields["create_num"]),
                    respawn_time=int(fields["respawn_time"]),
                    boundary=int(fields["boundary"]),
                    ignore_invincible=int(fields["ignore_invincible"]),
                    resolved_template_refs=int(fields["resolved_templates"]),
                    classic_warp_refs=int(fields["classic_warp_refs"]),
                    source_version=source_version or "",
                    evidence_role=evidence_role or "",
                )
            )
            continue
        if line.startswith("CLASSIC_WARP|"):
            fields = _fields(line, "CLASSIC_WARP")
            destination = _point3(fields["to"])
            warps.append(
                VersionedClassicWarpGeometry(
                    source_floor=int(fields["floor"]),
                    placement_id=int(fields["placement"]),
                    source_rect=_rect(fields["source"]),
                    destination_floor=destination[0],
                    destination_x=destination[1],
                    destination_y=destination[2],
                    conditional_time=bool(int(fields["conditional_time"])),
                    destination_is_stable_candidate=bool(
                        int(fields["destination_stable"])
                    ),
                    source_version=source_version or "",
                    evidence_role=evidence_role or "",
                )
            )
            continue
        if line.startswith("ENCOUNTER_AREA|"):
            fields = _fields(line, "ENCOUNTER_AREA")
            encounters.append(
                VersionedEncounterAreaGeometry(
                    index=int(fields["index"]),
                    floor_id=int(fields["floor"]),
                    rect=_rect(fields["rect"]),
                    probability_min=int(fields["prob_min"]),
                    probability_max=int(fields["prob_max"]),
                    enemy_max_num=int(fields["enemy_max"]),
                    zorder=int(fields["zorder"]),
                    positive_group_ref_count=int(fields["positive_group_refs"]),
                    source_version=source_version or "",
                    evidence_role=evidence_role or "",
                )
            )
            continue
        if line == "RESOLUTION|VERSIONED_WORLD_GEOMETRY_CLASSIFIED":
            resolution = True

    if source_version is None:
        raise ValueError("world geometry lacks semantic source version")
    if evidence_role != LATER_RECOVERED:
        raise ValueError(
            "world geometry evidence must remain LATER_RECOVERED"
        )
    if not resolution:
        raise ValueError("world geometry lacks closed resolution marker")

    detail_counts = {
        "npc_placements": len(placements),
        "classic_warp_edges": len(warps),
        "encounter_areas": len(encounters),
    }
    for name, actual in detail_counts.items():
        if name not in counts:
            raise ValueError(f"world geometry lacks {name} count")
        if counts[name] != actual:
            raise ValueError(
                f"world geometry {name} detail count drift: "
                f"declared={counts[name]}, actual={actual}"
            )

    return VersionedWorldGeometryManifest(
        world=world,
        placements=tuple(placements),
        classic_warps=tuple(warps),
        encounters=tuple(encounters),
        source_version=source_version,
    )
