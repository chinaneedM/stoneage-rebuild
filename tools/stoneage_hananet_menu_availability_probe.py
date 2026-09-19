#!/usr/bin/env python3
"""Probe Wayback Availability for Hananet StoneAge dedicated menu pages."""

from __future__ import annotations

import concurrent.futures
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
API="https://archive.org/wayback/available"
URLS=[
    "http://stoneage.hananet.net/main.htm",
    "http://stoneage.hananet.net/1.htm",
    "http://stoneage.hananet.net/2.htm",
    "http://stoneage.hananet.net/2_2.htm",
    "http://stoneage.hananet.net/2_3.htm",
    "http://stoneage.hananet.net/2_4.htm",
    "http://stoneage.hananet.net/2_5.htm",
]
DATES=["20001229","20010118","20010201","20010430"]


def request_json(url:str, timeout:int=8):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.load(r)


def closest(payload):
    c=payload.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):
        return None
    return str(c.get("timestamp","")),str(c.get("status","")),str(c.get("url",""))


def safe(v,limit=700):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def one(job):
    original,date=job
    q=urllib.parse.urlencode({"url":original,"timestamp":date})
    try:
        c=closest(request_json(API+"?"+q))
    except Exception as exc:
        return ("error",original,date,type(exc).__name__,str(exc))
    if not c:
        return ("miss",original,date,"","","")
    return ("hit",original,date,*c)


def main():
    print("StoneAge Hananet dedicated-menu availability probe — R1")
    print("SCOPE|metadata-only|no-page-body|no-client-binary-download")
    jobs=[(u,d) for u in URLS for d in DATES]
    results=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for row in ex.map(one,jobs):
            if row[0]=="error":
                errors.append(row)
            else:
                results.append(row)
    print(f"COUNT|queries|{len(jobs)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|available|{sum(1 for r in results if r[0]=='hit')}")
    for _,original,date,kind,message in sorted(errors):
        print(f"ERROR|requested={date}|url={safe(original)}|kind={kind}|message={safe(message)}")
    for row in sorted(results,key=lambda r:(r[1],r[2])):
        if row[0]=="miss":
            _,original,date,_,_,_=row
            print(f"RESULT|requested={date}|available=0|url={safe(original)}")
        else:
            _,original,date,ts,status,archived=row
            print(f"RESULT|requested={date}|available=1|timestamp={ts}|status={status}|url={safe(original)}|archived={safe(archived)}")


if __name__=="__main__":
    main()
