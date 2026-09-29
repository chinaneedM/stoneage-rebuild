#!/usr/bin/env python3
"""Audit runtime-reachable recovered25 supplemental world floors.

The input floor set comes from the closed runtime-valid reachability report.
For each supplemental floor this probe binds:
- recovered server-map copy identity (path, SHA-256, dimensions);
- duplicate-copy equivalence vs divergence;
- mapset-backed static collision materializability;
- derived NPC/Warp and encounter coverage.

Divergent duplicate server copies are never selected automatically.
All rows remain recovered25 / LATER_RECOVERED.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_client_server_map_probe import collect_server_maps
from tools.stoneage_server_static_map import (
    parse_ls2map,
    parse_mapset_collision_profile,
    summarize_static_collision,
)
from tools.stoneage_world_content_coverage_probe import (
    _encounter_floor_counts,
    _npc_floor_counts,
)


SOURCE_VERSION = "recovered25"
EVIDENCE_ROLE = "LATER_RECOVERED"

UNIQUE = "UNIQUE"
DUPLICATE_IDENTICAL = "DUPLICATE_IDENTICAL"
DUPLICATE_DIVERGENT = "DUPLICATE_DIVERGENT"

INPUT_RESOLUTION = "RESOLUTION|RECOVERED_RUNTIME_CLASSIC_WARP_REACHABILITY_CLOSED"
OUTPUT_RESOLUTION = "RESOLUTION|SUPPLEMENTAL_WORLD_AUDIT_CLASSIFIED"


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


@dataclass(frozen=True)
class SupplementalFloorTarget:
    floor_id: int
    depth: int
    status: str
    incoming_reachable_warps: int
    outgoing_runtime_warps: int


def parse_supplemental_targets(text: str) -> tuple[SupplementalFloorTarget, ...]:
    source_version: str | None = None
    evidence_role: str | None = None
    declared: int | None = None
    rows: list[SupplementalFloorTarget] = []
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
        if line.startswith("COUNT|supplemental_floor_ids|"):
            declared = int(line.rsplit("|", 1)[1])
            continue
        if line.startswith("SUPPLEMENTAL_FLOOR|"):
            fields = _fields(line, "SUPPLEMENTAL_FLOOR")
            if fields.get("server_map") != "1":
                raise ValueError(
                    "runtime supplemental floor unexpectedly lacks server map"
                )
            rows.append(
                SupplementalFloorTarget(
                    floor_id=int(fields["floor"]),
                    depth=int(fields["depth"]),
                    status=fields["status"],
                    incoming_reachable_warps=int(
                        fields["incoming_reachable_warps"]
                    ),
                    outgoing_runtime_warps=int(
                        fields["outgoing_runtime_warps"]
                    ),
                )
            )
            continue
        if line == INPUT_RESOLUTION:
            resolution = True

    if source_version != SOURCE_VERSION:
        raise ValueError("supplemental reachability source version drift")
    if evidence_role != EVIDENCE_ROLE:
        raise ValueError("supplemental reachability evidence-role drift")
    if not resolution:
        raise ValueError("supplemental reachability report is not closed")
    if declared is None or declared != len(rows):
        raise ValueError("supplemental target detail count drift")
    ids = [row.floor_id for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("supplemental reachability contains duplicate floors")
    return tuple(rows)


@dataclass(frozen=True)
class SupplementalFloorAudit:
    target: SupplementalFloorTarget
    copy_status: str
    server_paths: tuple[str, ...]
    server_sha256s: tuple[str, ...]
    server_dimensions: tuple[tuple[int, int], ...]
    static_materializable: bool
    cells: int | None
    missing_image_ids: int | None
    ordinary_walkable_cells: int | None
    flying_walkable_cells: int | None
    npc_create_count: int
    warp_functionset_create_count: int
    encounter_row_count: int
    active_encounter_row_count: int

    def __post_init__(self) -> None:
        if self.copy_status not in {
            UNIQUE,
            DUPLICATE_IDENTICAL,
            DUPLICATE_DIVERGENT,
        }:
            raise ValueError("invalid supplemental server-copy status")
        if len(self.server_paths) == 0:
            raise ValueError("supplemental floor requires server-map evidence")
        if len(self.server_paths) != len(self.server_sha256s):
            raise ValueError("server path/hash count drift")
        if len(self.server_paths) != len(self.server_dimensions):
            raise ValueError("server path/dimension count drift")
        if self.copy_status == UNIQUE and len(self.server_paths) != 1:
            raise ValueError("UNIQUE supplemental floor must have one copy")
        if self.copy_status != UNIQUE and len(self.server_paths) < 2:
            raise ValueError("duplicate supplemental floor needs multiple copies")
        if self.copy_status == DUPLICATE_DIVERGENT and self.static_materializable:
            raise ValueError("divergent server copies cannot be auto-materialized")


@dataclass(frozen=True)
class SupplementalWorldAudit:
    floors: tuple[SupplementalFloorAudit, ...]
    mapset_sha256: str
    encounter_file_name: str

    def __post_init__(self) -> None:
        ids = [row.target.floor_id for row in self.floors]
        if len(ids) != len(set(ids)):
            raise ValueError("supplemental audit contains duplicate floors")

    @property
    def counts(self) -> dict[str, int]:
        rows = self.floors
        out = {
            "supplemental_floor_ids": len(rows),
            "static_materializable_floors": sum(
                row.static_materializable for row in rows
            ),
            "static_unresolved_floors": sum(
                not row.static_materializable for row in rows
            ),
            "floors_with_npc": sum(row.npc_create_count > 0 for row in rows),
            "floors_with_warp_functionset": sum(
                row.warp_functionset_create_count > 0 for row in rows
            ),
            "floors_with_encounter": sum(
                row.encounter_row_count > 0 for row in rows
            ),
            "floors_with_active_encounter": sum(
                row.active_encounter_row_count > 0 for row in rows
            ),
            "npc_create_count": sum(row.npc_create_count for row in rows),
            "warp_functionset_create_count": sum(
                row.warp_functionset_create_count for row in rows
            ),
            "encounter_rows": sum(row.encounter_row_count for row in rows),
            "active_encounter_rows": sum(
                row.active_encounter_row_count for row in rows
            ),
        }
        for status in (UNIQUE, DUPLICATE_IDENTICAL, DUPLICATE_DIVERGENT):
            out[f"server_copy_status:{status}:ids"] = sum(
                row.copy_status == status for row in rows
            )

        materialized = [row for row in rows if row.static_materializable]
        out["materialized_cells"] = sum(int(row.cells or 0) for row in materialized)
        out["materialized_ordinary_walkable_cells"] = sum(
            int(row.ordinary_walkable_cells or 0) for row in materialized
        )
        out["materialized_flying_walkable_cells"] = sum(
            int(row.flying_walkable_cells or 0) for row in materialized
        )
        out["materialized_floors_with_missing_image_metadata"] = sum(
            int(row.missing_image_ids or 0) > 0 for row in materialized
        )
        return out


def _copy_identity(entries, server_map_root: Path):
    rows = []
    for entry in entries:
        path = entry["path"]
        raw = path.read_bytes()
        rows.append(
            (
                str(path.relative_to(server_map_root)),
                hashlib.sha256(raw).hexdigest(),
                (int(entry["width"]), int(entry["height"])),
                raw,
            )
        )
    rows.sort(key=lambda row: row[0].lower())
    return tuple(rows)


def analyze(
    *,
    reachability_text: str,
    server_map_root: Path,
    mapset_path: Path,
    npc_dir: Path,
    data_dir: Path,
    setup: Path | None,
) -> SupplementalWorldAudit:
    targets = parse_supplemental_targets(reachability_text)
    target_ids = {row.floor_id for row in targets}

    server_by_id, _total, _ls2, _invalid = collect_server_maps(
        server_map_root,
        sample_limit=0,
    )
    missing_server = sorted(target_ids - set(server_by_id))
    if missing_server:
        raise ValueError(
            f"supplemental floors missing recovered server maps: {missing_server}"
        )

    mapset = parse_mapset_collision_profile(mapset_path.read_bytes())
    npc_counts, warp_counts = _npc_floor_counts(npc_dir, set(server_by_id))
    encounter_name, encounter_counts, active_encounter_counts = (
        _encounter_floor_counts(data_dir, setup)
    )

    floors: list[SupplementalFloorAudit] = []
    for target in targets:
        identity = _copy_identity(
            tuple(server_by_id[target.floor_id]),
            server_map_root,
        )
        paths = tuple(row[0] for row in identity)
        hashes = tuple(row[1] for row in identity)
        dimensions = tuple(row[2] for row in identity)

        if len(identity) == 1:
            copy_status = UNIQUE
        elif len(set(hashes)) == 1 and len(set(dimensions)) == 1:
            copy_status = DUPLICATE_IDENTICAL
        else:
            copy_status = DUPLICATE_DIVERGENT

        materializable = False
        cells = None
        missing_image_ids = None
        ordinary = None
        flying = None

        if copy_status != DUPLICATE_DIVERGENT:
            chosen_raw = identity[0][3]
            parsed = parse_ls2map(chosen_raw)
            if parsed.floor_id != target.floor_id:
                raise ValueError(
                    f"supplemental LS2MAP embedded floor drift: {target.floor_id}"
                )
            summary = summarize_static_collision(parsed, mapset)
            missing_image_ids = len(summary.missing_image_ids)
            cells = summary.cells
            ordinary = summary.ordinary_walkable_cells
            flying = summary.flying_walkable_cells
            materializable = (
                missing_image_ids == 0
                and ordinary is not None
                and flying is not None
            )

        floors.append(
            SupplementalFloorAudit(
                target=target,
                copy_status=copy_status,
                server_paths=paths,
                server_sha256s=hashes,
                server_dimensions=dimensions,
                static_materializable=materializable,
                cells=cells,
                missing_image_ids=missing_image_ids,
                ordinary_walkable_cells=ordinary,
                flying_walkable_cells=flying,
                npc_create_count=int(npc_counts.get(target.floor_id, 0)),
                warp_functionset_create_count=int(
                    warp_counts.get(target.floor_id, 0)
                ),
                encounter_row_count=int(
                    encounter_counts.get(target.floor_id, 0)
                ),
                active_encounter_row_count=int(
                    active_encounter_counts.get(target.floor_id, 0)
                ),
            )
        )

    return SupplementalWorldAudit(
        floors=tuple(floors),
        mapset_sha256=mapset.payload_sha256,
        encounter_file_name=encounter_name,
    )


def _dims(values: tuple[tuple[int, int], ...]) -> str:
    return ",".join(f"{width}x{height}" for width, height in values)


def emit(audit: SupplementalWorldAudit) -> None:
    print("StoneAge runtime-reachable supplemental world audit — R1")
    print(
        "SCOPE|66 recovered25 supplemental floors|server-copy identity + "
        "static collision + floor gameplay coverage"
    )
    print(f"SEMANTIC_SOURCE_VERSION|{SOURCE_VERSION}")
    print(f"EVIDENCE_ROLE|{EVIDENCE_ROLE}")
    print(
        "RULE|divergent duplicate server copies remain unresolved and are never "
        "selected automatically"
    )
    print(f"MAPSET_SHA256|{audit.mapset_sha256}")
    print(f"ACTIVE_ENCOUNT_FILE|{audit.encounter_file_name}")
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    for row in audit.floors:
        target = row.target
        print(
            "SUPPLEMENTAL_AUDIT|"
            f"floor={target.floor_id}|depth={target.depth}|"
            f"reachability_status={target.status}|"
            f"incoming_reachable_warps={target.incoming_reachable_warps}|"
            f"outgoing_runtime_warps={target.outgoing_runtime_warps}|"
            f"server_copy_count={len(row.server_paths)}|"
            f"server_copy_status={row.copy_status}|"
            f"server_paths={','.join(row.server_paths)}|"
            f"server_dimensions={_dims(row.server_dimensions)}|"
            f"server_sha256s={','.join(row.server_sha256s)}|"
            f"static_materializable={int(row.static_materializable)}|"
            f"cells={row.cells if row.cells is not None else 'UNKNOWN'}|"
            f"missing_image_ids={row.missing_image_ids if row.missing_image_ids is not None else 'UNKNOWN'}|"
            f"ordinary_walkable_cells={row.ordinary_walkable_cells if row.ordinary_walkable_cells is not None else 'UNKNOWN'}|"
            f"flying_walkable_cells={row.flying_walkable_cells if row.flying_walkable_cells is not None else 'UNKNOWN'}|"
            f"npc_create_count={row.npc_create_count}|"
            f"warp_functionset_create_count={row.warp_functionset_create_count}|"
            f"encounter_rows={row.encounter_row_count}|"
            f"active_encounter_rows={row.active_encounter_row_count}"
        )

    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reachability-report", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    parser.add_argument("--mapset", type=Path, required=True)
    parser.add_argument("--npc-dir", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()

    emit(
        analyze(
            reachability_text=args.reachability_report.read_text(
                encoding="utf-8"
            ),
            server_map_root=args.server_map_root,
            mapset_path=args.mapset,
            npc_dir=args.npc_dir,
            data_dir=args.data_dir,
            setup=args.setup,
        )
    )


if __name__ == "__main__":
    main()
