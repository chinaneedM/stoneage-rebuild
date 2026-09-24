#!/usr/bin/env python3
"""Compare the recovered 2003-06 historical map pack to the preserved 2.5 map corpus.

This is a provenance/dating comparison. Inputs live in temporary CI directories.
Only derived hashes/counts are emitted; no DAT bytes are retained.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

from tools.stoneage_tw10_hit_map_model import (
    load_taiwan_v10_collision_profile,
    parse_stoneage_dat_map_cache,
)
from tools.stoneage_tw10_25_fieldmap_compat_probe import requires_profile

NUMERIC_DAT=re.compile(r"^(\d+)\.dat$",re.I)


def index_numeric_maps(root:Path):
    rows={}
    duplicates=[]
    for path in sorted(root.rglob("*"),key=lambda p:str(p).lower()):
        if not path.is_file():
            continue
        m=NUMERIC_DAT.match(path.name)
        if not m:
            continue
        map_id=int(m.group(1))
        raw=path.read_bytes()
        sha=hashlib.sha256(raw).hexdigest()
        try:
            cache=parse_stoneage_dat_map_cache(raw)
            valid=True
            dims=(cache.width,cache.height)
            planes=(cache.tile,cache.parts,cache.event)
        except Exception:
            valid=False
            dims=None
            planes=None
        row={
            "id":map_id,
            "path":str(path.relative_to(root)).replace("\\","/"),
            "bytes":len(raw),
            "sha256":sha,
            "valid":valid,
            "dims":dims,
            "planes":planes,
        }
        if map_id in rows:
            duplicates.append((map_id,rows[map_id],row))
        else:
            rows[map_id]=row
    return rows,duplicates



def compatibility_against_profile(row,profile_ids:set[int]):
    """Return (compatible, missing_ids) for a parsed map row, or (None, [])."""
    if row["planes"] is None:
        return None,[]
    missing=set()
    for plane in row["planes"][:2]:
        for value in plane:
            value=int(value)
            if requires_profile(value) and value not in profile_ids:
                missing.add(value)
    missing_ids=sorted(missing)
    return not missing_ids,missing_ids

def mapset_digest(rows):
    text="\n".join(f"{mid}:{rows[mid]['sha256']}" for mid in sorted(rows))
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def compare(a_root:Path,b_root:Path):
    a,a_dups=index_numeric_maps(a_root)
    b,b_dups=index_numeric_maps(b_root)
    common=sorted(set(a)&set(b))
    same=[mid for mid in common if a[mid]["sha256"]==b[mid]["sha256"]]
    different=[mid for mid in common if a[mid]["sha256"]!=b[mid]["sha256"]]
    return {
        "a":a,"b":b,"a_dups":a_dups,"b_dups":b_dups,
        "common":common,"same":same,"different":different,
        "only_a":sorted(set(a)-set(b)),
        "only_b":sorted(set(b)-set(a)),
    }


def emit(a_root:Path,b_root:Path,profile_path:Path|None=None):
    result=compare(a_root,b_root)
    a=result["a"]; b=result["b"]
    print("StoneAge 2003-06 historical map pack vs preserved 2.5 map corpus — R1")
    print("SCOPE|numeric-DAT-ID+SHA256+three-plane-shape|provenance-comparison|derived-only")
    print(
        f"A|label=historical-20030623-map.exe|numeric_maps={len(a)}|"
        f"valid_three_plane={sum(row['valid'] for row in a.values())}|"
        f"invalid={sum(not row['valid'] for row in a.values())}|mapset_sha256={mapset_digest(a)}"
    )
    print(
        f"B|label=preserved-2.5-map-dir|numeric_maps={len(b)}|"
        f"valid_three_plane={sum(row['valid'] for row in b.values())}|"
        f"invalid={sum(not row['valid'] for row in b.values())}|mapset_sha256={mapset_digest(b)}"
    )
    print(f"COUNT|common_ids|{len(result['common'])}")
    print(f"COUNT|byte_identical|{len(result['same'])}")
    print(f"COUNT|byte_different|{len(result['different'])}")
    print(f"COUNT|only_historical|{len(result['only_a'])}")
    print(f"COUNT|only_preserved25|{len(result['only_b'])}")
    print(f"COUNT|historical_duplicate_ids|{len(result['a_dups'])}")
    print(f"COUNT|preserved25_duplicate_ids|{len(result['b_dups'])}")
    profile_ids=None
    if profile_path is not None:
        profile=load_taiwan_v10_collision_profile(profile_path)
        profile_ids=set(profile.by_map_number)
        transitions=[]
        for mid in result["different"]:
            ac,_=compatibility_against_profile(a[mid],profile_ids)
            bc,_=compatibility_against_profile(b[mid],profile_ids)
            if ac is not None and bc is not None and ac!=bc:
                transitions.append(mid)
        print(f"TW1_PROFILE|map_numbers={len(profile_ids)}|min={min(profile_ids)}|max={max(profile_ids)}")
        print(f"COUNT|tw1_compatibility_transitions|{len(transitions)}")
    if result["different"]:
        for mid in result["different"]:
            ar=a[mid]; br=b[mid]
            plane_text=""
            if ar["planes"] is not None and br["planes"] is not None and ar["dims"]==br["dims"]:
                names=("tile","parts","event")
                pieces=[]
                total=0
                for name,ap,bp in zip(names,ar["planes"],br["planes"]):
                    diff=sum(x!=y for x,y in zip(ap,bp))
                    total+=diff
                    pieces.append(f"{name}_diff={diff}")
                plane_text="|"+("|".join(pieces))+f"|cell_value_diffs={total}"
            print(
                f"DIFF|id={mid}|a_bytes={ar['bytes']}|b_bytes={br['bytes']}|"
                f"a_sha256={ar['sha256']}|b_sha256={br['sha256']}|"
                f"a_dims={ar['dims']}|b_dims={br['dims']}{plane_text}"
                + (
                    (
                        lambda av,bv:
                            f"|a_tw1_compatible={str(av[0]).lower()}|b_tw1_compatible={str(bv[0]).lower()}|"
                            f"a_missing_ids={len(av[1])}|b_missing_ids={len(bv[1])}|"
                            f"a_first_missing={','.join(map(str,av[1][:20]))}|"
                            f"b_first_missing={','.join(map(str,bv[1][:20]))}"
                    )(
                        compatibility_against_profile(ar,profile_ids),
                        compatibility_against_profile(br,profile_ids),
                    )
                    if profile_ids is not None else ""
                )
            )
    if result["only_a"]:
        print("ONLY_HISTORICAL|ids="+",".join(map(str,result["only_a"])))
    if result["only_b"]:
        print("ONLY_PRESERVED25|ids="+",".join(map(str,result["only_b"])))
    if (
        len(a)==len(b)==len(result["same"])
        and not result["different"] and not result["only_a"] and not result["only_b"]
        and not result["a_dups"] and not result["b_dups"]
    ):
        print("RESOLUTION|NUMERIC_MAP_CORPUS_BYTE_IDENTICAL|preserved 2.5 numeric DAT set is byte-identical to archived 2003-06 map package")
    elif result["same"]:
        print("RESOLUTION|PARTIAL_IDENTITY|historical and preserved corpora overlap but are not wholly identical")
    else:
        print("RESOLUTION|NO_BYTE_IDENTITY|no common byte-identical numeric maps")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--historical-root",type=Path,required=True)
    parser.add_argument("--preserved-root",type=Path,required=True)
    parser.add_argument("--profile",type=Path)
    args=parser.parse_args()
    emit(args.historical_root,args.preserved_root,args.profile)


if __name__=="__main__":
    main()
