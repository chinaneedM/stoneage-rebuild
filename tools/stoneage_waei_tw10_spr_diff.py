#!/usr/bin/env python3
"""Compare archived Waei spr_1.bin against accepted Taiwan v1.0 structurally.

Original game bytes remain transient. Only hashes, counts and group-level derived
metadata are printed.
"""
from __future__ import annotations

import argparse
import hashlib
import struct
import urllib.request
from pathlib import Path

from tools.stoneage_tw10_technical_probe import find_rows
from tools.stoneage_tw10_client_inventory import normalize, row_bytes

WAEI_URL=("https://web.archive.org/web/20010605174550id_/"
          "http://www7.waei.net:80/download/file/%AD%D7%B8%C9%B5%7b%A6%A1/spr_1.bin")
WAEI_EXPECTED_SHA256="864fa3f6aaeb7d8d2dc9bdee46cecdc7dcee1af0c8f1ed949e09c0526e6aa17e"
TW_EXPECTED_SHA256="53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a"
INDEX_RECORD=12
ANIM_HEADER=12
FRAME=10

def fetch(url,timeout=90,max_bytes=16*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":"stoneage-rebuild-archaeology/1.0",
        "Accept":"application/octet-stream,*/*;q=0.1",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        data=r.read(max_bytes+1)
        if len(data)>max_bytes:
            raise ValueError(f"response-too-large:{len(data)}")
        return data

def extract_tw(bin_path:Path):
    img,rows,layout,joliet=find_rows(bin_path)
    try:
        by={normalize(r["path"]).lower():r for r in rows if not r["is_dir"]}
        spr=row_bytes(img,by["stoneage/data/spr_1.bin"])
        idx=row_bytes(img,by["stoneage/data/spradrn_1.bin"])
        return spr,idx,layout,joliet
    finally:
        img.close()

def parse_index(data):
    if len(data)%INDEX_RECORD:
        raise ValueError("index-not-divisible-by-12")
    return tuple(struct.unpack_from("<IIHH",data,i) for i in range(0,len(data),INDEX_RECORD))

def validate_spr(spr,index):
    rows=parse_index(index)
    groups=[]
    total_anim=total_frames=0
    for gi,(spr_no,offset,anim_count,reserved) in enumerate(rows):
        end=rows[gi+1][1] if gi+1<len(rows) else len(spr)
        if not (0<=offset<=end<=len(spr)):
            raise ValueError(f"invalid-span:{gi}:{offset}:{end}:{len(spr)}")
        cur=offset
        frames=0
        for ai in range(anim_count):
            if cur+ANIM_HEADER>len(spr):
                raise ValueError(f"truncated-anim:{gi}:{ai}")
            direction,anim_no,duration,frame_count=struct.unpack_from("<HHII",spr,cur)
            cur+=ANIM_HEADER
            need=frame_count*FRAME
            if cur+need>len(spr):
                raise ValueError(f"truncated-frames:{gi}:{ai}:{frame_count}")
            cur+=need
            frames+=frame_count
        if cur!=end:
            raise ValueError(f"group-span-mismatch:{gi}:{cur}:{end}")
        total_anim+=anim_count
        total_frames+=frames
        groups.append((gi,spr_no,offset,end,anim_count,frames,reserved))
    return tuple(groups),total_anim,total_frames

def diff_runs(a,b):
    if len(a)!=len(b):
        raise ValueError("length mismatch")
    changed=0;runs=[];start=None
    for i,(x,y) in enumerate(zip(a,b)):
        d=x!=y
        if d:
            changed+=1
            if start is None:start=i
        elif start is not None:
            runs.append((start,i));start=None
    if start is not None:runs.append((start,len(a)))
    return changed,tuple(runs)

def group_diffs(a,b,groups):
    out=[]
    for gi,spr_no,start,end,anim_count,frames,reserved in groups:
        aa=a[start:end];bb=b[start:end]
        if aa!=bb:
            n=sum(x!=y for x,y in zip(aa,bb))
            out.append((gi,spr_no,start,end,anim_count,frames,n,
                        hashlib.sha256(aa).hexdigest(),hashlib.sha256(bb).hexdigest()))
    return tuple(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--tw-bin",type=Path,required=True)
    ns=ap.parse_args()

    tw,idx,layout,joliet=extract_tw(ns.tw_bin)
    wae=fetch(WAEI_URL)
    tw_sha=hashlib.sha256(tw).hexdigest()
    wae_sha=hashlib.sha256(wae).hexdigest()
    print("StoneAge Waei-vs-Taiwan spr_1.bin structural diff — R1")
    print("SCOPE|accepted TW v1.0 + archived Waei 2001-06-05 spr_1.bin|transient bytes|derived metadata only")
    print(f"INPUT|tw_layout={layout}|tw_joliet={int(joliet)}|tw_bytes={len(tw)}|tw_sha256={tw_sha}|waei_bytes={len(wae)}|waei_sha256={wae_sha}|index_bytes={len(idx)}")
    print(f"VERIFY|tw_expected_hash={int(tw_sha==TW_EXPECTED_SHA256)}|waei_expected_hash={int(wae_sha==WAEI_EXPECTED_SHA256)}|same_size={int(len(tw)==len(wae))}|same_bytes={int(tw==wae)}")

    tw_groups,tw_anim,tw_frames=validate_spr(tw,idx)
    print(f"TW_PARSE|groups={len(tw_groups)}|animations={tw_anim}|frames={tw_frames}|closed=1")

    try:
        wae_groups,wae_anim,wae_frames=validate_spr(wae,idx)
        wae_closed=1
        print(f"WAEI_PARSE_WITH_TW_INDEX|groups={len(wae_groups)}|animations={wae_anim}|frames={wae_frames}|closed=1")
    except Exception as exc:
        wae_groups=();wae_closed=0
        print(f"WAEI_PARSE_WITH_TW_INDEX|closed=0|error={type(exc).__name__}:{exc}")

    changed,runs=diff_runs(tw,wae)
    maxrun=max((e-s for s,e in runs),default=0)
    print(f"BYTE_DIFF|changed_bytes={changed}|unchanged_bytes={len(tw)-changed}|changed_pct={changed*100/len(tw):.6f}|runs={len(runs)}|max_run={maxrun}|first_diff={runs[0][0] if runs else -1}|last_diff={runs[-1][1]-1 if runs else -1}")

    block=4096
    blocks=(len(tw)+block-1)//block
    changed_blocks=sum(tw[i:i+block]!=wae[i:i+block] for i in range(0,len(tw),block))
    print(f"BLOCK_DIFF|block_bytes={block}|blocks={blocks}|changed_blocks={changed_blocks}|unchanged_blocks={blocks-changed_blocks}")

    if wae_closed:
        gd=group_diffs(tw,wae,tw_groups)
        print(f"GROUP_DIFF|groups={len(tw_groups)}|changed_groups={len(gd)}|unchanged_groups={len(tw_groups)-len(gd)}")
        for gi,spr_no,start,end,anim_count,frames,n,th,wh in gd:
            print(f"CHANGED_GROUP|index={gi}|spr_no={spr_no}|offset={start}|end={end}|bytes={end-start}|animations={anim_count}|frames={frames}|changed_bytes={n}|tw_sha256={th}|waei_sha256={wh}")

    if wae_closed:
        print("RESOLUTION|SAME_STONEAGE_SPR_CONTAINER_GEOMETRY|Waei file parses exactly under accepted TW v1.0 spradrn index; classify as strong StoneAge-lineage resource evidence pending download-title binding")
    else:
        print("RESOLUTION|SAME_SIZE_DIFFERENT_BYTES_INDEX_INCOMPATIBLE|do not infer same container semantics")
    print("EVIDENCE_BOUNDARY|Structural compatibility establishes resource-lineage evidence, not by itself the exact Mainland client version or official package build.")

if __name__=="__main__":
    main()
