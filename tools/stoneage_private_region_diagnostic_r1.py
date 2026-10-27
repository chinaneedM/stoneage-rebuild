"""Private source-verified recovered25 map cell diagnostics, NOT original game art.

The engine-neutral region provider has already authenticated the actual DAT or
LS2MAP map payload against the pinned later-recovered source manifest. Colors,
markers and cell widths are OBSERVER-ONLY and not part of historical StoneAge.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "stoneage.private_recovered25_map_cell_diagnostic.r1"
CLIENT = "CLIENT_DAT_THREE_PLANE"
SERVER = "SERVER_LS2MAP_TWO_PLANE"
CLIENT_EVENT = "RECOVERED_CLIENT_DAT"
SERVER_EVENT = "ABSENT_IN_LS2MAP_WORLD_EVENT_LAYER_SEPARATE"
MAX_SIDE = 64
CELL_PX = 12


def need(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)


def _id_color(tile_id: int) -> tuple[int, int, int]:
    """Intentionally arbitrary stable ID colors, never historical palette."""
    h = hashlib.sha256(b"synthetic-tile-id\0" + struct.pack("<H", tile_id)).digest()
    return (55 + h[0] % 151, 55 + h[1] % 151, 55 + h[2] % 151)


def _chunk(name: bytes, body: bytes) -> bytes:
    raw = name + body
    return struct.pack(">I", len(body)) + raw + struct.pack(">I", zlib.crc32(raw) & 0xffffffff)


def _png(rows: list[bytes], w: int, h: int, *, role: str) -> bytes:
    need(len(rows) == h and all(len(row) == w * 3 for row in rows), "bad raw PNG dimensions")
    header = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    label = b"Comment\0SYNTHETIC TILE-ID DIAGNOSTIC - NOT ORIGINAL STONEAGE GAME PIXELS"
    role_text = b"OriginalArtwork\0FALSE; EvidenceRole=" + role.encode("ascii")
    raw = b"".join(b"\0" + row for row in rows)
    return (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", header) +
            _chunk(b"tEXt", label) + _chunk(b"tEXt", role_text) +
            _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b""))


def build(materialized) -> tuple[bytes, dict]:
    """Accept only a verified engine-neutral materialization, never caller-wish labels."""
    area, request = materialized.payload, materialized.request
    provenance = dict(materialized.provenance)
    need(provenance.get("content_role") == "LATER_RECOVERED", "not authenticated later-recovered content")
    need(provenance.get("evidence_role") == "LATER_RECOVERED", "unqualified historical evidence role")
    need(provenance.get("world_profile") == "recovered25" and request.world_profile == "recovered25",
         "profile mismatch")
    need(provenance.get("payload_sha256") == area.payload_sha256 and
         re.fullmatch(r"[0-9a-f]{64}", str(area.payload_sha256)) is not None,
         "map byte SHA not matched to the provider's evidence")
    need(provenance.get("payload_kind") == area.source_kind and
         provenance.get("event_plane_status") == area.event_plane_status,
         "provider provenance disagreement")
    need(all(getattr(area, k) == getattr(request, k) for k in ("floor_id", "x1", "y1", "x2", "y2")),
         "materialized region and request disagree")
    need(0 <= area.x1 <= area.x2 < area.map_width and 0 <= area.y1 <= area.y2 < area.map_height,
         "map bounds exceeded")
    width, height = area.x2 - area.x1 + 1, area.y2 - area.y1 + 1
    need(1 <= width <= MAX_SIDE and 1 <= height <= MAX_SIDE,
         "bounded viewport must fit 64 by 64 cells")
    size = width * height
    need(len(area.tile_ids) == len(area.object_ids) == size, "tile/object incomplete")
    if area.source_kind == CLIENT:
        need(area.event_plane_status == CLIENT_EVENT and area.event_ids is not None and
             len(area.event_ids) == size, "client event plane not verified")
    elif area.source_kind == SERVER:
        need(area.event_plane_status == SERVER_EVENT and area.event_ids is None,
             "LS2MAP event plane must remain truly absent")
    else:
        raise ValueError("unsupported map source class")
    for seq in (area.tile_ids, area.object_ids, area.event_ids or ()):
        need(all(type(v) is int and 0 <= v <= 65535 for v in seq), "not uint16 map identifiers")
    cells = []
    tile_hist, object_hist, event_hist = Counter(), Counter(), Counter()
    for i in range(size):
        tile, obj = area.tile_ids[i], area.object_ids[i]
        evt = None if area.event_ids is None else area.event_ids[i]
        cells.append({"x": area.x1 + (i % width), "y": area.y1 + (i // width),
                      "tile_id": tile, "object_id": obj, "event_id": evt})
        tile_hist[tile] += 1
        if obj: object_hist[obj] += 1
        if evt is not None and evt: event_hist[evt] += 1
    pw, ph = width * CELL_PX, height * CELL_PX
    rows = []
    for py in range(ph):
        row = bytearray()
        cy, local_y = divmod(py, CELL_PX)
        for px in range(pw):
            cx, local_x = divmod(px, CELL_PX)
            i = cy * width + cx
            col = _id_color(area.tile_ids[i])
            if local_x == 0 or local_y == 0:
                col = (18, 24, 29)  # Synthetic cell grid
            elif area.object_ids[i] != 0 and 6 <= local_x <= 9 and 6 <= local_y <= 9:
                col = (255, 218, 92)  # Arbitrary object marker
            elif area.event_ids is not None and area.event_ids[i] != 0 and 2 <= local_x <= 4 and 2 <= local_y <= 4:
                col = (240, 75, 181)  # Arbitrary event marker, never drawn for LS2MAP
            row.extend(col)
        rows.append(bytes(row))
    png = _png(rows, pw, ph, role="LATER_RECOVERED")
    out = {
        "schema": SCHEMA, "source_version_role": "LATER_RECOVERED",
        "world_profile": "recovered25", "source_kind": area.source_kind,
        "event_plane_status": area.event_plane_status,
        "source_payload_sha256": area.payload_sha256,
        "source_versions": list(provenance.get("source_versions", ())),
        "floor_id": area.floor_id,
        "map_dimensions": [area.map_width, area.map_height],
        "viewport_inclusive": [area.x1, area.y1, area.x2, area.y2],
        "viewport_dimensions": [width, height], "cell_count": size,
        "observed_tile_ids": [[k, v] for k, v in sorted(tile_hist.items())],
        "observed_nonzero_object_ids": [[k, v] for k, v in sorted(object_hist.items())],
        "observed_nonzero_event_ids": None if area.event_ids is None else
             [[k, v] for k, v in sorted(event_hist.items())],
        "cells": cells, "diagnostic_png_sha256": hashlib.sha256(png).hexdigest(),
        "synthetic_cell_color_mapping": "SHA256-derived per-ID, NOT original palette",
        "object_marker": "YELLOW_OBSERVER_ONLY", "event_marker":
            "ABSENT_NOT_ZERO" if area.event_ids is None else "PINK_OBSERVER_ONLY",
        "source_artwork_rendered": False, "historical_scene_layout_verified": False,
        "original_client_executed_in_this_workflow": False,
        "original_game_world_entered": False,
        "human_viewed_export": False, "interface_language": "zh-CN",
    }
    return png, out


def export_private(target: Path, materialized) -> Path:
    """Refuse any existing files; never write commercial source bytes to public Git."""
    target = Path(target).expanduser().resolve()
    need(target.is_dir() and target != ROOT and ROOT not in target.parents and
         not any(target.iterdir()), "destination must be an empty existing private folder outside Git")
    png, meta = build(materialized)
    image_path, manifest_path = target / "tile-id-diagnostic.png", target / "source-manifest.json"
    try:
        with image_path.open("xb") as f: f.write(png)
        with manifest_path.open("x", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except BaseException:
        image_path.unlink(missing_ok=True)
        manifest_path.unlink(missing_ok=True)
        raise
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description="PRIVATE map-ID diagnostic, NOT historical game screenshot")
    parser.add_argument("--client-dat-dir", type=Path, required=True)
    parser.add_argument("--server-map-root", type=Path, required=True)
    parser.add_argument("--floor", type=int, required=True)
    parser.add_argument("--x1", type=int, required=True)
    parser.add_argument("--y1", type=int, required=True)
    parser.add_argument("--x2", type=int, required=True)
    parser.add_argument("--y2", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    need(0 <= args.x1 <= args.x2 and 0 <= args.y1 <= args.y2 and
         args.x2 - args.x1 < MAX_SIDE and args.y2 - args.y1 < MAX_SIDE,
         "request only a finite bounded 64x64 viewport")
    from tools.stoneage_local_runtime_core import WorldRegionRequest, load_runtime_bootstrap_file
    from tools.stoneage_recovered25_world_profile_adapter import Recovered25WorldProfileAdapter
    from tools.stoneage_recovered25_region_payload import Recovered25RegionPayloadSource
    root = Path(__file__).resolve().parents[1]
    profile = load_runtime_bootstrap_file(root / "game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json")
    adapter = Recovered25WorldProfileAdapter.from_repository(profile)
    source = Recovered25RegionPayloadSource(
        profile=profile, adapter=adapter, client_dat_dir=args.client_dat_dir,
        server_map_root=args.server_map_root,
    )
    materialized = source.materialize_region(WorldRegionRequest(
        floor_id=args.floor, x1=args.x1, y1=args.y1, x2=args.x2, y2=args.y2,
        world_profile=profile.runtime_world_profile,
    ))
    manifest = export_private(args.output_dir, materialized)
    print("PRIVATE_SOURCE_VERIFIED_MAP_ID_DIAGNOSTIC=" + str(manifest))
    print("NOT_ACTUAL_TILE_TEXTURES_NOT_TAIWAN_V1_ORIGINAL_GAMEPLAY")


if __name__ == "__main__":
    main()
