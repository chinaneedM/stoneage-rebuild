#!/usr/bin/env python3
"""Audit recovered25 client-ADRN collision-attribute coverage.

Scope: the materializable recovered25 stable DAT floors that are not covered by
an unambiguous recovered server LS2MAP collision source.

This audit asks only whether every tile/parts id that the established StoneAge
client hit-map family treats as ADRN-backed has a same-bundle recovered25
adrn_15.bin mapping. It does not promote Taiwan-v1 readHitMap behavior into the
recovered25 runtime algorithm.

Only derived counts and unresolved floor/id summaries are emitted.
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


OUTPUT_RESOLUTION = "RESOLUTION|RECOVERED25_CLIENT_ADRN_COLLISION_COVERAGE_AUDITED"


def requires_adrn_lookup(value: int) -> bool:
    value = int(value)
    return value > 99 or 60 <= value <= 79


@dataclass(frozen=True)
class ClientAdrnFloorCoverage:
    floor_id: int
    tile_required_refs: int
    parts_required_refs: int
    tile_required_ids: int
    parts_required_ids: int
    unresolved_ids: tuple[int, ...]

    @property
    def closed(self) -> bool:
        return not self.unresolved_ids


@dataclass(frozen=True)
class ClientAdrnCoverageAudit:
    rows: tuple[ClientAdrnFloorCoverage, ...]
    adrn_sha256: str
    adrn_bytes: int
    adrn_records: int
    adrn_index_size: int
    adrn_duplicate_map_numbers: int

    @property
    def counts(self) -> Counter:
        out = Counter()
        out["server_uncovered_floors"] = len(self.rows)
        out["client_adrn_closed_floors"] = sum(row.closed for row in self.rows)
        out["client_adrn_unresolved_floors"] = sum(not row.closed for row in self.rows)
        out["tile_required_refs"] = sum(row.tile_required_refs for row in self.rows)
        out["parts_required_refs"] = sum(row.parts_required_refs for row in self.rows)
        out["tile_required_unique_floor_sum"] = sum(
            row.tile_required_ids for row in self.rows
        )
        out["parts_required_unique_floor_sum"] = sum(
            row.parts_required_ids for row in self.rows
        )
        out["unresolved_unique_floor_sum"] = sum(
            len(row.unresolved_ids) for row in self.rows
        )
        out["adrn_records"] = self.adrn_records
        out["adrn_index_size"] = self.adrn_index_size
        out["adrn_duplicate_map_numbers"] = self.adrn_duplicate_map_numbers
        return out


def classify_planes(
    *,
    floor_id: int,
    tile,
    parts,
    adrn_map_numbers: set[int],
) -> ClientAdrnFloorCoverage:
    tile_required = [int(v) for v in tile if requires_adrn_lookup(v)]
    parts_required = [int(v) for v in parts if requires_adrn_lookup(v)]
    tile_ids = set(tile_required)
    parts_ids = set(parts_required)
    unresolved = sorted((tile_ids | parts_ids) - set(adrn_map_numbers))
    return ClientAdrnFloorCoverage(
        floor_id=int(floor_id),
        tile_required_refs=len(tile_required),
        parts_required_refs=len(parts_required),
        tile_required_ids=len(tile_ids),
        parts_required_ids=len(parts_ids),
        unresolved_ids=tuple(unresolved),
    )


def analyze(
    *,
    client_dat_dir: Path,
    server_map_root: Path,
    mapset_path: Path,
    adrn_path: Path,
) -> ClientAdrnCoverageAudit:
    root = Path(__file__).resolve().parents[1]
    profile = load_runtime_bootstrap_file(
        root / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
    )
    adapter = Recovered25WorldProfileAdapter.from_repository(profile)
    region = Recovered25RegionPayloadSource(
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

    raw_adrn = Path(adrn_path).read_bytes()
    adrn = load_adrn(Path(adrn_path))
    adrn_ids = set(int(v) for v in adrn["by_bmp"])
    unsupported = sorted(server_collision.unsupported_floor_ids)

    stable = region.plan.stable_dat_floor_ids
    if not set(unsupported) <= set(stable):
        raise ValueError(
            "server-uncovered collision floors are not all stable client-DAT floors"
        )

    rows = []
    for floor_id in unsupported:
        (
            _width,
            _height,
            tile,
            parts,
            _event,
            _digest,
            _kind,
            _event_status,
        ) = region._stable_payload(floor_id)
        rows.append(
            classify_planes(
                floor_id=floor_id,
                tile=tile,
                parts=parts,
                adrn_map_numbers=adrn_ids,
            )
        )

    return ClientAdrnCoverageAudit(
        rows=tuple(rows),
        adrn_sha256=hashlib.sha256(raw_adrn).hexdigest(),
        adrn_bytes=len(raw_adrn),
        adrn_records=int(adrn["records"]),
        adrn_index_size=len(adrn["by_bmp"]),
        adrn_duplicate_map_numbers=int(adrn["duplicate"]),
    )


def emit(audit: ClientAdrnCoverageAudit) -> None:
    print("StoneAge recovered25 client ADRN collision-attribute coverage — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print(
        "RULE|coverage/provenance only; this report does not assert Taiwan-v1 "
        "readHitMap semantics as recovered25 runtime behavior"
    )
    print(f"ADRN_SHA256|{audit.adrn_sha256}")
    print(f"ADRN_BYTES|{audit.adrn_bytes}")
    for key in sorted(audit.counts):
        print(f"COUNT|{key}|{audit.counts[key]}")

    unresolved = [row for row in audit.rows if not row.closed]
    print(
        "FLOOR_IDS|client_adrn_unresolved|"
        + ",".join(str(row.floor_id) for row in unresolved)
    )
    all_unresolved = sorted(
        {value for row in unresolved for value in row.unresolved_ids}
    )
    print(
        "UNRESOLVED_ID_SAMPLE|"
        + ",".join(str(value) for value in all_unresolved[:80])
    )
    print(OUTPUT_RESOLUTION)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-dat-dir", type=Path, required=True)
    ap.add_argument("--server-map-root", type=Path, required=True)
    ap.add_argument("--mapset", type=Path, required=True)
    ap.add_argument("--adrn", type=Path, required=True)
    args = ap.parse_args()
    emit(
        analyze(
            client_dat_dir=args.client_dat_dir,
            server_map_root=args.server_map_root,
            mapset_path=args.mapset,
            adrn_path=args.adrn,
        )
    )


if __name__ == "__main__":
    main()
