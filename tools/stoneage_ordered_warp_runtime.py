#!/usr/bin/env python3
"""Create-order-resolved runtime topology for recovered25 classic Warps.

The strict materializable topology intentionally leaves multi-destination source
cells inactive. The recovered create-order audit can resolve a subset only when
all competing definitions occur in the same create file. Pinned descendant
control establishes the ordering contract:
- create-file blocks are loaded in file order;
- startup NPC generation walks create indices ascending;
- map objects are appended to the cell linked-list tail;
- overlap-event dispatch walks from the head and stops at first match.

Cross-file candidates remain unresolved because recursive create-file discovery
uses unsorted readdir(). This module never invents an ordering across files.
"""

from __future__ import annotations

import collections
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


def _position(value: str) -> MapPosition:
    parts = tuple(int(v) for v in str(value).split(","))
    if len(parts) != 3:
        raise ValueError(f"invalid source position: {value}")
    return MapPosition(parts[0], parts[1], parts[2])


@dataclass(frozen=True)
class CreateOrderSourceRecord:
    source: MapPosition
    classification: str
    first_placement_id: int | None


def parse_create_order_sources(
    text: str,
) -> Mapping[MapPosition, CreateOrderSourceRecord]:
    source_version: str | None = None
    evidence_role: str | None = None
    declared_sources: int | None = None
    rows: dict[MapPosition, CreateOrderSourceRecord] = {}
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
        if line.startswith("COUNT|ambiguous_sources|"):
            declared_sources = int(line.rsplit("|", 1)[1])
            continue
        if line.startswith("AMBIGUOUS_SOURCE_ORDER|"):
            fields = _fields(line, "AMBIGUOUS_SOURCE_ORDER")
            source = _position(fields["source"])
            if source in rows:
                raise ValueError(f"duplicate create-order source: {source}")
            first_raw = fields["first_placement"]
            rows[source] = CreateOrderSourceRecord(
                source=source,
                classification=fields["classification"],
                first_placement_id=(
                    None if first_raw == "NONE" else int(first_raw)
                ),
            )
            continue
        if line == CREATE_ORDER_RESOLUTION:
            resolution = True

    if source_version != "recovered25":
        raise ValueError("create-order source-version drift")
    if evidence_role != "LATER_RECOVERED":
        raise ValueError("create-order evidence-role drift")
    if not resolution:
        raise ValueError("create-order report is not closed")
    if declared_sources is None or declared_sources != len(rows):
        raise ValueError("create-order ambiguous-source count drift")
    return MappingProxyType(rows)


@dataclass(frozen=True)
class OrderedAmbiguousWarpResolution:
    source: MapPosition
    selected: RecoveredWarpGeometryRecord
    shadowed: tuple[RecoveredWarpGeometryRecord, ...]

    def __post_init__(self) -> None:
        if self.selected.source != self.source:
            raise ValueError("ordered selected Warp source drift")
        shadowed = tuple(self.shadowed)
        if not shadowed:
            raise ValueError("ordered resolution requires shadowed candidates")
        if any(row.source != self.source for row in shadowed):
            raise ValueError("ordered shadowed Warp source drift")
        if self.selected in shadowed:
            raise ValueError("selected Warp also appears as shadowed")
        object.__setattr__(self, "shadowed", shadowed)


