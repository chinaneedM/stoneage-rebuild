#!/usr/bin/env python3
"""Engine-neutral map delivery/materialization policy.

The accepted Taiwan-v1 runtime proves that ordinary field-map data may be
materialized into a local map cache at runtime through the M/MC protocol.
The pinned descendant source is used only as a control for the server-side
shape of that exchange.

This module deliberately models the semantic boundary rather than sockets or
legacy packet encoding. Concrete later recovered map content keeps its own
provenance and is never promoted to Taiwan-v1 membership by this mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import LATER_RECOVERED


TW1_RUNTIME_CACHE_DIRECT = "TW1_RUNTIME_CACHE_DIRECT"
DESCENDANT_SERVER_CONTROL = "DESCENDANT_SERVER_CONTROL"

CACHE_ACCEPT = "CACHE_ACCEPT"
REQUEST_MAP_RECT = "REQUEST_MAP_RECT"
MATERIALIZE_MAP_RECT = "MATERIALIZE_MAP_RECT"

SERVER_AUTHORITY_INTERNAL_MAP = "SERVER_AUTHORITY_INTERNAL_MAP"
NO_HISTORICAL_CLIENT_FILE_ASSERTION = "NO_HISTORICAL_CLIENT_FILE_ASSERTION"

SOURCE_VERSION = "recovered25"
REPORT_RESOLUTION = "RESOLUTION|MISSING_DAT_WARP_DESTINATION_PAYLOADS_CLASSIFIED"


@dataclass(frozen=True)
class MapRectangle:
    floor_id: int
    x1: int
    y1: int
    x2: int
    y2: int

    def __post_init__(self) -> None:
        values = (
            int(self.floor_id),
            int(self.x1),
            int(self.y1),
            int(self.x2),
            int(self.y2),
        )
        if values[0] < 0:
            raise ValueError("map floor id cannot be negative")
        if values[3] < values[1] or values[4] < values[2]:
            raise ValueError("map rectangle endpoints are reversed")
        object.__setattr__(self, "floor_id", values[0])
        object.__setattr__(self, "x1", values[1])
        object.__setattr__(self, "y1", values[2])
        object.__setattr__(self, "x2", values[3])
        object.__setattr__(self, "y2", values[4])

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1


@dataclass(frozen=True)
class MapDeliveryDecision:
    action: str
    rectangle: MapRectangle
    historical_basis: str


def receive_map_check(
    *,
    rectangle: MapRectangle,
    cache_checksum_matches: bool,
) -> MapDeliveryDecision:
    """Model the v1-direct MC client boundary.

    A checksum match accepts the local cache. A mismatch requests the same
    rectangle through the client-to-server M shape.
    """
    if bool(cache_checksum_matches):
        return MapDeliveryDecision(
            action=CACHE_ACCEPT,
            rectangle=rectangle,
            historical_basis=TW1_RUNTIME_CACHE_DIRECT,
        )
    return MapDeliveryDecision(
        action=REQUEST_MAP_RECT,
        rectangle=rectangle,
        historical_basis=TW1_RUNTIME_CACHE_DIRECT,
    )


def receive_map_payload(*, rectangle: MapRectangle) -> MapDeliveryDecision:
    """Model the v1-direct M receive boundary: write/materialize the rectangle."""
    return MapDeliveryDecision(
        action=MATERIALIZE_MAP_RECT,
        rectangle=rectangle,
        historical_basis=TW1_RUNTIME_CACHE_DIRECT,
    )


@dataclass(frozen=True)
class ServerOnlyFloorEvidence:
    floor_id: int
    edge_refs: int
    server_path: str
    width: int
    height: int
    source_version: str = SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        edge_refs = int(self.edge_refs)
        width = int(self.width)
        height = int(self.height)
        server_path = str(self.server_path)
        source_version = str(self.source_version)
        evidence_role = str(self.evidence_role)
        if floor_id < 0:
            raise ValueError("server-only floor id cannot be negative")
        if edge_refs <= 0:
            raise ValueError("server-only floor must have a warp reference")
        if not server_path:
            raise ValueError("server-only floor requires a server path")
        if width <= 0 or height <= 0:
            raise ValueError("server-only floor dimensions must be positive")
        if source_version != SOURCE_VERSION:
            raise ValueError("server-only materialization currently binds recovered25")
        if evidence_role != LATER_RECOVERED:
            raise ValueError("server-only evidence must remain LATER_RECOVERED")
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "edge_refs", edge_refs)
        object.__setattr__(self, "server_path", server_path)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "source_version", source_version)
        object.__setattr__(self, "evidence_role", evidence_role)


@dataclass(frozen=True)
class RuntimeMapMaterializationPlan:
    floor_id: int
    width: int
    height: int
    source_version: str
    evidence_role: str
    runtime_authority: str
    historical_client_file_claim: str
    network_required: bool
    legacy_cache_file_required: bool
    source_ref: str

    def __post_init__(self) -> None:
        if self.runtime_authority != SERVER_AUTHORITY_INTERNAL_MAP:
            raise ValueError("unexpected map materialization authority")
        if self.historical_client_file_claim != NO_HISTORICAL_CLIENT_FILE_ASSERTION:
            raise ValueError("must not fabricate a historical client-file claim")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("materialized later map cannot be promoted to Taiwan v1")
        if bool(self.network_required):
            raise ValueError("single-player materialization must not require networking")
        if bool(self.legacy_cache_file_required):
            raise ValueError("modern runtime must not require a legacy cache file")


@dataclass(frozen=True)
class ParsedServerOnlyPayloadReport:
    rows: tuple[ServerOnlyFloorEvidence, ...]
    counts: Mapping[str, int]

    def __post_init__(self) -> None:
        rows = tuple(self.rows)
        counts = dict(self.counts)
        ids = [row.floor_id for row in rows]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate server-only floor id")
        if counts.get("missing_dat_destination_ids") != len(rows):
            raise ValueError("server-only report id count drift")
        if counts.get("missing_dat_edges") != sum(row.edge_refs for row in rows):
            raise ValueError("server-only report edge count drift")
        if counts.get("status:SERVER_MAP_ONLY:ids") != len(rows):
            raise ValueError("server-only status id count drift")
        if counts.get("client_map_present:1:ids", 0) != 0:
            raise ValueError("server-only report unexpectedly has client MAP payloads")
        if counts.get("server_map_present:1:ids") != len(rows):
            raise ValueError("server-only report lacks server LS2MAP payloads")
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "counts", MappingProxyType(counts))


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


def _parse_single_dimension(value: str) -> tuple[int, int]:
    parts = tuple(part for part in str(value).split(",") if part)
    if len(parts) != 1 or "x" not in parts[0]:
        raise ValueError("server-only floor requires exactly one server dimension")
    width, height = parts[0].split("x", 1)
    return int(width), int(height)


def parse_server_only_payload_report(text: str) -> ParsedServerOnlyPayloadReport:
    counts: dict[str, int] = {}
    rows: list[ServerOnlyFloorEvidence] = []
    evidence_role: str | None = None
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            if evidence_role is not None:
                raise ValueError("duplicate evidence role")
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed COUNT row: {line}")
            if parts[1] in counts:
                raise ValueError(f"duplicate COUNT key: {parts[1]}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("MISSING_DAT_DESTINATION|"):
            fields = _fields(line, "MISSING_DAT_DESTINATION")
            if fields.get("status") != "SERVER_MAP_ONLY":
                raise ValueError(
                    "materialization input must contain only SERVER_MAP_ONLY rows"
                )
            if fields.get("client_map_paths"):
                raise ValueError("server-only row unexpectedly has client MAP path")
            server_paths = tuple(
                path for path in fields.get("server_map_paths", "").split(",")
                if path
            )
            if len(server_paths) != 1:
                raise ValueError("server-only floor requires exactly one server path")
            width, height = _parse_single_dimension(
                fields.get("server_map_dimensions", "")
            )
            rows.append(
                ServerOnlyFloorEvidence(
                    floor_id=int(fields["floor"]),
                    edge_refs=int(fields["edge_refs"]),
                    server_path=server_paths[0],
                    width=width,
                    height=height,
                    evidence_role=evidence_role or LATER_RECOVERED,
                )
            )
            continue
        if line == REPORT_RESOLUTION:
            resolution = True

    if evidence_role != LATER_RECOVERED:
        raise ValueError("server-only report must remain LATER_RECOVERED")
    if not resolution:
        raise ValueError("server-only report lacks closed resolution marker")
    return ParsedServerOnlyPayloadReport(rows=tuple(rows), counts=counts)


def build_singleplayer_materialization_plans(
    report: ParsedServerOnlyPayloadReport,
    *,
    source_ref: str,
) -> tuple[RuntimeMapMaterializationPlan, ...]:
    """Create provenance-safe plans without fabricating legacy client artifacts."""
    if not str(source_ref).strip():
        raise ValueError("materialization plan requires an evidence reference")
    return tuple(
        RuntimeMapMaterializationPlan(
            floor_id=row.floor_id,
            width=row.width,
            height=row.height,
            source_version=row.source_version,
            evidence_role=row.evidence_role,
            runtime_authority=SERVER_AUTHORITY_INTERNAL_MAP,
            historical_client_file_claim=NO_HISTORICAL_CLIENT_FILE_ASSERTION,
            network_required=False,
            legacy_cache_file_required=False,
            source_ref=str(source_ref),
        )
        for row in report.rows
    )
