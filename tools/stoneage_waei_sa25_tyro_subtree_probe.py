#!/usr/bin/env python3
"""Probe the archived Beijing-Waei StoneAge2 tyro subtree for 2.5 upgrade artifacts.

The official Feb-2002 rollout pages link to /ZHUANQU/stoneage2/tyro/upgrade.asp.
The exact target is poorly preserved. This probe therefore inspects the grounded
sibling subtree at CDX metadata level, including non-200 statuses, to recover
adjacent filenames, redirect-like variants and downloadable artifacts without
fetching any binary payload.
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
    ("www-upper","http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/"),
    ("www-lower","http://www.waei.com.cn/zhuanqu/stoneage2/tyro/"),
    ("bare-lower","http://waei.com.cn/zhuanqu/stoneage2/tyro/"),
)
DATE_FROM="20020101"
DATE_TO="20020630"
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".msi",".001",".002",".vcd",".iso")
HINTS=("upgrade","update","patch","setup","install","download","down","client","full","2.5","25","sa25","stoneage")

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
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",DATE_FROM),("to",DATE_TO),
        ("collapse","urlkey"),("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse_cdx(body):
    data=json.loads(body.decode("utf-8"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))

def score(row):
    original=urllib.parse.unquote_plus(str(row.get("original") or "")).lower()
    redirect=urllib.parse.unquote_plus(str(row.get("redirect") or "")).lower()
    mime=str(row.get("mimetype") or "").lower()
    blob=original+" "+redirect+" "+mime
    n=sum(2 for hint in HINTS if hint in blob)
    if any(re.search(re.escape(ext)+r"(?:$|[?#])",original) for ext in PAYLOAD_EXTS):
        n+=10
    if any(re.search(re.escape(ext)+r"(?:$|[?#])",redirect) for ext in PAYLOAD_EXTS):
        n+=12
    status=str(row.get("statuscode") or "")
    if status.startswith("3") and redirect:
        n+=6
    if original.endswith("/upgrade.asp") or "upgrade.asp?" in original:
        n+=8
    return n

def main():
    print("StoneAge Beijing-Waei StoneAge2 tyro-subtree probe — R1")
    print("SCOPE|official-tyro-prefix|2002-H1|CDX-all-status+redirect-metadata|no-payload-download")
    print(f"TARGET|from={DATE_FROM}|to={DATE_TO}|prefixes={len(PREFIXES)}")

    errors=[]
    rows_by_key={}
    for label,prefix in PREFIXES:
        try:
            u=cdx_url(prefix)
            status,final,body=fetch_bytes(u)
            rows=parse_cdx(body)
            print(
                f"CDX|label={label}|prefix={clean(prefix)}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for row in rows:
                key=(
                    str(row.get("timestamp") or ""),
                    str(row.get("original") or ""),
                    str(row.get("statuscode") or ""),
                    str(row.get("redirect") or ""),
                )
                rows_by_key[key]=row
        except Exception as exc:
            errors.append((label,type(exc).__name__,str(exc)))

    ranked=sorted(rows_by_key.values(),key=lambda r:(-score(r),str(r.get("original") or "")))
    relevant=[row for row in ranked if score(row)>0]
    strong=[row for row in ranked if score(row)>=8]

    for row in relevant[:500]:
        print(
            f"ROW|score={score(row)}|timestamp={clean(row.get('timestamp'))}|"
            f"original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|"
            f"mimetype={clean(row.get('mimetype'))}|redirect={clean(row.get('redirect'))}|"
            f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
        )

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|unique_rows|{len(rows_by_key)}")
    print(f"COUNT|relevant_rows|{len(relevant)}")
    print(f"COUNT|strong_rows|{len(strong)}")
    print(f"COUNT|errors|{len(errors)}")
    if strong:
        print("RESOLUTION|TYRO_STRONG_ARTIFACT_ROWS_FOUND|replay only HTML/redirect candidates and classify exact payload URLs next")
    elif relevant:
        print("RESOLUTION|TYRO_RELATED_ROWS_FOUND|inspect neighboring page names before broadening archive scope")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|one or more official tyro archive prefixes unavailable")
    else:
        print("RESOLUTION|NO_TYRO_ARCHIVE_ROWS|bounded official tyro subtree has no indexed upgrade artifact")

if __name__=="__main__":
    main()
