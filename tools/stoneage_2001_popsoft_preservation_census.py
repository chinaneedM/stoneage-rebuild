#!/usr/bin/env python3
"""Enumerate Internet Archive's Popsoft CD preservation namespace.

The refined StoneAge 2.0 carrier census found preserved 大众软件CD objects with
identifiers such as popsoftcd-1998-11. This probe enumerates popsoftcd-* item
metadata, tests the expected 2001-11 identifiers, and—only if an item exists—
reads its metadata file list for StoneAge/client-looking names. It never
downloads disc images or payload files.
"""
from __future__ import annotations
import collections, hashlib, json, re, urllib.error, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
IA_SEARCH="https://archive.org/advancedsearch.php"
IA_META="https://archive.org/metadata/"
TARGET_IDS=(
    "popsoftcd-2001-11",
    "popsoftcd-2001-11-alt",
    "popsoftcd-2001-11-a",
    "popsoftcd-2001-11-b",
    "popsoftcd-2001-11-1",
    "popsoftcd-2001-11-2",
)
FILE_TERMS=("stoneage","stone_age","stone-age","shiqi","waei","石器","sa20","sa2.0","2.0setup")

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=12*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/plain,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            b=r.read(max_bytes+1)
            return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
    except urllib.error.HTTPError as e:
        return int(e.code),e.geturl(),dict(e.headers.items()),e.read(max_bytes+1)

def search_url():
    p=[
      ("q","identifier:popsoftcd-*"),
      ("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("fl[]","year"),
      ("fl[]","creator"),("fl[]","uploader"),("fl[]","collection"),("fl[]","mediatype"),
      ("rows","1000"),("page","1"),("output","json"),
      ("sort[]","identifier asc"),
    ]
    return IA_SEARCH+"?"+urllib.parse.urlencode(p)

def parse_docs(body):
    obj=json.loads(body.decode("utf-8"))
    return tuple(((obj.get("response") or {}).get("docs") or []))

def parse_year_month(identifier):
    m=re.fullmatch(r"popsoftcd-(\d{4})(?:-(\d{1,2}))?(?:-.+)?",str(identifier).lower())
    if not m:return None,None
    return int(m.group(1)),int(m.group(2)) if m.group(2) else None

def metadata_exists(obj,identifier):
    if not isinstance(obj,dict):return False
    meta=obj.get("metadata")
    if not isinstance(meta,dict):return False
    got=str(meta.get("identifier") or obj.get("id") or "")
    return got.lower()==identifier.lower()

def interesting_file(name):
    s=urllib.parse.unquote_plus(str(name or "")).lower()
    return any(t in s for t in FILE_TERMS)

def main():
    print("StoneAge 2.0 Popsoft CD preservation census — R1")
    print("SCOPE|IA popsoftcd namespace + exact 2001-11 identifier metadata + file-list filtering|metadata-only|no-payload")
    errors=[];docs=();target_objects=[]
    try:
        st,final,h,b=fetch(search_url(),timeout=45)
        docs=parse_docs(b)
        print(f"NAMESPACE|status={st}|rows={len(docs)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        counts=collections.Counter()
        for d in docs:
            ident=str(d.get("identifier") or "")
            y,m=parse_year_month(ident)
            if y is not None:counts[y]+=1
            print(
                f"ITEM|identifier={clean(ident)}|year_token={clean(y)}|month_token={clean(m)}|"
                f"title={clean(d.get('title'))}|date={clean(d.get('date'))}|year={clean(d.get('year'))}|"
                f"creator={clean(d.get('creator'))}|uploader={clean(d.get('uploader'))}|"
                f"collection={clean(d.get('collection'))}|mediatype={clean(d.get('mediatype'))}"
            )
        for y in sorted(counts):
            print(f"YEAR_COUNT|year={y}|items={counts[y]}")
    except Exception as e:
        errors.append(("namespace",type(e).__name__,str(e)))

    known={str(d.get("identifier") or "").lower() for d in docs}
    for ident in TARGET_IDS:
        print(f"TARGET_NAMESPACE|identifier={ident}|listed={int(ident.lower() in known)}")
        try:
            st,final,h,b=fetch(IA_META+urllib.parse.quote(ident,safe=""),timeout=35)
            obj=json.loads(b.decode("utf-8")) if b else {}
            exists=metadata_exists(obj,ident)
            files=(obj.get("files") or []) if isinstance(obj,dict) else []
            print(
                f"TARGET_META|identifier={ident}|status={st}|exists={int(exists)}|"
                f"files={len(files) if isinstance(files,list) else 0}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}"
            )
            if exists:
                target_objects.append(ident)
                meta=obj.get("metadata") or {}
                print(
                    f"TARGET_ITEM|identifier={ident}|title={clean(meta.get('title'))}|date={clean(meta.get('date'))}|"
                    f"year={clean(meta.get('year'))}|creator={clean(meta.get('creator'))}|"
                    f"uploader={clean(meta.get('uploader'))}|collection={clean(meta.get('collection'))}"
                )
                for f in files if isinstance(files,list) else []:
                    name=str(f.get("name") or "")
                    if interesting_file(name):
                        print(
                            f"FILE_HIT|identifier={ident}|name={clean(name)}|size={clean(f.get('size'))}|"
                            f"mtime={clean(f.get('mtime'))}|md5={clean(f.get('md5'))}|sha1={clean(f.get('sha1'))}|"
                            f"crc32={clean(f.get('crc32'))}|source={clean(f.get('source'))}|format={clean(f.get('format'))}"
                        )
        except Exception as e:
            errors.append((f"target:{ident}",type(e).__name__,str(e)))

    years=[parse_year_month(d.get("identifier"))[0] for d in docs]
    years=[y for y in years if y is not None]
    print(f"COUNT|namespace_items|{len(docs)}")
    print(f"COUNT|target_objects|{len(target_objects)}")
    print(f"RANGE|min_year={min(years) if years else ''}|max_year={max(years) if years else ''}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if target_objects:
        print("RESOLUTION|POPSOFT_2001_11_ITEM_FOUND|inspect metadata file list and carrier identity before bounded payload work")
    elif any((parse_year_month(d.get("identifier"))[0] or 0)>=2001 for d in docs):
        print("RESOLUTION|NAMESPACE_REACHES_2001_NO_11_TARGET|inspect 2001 neighbors/uploader collections for missing November object")
    else:
        print("RESOLUTION|NAMESPACE_STOPS_BEFORE_2001|preserved popsoftcd series does not currently expose the required 2001-11 carrier")
    print("EVIDENCE_BOUNDARY|identifier/metadata continuity is preservation evidence only; no magazine-disc client identity is established without a matching 2001-11 carrier and file-level verification.")

if __name__=="__main__":
    main()
