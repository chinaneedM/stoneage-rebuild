#!/usr/bin/env python3
"""Search preservation indexes for exact Mainland StoneAge 2.0 retail client-disc carriers.

Period product evidence identifies both 石器时代2.0新手报到包 and
石器时代2.0老手削暴包 as packages containing a StoneAge 2.0 client CD.
This metadata-only probe searches exact carrier names, client-disc wording and
the Sina-labelled setup filename across Internet Archive and DiscMaster.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DM="https://discmaster.textfiles.com/search"

TOKENS=(
 "石器时代2.0新手报到包",
 "石器时代2.0老手削暴包",
 "新手报到包",
 "老手削暴包",
 "石器时代2.0客户端光盘",
 "stoneage2.0setup.exe",
 "stoneage2.0setup",
)
IA_QUERIES=(
 ("newbie-exact",'("石器时代2.0新手报到包" OR "石器时代2.0 新手报到包")'),
 ("veteran-exact",'("石器时代2.0老手削暴包" OR "石器时代2.0 老手削暴包")'),
 ("newbie-short",'"新手报到包"'),
 ("veteran-short",'"老手削暴包"'),
 ("client-disc",'("石器时代2.0" AND "客户端光盘")'),
 ("sina-filename",'"stoneage2.0setup.exe"'),
 ("sina-stem",'"stoneage2.0setup"'),
)
DM_QUERIES=(
 "石器时代2.0新手报到包",
 "石器时代2.0老手削暴包",
 "新手报到包",
 "老手削暴包",
 "石器时代2.0",
 "stoneage2.0setup.exe",
 "stoneage2.0setup",
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def norm(v):
    return urllib.parse.unquote_plus(str(v or "")).lower().replace(" ","")

def strict_text(v):
    s=norm(v)
    return any(norm(t) in s for t in TOKENS)

def fetch(url,timeout=45,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def ia_url(q,rows=300):
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

def dm_url(q,limit=500):
    p=[("q",q),("qfields","name"),("mode","deep"),("limit",str(limit)),("outputAs","json"),("showItemName","showItemName")]
    return DM+"?"+urllib.parse.urlencode(p)

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
        p=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        uniq[(str(r.get("itemid") or ""),p,str(r.get("b3sum") or ""))]=r
    return tuple(uniq.values())

def dm_path(r):
    return str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")

def main():
    print("StoneAge 2.0 retail client-disc preservation census — R1")
    print("SCOPE|Internet Archive metadata + DiscMaster filename index|exact retail carrier/client tokens|no-payload")
    print("TARGET|newbie=石器时代2.0新手报到包|veteran=石器时代2.0老手削暴包|sina=stoneage2.0setup.exe")
    errors=[];ia_seen={};dm_seen={}
    for label,q in IA_QUERIES:
        try:
            st,final,h,b=fetch(ia_url(q))
            rr=ia_docs(b)
            print(f"IA_QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|q={clean(q)}")
            for d in rr:
                ident=str(d.get("identifier") or "")
                text=" ".join(str(d.get(k) or "") for k in ("identifier","title","description"))
                strict=int(strict_text(text))
                ia_seen[ident]=d
                print(
                  f"IA_HIT|label={label}|strict={strict}|identifier={clean(ident)}|title={clean(d.get('title'))}|"
                  f"date={clean(d.get('date'))}|year={clean(d.get('year'))}|creator={clean(d.get('creator'))}|"
                  f"uploader={clean(d.get('uploader'))}|collection={clean(d.get('collection'))}|"
                  f"mediatype={clean(d.get('mediatype'))}|description={clean(d.get('description'),1200)}"
                )
        except Exception as e:
            errors.append(("ia:"+label,type(e).__name__,str(e)))
    for q in DM_QUERIES:
        try:
            st,final,h,b=fetch(dm_url(q))
            rr=dm_rows(json.loads(b.decode("utf-8")))
            print(f"DM_QUERY|q={clean(q)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rr:
                p=dm_path(r)
                text=str(r.get("itemName") or "")+" "+p
                strict=int(strict_text(text))
                key=(str(r.get("itemid") or ""),p,str(r.get("b3sum") or ""))
                dm_seen[key]=r
                print(
                  f"DM_HIT|q={clean(q)}|strict={strict}|itemid={clean(r.get('itemid'))}|"
                  f"itemName={clean(r.get('itemName'))}|path={clean(p)}|size={clean(r.get('size'))}|"
                  f"ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}"
                )
        except Exception as e:
            errors.append(("dm:"+q,type(e).__name__,str(e)))
    ia_strict=[
      d for d in ia_seen.values()
      if strict_text(" ".join(str(d.get(k) or "") for k in ("identifier","title","description")))
    ]
    dm_strict=[
      r for r in dm_seen.values()
      if strict_text(str(r.get("itemName") or "")+" "+dm_path(r))
    ]
    print(f"COUNT|ia_unique_items|{len(ia_seen)}")
    print(f"COUNT|ia_strict_items|{len(ia_strict)}")
    print(f"COUNT|dm_unique_rows|{len(dm_seen)}")
    print(f"COUNT|dm_strict_rows|{len(dm_strict)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if ia_strict or dm_strict:
        print("RESOLUTION|STRICT_RETAIL_CARRIER_CANDIDATE_FOUND|inspect exact item/filesystem before any payload or clean-client promotion")
    else:
        print("RESOLUTION|NO_STRICT_RETAIL_CARRIER_HIT|tested IA/DiscMaster exact retail/client token surface exposes no preserved client-disc candidate")
    print("EVIDENCE_BOUNDARY|index metadata is discovery evidence only; package-name matches do not establish optical pressing or client-byte identity.")

if __name__=="__main__":
    main()
