#!/usr/bin/env python3
"""Probe Wayback prefix/stem variants for evidence-derived 21CN sa25up URLs.

This closes normalization/suffix ambiguity such as the literal trailing space in the
2002-10-17 21CN downit JavaScript. CDX metadata only; no historical payload replay.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"

STEMS=(
    ("images-2002","http://images.21cn.com/download/file/game/maoxian/sa25up"),
    ("download-file","http://download.21cn.com/file/game/maoxian/sa25up"),
    ("download-file1","http://download.21cn.com/file1/game/maoxian/sa25up"),
    ("dg-file1","http://dg.download.21cn.com/file1/game/maoxian/sa25up"),
    ("dg-file1-21cn","http://dg.download.21cn.com/file1_21cn/game/maoxian/sa25up"),
    ("dg-file1xjy","http://dg.download.21cn.com/file1xjy/game/maoxian/sa25up"),
    ("dg-file1xzm","http://dg.download.21cn.com/file1xzm/game/maoxian/sa25up"),
)


def clean(v,limit=2600):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def query_url(stem):
    params=[
        ("url",stem),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2002"),("to","2006"),("limit","1000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def fetch(url,timeout=25,max_bytes=3_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),body


def parse(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))


def one(entry):
    label,stem=entry
    try:
        st,final,body=fetch(query_url(stem),30)
        return label,stem,st,final,body,parse(body),None
    except Exception as exc:
        return label,stem,None,None,None,(),(type(exc).__name__,str(exc))


def main():
    print("StoneAge 2.5 21CN sa25up prefix/normalization probe — R1")
    print("SCOPE|evidence-derived-stems|wayback-cdx-prefix-only|no-payload-replay")
    errors=[]; rows_total=0; rows_200=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
        for label,stem,st,final,body,rows,error in ex.map(one,STEMS):
            if error:
                errors.append((label,error[0],error[1]))
                continue
            print(
                f"QUERY|label={label}|stem={clean(stem)}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            rows_total+=len(rows)
            for row in rows:
                ok=str(row.get("statuscode") or "")=="200"
                if ok:
                    rows_200+=1
                original=str(row.get("original") or "")
                tail=original[len(stem):] if original.startswith(stem) else ""
                print(
                    f"ROW|label={label}|timestamp={clean(row.get('timestamp'))}|original={clean(original)}|"
                    f"suffix={clean(tail)}|status={clean(row.get('statuscode'))}|"
                    f"mime={clean(row.get('mimetype'))}|length={clean(row.get('length'))}|"
                    f"digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}"
                )
    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|stems|{len(STEMS)}")
    print(f"COUNT|rows|{rows_total}")
    print(f"COUNT|http200_rows|{rows_200}")
    print(f"COUNT|errors|{len(errors)}")
    if rows_200:
        print("RESOLUTION|PREFIX_HTTP200_CANDIDATE_FOUND|inspect only evidence-derived 200 rows and recover transient bytes if ZIP-sized")
    elif errors:
        print("RESOLUTION|PARTIAL_PREFIX_FAILURE_WITH_NO_HTTP200|retry only failed stems")
    else:
        print("RESOLUTION|NO_HTTP200_SA25UP_PREFIX_VARIANT|known 21CN stem/normalization surface bounded")
    print(
        "EVIDENCE_BOUNDARY|prefix rows can expose encoded spaces or crawler-normalized suffixes; "
        "non-200 rows do not establish payload preservation."
    )


if __name__=="__main__":
    main()
