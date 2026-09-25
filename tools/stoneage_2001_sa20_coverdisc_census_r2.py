#!/usr/bin/env python3
"""Refined Internet Archive census for named Mainland StoneAge 2.0 carriers.

R1 used unfielded full-text metadata searches and produced unrelated description
noise. R2 restricts carrier discovery to title fields and software media, plus
two StoneAge-specific software-metadata queries. Metadata only; no payload.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"

CARRIERS=(
 ("pc-renwoxing","PC任我行"),
 ("dazhong-software-cd","大众软件CD"),
 ("computer-magazine","电脑"),
 ("computer-fan-games","电脑爱好者"),
 ("computer-news-gameworld","游戏世界"),
 ("computer-campus","电脑校园"),
 ("jinghe-ruby","晶合秘藏"),
 ("young-computer-world","少年电世界"),
 ("online-club-gamebar","网上俱乐部"),
 ("new-gamer","新游戏人"),
 ("game-power","游戏原动力"),
 ("shengbier-sa20-guide","石器时代2.0攻略"),
 ("tengtu-stoneage-guide","石器时代攻略全集"),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def ia_url(q,rows=100):
    p=[
      ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
      ("fl[]","year"),("fl[]","description"),("fl[]","creator"),
      ("fl[]","mediatype"),("rows",str(rows)),("page","1"),("output","json")
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def title_query(phrase,key):
    esc=phrase.replace('"','\\\"')
    q=f'title:"{esc}" AND mediatype:software'
    if key=="computer-magazine":
        q=f'title:"{esc}" AND year:2001 AND mediatype:software'
    return q

def docs(body):
    obj=json.loads(body.decode("utf-8"))
    return tuple(((obj.get("response") or {}).get("docs") or []))

def emit(label,rows):
    print(f"COUNT|label={clean(label)}|rows={len(rows)}")
    for d in rows:
        print(
          f"HIT|label={clean(label)}|identifier={clean(d.get('identifier'))}|"
          f"title={clean(d.get('title'))}|date={clean(d.get('date'))}|year={clean(d.get('year'))}|"
          f"creator={clean(d.get('creator'))}|mediatype={clean(d.get('mediatype'))}|"
          f"description={clean(d.get('description'),1200)}"
        )

def main():
    print("StoneAge 2.0 named coverdisc carrier census — R2")
    print("SCOPE|Internet Archive title-field carrier search + StoneAge-specific software metadata|metadata-only|no-payload")
    errors=[];total=0
    for key,phrase in CARRIERS:
        q=title_query(phrase,key)
        try:
            st,final,h,b=fetch(ia_url(q))
            rr=docs(b); total+=len(rr)
            print(f"QUERY|key={key}|phrase={clean(phrase)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|q={clean(q)}")
            emit(key,rr)
        except Exception as e:
            errors.append((key,type(e).__name__,str(e)))
    globals_=(
      ("stoneage20-title",'title:"石器时代2.0" AND mediatype:software'),
      ("stoneage20-description",'description:"石器时代2.0" AND mediatype:software'),
      ("stoneage20-en",'("StoneAge 2.0" OR "Stone Age 2.0") AND mediatype:software'),
    )
    for label,q in globals_:
        try:
            st,final,h,b=fetch(ia_url(q,200))
            rr=docs(b); total+=len(rr)
            print(f"QUERY|key={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|q={clean(q)}")
            emit(label,rr)
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    print(f"COUNT|carriers|{len(CARRIERS)}")
    print(f"COUNT|all_rows|{total}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if total:
        print("RESOLUTION|REFINED_CANDIDATES_FOUND|classify exact carrier/version relevance before any filesystem read")
    else:
        print("RESOLUTION|NO_REFINED_CARRIER_CANDIDATE|title/software metadata exposes no named carrier or StoneAge 2.0 item")
    print("EVIDENCE_BOUNDARY|IA metadata hits identify candidate preserved items only; client presence and provenance require file-level verification.")

if __name__=="__main__":
    main()
