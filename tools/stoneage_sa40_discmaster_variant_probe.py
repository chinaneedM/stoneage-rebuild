#!/usr/bin/env python3
"""Search DiscMaster for historical StoneAge 4.0 map-patch filename variants.

The exact Sina filename is absent from previous exact searches. Optical media
may preserve ISO9660 8.3/truncated names, repacked names, or only distinctive
date/update tokens. This probe searches those bounded variants and filters the
returned file-level rows. Metadata only.
"""
from __future__ import annotations
import hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
BASE="https://discmaster.textfiles.com/search"
TARGET_SIZE=3440*1024
QUERIES=(
    "shiqi4",
    "shiqi",
    "shiqi4updatex",
    "updatex_02_11_08",
    "02_11_08",
    "02-11-08",
    "shiqi4up",
    "shiqi4u",
    "shiqi4~1",
)
TOKENS=("shiqi","stoneage","stone age","02_11_08","02-11-08","updatex","shiqi4")

def clean(v,n=2600):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch_json(url,timeout=45):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8"))

def url(q):
    params=[("q",q),("qfields","name"),("mode","deep"),("limit","500"),("outputAs","json"),("showItemName","showItemName")]
    return BASE+"?"+urllib.parse.urlencode(params)

def rows(value):
    out=[]
    def walk(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x):
                out.append(x)
            for y in x.values(): walk(y)
        elif isinstance(x,list):
            for y in x: walk(y)
    walk(value)
    d={}
    for r in out:
        p=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        k=(str(r.get("itemid") or ""),p)
        d[k]=r
    return tuple(d.values())

def path(r):
    return str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")

def score(r):
    p=path(r).lower().replace("\\","/")
    leaf=p.rsplit("/",1)[-1]
    s=0; reasons=[]
    for t in TOKENS:
        if t in leaf:
            s+=8; reasons.append("leaf:"+t)
        elif t in p:
            s+=3; reasons.append("path:"+t)
    if leaf.endswith((".zip",".rar",".exe",".7z",".cab")):
        s+=2; reasons.append("archive_ext")
    try:
        z=int(r.get("size") or 0)
        if z and abs(z-TARGET_SIZE)<=256*1024:
            s+=5; reasons.append("size_near_3440K")
    except Exception: pass
    return s,",".join(reasons)

def main():
    print("StoneAge 4.0 DiscMaster filename-variant probe — R2")
    print("SCOPE|ISO9660-8.3+truncation+date-token+repack-name-search|file-index-metadata-only|no-payload")
    errors=[]; allrows={}
    for q in QUERIES:
        try:
            st,final,b,obj=fetch_json(url(q))
            rr=rows(obj)
            print(f"QUERY|q={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rr)}|final={clean(final)}")
            for r in rr:
                k=(str(r.get("itemid") or ""),path(r))
                allrows[k]=r
        except Exception as exc:
            errors.append((q,type(exc).__name__,str(exc)))
    ranked=[]
    for r in allrows.values():
        s,why=score(r)
        if s>0: ranked.append((s,why,r))
    ranked.sort(key=lambda x:(-x[0],path(x[2]).lower()))
    print(f"COUNT|unique_rows|{len(allrows)}")
    print(f"COUNT|ranked_rows|{len(ranked)}")
    for i,(s,why,r) in enumerate(ranked[:300],1):
        print(
          f"HIT|rank={i}|score={s}|reason={clean(why)}|itemid={clean(r.get('itemid'))}|"
          f"itemName={clean(r.get('itemName'))}|path={clean(path(r))}|size={clean(r.get('size'))}|"
          f"ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}"
        )
    for q,k,m in errors:
        print(f"ERROR|q={clean(q)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if ranked:
        print("RESOLUTION|VARIANT_FILE_ROWS_FOUND|inspect top rows for StoneAge identity before payload recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_VARIANT_HIT|one or more query surfaces failed")
    else:
        print("RESOLUTION|NO_VARIANT_FILE_HIT|bounded filename-variant search found no candidate")

if __name__=="__main__": main()
