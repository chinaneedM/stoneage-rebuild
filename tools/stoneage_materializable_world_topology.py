#!/usr/bin/env python3
"""Strict executable topology for the materializable recovered25 world.

Consumes only derived, provenance-safe reports. The topology activates only
classic Warp sources that are:
- inside the 826 materializable map set;
- unconditional;
- unambiguous at their source cell.

Exact-equivalent duplicate records are collapsed. Conditional-time records and
multi-destination source conflicts remain explicit evidence queues rather than
being guessed into active runtime behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import (
    HistoricalWorldTopology,
    LegacyWarpEdge,
)
from tools.stoneage_supplemental_world_manifest import (
    SUPPLEMENTAL_AUDIT_REPORT_REF,
    SupplementalWorldExtension,
    parse_supplemental_world_audit,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


GEOMETRY_REPORT_REF = (
    "research/recovered/"
    "STONEAGE-25-MATERIALIZABLE-WORLD-WARP-GEOMETRY-R1.txt"
)
GEOMETRY_RESOLUTION = (
    "RESOLUTION|MATERIALIZABLE_RECOVERED_WORLD_WARP_GEOMETRY_CLOSED"
)


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} row")
    out: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        if not key or key in out:
            raise ValueError(f"duplicate/blank {prefix} field: {key}")
        out[key] = value
    return out


def _position(value: str) -> MapPosition:
    parts = tuple(int(v) for v in str(value).split(","))
    if len(parts) != 3:
        raise ValueError(f"expected floor,x,y position: {value}")
    return MapPosition(parts[0], parts[1], parts[2])


@dataclass(frozen=True)
class RecoveredWarpGeometryRecord:
    source: MapPosition
    placement_id: int
    destination: MapPosition
    conditional_time: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "placement_id", int(self.placement_id))
        object.__setattr__(
            self,
            "conditional_time",
            bool(self.conditional_time),
        )

    @property
    def signature(self) -> tuple[MapPosition, bool]:
        return self.destination, self.conditional_time


@dataclass(frozen=True)
class ExactDuplicateWarpGroup:
    source: MapPosition
    destination: MapPosition
    placement_ids: tuple[int, ...]

    def __post_init__(self) -> None:
        ids = tuple(int(v) for v in self.placement_ids)
        if len(ids) < 2:
            raise ValueError("exact duplicate group requires multiple records")
        object.__setattr__(self, "placement_ids", ids)


@dataclass(frozen=True)
class DeferredConditionalWarp:
    source: MapPosition
    destination: MapPosition
    placement_ids: tuple[int, ...]

    def __post_init__(self) -> None:
        ids = tuple(int(v) for v in self.placement_ids)
        if not ids:
            raise ValueError("deferred conditional Warp requires evidence")
        object.__setattr__(self, "placement_ids", ids)


@dataclass(frozen=True)
class AmbiguousWarpSource:
    source: MapPosition
    candidates: tuple[RecoveredWarpGeometryRecord, ...]

    def __post_init__(self) -> None:
        rows = tuple(self.candidates)
        if len(rows) < 2:
            raise ValueError("ambiguous Warp source requires multiple candidates")
        if any(row.source != self.source for row in rows):
            raise ValueError("ambiguous Warp candidates do not share source")
        signatures = {row.signature for row in rows}
        if len(signatures) < 2:
            raise ValueError("ambiguous Warp source has only one signature")
        object.__setattr__(self, "candidates", rows)


@dataclass(frozen=True)
class QuarantinedWarpRecord:
    source_floor: int
    placement_id: int
    source_rect: tuple[int, int, int, int]
    destination: MapPosition
    conditional_time: bool
    reason: str


@dataclass(frozen=True)
class MaterializableRuntimeTopology:
    extension: SupplementalWorldExtension
    topology: HistoricalWorldTopology
    exact_duplicate_groups: tuple[ExactDuplicateWarpGroup, ...]
    deferred_conditional_warps: tuple[DeferredConditionalWarp, ...]
    ambiguous_sources: tuple[AmbiguousWarpSource, ...]
    quarantined_warps: tuple[QuarantinedWarpRecord, ...]
    raw_materializable_warp_records: int

    def __post_init__(self) -> None:
        if len(self.topology.maps) != len(self.extension.materializable_floor_ids):
            raise ValueError("runtime topology map count drift")
        if set(self.topology.maps) != set(self.extension.materializable_floor_ids):
            raise ValueError("runtime topology map set drift")
        if any(edge.time_token is not None for edge in self.topology.legacy_warps):
            raise ValueError("active runtime Warp unexpectedly has time token")
        if any(not edge.active for edge in self.topology.legacy_warps):
            raise ValueError("runtime topology should contain active edges only")

    @property
    def ambiguous_by_source(self) -> Mapping[MapPosition, AmbiguousWarpSource]:
        return MappingProxyType({
            row.source: row for row in self.ambiguous_sources
        })

    @property
    def deferred_by_source(
        self,
    ) -> Mapping[MapPosition, DeferredConditionalWarp]:
        return MappingProxyType({
            row.source: row for row in self.deferred_conditional_warps
        })


def _load_extension(
    *,
    lineage_text: str,
    coverage_text: str,
    supplemental_text: str,
) -> SupplementalWorldExtension:
    stable_maps = parse_stable_later_map_manifest(lineage_text)
    stable_world = build_versioned_world_manifest(
        maps=stable_maps,
        coverage_text=coverage_text,
    )
    return parse_supplemental_world_audit(
        stable_world=stable_world,
        text=supplemental_text,
    )


def build_materializable_runtime_topology(
    *,
    extension: SupplementalWorldExtension,
    geometry_text: str,
) -> MaterializableRuntimeTopology:
    counts: dict[str, int] = {}
    records: list[RecoveredWarpGeometryRecord] = []
    quarantined: list[QuarantinedWarpRecord] = []
    resolution = False

    for raw in str(geometry_text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed geometry COUNT: {line}")
            if parts[1] in counts:
                raise ValueError(f"duplicate geometry COUNT: {parts[1]}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("MATERIALIZABLE_WARP|"):
            fields = _fields(line, "MATERIALIZABLE_WARP")
            records.append(
                RecoveredWarpGeometryRecord(
                    source=_position(fields["source"]),
                    placement_id=int(fields["placement"]),
                    destination=_position(fields["destination"]),
                    conditional_time=bool(int(fields["conditional_time"])),
                )
            )
            continue
        if line.startswith("QUARANTINED_WARP|"):
            fields = _fields(line, "QUARANTINED_WARP")
            rect = tuple(int(v) for v in fields["source"].split(","))
            if len(rect) != 4:
                raise ValueError("quarantined Warp source rect is malformed")
            quarantined.append(
                QuarantinedWarpRecord(
                    source_floor=int(fields["source_floor"]),
                    placement_id=int(fields["placement"]),
                    source_rect=rect,
                    destination=_position(fields["destination"]),
                    conditional_time=bool(int(fields["conditional_time"])),
                    reason=fields["reason"],
                )
            )
            continue
        if line == GEOMETRY_RESOLUTION:
            resolution = True

    if not resolution:
        raise ValueError("materializable Warp geometry report is not closed")
    if counts.get("materializable_floor_ids") != len(
        extension.materializable_floor_ids
    ):
        raise ValueError("geometry/extension materializable map count drift")
    if counts.get("represented_floor_ids") != len(
        extension.reachable_floor_ids
    ):
        raise ValueError("geometry/extension represented floor count drift")
    if counts.get("materializable_classic_warps") != len(records):
        raise ValueError("materializable Warp detail count drift")
    if counts.get("quarantined_classic_warps") != len(quarantined):
        raise ValueError("quarantined Warp detail count drift")

    materializable_ids = set(extension.materializable_floor_ids)
    for row in records:
        if row.source.floor_id not in materializable_ids:
            raise ValueError("materializable Warp source lacks materializable map")
        if row.destination.floor_id not in materializable_ids:
            raise ValueError(
                "materializable Warp destination lacks materializable map"
            )

    by_source: dict[MapPosition, list[RecoveredWarpGeometryRecord]] = {}
    for row in records:
        by_source.setdefault(row.source, []).append(row)

    active: list[LegacyWarpEdge] = []
    exact_duplicates: list[ExactDuplicateWarpGroup] = []
    deferred: list[DeferredConditionalWarp] = []
    ambiguous: list[AmbiguousWarpSource] = []

    for source in sorted(
        by_source,
        key=lambda pos: (pos.floor_id, pos.x, pos.y),
    ):
        group = tuple(by_source[source])
        signatures = {row.signature for row in group}
        if len(signatures) > 1:
            ambiguous.append(
                AmbiguousWarpSource(source=source, candidates=group)
            )
            continue

        exemplar = group[0]
        if len(group) > 1:
            exact_duplicates.append(
                ExactDuplicateWarpGroup(
                    source=source,
                    destination=exemplar.destination,
                    placement_ids=tuple(row.placement_id for row in group),
                )
            )

        if exemplar.conditional_time:
            deferred.append(
                DeferredConditionalWarp(
                    source=source,
                    destination=exemplar.destination,
                    placement_ids=tuple(row.placement_id for row in group),
                )
            )
            continue

        active.append(
            LegacyWarpEdge(
                source=source,
                destination=exemplar.destination,
                time_token=None,
                active=True,
            )
        )

    topology = HistoricalWorldTopology.from_provenance_maps(
        extension.materializable_map_definitions,
        legacy_warps=tuple(active),
    )

    # Cross-check the current derived aggregate without hard-coding the values.
    if counts.get("conditional_time_materializable_warps") != sum(
        row.conditional_time for row in records
    ):
        raise ValueError("conditional Warp aggregate drift")

    return MaterializableRuntimeTopology(
        extension=extension,
        topology=topology,
        exact_duplicate_groups=tuple(exact_duplicates),
        deferred_conditional_warps=tuple(deferred),
        ambiguous_sources=tuple(ambiguous),
        quarantined_warps=tuple(quarantined),
        raw_materializable_warp_records=len(records),
    )


def load_materializable_runtime_topology() -> MaterializableRuntimeTopology:
    extension = _load_extension(
        lineage_text=Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8"),
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
        supplemental_text=Path(SUPPLEMENTAL_AUDIT_REPORT_REF).read_text(
            encoding="utf-8"
        ),
    )
    return build_materializable_runtime_topology(
        extension=extension,
        geometry_text=Path(GEOMETRY_REPORT_REF).read_text(encoding="utf-8"),
    )
