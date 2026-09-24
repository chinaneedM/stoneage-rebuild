#!/usr/bin/env python3
"""Compare StoneAge field-map corpora across 2003-06, 2003-12 and preserved 2.5.

Inputs are transiently recovered outside the repository. The report retains only
hash/count/plane-difference and Taiwan-v1 resource-compatibility metadata.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.stoneage_historical_map_25_compare import (
    compatibility_against_profile,
    index_numeric_maps,
)
from tools.stoneage_tw10_hit_map_model import load_taiwan_v10_collision_profile

CORPORA=("june2003","dec2003","preserved25")

def corpus_summary(rows,profile_ids):
    valid=sum(row["valid"] for row in rows.values())
    invalid=len(rows)-valid
    compatible=0
    incompatible=0
    for row in rows.values():
        state,_=compatibility_against_profile(row,profile_ids)
        if state is True:
            compatible+=1
        elif state is False:
            incompatible+=1
    return {
        "numeric":len(rows),"valid":valid,"invalid":invalid,
        "compatible":compatible,"incompatible":incompatible,
    }

def pair_summary(a,b):
    common=sorted(set(a)&set(b))
    same=[mid for mid in common if a[mid]["sha256"]==b[mid]["sha256"]]
    different=[mid for mid in common if a[mid]["sha256"]!=b[mid]["sha256"]]
    return {
        "common":common,"same":same,"different":different,
        "only_a":sorted(set(a)-set(b)),"only_b":sorted(set(b)-set(a)),
    }

def plane_diffs(a,b):
    if a["planes"] is None or b["planes"] is None or a["dims"]!=b["dims"]:
        return None
    names=("tile","parts","event")
    out={}
    for name,ap,bp in zip(names,a["planes"],b["planes"]):
        out[name]=sum(x!=y for x,y in zip(ap,bp))
    out["total"]=sum(out.values())
    return out

def lineage_code(j,d,p):
    jh=j["sha256"]; dh=d["sha256"]; ph=p["sha256"]
    if jh==dh==ph:
        return "STABLE_ALL"
    if jh==dh and dh!=ph:
        return "JUNE_DEC_SAME_THEN_CHANGED"
    if jh!=dh and dh==ph:
        return "CHANGED_BY_DEC_THEN_STABLE"
    if jh==ph and jh!=dh:
        return "DEC_ONLY_DIVERGENCE"
    return "THREE_DISTINCT"

def emit(june_root:Path,dec_root:Path,preserved_root:Path,profile_path:Path):
    june,jdups=index_numeric_maps(june_root)
    dec,ddups=index_numeric_maps(dec_root)
    preserved,pdups=index_numeric_maps(preserved_root)
    corpora={"june2003":june,"dec2003":dec,"preserved25":preserved}

    profile=load_taiwan_v10_collision_profile(profile_path)
    profile_ids=set(profile.by_map_number)

    print("StoneAge field-map three-state timeline — R1")
    print("SCOPE|2003-06-vs-2003-12-vs-preserved-2.5|derived-only|Taiwan-v1-compatibility-is-necessary-not-provenance")
    print(f"TW1_PROFILE|map_numbers={len(profile_ids)}|min={min(profile_ids)}|max={max(profile_ids)}")

    dupsets={"june2003":jdups,"dec2003":ddups,"preserved25":pdups}
    for name in CORPORA:
        summary=corpus_summary(corpora[name],profile_ids)
        print(
            f"CORPUS|name={name}|numeric_maps={summary['numeric']}|valid={summary['valid']}|"
            f"invalid={summary['invalid']}|tw1_compatible={summary['compatible']}|"
            f"tw1_incompatible={summary['incompatible']}|duplicate_ids={len(dupsets[name])}"
        )

    for an,bn in (("june2003","dec2003"),("dec2003","preserved25"),("june2003","preserved25")):
        pair=pair_summary(corpora[an],corpora[bn])
        print(
            f"PAIR|a={an}|b={bn}|common={len(pair['common'])}|byte_identical={len(pair['same'])}|"
            f"byte_different={len(pair['different'])}|only_a={len(pair['only_a'])}|only_b={len(pair['only_b'])}"
        )
        if pair["only_a"]:
            print(f"PAIR_ONLY_A|a={an}|b={bn}|ids="+",".join(map(str,pair["only_a"])))
        if pair["only_b"]:
            print(f"PAIR_ONLY_B|a={an}|b={bn}|ids="+",".join(map(str,pair["only_b"])))

    common3=sorted(set(june)&set(dec)&set(preserved))
    lineage_counts={}
    compatibility_patterns={}
    rows=[]
    for mid in common3:
        j=june[mid]; d=dec[mid]; p=preserved[mid]
        code=lineage_code(j,d,p)
        lineage_counts[code]=lineage_counts.get(code,0)+1
        states=[]
        missings=[]
        for row in (j,d,p):
            state,missing=compatibility_against_profile(row,profile_ids)
            states.append(state)
            missings.append(missing)
        pattern="->".join(
            "C" if state is True else "I" if state is False else "X"
            for state in states
        )
        compatibility_patterns[pattern]=compatibility_patterns.get(pattern,0)+1
        if code!="STABLE_ALL" or len(set(states))>1:
            rows.append((mid,code,pattern,j,d,p,missings))

    print(f"COUNT|common_three|{len(common3)}")
    for code,count in sorted(lineage_counts.items()):
        print(f"LINEAGE_COUNT|code={code}|maps={count}")
    for pattern,count in sorted(compatibility_patterns.items()):
        print(f"COMPAT_PATTERN_COUNT|pattern={pattern}|maps={count}")

    for mid,code,pattern,j,d,p,missings in rows:
        jd=plane_diffs(j,d)
        dp=plane_diffs(d,p)
        extras=""
        if jd is not None:
            extras+=(
                f"|jd_tile_diff={jd['tile']}|jd_parts_diff={jd['parts']}|"
                f"jd_event_diff={jd['event']}|jd_total={jd['total']}"
            )
        if dp is not None:
            extras+=(
                f"|dp_tile_diff={dp['tile']}|dp_parts_diff={dp['parts']}|"
                f"dp_event_diff={dp['event']}|dp_total={dp['total']}"
            )
        print(
            f"MAP_TIMELINE|id={mid}|lineage={code}|compat={pattern}|"
            f"j_sha256={j['sha256']}|d_sha256={d['sha256']}|p_sha256={p['sha256']}|"
            f"j_missing={','.join(map(str,missings[0][:20]))}|"
            f"d_missing={','.join(map(str,missings[1][:20]))}|"
            f"p_missing={','.join(map(str,missings[2][:20]))}{extras}"
        )

    print("RESOLUTION|THREE_STATE_TIMELINE_CLASSIFIED|do not back-project descendant map bytes into Taiwan v1")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--june-root",type=Path,required=True)
    parser.add_argument("--dec-root",type=Path,required=True)
    parser.add_argument("--preserved-root",type=Path,required=True)
    parser.add_argument("--profile",type=Path,required=True)
    args=parser.parse_args()
    emit(args.june_root,args.dec_root,args.preserved_root,args.profile)

if __name__=="__main__":
    main()
