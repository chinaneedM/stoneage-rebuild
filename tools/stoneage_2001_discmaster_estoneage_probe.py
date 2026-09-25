#!/usr/bin/env python3
"""Expand DiscMaster's small non-strict 'estoneage' result set.

The primary preservation probe reported three rows for query 'estoneage' but no
exact Estoneage2.0map_1127.exe match. This diagnostic prints those rows and a
bounded item-local StoneAge/map neighborhood, metadata only.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
DISCM="https://discmaster.textfiles.com/search"
TARGET="Estoneage2.0map_1127.exe"

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def search_url(q,limit=500):
    p=[("q",q),("qfields","name"),("mode","deep"),("limit",str(limit)),("outputAs","json"),("showItemName","showItemName")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def walk_rows(node):
    rows=[]
    def walk(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x):
                rows.append(x)
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(node)
    uniq={}
    for r in rows:
        path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        key=(str(r.get("itemid") or ""),path,str(r.get("b3sum") or ""))
        uniq[key]=r
    return tuple(uniq.values())

def row_path(r):
    return str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")

def strict(r):
    return row_path(r).replace("\\","/").rsplit("/",1)[-1].lower()==TARGET.lower()

def main():
    print("StoneAge 2001 DiscMaster estoneage diagnostic — R1")
    print("SCOPE|DiscMaster non-strict estoneage rows + bounded metadata context|no-payload")
    print(f"TARGET|filename={TARGET}")
    errors=[];allrows=[]
    for q in ("estoneage","Estoneage2.0map","Estoneage2.0map_1127"):
        try:
            st,final,h,b=fetch(search_url(q),timeout=45)
            obj=json.loads(b.decode("utf-8")); rows=walk_rows(obj)
            print(f"QUERY|q={clean(q)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rows:
                allrows.append(r)
                print(
                    f"ROW|q={clean(q)}|strict={int(strict(r))}|itemid={clean(r.get('itemid'))}|"
                    f"itemName={clean(r.get('itemName'))}|path={clean(row_path(r))}|"
                    f"size={clean(r.get('size'))}|ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}"
                )
        except Exception as e:
            errors.append((q,type(e).__name__,str(e)))
    uniq={}
    for r in allrows:
        key=(str(r.get("itemid") or ""),row_path(r),str(r.get("b3sum") or ""))
        uniq[key]=r
    print(f"COUNT|unique_rows|{len(uniq)}")
    print(f"COUNT|strict_rows|{sum(1 for r in uniq.values() if strict(r))}")
    for q,k,m in errors:
        print(f"ERROR|q={clean(q)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if any(strict(r) for r in uniq.values()):
        print("RESOLUTION|STRICT_TARGET_FOUND|verify carrier metadata and file identity before any recovery")
    elif uniq:
        print("RESOLUTION|NONSTRICT_ROWS_ONLY|classify rows as possible naming/directory controls; do not promote to target")
    else:
        print("RESOLUTION|NO_ESTONEAGE_ROWS|previous non-strict result is no longer reproduced")
    print("EVIDENCE_BOUNDARY|DiscMaster index rows are discovery metadata; similar names do not establish StoneAge target identity.")

if __name__=="__main__":
    main()
