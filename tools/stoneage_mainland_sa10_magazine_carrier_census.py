#!/usr/bin/env python3
"""Probe candidate magazine/cover-disc carriers for the Mainland StoneAge test package.

Evidence boundary:
- A collector with direct possession history states that the Mainland 1.0 test
  package was a test manual + CD supplied with a magazine and had no box.
- The exact magazine title is unknown.
- Candidate publications below are search heuristics only. They are drawn from
  later documented Beijing-Waei client-distribution channels plus Jinghe's own
  disc channel. They are NOT asserted to be the Dec-2000 carrier.

This probe queries public preservation indexes only (Internet Archive metadata
and DiscMaster search). It never downloads a magazine-disc or client payload.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"

CANDIDATES=(
    ("diannaobao-gameworld","电脑报 游戏世界"),
    ("diannaoxiaoyuan","电脑校园"),
    ("shaoniandianshijie","少年电世界"),
    ("wangshangjulebu-youxiba","网上俱乐部 游戏吧"),
    ("xinyouxiren","新游戏人"),
    ("youxiyuandongli","游戏原动力"),
    ("gamestar","GAMESTAR 游戏族"),
    ("homepcgame","家用电脑与游戏"),
    ("homepcgameji","家用电脑与游戏机"),
    ("dazhongruanjian","大众软件"),
    ("jinghe-mizang","晶合秘藏"),
)
STONE_TERMS=("石器时代","StoneAge")
YEAR_MIN="1999"
YEAR_MAX="2002"

def clean(v,n=4000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def norm(v):
    return re.sub(r"[^0-9a-z一-鿿]+","",str(v or "").lower())

def fetch_json(url,timeout=45,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8"))

def ia_url(candidate,stone):
    q=f'("{candidate}") AND ("{stone}") AND year:[{YEAR_MIN} TO {YEAR_MAX}]'
    p=[
        ("q",q),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("fl[]","year"),
        ("fl[]","description"),("fl[]","collection"),("fl[]","mediatype"),
        ("rows","100"),("page","1"),("output","json"),
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(candidate,stone,field="t"):
    q=f'"{candidate}" "{stone}"'
    p=[
        ("q",q),("qfields",field),("mode","deep"),("dedup","dedup"),
        ("limit","200"),("outputAs","json"),("showItemName","showItemName"),
        ("tsMin",YEAR_MIN),("tsMax",YEAR_MAX),
    ]
    return DISCM+"?"+urllib.parse.urlencode(p)

def ia_docs(data):
    return tuple(x for x in data.get("response",{}).get("docs",[]) if isinstance(x,dict))

def discm_rows(data):
    rows=[]
    def walk(n):
        if isinstance(n,dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n):
                rows.append(n)
            for v in n.values(): walk(v)
        elif isinstance(n,list):
            for v in n: walk(v)
    walk(data)
    out=[]; seen=set()
    for row in rows:
        key=(str(row.get("itemid","")),str(row.get("fileid","")),str(row.get("href","")))
        if key not in seen:
            seen.add(key); out.append(row)
    return tuple(out)

def row_blob(row):
    if not isinstance(row,dict): return ""
    return norm(" ".join(str(v or "") for v in row.values()))

def main():
    print("StoneAge Mainland 1.0 magazine/carrier candidate preservation census — R1")
    print("SCOPE|candidate-publication heuristic|InternetArchive+DiscMaster metadata/search only|1999..2002|no payload")
    print("SOURCE_ANCHOR|collector first-person claim: Mainland 1.0 test package = test manual + CD + magazine giveaway + no box")
    print("CANDIDATE_BOUNDARY|candidate titles are later documented Beijing-Waei distribution channels / Jinghe disc-channel controls; none is assigned to Dec-2000 without direct evidence")

    errors=[]
    ia_hits=[]
    dm_hits=[]

    jobs=[]
    for label,candidate in CANDIDATES:
        for stone in STONE_TERMS:
            jobs.append(("ia",label,candidate,stone,""))
            jobs.append(("discm",label,candidate,stone,"t"))
            jobs.append(("discm",label,candidate,stone,"name"))

    def one(kind,label,candidate,stone,field):
        url=ia_url(candidate,stone) if kind=="ia" else discm_url(candidate,stone,field)
        st,final,b,data=fetch_json(url,timeout=55)
        rows=ia_docs(data) if kind=="ia" else discm_rows(data)
        return kind,label,candidate,stone,field,st,final,b,rows

    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs={ex.submit(one,*j):j for j in jobs}
        for fut in concurrent.futures.as_completed(futs):
            j=futs[fut]
            try:
                results.append(fut.result())
            except Exception as e:
                errors.append((f"{j[0]}:{j[1]}:{j[3]}:{j[4]}",type(e).__name__,str(e)))

    for kind,label,candidate,stone,field,st,final,b,rows in sorted(results,key=lambda x:(x[1],x[0],x[3],x[4])):
        sha=hashlib.sha256(b).hexdigest()
        if kind=="ia":
            print(f"IA_QUERY|label={label}|candidate={clean(candidate)}|stone={clean(stone)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={sha}|final={clean(final)}")
            for row in rows:
                blob=row_blob(row)
                stone_ok=("石器时代" in blob or "stoneage" in blob)
                candidate_ok=norm(candidate) in blob
                ia_hits.append((label,candidate,stone,row,stone_ok,candidate_ok))
                print(
                    f"IA_HIT|label={label}|candidate_ok={int(candidate_ok)}|stone_ok={int(stone_ok)}|"
                    f"identifier={clean(row.get('identifier'))}|title={clean(row.get('title'))}|"
                    f"date={clean(row.get('date'))}|year={clean(row.get('year'))}|collection={clean(row.get('collection'))}|mediatype={clean(row.get('mediatype'))}"
                )
        else:
            print(f"DISCM_QUERY|label={label}|candidate={clean(candidate)}|stone={clean(stone)}|field={field}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={sha}|final={clean(final)}")
            for row in rows:
                dm_hits.append((label,candidate,stone,field,row))
                print(
                    f"DISCM_HIT|label={label}|field={field}|itemid={clean(row.get('itemid'))}|"
                    f"itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|"
                    f"filename={clean(row.get('filename'))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
                )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")

    ia_strict=[x for x in ia_hits if x[4] and x[5]]
    print(f"COUNT|candidates={len(CANDIDATES)}")
    print(f"COUNT|queries_planned={len(jobs)}")
    print(f"COUNT|ia_hits={len(ia_hits)}")
    print(f"COUNT|ia_strict={len(ia_strict)}")
    print(f"COUNT|discm_hits={len(dm_hits)}")
    print(f"COUNT|errors={len(errors)}")

    labels=sorted({x[0] for x in ia_strict} | {x[0] for x in dm_hits})
    print("HIT_LABELS|"+",".join(labels))
    if ia_strict or dm_hits:
        print("RESOLUTION|MAGAZINE_CARRIER_PRESERVATION_SIGNAL_FOUND|inspect exact item/file identity and issue date before any provenance upgrade")
    elif errors and len(results)<len(jobs):
        print("RESOLUTION|MAGAZINE_CARRIER_CENSUS_PARTIAL|retry failed candidate surfaces only")
    else:
        print("RESOLUTION|MAGAZINE_CANDIDATE_INDEX_SURFACE_BOUNDED|no indexed StoneAge co-occurrence in tested candidate publications; magazine identity remains open")
    print("EVIDENCE_BOUNDARY|A query hit is only preservation/search evidence. It does not prove that publication carried the Dec-2000 test package unless issue/date/content directly bind the test manual/CD.")

if __name__=="__main__":
    main()
