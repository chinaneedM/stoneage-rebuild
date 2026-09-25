#!/usr/bin/env python3
"""Census preservation indexes for xinhaonanhai-linked StoneAge map carriers.

The active 2001 full-map target and the later 2002 StoneAge 4.0 full-map patch
share the contributor alias xinhaonanhai. This probe searches Internet Archive
metadata and DiscMaster filename indexes using the alias plus both exact/stem
package identities. Metadata only; no historical payload is downloaded.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"
TARGETS=("Estoneage2.0map_1127.exe","shiqi4updatex_02_11_08.zip")
IA_QUERIES=(
 ("alias",'xinhaonanhai AND mediatype:software'),
 ("alias-description",'description:xinhaonanhai AND mediatype:software'),
 ("alias-title",'title:xinhaonanhai AND mediatype:software'),
 ("map2001-stem",'"Estoneage2.0map_1127" AND mediatype:software'),
 ("map2002-stem",'"shiqi4updatex_02_11_08" AND mediatype:software'),
 ("community-map",'("游民部落" AND "石器时代" AND "地图") AND mediatype:software'),
)
TOKENS=("xinhaonanhai","estoneage2.0map_1127","shiqi4updatex_02_11_08")
DM_QUERIES=(
 "xinhaonanhai",
 "Estoneage2.0map_1127.exe",
 "Estoneage2.0map_1127",
 "shiqi4updatex_02_11_08.zip",
 "shiqi4updatex_02_11_08",
 "shiqi4updatex",
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=6*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def ia_url(q,rows=200):
    p=[
      ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
      ("fl[]","year"),("fl[]","creator"),("fl[]","uploader"),
      ("fl[]","collection"),("fl[]","mediatype"),("fl[]","description"),
      ("rows",str(rows)),("page","1"),("output","json")
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def ia_docs(body):
    obj=json.loads(body.decode("utf-8"))
    return tuple(((obj.get("response") or {}).get("docs") or []))

def ia_relevant(d):
    fields=("identifier","title","creator","uploader","description")
    text=" ".join(str(d.get(k) or "") for k in fields).lower()
    return any(t in text for t in TOKENS)

def dm_url(q,limit=500):
    p=[("q",q),("qfields","name"),("mode","deep"),("limit",str(limit)),("outputAs","json"),("showItemName","showItemName")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def dm_rows(node):
    rows=[]
    def walk(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x):
                rows.append(x)
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(node)
    uniq={}
    for r in rows:
        path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        uniq[(str(r.get("itemid") or ""),path,str(r.get("b3sum") or ""))]=r
    return tuple(uniq.values())

def dm_path(r):
    return str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")

def strict_leaf(path):
    leaf=str(path).replace("\\","/").rsplit("/",1)[-1].lower()
    return next((t for t in TARGETS if leaf==t.lower()),"")

def main():
    print("StoneAge xinhaonanhai carrier census — R2")
    print("SCOPE|IA metadata + DiscMaster filename index|same-contributor/two-generation map package discovery|no-payload")
    print("TARGET|2001=Estoneage2.0map_1127.exe|2002=shiqi4updatex_02_11_08.zip|alias=xinhaonanhai")
    errors=[]; ia_seen={}; ia_rel={}; dm_seen={}
    for label,q in IA_QUERIES:
        try:
            st,final,h,b=fetch(ia_url(q))
            rows=ia_docs(b)
            print(f"IA_QUERY|label={label}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|q={clean(q)}")
            for d in rows:
                ident=str(d.get("identifier") or "")
                ia_seen[ident]=d
                rel=ia_relevant(d)
                if rel: ia_rel[ident]=d
                print(
                  f"IA_HIT|label={label}|relevant={int(rel)}|identifier={clean(ident)}|title={clean(d.get('title'))}|"
                  f"date={clean(d.get('date'))}|year={clean(d.get('year'))}|creator={clean(d.get('creator'))}|"
                  f"uploader={clean(d.get('uploader'))}|collection={clean(d.get('collection'))}|"
                  f"description={clean(d.get('description'),1000)}"
                )
        except Exception as e:
            errors.append(("ia:"+label,type(e).__name__,str(e)))
    for q in DM_QUERIES:
        try:
            st,final,h,b=fetch(dm_url(q))
            rows=dm_rows(json.loads(b.decode("utf-8")))
            print(f"DM_QUERY|q={clean(q)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rows:
                path=dm_path(r); target=strict_leaf(path)
                key=(str(r.get("itemid") or ""),path,str(r.get("b3sum") or ""))
                dm_seen[key]=r
                print(
                  f"DM_HIT|q={clean(q)}|strict_target={clean(target)}|itemid={clean(r.get('itemid'))}|"
                  f"itemName={clean(r.get('itemName'))}|path={clean(path)}|size={clean(r.get('size'))}|"
                  f"ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}"
                )
        except Exception as e:
            errors.append(("dm:"+q,type(e).__name__,str(e)))
    strict=[]
    for r in dm_seen.values():
        t=strict_leaf(dm_path(r))
        if t: strict.append((t,r))
    print(f"COUNT|ia_raw_unique_items|{len(ia_seen)}")
    print(f"COUNT|ia_relevant_items|{len(ia_rel)}")
    print(f"COUNT|dm_unique_rows|{len(dm_seen)}")
    print(f"COUNT|strict_filename_rows|{len(strict)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if strict:
        print("RESOLUTION|STRICT_CARRIER_ROW_FOUND|inspect carrier metadata/filesystem before any payload recovery or provenance promotion")
    elif ia_rel or dm_seen:
        print("RESOLUTION|NONSTRICT_RELEVANT_CANDIDATES_ONLY|classify alias/stem hits; do not promote without exact carrier linkage")
    else:
        print("RESOLUTION|NO_CONTRIBUTOR_CARRIER_HIT|tested IA/DiscMaster alias+two-generation package surface exposes no relevant candidate; broad Chinese-query rows were filtered as unrelated noise")
    print("EVIDENCE_BOUNDARY|index metadata is discovery evidence only; alias continuity does not prove byte ancestry or operator originality.")

if __name__=="__main__":
    main()
