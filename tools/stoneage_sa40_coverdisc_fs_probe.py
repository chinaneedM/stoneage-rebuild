#!/usr/bin/env python3
from __future__ import annotations
import math,struct,urllib.parse
from collections import deque
from tools.stoneage_sa_arena_ia_probe import SECTOR,get_json,logical_sector_read

TARGET_BYTES=3440*1024
MAX_DIR_BYTES=2*1024*1024
MAX_DIRS=600
MAX_METADATA_BYTES=48*1024*1024
IDENTIFIERS=("NetFriends2003","gamespotEverquest2","gamespotLineage","gamespotEverquest")
TOKENS=("shiqi","stoneage","stone age","石器","sta4","sa4","updatex","02_11_08","02-11-08")
ARCHIVE_EXTS=(".zip",".rar",".exe",".cab",".7z",".arj",".lzh")

def clean(v,n=2200):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def dl(identifier,name):
    return "https://archive.org/download/"+urllib.parse.quote(identifier,safe="")+"/"+urllib.parse.quote(name,safe="/")

def dec_ascii(b): return b.decode("ascii","replace").rstrip(" \x00")
def dec_joliet(b):
    if len(b)%2:b=b[:-1]
    return b.decode("utf-16-be","replace").rstrip(" \x00")

def descriptor(block,lba):
    if len(block)<SECTOR or block[1:6]!=b"CD001" or block[0] not in (1,2):return None
    joliet=block[0]==2 and block[88:91] in (b"%/@",b"%/C",b"%/E")
    rl=block[156]
    if rl<34 or 156+rl>len(block):return None
    root=block[156:156+rl]
    return {"type":block[0],"lba":lba,"joliet":joliet,
      "volume_id":dec_joliet(block[40:72]) if joliet else dec_ascii(block[40:72]),
      "root_extent":struct.unpack_from("<I",root,2)[0],
      "root_size":struct.unpack_from("<I",root,10)[0]}

