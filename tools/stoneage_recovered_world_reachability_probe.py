#!/usr/bin/env python3
"""Compute recursive classic-Warp reachability beyond the stable map seed set.

This is a recovered-2.5 topology audit. The 761 stable later-map candidates are
multi-source depth-0 seeds, but every supplemental floor retains LATER_RECOVERED
provenance. Only numeric topology/payload-presence metadata is emitted.
"""

from __future__ import annotations

import argparse
import collections
from dataclasses import dataclass
from pathlib import Path

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


STABLE_COMPATIBLE = "STABLE_COMPATIBLE"
CHANGED = "CHANGED"
CLIENT_DAT_PRESENT_NONSTABLE = "CLIENT_DAT_PRESENT_NONSTABLE"
SERVER_WITH_CLIENT_MAP_ONLY = "SERVER_WITH_CLIENT_MAP_ONLY"
SERVER_ONLY = "SERVER_ONLY"
NO_SERVER_MAP = "NO_SERVER_MAP"


@dataclass(frozen=True)
class ReachabilityFloor:
    floor_id: int
    depth: int
    status: str
    server_map_present: bool
    client_dat_present: bool
    client_map_present: bool
    incoming_reachable_warps: int
    outgoing_classic_warps: int


@dataclass(frozen=True)
class ReachabilityAudit:
    stable_floor_ids: frozenset[int]
    reached_floor_ids: frozenset[int]
    supplemental: tuple[ReachabilityFloor, ...]
    reachable_edges: tuple[tuple[int, int], ...]
    server_source_warp_edges: int

    @property
    def counts(self) -> dict[str, int]:
        out = {
            "stable_seed_floors": len(self.stable_floor_ids),
            "reachable_floor_ids": len(self.reached_floor_ids),
            "supplemental_floor_ids": len(self.supplemental),
            "reachable_classic_warp_edges": len(self.reachable_edges),
            "server_source_classic_warp_edges": int(self.server_source_warp_edges),
            "max_supplemental_depth": max(
                (row.depth for row in self.supplemental),
                default=0,
            ),
        }
        for row in self.supplemental:
            out[f"status:{row.status}:ids"] = (
                out.get(f"status:{row.status}:ids", 0) + 1
            )
        return out


def compute_reachability(
    *,
    stable_ids: set[int],
    server_ids: set[int],
    warp_edges: tuple[tuple[int, int], ...],
    dat_ids: set[int],
    client_map_ids: set[int],
    changed_ids: set[int],
) -> ReachabilityAudit:
    stable = set(int(v) for v in stable_ids)
    server = set(int(v) for v in server_ids)
    dat = set(int(v) for v in dat_ids)
    client_map = set(int(v) for v in client_map_ids)
    changed = set(int(v) for v in changed_ids)
    edges = tuple((int(a), int(b)) for a, b in warp_edges)

    by_source: dict[int, list[int]] = collections.defaultdict(list)
    server_source_edges = 0
    for source, destination in edges:
        if source not in server:
            continue
        by_source[source].append(destination)
        server_source_edges += 1

    depth = {floor_id: 0 for floor_id in stable}
    queue = collections.deque(sorted(stable & server))
    reachable_edges: list[tuple[int, int]] = []

    while queue:
        source = queue.popleft()
        for destination in by_source.get(source, ()):
            reachable_edges.append((source, destination))
            if destination in depth:
                continue
            depth[destination] = depth[source] + 1
            if destination in server:
                queue.append(destination)

    incoming = collections.Counter(destination for _source, destination in reachable_edges)
    supplemental_rows = []
    for floor_id in sorted(set(depth) - stable):
        has_server = floor_id in server
        has_dat = floor_id in dat
        has_map = floor_id in client_map

        if not has_server:
            status = NO_SERVER_MAP
        elif floor_id in changed:
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
                server_map_present=has_server,
                client_dat_present=has_dat,
                client_map_present=has_map,
                incoming_reachable_warps=incoming[floor_id],
                outgoing_classic_warps=len(by_source.get(floor_id, ())),
            )
        )

    return ReachabilityAudit(
        stable_floor_ids=frozenset(stable),
        reached_floor_ids=frozenset(depth),
        supplemental=tuple(supplemental_rows),
        reachable_edges=tuple(reachable_edges),
        server_source_warp_edges=server_source_edges,
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
    server_ids = set(server_by_id)
    _placements, warps = _parse_create_geometry(npc_dir, server_ids)
    edges = tuple(
        (warp.source_floor, warp.destination_floor)
        for warp in warps
    )
    dat_paths = collect_numeric_dat_paths(client_map_root)
    client_maps = collect_numeric_client_maps(client_map_root)
    return compute_reachability(
        stable_ids=set(stable),
        server_ids=server_ids,
        warp_edges=edges,
        dat_ids=set(dat_paths),
        client_map_ids=set(client_maps),
        changed_ids=set(changed),
    )


def emit(audit: ReachabilityAudit) -> None:
    print("StoneAge recovered classic-Warp reachable-world closure — R1")
    print(
        "SCOPE|multi-source stable-map seeds -> recursive recovered25 classic Warp "
        "closure|numeric topology and payload presence only"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|supplemental reachability does not promote any floor into Taiwan-v1 membership"
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
            f"outgoing_classic_warps={row.outgoing_classic_warps}"
        )
    for source, destination in audit.reachable_edges:
        if source in audit.stable_floor_ids and destination in audit.stable_floor_ids:
            continue
        print(
            "REACHABLE_EDGE|"
            f"source={source}|destination={destination}|"
            f"source_stable={int(source in audit.stable_floor_ids)}|"
            f"destination_stable={int(destination in audit.stable_floor_ids)}"
        )
    print("RESOLUTION|RECOVERED_CLASSIC_WARP_REACHABILITY_CLOSED")


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
