#!/usr/bin/env python3
"""Focused recovered25 duplicate-floor candidate audit.

The current use is floor 130, the sole runtime-reachable supplemental floor
with divergent recovered server LS2MAP copies. This probe compares every
candidate against independent recovered client DAT/MAP surfaces and classic
Warp geometry. It emits derived counts/hashes only and never auto-selects the
lowest-difference candidate.

Selection is decisive only when exactly one candidate is an exact client-DAT
static-layer match (tile + parts/object). Otherwise the conflict remains open.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_client_server_map_probe import (
    collect_server_maps,
    read_client_map,
)
from tools.stoneage_dat_probe import parse_dat
from tools.stoneage_map_collision_model import static_point_walkable
from tools.stoneage_server_static_map import (
    parse_ls2map,
    parse_mapset_collision_profile,
)
from tools.stoneage_versioned_world_geometry_probe import (
    _parse_create_geometry,
)


EXACT_DAT_STATIC_MATCH = "EXACT_DAT_STATIC_MATCH"
NO_EXACT_DAT_STATIC_MATCH = "NO_EXACT_DAT_STATIC_MATCH"
MULTIPLE_EXACT_DAT_STATIC_MATCHES = "MULTIPLE_EXACT_DAT_STATIC_MATCHES"


def _find_numeric_file(root: Path, floor_id: int, suffix: str) -> Path:
    matches = sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.suffix.lower() == suffix.lower()
            and path.stem.isdigit()
            and int(path.stem) == int(floor_id)
        ),
        key=lambda path: str(path).lower(),
    )
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one client {suffix} for floor {floor_id}, "
            f"found {len(matches)}"
        )
    return matches[0]


def _diff(left, right) -> int:
    left = tuple(int(v) for v in left)
    right = tuple(int(v) for v in right)
    if len(left) != len(right):
        raise ValueError("plane length drift during duplicate-floor comparison")
    return sum(a != b for a, b in zip(left, right))


def _point_walkable(parsed, mapset, x: int, y: int) -> bool | None:
    x, y = int(x), int(y)
    if not (0 <= x < parsed.width and 0 <= y < parsed.height):
        return None
    index = y * parsed.width + x
    tile_id = parsed.tile_ids[index]
    object_id = parsed.object_ids[index]
    if tile_id not in mapset.images or object_id not in mapset.images:
        return None
    return static_point_walkable(
        tile=mapset.images[tile_id],
        object_part=mapset.images[object_id],
    ).allowed


@dataclass(frozen=True)
class CandidateAudit:
    path: str
    sha256: str
    width: int
    height: int
    dat_tile_diff_cells: int
    dat_parts_diff_cells: int
    client_map_tile_diff_cells: int
    client_map_object_diff_cells: int
    incoming_warp_points_in_bounds: int
    incoming_warp_points_walkable: int
    incoming_warp_points_blocked: int
    incoming_warp_points_unknown: int
    outgoing_warp_source_cells_in_bounds: int
    outgoing_warp_source_cells_walkable: int
    outgoing_warp_source_cells_blocked: int
    outgoing_warp_source_cells_unknown: int

    @property
    def dat_static_exact(self) -> bool:
        return (
            self.dat_tile_diff_cells == 0
            and self.dat_parts_diff_cells == 0
        )


@dataclass(frozen=True)
class DuplicateFloorAudit:
    floor_id: int
    client_dat_sha256: str
    client_map_sha256: str
    client_dimensions: tuple[int, int]
    candidates: tuple[CandidateAudit, ...]
    candidate_tile_diff_cells: int
    candidate_object_diff_cells: int
    incoming_classic_warps: int
    outgoing_classic_warps: int
    resolution: str
    selected_path: str | None

    def __post_init__(self) -> None:
        if len(self.candidates) < 2:
            raise ValueError("duplicate-floor audit requires multiple candidates")
        exact = [row.path for row in self.candidates if row.dat_static_exact]
        if self.resolution == EXACT_DAT_STATIC_MATCH:
            if len(exact) != 1 or self.selected_path != exact[0]:
                raise ValueError("exact-match resolution is inconsistent")
        elif self.resolution == NO_EXACT_DAT_STATIC_MATCH:
            if exact or self.selected_path is not None:
                raise ValueError("no-exact resolution cannot select a candidate")
        elif self.resolution == MULTIPLE_EXACT_DAT_STATIC_MATCHES:
            if len(exact) < 2 or self.selected_path is not None:
                raise ValueError("multiple-exact resolution cannot select one")
        else:
            raise ValueError("unknown duplicate-floor resolution")


def analyze(
    *,
    floor_id: int,
    client_map_root: Path,
    server_map_root: Path,
    mapset_path: Path,
    npc_dir: Path,
) -> DuplicateFloorAudit:
    floor_id = int(floor_id)
    dat_path = _find_numeric_file(client_map_root, floor_id, ".dat")
    map_path = _find_numeric_file(client_map_root, floor_id, ".map")

    dat_w, dat_h, dat_tile, dat_parts, _dat_event = parse_dat(dat_path)
    map_w, map_h, map_values = read_client_map(map_path)
    if (dat_w, dat_h) != (map_w, map_h):
        raise ValueError("client DAT/MAP dimensions disagree")

    server_by_id, _total, _ls2, _invalid = collect_server_maps(
        server_map_root,
        sample_limit=0,
    )
    entries = tuple(server_by_id.get(floor_id, ()))
    if len(entries) < 2:
        raise ValueError(
            f"floor {floor_id} no longer has multiple server-map copies"
        )

    mapset = parse_mapset_collision_profile(mapset_path.read_bytes())
    _placements, warps = _parse_create_geometry(
        npc_dir,
        set(server_by_id),
    )
    incoming = tuple(
        warp for warp in warps
        if warp.destination_floor == floor_id
    )
    outgoing = tuple(
        warp for warp in warps
        if warp.source_floor == floor_id
    )

    parsed_rows = []
    candidate_rows = []
    for entry in sorted(
        entries,
        key=lambda value: str(value["path"].relative_to(server_map_root)).lower(),
    ):
        raw = entry["path"].read_bytes()
        parsed = parse_ls2map(raw)
        if parsed.floor_id != floor_id:
            raise ValueError("server candidate embedded floor id drift")
        if (parsed.width, parsed.height) != (dat_w, dat_h):
            raise ValueError("server/client dimension drift for duplicate floor")

        missing = parsed.used_image_ids - set(mapset.images)
        if missing:
            raise ValueError(
                f"candidate {entry['path']} has missing mapset image ids"
            )

        incoming_bounds = incoming_walk = incoming_block = incoming_unknown = 0
        for warp in incoming:
            state = _point_walkable(
                parsed,
                mapset,
                warp.destination_x,
                warp.destination_y,
            )
            if state is None:
                incoming_unknown += 1
                continue
            incoming_bounds += 1
            if state:
                incoming_walk += 1
            else:
                incoming_block += 1

        source_bounds = source_walk = source_block = source_unknown = 0
        for warp in outgoing:
            x1, y1, x2, y2 = warp.source_rect
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    state = _point_walkable(parsed, mapset, x, y)
                    if state is None:
                        source_unknown += 1
                        continue
                    source_bounds += 1
                    if state:
                        source_walk += 1
                    else:
                        source_block += 1

        row = CandidateAudit(
            path=str(entry["path"].relative_to(server_map_root)),
            sha256=hashlib.sha256(raw).hexdigest(),
            width=parsed.width,
            height=parsed.height,
            dat_tile_diff_cells=_diff(dat_tile, parsed.tile_ids),
            dat_parts_diff_cells=_diff(dat_parts, parsed.object_ids),
            client_map_tile_diff_cells=_diff(map_values, parsed.tile_ids),
            client_map_object_diff_cells=_diff(map_values, parsed.object_ids),
            incoming_warp_points_in_bounds=incoming_bounds,
            incoming_warp_points_walkable=incoming_walk,
            incoming_warp_points_blocked=incoming_block,
            incoming_warp_points_unknown=incoming_unknown,
            outgoing_warp_source_cells_in_bounds=source_bounds,
            outgoing_warp_source_cells_walkable=source_walk,
            outgoing_warp_source_cells_blocked=source_block,
            outgoing_warp_source_cells_unknown=source_unknown,
        )
        parsed_rows.append(parsed)
        candidate_rows.append(row)

    # The current conflict has two copies. Keeping this explicit prevents a
    # pairwise aggregate from becoming ambiguous if another copy appears.
    if len(parsed_rows) != 2:
        raise ValueError(
            "focused pairwise duplicate audit currently requires exactly two copies"
        )
    candidate_tile_diff = _diff(
        parsed_rows[0].tile_ids,
        parsed_rows[1].tile_ids,
    )
    candidate_object_diff = _diff(
        parsed_rows[0].object_ids,
        parsed_rows[1].object_ids,
    )

    exact = [row for row in candidate_rows if row.dat_static_exact]
    if len(exact) == 1:
        resolution = EXACT_DAT_STATIC_MATCH
        selected = exact[0].path
    elif not exact:
        resolution = NO_EXACT_DAT_STATIC_MATCH
        selected = None
    else:
        resolution = MULTIPLE_EXACT_DAT_STATIC_MATCHES
        selected = None

    return DuplicateFloorAudit(
        floor_id=floor_id,
        client_dat_sha256=hashlib.sha256(dat_path.read_bytes()).hexdigest(),
        client_map_sha256=hashlib.sha256(map_path.read_bytes()).hexdigest(),
        client_dimensions=(dat_w, dat_h),
        candidates=tuple(candidate_rows),
        candidate_tile_diff_cells=candidate_tile_diff,
        candidate_object_diff_cells=candidate_object_diff,
        incoming_classic_warps=len(incoming),
        outgoing_classic_warps=len(outgoing),
        resolution=resolution,
        selected_path=selected,
    )


def emit(audit: DuplicateFloorAudit) -> None:
    print("StoneAge recovered duplicate-floor candidate audit — R1")
    print(f"FLOOR|{audit.floor_id}")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|only a unique exact client-DAT tile+parts match can select a "
        "server candidate automatically"
    )
    print(
        f"CLIENT|dimensions={audit.client_dimensions[0]}x"
        f"{audit.client_dimensions[1]}|dat_sha256={audit.client_dat_sha256}|"
        f"map_sha256={audit.client_map_sha256}"
    )
    print(f"COUNT|server_candidates|{len(audit.candidates)}")
    print(f"COUNT|incoming_classic_warps|{audit.incoming_classic_warps}")
    print(f"COUNT|outgoing_classic_warps|{audit.outgoing_classic_warps}")
    print(
        f"CANDIDATE_PAIR_DIFF|tile_cells={audit.candidate_tile_diff_cells}|"
        f"object_cells={audit.candidate_object_diff_cells}"
    )
    for row in audit.candidates:
        print(
            "CANDIDATE|"
            f"path={row.path}|sha256={row.sha256}|"
            f"dimensions={row.width}x{row.height}|"
            f"dat_tile_diff_cells={row.dat_tile_diff_cells}|"
            f"dat_parts_diff_cells={row.dat_parts_diff_cells}|"
            f"dat_static_exact={int(row.dat_static_exact)}|"
            f"client_map_tile_diff_cells={row.client_map_tile_diff_cells}|"
            f"client_map_object_diff_cells={row.client_map_object_diff_cells}|"
            f"incoming_warp_points_in_bounds={row.incoming_warp_points_in_bounds}|"
            f"incoming_warp_points_walkable={row.incoming_warp_points_walkable}|"
            f"incoming_warp_points_blocked={row.incoming_warp_points_blocked}|"
            f"incoming_warp_points_unknown={row.incoming_warp_points_unknown}|"
            f"outgoing_warp_source_cells_in_bounds={row.outgoing_warp_source_cells_in_bounds}|"
            f"outgoing_warp_source_cells_walkable={row.outgoing_warp_source_cells_walkable}|"
            f"outgoing_warp_source_cells_blocked={row.outgoing_warp_source_cells_blocked}|"
            f"outgoing_warp_source_cells_unknown={row.outgoing_warp_source_cells_unknown}"
        )
    print(
        f"RESOLUTION|{audit.resolution}|"
        f"selected_path={audit.selected_path or 'NONE'}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--floor", type=int, default=130)
    parser.add_argument("--client-map-root", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    parser.add_argument("--mapset", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze(
            floor_id=args.floor,
            client_map_root=args.client_map_root,
            server_map_root=args.server_map_root,
            mapset_path=args.mapset,
            npc_dir=args.npc_dir,
        )
    )


if __name__ == "__main__":
    main()