def parse_dir(buf,joliet):
    out=[];pos=0
    while pos<len(buf):
        ln=buf[pos]
        if ln==0:pos=((pos//SECTOR)+1)*SECTOR;continue
        if ln<34 or pos+ln>len(buf):break
        r=buf[pos:pos+ln];nl=r[32]
        if 33+nl>len(r):break
        raw=r[33:33+nl]
        if raw==b"\x00":name="."
        elif raw==b"\x01":name=".."
        else:
            name=dec_joliet(raw) if joliet else raw.decode("ascii","replace")
            name=name.split(";",1)[0]
        out.append({"name":name,"extent":struct.unpack_from("<I",r,2)[0],
                    "size":struct.unpack_from("<I",r,10)[0],"is_dir":bool(r[25]&2)})
        pos+=ln
    return tuple(out)

def relevance(path,size):
    low=path.casefold();reasons=[]
    for t in TOKENS:
        if t.casefold() in low:reasons.append("token:"+t)
    leaf=low.rsplit("/",1)[-1]
    if leaf.endswith(ARCHIVE_EXTS) and abs(int(size)-TARGET_BYTES)<=512*1024:
        reasons.append("archive_size_near_3440K")
    if 3_000_000<=int(size)<=4_200_000 and ("map" in leaf or "patch" in leaf or "update" in leaf):
        reasons.append("map_update_size_window")
    return tuple(reasons)

def scan_iso(identifier,row):
    name=str(row.get("name") or "");url=dl(identifier,name);errors=[]
    st,cr,raw,h=logical_sector_read(url,16,16,0,"MODE1/2048")
    if not h:raise RuntimeError(f"descriptor-range-not-honored:{st}:{cr}")
    desc=[]
    for i in range(16):
        b=raw[i*SECTOR:(i+1)*SECTOR]
        if b and b[0]==255 and b[1:6]==b"CD001":break
        d=descriptor(b,16+i)
        if d:desc.append(d)
    chosen=next((d for d in desc if d["joliet"]),None) or next((d for d in desc if d["type"]==1),None)
    if not chosen:raise RuntimeError("no-supported-volume-descriptor")
    print(f"DISC|identifier={clean(identifier)}|name={clean(name)}|size={clean(row.get('size'))}|md5={clean(row.get('md5'))}|sha1={clean(row.get('sha1'))}|volume_id={clean(chosen['volume_id'])}|joliet={int(chosen['joliet'])}|descriptor_lba={chosen['lba']}")
    q=deque([("",chosen["root_extent"],chosen["root_size"])]);seen=set();dirs=files=hits=0;meta=16*SECTOR
    while q and dirs<MAX_DIRS and meta<MAX_METADATA_BYTES:
        parent,extent,size=q.popleft();key=(extent,size)
        if key in seen:continue
        seen.add(key);dirs+=1
        if size<=0 or size>MAX_DIR_BYTES:continue
        count=math.ceil(size/SECTOR)
        try:
            st2,cr2,b,h2=logical_sector_read(url,extent,count,0,"MODE1/2048");meta+=count*SECTOR
            if not h2:errors.append((parent,"range-not-honored",f"{st2}:{cr2}"));continue
            for e in parse_dir(b[:size],chosen["joliet"]):
                if e["name"] in (".",".."):continue
                p=(parent+"/"+e["name"]).lstrip("/")
                if e["is_dir"]:q.append((p,e["extent"],e["size"]))
                else:
                    files+=1;why=relevance(p,e["size"])
                    if why:
                        hits+=1
                        print(f"HIT|disc={clean(identifier)}|path={clean(p)}|size={e['size']}|extent={e['extent']}|reason={clean(','.join(why))}")
        except Exception as exc:errors.append((parent,type(exc).__name__,str(exc)))
    print(f"DISC_COUNT|identifier={clean(identifier)}|dirs={dirs}|files={files}|metadata_bytes={meta}|hits={hits}|queue_remaining={len(q)}|errors={len(errors)}")
    for p,k,m in errors[:80]:print(f"ERROR|disc={clean(identifier)}|path={clean(p)}|kind={clean(k)}|message={clean(m)}")
    return hits

def main():
    print("StoneAge 4.0 selected coverdisc filesystem scan — R1")
    print("SCOPE|selected-2002Q4-2003Q1-coverdiscs+ISO9660/Joliet-directory-sectors-only|no-file-payload|no-full-ISO")
    total_hits=total_discs=0;errors=[]
    for ident in IDENTIFIERS:
        try:
            meta=get_json("https://archive.org/metadata/"+urllib.parse.quote(ident,safe=""))
            isos=[r for r in meta.get("files",[]) if str(r.get("name") or "").lower().endswith(".iso") and str(r.get("source") or "original")=="original"]
            print(f"ITEM|identifier={clean(ident)}|title={clean((meta.get('metadata') or {}).get('title'))}|date={clean((meta.get('metadata') or {}).get('date'))}|iso_count={len(isos)}")
            for row in isos:
                total_discs+=1
                try:total_hits+=scan_iso(ident,row)
                except Exception as exc:errors.append((ident,str(row.get("name") or ""),type(exc).__name__,str(exc)))
        except Exception as exc:errors.append((ident,"metadata",type(exc).__name__,str(exc)))
    for ident,name,k,m in errors:print(f"ERROR|item={clean(ident)}|name={clean(name)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|discs_scanned|{total_discs}");print(f"COUNT|candidate_hits|{total_hits}");print(f"COUNT|top_errors|{len(errors)}")
    print("RESOLUTION|"+("COVERDISC_FILE_CANDIDATES_FOUND|verify candidate identity and recover only candidate payload if bounded" if total_hits else "NO_COVERDISC_FILENAME_OR_SIZE_HIT|selected directory trees contain no target-like file"))
    print("EVIDENCE_BOUNDARY|coverdisc catalogue dates and directory filenames are discovery evidence; no file body is read and no candidate is promoted without byte verification.")
if __name__=="__main__":main()
