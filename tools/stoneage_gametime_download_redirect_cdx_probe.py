#!/usr/bin/env python3
"""Enumerate GameTime download-endpoint CDX records including redirects.

Metadata only. Unlike the broad prefix census, this probe intentionally keeps
3xx responses and requests the CDX redirect field so historical attachment
targets can be recovered without requesting client payload bytes.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="2000"
TO="2002"
TARGETS=[
    ("data-download-www","http://www.gametime.co.kr/data/download.asp"),
    ("data-download-bare","http://gametime.co.kr/data/download.asp"),
    ("legacy-download-www","http://www.gametime.co.kr/webzine/online/download.asp"),
    ("legacy-download-bare","http://gametime.co.kr/webzine/online/download.asp"),
]
STONE=re.compile(r"(?i)(GW_IDX=(?:9|34|76)\b|stone|age|demo|beta|sa[_./-])")


def clean(v,limit=1200):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=25,attempts=3):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(
                url,
                headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"},
            )
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last=exc
            if i+1<attempts:
                time.sleep(0.8*(i+1))
    raise last


def cdx_url(base):
    params=[
        ("url",base),
        ("matchType","prefix"),
        ("from",FROM),
        ("to",TO),
        ("output","json"),
        ("fl","urlkey,timestamp,original,mimetype,statuscode,digest,length,redirect"),
        ("collapse","timestamp:8"),
        ("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def parse(body):
    text=body.decode("utf-8","replace").strip()
    if not text:
        return []
    data=json.loads(text)
    if not isinstance(data,list) or not data:
        return []
    header=data[0]
    return [
        {str(header[i]):str(row[i]) if i<len(row) else "" for i in range(len(header))}
        for row in data[1:] if isinstance(row,list)
    ]


def one(target):
    label,base=target
    try:
        rows=parse(get(cdx_url(base)))
        return label,base,rows,None
    except Exception as exc:
        return label,base,[],(type(exc).__name__,str(exc))


def interesting(row):
    blob=" ".join((row.get("original",""),row.get("redirect","")))
    return bool(STONE.search(blob))


def main():
    print("StoneAge GameTime download redirect CDX probe — R1")
    print("SCOPE|cdx-metadata-including-3xx-redirects|no-payload-download")
    print(f"WINDOW|from={FROM}|to={TO}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results=list(ex.map(one,TARGETS))

    errors=[]
    all_rows=[]
    for label,base,rows,error in results:
        if error:
            errors.append((label,base,error[0],error[1]))
            print(f"PREFIX|label={clean(label)}|url={clean(base)}|status=error|rows=0")
            continue
        print(f"PREFIX|label={clean(label)}|url={clean(base)}|status=ok|rows={len(rows)}")
        for row in rows:
            all_rows.append((label,row))

    print(f"COUNT|queries|{len(TARGETS)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|rows|{len(all_rows)}")
    print(f"COUNT|redirect_rows|{sum(bool(r.get('redirect')) for _,r in all_rows)}")
    print(f"COUNT|interesting_rows|{sum(interesting(r) for _,r in all_rows)}")

    for label,base,kind,msg in errors:
        print(
            f"ERROR|label={clean(label)}|url={clean(base)}|kind={clean(kind)}|message={clean(msg)}"
        )

    for label,row in sorted(
        all_rows,
        key=lambda x:(not interesting(x[1]),x[0],x[1].get("timestamp",""),x[1].get("original","")),
    ):
        marker="HIT" if interesting(row) else "ROW"
        print(
            f"{marker}|label={clean(label)}|timestamp={clean(row.get('timestamp'))}|"
            f"url={clean(row.get('original'))}|status={clean(row.get('statuscode'))}|"
            f"mime={clean(row.get('mimetype'))}|redirect={clean(row.get('redirect'),1400)}|"
            f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
        )


if __name__=="__main__":
    main()
