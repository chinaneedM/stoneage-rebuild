#!/usr/bin/env python3
"""Version/provenance-safe world-map library for the StoneAge reconstruction.

This module consumes derived map-lineage metadata only. It never reads or
embeds proprietary map payloads. The complete stable-later manifest is used to
build concrete map definitions whose provenance remains explicitly
LATER_RECOVERED + V1_RESOURCE_COMPATIBLE rather than being promoted to Taiwan
v1 historical membership.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LATER_RECOVERED,
    STABLE_LATER_MAP_CANDIDATE,
    V1_RESOURCE_COMPATIBLE,
    LegacyWarpEdge,
    WorldMapProvenance,
)


LINEAGE_REPORT_REF = (
    "research/recovered/STONEAGE-TW10-FIELDMAP-LINEAGE-R1.txt"
)
RECOVERED_25_VERSION = "recovered25"
ARCHIVED_2003_VERSION = "archived2003"


@dataclass(frozen=True)
class StableLaterMapCandidate:
    path: str
    floor_id: int
    width: int
    height: int
    byte_length: int
    sha256: str
    required_ids: int
    required_cells: int

    def __post_init__(self) -> None:
        path = str(self.path).replace("\\", "/").lower()
        floor_id = int(self.floor_id)
        width = int(self.width)
        height = int(self.height)
        byte_length = int(self.byte_length)
        required_ids = int(self.required_ids)
        required_cells = int(self.required_cells)
        sha256 = str(self.sha256).lower()

        if PurePosixPath(path).suffix != ".dat":
            raise ValueError("stable map candidate path must end in .dat")
        if PurePosixPath(path).stem != str(floor_id):
            raise ValueError(
                "stable map candidate floor_id must match numeric path stem"
            )
        if width <= 0 or height <= 0:
            raise ValueError("stable map candidate dimensions must be positive")
        expected_length = 8 + (width * height * 6)
        if byte_length != expected_length:
            raise ValueError(
                "stable map candidate byte length does not match three-plane DAT"
            )
        if required_ids < 0 or required_cells < 0:
            raise ValueError("stable map candidate resource counts cannot be negative")
        if len(sha256) != 64 or any(
            ch not in "0123456789abcdef" for ch in sha256
        ):
            raise ValueError("stable map candidate sha256 must be 64 hex digits")

        object.__setattr__(self, "path", path)
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "byte_length", byte_length)
        object.__setattr__(self, "sha256", sha256)
        object.__setattr__(self, "required_ids", required_ids)
        object.__setattr__(self, "required_cells", required_cells)

    @property
    def provenance(self) -> WorldMapProvenance:
        return WorldMapProvenance(
            content_role=LATER_RECOVERED,
            resource_role=V1_RESOURCE_COMPATIBLE,
            source_versions=(
                RECOVERED_25_VERSION,
                ARCHIVED_2003_VERSION,
            ),
            evidence_refs=(LINEAGE_REPORT_REF,),
            payload_sha256=self.sha256,
            qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
        )

    def to_map_definition(self) -> HistoricalMapDefinition:
        return HistoricalMapDefinition(
            floor_id=self.floor_id,
            width=self.width,
            height=self.height,
            evidence=STABLE_LATER_MAP_CANDIDATE,
            provenance=self.provenance,
        )


@dataclass(frozen=True)
class ChangedLaterMapRecord:
    path: str
    floor_id: int
    sha_a: str
    sha_b: str
    compatible_a: bool
    compatible_b: bool
    width_a: int
    height_a: int
    width_b: int
    height_b: int

    def __post_init__(self) -> None:
        path = str(self.path).replace("\\", "/").lower()
        floor_id = int(self.floor_id)
        if PurePosixPath(path).suffix != ".dat":
            raise ValueError("changed map path must end in .dat")
        if PurePosixPath(path).stem != str(floor_id):
            raise ValueError("changed map floor_id must match numeric path stem")
        for name in ("sha_a", "sha_b"):
            value = str(getattr(self, name)).lower()
            if len(value) != 64 or any(
                ch not in "0123456789abcdef" for ch in value
            ):
                raise ValueError(f"changed map {name} must be 64 hex digits")
            object.__setattr__(self, name, value)
        for name in ("width_a", "height_a", "width_b", "height_b"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError("changed map dimensions must be positive")
            object.__setattr__(self, name, value)
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "compatible_a", bool(self.compatible_a))
        object.__setattr__(self, "compatible_b", bool(self.compatible_b))


@dataclass(frozen=True)
class StableLaterMapManifest:
    candidates: tuple[StableLaterMapCandidate, ...]
    changed: tuple[ChangedLaterMapRecord, ...]
    shared_path_count: int
    same_sha_count: int
    declared_stable_count: int
    declared_changed_count: int

    def __post_init__(self) -> None:
        candidates = tuple(self.candidates)
        changed = tuple(self.changed)
        floors = [record.floor_id for record in candidates]
        paths = [record.path for record in candidates]
        if len(floors) != len(set(floors)):
            raise ValueError("stable map manifest contains duplicate floor ids")
        if len(paths) != len(set(paths)):
            raise ValueError("stable map manifest contains duplicate paths")
        if len(candidates) != int(self.declared_stable_count):
            raise ValueError(
                "stable map detail count does not match declared stable count"
            )
        if len(changed) != int(self.declared_changed_count):
            raise ValueError(
                "changed map detail count does not match declared changed count"
            )
        if int(self.same_sha_count) < len(candidates):
            raise ValueError("stable-compatible count cannot exceed same-SHA count")
        if int(self.shared_path_count) < int(self.same_sha_count):
            raise ValueError("same-SHA count cannot exceed shared-path count")
        object.__setattr__(self, "candidates", candidates)
        object.__setattr__(self, "changed", changed)
        object.__setattr__(self, "shared_path_count", int(self.shared_path_count))
        object.__setattr__(self, "same_sha_count", int(self.same_sha_count))
        object.__setattr__(
            self,
            "declared_stable_count",
            int(self.declared_stable_count),
        )
        object.__setattr__(
            self,
            "declared_changed_count",
            int(self.declared_changed_count),
        )

    @property
    def maps_by_floor(self) -> Mapping[int, HistoricalMapDefinition]:
        return MappingProxyType({
            candidate.floor_id: candidate.to_map_definition()
            for candidate in self.candidates
        })

    def to_topology(
        self,
        *,
        legacy_warps: Sequence[LegacyWarpEdge] = (),
    ) -> HistoricalWorldTopology:
        """Strict topology containing only provenance-bearing map definitions."""
        return HistoricalWorldTopology.from_provenance_maps(
            self.maps_by_floor,
            legacy_warps=tuple(legacy_warps),
        )


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


def _required(fields: Mapping[str, str], names: Sequence[str]) -> None:
    missing = [name for name in names if name not in fields]
    if missing:
        raise ValueError(f"missing lineage fields: {missing}")


def _floor_id(path: str) -> int:
    normalized = str(path).replace("\\", "/").lower()
    stem = PurePosixPath(normalized).stem
    if not stem.isdigit():
        raise ValueError(f"map path stem is not numeric: {path}")
    return int(stem)


def _dimensions(value: str) -> tuple[int, int]:
    pieces = str(value).lower().split("x", 1)
    if len(pieces) != 2:
        raise ValueError(f"invalid map size: {value}")
    return int(pieces[0]), int(pieces[1])


def parse_stable_later_map_manifest(text: str) -> StableLaterMapManifest:
    """Parse/validate the complete derived lineage report.

    The report must contain one detail row for every declared stable candidate
    and every changed path. A sample-limited report is rejected.
    """
    counts: dict[str, int] = {}
    candidates: list[StableLaterMapCandidate] = []
    changed: list[ChangedLaterMapRecord] = []
    resolution_seen = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed COUNT record: {line}")
            name = parts[1]
            if name in counts:
                raise ValueError(f"duplicate COUNT record: {name}")
            counts[name] = int(parts[2])
            continue
        if line.startswith("STABLE_COMPATIBLE|"):
            fields = _fields(line, "STABLE_COMPATIBLE")
            _required(
                fields,
                (
                    "path",
                    "width",
                    "height",
                    "bytes",
                    "sha256",
                    "required_ids",
                    "required_cells",
                ),
            )
            candidates.append(
                StableLaterMapCandidate(
                    path=fields["path"],
                    floor_id=_floor_id(fields["path"]),
                    width=int(fields["width"]),
                    height=int(fields["height"]),
                    byte_length=int(fields["bytes"]),
                    sha256=fields["sha256"],
                    required_ids=int(fields["required_ids"]),
                    required_cells=int(fields["required_cells"]),
                )
            )
            continue
        if line.startswith("CHANGED|"):
            fields = _fields(line, "CHANGED")
            _required(
                fields,
                (
                    "path",
                    "sha_a",
                    "sha_b",
                    "compat_a",
                    "compat_b",
                    "size_a",
                    "size_b",
                ),
            )
            width_a, height_a = _dimensions(fields["size_a"])
            width_b, height_b = _dimensions(fields["size_b"])
            changed.append(
                ChangedLaterMapRecord(
                    path=fields["path"],
                    floor_id=_floor_id(fields["path"]),
                    sha_a=fields["sha_a"],
                    sha_b=fields["sha_b"],
                    compatible_a=bool(int(fields["compat_a"])),
                    compatible_b=bool(int(fields["compat_b"])),
                    width_a=width_a,
                    height_a=height_a,
                    width_b=width_b,
                    height_b=height_b,
                )
            )
            continue
        if line == "RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED":
            resolution_seen = True

    required_counts = (
        "shared_paths",
        "same_path_same_sha256",
        "same_path_changed_sha256",
        "same_sha256_and_tw1_compatible_both",
    )
    missing_counts = [name for name in required_counts if name not in counts]
    if missing_counts:
        raise ValueError(f"lineage report missing counts: {missing_counts}")
    if not resolution_seen:
        raise ValueError("lineage report lacks closed resolution marker")

    return StableLaterMapManifest(
        candidates=tuple(candidates),
        changed=tuple(changed),
        shared_path_count=counts["shared_paths"],
        same_sha_count=counts["same_path_same_sha256"],
        declared_stable_count=counts[
            "same_sha256_and_tw1_compatible_both"
        ],
        declared_changed_count=counts["same_path_changed_sha256"],
    )
