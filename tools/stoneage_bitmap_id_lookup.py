#!/usr/bin/env python3
"""Lookup bitmap IDs in derived ADRN metadata (no original asset bytes required)."""
from __future__ import annotations
import argparse,csv,gzip
from pathlib import Path

def lookup(path:Path,ids:set[int]):
    found={}
    with gzip.open(path,"rt",encoding="utf-8",newline="") as f:
        for row in csv.DictReader(f,delimiter="\t"):
            try:n=int(row["bitmapno"])
            except (KeyError,ValueError):continue
            if n in ids:found[n]=row
    return found

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--adrn",type=Path,required=True)
    ap.add_argument("--ids",nargs="+",type=int,required=True)
    ns=ap.parse_args()
    ids=set(ns.ids);found=lookup(ns.adrn,ids)
    print("StoneAge TW v1.0 ADRN bitmap-ID lookup — R1")
    print("SCOPE|derived ADRN metadata only|no original image payload")
    for n in ns.ids:
        r=found.get(n)
        if r:
            print("FOUND|bitmapno={}|index={}|adder={}|size={}|xoff={}|yoff={}|width={}|height={}|rd_flag={}|rd_block_sha256={}".format(
                n,r.get("index",""),r.get("adder",""),r.get("size",""),r.get("xoff",""),r.get("yoff",""),
                r.get("width",""),r.get("height",""),r.get("rd_flag",""),r.get("rd_block_sha256","")
            ))
        else:
            print(f"MISSING|bitmapno={n}")
    print(f"COUNT|requested|{len(ns.ids)}")
    print(f"COUNT|found|{len(found)}")
    print(f"COUNT|missing|{len(ids-found.keys())}")
    print("RESOLUTION|"+("ALL_PRESENT" if len(found)==len(ids) else "SOME_OR_ALL_MISSING"))
if __name__=="__main__":main()
