#!/usr/bin/env python3
"""Probe long-window Wayback CDX survival for exact GameTime StoneAge payload paths.

Metadata only. No archived payload bytes are requested.
"""

from __future__ import annotations

import concurrent.futures
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="2000"
TO="2012"

BASE_TARGETS=[
    ("gw9-onlstoneage","/images/Online/pds/2001/02/onlStoneAge.zip"),
    ("gw76-stone-demo","/images/Online/pds/2001/02/stone_demo.exe"),
]

HOSTS=[
    "www.gametime.co.kr",
    "gametime.co.kr",
    "www.gametime.co.kr:80",
    "gametime.co.kr:80",
]
SCHEMES=["http","https"]


def variants():
    out=[]
    seen=set()
    for label,path in BASE_TARGETS:
        for scheme in SCHEMES:
            for host in HOSTS:
                url=f"{scheme}://{host}{path}"
                if url in seen:
                    continue
                seen.add(url)
                out.append((label,url))
    return out


def clean(v,limit=1000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=20):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.read()


def parse(body):
    text=body.decode("utf-8","replace").strip()
    if not text:
        return []
    data=json.loads(text)
    if not isinstance(data,list) or not data:
        return []
    header=data[0]
    if not isinstance(header,list):
        return []
    return [
        {str(header[i]):str(row[i]) if i<len(row) else "" for i in range(len(header))}
        for row in data[1:] if isinstance(row,list)
    ]


def query_url(url):
    params=[
        ("url",url),
        ("matchType","exact"),
        ("from",FROM),
        ("to",TO),
        ("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length,redirect"),
        ("collapse","digest"),
        ("limit","1000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def one(row):
    label,url=row
    try:
        rows=parse(get(query_url(url)))
        return label,url,rows,None
    except Exception as exc:
        return label,url,[],(type(exc).__name__,str(exc))


def main():
    targets=variants()
    print("StoneAge GameTime long-window exact payload CDX probe — R1")
    print("SCOPE|wayback-cdx-metadata-only|no-payload-download")
    print(f"WINDOW|from={FROM}|to={TO}")
    print(f"COUNT|queries|{len(targets)}")

    results=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for label,url,rows,error in ex.map(one,targets):
            if error:
                errors.append((label,url,error[0],error[1]))
            else:
                results.append((label,url,rows))

    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|rows|{sum(len(rows) for _,_,rows in results)}")
    print(f"COUNT|queries_with_rows|{sum(bool(rows) for _,_,rows in results)}")

    for label,url,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|url={clean(url)}|kind={clean(kind)}|message={clean(msg)}")

    for label,url,rows in results:
        print(f"QUERY|label={clean(label)}|url={clean(url)}|rows={len(rows)}")
        for row in rows:
            print(
                f"ROW|label={clean(label)}|query={clean(url)}|"
                f"timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
                f"status={clean(row.get('statuscode'))}|mime={clean(row.get('mimetype'))}|"
                f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}|"
                f"redirect={clean(row.get('redirect'))}"
            )


if __name__=="__main__":
    main()
