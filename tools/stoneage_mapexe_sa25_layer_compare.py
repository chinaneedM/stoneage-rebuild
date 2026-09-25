#!/usr/bin/env python3
"""Layer-level comparison for the 16 DAT files that differ between the
historical 2003-06-10 map package and the recovered mixed-2.5 corpus.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, struct

def sha(b): return hashlib.sha256(b).hexdigest()

def parse_dat(path):
    b=path.read_bytes()
    if len(b)<8: return None
    w,h=struct.unpack_from("<II",b,0)
    if not w or not h or w>10000 or h>10000: return None
    n=w*h; span=n*2
    if len(b)!=8+3*span: return None
    return {
        "bytes":b,"w":w,"h":h,"n":n,
        "tile":b[8:8+span],
        "parts":b[8+span:8+2*span],
        "event":b[8+2*span:8+3*span],
    }

def vals(layer):
    return struct.unpack("<"+"H"*(len(layer)//2),layer)

def compare(a,b):
    out={}
    for key in ("tile","parts","event"):
        av,bv=vals(a[key]),vals(b[key])
        out[key+"_changed"]=sum(x!=y for x,y in zip(av,bv))
        out[key+"_a_sha"]=sha(a[key]); out[key+"_b_sha"]=sha(b[key])
        if key=="event":
            out["event_low12_changed"]=sum((x&0x0fff)!=(y&0x0fff) for x,y in zip(av,bv))
            out["event_flags_changed"]=sum((x&0xf000)!=(y&0xf000) for x,y in zip(av,bv))
    return out

def files(root):
    return {p.name.casefold():p for p in pathlib.Path(root).iterdir() if p.is_file() and p.suffix.casefold()==".dat"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--historical-map",required=True)
    ap.add_argument("--mixed-map",required=True)
    a=ap.parse_args()
    old=files(a.historical_map); mixed=files(a.mixed_map)
    both=sorted(set(old)&set(mixed))
    diffs=[k for k in both if sha(old[k].read_bytes())!=sha(mixed[k].read_bytes())]
    print("StoneAge historical Jun10 vs mixed-2.5 DAT layer diff — R1")
    print("SCOPE|16-whole-file-differences+tile/parts/event-cell-comparison|no-payload-commit")
    print(f"DIFF_FILE_COUNT|{len(diffs)}")
    normal=0; special=0
    totals={"tile":0,"parts":0,"event":0,"low12":0,"flags":0}
    for k in diffs:
        x=parse_dat(old[k]); y=parse_dat(mixed[k])
        if not x or not y or (x["w"],x["h"])!=(y["w"],y["h"]):
            special+=1
            print(
                f"SPECIAL_DIFF|name={old[k].name}|historical_size={old[k].stat().st_size}|"
                f"mixed_size={mixed[k].stat().st_size}|historical_sha256={sha(old[k].read_bytes())}|"
                f"mixed_sha256={sha(mixed[k].read_bytes())}"
            )
            continue
        normal+=1; d=compare(x,y)
        totals["tile"]+=d["tile_changed"]; totals["parts"]+=d["parts_changed"]
        totals["event"]+=d["event_changed"]; totals["low12"]+=d["event_low12_changed"]
        totals["flags"]+=d["event_flags_changed"]
        print(
            f"LAYER_DIFF|name={old[k].name}|dims={x['w']}x{x['h']}|cells={x['n']}|"
            f"tile_changed={d['tile_changed']}|parts_changed={d['parts_changed']}|"
            f"event_changed={d['event_changed']}|event_low12_changed={d['event_low12_changed']}|"
            f"event_flags_changed={d['event_flags_changed']}|"
            f"historical_tile_sha256={d['tile_a_sha']}|mixed_tile_sha256={d['tile_b_sha']}|"
            f"historical_parts_sha256={d['parts_a_sha']}|mixed_parts_sha256={d['parts_b_sha']}|"
            f"historical_event_sha256={d['event_a_sha']}|mixed_event_sha256={d['event_b_sha']}"
        )
    print(f"NORMAL_DIFF_COUNT|{normal}")
    print(f"SPECIAL_DIFF_COUNT|{special}")
    print(f"TOTAL_TILE_CHANGED_CELLS|{totals['tile']}")
    print(f"TOTAL_PARTS_CHANGED_CELLS|{totals['parts']}")
    print(f"TOTAL_EVENT_CHANGED_CELLS|{totals['event']}")
    print(f"TOTAL_EVENT_LOW12_CHANGED_CELLS|{totals['low12']}")
    print(f"TOTAL_EVENT_FLAG_CHANGED_CELLS|{totals['flags']}")
    for control in ("1021.dat","817.dat"):
        if control in old and control in mixed:
            h1=sha(old[control].read_bytes()); h2=sha(mixed[control].read_bytes())
            p=parse_dat(old[control])
            print(
                f"CONTROL|name={old[control].name}|exact={int(h1==h2)}|sha256={h1}|"
                f"size={old[control].stat().st_size}|dims="
                + (f"{p['w']}x{p['h']}" if p else "special")
            )
    print("EVIDENCE_BOUNDARY|layer differences describe only the two recovered corpora. Exact equality with the Jun10 historical package independently rules out later mutation inside the recovered mixed bundle for the named control files, but does not establish their first historical appearance date.")

if __name__=="__main__": main()
