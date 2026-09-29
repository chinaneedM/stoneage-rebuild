#!/usr/bin/env python3
"""Audit payload presence for classic-warp destinations with no client DAT.

Input is the first-stage outside-stable destination audit. Only rows already
classified CLIENT_DAT_MISSING are inspected here. The audit checks independent
recovered-2.5 payload surfaces:
- numeric client .MAP files;
- server LS2MAP files by embedded map id.

Presence on either surface is later recovered evidence only and does not prove
Taiwan-v1 membership. No map payload bytes or server name bytes are emitted.
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


CLIENT_MAP_AND_SERVER_MAP_PRESENT = "CLIENT_MAP_AND_SERVER_MAP_PRESENT"
CLIENT_MAP_ONLY = "CLIENT_MAP_ONLY"
SERVER_MAP_ONLY = "SERVER_MAP_ONLY"
NO_CLIENT_MAP_OR_SERVER_MAP = "NO_CLIENT_MAP_OR_SERVER_MAP"


def _fields(line: str, prefix: str) -> dict[str, str]:
    parts = line.split("|")
    if not parts or parts[0] != prefix:
        raise ValueError(f"expected {prefix} record")
    out: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"malformed {prefix} field: {part}")
        key, value = part.split("=", 1)
        if not key or key in out:
            raise ValueError(f"duplicate/blank {prefix} field: {key}")
        out[key] = value
    return out


def parse_missing_dat_destinations(text: str) -> dict[int, int]:
    declared_ids: int | None = None
    declared_edges: int | None = None
    rows: dict[int, int] = {}
    resolution = False

    for raw in str(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("COUNT|status:CLIENT_DAT_MISSING:ids|"):
            declared_ids = int(line.rsplit("|", 1)[1])
            continue
        if line.startswith("COUNT|status:CLIENT_DAT_MISSING:edges|"):
            declared_edges = int(line.rsplit("|", 1)[1])
            continue
        if line.startswith("DESTINATION|"):
            fields = _fields(line, "DESTINATION")
            if fields.get("status") != "CLIENT_DAT_MISSING":
                continue
            floor_id = int(fields["floor"])
            if floor_id in rows:
                raise ValueError(f"duplicate missing-DAT floor {floor_id}")
            rows[floor_id] = int(fields["edge_refs"])
            continue
        if line == "RESOLUTION|OUTSIDE_STABLE_WARP_DESTINATIONS_CLASSIFIED":
            resolution = True

    if not resolution:
        raise ValueError("outside-stable destination audit is not closed")
    if declared_ids is None or declared_edges is None:
        raise ValueError("outside-stable audit lacks missing-DAT counts")
    if declared_ids != len(rows):
        raise ValueError("missing-DAT destination detail count drift")
    if declared_edges != sum(rows.values()):
        raise ValueError("missing-DAT edge count drift")
    return rows


def collect_numeric_client_maps(root: Path) -> dict[int, tuple[Path, ...]]:
    grouped: dict[int, list[Path]] = {}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() != ".map":
            continue
        try:
            floor_id = int(path.stem)
        except ValueError:
            continue
        grouped.setdefault(floor_id, []).append(path)
    return {
        floor_id: tuple(sorted(paths, key=lambda p: str(p).lower()))
        for floor_id, paths in grouped.items()
    }


@dataclass(frozen=True)
class MissingWarpDestinationPayload:
    floor_id: int
    edge_refs: int
    status: str
    client_map_paths: tuple[str, ...]
    client_map_dimensions: tuple[tuple[int, int], ...]
    client_map_sha256: tuple[str, ...]
    server_map_paths: tuple[str, ...]
    server_map_dimensions: tuple[tuple[int, int], ...]

    @property
    def client_map_present(self) -> bool:
        return bool(self.client_map_paths)

    @property
    def server_map_present(self) -> bool:
        return bool(self.server_map_paths)


@dataclass(frozen=True)
class MissingWarpDestinationPayloadAudit:
    rows: tuple[MissingWarpDestinationPayload, ...]

    @property
    def counts(self) -> dict[str, int]:
        out = {
            "missing_dat_destination_ids": len(self.rows),
            "missing_dat_edges": sum(row.edge_refs for row in self.rows),
        }
        for row in self.rows:
            out[f"status:{row.status}:ids"] = (
                out.get(f"status:{row.status}:ids", 0) + 1
            )
            out[f"status:{row.status}:edges"] = (
                out.get(f"status:{row.status}:edges", 0) + row.edge_refs
            )
            for surface, present in (
                ("client_map_present", row.client_map_present),
                ("server_map_present", row.server_map_present),
            ):
                key_ids = f"{surface}:{int(present)}:ids"
                key_edges = f"{surface}:{int(present)}:edges"
                out[key_ids] = out.get(key_ids, 0) + 1
                out[key_edges] = out.get(key_edges, 0) + row.edge_refs
        return out


def classify(
    *,
    first_stage_text: str,
    client_map_root: Path,
    server_map_root: Path,
) -> MissingWarpDestinationPayloadAudit:
    missing = parse_missing_dat_destinations(first_stage_text)
    client_maps = collect_numeric_client_maps(client_map_root)
    server_by_id, _, _, _ = collect_server_maps(
        server_map_root,
        sample_limit=0,
    )

    rows: list[MissingWarpDestinationPayload] = []
    for floor_id in sorted(missing):
        client_paths = client_maps.get(floor_id, ())
        client_dims: list[tuple[int, int]] = []
        client_hashes: list[str] = []
        for path in client_paths:
            width, height, _ = read_client_map(path)
            client_dims.append((int(width), int(height)))
            client_hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())

        server_entries = tuple(server_by_id.get(floor_id, ()))
        server_paths = tuple(
            str(entry["path"].relative_to(server_map_root))
            for entry in server_entries
        )
        server_dims = tuple(
            (int(entry["width"]), int(entry["height"]))
            for entry in server_entries
        )

        has_client = bool(client_paths)
        has_server = bool(server_entries)
        if has_client and has_server:
            status = CLIENT_MAP_AND_SERVER_MAP_PRESENT
        elif has_client:
            status = CLIENT_MAP_ONLY
        elif has_server:
            status = SERVER_MAP_ONLY
        else:
            status = NO_CLIENT_MAP_OR_SERVER_MAP

        rows.append(
            MissingWarpDestinationPayload(
                floor_id=floor_id,
                edge_refs=missing[floor_id],
                status=status,
                client_map_paths=tuple(
                    str(path.relative_to(client_map_root))
                    for path in client_paths
                ),
                client_map_dimensions=tuple(client_dims),
                client_map_sha256=tuple(client_hashes),
                server_map_paths=server_paths,
                server_map_dimensions=server_dims,
            )
        )

    return MissingWarpDestinationPayloadAudit(rows=tuple(rows))


def _dims(value: tuple[tuple[int, int], ...]) -> str:
    return ",".join(f"{w}x{h}" for w, h in value)


def emit(audit: MissingWarpDestinationPayloadAudit) -> None:
    print("StoneAge missing-DAT warp destination payload audit — R1")
    print(
        "SCOPE|outside-stable classic-Warp destinations with no recovered25 "
        "client DAT|client-MAP+server-LS2MAP-presence"
    )
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|payload presence on recovered25 surfaces does not prove "
        "Taiwan-v1 historical membership"
    )
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")
    for row in audit.rows:
        print(
            "MISSING_DAT_DESTINATION|"
            f"floor={row.floor_id}|edge_refs={row.edge_refs}|"
            f"status={row.status}|"
            f"client_map_paths={','.join(row.client_map_paths)}|"
            f"client_map_dimensions={_dims(row.client_map_dimensions)}|"
            f"client_map_sha256={','.join(row.client_map_sha256)}|"
            f"server_map_paths={','.join(row.server_map_paths)}|"
            f"server_map_dimensions={_dims(row.server_map_dimensions)}"
        )
    print("RESOLUTION|MISSING_DAT_WARP_DESTINATION_PAYLOADS_CLASSIFIED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-stage-report", type=Path, required=True)
    parser.add_argument("--client-map-root", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    args = parser.parse_args()

    audit = classify(
        first_stage_text=args.first_stage_report.read_text(encoding="utf-8"),
        client_map_root=args.client_map_root,
        server_map_root=args.server_map_root,
    )
    emit(audit)


if __name__ == "__main__":
    main()
