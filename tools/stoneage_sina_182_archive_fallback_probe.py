#!/usr/bin/env python3
"""Fallback archive-index probe for Sina-labelled sa1.82.exe.

R1 found zero HTTP/IA/DiscMaster hits but Wayback FTP CDX returned 503.
This probe uses independent metadata surfaces: Wayback Availability,
Memento TimeMap, and Arquivo.pt CDX. No client payload is downloaded.
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
    ("ftp-original","ftp://211.90.133.5/dowload/sa/sa1.82.exe"),
    ("http-equivalent","http://211.90.133.5/dowload/sa/sa1.82.exe"),
)

KEY_DATES=(
    "20010110","20010123","20010601","20010908",
    "20020101","20020420","20030101","20030403","20030601",
)


def clean(value,limit=1600):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch_bytes(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return int(getattr(response,"status",response.getcode())),response.geturl(),response.read()


def availability(target,date):
    url=AVAIL+"?"+urllib.parse.urlencode({"url":target,"timestamp":date})
    status,final,body=fetch_bytes(url)
    data=json.loads(body.decode("utf-8"))
    closest=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return date,status,final,None
    return date,status,final,{
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def timemap(target):
    url=TIMEMAP+target
    status,final,body=fetch_bytes(url)
    text=body.decode("utf-8","replace")
    rows=[]
    seen=set()
    for match in re.finditer(
        r'<(?P<replay>https?://[^>]+)>;\s*rel="(?P<rel>[^"]*memento[^"]*)"(?:;\s*datetime="(?P<datetime>[^"]+)")?',
        text,re.I,
    ):
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
    return status,final,tuple(sorted(rows,key=lambda r:r["timestamp"]))


def parse_arquivo(body):
    try:
        data=json.loads(body.decode("utf-8"))
    except Exception:
        return ()
    if isinstance(data,list):
        if data and isinstance(data[0],list) and all(isinstance(x,str) for x in data[0]):
            header=data[0]
            return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))
        return tuple(x for x in data if isinstance(x,dict))
    if isinstance(data,dict):
        rows=data.get("results") or data.get("response") or data.get("captures") or []
        if isinstance(rows,list):
            return tuple(x for x in rows if isinstance(x,dict))
        if any(k in data for k in ("url","original","timestamp")):
            return (data,)
    return ()


def arquivo(target):
    params=[
        ("url",target),("output","json"),
        ("filter","statuscode:200"),("collapse","digest"),
    ]
    url=ARQUIVO+"?"+urllib.parse.urlencode(params)
    status,final,body=fetch_bytes(url)
    return status,final,parse_arquivo(body)


def main():
    print("StoneAge Sina-labelled 1.82 archive fallback probe — R1")
    print("SCOPE|TARGET-B|Wayback-Availability+Memento-TimeMap+Arquivo-CDX|metadata-only|no-client-payload")
    print("KEY_DATES|"+",".join(KEY_DATES))

    total_hits=0
    errors=[]

    for label,target in TARGETS:
        availability_rows=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures={executor.submit(availability,target,date):date for date in KEY_DATES}
            for future in concurrent.futures.as_completed(futures):
                date=futures[future]
                try:
                    availability_rows.append(future.result())
                except Exception as exc:
                    errors.append((f"availability:{label}:{date}",type(exc).__name__,str(exc)))
        availability_rows.sort(key=lambda row:row[0])
        unique={}
        for date,status,final,closest in availability_rows:
            if closest:
                key=(closest["timestamp"],closest["url"])
                unique[key]=closest
            print(
                f"AVAIL|label={label}|date={date}|status={status}|"
                f"hit={int(closest is not None)}|timestamp={clean(closest['timestamp'] if closest else '')}|"
                f"capture={clean(closest['url'] if closest else '')}"
            )
        total_hits+=len(unique)

        try:
            status,final,rows=timemap(target)
            total_hits+=len(rows)
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
            total_hits+=len(rows)
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

    print(f"COUNT|raw_surface_hits|{total_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if total_hits:
        print("RESOLUTION|SINA_182_FALLBACK_CANDIDATES_FOUND|inspect capture identity before payload recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|fallback archive surfaces incomplete")
    else:
        print("RESOLUTION|SINA_182_FALLBACK_NO_HIT|independent fallback indexes returned no capture")


if __name__=="__main__":
    main()
