#!/usr/bin/env python3
"""Verify exact Japanese StoneAge 1.74a payload URLs recovered from sadl.asp.

Metadata and at most 64 KiB of archived response bytes are read. No full client
payload is downloaded or committed by this probe.
"""

from __future__ import annotations

import hashlib
import json
import re
import struct
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
TIMEMAP="https://web.archive.org/web/timemap/link/"
MAX_PREFIX=64*1024

TARGETS=(
    (
        "launch-client-sa174hg",
        "http://hangame.gamania.co.jp/stoneage/sa174hg.exe",
    ),
    (
        "sadl-relative-stoneage-exe",
        "http://www.hangame.co.jp:80/publish/sa/stoneage.exe",
    ),
)
KEY_DATES=("20031212","20031214","20031215","20031216","20031217","20040115","20040401")


def clean(value,limit=1400):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|","%7C")[:limit]


def get(url,*,timeout=12,headers=None,limit=MAX_PREFIX):
    hdr={"User-Agent":UA,"Accept":"*/*","Accept-Encoding":"identity"}
    if headers:
        hdr.update(headers)
    req=urllib.request.Request(url,headers=hdr)
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read(limit+1)
        return {
            "status":int(getattr(response,"status",200)),
            "final":response.geturl(),
            "headers":dict(response.headers),
            "body":body[:limit],
            "truncated":len(body)>limit,
        }


def get_json(url,timeout=8):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Accept":"application/json"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8","replace"))


def cdx_exact(url):
    params=[
        ("url",url),("matchType","exact"),("from","2003"),("to","2005"),
        ("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length,redirect"),
        ("limit","100"),
    ]
    endpoint=CDX+"?"+urllib.parse.urlencode(params)
    try:
        raw=get(endpoint,timeout=12,limit=256*1024)["body"]
    except urllib.error.HTTPError as exc:
        if exc.code in (404,503):
            return [],f"HTTPError:{exc.code}"
        raise
    text=raw.decode("utf-8","replace").strip()
    if not text:
        return [],None
    data=json.loads(text)
    if not isinstance(data,list) or not data:
        return [],None
    header=data[0]
    rows=[]
    for row in data[1:]:
        if not isinstance(row,list):
            continue
        rows.append({
            str(header[i]):str(row[i]) if i < len(row) else ""
            for i in range(len(header))
        })
    return rows,None


def availability(url,date):
    params=urllib.parse.urlencode({"url":url,"timestamp":date})
    data=get_json(AVAIL+"?"+params)
    closest=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return None
    return {
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def parse_timemap_link(data,url):
    """Normalize Memento link-format rows for one exact original URL."""
    text=data.decode("utf-8","replace")
    rows=[]
    seen=set()
    pattern=re.compile(
        r'<(?P<replay>https?://[^>]+)>;\s*'
        r'rel="(?P<rel>[^"]*memento[^"]*)"'
        r'(?:;\s*datetime="(?P<datetime>[^"]+)")?',
        re.I,
    )
    for match in pattern.finditer(text):
        replay=match.group("replay")
        ts_match=re.search(r"/web/(\d{14})(?:[a-z_]+)?/",replay,re.I)
        if not ts_match:
            continue
        timestamp=ts_match.group(1)
        key=(timestamp,url)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "timestamp":timestamp,
                "status":"200",
                "url":url,
                "source":"timemap",
                "replay":replay,
                "rel":match.group("rel"),
                "datetime":match.group("datetime") or "",
            }
        )
    return tuple(sorted(rows,key=lambda row:row["timestamp"]))


def timemap_exact(url):
    endpoint=TIMEMAP+url
    raw=get(endpoint,timeout=12,limit=256*1024)["body"]
    return parse_timemap_link(raw,url)


def signature(body):
    body=bytes(body)
    if body.startswith(b"MZ"):
        return "pe-mz"
    if body.startswith(b"MSCF"):
        return "cab-mscf"
    if body.startswith(b"PK\x03\x04"):
        return "zip"
    lower=body[:64].lstrip().lower()
    if lower.startswith(b"<html") or lower.startswith(b"<!doctype"):
        return "html"
    return "other:"+body[:16].hex()


def pe_header_summary(body):
    data=bytes(body)
    if len(data)<0x40 or data[:2] != b"MZ":
        return None
    pe_off=struct.unpack_from("<I",data,0x3C)[0]
    if pe_off+24 > len(data) or data[pe_off:pe_off+4] != b"PE\0\0":
        return {"pe_offset":pe_off,"complete":False}
    machine,sections,timestamp,_,_,optional_size,characteristics=struct.unpack_from(
        "<HHIIIHH",data,pe_off+4
    )
    magic=None
    subsystem=None
    linker_major=None
    linker_minor=None
    if pe_off+24+optional_size <= len(data) and optional_size >= 70:
        optional=pe_off+24
        magic=struct.unpack_from("<H",data,optional)[0]
        linker_major=data[optional+2]
        linker_minor=data[optional+3]
        subsystem=struct.unpack_from("<H",data,optional+68)[0]
    return {
        "pe_offset":pe_off,
        "complete":True,
        "machine":machine,
        "sections":sections,
        "coff_timestamp":timestamp,
        "optional_size":optional_size,
        "characteristics":characteristics,
        "optional_magic":magic,
        "linker_major":linker_major,
        "linker_minor":linker_minor,
        "subsystem":subsystem,
    }


