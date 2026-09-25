#!/usr/bin/env python3
"""Search the historical Sina download IP for target filename/path aliases.

Scope is intentionally bounded to 202.106.184.193/downfiles/ and metadata only.
Server-side CDX filters look for samap, 1220, StoneAge, and the exact target stem
across alternate directories/canonicalizations.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
HOSTROOT="http://202.106.184.193/downfiles/"
TARGET="samap_1220.zip"
CDX="https://web.archive.org/cdx/search/cdx"
FILTERS=(
    ("exact-stem",r".*samap_1220.*"),
    ("samap",r".*samap.*"),
    ("1220",r".*1220.*"),
    ("stoneage",r".*stoneage.*"),
)

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=60,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cdx_url(pattern,start,end):
    p=[
        ("url",HOSTROOT),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",start),("to",end),("filter",f"original:{pattern}"),
        ("collapse","urlkey"),("limit","20000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def relevant(rows):
    out=[]
    for r in rows:
        u=urllib.parse.unquote_plus(str(r.get("original") or "")).lower()
        if any(k in u for k in ("samap","stoneage","1220")):
            out.append(r)
    return tuple(out)

def main():
    print("StoneAge 2000 Sina host-wide filename probe — R1")
    print("SCOPE|202.106.184.193/downfiles prefix + server-side filename filters|metadata-only")
    print(f"TARGET|filename={TARGET}|hostroot={HOSTROOT}")
    errors=[];allhits=[]
    for label,pat in FILTERS:
        for window,start,end in (("2000-2001","2000","2001"),("2002-2003","2002","2003"),("2004-2006","2004","2006")):
            try:
                st,final,h,b=fetch(cdx_url(pat,start,end),timeout=70)
                rows=parse_cdx(b);rr=relevant(rows);allhits.extend(rr)
                print(f"CDX|label={label}|window={window}|status={st}|rows={len(rows)}|relevant={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
                for r in rr:
                    print(f"ROW|label={label}|window={window}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
            except Exception as e:
                errors.append((f"{label}:{window}",type(e).__name__,str(e)))
    uniq={}
    for r in allhits:
        key=str(r.get("original") or "").lower()
        uniq[key]=r
    print(f"COUNT|unique_relevant_urls|{len(uniq)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    exact=[r for r in uniq.values() if "samap_1220" in urllib.parse.unquote_plus(str(r.get("original") or "")).lower()]
    if exact:
        print("RESOLUTION|HOSTWIDE_TARGET_ALIAS_FOUND|verify the exact archived object and compare route provenance")
    elif uniq:
        print("RESOLUTION|HOSTWIDE_RELATED_URLS_FOUND|use related URLs only as directory/mirror topology evidence")
    else:
        print("RESOLUTION|NO_HOSTWIDE_FILENAME_ALIAS|move to independent mirrors/caches keyed by exact direct URL and filename")
    print("EVIDENCE_BOUNDARY|host-wide filename rows are discovery metadata; only exact recovered bytes can establish target package identity.")

if __name__=="__main__":
    main()
