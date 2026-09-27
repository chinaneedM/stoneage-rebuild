#!/usr/bin/env python3
"""Map the 16 Waei-vs-TW spr_1.bin differences to parsed animation/frame fields."""
from __future__ import annotations
import argparse, hashlib, struct
from pathlib import Path
from tools.stoneage_waei_tw10_spr_diff import fetch, extract_tw, WAEI_URL, parse_index

FIELDS_ANIM=(("direction",0,2),("anim_no",2,2),("duration",4,4),("frame_count",8,4))
FIELDS_FRAME=(("bmp_no",0,4),("pos_x",4,2),("pos_y",6,2),("sound_no",8,2))

def spans(index,spr_len):
    rows=parse_index(index)
    out=[]
    for gi,(spr_no,offset,anim_count,reserved) in enumerate(rows):
        end=rows[gi+1][1] if gi+1<len(rows) else spr_len
        cur=offset
        for ai in range(anim_count):
            direction,anim_no,duration,frame_count=struct.unpack_from("<HHII",b"\0"*0 if False else CURRENT_SPR,cur)
            out.append(("anim",gi,spr_no,ai,-1,cur,cur+12))
            cur+=12
            for fi in range(frame_count):
                out.append(("frame",gi,spr_no,ai,fi,cur,cur+10))
                cur+=10
    return out

def unpack_anim(data,off):
    return dict(zip(("direction","anim_no","duration","frame_count"),struct.unpack_from("<HHII",data,off)))
def unpack_frame(data,off):
    return dict(zip(("bmp_no","pos_x","pos_y","sound_no"),struct.unpack_from("<IhhH",data,off)))

def changed_runs(a,b):
    out=[];s=None
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y and s is None:s=i
        if x==y and s is not None:
            out.append((s,i));s=None
    if s is not None:out.append((s,len(a)))
    return out

def main():
    global CURRENT_SPR
    ap=argparse.ArgumentParser();ap.add_argument("--tw-bin",type=Path,required=True);ns=ap.parse_args()
    tw,idx,layout,joliet=extract_tw(ns.tw_bin)
    wae=fetch(WAEI_URL)
    CURRENT_SPR=tw
    recs=spans(idx,len(tw))
    runs=changed_runs(tw,wae)
    print("StoneAge Waei-vs-Taiwan spr_1.bin semantic field diff — R2")
    print(f"INPUT|tw_sha256={hashlib.sha256(tw).hexdigest()}|waei_sha256={hashlib.sha256(wae).hexdigest()}|bytes={len(tw)}|runs={len(runs)}")
    for ri,(s,e) in enumerate(runs,1):
        overlaps=[r for r in recs if r[5]<e and r[6]>s]
        print(f"RUN|index={ri}|start={s}|end={e}|bytes={e-s}|tw_hex={tw[s:e].hex()}|waei_hex={wae[s:e].hex()}|records={len(overlaps)}")
        for kind,gi,spr_no,ai,fi,off,end in overlaps:
            if kind=="anim":
                tv=unpack_anim(tw,off);wv=unpack_anim(wae,off)
            else:
                tv=unpack_frame(tw,off);wv=unpack_frame(wae,off)
            changed=[k for k in tv if tv[k]!=wv[k]]
            print(f"RECORD|kind={kind}|group={gi}|spr_no={spr_no}|anim={ai}|frame={fi}|offset={off}|changed={','.join(changed)}|tw={tv}|waei={wv}")
    print("RESOLUTION|SEMANTIC_DIFF_MAPPED|interpret changed parsed fields within StoneAge sprite lineage")
    print("EVIDENCE_BOUNDARY|Field-level differences describe resource content only; they do not identify the exact Mainland client build without download-page/version binding.")
if __name__=="__main__":
    main()
