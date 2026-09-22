#!/usr/bin/env python3
"""Resolve the 1999 StoneAge beta application URL without guessing OCR.

The printed Play Online URL is known to use the Gamer's Dream host and end in
PO/sa_apply.html, but one character immediately before PO remains ambiguous.
This probe asks public archive indexes for wildcard matches and records only
index metadata. It never normalizes the ambiguous character or downloads an
archived page body.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
WAYBACK_CDX="https://web.archive.org/cdx/search/cdx"
ARQUIVO_CDX="https://arquivo.pt/wayback/cdx"
YEAR="1999"

PATTERNS=(
    ("www-dp-tail","www.dp.gamersdream.ne.jp/*PO/sa_apply.html"),
    ("dp-tail","dp.gamersdream.ne.jp/*PO/sa_apply.html"),
    ("www-dp-file","www.dp.gamersdream.ne.jp/*sa_apply.html"),
    ("dp-file","dp.gamersdream.ne.jp/*sa_apply.html"),
)


def request(url,*,timeout=12):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return response.read()


def parse_wayback(data):
    obj=json.loads(data.decode("utf-8","replace"))
    if not isinstance(obj,list) or not obj:
        return []
    header=obj[0]
    if not isinstance(header,list):
        return []
    out=[]
    for row in obj[1:]:
        if not isinstance(row,list):
            continue
        out.append({
            str(header[i]):str(row[i]) if i < len(row) else ""
            for i in range(len(header))
        })
    return out


def parse_arquivo(data):
    text=data.decode("utf-8","replace").strip()
    if not text:
        return []
    try:
        obj=json.loads(text)
    except json.JSONDecodeError:
        out=[]
        for line in text.splitlines():
            line=line.strip()
            if not line:
                continue
            brace=line.find("{")
            if brace > 0:
                line=line[brace:]
            try:
                item=json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item,dict):
                out.append(item)
        return out
    if isinstance(obj,list):
        if obj and isinstance(obj[0],list):
            header=obj[0]
            return [
                {str(header[i]):str(row[i]) if i < len(row) else "" for i in range(len(header))}
                for row in obj[1:]
                if isinstance(row,list)
            ]
        return [item for item in obj if isinstance(item,dict)]
    if isinstance(obj,dict):
        for key in ("results","captures","response","items"):
            value=obj.get(key)
            if isinstance(value,list):
                return [item for item in value if isinstance(item,dict)]
        if any(key in obj for key in ("url","original","timestamp")):
            return [obj]
    return []


def wayback_url(pattern):
    params=[
        ("url",pattern),
        ("from",YEAR),
        ("to",YEAR),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("filter","statuscode:200"),
        ("limit","500"),
        ("collapse","urlkey"),
    ]
    return WAYBACK_CDX+"?"+urllib.parse.urlencode(params)


def arquivo_url(pattern):
    params=[
        ("url",pattern),
        ("from",YEAR),
        ("to",YEAR),
        ("output","json"),
        ("fields","timestamp,url,status,mime,digest,length"),
        ("filter","=status:200"),
        ("limit","500"),
    ]
    return ARQUIVO_CDX+"?"+urllib.parse.urlencode(params)


def normalize(row):
    return {
        "timestamp":str(row.get("timestamp") or row.get("date") or ""),
        "original":str(row.get("original") or row.get("url") or ""),
        "status":str(row.get("statuscode") or row.get("status") or ""),
        "mime":str(row.get("mimetype") or row.get("mime") or ""),
        "digest":str(row.get("digest") or ""),
        "length":str(row.get("length") or ""),
    }


def candidate_detail(original):
    """Describe only literal archive-returned path characters."""
    value=str(original or "")
    try:
        path=urllib.parse.urlsplit(value).path
    except ValueError:
        path=""
    tail="PO/sa_apply.html"
    if not path.endswith(tail):
        return {
            "matches_tail":False,
            "path":path,
            "prefix_before_po":"",
            "immediate_before_po":"",
        }
    prefix=path[:-len(tail)]
    return {
        "matches_tail":True,
        "path":path,
        "prefix_before_po":prefix,
        "immediate_before_po":prefix[-1:] if prefix else "",
    }


def clean(value,limit=900):
    value=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f").replace("|","%7C")[:limit]


def main():
    print("StoneAge 1999 beta application wildcard archive probe — R1")
    print("SCOPE|cdx-index-metadata-only|no-page-body|no-url-character-normalization")
    print("YEAR|1999")
    print("KNOWN|host=www.dp.gamersdream.ne.jp|tail=PO/sa_apply.html|preceding-character=OPEN")

    results=[]
    errors=[]
    success=0
    for backend,url_builder,parser in (
        ("wayback",wayback_url,parse_wayback),
        ("arquivo",arquivo_url,parse_arquivo),
    ):
        for label,pattern in PATTERNS:
            endpoint=url_builder(pattern)
            try:
                rows=parser(request(endpoint))
                success+=1
            except Exception as exc:
                errors.append((backend,label,pattern,type(exc).__name__,str(exc)))
                continue
            print(
                f"QUERY|backend={backend}|label={label}|rows={len(rows)}|"
                f"pattern={clean(pattern)}"
            )
            for row in rows:
                normalized=normalize(row)
                detail=candidate_detail(normalized["original"])
                if detail["matches_tail"]:
                    results.append((backend,label,normalized,detail))

    emitted={}
    for backend,label,row,detail in results:
        key=(row["timestamp"],row["original"],row["digest"])
        emitted.setdefault(key,(backend,label,row,detail))

    print(f"COUNT|queries_succeeded|{success}")
    print(f"COUNT|queries_failed|{len(errors)}")
    print(f"COUNT|tail_matches|{len(emitted)}")
    for backend,label,pattern,kind,message in sorted(errors):
        print(
            f"ERROR|backend={backend}|label={label}|kind={clean(kind)}|"
            f"pattern={clean(pattern)}|message={clean(message)}"
        )
    for _,(backend,label,row,detail) in sorted(emitted.items()):
        print(
            "RESULT|"
            f"backend={backend}|label={label}|timestamp={clean(row['timestamp'])}|"
            f"status={clean(row['status'])}|mime={clean(row['mime'])}|"
            f"length={clean(row['length'])}|digest={clean(row['digest'])}|"
            f"original={clean(row['original'])}|path={clean(detail['path'])}|"
            f"prefix_before_po={clean(detail['prefix_before_po'])}|"
            f"immediate_before_po={clean(detail['immediate_before_po'])}"
        )

    if emitted:
        print("RESOLUTION|ARCHIVE_URL_FOUND|use literal RESULT original/path; do not reinterpret")
    elif success:
        print("RESOLUTION|BOUNDED_NO_MATCH|ambiguous character remains OPEN")
    else:
        print("RESOLUTION|INCONCLUSIVE|all archive index queries failed")


if __name__=="__main__":
    main()
