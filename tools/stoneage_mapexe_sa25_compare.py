#!/usr/bin/env python3
"""Compare the clean 2003-06-10 map.exe DAT inventory with the recovered mixed 2.5 DAT corpus.

Only derived hashes, sizes and dimensions are written. Proprietary DAT payload bytes
remain transient in CI.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, struct

MAPEXE_RE=re.compile(
    r"^DAT\|path=map/(?P<name>[^|]+)\|size=(?P<size>\d+)\|sha256=(?P<sha>[0-9a-f]{64})"
    r"(?:\|width=(?P<w>\d+)\|height=(?P<h>\d+)\|cells=(?P<cells>\d+)\|expected=(?P<expected>\d+))?"
    r"\|valid_three_layer=(?P<valid>[01])$",
    re.I,
)

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def dat_info(path):
    data=path.read_bytes()
    if len(data)<8: return None
    w,h=struct.unpack_from("<II",data,0)
    if not w or not h or w>10000 or h>10000: return None
    cells=w*h
    exp=8+cells*6
    return (w,h,cells,int(exp==len(data)))

def load_mapexe(report):
    out={}
    for line in pathlib.Path(report).read_text("utf-8",errors="replace").splitlines():
        m=MAPEXE_RE.match(line)
        if not m: continue
        d=m.groupdict()
        out[d["name"].casefold()]={
            "name":d["name"],"size":int(d["size"]),"sha":d["sha"].lower(),
            "w":int(d["w"]) if d["w"] else None,
            "h":int(d["h"]) if d["h"] else None,
            "valid":int(d["valid"]),
        }
    return out

def load_local(root):
    out={}
    for p in sorted(pathlib.Path(root).iterdir(),key=lambda x:x.name.casefold()):
        if not p.is_file() or p.suffix.casefold()!=".dat": continue
        info=dat_info(p)
        out[p.name.casefold()]={
            "name":p.name,"size":p.stat().st_size,"sha":sha256_file(p),
            "w":info[0] if info else None,"h":info[1] if info else None,
            "valid":info[3] if info else 0,
        }
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mapexe-report",required=True)
    ap.add_argument("--sa25-map",required=True)
    a=ap.parse_args()

    clean=load_mapexe(a.mapexe_report)
    mixed=load_local(a.sa25_map)
    ck=set(clean); mk=set(mixed)
    both=sorted(ck&mk)
    exact=[k for k in both if clean[k]["sha"]==mixed[k]["sha"]]
    diff=[k for k in both if clean[k]["sha"]!=mixed[k]["sha"]]
    clean_only=sorted(ck-mk); mixed_only=sorted(mk-ck)
    same_size=[k for k in diff if clean[k]["size"]==mixed[k]["size"]]
    same_dims=[k for k in diff if clean[k]["w"] is not None and clean[k]["w"]==mixed[k]["w"] and clean[k]["h"]==mixed[k]["h"]]
    valid_both=[k for k in both if clean[k]["valid"] and mixed[k]["valid"]]

    agg=hashlib.sha256()
    for k in exact:
        agg.update(k.encode()+b"\0"+clean[k]["sha"].encode()+b"\n")

    print("StoneAge 2003-06-10 map.exe vs recovered mixed-2.5 DAT lineage — R1")
    print("SCOPE|whole-file-SHA256+name+size+dimension|derived-metadata-only|no-payload-commit")
    print(f"CLEAN_JUN10_DAT_COUNT|{len(clean)}")
    print(f"MIXED_SA25_DAT_COUNT|{len(mixed)}")
    print(f"SAME_NAME_COUNT|{len(both)}")
    print(f"EXACT_WHOLE_FILE_MATCH_COUNT|{len(exact)}")
    print(f"DIFFERENT_WHOLE_FILE_COUNT|{len(diff)}")
    print(f"DIFF_SAME_SIZE_COUNT|{len(same_size)}")
    print(f"DIFF_SAME_DIMENSIONS_COUNT|{len(same_dims)}")
    print(f"VALID_THREE_LAYER_BOTH_COUNT|{len(valid_both)}")
    print(f"CLEAN_ONLY_COUNT|{len(clean_only)}")
    print(f"MIXED_ONLY_COUNT|{len(mixed_only)}")
    print(f"EXACT_SET_AGGREGATE_SHA256|{agg.hexdigest()}")
    print("CLEAN_ONLY|"+",".join(clean[k]["name"] for k in clean_only[:200]))
    print("MIXED_ONLY|"+",".join(mixed[k]["name"] for k in mixed_only[:200]))

    for k in diff:
        c,m=clean[k],mixed[k]
        print(
            f"DIFF|name={c['name']}|clean_size={c['size']}|mixed_size={m['size']}|"
            f"clean_sha256={c['sha']}|mixed_sha256={m['sha']}|"
            f"clean_dims={c['w']}x{c['h']}|mixed_dims={m['w']}x{m['h']}|"
            f"same_size={int(c['size']==m['size'])}|"
            f"same_dims={int(c['w'] is not None and c['w']==m['w'] and c['h']==m['h'])}"
        )
    for k in exact[:80]:
        c=clean[k]
        print(f"EXACT_SAMPLE|name={c['name']}|size={c['size']}|sha256={c['sha']}|dims={c['w']}x{c['h']}")
    print("EVIDENCE_BOUNDARY|exact matches prove byte identity between the 2003-06-10 archived map package and this recovered mixed bundle only; they do not by themselves date those bytes to 2.5 release time or prove the mixed bundle is a clean 2.5 client.")

if __name__=="__main__": main()
