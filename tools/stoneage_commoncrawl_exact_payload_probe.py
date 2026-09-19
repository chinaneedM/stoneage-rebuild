#!/usr/bin/env python3
"""Probe Common Crawl indexes for exact and nearby StoneAge Korean mirror URLs.

Metadata only. No WARC records or payload bytes are downloaded.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
COLLINFO="https://index.commoncrawl.org/collinfo.json"

EXACT_TARGETS=[
    ("hananet-formal","http://stoneage.hananet.net/down/sa.exe"),
    ("hananet-trial","http://stoneage.hananet.net/down/sa_demo.exe"),
    ("cnet-zip","http://korea.cnet.com/pc/games/online/stoneage.zip"),
    ("gagamel-zip","http://www.gagamel.com/web_data/download/stoneagebeta.zip"),
    ("hananet-pds","http://pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"),
    ("gametime-gw9","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
]

PREFIX_TARGETS=[
    ("hananet-down-prefix","http://stoneage.hananet.net/down/"),
    ("cnet-online-prefix","http://korea.cnet.com/pc/games/online/"),
    ("gagamel-download-prefix","http://www.gagamel.com/web_data/download/"),
    ("gametime-data-prefix","http://www.gametime.co.kr/data/"),
    ("hananet-pds-prefix","http://pds.hananet.net/view.asp"),
]

RELEVANT=re.compile(
    r"(?i)(stoneage|sa_demo\.exe|(?:^|/)sa\.exe|stoneagebeta\.zip|"
    r"20001031524596220|gw_idx=9|gw_name=online)"
)


def fetch(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.read()


def collections(limit=8):
    rows=json.loads(fetch(COLLINFO,20).decode("utf-8","replace"))
    entries=[]
    for row in rows:
        index_id=str(row.get("id","")).strip()
        api=str(row.get("cdx-api","") or row.get("cdx_api","")).strip()
        if index_id and api:
            entries.append((index_id,api))
    return list(reversed(entries))[:limit]


def query_url(api,url,match_type="exact"):
    separator="&" if "?" in api else "?"
    params={
        "url":url,
        "output":"json",
        "filter":"status:200",
    }
    if match_type!="exact":
        params["matchType"]=match_type
        params["limit"]="100"
    return api+separator+urllib.parse.urlencode(params)


def query(api,url,match_type="exact"):
    endpoint=query_url(api,url,match_type)
    try:
        data=fetch(endpoint,15)
    except urllib.error.HTTPError as exc:
        if exc.code==404:
            return []
        raise
    text=data.decode("utf-8","replace").strip()
    out=[]
    for line in text.splitlines():
        line=line.strip()
        if not line:
            continue
        try:
            item=json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item,dict):
            out.append(item)
    return out


def is_relevant(url):
    return bool(RELEVANT.search(str(url or "")))


def clean(v,limit=800):
    v=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def record(index_id,label,mode,target,row):
    return (
        clean(index_id),clean(label),clean(mode),clean(row.get("timestamp")),
        clean(row.get("status")),clean(row.get("mime")),clean(row.get("mime-detected")),
        clean(row.get("digest")),clean(row.get("length")),clean(row.get("filename")),
        clean(row.get("offset")),clean(row.get("url") or target),
    )


def main():
    print("StoneAge Common Crawl mirror-neighborhood probe — R2")
    print("SCOPE|cdxj-metadata-only|no-warc-download|no-client-binary-download")
    print("METHOD|exact-targets+prefix-neighborhoods|404-means-no-index-match")
    try:
        indexes=collections()
    except Exception as exc:
        print(f"FATAL|collinfo|{type(exc).__name__}|{clean(exc)}")
        return

    print("INDEXES|" + ",".join(index_id for index_id,_ in indexes))
    print(f"COUNT|indexes|{len(indexes)}")
    print(f"COUNT|exact_targets|{len(EXACT_TARGETS)}")
    print(f"COUNT|prefix_targets|{len(PREFIX_TARGETS)}")

    exact_results=[]
    prefix_rows=[]
    errors=[]
    for index_id,api in indexes:
        for label,url in EXACT_TARGETS:
            try:
                rows=query(api,url,"exact")
            except Exception as exc:
                errors.append((index_id,label,"exact",url,type(exc).__name__,str(exc)))
            else:
                for row in rows:
                    exact_results.append(record(index_id,label,"exact",url,row))
            time.sleep(0.35)
        for label,url in PREFIX_TARGETS:
            try:
                rows=query(api,url,"prefix")
            except Exception as exc:
                errors.append((index_id,label,"prefix",url,type(exc).__name__,str(exc)))
            else:
                for row in rows:
                    prefix_rows.append((index_id,label,url,row))
            time.sleep(0.35)

    relevant_prefix=[]
    for index_id,label,target,row in prefix_rows:
        if is_relevant(row.get("url") or target):
            relevant_prefix.append(record(index_id,label,"prefix",target,row))

    print(f"COUNT|queries|{len(indexes)*(len(EXACT_TARGETS)+len(PREFIX_TARGETS))}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|exact_raw_results|{len(exact_results)}")
    print(f"COUNT|prefix_raw_results|{len(prefix_rows)}")
    print(f"COUNT|prefix_relevant_results|{len(relevant_prefix)}")

    for index_id,label,mode,url,kind,msg in errors:
        print(
            f"ERROR|index={clean(index_id)}|target={clean(label)}|mode={mode}|kind={clean(kind)}|"
            f"url={clean(url)}|message={clean(msg)}"
        )

    emitted=set(exact_results+relevant_prefix)
    print(f"COUNT|unique_relevant_results|{len(emitted)}")
    for rec in sorted(emitted):
        print("RESULT|"+"|".join(rec))


if __name__=="__main__":
    main()
