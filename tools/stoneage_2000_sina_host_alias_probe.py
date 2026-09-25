#!/usr/bin/env python3
"""Probe historical Sina download CGI host aliases for the 2000 StoneAge map token.

Surviving 2000 Sina StoneAge pages use both games.sina.com.cn and
games1.sina.com.cn for the same /cgi-bin/games/downgames/download.pl route.
This metadata-only probe checks both aliases without downloading payloads.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
HOSTS=("games.sina.com.cn","games1.sina.com.cn")
PATH="/cgi-bin/games/downgames/download.pl"
TARGET_AID="23223"
TARGET_FILENAME="samap_1220.zip"
TARGET_QUERY="col=map&aid=23223&filename=samap_1220.zip&size=1410"
WINDOWS=(("2000","20000101","20001231"),("2001","20010101","20011231"),("2002","20020101","20021231"))

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=55,max_bytes=5*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def cdx_url(base,start,end,match="prefix"):
    p=[("url",base),("matchType",match),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from",start),("to",end),("limit","10000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def params(url):
    try:return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(str(url)).query,keep_blank_values=True))
    except Exception:return {}

def relevant(row):
    p=params(row.get("original") or "")
    return str(p.get("aid") or "")==TARGET_AID or str(p.get("filename") or "").lower()==TARGET_FILENAME.lower()

def availability(url,date):
    q=AVAIL+"?"+urllib.parse.urlencode({"url":url,"timestamp":date})
    st,final,h,b=fetch(q,timeout=25,max_bytes=512*1024)
    d=json.loads(b.decode("utf-8"));c=(d.get("archived_snapshots") or {}).get("closest") or {}
    return st,c

def main():
    print("StoneAge 2000 Sina download-host alias probe — R1")
    print("SCOPE|games + games1 download.pl aliases|Wayback metadata-only|no-payload")
    print(f"TARGET|aid={TARGET_AID}|filename={TARGET_FILENAME}")
    errors=[];hits=[]
    for host in HOSTS:
        base=f"http://{host}{PATH}"
        for label,start,end in WINDOWS:
            try:
                st,final,h,b=fetch(cdx_url(base,start,end),timeout=60)
                rows=parse_cdx(b);rr=[r for r in rows if relevant(r)]
                maprows=[r for r in rows if str(params(r.get("original") or "").get("col") or "").lower()=="map"]
                print(f"CDX|host={host}|window={label}|status={st}|rows={len(rows)}|map_rows={len(maprows)}|relevant={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
                for r in rr:
                    hits.append((host,r))
                    print(f"HIT|host={host}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
            except Exception as e:
                errors.append((f"cdx:{host}:{label}",type(e).__name__,str(e)))
        target=f"{base}?{TARGET_QUERY}"
        for date in ("20001220","20010124","20011220","20020101"):
            try:
                st,c=availability(target,date)
                print(f"AVAIL|host={host}|date={date}|status={st}|hit={int(bool(c.get('available')))}|timestamp={clean(c.get('timestamp'))}|capture={clean(c.get('url'))}|http_status={clean(c.get('status'))}")
            except Exception as e:
                errors.append((f"avail:{host}:{date}",type(e).__name__,str(e)))
    print(f"COUNT|relevant_hits|{len(hits)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|HOST_ALIAS_TARGET_ROW_FOUND|replay only the exact historical response before considering payload recovery")
    else:
        print("RESOLUTION|NO_TARGET_ROW_ON_TESTED_HOST_ALIASES|games/games1 aliases bounded on tested Wayback prefix surfaces")
    print("EVIDENCE_BOUNDARY|host-alias rows are route evidence only; payload identity still requires recovered bytes.")

if __name__=="__main__":
    main()
