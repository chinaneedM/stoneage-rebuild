#!/usr/bin/env python3
"""Probe oldest Common Crawl CDXJ indexes for exact StoneAge Korean payload URLs.

Metadata only. No WARC records or payload bytes are downloaded.
"""

from __future__ import annotations
import json
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
COLLINFO="https://index.commoncrawl.org/collinfo.json"
TARGETS=[
 ("hananet-formal","http://stoneage.hananet.net/down/sa.exe"),
 ("hananet-trial","http://stoneage.hananet.net/down/sa_demo.exe"),
 ("cnet-zip","http://korea.cnet.com/pc/games/online/stoneage.zip"),
 ("gagamel-zip","http://www.gagamel.com/web_data/download/stoneagebeta.zip"),
 ("hananet-pds","http://pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"),
]

def fetch(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()

def collections(limit=8):
    rows=json.loads(fetch(COLLINFO,20).decode("utf-8","replace"))
    ids=[str(x.get("id","")) for x in rows if x.get("id")]
    # collinfo is normally newest-first; oldest indexes are the most useful here.
    return list(reversed(ids))[:limit]

def query(index_id,url):
    endpoint=f"https://index.commoncrawl.org/{index_id}-index?"
    params=urllib.parse.urlencode({"url":url,"output":"json","filter":"status:200"})
    text=fetch(endpoint+params,15).decode("utf-8","replace").strip()
    out=[]
    for line in text.splitlines():
        line=line.strip()
        if not line:continue
        try:item=json.loads(line)
        except json.JSONDecodeError:continue
        if isinstance(item,dict):out.append(item)
    return out

def clean(v,limit=800):
    v=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def main():
    print("StoneAge exact-payload Common Crawl index probe — R1")
    print("SCOPE|cdxj-metadata-only|no-warc-download|no-client-binary-download")
    try:indexes=collections()
    except Exception as exc:
        print(f"FATAL|collinfo|{type(exc).__name__}|{clean(exc)}");return
    print("INDEXES|" + ",".join(indexes))
    print(f"COUNT|indexes|{len(indexes)}")
    print(f"COUNT|targets|{len(TARGETS)}")

    results=[]; errors=[]
    for index_id in indexes:
        for label,url in TARGETS:
            try:rows=query(index_id,url)
            except Exception as exc:
                errors.append((index_id,label,url,type(exc).__name__,str(exc)))
            else:
                for row in rows:results.append((index_id,label,url,row))
            time.sleep(0.7)

    print(f"COUNT|queries|{len(indexes)*len(TARGETS)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|raw_results|{len(results)}")
    for index_id,label,url,kind,msg in errors:
        print(f"ERROR|index={clean(index_id)}|target={clean(label)}|kind={clean(kind)}|url={clean(url)}|message={clean(msg)}")
    emitted=set()
    for index_id,label,url,row in results:
        rec=(
          clean(index_id),clean(label),clean(row.get("timestamp")),clean(row.get("status")),
          clean(row.get("mime")),clean(row.get("mime-detected")),clean(row.get("digest")),
          clean(row.get("length")),clean(row.get("filename")),clean(row.get("offset")),
          clean(row.get("url") or url),
        )
        emitted.add(rec)
    print(f"COUNT|unique_results|{len(emitted)}")
    for rec in sorted(emitted):print("RESULT|"+"|".join(rec))

if __name__=="__main__":main()
