#!/usr/bin/env python3
"""Fast metadata-only census of Waei's historical central download center.

This intentionally does NOT replay archived HTML and does NOT fetch game binaries.
It enumerates Wayback CDX URL metadata for the Waei download namespace so later
probes can target a small set of exact detail IDs / filenames instead of timing
out while replaying hundreds of pages.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"
TO="20010630"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"
TARGETS=(
    ("download-prefix","http://www7.waei.net/download/","prefix"),
    ("detail-prefix","http://www7.waei.net/download/dldetial.asp","prefix"),
    ("file-prefix","http://www7.waei.net/download/file/","prefix"),
    ("list-prefix","http://www7.waei.net/download/dllist.asp","prefix"),
)
BINARY_EXTS=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z",".iso",".bin",".cue")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=75,max_bytes=16*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(url,match):
    params=[
        ("url",url),("matchType",match),("output","json"),("fl",FIELDS),
        ("from",FROM),("to",TO),("filter","statuscode:200"),
        ("limit","30000"),("collapse","urlkey"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,row)) for row in obj[1:] if isinstance(row,list))

def low(v):
    return urllib.parse.unquote_plus(str(v or "")).lower()

def is_binary(url):
    return urllib.parse.urlsplit(low(url)).path.endswith(BINARY_EXTS)

def detail_id(url):
    q=urllib.parse.parse_qs(urllib.parse.urlsplit(str(url or "")).query)
    vals=q.get("ID") or q.get("id") or ()
    if vals and str(vals[0]).isdigit():
        return str(vals[0])
    m=re.search(r"(?:[?&](?:id|ID)=)(\d+)",str(url or ""))
    return m.group(1) if m else ""

def xpage(url):
    q=urllib.parse.parse_qs(urllib.parse.urlsplit(str(url or "")).query)
    vals=q.get("xPage") or q.get("xpage") or ()
    return str(vals[0]) if vals else ""

def basename(url):
    p=urllib.parse.unquote(urllib.parse.urlsplit(str(url or "")).path)
    return p.rsplit("/",1)[-1]

def classify(url):
    l=low(url)
    if "/download/file/" in l:
        return "file"
    if "dldetial.asp" in l:
        return "detail"
    if "dllist.asp" in l:
        return "list"
    if is_binary(url):
        return "binary-other"
    return "other"

def main():
    print("StoneAge Waei central-download metadata census — R1")
    print(f"SCOPE|Wayback CDX metadata only|window={FROM}..{TO}|no archived-body|no binary payload")
    all_rows={}
    errors=[]
    for label,url,match in TARGETS:
        try:
            st,final,b=fetch(cdx_url(url,match))
            rows=parse(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rows:
                orig=str(r.get("original") or "")
                key=(orig,str(r.get("timestamp") or ""))
                all_rows[key]=r
        except Exception as exc:
            errors.append((label,type(exc).__name__,str(exc)))

    rows=sorted(all_rows.values(),key=lambda r:(str(r.get("timestamp") or ""),str(r.get("original") or "")))
    ids=set()
    binaries=[]
    details=[]
    files=[]
    lists=[]
    for r in rows:
        orig=str(r.get("original") or "")
        kind=classify(orig)
        did=detail_id(orig)
        xp=xpage(orig)
        if did: ids.add(int(did))
        if is_binary(orig): binaries.append(r)
        if kind=="detail": details.append(r)
        elif kind=="file": files.append(r)
        elif kind=="list": lists.append(r)
        print("ROW|timestamp={}|kind={}|id={}|xpage={}|basename={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
            clean(r.get("timestamp")),kind,clean(did),clean(xp),clean(basename(orig),1000),
            clean(r.get("statuscode")),clean(r.get("mimetype")),clean(r.get("length")),
            clean(r.get("digest")),clean(r.get("redirect")),clean(orig)
        ))

    print(f"COUNT|unique_rows|{len(rows)}")
    print(f"COUNT|detail_rows|{len(details)}")
    print(f"COUNT|file_rows|{len(files)}")
    print(f"COUNT|list_rows|{len(lists)}")
    print(f"COUNT|binary_rows|{len(binaries)}")
    print(f"COUNT|detail_ids|{len(ids)}")
    if ids:
        s=sorted(ids)
        print("DETAIL_IDS|"+",".join(map(str,s)))
        print(f"DETAIL_ID_RANGE|{s[0]}|{s[-1]}")
    for label,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if binaries or files:
        print("RESOLUTION|DOWNLOAD_FILE_NAMESPACE_FOUND|classify exact filenames/IDs next")
    elif ids:
        print("RESOLUTION|DETAIL_ID_NAMESPACE_FOUND|replay only exact detail IDs next")
    elif rows:
        print("RESOLUTION|DOWNLOAD_NAMESPACE_FOUND_NO_DETAIL_IDS|inspect URL topology next")
    elif errors:
        print("RESOLUTION|PARTIAL_CDX_CENSUS|retry failed metadata query only")
    else:
        print("RESOLUTION|NO_CDX_ROWS|current tested Waei download namespace has no indexed rows in window")
    print("EVIDENCE_BOUNDARY|CDX URL metadata establishes archive topology only; it does not authenticate StoneAge payload bytes.")

if __name__=="__main__":
    main()
