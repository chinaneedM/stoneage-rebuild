#!/usr/bin/env python3
"""Focused launch-window probe for the official Hangame StoneAge sadl.asp page.

Only Wayback Availability metadata and bounded archived HTML are read. No
client binary is downloaded or committed.
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

from tools.stoneage_japan174a_exact_install_probe import (
    MAX_BODY,
    clean,
    interesting_html_refs,
    signature,
)

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
AVAIL="https://archive.org/wayback/available"
TARGET="http://www.hangame.co.jp:80/publish/sa/sadl.asp"
KEY_DATES=("20031212","20031214","20031215","20031216","20031217","20040115")


def get_json(url,timeout=8):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8","replace"))


def availability(date):
    query=urllib.parse.urlencode({"url":TARGET,"timestamp":date})
    data=get_json(AVAIL+"?"+query)
    closest=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return None
    return {
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def bounded_replay(timestamp,timeout=12):
    replay=f"https://web.archive.org/web/{timestamp}id_/{TARGET}"
    req=urllib.request.Request(
        replay,
        headers={
            "User-Agent":UA,
            "Accept":"text/html,*/*",
            "Accept-Encoding":"identity",
            "Range":f"bytes=0-{MAX_BODY-1}",
        },
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read(MAX_BODY+1)
        return {
            "status":int(getattr(response,"status",200)),
            "final":response.geturl(),
            "body":body[:MAX_BODY],
            "truncated":len(body)>MAX_BODY,
            "content_type":response.headers.get("Content-Type",""),
        }


def main():
    print("StoneAge Japan 1.74a Hangame sadl.asp launch-window probe — R1")
    print("SCOPE|exact-official-page|availability+bounded-html-only|no-client-binary-download")
    print("TARGET|"+TARGET)
    print("KEY_DATES|"+",".join(KEY_DATES))

    captures={}
    errors=[]
    for date in KEY_DATES:
        try:
            cap=availability(date)
        except Exception as exc:
            errors.append((date,type(exc).__name__,str(exc)))
            continue
        if cap is None:
            print(f"AVAIL|requested={date}|available=0")
            continue
        print(
            f"AVAIL|requested={date}|available=1|timestamp={clean(cap['timestamp'])}|"
            f"status={clean(cap['status'])}|url={clean(cap['url'])}"
        )
        if cap["status"]=="200" and cap["timestamp"]:
            captures.setdefault(cap["timestamp"],cap)

    refs=set()
    for timestamp in sorted(captures):
        try:
            result=bounded_replay(timestamp)
        except Exception as exc:
            print(
                f"FETCH_ERROR|timestamp={timestamp}|"
                f"kind={type(exc).__name__}|message={clean(exc)}"
            )
            continue
        body=result["body"]
        sig=signature(body)
        sha=hashlib.sha256(body).hexdigest()
        print(
            f"FETCH|timestamp={timestamp}|status={result['status']}|"
            f"bytes={len(body)}|truncated={int(result['truncated'])}|"
            f"signature={clean(sig)}|sha256={sha}|"
            f"content_type={clean(result['content_type'])}|final={clean(result['final'])}"
        )
        if sig=="html":
            for ref in interesting_html_refs(body):
                refs.add((timestamp,ref))

    for date,kind,message in errors:
        print(
            f"ERROR|requested={date}|kind={clean(kind)}|message={clean(message)}"
        )
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|unique_200_captures|{len(captures)}")
    print(f"COUNT|interesting_refs|{len(refs)}")
    for timestamp,ref in sorted(refs):
        print(f"REF|timestamp={timestamp}|value={clean(ref)}")


if __name__=="__main__":
    main()
