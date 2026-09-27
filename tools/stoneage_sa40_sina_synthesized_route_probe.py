#!/usr/bin/env python3
"""Probe the evidence-synthesized Sina StoneAge 4.0 map-package route.

A Q4-2002 archived Sina download.pl row with col=updatex and its own filename
directly resolves to http://202.106.185.223/updatex_1024/<filename>. The target
record is also col=updatex, so this probe tests exactly one synthesized target
basename on that category-specific base plus the base-directory CDX surface.
Metadata/headers only; no package payload is downloaded.
"""
from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
BASE="http://202.106.185.223/updatex_1024/"
TARGET_FILE="shiqi4updatex_02_11_08.zip"
TARGET=BASE+TARGET_FILE


def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=40,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.4","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b


def cdx(url,match_type,from_="20021001",to="20030331",limit=10000):
    p=[
      ("url",url),("matchType",match_type),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from",from_),("to",to),("limit",str(limit)),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))


def availability(url,date):
    u=AVAIL+"?"+urllib.parse.urlencode({"url":url,"timestamp":date})
    st,final,h,b=fetch(u,timeout=25,max_bytes=512*1024)
    d=json.loads(b.decode("utf-8"))
    c=(d.get("archived_snapshots") or {}).get("closest") or {}
    return st,c if c.get("available") else None


def main():
    print("StoneAge 4.0 synthesized Sina updatex route probe — R1")
    print("SCOPE|category-derived exact base + exact target + directory CDX|metadata-only|no-payload")
    print(f"EVIDENCE_BASE|col=updatex|sample=aid15055:f99adidasball_629.zip|base={BASE}")
    print(f"TARGET|filename={TARGET_FILE}|url={TARGET}")
    errors=[];exact_rows=[];dir_rows=[]
    for label,url,mt in (("target-exact",TARGET,"exact"),("updatex-base",BASE,"prefix")):
        try:
            st,final,h,b=fetch(cdx(url,mt),timeout=50,max_bytes=8*1024*1024)
            rr=rows(b)
            print(f"CDX|label={label}|match={mt}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                line=(
                  f"ROW|label={label}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|"
                  f"statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|"
                  f"digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}"
                )
                print(line)
            if label=="target-exact":exact_rows.extend(rr)
            else:dir_rows.extend(rr)
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))

    for date in ("20021108","20021109","20021116","20021201","20030101"):
        try:
            st,c=availability(TARGET,date)
            print(
              f"AVAIL|date={date}|status={st}|hit={int(c is not None)}|"
              f"timestamp={clean(c.get('timestamp') if c else '')}|"
              f"capture={clean(c.get('url') if c else '')}"
            )
        except Exception as e:
            errors.append((f"avail:{date}",type(e).__name__,str(e)))

    exact_in_dir=[
      r for r in dir_rows
      if urllib.parse.urlsplit(str(r.get("original") or "")).path.lower().endswith("/"+TARGET_FILE.lower())
    ]
    print(f"COUNT|exact_rows|{len(exact_rows)}")
    print(f"COUNT|directory_rows|{len(dir_rows)}")
    print(f"COUNT|target_rows_inside_directory|{len(exact_in_dir)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact_rows or exact_in_dir:
        print("RESOLUTION|SYNTHESIZED_TARGET_CAPTURE_FOUND|next step is bounded header/byte recovery and archive verification")
    elif dir_rows:
        print("RESOLUTION|UPDATE_X_DIRECTORY_ARCHIVED_NO_TARGET_ROW|retain base as proven category topology; target package remains unpreserved on tested Wayback surface")
    elif errors:
        print("RESOLUTION|SYNTHESIZED_ROUTE_SURFACE_INCOMPLETE|retry exact target/base only")
    else:
        print("RESOLUTION|NO_WAYBACK_ROW_FOR_SYNTHESIZED_ROUTE|close this exact Wayback candidate unless a new host/directory token appears")
    print("EVIDENCE_BOUNDARY|The base is proven by a neighboring updatex record, but target-path synthesis is still a hypothesis until the target URL or bytes are independently observed.")


if __name__=="__main__":
    main()
