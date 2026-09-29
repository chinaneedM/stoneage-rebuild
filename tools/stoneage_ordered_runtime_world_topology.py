#!/usr/bin/env python3
"""Apply recovered create-order arbitration to strict materializable Warp sources.

The base strict topology intentionally excludes all multi-destination source
cells. A separate recovered25 audit proves whether candidates at each source
reside in the same create file and, when they do, which placement is created
first.

Pinned descendant controls establish the relevant runtime ordering semantics:
- map objects are appended to a cell's linked-list tail;
- overlap dispatch scans from the list head and stops at the first matching
  event object;
- NPC generation processes create indices in ascending order.

Therefore a SAME_FILE_ORDERED source may activate exactly its first placement.
Later candidates remain structured shadowed evidence. Cross-file groups, if any
appear in future evidence, remain unresolved and inactive because recursive
file discovery is unsorted readdir().
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_materializable_world_topology import (
    AmbiguousWarpSource,
    MaterializableRuntimeTopology,
    RecoveredWarpGeometryRecord,
    load_materializable_runtime_topology,
)
from tools.stoneage_singleplayer_domain import MapPosition
from tools.stoneage_singleplayer_world import (
    HistoricalWorldTopology,
    LegacyWarpEdge,
)


CREATE_ORDER_REPORT_REF = (
    "research/recovered/STONEAGE-25-AMBIGUOUS-WARP-CREATE-ORDER-R1.txt"
)
CREATE_ORDER_RESOLUTION = (
    "RESOLUTION|AMBIGUOUS_WARP_CREATE_ORDER_CLASSIFIED"
)

SAME_FILE_ORDERED = "SAME_FILE_ORDERED"
CROSS_FILE_UNORDERED = "CROSS_FILE_UNORDERED"


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


def _point(value: str) -> MapPosition:
    parts = tuple(int(v) for v in str(value).split(","))
    if len(parts) != 3:
        raise ValueError(f"invalid map point: {value}")
    return MapPosition(parts[0], parts[1], parts[2])


@dataclass(frozen=True)
class CreateOrderCandidate:
    placement_id: int
    source: MapPosition
    destination: MapPosition
    create_path: str
    block_ordinal: int
    create_num: int
    respawn_time: int

    def __post_init__(self) -> None:
        placement_id = int(self.placement_id)
        block_ordinal = int(self.block_ordinal)
        if placement_id < 0:
            raise ValueError("placement id cannot be negative")
        if block_ordinal <= 0:
            raise ValueError("create block ordinal must be positive")
        if not str(self.create_path):
            raise ValueError("create-order candidate requires file path")
        object.__setattr__(self, "placement_id", placement_id)
        object.__setattr__(self, "block_ordinal", block_ordinal)
        object.__setattr__(self, "create_num", int(self.create_num))
        object.__setattr__(self, "respawn_time", int(self.respawn_time))


@dataclass(frozen=True)
class CreateOrderSource:
    source: MapPosition
    classification: str
    first_placement_id: int | None
    candidates: tuple[CreateOrderCandidate, ...]

    def __post_init__(self) -> None:
        rows = tuple(self.candidates)
        if len(rows) < 2:
            raise ValueError("create-order source requires multiple candidates")
        if any(row.source != self.source for row in rows):
            raise ValueError("create-order candidate source drift")
        if len({row.placement_id for row in rows}) != len(rows):
            raise ValueError("duplicate placement id in create-order source")
        if self.classification == SAME_FILE_ORDERED:
            if len({row.create_path for row in rows}) != 1:
                raise ValueError("same-file source contains multiple create files")
            if self.first_placement_id is None:
                raise ValueError("same-file source requires first placement")
            if self.first_placement_id not in {row.placement_id for row in rows}:
                raise ValueError("first placement not present in candidate set")
            first = min(rows, key=lambda row: row.block_ordinal)
            if first.placement_id != self.first_placement_id:
                raise ValueError("first placement disagrees with block order")
        elif self.classification == CROSS_FILE_UNORDERED:
            if len({row.create_path for row in rows}) < 2:
                raise ValueError("cross-file source contains one create file")
            if self.first_placement_id is not None:
                raise ValueError("cross-file source cannot select first placement")
        else:
            raise ValueError("unknown create-order classification")
        object.__setattr__(self, "candidates", rows)

    @property
    def by_placement(self) -> Mapping[int, CreateOrderCandidate]:
        return MappingProxyType({
            row.placement_id: row for row in self.candidates
        })


@dataclass(frozen=True)
class ParsedCreateOrderAudit:
    sources: tuple[CreateOrderSource, ...]
    counts: Mapping[str, int]

    def __post_init__(self) -> None:
        rows = tuple(self.sources)
        counts = dict(self.counts)
        if len({row.source for row in rows}) != len(rows):
            raise ValueError("duplicate source in create-order audit")
        if counts.get("ambiguous_sources") != len(rows):
            raise ValueError("create-order source count drift")
        if counts.get("ambiguous_candidate_records") != sum(
            len(row.candidates) for row in rows
        ):
            raise ValueError("create-order candidate count drift")
        if counts.get("same_file_ordered_sources") != sum(
            row.classification == SAME_FILE_ORDERED for row in rows
        ):
            raise ValueError("same-file create-order aggregate drift")
        if counts.get("cross_file_unordered_sources") != sum(
            row.classification == CROSS_FILE_UNORDERED for row in rows
        ):
            raise ValueError("cross-file create-order aggregate drift")
        object.__setattr__(self, "sources", rows)
        object.__setattr__(self, "counts", MappingProxyType(counts))

    @property
    def by_source(self) -> Mapping[MapPosition, CreateOrderSource]:
        return MappingProxyType({row.source: row for row in self.sources})


def parse_create_order_audit(text: str) -> ParsedCreateOrderAudit:
    counts: dict[str, int] = {}
    source_rows: dict[MapPosition, dict[str, object]] = {}
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed create-order COUNT: {line}")
            if parts[1] in counts:
                raise ValueError(f"duplicate create-order COUNT: {parts[1]}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("AMBIGUOUS_SOURCE_ORDER|"):
            fields = _fields(line, "AMBIGUOUS_SOURCE_ORDER")
            source = _point(fields["source"])
            if source in source_rows:
                raise ValueError("duplicate create-order source row")
            first = fields["first_placement"]
            source_rows[source] = {
                "classification": fields["classification"],
                "first": None if first == "NONE" else int(first),
                "candidates": [],
            }
            continue
        if line.startswith("AMBIGUOUS_CANDIDATE_ORDER|"):
            fields = _fields(line, "AMBIGUOUS_CANDIDATE_ORDER")
            source = _point(fields["source"])
            if source not in source_rows:
                raise ValueError("candidate precedes create-order source row")
            source_rows[source]["candidates"].append(
                CreateOrderCandidate(
                    placement_id=int(fields["placement"]),
                    source=source,
                    destination=_point(fields["destination"]),
                    create_path=fields["create_path"],
                    block_ordinal=int(fields["block_ordinal"]),
                    create_num=int(fields["create_num"]),
                    respawn_time=int(fields["respawn_time"]),
                )
            )
            continue
        if line == CREATE_ORDER_RESOLUTION:
            resolution = True

    if not resolution:
        raise ValueError("create-order audit lacks closed resolution marker")

    rows = tuple(
        CreateOrderSource(
            source=source,
            classification=str(data["classification"]),
            first_placement_id=data["first"],
            candidates=tuple(data["candidates"]),
        )
        for source, data in sorted(
            source_rows.items(),
            key=lambda item: (
                item[0].floor_id,
                item[0].x,
                item[0].y,
            ),
        )
    )
    return ParsedCreateOrderAudit(sources=rows, counts=counts)


@dataclass(frozen=True)
class OrderedWarpResolution:
    source: MapPosition
    selected: RecoveredWarpGeometryRecord
    shadowed: tuple[RecoveredWarpGeometryRecord, ...]
    create_path: str
    selected_block_ordinal: int

    def __post_init__(self) -> None:
        shadowed = tuple(self.shadowed)
        if self.selected.source != self.source:
            raise ValueError("selected Warp source drift")
        if any(row.source != self.source for row in shadowed):
            raise ValueError("shadowed Warp source drift")
        if self.selected.placement_id in {
            row.placement_id for row in shadowed
        }:
            raise ValueError("selected placement leaked into shadowed candidates")
        if not shadowed:
            raise ValueError("ordered resolution must preserve shadowed candidates")
        object.__setattr__(self, "shadowed", shadowed)


@dataclass(frozen=True)
class OrderedMaterializableRuntimeTopology:
    base: MaterializableRuntimeTopology
    topology: HistoricalWorldTopology
    ordered_resolutions: tuple[OrderedWarpResolution, ...]
    unresolved_cross_file_sources: tuple[AmbiguousWarpSource, ...]

    def __post_init__(self) -> None:
        if set(self.topology.maps) != set(self.base.topology.maps):
            raise ValueError("ordered runtime topology map set drift")
        active_sources = [edge.source for edge in self.topology.legacy_warps]
        if len(active_sources) != len(set(active_sources)):
            raise ValueError("ordered runtime topology contains duplicate sources")
        if any(edge.time_token is not None for edge in self.topology.legacy_warps):
            raise ValueError("ordered active Warp unexpectedly has time token")
        if any(not edge.active for edge in self.topology.legacy_warps):
            raise ValueError("ordered runtime topology must contain active edges only")
        object.__setattr__(
            self,
            "ordered_resolutions",
            tuple(self.ordered_resolutions),
        )
        object.__setattr__(
            self,
            "unresolved_cross_file_sources",
            tuple(self.unresolved_cross_file_sources),
        )

    @property
    def resolution_by_source(self) -> Mapping[MapPosition, OrderedWarpResolution]:
        return MappingProxyType({
            row.source: row for row in self.ordered_resolutions
        })

    @property
    def shadowed_candidate_records(self) -> int:
        return sum(len(row.shadowed) for row in self.ordered_resolutions)


def _geometry_by_placement(
    source: AmbiguousWarpSource,
) -> Mapping[int, RecoveredWarpGeometryRecord]:
    rows = {}
    for row in source.candidates:
        if row.placement_id in rows:
            raise ValueError("duplicate placement in ambiguous geometry source")
        rows[row.placement_id] = row
    return MappingProxyType(rows)


def apply_create_order_arbitration(
    *,
    runtime: MaterializableRuntimeTopology,
    create_order_text: str,
) -> OrderedMaterializableRuntimeTopology:
    audit = parse_create_order_audit(create_order_text)
    audit_by_source = audit.by_source
    base_by_source = runtime.ambiguous_by_source

    if set(audit_by_source) != set(base_by_source):
        missing = sorted(
            set(base_by_source) - set(audit_by_source),
            key=lambda pos: (pos.floor_id, pos.x, pos.y),
        )
        extra = sorted(
            set(audit_by_source) - set(base_by_source),
            key=lambda pos: (pos.floor_id, pos.x, pos.y),
        )
        raise ValueError(
            "create-order/topology ambiguous source-set drift; "
            f"missing={missing}, extra={extra}"
        )

    active = list(runtime.topology.legacy_warps)
    ordered: list[OrderedWarpResolution] = []
    unresolved: list[AmbiguousWarpSource] = []

    for source in sorted(
        base_by_source,
        key=lambda pos: (pos.floor_id, pos.x, pos.y),
    ):
        ambiguous = base_by_source[source]
        order = audit_by_source[source]
        geometry = _geometry_by_placement(ambiguous)

        if set(geometry) != set(order.by_placement):
            raise ValueError(
                f"create-order candidate-set drift at source {source}"
            )
        for placement_id, geometry_row in geometry.items():
            order_row = order.by_placement[placement_id]
            if order_row.source != geometry_row.source:
                raise ValueError("create-order source drift")
            if order_row.destination != geometry_row.destination:
                raise ValueError("create-order destination drift")

        if order.classification == CROSS_FILE_UNORDERED:
            unresolved.append(ambiguous)
            continue

        if order.classification != SAME_FILE_ORDERED:
            raise ValueError("unsupported create-order classification")
        if order.first_placement_id is None:
            raise ValueError("ordered source lacks first placement")

        selected = geometry[order.first_placement_id]
        selected_order = order.by_placement[order.first_placement_id]
        shadowed = tuple(
            row
            for placement_id, row in sorted(geometry.items())
            if placement_id != order.first_placement_id
        )
        ordered.append(
            OrderedWarpResolution(
                source=source,
                selected=selected,
                shadowed=shadowed,
                create_path=selected_order.create_path,
                selected_block_ordinal=selected_order.block_ordinal,
            )
        )
        active.append(
            LegacyWarpEdge(
                source=selected.source,
                destination=selected.destination,
                time_token=None,
                active=True,
            )
        )

    topology = HistoricalWorldTopology.from_provenance_maps(
        runtime.topology.maps,
        legacy_warps=tuple(active),
    )
    return OrderedMaterializableRuntimeTopology(
        base=runtime,
        topology=topology,
        ordered_resolutions=tuple(ordered),
        unresolved_cross_file_sources=tuple(unresolved),
    )


def load_ordered_materializable_runtime_topology(
) -> OrderedMaterializableRuntimeTopology:
    return apply_create_order_arbitration(
        runtime=load_materializable_runtime_topology(),
        create_order_text=Path(CREATE_ORDER_REPORT_REF).read_text(
            encoding="utf-8"
        ),
    )
