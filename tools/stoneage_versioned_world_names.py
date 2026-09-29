#!/usr/bin/env python3
"""Provenance-safe recovered map-name semantics for the versioned world.

The recovered 2.5 server specimen exposes short map-header name text for a
subset of the stable-later map corpus. This module binds that text to the
already validated VersionedWorldManifest without treating the text as
Taiwan-v1 membership evidence and without guessing through conflicting rows.

Important boundary:
- this is recovered name text, not a presentation-cleaned display label;
- legacy suffixes such as "|0" are preserved exactly;
- unresolved/conflicting rows remain explicit evidence gaps;
- every bound name remains LATER_RECOVERED.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_versioned_world_manifest import VersionedWorldManifest


MAP_NAMES_REPORT_REF = (
    "research/recovered/STONEAGE-25-STABLE-MAP-NAMES-R1.txt"
)
SEMANTIC_SOURCE_VERSION = "recovered25"
RESOLVED_STATUS = "RESOLVED_BIG5_CP950_CONSENSUS"
RESOLUTION_MARKER = "RESOLUTION|STABLE_SERVER_MAP_NAMES_DECODED"


def _decode_report_text(value: str) -> str:
    """Reverse only the report writer's delimiter-safe percent escaping."""
    text = str(value)
    for encoded, decoded in (
        ("%0D", "\r"),
        ("%0A", "\n"),
        ("%3B", ";"),
        ("%7C", "|"),
        ("%25", "%"),
    ):
        text = text.replace(encoded, decoded)
    return text


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


def _hashes(value: str) -> tuple[str, ...]:
    hashes = tuple(part.lower() for part in str(value).split(",") if part)
    if not hashes:
        raise ValueError("map-name evidence requires at least one raw SHA-256")
    for digest in hashes:
        if len(digest) != 64 or any(
            ch not in "0123456789abcdef" for ch in digest
        ):
            raise ValueError("map-name raw SHA-256 must be 64 hex digits")
    return hashes


@dataclass(frozen=True)
class VersionedWorldRecoveredName:
    """One conflict-free recovered name-text row."""

    floor_id: int
    text: str
    raw_sha256: tuple[str, ...]
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED
    status: str = RESOLVED_STATUS

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        text = str(self.text)
        source_version = str(self.source_version)
        evidence_role = str(self.evidence_role)
        status = str(self.status)
        raw_sha256 = tuple(self.raw_sha256)

        if floor_id < 0:
            raise ValueError("map-name floor id cannot be negative")
        if not text:
            raise ValueError("resolved map-name text cannot be empty")
        if not source_version:
            raise ValueError("map-name evidence requires source_version")
        if evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered map-name evidence must remain LATER_RECOVERED"
            )
        if status != RESOLVED_STATUS:
            raise ValueError("resolved map-name row has unexpected status")
        _hashes(",".join(raw_sha256))

        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "text", text)
        object.__setattr__(self, "raw_sha256", raw_sha256)
        object.__setattr__(self, "source_version", source_version)
        object.__setattr__(self, "evidence_role", evidence_role)
        object.__setattr__(self, "status", status)


@dataclass(frozen=True)
class VersionedWorldUnresolvedName:
    """One recovered name row that must not be selected automatically."""

    floor_id: int
    candidate_texts: tuple[str, ...]
    raw_sha256: tuple[str, ...]
    status: str
    source_version: str = SEMANTIC_SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        candidate_texts = tuple(str(x) for x in self.candidate_texts)
        raw_sha256 = tuple(self.raw_sha256)
        status = str(self.status)
        source_version = str(self.source_version)
        evidence_role = str(self.evidence_role)

        if floor_id < 0:
            raise ValueError("map-name floor id cannot be negative")
        if status == RESOLVED_STATUS or not status:
            raise ValueError("unresolved map-name row has invalid status")
        if not source_version:
            raise ValueError("map-name evidence requires source_version")
        if evidence_role != LATER_RECOVERED:
            raise ValueError(
                "recovered map-name evidence must remain LATER_RECOVERED"
            )
        _hashes(",".join(raw_sha256))

        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "candidate_texts", candidate_texts)
        object.__setattr__(self, "raw_sha256", raw_sha256)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "source_version", source_version)
        object.__setattr__(self, "evidence_role", evidence_role)


