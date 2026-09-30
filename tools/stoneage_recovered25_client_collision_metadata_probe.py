#!/usr/bin/env python3
"""Audit recovered25 client ADRN metadata coverage for server-collision gaps.

This is a provenance/coverage probe, not a claim that Taiwan-v1 collision
semantics automatically apply to recovered25. It asks only whether the
recovered25 client DAT graphics referenced by server-uncovered materializable
floors have corresponding records in the recovered25 client adrn_15.bin
80-byte resource.

No proprietary DAT/ADRN payload bytes are emitted.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from tools.stoneage_dat_probe import load_adrn
from tools.stoneage_local_runtime_core import load_runtime_bootstrap_file
from tools.stoneage_recovered25_region_payload import Recovered25RegionPayloadSource
from tools.stoneage_recovered25_server_collision_provider import (
    Recovered25ServerCollisionProvider,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    Recovered25WorldProfileAdapter,
)


METADATA_COMPLETE = "RECOVERED25_ADRN_METADATA_COMPLETE"
MISSING_ADRN_GRAPHICS = "MISSING_RECOVERED25_ADRN_GRAPHICS"
NOT_CLIENT_DAT_STABLE_FLOOR = "NOT_CLIENT_DAT_STABLE_FLOOR"

OUTPUT_RESOLUTION = "RESOLUTION|RECOVERED25_CLIENT_COLLISION_METADATA_COVERAGE_AUDITED"


def _uses_adrn(value: int) -> bool:
    value = int(value)
    return value > 99 or 60 <= value <= 79


@dataclass(frozen=True)
class ClientCollisionMetadataRow:
    floor_id: int
    status: str
    missing_unique_graphics: int
    missing_graphic_refs: int


@dataclass(frozen=True)
class ClientCollisionMetadataAudit:
    rows: tuple[ClientCollisionMetadataRow, ...]
    adrn_sha256: str
    adrn_bytes: int
    adrn_records: int
    adrn_index_size: int
    adrn_duplicate_assignments: int

    @property
    def counts(self):
        c = Counter()
        c["server_collision_gap_floors"] = len(self.rows)
        for row in self.rows:
            c[f"status:{row.status}"] += 1
            c["missing_graphic_refs"] += row.missing_graphic_refs
            c["missing_unique_graphics_floor_sum"] += row.missing_unique_graphics
        return c


def analyze(
    *,
    client_dat_dir: Path,
    client_adrn: Path,
    server_map_root: Path,
    mapset_path: Path,
) -> ClientCollisionMetadataAudit:
    root = Path(__file__).resolve().parents[1]
    profile = load_runtime_bootstrap_file(
        root / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
    )
    adapter = Recovered25WorldProfileAdapter.from_repository(profile)
    regions = Recovered25RegionPayloadSource(
        profile=profile,
        adapter=adapter,
        client_dat_dir=client_dat_dir,
        server_map_root=server_map_root,
    )
    server_collision = Recovered25ServerCollisionProvider(
        profile=profile,
        adapter=adapter,
        server_map_root=server_map_root,
        mapset_path=mapset_path,
    )
    adrn_path = Path(client_adrn)
    adrn_raw = adrn_path.read_bytes()
    adrn = load_adrn(adrn_path)
    adrn_keys = set(int(k) for k in adrn["by_bmp"])

    rows = []
    for floor_id in sorted(server_collision.unsupported_floor_ids):
        if floor_id not in regions.plan.stable_dat_floor_ids:
            rows.append(
                ClientCollisionMetadataRow(
                    floor_id=floor_id,
                    status=NOT_CLIENT_DAT_STABLE_FLOOR,
                    missing_unique_graphics=0,
                    missing_graphic_refs=0,
                )
            )
            continue

        _w, _h, tile, parts, _event, _digest, _kind, _event_status = (
            regions._full_payload(floor_id)
        )
        missing = Counter(
            int(value)
            for value in tuple(tile) + tuple(parts)
            if _uses_adrn(value) and int(value) not in adrn_keys
        )
        rows.append(
            ClientCollisionMetadataRow(
                floor_id=floor_id,
                status=(
                    METADATA_COMPLETE
                    if not missing
                    else MISSING_ADRN_GRAPHICS
                ),
                missing_unique_graphics=len(missing),
                missing_graphic_refs=sum(missing.values()),
            )
        )

    return ClientCollisionMetadataAudit(
        rows=tuple(rows),
        adrn_sha256=hashlib.sha256(adrn_raw).hexdigest(),
        adrn_bytes=len(adrn_raw),
        adrn_records=int(adrn["records"]),
        adrn_index_size=len(adrn["by_bmp"]),
        adrn_duplicate_assignments=int(adrn["duplicate"]),
    )


def emit(audit: ClientCollisionMetadataAudit) -> None:
    print("StoneAge recovered25 client collision metadata coverage — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|metadata coverage only; this report does not promote Taiwan-v1 "
        "readHitMap semantics into recovered25"
    )
    print(f"ADRN_SHA256|{audit.adrn_sha256}")
    print(f"ADRN_BYTES|{audit.adrn_bytes}")
    print(f"ADRN_RECORDS|{audit.adrn_records}")
    print(f"ADRN_INDEX_SIZE|{audit.adrn_index_size}")
    print(f"ADRN_DUPLICATE_ASSIGNMENTS|{audit.adrn_duplicate_assignments}")
    for key, value in sorted(audit.counts.items()):
        print(f"COUNT|{key}|{value}")
    for status in (
        MISSING_ADRN_GRAPHICS,
        NOT_CLIENT_DAT_STABLE_FLOOR,
    ):
        ids = [str(row.floor_id) for row in audit.rows if row.status == status]
        print(f"FLOOR_IDS|status:{status}|{','.join(ids)}")
    print(OUTPUT_RESOLUTION)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-dat-dir", type=Path, required=True)
    ap.add_argument("--client-adrn", type=Path, required=True)
    ap.add_argument("--server-map-root", type=Path, required=True)
    ap.add_argument("--mapset", type=Path, required=True)
    args = ap.parse_args()
    emit(
        analyze(
            client_dat_dir=args.client_dat_dir,
            client_adrn=args.client_adrn,
            server_map_root=args.server_map_root,
            mapset_path=args.mapset,
        )
    )


if __name__ == "__main__":
    main()
