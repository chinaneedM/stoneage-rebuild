#!/usr/bin/env python3
"""Provenance-safe recovered25 supplemental world extension.

This module consumes only derived audit metadata. It references the existing
761-floor stable VersionedWorldManifest without mutating or reclassifying it.

Runtime-reachable supplemental floors are split into:
- resolved/materializable concrete recovered25 maps;
- unresolved floors whose concrete payload identity is ambiguous.

No unresolved payload candidate is selected automatically. Supplemental content
remains LATER_RECOVERED with RESOURCE_RELATION_UNKNOWN.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LATER_RECOVERED,
    RESOURCE_RELATION_UNKNOWN,
    WorldMapProvenance,
)
from tools.stoneage_versioned_world_manifest import (
    VersionedWorldManifest,
    VersionedWorldSemanticCoverage,
)


SUPPLEMENTAL_AUDIT_REPORT_REF = (
    "research/recovered/STONEAGE-25-SUPPLEMENTAL-WORLD-AUDIT-R1.txt"
)
SEMANTIC_SOURCE_VERSION = "recovered25"
UNIQUE = "UNIQUE"
DUPLICATE_IDENTICAL = "DUPLICATE_IDENTICAL"
DUPLICATE_DIVERGENT = "DUPLICATE_DIVERGENT"
RESOLUTION = "RESOLUTION|SUPPLEMENTAL_WORLD_AUDIT_CLASSIFIED"
SUPPLEMENTAL_MAP_EVIDENCE = "RECOVERED25_SUPPLEMENTAL_SERVER_MAP"


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


def _hash(value: str) -> str:
    digest = str(value).lower()
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError("supplemental map SHA-256 must be 64 hex digits")
    return digest


def _dimensions(value: str) -> tuple[int, int]:
    pieces = str(value).lower().split("x", 1)
    if len(pieces) != 2:
        raise ValueError(f"invalid supplemental map dimensions: {value}")
    width, height = int(pieces[0]), int(pieces[1])
    if width <= 0 or height <= 0:
        raise ValueError("supplemental map dimensions must be positive")
    return width, height


@dataclass(frozen=True)
class SupplementalWorldSemantic:
    depth: int
    reachability_status: str
    incoming_reachable_warps: int
    outgoing_runtime_warps: int
    coverage: VersionedWorldSemanticCoverage

    def __post_init__(self) -> None:
        depth = int(self.depth)
        incoming = int(self.incoming_reachable_warps)
        outgoing = int(self.outgoing_runtime_warps)
        if depth <= 0:
            raise ValueError("supplemental floor depth must be positive")
        if incoming <= 0:
            raise ValueError("supplemental floor must have a reachable ingress")
        if outgoing < 0:
            raise ValueError("supplemental outgoing warp count cannot be negative")
        if not str(self.reachability_status):
            raise ValueError("supplemental floor requires reachability status")
        if self.coverage.source_version != SEMANTIC_SOURCE_VERSION:
            raise ValueError("supplemental semantic source-version drift")
        if self.coverage.evidence_role != LATER_RECOVERED:
            raise ValueError("supplemental semantics were promoted")
        object.__setattr__(self, "depth", depth)
        object.__setattr__(self, "incoming_reachable_warps", incoming)
        object.__setattr__(self, "outgoing_runtime_warps", outgoing)


@dataclass(frozen=True)
class ResolvedSupplementalWorldFloor:
    floor_id: int
    server_paths: tuple[str, ...]
    width: int
    height: int
    map_sha256: str
    server_copy_status: str
    semantic: SupplementalWorldSemantic

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        paths = tuple(str(path) for path in self.server_paths)
        width = int(self.width)
        height = int(self.height)
        digest = _hash(self.map_sha256)
        if floor_id < 0:
            raise ValueError("supplemental floor id cannot be negative")
        if not paths:
            raise ValueError("resolved supplemental floor requires server path")
        if width <= 0 or height <= 0:
            raise ValueError("resolved supplemental dimensions must be positive")
        if self.server_copy_status not in {UNIQUE, DUPLICATE_IDENTICAL}:
            raise ValueError("resolved supplemental floor has unsafe copy status")
        if self.server_copy_status == UNIQUE and len(paths) != 1:
            raise ValueError("UNIQUE supplemental floor must have one path")
        if self.server_copy_status == DUPLICATE_IDENTICAL and len(paths) < 2:
            raise ValueError("identical duplicate floor must preserve all paths")
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "server_paths", paths)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "map_sha256", digest)

    @property
    def provenance(self) -> WorldMapProvenance:
        return WorldMapProvenance(
            content_role=LATER_RECOVERED,
            resource_role=RESOURCE_RELATION_UNKNOWN,
            source_versions=(SEMANTIC_SOURCE_VERSION,),
            evidence_refs=(SUPPLEMENTAL_AUDIT_REPORT_REF,),
            payload_sha256=self.map_sha256,
        )

    def to_map_definition(self) -> HistoricalMapDefinition:
        return HistoricalMapDefinition(
            floor_id=self.floor_id,
            width=self.width,
            height=self.height,
            evidence=SUPPLEMENTAL_MAP_EVIDENCE,
            provenance=self.provenance,
        )


@dataclass(frozen=True)
class UnresolvedSupplementalWorldFloor:
    floor_id: int
    server_paths: tuple[str, ...]
    server_dimensions: tuple[tuple[int, int], ...]
    server_sha256s: tuple[str, ...]
    server_copy_status: str
    semantic: SupplementalWorldSemantic

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        paths = tuple(str(path) for path in self.server_paths)
        dimensions = tuple(
            (int(width), int(height))
            for width, height in self.server_dimensions
        )
        hashes = tuple(_hash(value) for value in self.server_sha256s)
        if floor_id < 0:
            raise ValueError("unresolved supplemental floor id cannot be negative")
        if self.server_copy_status != DUPLICATE_DIVERGENT:
            raise ValueError("unresolved floor must preserve divergent-copy status")
        if len(paths) < 2:
            raise ValueError("divergent floor requires multiple candidate paths")
        if len(paths) != len(dimensions) or len(paths) != len(hashes):
            raise ValueError("unresolved supplemental candidate count drift")
        if len(set(hashes)) < 2:
            raise ValueError("divergent supplemental floor hashes are not divergent")
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "server_paths", paths)
        object.__setattr__(self, "server_dimensions", dimensions)
        object.__setattr__(self, "server_sha256s", hashes)


@dataclass(frozen=True)
class SupplementalWorldExtension:
    stable_world: VersionedWorldManifest
    resolved_floors: tuple[ResolvedSupplementalWorldFloor, ...]
    unresolved_floors: tuple[UnresolvedSupplementalWorldFloor, ...]
    semantic_source_version: str = SEMANTIC_SOURCE_VERSION
    audit_report_ref: str = SUPPLEMENTAL_AUDIT_REPORT_REF

    def __post_init__(self) -> None:
        resolved = tuple(self.resolved_floors)
        unresolved = tuple(self.unresolved_floors)
        stable_ids = set(self.stable_world.by_floor)
        resolved_ids = [row.floor_id for row in resolved]
        unresolved_ids = [row.floor_id for row in unresolved]
        if len(resolved_ids) != len(set(resolved_ids)):
            raise ValueError("supplemental extension has duplicate resolved floors")
        if len(unresolved_ids) != len(set(unresolved_ids)):
            raise ValueError("supplemental extension has duplicate unresolved floors")
        if set(resolved_ids) & set(unresolved_ids):
            raise ValueError("supplemental floor cannot be both resolved and unresolved")
        overlap = stable_ids & (set(resolved_ids) | set(unresolved_ids))
        if overlap:
            raise ValueError(
                f"supplemental extension overlaps stable world: {sorted(overlap)}"
            )
        if str(self.semantic_source_version) != SEMANTIC_SOURCE_VERSION:
            raise ValueError("supplemental extension source-version drift")
        if not str(self.audit_report_ref):
            raise ValueError("supplemental extension requires audit report ref")
        object.__setattr__(self, "resolved_floors", resolved)
        object.__setattr__(self, "unresolved_floors", unresolved)

    @property
    def resolved_by_floor(self) -> Mapping[int, ResolvedSupplementalWorldFloor]:
        return MappingProxyType({
            row.floor_id: row for row in self.resolved_floors
        })

    @property
    def unresolved_by_floor(
        self,
    ) -> Mapping[int, UnresolvedSupplementalWorldFloor]:
        return MappingProxyType({
            row.floor_id: row for row in self.unresolved_floors
        })

    @property
    def reachable_floor_ids(self) -> frozenset[int]:
        return frozenset(
            set(self.stable_world.by_floor)
            | set(self.resolved_by_floor)
            | set(self.unresolved_by_floor)
        )

    @property
    def materializable_floor_ids(self) -> frozenset[int]:
        return frozenset(
            set(self.stable_world.by_floor) | set(self.resolved_by_floor)
        )

    @property
    def materializable_map_definitions(
        self,
    ) -> Mapping[int, HistoricalMapDefinition]:
        maps = dict(self.stable_world.topology.maps)
        for row in self.resolved_floors:
            if row.floor_id in maps:
                raise ValueError("supplemental materialization would replace stable map")
            maps[row.floor_id] = row.to_map_definition()
        return MappingProxyType(maps)

    def materializable_map_topology(self) -> HistoricalWorldTopology:
        """Map-only topology; unresolved floors and warp edges remain external."""
        return HistoricalWorldTopology.from_provenance_maps(
            self.materializable_map_definitions
        )


def parse_supplemental_world_audit(
    *,
    stable_world: VersionedWorldManifest,
    text: str,
) -> SupplementalWorldExtension:
    source_version: str | None = None
    evidence_role: str | None = None
    counts: dict[str, int] = {}
    resolved: list[ResolvedSupplementalWorldFloor] = []
    unresolved: list[UnresolvedSupplementalWorldFloor] = []
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SEMANTIC_SOURCE_VERSION|"):
            source_version = line.split("|", 1)[1]
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed supplemental COUNT row: {line}")
            if parts[1] in counts:
                raise ValueError(f"duplicate supplemental COUNT key: {parts[1]}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("SUPPLEMENTAL_AUDIT|"):
            fields = _fields(line, "SUPPLEMENTAL_AUDIT")
            floor_id = int(fields["floor"])
            paths = tuple(
                value for value in fields["server_paths"].split(",") if value
            )
            dimensions = tuple(
                _dimensions(value)
                for value in fields["server_dimensions"].split(",")
                if value
            )
            hashes = tuple(
                _hash(value)
                for value in fields["server_sha256s"].split(",")
                if value
            )
            semantic = SupplementalWorldSemantic(
                depth=int(fields["depth"]),
                reachability_status=fields["reachability_status"],
                incoming_reachable_warps=int(fields["incoming_reachable_warps"]),
                outgoing_runtime_warps=int(fields["outgoing_runtime_warps"]),
                coverage=VersionedWorldSemanticCoverage(
                    source_version=source_version or "",
                    server_map_present=True,
                    npc_create_count=int(fields["npc_create_count"]),
                    warp_functionset_create_count=int(
                        fields["warp_functionset_create_count"]
                    ),
                    encounter_row_count=int(fields["encounter_rows"]),
                    active_encounter_row_count=int(
                        fields["active_encounter_rows"]
                    ),
                ),
            )
            copy_status = fields["server_copy_status"]
            materializable = bool(int(fields["static_materializable"]))

            if copy_status == DUPLICATE_DIVERGENT:
                if materializable:
                    raise ValueError(
                        f"divergent floor {floor_id} was silently materialized"
                    )
                unresolved.append(
                    UnresolvedSupplementalWorldFloor(
                        floor_id=floor_id,
                        server_paths=paths,
                        server_dimensions=dimensions,
                        server_sha256s=hashes,
                        server_copy_status=copy_status,
                        semantic=semantic,
                    )
                )
                continue

            if not materializable:
                raise ValueError(
                    f"non-divergent supplemental floor {floor_id} is not materializable"
                )
            if int(fields["missing_image_ids"]) != 0:
                raise ValueError(
                    f"materializable supplemental floor {floor_id} has missing metadata"
                )
            if len(set(dimensions)) != 1:
                raise ValueError(
                    f"resolved supplemental floor {floor_id} has dimension drift"
                )
            if len(set(hashes)) != 1:
                raise ValueError(
                    f"resolved supplemental floor {floor_id} has payload drift"
                )
            width, height = dimensions[0]
            resolved.append(
                ResolvedSupplementalWorldFloor(
                    floor_id=floor_id,
                    server_paths=paths,
                    width=width,
                    height=height,
                    map_sha256=hashes[0],
                    server_copy_status=copy_status,
                    semantic=semantic,
                )
            )
            continue

        if line == RESOLUTION:
            resolution = True

    if source_version != SEMANTIC_SOURCE_VERSION:
        raise ValueError("supplemental audit source-version drift")
    if evidence_role != LATER_RECOVERED:
        raise ValueError("supplemental audit evidence was promoted")
    if not resolution:
        raise ValueError("supplemental audit lacks closed resolution marker")

    extension = SupplementalWorldExtension(
        stable_world=stable_world,
        resolved_floors=tuple(sorted(resolved, key=lambda row: row.floor_id)),
        unresolved_floors=tuple(
            sorted(unresolved, key=lambda row: row.floor_id)
        ),
        semantic_source_version=source_version,
    )

    declared_total = counts.get("supplemental_floor_ids")
    if declared_total is None:
        raise ValueError("supplemental audit lacks floor count")
    actual_total = len(extension.resolved_floors) + len(extension.unresolved_floors)
    if declared_total != actual_total:
        raise ValueError(
            "supplemental audit detail count drift: "
            f"declared={declared_total}, actual={actual_total}"
        )
    if counts.get("static_materializable_floors") != len(
        extension.resolved_floors
    ):
        raise ValueError("supplemental resolved-floor aggregate drift")
    if counts.get("static_unresolved_floors") != len(
        extension.unresolved_floors
    ):
        raise ValueError("supplemental unresolved-floor aggregate drift")
    return extension
