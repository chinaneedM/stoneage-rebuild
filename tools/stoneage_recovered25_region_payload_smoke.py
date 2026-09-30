#!/usr/bin/env python3
"""Validate all 826 recovered25 map payload bindings without retaining bytes."""

from __future__ import annotations
import argparse
from pathlib import Path

from tools.stoneage_local_runtime_core import (
    WorldRegionRequest,
    load_runtime_bootstrap_file,
)
from tools.stoneage_recovered25_region_payload import (
    CLIENT_DAT_THREE_PLANE,
    SERVER_LS2MAP_TWO_PLANE,
    Recovered25RegionPayloadSource,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    Recovered25WorldProfileAdapter,
)

RESOLUTION="RESOLUTION|RECOVERED25_REGION_PAYLOAD_SOURCE_CLOSED"


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--client-dat-dir",type=Path,required=True)
    ap.add_argument("--server-map-root",type=Path,required=True)
    a=ap.parse_args()

    root=Path(__file__).resolve().parents[1]
    profile=load_runtime_bootstrap_file(
        root/"game"/"RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
    )
    adapter=Recovered25WorldProfileAdapter.from_repository(profile)
    source=Recovered25RegionPayloadSource(
        profile=profile,
        adapter=adapter,
        client_dat_dir=a.client_dat_dir,
        server_map_root=a.server_map_root,
    )
    counts=source.validate_all_payloads()

    stable_id=min(source.plan.stable_dat_floor_ids)
    supplemental_id=min(source.plan.supplemental_ls2map_floor_ids)
    samples=[]
    for floor_id in (stable_id,supplemental_id):
        region=source.materialize_region(WorldRegionRequest(
            floor_id=floor_id,x1=0,y1=0,x2=0,y2=0,
            world_profile=profile.runtime_world_profile,
        ))
        samples.append(region.payload.source_kind)

    print("StoneAge recovered25 region payload source audit — R1")
    print("SEMANTIC_SOURCE_VERSION|recovered25")
    print("EVIDENCE_ROLE|LATER_RECOVERED")
    print("RULE|raw map planes are transient and are not written to this report")
    print("RULE|server LS2MAP has tile/object planes only; event semantics remain a separate world layer and are never fabricated as zero cells")
    for key in sorted(counts):
        print(f"COUNT|{key}|{counts[key]}")
    print(
        "SAMPLE_SOURCE_KINDS|client_dat="
        f"{int(CLIENT_DAT_THREE_PLANE in samples)}|"
        f"server_ls2map={int(SERVER_LS2MAP_TWO_PLANE in samples)}"
    )
    print(RESOLUTION)


if __name__=="__main__":
    main()
