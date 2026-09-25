#!/usr/bin/env python3
"""Transient full recovery and derived inventory for the 2003-06-23 map.exe capture."""
from __future__ import annotations
import argparse, hashlib, os, pathlib, struct, urllib.request

URL="https://web.archive.org/web/20030623234451id_/http://www.wuxitianlong.com:80/sa/map.exe"
EXPECTED_SIZE=4223728
MAX_SIZE=8*1024*1024
UA="stoneage-rebuild-archaeology/1.0"

def clean(v,limit=1800):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c >= " " and c != "\x7f").replace("|","%7C")[:limit]

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def hget(headers,name):
    want=name.lower()
    for k,v in headers.items():
        if str(k).lower()==want: return v
    return ""

def recover(path):
    if EXPECTED_SIZE>MAX_SIZE: raise RuntimeError("expected-size-over-bound")
    req=urllib.request.Request(URL,headers={
        "User-Agent":UA,"Accept":"*/*","Accept-Encoding":"identity",
        "Range":f"bytes=0-{EXPECTED_SIZE-1}",
    })
    with urllib.request.urlopen(req,timeout=90) as r:
        body=r.read(MAX_SIZE+1)
        status=int(getattr(r,"status",r.getcode()))
        headers=dict(r.headers.items())
        final=r.geturl()
    if len(body)>MAX_SIZE: raise RuntimeError("payload-over-bound")
    if len(body)!=EXPECTED_SIZE: raise RuntimeError(f"size-mismatch:{len(body)}")
    cr=hget(headers,"Content-Range")
    if cr and not cr.endswith(f"/{EXPECTED_SIZE}"):
        raise RuntimeError(f"content-range-total-mismatch:{cr}")
    with open(path,"wb") as f: f.write(body)
    print(
        f"PAYLOAD|status={status}|final={clean(final)}|size={len(body)}|"
        f"sha256={sha256_bytes(body)}|content_range={clean(cr)}|"
        f"orig_last_modified={clean(hget(headers,'X-Archive-Orig-Last-Modified'))}|"
        f"memento={clean(hget(headers,'Memento-Datetime'))}"
    )

def dat_info(data):
    if len(data)<8: return None
    w,h=struct.unpack_from("<II",data,0)
    if w==0 or h==0 or w>10000 or h>10000: return None
    cells=w*h
    expected=8+cells*6
    return {"width":w,"height":h,"cells":cells,"expected":expected,"valid":int(expected==len(data))}

def analyze(root):
    root=pathlib.Path(root)
    files=sorted(p for p in root.rglob("*") if p.is_file())
    print("StoneAge historical map.exe extracted inventory — R1")
    print("SCOPE|transient-full-4MiB-SFX+derived-file-hashes+DAT-structure|no-payload-commit")
    print(f"COUNT|files|{len(files)}")
    print(f"COUNT|bytes|{sum(p.stat().st_size for p in files)}")
    dats=[]
    agg=hashlib.sha256()
    for p in files:
        rel=p.relative_to(root).as_posix()
        size=p.stat().st_size
        digest=sha256_file(p)
        agg.update(rel.encode("utf-8","surrogateescape")+b"\0"+str(size).encode()+b"\0"+digest.encode()+b"\n")
        if p.suffix.lower()==".dat":
            data=p.read_bytes()
            info=dat_info(data)
            dats.append((p,rel,size,digest,info))
        else:
            print(f"FILE|path={clean(rel)}|size={size}|sha256={digest}")
    print(f"AGGREGATE_SHA256|{agg.hexdigest()}")
    print(f"COUNT|dat_files|{len(dats)}")
    valid=0
    ids=[]
    for p,rel,size,digest,info in dats:
        stem=p.stem
        if stem.isdigit(): ids.append(int(stem))
        if info and info["valid"]: valid+=1
        if info:
            print(
                f"DAT|path={clean(rel)}|size={size}|sha256={digest}|"
                f"width={info['width']}|height={info['height']}|cells={info['cells']}|"
                f"expected={info['expected']}|valid_three_layer={info['valid']}"
            )
        else:
            print(f"DAT|path={clean(rel)}|size={size}|sha256={digest}|valid_three_layer=0")
    print(f"COUNT|dat_valid_three_layer|{valid}")
    if ids:
        ids=sorted(set(ids))
        print(f"DAT_ID_RANGE|min={ids[0]}|max={ids[-1]}|numeric_unique={len(ids)}")
        missing=[x for x in range(ids[0],ids[-1]+1) if x not in set(ids)]
        print("DAT_ID_SAMPLE|first="+",".join(map(str,ids[:30]))+"|last="+",".join(map(str,ids[-30:])))
        print("DAT_MISSING_SAMPLE|"+",".join(map(str,missing[:120])))
    print("EVIDENCE_BOUNDARY|the recovered executable and extracted map bytes are transient CI artifacts; only derived hashes, paths and structural metadata are committed.")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--recover")
    ap.add_argument("--analyze")
    args=ap.parse_args()
    if bool(args.recover)==bool(args.analyze): ap.error("choose exactly one")
    if args.recover: recover(args.recover)
    else: analyze(args.analyze)

if __name__=="__main__": main()
