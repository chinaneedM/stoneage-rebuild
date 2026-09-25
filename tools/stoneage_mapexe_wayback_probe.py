#!/usr/bin/env python3
"""Bounded replay probe for the preserved historical StoneAge map.exe capture.

The exact HTTP mirror URL comes from contemporaneous Sina StoneAge 5.0/6.0
download pages. Wayback Availability identifies a 2003-06-23 capture. This
probe reads only a bounded prefix and response metadata; it never downloads
the complete executable.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="http://www.wuxitianlong.com:80/sa/map.exe"
CAPTURE_TS="20030623234451"
REPLAY=f"https://web.archive.org/web/{CAPTURE_TS}id_/{TARGET}"
MAX_PREFIX=256*1024


def clean(v,limit=2000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c >= " " and c != "\x7f").replace("|","%7C")[:limit]


def fetch_json(url,timeout=40):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(1024*1024)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),json.loads(body.decode("utf-8"))


def fetch_prefix(url,limit=MAX_PREFIX,timeout=60):
    req=urllib.request.Request(
        url,
        headers={
            "User-Agent":UA,
            "Accept":"*/*",
            "Range":f"bytes=0-{limit-1}",
            "Accept-Encoding":"identity",
        },
    )
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(limit+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body


def hget(headers,name):
    want=name.lower()
    for key,value in headers.items():
        if str(key).lower()==want:
            return value
    return ""


def pe_info(data):
    if len(data)<64 or data[:2]!=b"MZ":
        return None
    peoff=struct.unpack_from("<I",data,0x3c)[0]
    if peoff+24>len(data) or data[peoff:peoff+4]!=b"PE\x00\x00":
        return {"mz":1,"pe":0,"peoff":peoff}
    machine,sections,timestamp=struct.unpack_from("<HHI",data,peoff+4)
    return {"mz":1,"pe":1,"peoff":peoff,"machine":machine,"sections":sections,"timestamp":timestamp}


def strings(data):
    vals=[]
    seen=set()
    for raw in re.findall(rb"[\x20-\x7e]{6,}",data):
        s=raw.decode("latin1","replace")
        if s not in seen:
            seen.add(s);vals.append(s)
    for raw in re.findall(rb"(?:[\x20-\x7e]\x00){6,}",data):
        s=raw.decode("utf-16le","replace")
        if s not in seen:
            seen.add(s);vals.append(s)
    pat=re.compile(r"(?i)(stone|map|setup|install|waei|sina|version|winzip|rar|cab|7-zip|nsis|wise|inno|patch)")
    return [s for s in vals if pat.search(s)][:120]


def main():
    print("StoneAge historical map.exe Wayback replay probe — R1")
    print("SCOPE|exact-Sina-derived-mirror+Wayback-capture+bounded-prefix|no-full-payload-download")
    print(f"TARGET|url={TARGET}|capture={CAPTURE_TS}|replay={REPLAY}")
    errors=[]
    for date in ("20030101","20030403","20030601","20030623","20030701"):
        try:
            q="https://archive.org/wayback/available?"+urllib.parse.urlencode({"url":TARGET,"timestamp":date})
            status,final,headers,obj=fetch_json(q)
            closest=(obj.get("archived_snapshots") or {}).get("closest") or {}
            print(
                f"AVAIL|date={date}|status={status}|available={int(bool(closest.get('available')))}|"
                f"timestamp={clean(closest.get('timestamp'))}|capture={clean(closest.get('url'))}|"
                f"http_status={clean(closest.get('status'))}|final={clean(final)}"
            )
        except Exception as exc:
            errors.append((f"availability:{date}",type(exc).__name__,str(exc)))
    try:
        status,final,headers,body=fetch_prefix(REPLAY)
        print(
            f"REPLAY|status={status}|final={clean(final)}|bytes_read={len(body)}|"
            f"truncated={int(len(body)>MAX_PREFIX)}|sha256_prefix={hashlib.sha256(body[:MAX_PREFIX]).hexdigest()}|"
            f"content_type={clean(hget(headers,'Content-Type'))}|content_length={clean(hget(headers,'Content-Length'))}|"
            f"content_range={clean(hget(headers,'Content-Range'))}|"
            f"orig_length={clean(hget(headers,'X-Archive-Orig-Content-Length'))}|"
            f"orig_type={clean(hget(headers,'X-Archive-Orig-Content-Type'))}|"
            f"orig_last_modified={clean(hget(headers,'X-Archive-Orig-Last-Modified'))}|"
            f"orig_etag={clean(hget(headers,'X-Archive-Orig-Etag'))}|"
            f"memento={clean(hget(headers,'Memento-Datetime'))}"
        )
        sample=body[:MAX_PREFIX]
        print(f"MAGIC|hex={sample[:32].hex()}")
        info=pe_info(sample)
        if info:
            print("PE|"+"|".join(f"{k}={clean(v)}" for k,v in info.items()))
        else:
            print("PE|mz=0|pe=0")
        ss=strings(sample)
        print(f"COUNT|interesting_strings|{len(ss)}")
        for i,s in enumerate(ss,1):
            print(f"STRING|index={i}|value={clean(s,1200)}")
    except Exception as exc:
        errors.append(("replay",type(exc).__name__,str(exc)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    print("EVIDENCE_BOUNDARY|capture timestamp proves archival observation time only; internal executable metadata may predate capture but does not alone prove the exact bytes were served on the earlier 5.0-page date.")


if __name__=="__main__":
    main()
