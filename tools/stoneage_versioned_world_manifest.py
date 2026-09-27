#!/usr/bin/env python3
"""Engine-neutral versioned world-content manifest.

This joins the complete stable-later map lineage manifest to derived floor-level
world-semantic coverage from the recovered 2.5 server specimen.

The join is deliberately strict:
- map payload identity/dimensions come from the provenance-safe map library;
- NPC/warp/encounter coverage remains LATER_RECOVERED semantic evidence;
- no recovered 2.5 semantic row can promote a map to Taiwan-v1 membership;
- missing later semantic coverage is explicit and never treated as "empty map".
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import (
    HistoricalWorldTopology,
    LATER_RECOVERED,
)
from tools.stoneage_world_map_library import (
    StableLaterMapManifest,
)


COVERAGE_REPORT_REF = (
    "research/recovered/STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt"
)
SEMANTIC_SOURCE_VERSION = "recovered25"


@dataclass(frozen=True)
class VersionedWorldSemanticCoverage:
    """Recovered semantic coverage for one concrete map floor."""

    source_version: str
    server_map_present: bool
    npc_create_count: int
    warp_functionset_create_count: int
    encounter_row_count: int
    active_encounter_row_count: int
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        source_version = str(self.source_version)
        evidence_role = str(self.evidence_role)
        if not source_version:
            raise ValueError("world semantic coverage requires source_version")
        if evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered 2.5 world semantics must remain LATER_RECOVERED"
            )
        values = {}
        for name in (
            "npc_create_count",
            "warp_functionset_create_count",
            "encounter_row_count",
            "active_encounter_row_count",
        ):
            value = int(getattr(self, name))
            if value < 0:
                raise ValueError(f"{name} cannot be negative")
            values[name] = value
        if (
            values["warp_functionset_create_count"]
            > values["npc_create_count"]
        ):
            raise ValueError("warp count cannot exceed NPC create count")
        if (
            values["active_encounter_row_count"]
            > values["encounter_row_count"]
        ):
            raise ValueError(
                "active encounter count cannot exceed encounter row count"
            )
        object.__setattr__(self, "source_version", source_version)
        object.__setattr__(self, "evidence_role", evidence_role)
        object.__setattr__(
            self, "server_map_present", bool(self.server_map_present)
        )
        for name, value in values.items():
            object.__setattr__(self, name, value)

    @property
    def has_npc_semantics(self) -> bool:
        return self.npc_create_count > 0

    @property
    def has_warp_semantics(self) -> bool:
        return self.warp_functionset_create_count > 0

    @property
    def has_encounter_semantics(self) -> bool:
        return self.encounter_row_count > 0

    @property
    def has_recovered_world_semantics(self) -> bool:
        return self.has_npc_semantics or self.has_encounter_semantics


@dataclass(frozen=True)
class VersionedWorldFloor:
    """One stable map plus separately provenance-tagged world semantics."""

    floor_id: int
    path: str
    width: int
    height: int
    map_sha256: str
    semantic: VersionedWorldSemanticCoverage

    def __post_init__(self) -> None:
        object.__setattr__(self, "floor_id", int(self.floor_id))
        object.__setattr__(self, "path", str(self.path).lower())
        object.__setattr__(self, "width", int(self.width))
        object.__setattr__(self, "height", int(self.height))
        sha = str(self.map_sha256).lower()
        if len(sha) != 64 or any(
            ch not in "0123456789abcdef" for ch in sha
        ):
            raise ValueError("world floor map_sha256 must be 64 hex digits")
        object.__setattr__(self, "map_sha256", sha)
        if not isinstance(self.semantic, VersionedWorldSemanticCoverage):
            raise TypeError(
                "world floor semantic coverage has wrong type"
            )

    @property
    def semantic_gap(self) -> bool:
        """True means semantics are not recovered, not that the map was empty."""
        return not self.semantic.has_recovered_world_semantics


@dataclass(frozen=True)
class VersionedWorldManifest:
    """Strict cross-domain manifest for stable recovered-later world content."""

    floors: tuple[VersionedWorldFloor, ...]
    topology: HistoricalWorldTopology
    semantic_source_version: str
    coverage_report_ref: str = COVERAGE_REPORT_REF

    def __post_init__(self) -> None:
        floors = tuple(self.floors)
        by_id = {floor.floor_id: floor for floor in floors}
        if len(by_id) != len(floors):
            raise ValueError("versioned world manifest has duplicate floor ids")
        if set(by_id) != set(self.topology.maps):
            raise ValueError(
                "versioned world floors do not match topology map ids"
            )
        source = str(self.semantic_source_version)
        if not source:
            raise ValueError(
                "versioned world manifest requires semantic source version"
            )
        for floor_id, floor in by_id.items():
            definition = self.topology.maps[floor_id]
            if definition.provenance is None:
                raise ValueError(
                    f"topology map {floor_id} lacks structured provenance"
                )
            if definition.floor_id != floor.floor_id:
                raise ValueError("world manifest floor identity drift")
            if definition.width != floor.width:
                raise ValueError("world manifest map width drift")
            if definition.height != floor.height:
                raise ValueError("world manifest map height drift")
            if (
                definition.provenance.payload_sha256
                != floor.map_sha256
            ):
                raise ValueError("world manifest map SHA-256 drift")
            if floor.semantic.source_version != source:
                raise ValueError("world manifest semantic source drift")
            if floor.semantic.evidence_role != LATER_RECOVERED:
                raise ValueError(
                    "world semantics were promoted beyond later evidence"
                )

        object.__setattr__(self, "floors", floors)
        object.__setattr__(self, "semantic_source_version", source)

    @property
    def by_floor(self) -> Mapping[int, VersionedWorldFloor]:
        return MappingProxyType({
            floor.floor_id: floor for floor in self.floors
        })

    @property
    def semantic_gap_floor_ids(self) -> tuple[int, ...]:
        return tuple(
            floor.floor_id for floor in self.floors if floor.semantic_gap
        )

    def count(self, predicate) -> int:
        return sum(1 for floor in self.floors if predicate(floor))


def _kv_fields(line: str, prefix: str) -> dict[str, str]:
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


def parse_world_content_coverage(
    text: str,
) -> tuple[
    str,
    Mapping[int, dict[str, str]],
    Mapping[str, int],
]:
    source_version: str | None = None
    rows: dict[int, dict[str, str]] = {}
    counts: dict[str, int] = {}
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SEMANTIC_SOURCE_VERSION|"):
            parts = line.split("|", 1)
            if source_version is not None:
                raise ValueError(
                    "duplicate SEMANTIC_SOURCE_VERSION record"
                )
            source_version = parts[1]
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed COUNT record: {line}")
            if parts[1] in counts:
                raise ValueError(f"duplicate COUNT record: {parts[1]}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("FLOOR|"):
            fields = _kv_fields(line, "FLOOR")
            required = (
                "id",
                "path",
                "width",
                "height",
                "map_sha256",
                "server_map",
                "npc_create",
                "warp_functionset_create",
                "encounter_rows",
                "active_encounter_rows",
            )
            missing = [name for name in required if name not in fields]
            if missing:
                raise ValueError(
                    f"world coverage floor missing fields: {missing}"
                )
            floor_id = int(fields["id"])
            if floor_id in rows:
                raise ValueError(
                    f"duplicate world coverage floor: {floor_id}"
                )
            rows[floor_id] = fields
            continue
        if line == "RESOLUTION|VERSIONED_WORLD_CONTENT_COVERAGE_CLASSIFIED":
            resolution = True

    if source_version is None:
        raise ValueError("world coverage lacks semantic source version")
    if not resolution:
        raise ValueError("world coverage lacks closed resolution marker")
    if "stable_floor_candidates" not in counts:
        raise ValueError(
            "world coverage lacks stable_floor_candidates count"
        )
    if len(rows) != counts["stable_floor_candidates"]:
        raise ValueError(
            "world coverage floor detail count does not match declaration"
        )
    return source_version, MappingProxyType(rows), MappingProxyType(counts)


def build_versioned_world_manifest(
    *,
    maps: StableLaterMapManifest,
    coverage_text: str,
) -> VersionedWorldManifest:
    """Join stable map provenance to later semantic coverage without promotion."""
    source_version, coverage_rows, counts = (
        parse_world_content_coverage(coverage_text)
    )
    topology = maps.to_topology()
    candidate_by_id = {
        candidate.floor_id: candidate for candidate in maps.candidates
    }
    if set(candidate_by_id) != set(coverage_rows):
        missing = sorted(set(candidate_by_id) - set(coverage_rows))
        extra = sorted(set(coverage_rows) - set(candidate_by_id))
        raise ValueError(
            "world coverage/map lineage floor mismatch; "
            f"missing={missing}, extra={extra}"
        )

    floors: list[VersionedWorldFloor] = []
    for floor_id in sorted(candidate_by_id):
        candidate = candidate_by_id[floor_id]
        row = coverage_rows[floor_id]
        if str(row["path"]).lower() != candidate.path:
            raise ValueError(f"world coverage path drift for floor {floor_id}")
        if int(row["width"]) != candidate.width:
            raise ValueError(f"world coverage width drift for floor {floor_id}")
        if int(row["height"]) != candidate.height:
            raise ValueError(f"world coverage height drift for floor {floor_id}")
        if str(row["map_sha256"]).lower() != candidate.sha256:
            raise ValueError(f"world coverage SHA drift for floor {floor_id}")

        floors.append(
            VersionedWorldFloor(
                floor_id=floor_id,
                path=candidate.path,
                width=candidate.width,
                height=candidate.height,
                map_sha256=candidate.sha256,
                semantic=VersionedWorldSemanticCoverage(
                    source_version=source_version,
                    server_map_present=bool(int(row["server_map"])),
                    npc_create_count=int(row["npc_create"]),
                    warp_functionset_create_count=int(
                        row["warp_functionset_create"]
                    ),
                    encounter_row_count=int(row["encounter_rows"]),
                    active_encounter_row_count=int(
                        row["active_encounter_rows"]
                    ),
                ),
            )
        )

    manifest = VersionedWorldManifest(
        floors=tuple(floors),
        topology=topology,
        semantic_source_version=source_version,
    )

    declared_checks = {
        "stable_with_server_map": manifest.count(
            lambda f: f.semantic.server_map_present
        ),
        "stable_with_npc_semantics": manifest.count(
            lambda f: f.semantic.has_npc_semantics
        ),
        "stable_with_warp_functionset_semantics": manifest.count(
            lambda f: f.semantic.has_warp_semantics
        ),
        "stable_with_encounter_semantics": manifest.count(
            lambda f: f.semantic.has_encounter_semantics
        ),
        "stable_with_npc_and_encounter_semantics": manifest.count(
            lambda f: (
                f.semantic.has_npc_semantics
                and f.semantic.has_encounter_semantics
            )
        ),
        "stable_without_recovered25_world_semantics": len(
            manifest.semantic_gap_floor_ids
        ),
    }
    for name, actual in declared_checks.items():
        if name in counts and int(counts[name]) != actual:
            raise ValueError(
                f"world coverage aggregate drift for {name}: "
                f"declared={counts[name]}, actual={actual}"
            )
    return manifest
