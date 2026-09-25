#!/usr/bin/env python3
"""Probe preservation indexes for a bounded cluster of 2000 Sina StoneAge packages.

The cluster comes from surviving Sina download pages and spans Aug-Dec 2000.
Only metadata/search results are fetched; no package payload is downloaded.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"
ARQUIVO="https://arquivo.pt/textsearch"

TOKENS=(
 ("map-display","0969-5_807.zip",16654,925,"2000-08-07"),
 ("speed","0969-4_807.zip",16653,106,"2000-08-07"),
 ("speed-teleport","0969-6_807.zip",16652,33,"2000-08-07"),
 ("screensaver","stoneage_800_1219.zip",23186,2220,"2000-12-19"),
 ("full-map","samap_1220.zip",23223,1410,"2000-12-20"),
 ("north-island","northisland_1228.zip",23680,134,"2000-12-28"),
 ("south-island","southisland_1228.zip",23681,202,"2000-12-28"),
)

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=3*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,text/html,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def ia_url(filename):
    p=[("q",f'"{filename}"'),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("rows","100"),("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(filename):
    p=[("q",filename),("qfields","name"),("mode","deep"),("limit","500"),("outputAs","json"),("showItemName","showItemName")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def arquivo_url(filename):
    p=[("q",f'"{filename}"'),("maxItems","100")]
    return ARQUIVO+"?"+urllib.parse.urlencode(p)

def rows_walk(x):
    out=[]
    def w(v):
        if isinstance(v,dict):
            if ("itemid" in v or "itemName" in v) and ("fileid" in v or "filename" in v or "name" in v):
                out.append(v)
            for z in v.values(): w(z)
        elif isinstance(v,list):
            for z in v:w(z)
    w(x);return out

def leaf(path):
    return str(path).replace("\\","/").rsplit("/",1)[-1].lower()

def exact_disc_rows(data,filename):
    target=filename.lower()
    out=[]
    for r in rows_walk(data):
        path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        if leaf(path)==target: out.append(r)
    return tuple(out)

def arquivo_rows(data):
    if not isinstance(data,dict): return ()
    for k in ("response_items","items","results"):
        v=data.get(k)
        if isinstance(v,list): return tuple(v)
    return ()

def main():
    print("StoneAge 2000 Sina package-cluster preservation probe — R1")
    print("SCOPE|7 exact Sina package tokens + IA/DiscMaster/Arquivo public indexes|metadata-only|no-payload")
    errors=[];strict=[];arquivo_ok=0;arquivo_fail=0
    for role,fn,aid,size,date in TOKENS:
        print(f"TOKEN|role={role}|date={date}|aid={aid}|filename={fn}|size_kib={size}")
        try:
            st,final,h,b=fetch(ia_url(fn),timeout=35)
            d=json.loads(b.decode("utf-8"));docs=((d.get("response") or {}).get("docs") or [])
            print(f"IA|role={role}|status={st}|items={len(docs)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for x in docs[:50]:
                print(f"IA_HIT|role={role}|identifier={clean(x.get('identifier'))}|title={clean(x.get('title'))}|date={clean(x.get('date'))}")
                strict.append(("ia",role,fn,x))
        except Exception as e: errors.append((f"ia:{role}",type(e).__name__,str(e)))

        try:
            st,final,h,b=fetch(discm_url(fn),timeout=45)
            d=json.loads(b.decode("utf-8"));rr=exact_disc_rows(d,fn)
            print(f"DISCM|role={role}|status={st}|strict_rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for x in rr:
                path=str(x.get("fileid") or x.get("path") or x.get("filename") or x.get("name") or "")
                print(f"DISCM_HIT|role={role}|itemid={clean(x.get('itemid'))}|itemName={clean(x.get('itemName'))}|path={clean(path)}|size={clean(x.get('size'))}|ts={clean(x.get('ts'))}|b3sum={clean(x.get('b3sum'))}")
                strict.append(("discm",role,fn,x))
        except Exception as e: errors.append((f"discm:{role}",type(e).__name__,str(e)))

        try:
            st,final,h,b=fetch(arquivo_url(fn),timeout=35)
            d=json.loads(b.decode("utf-8"));rr=arquivo_rows(d);arquivo_ok+=1
            print(f"ARQUIVO|role={role}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for x in rr[:50]:
                print(f"ARQUIVO_HIT|role={role}|url={clean(x.get('originalURL') or x.get('url'))}|title={clean(x.get('title'))}|tstamp={clean(x.get('tstamp') or x.get('timestamp'))}")
                strict.append(("arquivo",role,fn,x))
        except Exception as e:
            arquivo_fail+=1;errors.append((f"arquivo:{role}",type(e).__name__,str(e)))

    print(f"COUNT|strict_index_hits|{len(strict)}")
    print(f"COUNT|arquivo_success|{arquivo_ok}")
    print(f"COUNT|arquivo_fail|{arquivo_fail}")
    for s,k,m in errors[:200]:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if strict:
        print("RESOLUTION|CLUSTER_CARRIER_LEAD_FOUND|inspect exact hit provenance and neighboring files before any payload recovery")
    elif arquivo_fail:
        print("RESOLUTION|NO_CLUSTER_CARRIER_ON_COMPLETED_INDEXES|IA+DiscMaster strict exact-name searches are zero for all seven tokens; Arquivo coverage is incomplete because some queries failed")
    else:
        print("RESOLUTION|NO_CLUSTER_CARRIER_ON_TESTED_INDEXES|seven-token early-Sina carrier cluster is bounded on all three tested public indexes")
    print("EVIDENCE_BOUNDARY|an index hit is a carrier lead only; package identity requires exact filename/size and recovered bytes.")

if __name__=="__main__":
    main()
