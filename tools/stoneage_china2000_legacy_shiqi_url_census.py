#!/usr/bin/env python3
"""Census the legacy China.com StoneAge special-site URL tree.

Why:
- contemporaneous China.com pages link a /zh_cn/hotspot/shiqi/ StoneAge topic;
- surviving old China.com pages are also visible under /hotspot/shiqi/... without
  the /zh_cn prefix;
- prior project work tested only a few guessed legacy pages, not the complete
  legacy prefix.

This probe enumerates archive URL metadata only for the source-derived legacy
prefix during the launch/early-operation window. It does not replay page bodies
or fetch payloads.
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
TO="20010331"
TARGETS=(
    ("game","http://game.china.com/hotspot/shiqi/"),
    ("game80","http://game.china.com:80/hotspot/shiqi/"),
)
TOKENS=(
    "download","down","client","setup","install","trial","test","demo",
    "shiwan","ceshi","reg","register","list","name","winner","give","gift",
    "mail","order","news","active","activity","huodong","download",
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=55,max_bytes=16*1024*1024):
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

def cdx_url(prefix):
    q=[
        ("url",prefix),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("limit","30000"),("collapse","urlkey"),
    ]
    return CDX+"?"+urllib.parse.urlencode(q)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))

def norm_path(url):
    try:
        return urllib.parse.unquote_plus(urllib.parse.urlsplit(url).path).lower()
    except Exception:
        return str(url).lower()

def score(url):
    low=urllib.parse.unquote_plus(str(url).lower())
    path=norm_path(url)
    s=0
    hit=[]
    for token in TOKENS:
        if token in low:
            hit.append(token)
            s+=4
    if path.endswith((".exe",".zip",".rar",".cab",".msi",".arj",".lzh",".7z")):
        s+=20; hit.append("payload-ext")
    if any(x in path for x in ("/news/","/active/","/activity/","/download/","/down/")):
        s+=5
    if re.search(r"(?:^|[/_-])(test|trial|demo)(?:[/_.-]|$)",path):
        s+=8
    return s,tuple(dict.fromkeys(hit))

def main():
    print("StoneAge China.com legacy /hotspot/shiqi/ URL census — R1")
    print(f"SCOPE|Wayback CDX metadata only|prefix=/hotspot/shiqi/|window={FROM}..{TO}|collapse=urlkey|no replay|no payload")
    errors=[];allrows={}

    for label,prefix in TARGETS:
        try:
            st,final,b=fetch(cdx_url(prefix))
            rr=rows(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                key=(str(r.get("original") or ""),str(r.get("digest") or ""))
                allrows[key]=r
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))

    ranked=[]
    mime_counts={}
    ext_counts={}
    for (orig,digest),r in allrows.items():
        sc,hits=score(orig)
        ranked.append((sc,orig,digest,r,hits))
        mt=str(r.get("mimetype") or "")
        mime_counts[mt]=mime_counts.get(mt,0)+1
        ext=norm_path(orig).rsplit("/",1)[-1]
        ext=("."+ext.rsplit(".",1)[-1]) if "." in ext else "(none)"
        ext_counts[ext]=ext_counts.get(ext,0)+1

    ranked.sort(key=lambda x:(-x[0],x[1]))
    print(f"COUNT|unique_rows|{len(allrows)}")
    print(f"COUNT|positive_score_rows|{sum(1 for x in ranked if x[0]>0)}")
    for mt,n in sorted(mime_counts.items(),key=lambda kv:(-kv[1],kv[0]))[:30]:
        print(f"MIME|count={n}|value={clean(mt)}")
    for ext,n in sorted(ext_counts.items(),key=lambda kv:(-kv[1],kv[0]))[:40]:
        print(f"EXT|count={n}|value={clean(ext)}")

    for sc,orig,digest,r,hits in ranked[:500]:
        if sc<=0:
            break
        print(
            f"RANKED|score={sc}|tokens={','.join(hits)}|timestamp={clean(r.get('timestamp'))}|"
            f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
            f"digest={clean(digest)}|original={clean(orig)}"
        )

    # Also emit a bounded alphabetical URL inventory when census is tractable.
    if len(allrows)<=2500:
        for orig,digest in sorted(allrows):
            r=allrows[(orig,digest)]
            print(
                f"URL|timestamp={clean(r.get('timestamp'))}|status={clean(r.get('statuscode'))}|"
                f"mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|original={clean(orig)}"
            )

    for label,kind,msg in errors:
        print(f"ERROR|scope={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if allrows:
        print("RESOLUTION|LEGACY_SHIQI_URL_TREE_RECOVERED|classify ranked paths and replay only source-derived high-value pages")
    elif errors:
        print("RESOLUTION|LEGACY_SHIQI_PREFIX_PARTIAL|retry failed exact prefix surfaces")
    else:
        print("RESOLUTION|LEGACY_SHIQI_PREFIX_UNINDEXED|do not infer missing site structure")
    print("EVIDENCE_BOUNDARY|CDX URL metadata establishes archived topology only; path vocabulary does not prove page meaning or payload identity.")

if __name__=="__main__":
    main()
