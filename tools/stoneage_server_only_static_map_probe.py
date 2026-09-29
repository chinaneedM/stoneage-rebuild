#!/usr/bin/env python3
"""Validate server-only recovered floors as engine-neutral static maps.

Only derived counts, hashes and dimensions are emitted. Raw tile/object planes
and mapset rows are never written to the report.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_server_static_map import (
    parse_ls2map,
    parse_mapset_collision_profile,
    summarize_static_collision,
)


REPORT_RESOLUTION = "RESOLUTION|MISSING_DAT_WARP_DESTINATION_PAYLOADS_CLASSIFIED"
OUTPUT_RESOLUTION = "RESOLUTION|SERVER_ONLY_STATIC_MAPS_MATERIALIZABLE"


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
class ServerOnlyStaticTarget:
    floor_id: int
    path: str
    width: int
    height: int
    sha256: str


def parse_targets(text: str) -> tuple[ServerOnlyStaticTarget, ...]:
    evidence_role: str | None = None
    declared_ids: int | None = None
    rows: list[ServerOnlyStaticTarget] = []
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("EVIDENCE_ROLE|"):
            evidence_role = line.split("|", 1)[1]
            continue
        if line.startswith("COUNT|status:SERVER_MAP_ONLY:ids|"):
            declared_ids = int(line.rsplit("|", 1)[1])
            continue
        if line.startswith("MISSING_DAT_DESTINATION|"):
            fields = _fields(line, "MISSING_DAT_DESTINATION")
            if fields.get("status") != "SERVER_MAP_ONLY":
                continue
            paths = tuple(p for p in fields.get("server_map_paths", "").split(",") if p)
            dims = tuple(p for p in fields.get("server_map_dimensions", "").split(",") if p)
            hashes = tuple(p for p in fields.get("server_map_sha256", "").split(",") if p)
            if len(paths) != 1 or len(dims) != 1 or len(hashes) != 1:
                raise ValueError("server-only static target requires one path/dimension/hash")
            if "x" not in dims[0]:
                raise ValueError("server-only dimension is malformed")
            width, height = (int(v) for v in dims[0].split("x", 1))
            digest = hashes[0].lower()
            if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError("server-only target SHA-256 is malformed")
            rows.append(
                ServerOnlyStaticTarget(
                    floor_id=int(fields["floor"]),
                    path=paths[0],
                    width=width,
                    height=height,
                    sha256=digest,
                )
            )
            continue
        if line == REPORT_RESOLUTION:
            resolution = True

    if evidence_role != "LATER_RECOVERED":
        raise ValueError("server-only target evidence must remain LATER_RECOVERED")
    if not resolution:
        raise ValueError("server-only payload report is not closed")
    if declared_ids is None or declared_ids != len(rows):
        raise ValueError("server-only target count drift")
    if len({row.floor_id for row in rows}) != len(rows):
        raise ValueError("duplicate server-only target floor")
    return tuple(rows)


@dataclass(frozen=True)
class ServerOnlyStaticAudit:
    rows: tuple
    mapset_sha256: str
    mapset_rows: int
    mapset_unique_images: int
    mapset_duplicate_ids: int

    @property
    def counts(self) -> dict[str, int]:
        used_union = set()
        # Row summaries intentionally expose only counts, so recompute aggregate
        # image-id cardinality is not possible here; callers set it separately.
        out = {
            "target_floors": len(self.rows),
            "total_cells": sum(row.cells for row in self.rows),
            "floors_with_missing_image_metadata": sum(
                bool(row.missing_image_ids) for row in self.rows
            ),
            "missing_image_id_references_unique_floor_sum": sum(
                len(row.missing_image_ids) for row in self.rows
            ),
            "mapset_rows": self.mapset_rows,
            "mapset_unique_images": self.mapset_unique_images,
            "mapset_duplicate_ids": self.mapset_duplicate_ids,
        }
        ordinary = [row.ordinary_walkable_cells for row in self.rows]
        flying = [row.flying_walkable_cells for row in self.rows]
        if all(value is not None for value in ordinary):
            out["ordinary_walkable_cells"] = sum(int(value) for value in ordinary)
            out["ordinary_blocked_cells"] = out["total_cells"] - out["ordinary_walkable_cells"]
        if all(value is not None for value in flying):
            out["flying_walkable_cells"] = sum(int(value) for value in flying)
            out["flying_blocked_cells"] = out["total_cells"] - out["flying_walkable_cells"]
        return out


def analyze(
    *,
    payload_report_text: str,
    server_map_root: Path,
    mapset_path: Path,
) -> ServerOnlyStaticAudit:
    targets = parse_targets(payload_report_text)
    mapset = parse_mapset_collision_profile(mapset_path.read_bytes())
    summaries = []

    for target in targets:
        path = server_map_root / target.path
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != target.sha256:
            raise ValueError(f"server map SHA drift for floor {target.floor_id}")
        parsed = parse_ls2map(raw)
        if parsed.floor_id != target.floor_id:
            raise ValueError(f"embedded floor id drift for {target.floor_id}")
        if (parsed.width, parsed.height) != (target.width, target.height):
            raise ValueError(f"server map dimension drift for floor {target.floor_id}")
        summaries.append(summarize_static_collision(parsed, mapset))

    return ServerOnlyStaticAudit(
        rows=tuple(summaries),
        mapset_sha256=mapset.payload_sha256,
        mapset_rows=mapset.row_count,
        mapset_unique_images=len(mapset.images),
        mapset_duplicate_ids=len(mapset.duplicate_image_ids),
    )


def emit(audit: ServerOnlyStaticAudit) -> None:
    print("StoneAge server-only static map materialization audit — R1")
    print(
        "SCOPE|server-only recovered25 floors|LS2MAP tile/object + mapset "
        "WALKABLE/HAVEHEIGHT|derived counts/hashes only"
    )
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(f"MAPSET_SHA256|{audit.mapset_sha256}")
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.rows:
        print(
            "FLOOR|"
            f"floor={row.floor_id}|width={row.width}|height={row.height}|"
            f"cells={row.cells}|unique_tile_ids={row.unique_tile_ids}|"
            f"unique_object_ids={row.unique_object_ids}|"
            f"used_image_ids={row.used_image_ids}|"
            f"missing_image_ids={len(row.missing_image_ids)}|"
            f"duplicate_mapset_ids_used={len(row.duplicate_mapset_ids_used)}|"
            f"ordinary_walkable_cells={row.ordinary_walkable_cells if row.ordinary_walkable_cells is not None else 'UNKNOWN'}|"
            f"flying_walkable_cells={row.flying_walkable_cells if row.flying_walkable_cells is not None else 'UNKNOWN'}|"
            f"server_map_sha256={row.server_map_sha256}"
        )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload-report", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    parser.add_argument("--mapset", type=Path, required=True)
    args = parser.parse_args()
    emit(
        analyze(
            payload_report_text=args.payload_report.read_text(encoding="utf-8"),
            server_map_root=args.server_map_root,
            mapset_path=args.mapset,
        )
    )


if __name__ == "__main__":
    main()
