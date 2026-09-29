#!/usr/bin/env python3
"""Compare divergent recovered server-map copies against two DAT generations.

This focused lineage audit is intended for a duplicate floor such as floor 130.
It compares archived-2003 and recovered25 client DAT static planes against every
recovered25 server LS2MAP copy, and measures how each candidate aligns on the
cells that changed between the two DAT generations.

No raw map planes are emitted.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_client_server_map_probe import collect_server_maps
from tools.stoneage_dat_probe import parse_dat
from tools.stoneage_server_static_map import parse_ls2map


def _find_dat(root: Path, floor_id: int) -> Path:
    matches = sorted(
        (
            path for path in root.rglob("*")
            if path.is_file()
            and path.suffix.lower() == ".dat"
            and path.stem.isdigit()
            and int(path.stem) == int(floor_id)
        ),
        key=lambda path: str(path).lower(),
    )
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one DAT for floor {floor_id}, found {len(matches)}"
        )
    return matches[0]


def _diff(left, right) -> int:
    left = tuple(int(v) for v in left)
    right = tuple(int(v) for v in right)
    if len(left) != len(right):
        raise ValueError("plane length drift")
    return sum(a != b for a, b in zip(left, right))


def _changed_alignment(old, new, candidate) -> tuple[int, int, int, int]:
    old = tuple(int(v) for v in old)
    new = tuple(int(v) for v in new)
    candidate = tuple(int(v) for v in candidate)
    if not (len(old) == len(new) == len(candidate)):
        raise ValueError("changed-cell alignment plane length drift")
    changed = old_match = new_match = neither = 0
    for before, after, value in zip(old, new, candidate):
        if before == after:
            continue
        changed += 1
        if value == before:
            old_match += 1
        if value == after:
            new_match += 1
        if value != before and value != after:
            neither += 1
    return changed, old_match, new_match, neither


@dataclass(frozen=True)
class CandidateLineage:
    path: str
    sha256: str
    historical_tile_diff: int
    historical_parts_diff: int
    recovered25_tile_diff: int
    recovered25_parts_diff: int
    changed_tile_cells: int
    changed_tile_match_historical: int
    changed_tile_match_recovered25: int
    changed_tile_match_neither: int
    changed_parts_cells: int
    changed_parts_match_historical: int
    changed_parts_match_recovered25: int
    changed_parts_match_neither: int

    @property
    def historical_static_exact(self) -> bool:
        return self.historical_tile_diff == 0 and self.historical_parts_diff == 0

    @property
    def recovered25_static_exact(self) -> bool:
        return self.recovered25_tile_diff == 0 and self.recovered25_parts_diff == 0


@dataclass(frozen=True)
class DuplicateFloorLineageAudit:
    floor_id: int
    historical_sha256: str
    recovered25_sha256: str
    width: int
    height: int
    dat_tile_diff: int
    dat_parts_diff: int
    dat_event_diff: int
    candidates: tuple[CandidateLineage, ...]


def analyze(
    *,
    floor_id: int,
    historical_root: Path,
    recovered25_root: Path,
    server_map_root: Path,
) -> DuplicateFloorLineageAudit:
    floor_id = int(floor_id)
    old_path = _find_dat(historical_root, floor_id)
    new_path = _find_dat(recovered25_root, floor_id)
    old_w, old_h, old_tile, old_parts, old_event = parse_dat(old_path)
    new_w, new_h, new_tile, new_parts, new_event = parse_dat(new_path)
    if (old_w, old_h) != (new_w, new_h):
        raise ValueError("DAT lineage dimension drift")

    server_by_id, _total, _ls2, _invalid = collect_server_maps(
        server_map_root,
        sample_limit=0,
    )
    entries = tuple(server_by_id.get(floor_id, ()))
    if len(entries) < 2:
        raise ValueError("lineage audit requires multiple server candidates")

    rows = []
    for entry in sorted(
        entries,
        key=lambda value: str(value["path"].relative_to(server_map_root)).lower(),
    ):
        raw = entry["path"].read_bytes()
        parsed = parse_ls2map(raw)
        if parsed.floor_id != floor_id:
            raise ValueError("candidate embedded floor id drift")
        if (parsed.width, parsed.height) != (old_w, old_h):
            raise ValueError("candidate/DAT dimensions disagree")

        tc, toh, tnh, tneither = _changed_alignment(
            old_tile, new_tile, parsed.tile_ids
        )
        pc, poh, pnh, pneither = _changed_alignment(
            old_parts, new_parts, parsed.object_ids
        )
        rows.append(
            CandidateLineage(
                path=str(entry["path"].relative_to(server_map_root)),
                sha256=hashlib.sha256(raw).hexdigest(),
                historical_tile_diff=_diff(old_tile, parsed.tile_ids),
                historical_parts_diff=_diff(old_parts, parsed.object_ids),
                recovered25_tile_diff=_diff(new_tile, parsed.tile_ids),
                recovered25_parts_diff=_diff(new_parts, parsed.object_ids),
                changed_tile_cells=tc,
                changed_tile_match_historical=toh,
                changed_tile_match_recovered25=tnh,
                changed_tile_match_neither=tneither,
                changed_parts_cells=pc,
                changed_parts_match_historical=poh,
                changed_parts_match_recovered25=pnh,
                changed_parts_match_neither=pneither,
            )
        )

    return DuplicateFloorLineageAudit(
        floor_id=floor_id,
        historical_sha256=hashlib.sha256(old_path.read_bytes()).hexdigest(),
        recovered25_sha256=hashlib.sha256(new_path.read_bytes()).hexdigest(),
        width=old_w,
        height=old_h,
        dat_tile_diff=_diff(old_tile, new_tile),
        dat_parts_diff=_diff(old_parts, new_parts),
        dat_event_diff=_diff(old_event, new_event),
        candidates=tuple(rows),
    )


def emit(audit: DuplicateFloorLineageAudit) -> None:
    print("StoneAge duplicate-floor DAT lineage candidate audit — R1")
    print(f"FLOOR|{audit.floor_id}")
    print("EVIDENCE_ROLE|LATER_RECOVERED_LINEAGE")
    print(
        f"DAT_LINEAGE|dimensions={audit.width}x{audit.height}|"
        f"historical_2003_sha256={audit.historical_sha256}|"
        f"recovered25_sha256={audit.recovered25_sha256}|"
        f"tile_diff_cells={audit.dat_tile_diff}|"
        f"parts_diff_cells={audit.dat_parts_diff}|"
        f"event_diff_cells={audit.dat_event_diff}"
    )
    print(f"COUNT|server_candidates|{len(audit.candidates)}")
    for row in audit.candidates:
        print(
            "CANDIDATE_LINEAGE|"
            f"path={row.path}|sha256={row.sha256}|"
            f"historical_tile_diff={row.historical_tile_diff}|"
            f"historical_parts_diff={row.historical_parts_diff}|"
            f"historical_static_exact={int(row.historical_static_exact)}|"
            f"recovered25_tile_diff={row.recovered25_tile_diff}|"
            f"recovered25_parts_diff={row.recovered25_parts_diff}|"
            f"recovered25_static_exact={int(row.recovered25_static_exact)}|"
            f"changed_tile_cells={row.changed_tile_cells}|"
            f"changed_tile_match_historical={row.changed_tile_match_historical}|"
            f"changed_tile_match_recovered25={row.changed_tile_match_recovered25}|"
            f"changed_tile_match_neither={row.changed_tile_match_neither}|"
            f"changed_parts_cells={row.changed_parts_cells}|"
            f"changed_parts_match_historical={row.changed_parts_match_historical}|"
            f"changed_parts_match_recovered25={row.changed_parts_match_recovered25}|"
            f"changed_parts_match_neither={row.changed_parts_match_neither}"
        )
    exact_old = [row.path for row in audit.candidates if row.historical_static_exact]
    exact_new = [row.path for row in audit.candidates if row.recovered25_static_exact]
    print(
        "RESOLUTION|DUPLICATE_FLOOR_LINEAGE_COMPARED|"
        f"historical_exact={','.join(exact_old) or 'NONE'}|"
        f"recovered25_exact={','.join(exact_new) or 'NONE'}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--floor", type=int, default=130)
    parser.add_argument("--historical-root", type=Path, required=True)
    parser.add_argument("--recovered25-root", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze(
            floor_id=args.floor,
            historical_root=args.historical_root,
            recovered25_root=args.recovered25_root,
            server_map_root=args.server_map_root,
        )
    )


if __name__ == "__main__":
    main()
