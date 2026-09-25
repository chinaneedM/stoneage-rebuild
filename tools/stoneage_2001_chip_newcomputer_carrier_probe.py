#!/usr/bin/env python3
"""Probe public preservation indexes for the November-2001 CHIP 新电脑 carrier.

A preserved Popsoft issue adds 《CHIP 新电脑》11月号 to the list of media
carrying the StoneAge 2.0 complete upgrade. This probe searches carrier-level
metadata/filesystem indexes; it does not download historical payloads.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"

IA_QUERIES=(
 ("chip-newcomputer-2001", 'title:"CHIP 新电脑" AND year:2001'),
 ("chipnewcomputer-2001", 'title:"CHIP新电脑" AND year:2001'),
 ("newcomputer-2001-11", 'title:"新电脑" AND year:2001 AND (month:11 OR date:[2001-11-01 TO 2001-11-30])'),
 ("chip-2001-11", 'title:CHIP AND year:2001 AND (month:11 OR date:[2001-11-01 TO 2001-11-30])'),
 ("chip-desc-stoneage", 'description:("CHIP 新电脑" AND "石器时代2.0")'),
 ("identifier-chip-2001-11", 'identifier:*chip*2001*11*'),
)
DM_QUERIES=(
 "CHIP 新电脑",
 "CHIP新电脑",
 "新电脑",
 "stoneage2.0setup.exe",
 "stoneage2.0setup",
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

def docs(body):
    obj=json.loads(body.decode("utf-8"))
    return tuple(((obj.get("response") or {}).get("docs") or []))

def dm_url(q,limit=500):
    p=[("q",q),("qfields","name"),("mode","deep"),("limit",str(limit)),("outputAs","json"),("showItemName","showItemName")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def dm_rows(node):
    out=[]
    def walk(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x):
                out.append(x)
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(node)
    uniq={}
    for r in out:
        path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        uniq[(str(r.get("itemid") or ""),path,str(r.get("b3sum") or ""))]=r
    return tuple(uniq.values())

def path_of(r):
    return str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")

def targetish_text(s):
    low=urllib.parse.unquote_plus(str(s or "")).lower().replace(" ","")
    return any(k in low for k in (
      "chip新电脑","新电脑","stoneage2.0setup","石器时代2.0","stoneage2"
    ))

def main():
    print("StoneAge 2.0 CHIP 新电脑 November-2001 carrier probe — R1")
    print("SCOPE|Internet Archive metadata + DiscMaster filename index|carrier-level|no-payload")
    print("TARGET|carrier=CHIP 新电脑 11月号|period=2001-11|client=StoneAge 2.0 complete upgrade")
    errors=[];ia_seen={};dm_seen={}
    for label,q in IA_QUERIES:
        try:
            st,final,h,b=fetch(ia_url(q))
            rr=docs(b)
            print(f"IA_QUERY|label={clean(label)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|q={clean(q)}")
            for d in rr:
                ident=str(d.get("identifier") or "")
                ia_seen[ident]=d
                relevant=int(targetish_text(" ".join(str(d.get(k) or "") for k in ("title","description","identifier"))))
                print(
                  f"IA_HIT|label={clean(label)}|relevant={relevant}|identifier={clean(ident)}|"
                  f"title={clean(d.get('title'))}|date={clean(d.get('date'))}|year={clean(d.get('year'))}|"
                  f"creator={clean(d.get('creator'))}|uploader={clean(d.get('uploader'))}|"
                  f"collection={clean(d.get('collection'))}|mediatype={clean(d.get('mediatype'))}|"
                  f"description={clean(d.get('description'),1200)}"
                )
        except Exception as e:
            errors.append(("ia:"+label,type(e).__name__,str(e)))
    for q in DM_QUERIES:
        try:
            st,final,h,b=fetch(dm_url(q))
            rr=dm_rows(json.loads(b.decode("utf-8")))
            print(f"DM_QUERY|q={clean(q)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rr:
                path=path_of(r)
                key=(str(r.get("itemid") or ""),path,str(r.get("b3sum") or ""))
                dm_seen[key]=r
                relevant=int(targetish_text((r.get("itemName") or "")+" "+path))
                print(
                  f"DM_HIT|q={clean(q)}|relevant={relevant}|itemid={clean(r.get('itemid'))}|"
                  f"itemName={clean(r.get('itemName'))}|path={clean(path)}|size={clean(r.get('size'))}|"
                  f"ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}"
                )
        except Exception as e:
            errors.append(("dm:"+q,type(e).__name__,str(e)))
    ia_rel=[d for d in ia_seen.values() if targetish_text(" ".join(str(d.get(k) or "") for k in ("title","description","identifier")))]
    dm_rel=[r for r in dm_seen.values() if targetish_text((r.get("itemName") or "")+" "+path_of(r))]
    print(f"COUNT|ia_unique_items|{len(ia_seen)}")
    print(f"COUNT|ia_relevant_items|{len(ia_rel)}")
    print(f"COUNT|dm_unique_rows|{len(dm_seen)}")
    print(f"COUNT|dm_relevant_rows|{len(dm_rel)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if ia_rel or dm_rel:
        print("RESOLUTION|CARRIER_CANDIDATE_FOUND|classify exact issue/disc date and filesystem before any client provenance promotion")
    else:
        print("RESOLUTION|NO_CHIP_2001_CARRIER_HIT|tested public IA/DiscMaster surfaces expose no relevant preserved carrier")
    print("EVIDENCE_BOUNDARY|carrier/index metadata is discovery evidence only; no client byte identity is inferred from magazine title or month.")

if __name__=="__main__":
    main()