@dataclass(frozen=True)
class OrderedMaterializableRuntime:
    strict_runtime: MaterializableRuntimeTopology
    topology: HistoricalWorldTopology
    ordered_resolutions: tuple[OrderedAmbiguousWarpResolution, ...]
    unresolved_ambiguous_sources: tuple[AmbiguousWarpSource, ...]

    def __post_init__(self) -> None:
        if set(self.topology.maps) != set(self.strict_runtime.topology.maps):
            raise ValueError("ordered runtime map-set drift")
        active_sources = [edge.source for edge in self.topology.legacy_warps]
        if len(active_sources) != len(set(active_sources)):
            raise ValueError("ordered runtime contains duplicate active Warp source")
        ordered = tuple(self.ordered_resolutions)
        unresolved = tuple(self.unresolved_ambiguous_sources)
        if {
            row.source for row in ordered
        } & {
            row.source for row in unresolved
        }:
            raise ValueError("ambiguous source both ordered and unresolved")
        object.__setattr__(self, "ordered_resolutions", ordered)
        object.__setattr__(self, "unresolved_ambiguous_sources", unresolved)

    @property
    def ordered_by_source(
        self,
    ) -> Mapping[MapPosition, OrderedAmbiguousWarpResolution]:
        return MappingProxyType({
            row.source: row for row in self.ordered_resolutions
        })

    @property
    def stable_floor_ids(self) -> frozenset[int]:
        return frozenset(self.strict_runtime.extension.stable_world.by_floor)

    @property
    def resolved_supplemental_floor_ids(self) -> frozenset[int]:
        return frozenset(self.strict_runtime.extension.resolved_by_floor)

    @property
    def reachable_floor_ids(self) -> frozenset[int]:
        adjacency: dict[int, list[int]] = collections.defaultdict(list)
        for edge in self.topology.legacy_warps:
            adjacency[edge.source.floor_id].append(edge.destination.floor_id)

        reached = set(self.stable_floor_ids)
        queue = collections.deque(sorted(reached))
        while queue:
            source = queue.popleft()
            for destination in adjacency.get(source, ()):
                if destination in reached:
                    continue
                reached.add(destination)
                queue.append(destination)
        return frozenset(reached)

    @property
    def unreachable_resolved_supplemental_ids(self) -> tuple[int, ...]:
        return tuple(sorted(
            self.resolved_supplemental_floor_ids - self.reachable_floor_ids
        ))


def build_ordered_materializable_runtime(
    *,
    strict_runtime: MaterializableRuntimeTopology,
    create_order_text: str,
) -> OrderedMaterializableRuntime:
    order = parse_create_order_sources(create_order_text)
    strict_ambiguous = strict_runtime.ambiguous_by_source

    if set(order) != set(strict_ambiguous):
        missing = sorted(
            set(strict_ambiguous) - set(order),
            key=lambda p: (p.floor_id, p.x, p.y),
        )
        extra = sorted(
            set(order) - set(strict_ambiguous),
            key=lambda p: (p.floor_id, p.x, p.y),
        )
        raise ValueError(
            f"create-order/strict-ambiguity source drift; "
            f"missing={missing}, extra={extra}"
        )

    active = list(strict_runtime.topology.legacy_warps)
    ordered: list[OrderedAmbiguousWarpResolution] = []
    unresolved: list[AmbiguousWarpSource] = []

    for source in sorted(
        strict_ambiguous,
        key=lambda pos: (pos.floor_id, pos.x, pos.y),
    ):
        group = strict_ambiguous[source]
        record = order[source]

        if record.classification == CROSS_FILE_UNORDERED:
            if record.first_placement_id is not None:
                raise ValueError("cross-file create order unexpectedly selects first")
            unresolved.append(group)
            continue

        if record.classification != SAME_FILE_ORDERED:
            raise ValueError(
                f"unknown create-order classification: {record.classification}"
            )
        if record.first_placement_id is None:
            raise ValueError("same-file create order lacks first placement")

        matches = tuple(
            row for row in group.candidates
            if row.placement_id == record.first_placement_id
        )
        if len(matches) != 1:
            raise ValueError(
                f"ordered placement not unique at source {source}: "
                f"{record.first_placement_id}"
            )
        selected = matches[0]
        if selected.conditional_time:
            raise ValueError(
                "ordered ambiguous source unexpectedly selects conditional Warp"
            )
        shadowed = tuple(
            row for row in group.candidates if row is not selected
        )
        ordered.append(
            OrderedAmbiguousWarpResolution(
                source=source,
                selected=selected,
                shadowed=shadowed,
            )
        )
        active.append(
            LegacyWarpEdge(
                source=source,
                destination=selected.destination,
                time_token=None,
                active=True,
            )
        )

    topology = HistoricalWorldTopology.from_provenance_maps(
        strict_runtime.topology.maps,
        legacy_warps=tuple(active),
    )
    return OrderedMaterializableRuntime(
        strict_runtime=strict_runtime,
        topology=topology,
        ordered_resolutions=tuple(ordered),
        unresolved_ambiguous_sources=tuple(unresolved),
    )


def load_ordered_materializable_runtime() -> OrderedMaterializableRuntime:
    return build_ordered_materializable_runtime(
        strict_runtime=load_materializable_runtime_topology(),
        create_order_text=Path(CREATE_ORDER_REPORT_REF).read_text(
            encoding="utf-8"
        ),
    )
