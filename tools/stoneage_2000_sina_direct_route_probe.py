#!/usr/bin/env python3
"""Probe the exact direct download route recovered from Sina's archived CGI.

The historical CGI replay exposes:
  http://202.106.184.193/downfiles/map_1212/samap_1220.zip

This stage is metadata-first. It queries archive indexes/availability for the
exact URL and tightly bounded host/path variants. It does not download ZIP
payload bytes.
"""
from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="http://202.106.184.193/downfiles/map_1212/samap_1220.zip"
FILENAME="samap_1220.zip"
HOST="202.106.184.193"
DIR="/downfiles/map_1212/"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
ARQUIVO_VERSION="https://arquivo.pt/wayback/cdx"

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=50,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/plain,text/html,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def parse_cdx(body):
    d=json.loads(body.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):
        return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cdx_url(url,match="exact",start="2000",end="2006"):
    p=[
        ("url",url),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",start),("to",end),("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def availability(url,date):
    q=AVAIL+"?"+urllib.parse.urlencode({"url":url,"timestamp":date})
    st,final,h,b=fetch(q,timeout=30,max_bytes=1024*1024)
    d=json.loads(b.decode("utf-8"))
    c=(d.get("archived_snapshots") or {}).get("closest") or {}
    return st,c if c.get("available") else None

def variants():
    vals=[
        TARGET,
        "http://202.106.184.193:80/downfiles/map_1212/samap_1220.zip",
        "https://202.106.184.193/downfiles/map_1212/samap_1220.zip",
        "http://202.106.184.193/downfiles/map_1212/SAMAP_1220.ZIP",
    ]
    return tuple(dict.fromkeys(vals))

def relevant(rows):
    out=[]
    for r in rows:
        u=urllib.parse.unquote(str(r.get("original") or "")).lower()
        if FILENAME.lower() in u and HOST in u:
            out.append(r)
    return tuple(out)

def main():
    print("StoneAge 2000 Sina direct-route preservation probe — R1")
    print("SCOPE|exact recovered IP path + bounded host-directory archive metadata|no-payload")
    print(f"TARGET|url={TARGET}|filename={FILENAME}")
    errors=[];hits=[]
    for i,u in enumerate(variants(),1):
        for match in ("exact","prefix"):
            try:
                st,final,h,b=fetch(cdx_url(u,match),timeout=55)
                rows=parse_cdx(b); rr=relevant(rows); hits.extend(rr)
                print(f"CDX|variant={i}|match={match}|status={st}|rows={len(rows)}|relevant={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|target={clean(u)}")
                for r in rr:
                    print(f"ROW|variant={i}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
            except Exception as e:
                errors.append((f"cdx:{i}:{match}",type(e).__name__,str(e)))
    # Tight directory-prefix census: useful if the exact URL was canonicalized.
    try:
        droot=f"http://{HOST}{DIR}"
        st,final,h,b=fetch(cdx_url(droot,"prefix"),timeout=60)
        rows=parse_cdx(b); rr=relevant(rows); hits.extend(rr)
        print(f"DIR_CDX|status={st}|rows={len(rows)}|relevant={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|target={droot}")
        for r in rr:
            print(f"DIR_ROW|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
    except Exception as e:
        errors.append(("cdx:directory",type(e).__name__,str(e)))
    for date in ("20001220","20010101","20010126","20011220","20020101","20051103"):
        try:
            st,c=availability(TARGET,date)
            print(f"AVAIL|date={date}|status={st}|hit={int(c is not None)}|timestamp={clean(c.get('timestamp') if c else '')}|capture={clean(c.get('url') if c else '')}|http_status={clean(c.get('status') if c else '')}")
        except Exception as e:
            errors.append((f"avail:{date}",type(e).__name__,str(e)))
    uniq={(str(r.get("timestamp","")),str(r.get("original",""))) for r in hits}
    print(f"COUNT|relevant_unique|{len(uniq)}")
    for s,k,m in errors[:100]:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if uniq:
        print("RESOLUTION|DIRECT_ROUTE_ARCHIVE_HIT|recover only the exact archived object transiently, hash it, and inventory ZIP entries")
    else:
        print("RESOLUTION|NO_DIRECT_ROUTE_ARCHIVE_HIT|retain exact IP/path as primary mirror token and search independent caches/carriers")
    print("EVIDENCE_BOUNDARY|the CGI proves this was the historical Sina download route; archive metadata still does not establish package bytes until an exact object is recovered.")

if __name__=="__main__":
    main()
