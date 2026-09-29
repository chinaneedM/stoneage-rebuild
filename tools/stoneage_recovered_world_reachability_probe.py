#!/usr/bin/env python3
"""Compute runtime-valid classic-Warp reachability beyond the stable map seeds.

The 761 stable later-map candidates are multi-source depth-0 seeds. Expansion
uses only classic Warp edges whose destination floor exists on the recovered
server and whose destination coordinate is valid for at least one recovered
server-map copy. This mirrors the classic Warp initialization validity gate
instead of treating every syntactically parseable argument as executable.

All supplemental floors remain recovered25 / LATER_RECOVERED.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from tools.stoneage_client_server_map_probe import collect_server_maps
from tools.stoneage_missing_warp_destination_payload_probe import (
    collect_numeric_client_maps,
)
from tools.stoneage_versioned_world_geometry_probe import (
    _parse_create_geometry,
)
from tools.stoneage_warp_destination_corpus_probe import (
    collect_numeric_dat_paths,
    parse_later_lineage,
)


CHANGED = "CHANGED"
CLIENT_DAT_PRESENT_NONSTABLE = "CLIENT_DAT_PRESENT_NONSTABLE"
SERVER_WITH_CLIENT_MAP_ONLY = "SERVER_WITH_CLIENT_MAP_ONLY"
SERVER_ONLY = "SERVER_ONLY"

NO_SERVER_MAP = "NO_SERVER_MAP"
DESTINATION_OUT_OF_BOUNDS = "DESTINATION_OUT_OF_BOUNDS"


@dataclass(frozen=True)
class ReachabilityFloor:
    floor_id: int
    depth: int
    status: str
    server_map_present: bool
    client_dat_present: bool
    client_map_present: bool
    incoming_reachable_warps: int
    outgoing_runtime_warps: int


@dataclass(frozen=True)
class InvalidReachableWarp:
    source_floor: int
    destination_floor: int
    destination_x: int
    destination_y: int
    reason: str


@dataclass(frozen=True)
class ReachabilityAudit:
    stable_floor_ids: frozenset[int]
    reached_floor_ids: frozenset[int]
    supplemental: tuple[ReachabilityFloor, ...]
    reachable_edges: tuple[tuple[int, int], ...]
    invalid_reachable_edges: tuple[InvalidReachableWarp, ...]
    syntactic_server_source_edges: int
    runtime_valid_server_source_edges: int

    @property
    def counts(self) -> dict[str, int]:
        out = {
            "stable_seed_floors": len(self.stable_floor_ids),
            "reachable_floor_ids": len(self.reached_floor_ids),
            "supplemental_floor_ids": len(self.supplemental),
            "syntactic_server_source_classic_warp_edges": int(
                self.syntactic_server_source_edges
            ),
            "runtime_valid_server_source_classic_warp_edges": int(
                self.runtime_valid_server_source_edges
            ),
            "reachable_runtime_classic_warp_edges": len(self.reachable_edges),
            "reachable_invalid_classic_warp_edges": len(
                self.invalid_reachable_edges
            ),
            "max_supplemental_depth": max(
                (row.depth for row in self.supplemental),
                default=0,
            ),
        }
        for row in self.supplemental:
            out[f"status:{row.status}:ids"] = (
                out.get(f"status:{row.status}:ids", 0) + 1
            )
        for edge in self.invalid_reachable_edges:
            out[f"invalid_reason:{edge.reason}:edges"] = (
                out.get(f"invalid_reason:{edge.reason}:edges", 0) + 1
            )
        return out


def _destination_validity(
    *,
    destination_floor: int,
    destination_x: int,
    destination_y: int,
    server_dimensions: Mapping[int, tuple[tuple[int, int], ...]],
) -> str | None:
    copies = server_dimensions.get(int(destination_floor), ())
    if not copies:
        return NO_SERVER_MAP
    x = int(destination_x)
    y = int(destination_y)
    if any(0 <= x < width and 0 <= y < height for width, height in copies):
        return None
    return DESTINATION_OUT_OF_BOUNDS


def compute_reachability(
    *,
    stable_ids: set[int],
    server_dimensions: Mapping[int, tuple[tuple[int, int], ...]],
    warp_edges: tuple[tuple[int, int, int, int], ...],
    dat_ids: set[int],
    client_map_ids: set[int],
    changed_ids: set[int],
) -> ReachabilityAudit:
    stable = set(int(v) for v in stable_ids)
    dimensions = {
        int(floor_id): tuple((int(w), int(h)) for w, h in copies)
        for floor_id, copies in server_dimensions.items()
    }
    server = set(dimensions)
    dat = set(int(v) for v in dat_ids)
    client_map = set(int(v) for v in client_map_ids)
    changed = set(int(v) for v in changed_ids)
    edges = tuple(
        (int(source), int(destination), int(x), int(y))
        for source, destination, x, y in warp_edges
    )

    by_source: dict[int, list[tuple[int, int, int, str | None]]] = (
        collections.defaultdict(list)
    )
    syntactic_edges = 0
    runtime_valid_edges = 0
    for source, destination, x, y in edges:
        if source not in server:
            continue
        syntactic_edges += 1
        reason = _destination_validity(
            destination_floor=destination,
            destination_x=x,
            destination_y=y,
            server_dimensions=dimensions,
        )
        if reason is None:
            runtime_valid_edges += 1
        by_source[source].append((destination, x, y, reason))

    depth = {floor_id: 0 for floor_id in stable}
    queue = collections.deque(sorted(stable & server))
    reachable_edges: list[tuple[int, int]] = []
    invalid_reachable_edges: list[InvalidReachableWarp] = []

    while queue:
        source = queue.popleft()
        for destination, x, y, reason in by_source.get(source, ()):
            if reason is not None:
                invalid_reachable_edges.append(
                    InvalidReachableWarp(
                        source_floor=source,
                        destination_floor=destination,
                        destination_x=x,
                        destination_y=y,
                        reason=reason,
                    )
                )
                continue

            reachable_edges.append((source, destination))
            if destination in depth:
                continue
            depth[destination] = depth[source] + 1
            queue.append(destination)

    incoming = collections.Counter(
        destination for _source, destination in reachable_edges
    )
    runtime_outgoing = collections.Counter(
        source for source, _destination in reachable_edges
    )

    supplemental_rows = []
    for floor_id in sorted(set(depth) - stable):
        has_server = floor_id in server
        if not has_server:
            raise ValueError(
                "runtime-valid closure admitted a floor without server map: "
                f"{floor_id}"
            )
        has_dat = floor_id in dat
        has_map = floor_id in client_map

        if floor_id in changed:
            status = CHANGED
        elif has_dat:
            status = CLIENT_DAT_PRESENT_NONSTABLE
        elif has_map:
            status = SERVER_WITH_CLIENT_MAP_ONLY
        else:
            status = SERVER_ONLY

        supplemental_rows.append(
            ReachabilityFloor(
                floor_id=floor_id,
                depth=depth[floor_id],
                status=status,
                server_map_present=True,
                client_dat_present=has_dat,
                client_map_present=has_map,
                incoming_reachable_warps=incoming[floor_id],
                outgoing_runtime_warps=runtime_outgoing[floor_id],
            )
        )

    return ReachabilityAudit(
        stable_floor_ids=frozenset(stable),
        reached_floor_ids=frozenset(depth),
        supplemental=tuple(supplemental_rows),
        reachable_edges=tuple(reachable_edges),
        invalid_reachable_edges=tuple(invalid_reachable_edges),
        syntactic_server_source_edges=syntactic_edges,
        runtime_valid_server_source_edges=runtime_valid_edges,
    )


def analyze(
    *,
    lineage_text: str,
    npc_dir: Path,
    server_map_root: Path,
    client_map_root: Path,
) -> ReachabilityAudit:
    stable, changed, _counts = parse_later_lineage(lineage_text)
    server_by_id, _files, _ls2, _invalid = collect_server_maps(
        server_map_root,
        sample_limit=0,
    )
    server_dimensions = {
        floor_id: tuple(
            (int(entry["width"]), int(entry["height"]))
            for entry in entries
        )
        for floor_id, entries in server_by_id.items()
    }
    _placements, warps = _parse_create_geometry(
        npc_dir,
        set(server_by_id),
    )
    edges = tuple(
        (
            warp.source_floor,
            warp.destination_floor,
            warp.destination_x,
            warp.destination_y,
        )
        for warp in warps
    )
    dat_paths = collect_numeric_dat_paths(client_map_root)
    client_maps = collect_numeric_client_maps(client_map_root)
    return compute_reachability(
        stable_ids=set(stable),
        server_dimensions=server_dimensions,
        warp_edges=edges,
        dat_ids=set(dat_paths),
        client_map_ids=set(client_maps),
        changed_ids=set(changed),
    )


def emit(audit: ReachabilityAudit) -> None:
    print("StoneAge recovered runtime-valid classic-Warp world closure — R1")
    print(
        "SCOPE|multi-source stable-map seeds -> recursive recovered25 classic "
        "Warp closure|destination server-map + coordinate validity required"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|supplemental reachability does not promote any floor into "
        "Taiwan-v1 membership"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.supplemental:
        print(
            "SUPPLEMENTAL_FLOOR|"
            f"floor={row.floor_id}|depth={row.depth}|status={row.status}|"
            f"server_map={int(row.server_map_present)}|"
            f"client_dat={int(row.client_dat_present)}|"
            f"client_map={int(row.client_map_present)}|"
            f"incoming_reachable_warps={row.incoming_reachable_warps}|"
            f"outgoing_runtime_warps={row.outgoing_runtime_warps}"
        )
    for edge in audit.invalid_reachable_edges:
        print(
            "INVALID_REACHABLE_WARP|"
            f"source={edge.source_floor}|destination={edge.destination_floor}|"
            f"destination_x={edge.destination_x}|"
            f"destination_y={edge.destination_y}|reason={edge.reason}"
        )
    for source, destination in audit.reachable_edges:
        if (
            source in audit.stable_floor_ids
            and destination in audit.stable_floor_ids
        ):
            continue
        print(
            "REACHABLE_EDGE|"
            f"source={source}|destination={destination}|"
            f"source_stable={int(source in audit.stable_floor_ids)}|"
            f"destination_stable={int(destination in audit.stable_floor_ids)}"
        )
    print("RESOLUTION|RECOVERED_RUNTIME_CLASSIC_WARP_REACHABILITY_CLOSED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-report", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    parser.add_argument("--client-map-root", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze(
            lineage_text=args.lineage_report.read_text(encoding="utf-8"),
            npc_dir=args.npc_dir,
            server_map_root=args.server_map_root,
            client_map_root=args.client_map_root,
        )
    )


if __name__ == "__main__":
    main()
