#!/usr/bin/env python3
"""Map the Wayback crawl-time neighborhood around 21CN sa25up.jpg (2002-05-17).

Metadata only. The goal is to identify list.php/downit.php records captured near the
same crawl timestamp as the archived sa25up.jpg sidecar, without replaying or
downloading any historical software payload.
"""
from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
HOSTS=("http://download.21cn.com/","http://202.104.32.168/")
FROM="20020517230000"
TO="20020518010000"
IMAGE_TS="20020517235842"
IMAGE_PATH="/file/game/maoxian/sa25up.jpg"

def clean(v,limit=1800):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]

def fetch(url,timeout=40):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(prefix):
    p=[
        ("url",prefix),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("limit","10000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    h=data[0]
    return tuple(dict(zip(h,row)) for row in data[1:] if isinstance(row,list))

def ms_distance(ts):
    # Timestamp precision is seconds; absolute decimal difference is sufficient
    # inside this fixed two-hour window for ordering, not elapsed-time math.
    try: return abs(int(ts)-int(IMAGE_TS))
    except Exception: return 10**20

def classify(url):
    p=urllib.parse.urlsplit(url)
    path=p.path.lower()
    if path=="/list.php": return "list"
    if path=="/downit.php": return "downit"
    if path.startswith("/file/game/"): return "game-file"
    if path=="/second.php": return "category"
    return "other"

def main():
    print("StoneAge 2.5 21CN sa25up crawl-neighborhood probe — R1")
    print("SCOPE|wayback-cdx-crawl-window|metadata-only|no-replay|no-software-payload")
    print(f"WINDOW|from={FROM}|to={TO}|anchor={IMAGE_TS}|image={IMAGE_PATH}")
    errors=[]; allrows={}
    for prefix in HOSTS:
        try:
            st,final,b=fetch(cdx_url(prefix))
            rows=parse(b)
            print(f"CDX|prefix={clean(prefix)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|final={clean(final)}")
            for row in rows:
                key=(str(row.get("timestamp") or ""),str(row.get("original") or ""))
                allrows[key]=row
        except Exception as e:
            errors.append((prefix,type(e).__name__,str(e)))
    rows=sorted(allrows.values(),key=lambda r:(ms_distance(str(r.get("timestamp") or "")),str(r.get("timestamp") or ""),str(r.get("original") or "")))
    counts={}
    for r in rows:
        k=classify(str(r.get("original") or ""))
        counts[k]=counts.get(k,0)+1
    for k,n in sorted(counts.items()):
        print(f"CLASS_COUNT|class={k}|count={n}")
    focused=[r for r in rows if classify(str(r.get("original") or "")) in ("list","downit","game-file","category")]
    for n,r in enumerate(focused[:1000],1):
        original=str(r.get("original") or "")
        print(
            f"NEAR|order={n}|class={classify(original)}|distance_key={ms_distance(str(r.get('timestamp') or ''))}|"
            f"timestamp={clean(r.get('timestamp'))}|original={clean(original)}|status={clean(r.get('statuscode'))}|"
            f"mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
        )
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|unique_rows|{len(rows)}")
    print(f"COUNT|focused_rows|{len(focused)}")
    print(f"COUNT|errors|{len(errors)}")
    if focused:
        print("RESOLUTION|CRAWL_NEIGHBORHOOD_MAPPED|use nearest list/downit records as candidates only, then require page/path evidence")
    elif errors:
        print("RESOLUTION|PARTIAL_CRAWL_NEIGHBORHOOD_FAILURE|retry failed host only")
    else:
        print("RESOLUTION|NO_CRAWL_NEIGHBORHOOD_SIGNAL|bounded two-hour CDX window empty")
    print("EVIDENCE_BOUNDARY|crawl-time proximity is a discovery heuristic, not proof that a list/downit record references sa25up.jpg or sa25up.zip.")

if __name__=="__main__":
    main()
