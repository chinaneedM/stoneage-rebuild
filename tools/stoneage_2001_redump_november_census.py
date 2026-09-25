#!/usr/bin/env python3
"""Search IA preservation collections for November-2001 software/coverdisc items.

The Popsoft namespace stops in 1998, but those items belong mainly to the
redump/softwarecapsules collections. This metadata-only census looks for
2001.11/2001-11 title and identifier patterns inside those same collections,
then emits candidate item metadata for manual carrier classification.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
QUERIES=(
 ("redump-title-dot",'collection:redump AND mediatype:software AND title:"2001.11"'),
 ("redump-title-dash",'collection:redump AND mediatype:software AND title:"2001-11"'),
 ("redump-id",'collection:redump AND mediatype:software AND identifier:*2001*11*'),
 ("capsules-title-dot",'collection:softwarecapsules AND mediatype:software AND title:"2001.11"'),
 ("capsules-title-dash",'collection:softwarecapsules AND mediatype:software AND title:"2001-11"'),
 ("capsules-id",'collection:softwarecapsules AND mediatype:software AND identifier:*2001*11*'),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=30,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def ia_url(q):
    p=[
      ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
      ("fl[]","year"),("fl[]","creator"),("fl[]","uploader"),
      ("fl[]","collection"),("fl[]","mediatype"),("fl[]","description"),
      ("rows","500"),("page","1"),("output","json"),
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def docs(body):
    obj=json.loads(body.decode("utf-8"))
    return tuple(((obj.get("response") or {}).get("docs") or []))

def main():
    print("StoneAge 2.0 November-2001 preservation-collection census — R1")
    print("SCOPE|IA redump/softwarecapsules month-pattern metadata search|no-payload")
    errors=[];seen={}
    for label,q in QUERIES:
        try:
            st,final,h,b=fetch(ia_url(q))
            rr=docs(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|q={clean(q)}")
            for d in rr:
                ident=str(d.get("identifier") or "")
                seen[ident]=d
                print(
                  f"HIT|label={label}|identifier={clean(ident)}|title={clean(d.get('title'))}|"
                  f"date={clean(d.get('date'))}|year={clean(d.get('year'))}|creator={clean(d.get('creator'))}|"
                  f"uploader={clean(d.get('uploader'))}|collection={clean(d.get('collection'))}|"
                  f"mediatype={clean(d.get('mediatype'))}|description={clean(d.get('description'),1000)}"
                )
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    print(f"COUNT|unique_items|{len(seen)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if seen:
        print("RESOLUTION|NOVEMBER_2001_COLLECTION_ITEMS_FOUND|classify candidates against the 13 named StoneAge 2.0 carriers")
    else:
        print("RESOLUTION|NO_NOVEMBER_2001_COLLECTION_ITEM|tested redump/softwarecapsules month patterns expose no candidate item")
    print("EVIDENCE_BOUNDARY|month-pattern collection hits are carrier-discovery metadata only; StoneAge content requires item/file-level verification.")

if __name__=="__main__":
    main()