def select_capture_rows(url,cdx_rows,avail_rows):
    merged={}
    for row in cdx_rows:
        ts=str(row.get("timestamp",""))
        original=str(row.get("original","") or url)
        if not ts:
            continue
        merged[(ts,original)]={
            "timestamp":ts,
            "original":original,
            "status":str(row.get("statuscode","")),
            "mime":str(row.get("mimetype","")),
            "digest":str(row.get("digest","")),
            "length":str(row.get("length","")),
            "redirect":str(row.get("redirect","")),
            "source":"cdx",
        }
    for cap in avail_rows:
        if not cap or not cap.get("timestamp"):
            continue
        merged.setdefault(
            (str(cap["timestamp"]),url),
            {
                "timestamp":str(cap["timestamp"]),
                "original":url,
                "status":str(cap.get("status","")),
                "mime":"",
                "digest":"",
                "length":"",
                "redirect":"",
                "source":str(cap.get("source","availability")),
            },
        )
    return tuple(sorted(merged.values(),key=lambda x:(x["timestamp"],x["original"])))


def prefix_probe(row):
    replay=f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"
    try:
        result=get(
            replay,
            timeout=15,
            headers={"Range":f"bytes=0-{MAX_PREFIX-1}"},
            limit=MAX_PREFIX,
        )
    except Exception as exc:
        return {
            "ok":False,"replay":replay,"error":f"{type(exc).__name__}:{exc}",
            "status":"","bytes":0,"truncated":False,"signature":"",
            "sha256":"","content_type":"","content_length":"",
            "content_range":"","final":"","pe":None,
        }
    body=result["body"]
    return {
        "ok":True,
        "replay":replay,
        "error":"",
        "status":result["status"],
        "bytes":len(body),
        "truncated":result["truncated"],
        "signature":signature(body),
        "sha256":hashlib.sha256(body).hexdigest(),
        "content_type":result["headers"].get("Content-Type",""),
        "content_length":result["headers"].get("Content-Length",""),
        "content_range":result["headers"].get("Content-Range",""),
        "final":result["final"],
        "pe":pe_header_summary(body),
    }


def main():
    print("StoneAge Japan 1.74a exact payload metadata probe — R2")
    print("SCOPE|launch-page-exact-urls|cdx+availability+timemap+64KiB-prefix-only|no-full-client-download")
    print("PROVENANCE|sa174hg.exe recovered from official Hangame sadl.asp snapshot 20031214051053")
    print("KEY_DATES|"+",".join(KEY_DATES))

    for label,url in TARGETS:
        try:
            cdx_rows,cdx_error=cdx_exact(url)
        except Exception as exc:
            cdx_rows=[]
            cdx_error=f"{type(exc).__name__}:{exc}"

        timemap_rows=[]
        timemap_error=""
        try:
            timemap_rows=list(timemap_exact(url))
        except Exception as exc:
            timemap_error=f"{type(exc).__name__}:{exc}"

        avail_rows=[]
        avail_errors=[]
        for date in KEY_DATES:
            try:
                avail_rows.append(availability(url,date))
            except Exception as exc:
                avail_errors.append((date,f"{type(exc).__name__}:{exc}"))

        captures=select_capture_rows(url,cdx_rows,avail_rows+timemap_rows)
        launch_rows=[
            row for row in captures
            if "20031212" <= row["timestamp"][:8] <= "20040131"
        ]
        print(
            f"TARGET|label={clean(label)}|url={clean(url)}|"
            f"cdx_rows={len(cdx_rows)}|cdx_error={clean(cdx_error)}|"
            f"timemap_rows={len(timemap_rows)}|timemap_error={clean(timemap_error)}|"
            f"availability_hits={sum(x is not None for x in avail_rows)}|"
            f"availability_errors={len(avail_errors)}|captures={len(captures)}|"
            f"launch_window_captures={len(launch_rows)}"
        )
        for date,error in avail_errors:
            print(f"AVAIL_ERROR|label={clean(label)}|date={date}|error={clean(error)}")
        for row in captures:
            print(
                f"CAPTURE|label={clean(label)}|timestamp={row['timestamp']}|"
                f"source={row['source']}|status={clean(row['status'])}|"
                f"mime={clean(row['mime'])}|length={clean(row['length'])}|"
                f"digest={clean(row['digest'])}|redirect={clean(row['redirect'])}|"
                f"url={clean(row['original'])}"
            )

        # Probe no more than the earliest three launch/near-launch captures.
        selected=(launch_rows or list(captures))[:3]
        for row in selected:
            result=prefix_probe(row)
            print(
                f"PREFIX|label={clean(label)}|timestamp={row['timestamp']}|"
                f"ok={int(result['ok'])}|status={clean(result['status'])}|"
                f"bytes={result['bytes']}|truncated={int(result['truncated'])}|"
                f"signature={clean(result['signature'])}|sha256={clean(result['sha256'])}|"
                f"content_type={clean(result['content_type'])}|"
                f"content_length={clean(result['content_length'])}|"
                f"content_range={clean(result['content_range'])}|"
                f"final={clean(result['final'])}|error={clean(result['error'])}"
            )
            if result["pe"] is not None:
                pe=result["pe"]
                print(
                    f"PE|label={clean(label)}|timestamp={row['timestamp']}|"
                    f"pe_offset={pe.get('pe_offset','')}|complete={int(bool(pe.get('complete')))}|"
                    f"machine={pe.get('machine','')}|sections={pe.get('sections','')}|"
                    f"coff_timestamp={pe.get('coff_timestamp','')}|"
                    f"optional_size={pe.get('optional_size','')}|"
                    f"optional_magic={pe.get('optional_magic','')}|"
                    f"linker={pe.get('linker_major','')}.{pe.get('linker_minor','')}|"
                    f"subsystem={pe.get('subsystem','')}|"
                    f"characteristics={pe.get('characteristics','')}"
                )


if __name__=="__main__":
    main()
