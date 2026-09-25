#!/usr/bin/env python3
"""Census public preservation indexes for named Mainland StoneAge 2.0 carriers.

Carrier names come from the preserved 17173 2.0 upgrade guide. The first pass
uses metadata/index search only: Internet Archive item metadata and DiscMaster
deep-name results. It does not download disc images or client payloads.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"

CARRIERS=(
 ("pc-renwoxing","PC任我行 2001 11"),
 ("dazhong-software-cd","大众软件CD 2001 11"),
 ("computer-magazine","电脑 2001 11 光盘"),
 ("computer-fan-games","电脑爱好者 玩游戏 2001 11"),
 ("computer-news-gameworld","电脑报 游戏世界 2001 11"),
 ("computer-campus","电脑校园 2001 11"),
 ("jinghe-ruby","晶合秘藏 红宝石"),
 ("young-computer-world","少年电世界 2001 11"),
 ("online-club-gamebar","网上俱乐部 游戏吧 2001 11"),
 ("new-gamer","新游戏人 2001 11"),
 ("game-power","游戏原动力 2001 11"),
 ("shengbier-sa20-guide","石器时代2.0攻略 圣比尔"),
 ("tengtu-stoneage-guide","石器时代攻略全集 腾图"),
)

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=6*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/plain,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def ia_url(q):
    p=[
      ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
      ("fl[]","description"),("fl[]","creator"),("fl[]","mediatype"),
      ("rows","50"),("page","1"),("output","json")
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(q):
    p=[
      ("q",q),("qfields","name"),("mode","deep"),("limit","100"),
      ("outputAs","json"),("showItemName","showItemName")
    ]
    return DISCM+"?"+urllib.parse.urlencode(p)

def walk_rows(node):
    out=[]
    def walk(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x):
                out.append(x)
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(node)
    uniq={}
    for r in out:
        path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        uniq[(str(r.get("itemid") or ""),path,str(r.get("b3sum") or ""))]=r
    return tuple(uniq.values())

def main():
    print("StoneAge 2.0 named coverdisc carrier census — R1")
    print("SCOPE|17173-listed carrier identities + Internet Archive metadata + DiscMaster name index|metadata-only|no-payload")
    errors=[];ia_hits=[];dm_hits=[]
    for key,term in CARRIERS:
        # IA search deliberately keeps terms unfielded because historical Chinese
        # item metadata is inconsistent across title/description/collection fields.
        try:
            st,final,h,b=fetch(ia_url(term),timeout=35)
            obj=json.loads(b.decode("utf-8")); docs=((obj.get("response") or {}).get("docs") or [])
            print(f"IA|key={key}|term={clean(term)}|status={st}|items={len(docs)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for d in docs[:50]:
                ia_hits.append((key,d))
                print(
                    f"IA_HIT|key={key}|identifier={clean(d.get('identifier'))}|title={clean(d.get('title'))}|"
                    f"date={clean(d.get('date'))}|creator={clean(d.get('creator'))}|"
                    f"mediatype={clean(d.get('mediatype'))}|description={clean(d.get('description'))}"
                )
        except Exception as e:
            errors.append((f"ia:{key}",type(e).__name__,str(e)))
        try:
            st,final,h,b=fetch(discm_url(term),timeout=35)
            obj=json.loads(b.decode("utf-8")); rows=walk_rows(obj)
            print(f"DISCM|key={key}|term={clean(term)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rows[:100]:
                dm_hits.append((key,r))
                path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
                print(
                    f"DISCM_HIT|key={key}|itemid={clean(r.get('itemid'))}|itemName={clean(r.get('itemName'))}|"
                    f"path={clean(path)}|size={clean(r.get('size'))}|ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}"
                )
        except Exception as e:
            errors.append((f"discm:{key}",type(e).__name__,str(e)))
    print(f"COUNT|carriers|{len(CARRIERS)}")
    print(f"COUNT|ia_rows|{len(ia_hits)}")
    print(f"COUNT|discm_rows|{len(dm_hits)}")
    for s,k,m in errors[:200]:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if ia_hits or dm_hits:
        print("RESOLUTION|CARRIER_INDEX_CANDIDATES_FOUND|manually classify candidates before any filesystem or payload read")
    else:
        print("RESOLUTION|NO_CARRIER_INDEX_CANDIDATE|named carrier strings expose no public preservation row on tested indexes")
    print("EVIDENCE_BOUNDARY|name-index hits identify candidate carriers only; StoneAge 2.0 content requires filesystem/file-level verification.")

if __name__=="__main__":
    main()
