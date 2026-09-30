#!/usr/bin/env python3
"""Audit recovered25 server-backed collision coverage for materializable floors.

The coordinator requires an explicit collision verdict. This audit measures
exactly how much of the closed 826-floor recovered25 runtime world can obtain
that verdict from recovered server LS2MAP + recovered mapset metadata without
fallback or guessing.

Only derived counts, floor IDs, dimensions and hashes are emitted. Raw map
planes and mapset rows are not persisted.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_local_runtime_core import load_runtime_bootstrap_file
from tools.stoneage_recovered25_world_profile_adapter import (
    Recovered25WorldProfileAdapter,
)
from tools.stoneage_server_static_map import (
    RecoveredMapsetProfile,
    RecoveredServerStaticMap,
    parse_ls2map,
    parse_mapset_collision_profile,
    summarize_static_collision,
)
from tools.stoneage_singleplayer_world import HistoricalMapDefinition


SERVER_COLLISION_CLOSED = "SERVER_COLLISION_CLOSED"
NO_SERVER_MAP = "NO_SERVER_MAP"
DIVERGENT_SERVER_DUPLICATE = "DIVERGENT_SERVER_DUPLICATE"
SERVER_DIMENSION_MISMATCH = "SERVER_DIMENSION_MISMATCH"
MISSING_MAPSET_METADATA = "MISSING_MAPSET_METADATA"

OUTPUT_RESOLUTION = "RESOLUTION|RECOVERED25_SERVER_COLLISION_COVERAGE_AUDITED"


@dataclass(frozen=True)
class FloorCollisionCoverage:
    floor_id: int
    status: str
    server_copy_count: int
    unique_payload_count: int
    ordinary_walkable_cells: int | None = None
    total_cells: int | None = None


@dataclass(frozen=True)
class CollisionCoverageAudit:
    rows: tuple[FloorCollisionCoverage, ...]
    stable_floor_ids: frozenset[int]
    supplemental_floor_ids: frozenset[int]
    mapset_sha256: str
    valid_server_files: int
    invalid_server_files: int

    @property
    def counts(self) -> Counter:
        out = Counter()
        out["materializable_floors"] = len(self.rows)
        out["stable_floors"] = len(self.stable_floor_ids)
        out["supplemental_floors"] = len(self.supplemental_floor_ids)
        out["valid_server_files"] = self.valid_server_files
        out["invalid_server_files"] = self.invalid_server_files
        for row in self.rows:
            out[f"status:{row.status}"] += 1
            if row.server_copy_count > 1 and row.unique_payload_count == 1:
                out["byte_identical_duplicate_floor_ids"] += 1
            if row.status == SERVER_COLLISION_CLOSED:
                out["server_collision_closed_cells"] += int(row.total_cells or 0)
                out["server_collision_ordinary_walkable_cells"] += int(
                    row.ordinary_walkable_cells or 0
                )
                if row.floor_id in self.stable_floor_ids:
                    out["stable_server_collision_closed"] += 1
                if row.floor_id in self.supplemental_floor_ids:
                    out["supplemental_server_collision_closed"] += 1
        out["server_collision_uncovered_floors"] = (
            out["materializable_floors"]
            - out[f"status:{SERVER_COLLISION_CLOSED}"]
        )
        return out


def _classify_floor(
    definition: HistoricalMapDefinition,
    copies: tuple[RecoveredServerStaticMap, ...],
    mapset: RecoveredMapsetProfile,
) -> FloorCollisionCoverage:
    floor_id = int(definition.floor_id)
    if not copies:
        return FloorCollisionCoverage(
            floor_id=floor_id,
            status=NO_SERVER_MAP,
            server_copy_count=0,
            unique_payload_count=0,
        )

    by_hash = {row.payload_sha256: row for row in copies}
    if len(by_hash) > 1:
        return FloorCollisionCoverage(
            floor_id=floor_id,
            status=DIVERGENT_SERVER_DUPLICATE,
            server_copy_count=len(copies),
            unique_payload_count=len(by_hash),
        )

    parsed = next(iter(by_hash.values()))
    if (parsed.width, parsed.height) != (definition.width, definition.height):
        return FloorCollisionCoverage(
            floor_id=floor_id,
            status=SERVER_DIMENSION_MISMATCH,
            server_copy_count=len(copies),
            unique_payload_count=1,
        )

    summary = summarize_static_collision(parsed, mapset)
    if summary.missing_image_ids:
        return FloorCollisionCoverage(
            floor_id=floor_id,
            status=MISSING_MAPSET_METADATA,
            server_copy_count=len(copies),
            unique_payload_count=1,
            total_cells=summary.cells,
        )

    return FloorCollisionCoverage(
        floor_id=floor_id,
        status=SERVER_COLLISION_CLOSED,
        server_copy_count=len(copies),
        unique_payload_count=1,
        ordinary_walkable_cells=summary.ordinary_walkable_cells,
        total_cells=summary.cells,
    )


def _scan_server_maps(
    root: Path,
) -> tuple[dict[int, tuple[RecoveredServerStaticMap, ...]], int, int]:
    by_floor: dict[int, list[RecoveredServerStaticMap]] = defaultdict(list)
    valid = 0
    invalid = 0
    for path in sorted(Path(root).rglob("*"), key=lambda p: str(p).lower()):
        if not path.is_file() or path.name.lower() == "mapset.txt":
            continue
        try:
            parsed = parse_ls2map(path.read_bytes())
        except (OSError, ValueError):
            invalid += 1
            continue
        valid += 1
        by_floor[int(parsed.floor_id)].append(parsed)
    return (
        {floor: tuple(rows) for floor, rows in by_floor.items()},
        valid,
        invalid,
    )


def analyze(
    *,
    server_map_root: Path,
    mapset_path: Path,
) -> CollisionCoverageAudit:
    root = Path(__file__).resolve().parents[1]
    profile = load_runtime_bootstrap_file(
        root / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
    )
    adapter = Recovered25WorldProfileAdapter.from_repository(profile)
    mapset = parse_mapset_collision_profile(Path(mapset_path).read_bytes())
    server_by_floor, valid, invalid = _scan_server_maps(server_map_root)

    extension = adapter.runtime.base.extension
    stable = frozenset(int(x) for x in extension.stable_world.by_floor)
    supplemental = frozenset(int(x) for x in extension.resolved_by_floor)
    if stable & supplemental:
        raise ValueError("stable and supplemental materializable floors overlap")
    if stable | supplemental != frozenset(adapter.topology.maps):
        raise ValueError("collision audit floor classes do not match runtime topology")

    rows = tuple(
        _classify_floor(
            adapter.topology.maps[floor_id],
            server_by_floor.get(int(floor_id), ()),
            mapset,
        )
        for floor_id in sorted(adapter.topology.maps)
    )
    return CollisionCoverageAudit(
        rows=rows,
        stable_floor_ids=stable,
        supplemental_floor_ids=supplemental,
        mapset_sha256=mapset.payload_sha256,
        valid_server_files=valid,
        invalid_server_files=invalid,
    )


def emit(audit: CollisionCoverageAudit) -> None:
    print("StoneAge recovered25 server-backed collision coverage — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|server LS2MAP + recovered mapset only; no Taiwan-v1 ADRN "
        "substitution; uncovered floors remain explicit"
    )
    print(f"MAPSET_SHA256|{audit.mapset_sha256}")
    counts = audit.counts
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")

    for status in (
        NO_SERVER_MAP,
        DIVERGENT_SERVER_DUPLICATE,
        SERVER_DIMENSION_MISMATCH,
        MISSING_MAPSET_METADATA,
    ):
        floor_ids = [
            str(row.floor_id)
            for row in audit.rows
            if row.status == status
        ]
        print(f"FLOOR_IDS|status:{status}|{','.join(floor_ids)}")

    print(OUTPUT_RESOLUTION)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server-map-root", type=Path, required=True)
    ap.add_argument("--mapset", type=Path, required=True)
    args = ap.parse_args()
    emit(
        analyze(
            server_map_root=args.server_map_root,
            mapset_path=args.mapset,
        )
    )


if __name__ == "__main__":
    main()
