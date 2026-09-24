#!/usr/bin/env python3
"""Probe the archived Beijing Waei StoneAge2 subtree for 2.5 payload filenames.

The official Jan-Mar 2002 archive surface independently exposes
/ZHUANQU/stoneage2/. This probe works at CDX metadata level first, prioritizing
binary/archive filenames and download/update/setup semantics. It does not
download any candidate client payload.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIXES=(
    ("www-upper","http://www.waei.com.cn/ZHUANQU/stoneage2/"),
    ("www-lower","http://www.waei.com.cn/zhuanqu/stoneage2/"),
    ("bare-lower","http://waei.com.cn/zhuanqu/stoneage2/"),
)
DATE_FROM="20020115"
DATE_TO="20020315"
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".001",".002",".vcd",".iso",".msi")
NAME_HINTS=("download","down","update","upgrade","patch","setup","install","client","full","25","2.5","sa25","stoneage")
MIME_HINTS=("octet-stream","zip","x-msdownload","x-zip","rar","cab")

def clean(value,limit=2400):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch_bytes(url,timeout=45):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),body

def cdx_url(prefix):
    params=[
        ("url",prefix),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from",DATE_FROM),("to",DATE_TO),("filter","statuscode:200"),
        ("collapse","urlkey"),("limit","10000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse_cdx(body):
    data=json.loads(body.decode("utf-8"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))

def candidate_score(row):
    original=urllib.parse.unquote_plus(str(row.get("original") or "")).lower()
    mime=str(row.get("mimetype") or "").lower()
    score=0
    if any(re.search(re.escape(ext)+r"(?:$|[?#])",original) for ext in PAYLOAD_EXTS):
        score+=8
    score+=sum(2 for hint in NAME_HINTS if hint in original)
    score+=sum(3 for hint in MIME_HINTS if hint in mime)
    if "/qqskin/" in original or "/img/" in original:
        score-=8
    if any(token in original for token in ("/service/","/hotline/","/map/img/")):
        score-=3
    return score

def main():
    print("StoneAge Beijing-Waei StoneAge2 payload-index probe — R1")
    print("SCOPE|official-stoneage2-CDX|2002-01-15..2002-03-15|payload-filename-metadata-only|no-payload-download")
    print(f"TARGET|from={DATE_FROM}|to={DATE_TO}|prefixes={len(PREFIXES)}")

    errors=[]
    all_rows={}
    for label,prefix in PREFIXES:
        try:
            url=cdx_url(prefix)
            status,final,body=fetch_bytes(url)
            rows=parse_cdx(body)
            print(
                f"CDX|label={label}|prefix={clean(prefix)}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for row in rows:
                key=(str(row.get("timestamp") or ""),str(row.get("original") or ""))
                all_rows[key]=row
        except Exception as exc:
            errors.append((label,type(exc).__name__,str(exc)))

    ranked=sorted(
        all_rows.values(),
        key=lambda row:(-candidate_score(row),str(row.get("original") or "")),
    )
    candidates=[row for row in ranked if candidate_score(row)>0]
    strong=[row for row in ranked if candidate_score(row)>=8]

    for row in candidates[:500]:
        print(
            f"CANDIDATE|score={candidate_score(row)}|timestamp={clean(row.get('timestamp'))}|"
            f"original={clean(row.get('original'))}|mimetype={clean(row.get('mimetype'))}|"
            f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
        )

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|unique_rows|{len(all_rows)}")
    print(f"COUNT|candidates|{len(candidates)}")
    print(f"COUNT|strong_payload_candidates|{len(strong)}")
    print(f"COUNT|errors|{len(errors)}")
    if strong:
        print("RESOLUTION|STONEAGE2_PAYLOAD_INDEX_CANDIDATES_FOUND|classify exact candidate filenames before any transient recovery")
    elif candidates:
        print("RESOLUTION|STONEAGE2_DOWNLOAD_PAGE_CANDIDATES_FOUND|replay only the high-score candidate pages to recover payload hrefs")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|one or more official StoneAge2 archive prefixes unavailable")
    else:
        print("RESOLUTION|NO_STONEAGE2_PAYLOAD_INDEX_HIT|bounded official CDX surface contains no payload-like filename")

if __name__=="__main__":
    main()
