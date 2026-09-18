#!/usr/bin/env python3
import argparse,collections
from pathlib import Path
from tools.stoneage_client_server_map_probe import read_server_map
from tools.stoneage_dat_probe import EVENT_MASK,EVENT_NAMES,parse_dat

def collect_server(root):
    by_id=collections.defaultdict(list); total=ls2=0
    for p in root.rglob("*"):
        if not p.is_file(): continue
        total+=1
        try: mid,name,w,h,t,o=read_server_map(p)
        except ValueError: continue
        ls2+=1; by_id[mid].append((p,w,h,t,o))
    return by_id,total,ls2

def analyze(dat_dir,server_root,focus_ids=()):
    focus_ids=set(focus_ids)
    server,total,ls2=collect_server(server_root); c=collections.Counter()
    mismatch=[]; unknown=[]; focus=[]
    for p in sorted((x for x in dat_dir.iterdir() if x.is_file() and x.suffix.lower()==".dat"),key=lambda x:x.name.lower()):
        c["dat_files"]+=1
        try: mid=int(p.stem)
        except ValueError: c["dat_non_numeric"]+=1; continue
        try: w,h,tile,parts,event=parse_dat(p)
        except ValueError: c["dat_invalid"]+=1; continue
        c["dat_valid_numeric"]+=1
        u=sum(1 for v in event if (v&EVENT_MASK) not in EVENT_NAMES)
        if u: unknown.append((p.name,w,h,u))
        entries=server.get(mid,[])
        if not entries:
            c["no_server_id"]+=1
            if mid in focus_ids: focus.append((mid,w,h,"NO_SERVER_ID",-1,-1,u))
            continue
        c["matched_id"]+=1; best=None
        for sp,sw,sh,st,so in entries:
            if (w,h)!=(sw,sh): continue
            td=sum(a!=b for a,b in zip(tile,st)); pd=sum(a!=b for a,b in zip(parts,so))
            cand=(td+pd,td,pd,str(sp.relative_to(server_root)))
            if best is None or cand[:3]<best[:3]: best=cand
        if best is None:
            c["dimension_mismatch"]+=1
            if mid in focus_ids: focus.append((mid,w,h,"DIMENSION_MISMATCH",-1,-1,u))
            continue
        c["matched_dimensions"]+=1
        _,td,pd,sp=best; c["tile_diff_cells"]+=td; c["parts_diff_cells"]+=pd
        if td==0:c["tile_exact"]+=1
        if pd==0:c["parts_exact"]+=1
        if td==0 and pd==0:c["both_exact"]+=1
        else:
            c["static_mismatch"]+=1
            if len(mismatch)<40:mismatch.append((mid,w,h,sp,td,pd))
        if mid in focus_ids: focus.append((mid,w,h,sp,td,pd,u))
    c["server_files"]=total;c["server_ls2map"]=ls2;c["server_unique_ids"]=len(server)
    return c,mismatch,unknown,focus

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--dat-dir",type=Path,required=True);ap.add_argument("--server-map-root",type=Path,required=True);ap.add_argument("--focus-id",type=int,action="append",default=[]);a=ap.parse_args()
    c,m,u,d=analyze(a.dat_dir,a.server_map_root,a.focus_id)
    print("StoneAge recovered DAT/server static-layer crosscheck — R1")
    print("No proprietary payload bytes are stored in this report.")
    for k in sorted(c):print(f"COUNT|{k}|{c[k]}")
    for row in m:print("MISMATCH|"+"|".join(map(str,row)))
    for row in u[:40]:print("UNKNOWN_EVENT_FILE|"+"|".join(map(str,row)))
    for row in d:print("FOCUS_MAP|"+"|".join(map(str,row)))
if __name__=="__main__":main()
