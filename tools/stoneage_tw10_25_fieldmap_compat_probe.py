#!/usr/bin/env python3
"""Classify recovered 2.5 DAT maps by compatibility with Taiwan-v1 ADRN map numbers.

This is an exclusion/prioritization tool only. A map that uses only Taiwan-v1
resource IDs is merely *asset-compatible* with v1; it is not evidence that the
map bytes or layout existed in v1.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
from pathlib import Path

from tools.stoneage_tw10_hit_map_model import (
    load_taiwan_v10_collision_profile,
    parse_stoneage_dat_map_cache,
)


def requires_profile(value:int)->bool:
    value=int(value)
    return value>99 or 60<=value<=79


def analyze_map(path:Path,profile_ids:set[int]):
    raw=path.read_bytes()
    cache=parse_stoneage_dat_map_cache(raw)
    missing=collections.Counter()
    required=collections.Counter()
    for plane_name,plane in (("tile",cache.tile),("parts",cache.parts)):
        for value in plane:
            value=int(value)
            if requires_profile(value):
                required[(plane_name,value)]+=1
                if value not in profile_ids:
                    missing[(plane_name,value)]+=1
    missing_ids=sorted({value for _,value in missing})
    return {
        "width":cache.width,
        "height":cache.height,
        "bytes":len(raw),
        "sha256":hashlib.sha256(raw).hexdigest(),
        "required_cells":sum(required.values()),
        "required_ids":len({value for _,value in required}),
        "missing_cells":sum(missing.values()),
        "missing_ids":missing_ids,
        "compatible":not missing_ids,
        "max_tile":max(cache.tile) if cache.tile else 0,
        "max_parts":max(cache.parts) if cache.parts else 0,
    }


def analyze(root:Path,profile_path:Path):
    profile=load_taiwan_v10_collision_profile(profile_path)
    profile_ids=set(profile.by_map_number)
    rows=[]
    invalid=[]
    for path in sorted((p for p in root.rglob("*") if p.is_file() and p.suffix.lower()==".dat"),key=lambda p:str(p).lower()):
        try:
            info=analyze_map(path,profile_ids)
            rows.append((path,info))
        except Exception as exc:
            invalid.append((path,type(exc).__name__,str(exc)))
    return profile_ids,rows,invalid


def emit(root:Path,profile_path:Path,sample_limit=100):
    profile_ids,rows,invalid=analyze(root,profile_path)
    compatible=[row for row in rows if row[1]["compatible"]]
    incompatible=[row for row in rows if not row[1]["compatible"]]
    missing_freq=collections.Counter()
    for _,info in incompatible:
        missing_freq.update(info["missing_ids"])

    print("StoneAge Taiwan-v1 / recovered-2.5 field-map asset compatibility — R1")
    print("SCOPE|necessary-not-sufficient-resource-id-compatibility|HYPOTHESIS-prioritization-only|no-map-payload-retained")
    print(f"PROFILE|tw1_map_numbers={len(profile_ids)}|min={min(profile_ids)}|max={max(profile_ids)}")
    print(f"COUNT|dat_maps|{len(rows)}")
    print(f"COUNT|asset_compatible|{len(compatible)}")
    print(f"COUNT|asset_incompatible|{len(incompatible)}")
    print(f"COUNT|invalid|{len(invalid)}")
    print("RULE|compatible means every tile/parts value requiring ADRN lookup resolves in Taiwan-v1 profile; it does NOT prove historical v1 membership")

    for path,info in compatible[:sample_limit]:
        print(
            "COMPATIBLE|"
            f"path={path.relative_to(root)}|width={info['width']}|height={info['height']}|"
            f"bytes={info['bytes']}|required_ids={info['required_ids']}|"
            f"required_cells={info['required_cells']}|max_tile={info['max_tile']}|"
            f"max_parts={info['max_parts']}|sha256={info['sha256']}"
        )

    for path,info in sorted(incompatible,key=lambda row:(len(row[1]["missing_ids"]),row[1]["missing_cells"],str(row[0]).lower()))[:sample_limit]:
        print(
            "INCOMPATIBLE_SAMPLE|"
            f"path={path.relative_to(root)}|width={info['width']}|height={info['height']}|"
            f"missing_ids={len(info['missing_ids'])}|missing_cells={info['missing_cells']}|"
            f"first_missing={','.join(map(str,info['missing_ids'][:20]))}|sha256={info['sha256']}"
        )

    for value,count in missing_freq.most_common(50):
        print(f"LATER_ONLY_ID_FREQUENCY|map_number={value}|maps={count}")

    for path,kind,message in invalid[:50]:
        print(f"INVALID|path={path.relative_to(root)}|kind={kind}|message={message}")

    if rows:
        print("RESOLUTION|TW1_ASSET_COMPATIBILITY_CLASSIFIED|use only to exclude later-only maps and prioritize provenance work")
    else:
        print("RESOLUTION|NO_DAT_MAPS")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--map-root",type=Path,required=True)
    parser.add_argument("--profile",type=Path,required=True)
    args=parser.parse_args()
    emit(args.map_root,args.profile)


if __name__=="__main__":
    main()
