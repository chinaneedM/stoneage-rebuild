#!/usr/bin/env python3
"""Enumerate archived filenames under known Korean StoneAge distribution directories.

Metadata only. Uses Wayback CDX prefix queries and does not fetch archived payload bytes.
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
    ("hananet-down","http://stoneage.hananet.net/down/"),
    ("hananet-down-www","http://www.stoneage.hananet.net/down/"),
    ("cnet-online","http://korea.cnet.com/pc/games/online/"),
    ("cnet-online-www","http://www.korea.cnet.com/pc/games/online/"),
    ("gagamel-webdata","http://www.gagamel.com/web_data/download/"),
    ("gagamel-webdata-bare","http://gagamel.com/web_data/download/"),
    ("gametime-data","http://www.gametime.co.kr/data/"),
    ("gametime-data-bare","http://gametime.co.kr/data/"),
    ("gametime-webzine","http://www.gametime.co.kr/webzine/online/"),
    ("gametime-webzine-bare","http://gametime.co.kr/webzine/online/"),
    ("gametime-pds","http://pds.gametime.co.kr/"),
    ("gametime-image-pds","http://www.gametime.co.kr/images/Online/pds/2001/02/"),
    ("gametime-image-pds-bare","http://gametime.co.kr/images/Online/pds/2001/02/"),
    ("inium-root-download","http://stoneage.enium.co.kr/down"),
    ("inium-root-download-www","http://www.stoneage.enium.co.kr/down"),
]
INTEREST=re.compile(
    r"(?i)(stone|age|sa(?:_|\.|/)|demo|client|setup|install|patch|update|beta|exe|zip|cab|rar|download)"
)


def clean(v,limit=900):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=25,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last=exc
            if i+1<attempts:
                time.sleep(0.8*(i+1))
    raise last


def cdx_url(prefix):
    params=[
        ("url",prefix),
        ("matchType","prefix"),
        ("from",FROM),
        ("to",TO),
        ("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length"),
        ("filter","statuscode:200"),
        ("collapse","urlkey"),
        ("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def parse_response(body):
    text=body.decode("utf-8","replace").strip()
    if not text:
        return []
    data=json.loads(text)
    if not isinstance(data,list) or not data:
        return []
    header=data[0]
    if not isinstance(header,list):
        return []
    out=[]
    for row in data[1:]:
        if not isinstance(row,list):
            continue
        item={str(header[i]):str(row[i]) if i<len(row) else "" for i in range(len(header))}
        out.append(item)
    return out


def relevant(row):
    original=row.get("original","")
    path=urllib.parse.urlsplit(original).path
    query=urllib.parse.urlsplit(original).query
    tail=(path.rsplit("/",1)[-1]+"?"+query).strip("?")
    return bool(INTEREST.search(tail))


def one(target):
    label,prefix=target
    try:
        rows=parse_response(get(cdx_url(prefix)))
        return label,prefix,rows,None
    except Exception as exc:
        return label,prefix,[],(type(exc).__name__,str(exc))


def main():
    print("StoneAge Korean distribution-directory Wayback CDX enumeration — R1")
    print("SCOPE|cdx-metadata-only|no-archived-payload-download")
    print(f"WINDOW|from={FROM}|to={TO}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results=list(ex.map(one,TARGETS))

    errors=[]
    all_rows=[]
    for label,prefix,rows,error in results:
        if error:
            errors.append((label,prefix,error[0],error[1]))
            print(
                f"PREFIX|label={clean(label)}|url={clean(prefix)}|status=error|"
                f"rows=0|relevant=0"
            )
            continue
        rel=[r for r in rows if relevant(r)]
        print(
            f"PREFIX|label={clean(label)}|url={clean(prefix)}|status=ok|"
            f"rows={len(rows)}|relevant={len(rel)}"
        )
        for row in rows:
            all_rows.append((label,prefix,row,relevant(row)))

    print(f"COUNT|queries|{len(TARGETS)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|rows|{len(all_rows)}")
    print(f"COUNT|relevant_rows|{sum(int(x[3]) for x in all_rows)}")
    print(f"COUNT|unique_urls|{len(set(x[2].get('original','') for x in all_rows))}")

    for label,prefix,kind,msg in errors:
        print(
            f"ERROR|label={clean(label)}|url={clean(prefix)}|kind={clean(kind)}|"
            f"message={clean(msg)}"
        )

    for label,prefix,row,is_rel in sorted(
        all_rows,
        key=lambda x:(not x[3],x[0],x[2].get("original",""),x[2].get("timestamp","")),
    ):
        marker="HIT" if is_rel else "ROW"
        print(
            f"{marker}|label={clean(label)}|timestamp={clean(row.get('timestamp'))}|"
            f"url={clean(row.get('original'))}|mime={clean(row.get('mimetype'))}|"
            f"status={clean(row.get('statuscode'))}|digest={clean(row.get('digest'))}|"
            f"length={clean(row.get('length'))}"
        )


if __name__=="__main__":
    main()
