#!/usr/bin/env python3
"""Audit reachability of the default materializable recovered world.

The default world is the immutable 761-floor stable manifest plus the 65
resolved supplemental floors. Floor 130 remains represented as an unresolved
version fork and is not a default map. Reachability uses only MATERIALIZABLE_WARP
rows from the closed derived geometry report.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_supplemental_world_manifest import (
    parse_supplemental_world_audit,
)
from tools.stoneage_versioned_world_manifest import (
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    parse_stable_later_map_manifest,
)


GEOMETRY_RESOLUTION = (
    "RESOLUTION|MATERIALIZABLE_RECOVERED_WORLD_WARP_GEOMETRY_CLOSED"
)
OUTPUT_RESOLUTION = "RESOLUTION|MATERIALIZABLE_WORLD_REACHABILITY_CLOSED"


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


def _point3(value: str) -> tuple[int, int, int]:
    pieces = str(value).split(",")
    if len(pieces) != 3:
        raise ValueError(f"invalid floor/x/y tuple: {value}")
    return tuple(int(piece) for piece in pieces)  # type: ignore[return-value]


@dataclass(frozen=True)
class MaterializableWarpEdge:
    source_floor: int
    destination_floor: int


def parse_materializable_geometry(
    text: str,
) -> tuple[tuple[MaterializableWarpEdge, ...], dict[str, int]]:
    counts: dict[str, int] = {}
    edges: list[MaterializableWarpEdge] = []
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("COUNT|"):
            parts = line.split("|")
            if len(parts) != 3:
                raise ValueError(f"malformed materializable COUNT row: {line}")
            if parts[1] in counts:
                raise ValueError(f"duplicate materializable COUNT key: {parts[1]}")
            counts[parts[1]] = int(parts[2])
            continue
        if line.startswith("MATERIALIZABLE_WARP|"):
            fields = _fields(line, "MATERIALIZABLE_WARP")
            source = _point3(fields["source"])
            destination = _point3(fields["destination"])
            edges.append(
                MaterializableWarpEdge(
                    source_floor=source[0],
                    destination_floor=destination[0],
                )
            )
            continue
        if line == GEOMETRY_RESOLUTION:
            resolution = True

    if not resolution:
        raise ValueError("materializable Warp geometry report is not closed")
    declared = counts.get("materializable_classic_warps")
    if declared is None:
        raise ValueError("materializable Warp geometry lacks edge count")
    if declared != len(edges):
        raise ValueError(
            "materializable Warp detail count drift: "
            f"declared={declared}, actual={len(edges)}"
        )
    return tuple(edges), counts


@dataclass(frozen=True)
class ResolvedSupplementalReachability:
    floor_id: int
    depth: int
    incoming_materializable_warps: int
    outgoing_materializable_warps: int


@dataclass(frozen=True)
class MaterializableWorldReachabilityAudit:
    stable_floor_ids: frozenset[int]
    resolved_supplemental_ids: frozenset[int]
    unresolved_supplemental_ids: frozenset[int]
    reached_floor_ids: frozenset[int]
    resolved_rows: tuple[ResolvedSupplementalReachability, ...]
    orphan_resolved_supplemental_ids: tuple[int, ...]
    materializable_warp_edges: int

    @property
    def counts(self) -> dict[str, int]:
        return {
            "stable_seed_floors": len(self.stable_floor_ids),
            "resolved_supplemental_floor_ids": len(
                self.resolved_supplemental_ids
            ),
            "unresolved_supplemental_floor_ids": len(
                self.unresolved_supplemental_ids
            ),
            "materializable_floor_ids": (
                len(self.stable_floor_ids) + len(self.resolved_supplemental_ids)
            ),
            "materializable_classic_warps": int(self.materializable_warp_edges),
            "reachable_floor_ids": len(self.reached_floor_ids),
            "reachable_resolved_supplemental_floors": len(self.resolved_rows),
            "orphan_resolved_supplemental_floors": len(
                self.orphan_resolved_supplemental_ids
            ),
            "max_resolved_supplemental_depth": max(
                (row.depth for row in self.resolved_rows),
                default=0,
            ),
        }


def compute_materializable_reachability(
    *,
    stable_floor_ids: set[int],
    resolved_supplemental_ids: set[int],
    unresolved_supplemental_ids: set[int],
    edges: tuple[MaterializableWarpEdge, ...],
) -> MaterializableWorldReachabilityAudit:
    stable = set(int(v) for v in stable_floor_ids)
    resolved = set(int(v) for v in resolved_supplemental_ids)
    unresolved = set(int(v) for v in unresolved_supplemental_ids)
    materializable = stable | resolved

    if stable & resolved:
        raise ValueError("stable/resolved supplemental floor overlap")
    if materializable & unresolved:
        raise ValueError("unresolved floor leaked into materializable set")

    by_source: dict[int, list[int]] = collections.defaultdict(list)
    incoming = collections.Counter()
    outgoing = collections.Counter()
    for edge in edges:
        source = int(edge.source_floor)
        destination = int(edge.destination_floor)
        if source not in materializable:
            raise ValueError(
                f"materializable edge source outside materializable world: {source}"
            )
        if destination not in materializable:
            raise ValueError(
                "materializable edge destination outside materializable world: "
                f"{destination}"
            )
        by_source[source].append(destination)
        outgoing[source] += 1
        incoming[destination] += 1

    depth = {floor_id: 0 for floor_id in stable}
    queue = collections.deque(sorted(stable))
    while queue:
        source = queue.popleft()
        for destination in by_source.get(source, ()):
            if destination in depth:
                continue
            depth[destination] = depth[source] + 1
            queue.append(destination)

    reached_resolved = sorted(resolved & set(depth))
    orphans = tuple(sorted(resolved - set(depth)))
    rows = tuple(
        ResolvedSupplementalReachability(
            floor_id=floor_id,
            depth=depth[floor_id],
            incoming_materializable_warps=int(incoming[floor_id]),
            outgoing_materializable_warps=int(outgoing[floor_id]),
        )
        for floor_id in reached_resolved
    )

    return MaterializableWorldReachabilityAudit(
        stable_floor_ids=frozenset(stable),
        resolved_supplemental_ids=frozenset(resolved),
        unresolved_supplemental_ids=frozenset(unresolved),
        reached_floor_ids=frozenset(depth),
        resolved_rows=rows,
        orphan_resolved_supplemental_ids=orphans,
        materializable_warp_edges=len(edges),
    )


def analyze(
    *,
    lineage_text: str,
    coverage_text: str,
    supplemental_audit_text: str,
    materializable_geometry_text: str,
) -> MaterializableWorldReachabilityAudit:
    stable_maps = parse_stable_later_map_manifest(lineage_text)
    stable_world = build_versioned_world_manifest(
        maps=stable_maps,
        coverage_text=coverage_text,
    )
    extension = parse_supplemental_world_audit(
        stable_world=stable_world,
        text=supplemental_audit_text,
    )
    edges, geometry_counts = parse_materializable_geometry(
        materializable_geometry_text
    )

    expected_materializable = len(extension.materializable_floor_ids)
    declared_materializable = geometry_counts.get("materializable_floor_ids")
    if declared_materializable != expected_materializable:
        raise ValueError(
            "geometry/extension materializable floor count drift: "
            f"geometry={declared_materializable}, "
            f"extension={expected_materializable}"
        )

    return compute_materializable_reachability(
        stable_floor_ids=set(stable_world.by_floor),
        resolved_supplemental_ids=set(extension.resolved_by_floor),
        unresolved_supplemental_ids=set(extension.unresolved_by_floor),
        edges=edges,
    )


def emit(audit: MaterializableWorldReachabilityAudit) -> None:
    print("StoneAge default materializable world reachability — R1")
    print(
        "SCOPE|761 stable seeds -> materializable classic Warp BFS|"
        "resolved supplemental closure with unresolved forks quarantined"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|unresolved supplemental floors are represented but cannot act as "
        "default traversal intermediates"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.resolved_rows:
        print(
            "REACHABLE_RESOLVED_SUPPLEMENTAL|"
            f"floor={row.floor_id}|depth={row.depth}|"
            f"incoming_materializable_warps={row.incoming_materializable_warps}|"
            f"outgoing_materializable_warps={row.outgoing_materializable_warps}"
        )
    for floor_id in audit.orphan_resolved_supplemental_ids:
        print(f"ORPHAN_RESOLVED_SUPPLEMENTAL|floor={floor_id}")
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--coverage-report", type=Path, required=True)
    parser.add_argument("--supplemental-audit", type=Path, required=True)
    parser.add_argument("--materializable-geometry", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze(
            lineage_text=args.lineage_report.read_text(encoding="utf-8"),
            coverage_text=args.coverage_report.read_text(encoding="utf-8"),
            supplemental_audit_text=args.supplemental_audit.read_text(
                encoding="utf-8"
            ),
            materializable_geometry_text=args.materializable_geometry.read_text(
                encoding="utf-8"
            ),
        )
    )


if __name__ == "__main__":
    main()