@dataclass(frozen=True)
class ParsedVersionedWorldNames:
    source_version: str
    evidence_role: str
    resolved: tuple[VersionedWorldRecoveredName, ...]
    unresolved: tuple[VersionedWorldUnresolvedName, ...]
    counts: Mapping[str, int]

    def __post_init__(self) -> None:
        source_version = str(self.source_version)
        evidence_role = str(self.evidence_role)
        resolved = tuple(self.resolved)
        unresolved = tuple(self.unresolved)
        counts = dict(self.counts)

        if not source_version:
            raise ValueError("map-name report requires source version")
        if evidence_role != LATER_RECOVERED:
            raise ValueError("map-name report must remain LATER_RECOVERED")

        floor_ids = [row.floor_id for row in resolved]
        floor_ids.extend(row.floor_id for row in unresolved)
        if len(floor_ids) != len(set(floor_ids)):
            raise ValueError("map-name report contains duplicate floor ids")

        object.__setattr__(self, "source_version", source_version)
        object.__setattr__(self, "evidence_role", evidence_role)
        object.__setattr__(self, "resolved", resolved)
        object.__setattr__(self, "unresolved", unresolved)
        object.__setattr__(self, "counts", MappingProxyType(counts))

    @property
    def resolved_by_floor(self) -> Mapping[int, VersionedWorldRecoveredName]:
        return MappingProxyType({row.floor_id: row for row in self.resolved})

    @property
    def unresolved_by_floor(self) -> Mapping[int, VersionedWorldUnresolvedName]:
        return MappingProxyType({row.floor_id: row for row in self.unresolved})

    @property
    def evidence_floor_ids(self) -> frozenset[int]:
        return frozenset(
            tuple(row.floor_id for row in self.resolved)
            + tuple(row.floor_id for row in self.unresolved)
        )


@dataclass(frozen=True)
class VersionedWorldNameOverlay:
    """Validated name-evidence overlay for one versioned world manifest."""

    world: VersionedWorldManifest
    evidence: ParsedVersionedWorldNames
    report_ref: str = MAP_NAMES_REPORT_REF

    def __post_init__(self) -> None:
        if not isinstance(self.world, VersionedWorldManifest):
            raise TypeError("world-name overlay requires VersionedWorldManifest")
        if not isinstance(self.evidence, ParsedVersionedWorldNames):
            raise TypeError("world-name overlay requires parsed name evidence")
        if self.evidence.source_version != self.world.semantic_source_version:
            raise ValueError("map-name/world semantic source version drift")

        world_ids = set(self.world.by_floor)
        evidence_ids = set(self.evidence.evidence_floor_ids)
        unknown = sorted(evidence_ids - world_ids)
        if unknown:
            raise ValueError(
                f"map-name evidence references unknown floors: {unknown}"
            )

        declared = self.evidence.counts.get("stable_floor_candidates")
        if declared is None or int(declared) != len(world_ids):
            raise ValueError(
                "map-name stable floor count does not match world manifest"
            )

        server_map_ids = {
            floor.floor_id
            for floor in self.world.floors
            if floor.semantic.server_map_present
        }
        if evidence_ids != server_map_ids:
            missing = sorted(server_map_ids - evidence_ids)
            extra = sorted(evidence_ids - server_map_ids)
            raise ValueError(
                "map-name/server-map floor mismatch; "
                f"missing={missing}, extra={extra}"
            )

        object.__setattr__(self, "report_ref", str(self.report_ref))

    @property
    def by_floor(self) -> Mapping[int, VersionedWorldRecoveredName]:
        """Conflict-free recovered name text only."""
        return self.evidence.resolved_by_floor

    @property
    def unresolved_by_floor(self) -> Mapping[int, VersionedWorldUnresolvedName]:
        return self.evidence.unresolved_by_floor

    @property
    def no_name_evidence_floor_ids(self) -> tuple[int, ...]:
        evidence_ids = set(self.evidence.evidence_floor_ids)
        return tuple(
            floor_id
            for floor_id in sorted(self.world.by_floor)
            if floor_id not in evidence_ids
        )

    @property
    def without_resolved_name_floor_ids(self) -> tuple[int, ...]:
        resolved_ids = set(self.by_floor)
        return tuple(
            floor_id
            for floor_id in sorted(self.world.by_floor)
            if floor_id not in resolved_ids
        )

    def recovered_text(self, floor_id: int) -> str | None:
        row = self.by_floor.get(int(floor_id))
        return None if row is None else row.text


