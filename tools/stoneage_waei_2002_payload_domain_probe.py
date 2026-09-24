#!/usr/bin/env python3
"""Probe archived Waei-domain payload filenames during the StoneAge 2.5 rollout.

Official Feb-2002 StoneAge2 pages visibly use Waei subdomains, including
product.waei.com.cn. The client upgrade landing page itself may be uncaptured,
so this probe searches the whole waei.com.cn domain family at CDX metadata
level for archived EXE/ZIP/CAB/RAR URLs in Jan-Mar 2002. No payload is fetched.
"""

from __future__ import annotations
import concurrent.futures, hashlib, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
DOMAIN="waei.com.cn"
WINDOWS=(("jan","20020101","20020131"),("feb","20020201","20020228"),("mar","20020301","20020331"))
EXTENSIONS=("exe","zip","cab","rar")
PROJECT_HINTS=("stoneage","stone_age","stone-age","sa25","sa2.5","2.5","jlw","jingling","spirit")
NOISE_HINTS=("qqskin","passwordtable","record.zip","bonus.zip","series-pwd","rwmcxgxys","/stoneage2/stpic/flash/")

def clean(v,limit=2500):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=50):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(start,end,ext):
    # Regex is intentionally suffix-like but allows historical query strings.
    flt=rf"original:.*[.]{ext}(?:[?].*)?$"
    p=[
        ("url",DOMAIN),("matchType","domain"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from",start),("to",end),("collapse","urlkey"),("limit","5000"),
        ("filter",flt),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(body):
    d=json.loads(body.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def score(row):
    url=urllib.parse.unquote_plus(str(row.get("original") or "")).lower()
    mime=str(row.get("mimetype") or "").lower()
    try: length=int(str(row.get("length") or "0"))
    except: length=0
    s=0
    if any(h in url for h in PROJECT_HINTS): s+=12
    if "/stoneage" in url or "/stone/" in url: s+=10
    if "setup" in url or "update" in url or "upgrade" in url or "patch" in url or "client" in url: s+=6
    if any(x in mime for x in ("octet-stream","x-msdownload","zip","compressed")): s+=2
    if 7_000_000 <= length <= 11_000_000: s+=4
    if length >= 100_000_000: s+=3
    if any(n in url for n in NOISE_HINTS): s-=20
    return s

def one(args):
    label,start,end,ext=args
    u=cdx_url(start,end,ext)
    st,final,body=fetch(u)
    return label,start,end,ext,u,st,final,body,parse(body)

def main():
    print("StoneAge Waei-domain Jan-Mar 2002 payload-index probe — R1")
    print("SCOPE|waei.com.cn-domain-family|EXE+ZIP+CAB+RAR|2002-Q1|CDX-metadata-only|no-payload")
    tasks=[(label,start,end,ext) for label,start,end in WINDOWS for ext in EXTENSIONS]
    errors=[]; results=[]; rows={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs={ex.submit(one,t):t for t in tasks}
        for fut in concurrent.futures.as_completed(futs):
            t=futs[fut]
            try: results.append(fut.result())
            except Exception as exc: errors.append((f"{t[0]}:{t[3]}",type(exc).__name__,str(exc)))
    for label,start,end,ext,u,st,final,body,found in sorted(results):
        print(f"CDX|window={label}|ext={ext}|from={start}|to={end}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(found)}|final={clean(final)}")
        for row in found:
            key=(str(row.get("timestamp") or ""),str(row.get("original") or ""),str(row.get("statuscode") or ""))
            rows[key]=row
    ranked=sorted(rows.values(),key=lambda r:(-score(r),str(r.get("original") or "")))
    relevant=[r for r in ranked if score(r)>0]
    strong=[r for r in ranked if score(r)>=10]
    for row in relevant[:500]:
        print(f"CANDIDATE|score={score(row)}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|length={clean(row.get('length'))}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|queries|{len(tasks)}")
    print(f"COUNT|completed_queries|{len(results)}")
    print(f"COUNT|unique_payload_urls|{len(rows)}")
    print(f"COUNT|relevant_candidates|{len(relevant)}")
    print(f"COUNT|strong_candidates|{len(strong)}")
    print(f"COUNT|errors|{len(errors)}")
    if strong:
        print("RESOLUTION|WAEI_2002_STRONG_PAYLOAD_CANDIDATES_FOUND|classify StoneAge identity and archival bytes before recovery")
    elif relevant:
        print("RESOLUTION|WAEI_2002_PAYLOAD_CANDIDATES_FOUND|inspect candidate semantics before recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|one or more Waei domain payload index slices failed")
    else:
        print("RESOLUTION|NO_WAEI_2002_PAYLOAD_HIT|tested Waei-domain payload URL surface has no relevant candidate")

if __name__=="__main__": main()
