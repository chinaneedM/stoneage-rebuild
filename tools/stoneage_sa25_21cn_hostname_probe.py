#!/usr/bin/env python3
"""Probe 21CN hostname variants for the historical sa25up.zip path.

The hostname is evidence-derived from archived pages served by the same IP. This probe
queries archive metadata/replays only; it does not assume DNS equivalence or download
the historical game payload.
"""
from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAILABLE="https://archive.org/wayback/available"

TARGETS=(
    ("download-http","http://download.21cn.com/file/game/maoxian/sa25up.zip"),
    ("download-www-http","http://www.download.21cn.com/file/game/maoxian/sa25up.zip"),
    ("www21cn-http","http://www.21cn.com/file/game/maoxian/sa25up.zip"),
)
PREFIXES=(
    ("download-maoxian","http://download.21cn.com/file/game/maoxian/"),
    ("download-game","http://download.21cn.com/file/game/"),
)
DATES=("20020120","20020712","20020929","20030605","20030623","20040101")


def clean(v,limit=1600):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),body


def cdx_url(url,match="exact",status=None,limit=1000):
    p=[
        ("url",url),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2001"),("to","2005"),("collapse","urlkey"),("limit",str(limit)),
    ]
    if status is not None:
        p.append(("filter",f"statuscode:{status}"))
    return CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    h=data[0]
    return tuple(dict(zip(h,row)) for row in data[1:] if isinstance(row,list))


def availability_url(url,date):
    return AVAILABLE+"?"+urllib.parse.urlencode({"url":url,"timestamp":date})


def closest(body):
    data=json.loads(body.decode("utf-8","replace"))
    c=(data.get("archived_snapshots") or {}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):
        return None
    return c


def emit(label,row):
    print(
        f"HIT|label={clean(label)}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
        f"status={clean(row.get('statuscode'))}|mime={clean(row.get('mimetype'))}|"
        f"length={clean(row.get('length'))}|digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}"
    )


def main():
    print("StoneAge 2.5 21CN hostname sa25up mirror probe — R1")
    print("SCOPE|archive-metadata-only|evidence-derived-hostname-variants|no-game-payload-download")
    print("HOST_EVIDENCE|archived IP-served pages identify 21CN.COM and download.21cn.com")

    errors=[]
    hits=0
    for label,url in TARGETS:
        try:
            st,final,body=fetch(cdx_url(url,"exact",None,200))
            rows=parse_cdx(body)
            print(
                f"CDX_EXACT|label={label}|url={clean(url)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for row in rows:
                hits+=1; emit(label,row)
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))

        for date in DATES:
            try:
                st,final,body=fetch(availability_url(url,date),20)
                c=closest(body)
                print(
                    f"AVAILABLE|label={label}|requested={date}|status={st}|bytes={len(body)}|"
                    f"sha256={hashlib.sha256(body).hexdigest()}|available={1 if c else 0}|final={clean(final)}"
                )
                if c:
                    print(
                        f"AVAILABLE_HIT|label={label}|requested={date}|timestamp={clean(c.get('timestamp'))}|"
                        f"status={clean(c.get('status'))}|url={clean(c.get('url'))}"
                    )
            except Exception as e:
                errors.append((f"available:{label}:{date}",type(e).__name__,str(e)))

    for label,prefix in PREFIXES:
        try:
            st,final,body=fetch(cdx_url(prefix,"prefix",None,2000))
            rows=parse_cdx(body)
            relevant=[r for r in rows if "sa25" in urllib.parse.unquote(str(r.get("original") or "")).lower() or "stoneage" in urllib.parse.unquote(str(r.get("original") or "")).lower()]
            print(
                f"CDX_PREFIX|label={label}|prefix={clean(prefix)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|relevant={len(relevant)}|final={clean(final)}"
            )
            for row in relevant:
                hits+=1; emit(label,row)
        except Exception as e:
            errors.append((f"prefix:{label}",type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|hits|{hits}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|21CN_HOSTNAME_ARCHIVE_SIGNAL_FOUND|compare status,digest,path against IP-form records before any payload recovery claim")
    elif errors:
        print("RESOLUTION|PARTIAL_21CN_HOSTNAME_FAILURE|retry failed archive surfaces only")
    else:
        print("RESOLUTION|NO_21CN_HOSTNAME_SA25UP_HIT|hostname-variant archive surface bounded")
    print(
        "EVIDENCE_BOUNDARY|21CN branding on the IP host justifies hostname variants as search candidates; "
        "it does not prove historical DNS equivalence or byte identity."
    )


if __name__=="__main__":
    main()
