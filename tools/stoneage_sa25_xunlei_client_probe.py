#!/usr/bin/env python3
"""Probe preservation metadata for a 2013 StoneAge 2.5 standalone client Xunlei token.

The source post labels the exact kuai.xunlei.com URL as the client download and
also says elize.ini had been modified for LAN use. This is therefore a descendant
client-backup lead, not original-2002 provenance. Metadata only; no payload download.
"""
from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request
from tools.stoneage_sa25_exact_carrier_probe import clean
from tools.stoneage_exact_mirror_arquivopt_cdx_probe import fetch_bytes as arquivo_fetch_bytes, parse_rows as arquivo_parse_rows

UA="stoneage-rebuild-archaeology/1.0"
SOURCE_PAGE="https://www.7chaowan.com/55833.html"
TARGET="http://kuai.xunlei.com/d/DX1fAAJeiQBWT-tR9ee"
WAYBACK="https://web.archive.org/cdx/search/cdx"
AVAILABLE="https://archive.org/wayback/available"
ARQUIVO="https://arquivo.pt/wayback/cdx"
DATES=("20130801","20130823","20131231","20141231")

def get(url,timeout=20,max_bytes=2_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url(target,match="exact"):
    return WAYBACK+"?"+urllib.parse.urlencode([
        ("url",target),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2013"),("to","2018"),("limit","500"),
    ])

def parse_cdx(b):
    d=json.loads(b.decode("utf-8","replace"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def avail_url(ts):
    return AVAILABLE+"?"+urllib.parse.urlencode({"url":TARGET,"timestamp":ts})

def arquivo_url():
    return ARQUIVO+"?"+urllib.parse.urlencode({
        "url":TARGET,"from":"2013","to":"2018","limit":"200","output":"json"
    })

def main():
    print("StoneAge 2.5 2013 Xunlei standalone-client preservation probe — R1")
    print("SCOPE|exact-source+exact-xunlei-url|archive-metadata-only|no-payload-download")
    print(f"SOURCE_PAGE|{SOURCE_PAGE}")
    print(f"TARGET|{TARGET}")
    errors=[]; hits=0

    try:
        st,final,h,b=get(SOURCE_PAGE,20,3_000_000)
        text=b.decode("utf-8","replace")
        has_target=TARGET in text
        print(f"SOURCE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|target_literal={1 if has_target else 0}|final={clean(final)}")
    except Exception as e:
        errors.append(("source",type(e).__name__,str(e)))

    for match in ("exact","prefix"):
        try:
            st,final,h,b=get(cdx_url(TARGET,match),25)
            rows=parse_cdx(b)
            print(f"WAYBACK_CDX|match={match}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|final={clean(final)}")
            for r in rows:
                hits+=1
                print(
                    f"WAYBACK_ROW|match={match}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|"
                    f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
                    f"digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
                )
        except Exception as e:
            errors.append((f"wayback-cdx:{match}",type(e).__name__,str(e)))

    for ts in DATES:
        try:
            st,final,h,b=get(avail_url(ts),20)
            d=json.loads(b.decode("utf-8","replace"))
            c=(d.get("archived_snapshots") or {}).get("closest") or {}
            available=bool(c.get("available"))
            print(f"WAYBACK_AVAILABLE|requested={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|available={1 if available else 0}|closest_ts={clean(c.get('timestamp'))}|closest_status={clean(c.get('status'))}|closest_url={clean(c.get('url'))}")
            if available: hits+=1
        except Exception as e:
            errors.append((f"wayback-available:{ts}",type(e).__name__,str(e)))

    try:
        b=arquivo_fetch_bytes(arquivo_url(),timeout=20,attempts=2)
        rows=arquivo_parse_rows(b)
        print(f"ARQUIVO|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}")
        for r in rows:
            hits+=1
            print(
                f"ARQUIVO_ROW|timestamp={clean(r.get('timestamp') or r.get('date'))}|"
                f"original={clean(r.get('original') or r.get('url'))}|status={clean(r.get('statuscode') or r.get('status'))}|"
                f"mime={clean(r.get('mimetype') or r.get('mime'))}|length={clean(r.get('length') or r.get('contentLength'))}|"
                f"digest={clean(r.get('digest'))}"
            )
    except Exception as e:
        errors.append(("arquivo",type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|hits|{hits}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|XUNLEI_CLIENT_ARCHIVE_METADATA_FOUND|inspect redirects/captures before any descendant-client byte recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_XUNLEI_INDEX_FAILURE|retry only failed surfaces")
    else:
        print("RESOLUTION|XUNLEI_EXACT_ROUTE_BOUNDED|no archive metadata hit on tested exact/prefix surfaces")
    print("EVIDENCE_BOUNDARY|the 2013 source identifies a standalone client download and states local elize.ini modification; even recovered bytes would be descendant/private-server evidence, not original 2002 disc provenance.")

if __name__=="__main__":
    main()
