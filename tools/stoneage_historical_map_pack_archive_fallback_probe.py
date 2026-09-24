#!/usr/bin/env python3
"""Fallback archive-index probe for historical StoneAge full-map packages.

Complements STONEAGE-HISTORICAL-MAP-PACK-ARCHIVE-R1 when Wayback CDX is
incomplete. Queries Wayback Availability, Memento TimeMap and Arquivo.pt CDX
for the exact source-derived 4.0/5.0/6.0 map-package targets. Metadata only;
no proprietary package payload is downloaded.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
AVAIL="https://archive.org/wayback/available"
TIMEMAP="https://web.archive.org/web/timemap/link/"
ARQUIVO="https://arquivo.pt/wayback/cdx"

TARGETS=(
    (
        "40-map-patch",
        "http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=updatex&aid=61620&title=%A1%B6%CA%AF%C6%F7%CA%B1%B4%FA4.0%A1%B7%D7%EE%D0%C2%B5%D8%CD%BC%B2%B9%B6%A1&author=%D3%CE%C3%F1%B2%BF%C2%E4%CD%F8xinhaonanhai&filename=shiqi4updatex_02_11_08.zip&size=3440",
    ),
    ("50-60-map-ftp","ftp://211.90.133.5/dowload/sa/map.exe"),
    ("50-60-map-http-mirror","http://www.wuxitianlong.com/sa/map.exe"),
)

KEY_DATES=(
    "20020401","20021108","20021201",
    "20030101","20030403","20030601","20040101",
)


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch_bytes(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return int(getattr(response,"status",response.getcode())),response.geturl(),response.read()


def availability(target,date):
    endpoint=AVAIL+"?"+urllib.parse.urlencode({"url":target,"timestamp":date})
    status,final,body=fetch_bytes(endpoint)
    data=json.loads(body.decode("utf-8"))
    closest=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return date,status,None
    return date,status,{
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def timemap(target):
    endpoint=TIMEMAP+target
    status,final,body=fetch_bytes(endpoint)
    text=body.decode("utf-8","replace")
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
        ts=re.search(r"/web/(\d{14})(?:[a-z_]+)?/",replay,re.I)
        if not ts:
            continue
        key=(ts.group(1),replay)
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "timestamp":ts.group(1),
            "replay":replay,
            "datetime":match.group("datetime") or "",
        })
    return status,final,tuple(sorted(rows,key=lambda row:row["timestamp"]))


def parse_arquivo(body):
    try:
        data=json.loads(body.decode("utf-8"))
    except Exception:
        return ()
    if isinstance(data,list):
        if data and isinstance(data[0],list) and all(isinstance(x,str) for x in data[0]):
            header=data[0]
            return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))
        return tuple(row for row in data if isinstance(row,dict))
    if isinstance(data,dict):
        rows=data.get("results") or data.get("response") or data.get("captures") or []
        if isinstance(rows,list):
            return tuple(row for row in rows if isinstance(row,dict))
        if any(key in data for key in ("url","original","timestamp")):
            return (data,)
    return ()


def arquivo(target):
    params=[
        ("url",target),("output","json"),
        ("filter","statuscode:200"),("collapse","digest"),
    ]
    endpoint=ARQUIVO+"?"+urllib.parse.urlencode(params)
    status,final,body=fetch_bytes(endpoint)
    return status,final,parse_arquivo(body)


def main():
    print("StoneAge historical full-map package archive fallback — R1")
    print("SCOPE|Wayback-Availability+Memento-TimeMap+Arquivo-CDX|exact-source-derived-targets|metadata-only|no-payload-download")
    print("KEY_DATES|"+",".join(KEY_DATES))

    errors=[]
    raw_hits=0

    for label,target in TARGETS:
        avail_rows=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures={executor.submit(availability,target,date):date for date in KEY_DATES}
            for future in concurrent.futures.as_completed(futures):
                date=futures[future]
                try:
                    avail_rows.append(future.result())
                except Exception as exc:
                    errors.append((f"availability:{label}:{date}",type(exc).__name__,str(exc)))
        avail_rows.sort(key=lambda row:row[0])
        unique={}
        for date,status,closest in avail_rows:
            if closest:
                unique[(closest["timestamp"],closest["url"])]=closest
            print(
                f"AVAIL|label={label}|date={date}|status={status}|hit={int(closest is not None)}|"
                f"timestamp={clean(closest['timestamp'] if closest else '')}|"
                f"capture={clean(closest['url'] if closest else '')}"
            )
        raw_hits+=len(unique)

        try:
            status,final,rows=timemap(target)
            raw_hits+=len(rows)
            print(f"TIMEMAP|label={label}|status={status}|rows={len(rows)}|final={clean(final)}")
            for row in rows:
                print(
                    f"TIMEMAP_HIT|label={label}|timestamp={row['timestamp']}|"
                    f"datetime={clean(row['datetime'])}|replay={clean(row['replay'])}"
                )
        except Exception as exc:
            errors.append((f"timemap:{label}",type(exc).__name__,str(exc)))

        try:
            status,final,rows=arquivo(target)
            raw_hits+=len(rows)
            print(f"ARQUIVO|label={label}|status={status}|rows={len(rows)}|final={clean(final)}")
            for row in rows[:100]:
                print(
                    f"ARQUIVO_HIT|label={label}|timestamp={clean(row.get('timestamp') or row.get('tstamp'))}|"
                    f"original={clean(row.get('original') or row.get('url') or row.get('originalURL'))}|"
                    f"statuscode={clean(row.get('statuscode') or row.get('status'))}|"
                    f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
                )
        except Exception as exc:
            errors.append((f"arquivo:{label}",type(exc).__name__,str(exc)))

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|raw_surface_hits|{raw_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if raw_hits:
        print("RESOLUTION|MAP_PACK_FALLBACK_CANDIDATES_FOUND|verify capture identity before transient payload analysis")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|fallback map-package archive surfaces incomplete")
    else:
        print("RESOLUTION|MAP_PACK_FALLBACK_NO_HIT|independent fallback indexes returned no capture")


if __name__=="__main__":
    main()