def parse_versioned_world_names(text: str) -> ParsedVersionedWorldNames:
    source_version: str | None = None
    evidence_role: str | None = None
    counts: dict[str, int] = {}
    resolved: list[VersionedWorldRecoveredName] = []
    unresolved: list[VersionedWorldUnresolvedName] = []
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SEMANTIC_SOURCE_VERSION|"):
            if source_version is not None:
                raise ValueError("duplicate map-name source version")
            source_version = line.split("|", 1)[1]
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            if evidence_role is not None:
                raise ValueError("duplicate map-name evidence role")
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed map-name COUNT record: {line}")
            if parts[1] in counts:
                raise ValueError(
                    f"duplicate map-name COUNT record: {parts[1]}"
                )
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("MAP_NAME|"):
            fields = _fields(line, "MAP_NAME")
            for required in ("floor", "name", "raw_sha256", "status"):
                if required not in fields:
                    raise ValueError(f"map-name row missing {required}")
            resolved.append(
                VersionedWorldRecoveredName(
                    floor_id=int(fields["floor"]),
                    text=_decode_report_text(fields["name"]),
                    raw_sha256=_hashes(fields["raw_sha256"]),
                    source_version=source_version or SEMANTIC_SOURCE_VERSION,
                    evidence_role=evidence_role or LATER_RECOVERED,
                    status=fields["status"],
                )
            )
            continue
        if line.startswith("MAP_NAME_UNRESOLVED|"):
            fields = _fields(line, "MAP_NAME_UNRESOLVED")
            for required in (
                "floor",
                "candidate_count",
                "candidates",
                "raw_sha256",
                "status",
            ):
                if required not in fields:
                    raise ValueError(
                        f"unresolved map-name row missing {required}"
                    )
            candidates = tuple(
                _decode_report_text(part)
                for part in fields["candidates"].split(";")
                if part
            )
            if len(candidates) != int(fields["candidate_count"]):
                raise ValueError("map-name candidate count drift")
            unresolved.append(
                VersionedWorldUnresolvedName(
                    floor_id=int(fields["floor"]),
                    candidate_texts=candidates,
                    raw_sha256=_hashes(fields["raw_sha256"]),
                    status=fields["status"],
                    source_version=source_version or SEMANTIC_SOURCE_VERSION,
                    evidence_role=evidence_role or LATER_RECOVERED,
                )
            )
            continue
        if line == RESOLUTION_MARKER:
            resolution = True

    if source_version is None:
        raise ValueError("map-name report lacks semantic source version")
    if evidence_role is None:
        raise ValueError("map-name report lacks evidence role")
    if evidence_role != LATER_RECOVERED:
        raise ValueError("map-name report must remain LATER_RECOVERED")
    if not resolution:
        raise ValueError("map-name report lacks closed resolution marker")

    required_counts = (
        "stable_floor_candidates",
        "stable_with_dimension_matched_server_name",
        "stable_without_dimension_matched_server_name",
        f"status:{RESOLVED_STATUS}",
    )
    missing_counts = [key for key in required_counts if key not in counts]
    if missing_counts:
        raise ValueError(f"map-name report lacks counts: {missing_counts}")

    matched = len(resolved) + len(unresolved)
    if matched != counts["stable_with_dimension_matched_server_name"]:
        raise ValueError(
            "map-name detail count does not match matched-name count"
        )
    if len(resolved) != counts[f"status:{RESOLVED_STATUS}"]:
        raise ValueError("resolved map-name detail count drift")
    if (
        counts["stable_floor_candidates"]
        - counts["stable_with_dimension_matched_server_name"]
        != counts["stable_without_dimension_matched_server_name"]
    ):
        raise ValueError("map-name matched/missing aggregate drift")

    status_counts: dict[str, int] = {}
    for row in resolved:
        status_counts[row.status] = status_counts.get(row.status, 0) + 1
    for row in unresolved:
        status_counts[row.status] = status_counts.get(row.status, 0) + 1
    for status, actual in status_counts.items():
        declared = counts.get(f"status:{status}")
        if declared is not None and int(declared) != actual:
            raise ValueError(f"map-name status count drift for {status}")

    return ParsedVersionedWorldNames(
        source_version=source_version,
        evidence_role=evidence_role,
        resolved=tuple(resolved),
        unresolved=tuple(unresolved),
        counts=counts,
    )


def bind_versioned_world_names(
    *,
    world: VersionedWorldManifest,
    names_text: str,
) -> VersionedWorldNameOverlay:
    """Bind recovered name evidence to a validated versioned world."""
    return VersionedWorldNameOverlay(
        world=world,
        evidence=parse_versioned_world_names(names_text),
    )
