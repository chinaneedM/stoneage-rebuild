#!/usr/bin/env python3
"""Probe archival indexes for the China.com Dec-2000 StoneAge test-CD activity trail.

The surviving China.com giveaway page links/points into an older news namespace
whose high-value exact token is article 63271 on 2000-12-20. This probe searches
Wayback and Arquivo.pt index metadata only. No archived page body or binary is
downloaded.

The goal is to recover:
- exact captures of the 63271 article URL under plausible China.com hosts;
- same-day neighboring URLs under the 20001220 directory;
- captures of the surviving StoneAge legacy activity/product/news pages as
  topology controls.
"""
from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
WAYBACK="https://web.archive.org/cdx/search/cdx"
ARQUIVO="https://arquivo.pt/wayback/cdx"

EXACT_TARGETS=(
    ("china-63271-game-http","http://game.china.com/zh_cn/news/news1/444/20001220/63271.html"),
    ("china-63271-game-https","https://game.china.com/zh_cn/news/news1/444/20001220/63271.html"),
    ("china-63271-www-http","http://www.china.com/zh_cn/news/news1/444/20001220/63271.html"),
    ("china-63271-bare-http","http://china.com/zh_cn/news/news1/444/20001220/63271.html"),
    ("legacy-answer-http","http://game.china.com/hotspot/shiqi/answer/index.html"),
    ("legacy-news1-http","http://game.china.com/hotspot/shiqi/news/1.html"),
    ("legacy-news2-http","http://game.china.com/hotspot/shiqi/news/2.html"),
)

PREFIX_TARGETS=(
    ("china-game-20001220","http://game.china.com/zh_cn/news/news1/444/20001220/"),
    ("china-www-20001220","http://www.china.com/zh_cn/news/news1/444/20001220/"),
    ("china-bare-20001220","http://china.com/zh_cn/news/news1/444/20001220/"),
)

def clean(v,n=4000):
    return " ".join(str(v or "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=55,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/plain,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes)
        return int(getattr(r,"status",r.getcode())),r.geturl(),body

def wb_url(original,match_type):
    params=[
        ("url",original),
        ("matchType",match_type),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2000"),
        ("to","2003"),
        ("filter","statuscode:200"),
        ("limit","500"),
    ]
    return WAYBACK+"?"+urllib.parse.urlencode(params)

def arquivo_url(original):
    params={
        "url":original,
        "from":"2000",
        "to":"2003",
        "limit":"500",
        "output":"json",
    }
    return ARQUIVO+"?"+urllib.parse.urlencode(params)

def parse_rows(body):
    text=body.decode("utf-8","replace").strip()
    if not text:
        return ()
    try:
        obj=json.loads(text)
    except json.JSONDecodeError:
        rows=[]
        for line in text.splitlines():
            line=line.strip()
            if not line:
                continue
            brace=line.find("{")
            if brace>0:
                line=line[brace:]
            try:
                x=json.loads(line)
            except Exception:
                continue
            if isinstance(x,dict):
                rows.append(x)
        return tuple(rows)
    if isinstance(obj,list):
        if obj and isinstance(obj[0],list):
            header=obj[0]
            return tuple(dict(zip(header,row)) for row in obj[1:] if isinstance(row,list))
        return tuple(x for x in obj if isinstance(x,dict))
    if isinstance(obj,dict):
        for key in ("results","captures","response","items"):
            val=obj.get(key)
            if isinstance(val,list):
                return tuple(x for x in val if isinstance(x,dict))
        if any(k in obj for k in ("url","original","timestamp")):
            return (obj,)
    return ()

def norm(row):
    return {
        "timestamp":row.get("timestamp") or row.get("date") or row.get("datetime") or "",
        "original":row.get("original") or row.get("url") or row.get("originalURL") or "",
        "status":row.get("statuscode") or row.get("status") or "",
        "mime":row.get("mimetype") or row.get("mime") or row.get("mimeType") or "",
        "digest":row.get("digest") or "",
        "length":row.get("length") or row.get("contentLength") or "",
        "redirect":row.get("redirect") or "",
        "filename":row.get("filename") or "",
        "offset":row.get("offset") or "",
        "collection":row.get("collection") or "",
    }

def article_id(url):
    p=urllib.parse.urlsplit(str(url or "")).path
    base=p.rsplit("/",1)[-1]
    if base.endswith(".html"):
        base=base[:-5]
    return base if base.isdigit() else ""

def main():
    print("StoneAge China.com Dec-2000 test-CD legacy archive probe — R1")
    print("SCOPE|Wayback+Arquivo CDX metadata only|exact article+same-day prefix+legacy controls|no archived-body|no payload")
    errors=[]
    emitted=set()
    exact_63271=0
    prefix_rows=0
    neighbor_ids=set()

    for label,original in EXACT_TARGETS:
        for source,url in (
            ("wayback",wb_url(original,"exact")),
            ("arquivo",arquivo_url(original)),
        ):
            try:
                st,final,body=fetch(url)
                rows=parse_rows(body)
                print(f"QUERY|source={source}|kind=exact|label={label}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}")
                for raw in rows:
                    r=norm(raw)
                    key=(source,label,clean(r["timestamp"]),clean(r["original"]),clean(r["status"]),clean(r["digest"]))
                    if key in emitted:
                        continue
                    emitted.add(key)
                    aid=article_id(r["original"])
                    if "63271"==aid:
                        exact_63271+=1
                    print("RESULT|source={}|kind=exact|label={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|article_id={}|original={}|filename={}|offset={}|collection={}".format(
                        source,label,clean(r["timestamp"]),clean(r["status"]),clean(r["mime"]),clean(r["length"]),
                        clean(r["digest"]),clean(r["redirect"]),clean(aid),clean(r["original"]),clean(r["filename"]),
                        clean(r["offset"]),clean(r["collection"])
                    ))
            except Exception as e:
                errors.append((source,"exact",label,type(e).__name__,str(e)))

    for label,prefix in PREFIX_TARGETS:
        try:
            st,final,body=fetch(wb_url(prefix,"prefix"))
            rows=parse_rows(body)
            print(f"QUERY|source=wayback|kind=prefix|label={label}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}")
            for raw in rows:
                r=norm(raw); prefix_rows+=1
                aid=article_id(r["original"])
                if aid:
                    neighbor_ids.add(aid)
                print("PREFIX_RESULT|label={}|timestamp={}|status={}|mime={}|length={}|digest={}|article_id={}|original={}".format(
                    label,clean(r["timestamp"]),clean(r["status"]),clean(r["mime"]),clean(r["length"]),
                    clean(r["digest"]),clean(aid),clean(r["original"])
                ))
        except Exception as e:
            errors.append(("wayback","prefix",label,type(e).__name__,str(e)))

    for source,kind,label,ename,msg in errors:
        print(f"ERROR|source={clean(source)}|kind={clean(kind)}|label={clean(label)}|error={clean(ename)}|message={clean(msg)}")
    print(f"COUNT|exact_targets|{len(EXACT_TARGETS)}")
    print(f"COUNT|prefix_targets|{len(PREFIX_TARGETS)}")
    print(f"COUNT|exact_63271_rows|{exact_63271}")
    print(f"COUNT|prefix_rows|{prefix_rows}")
    print(f"COUNT|neighbor_article_ids|{len(neighbor_ids)}")
    if neighbor_ids:
        print("NEIGHBOR_IDS|"+",".join(sorted(neighbor_ids,key=lambda x:int(x))[:500]))
    print(f"COUNT|errors|{len(errors)}")

    if exact_63271:
        print("RESOLUTION|EXACT_63271_CAPTURE_FOUND|next recover archived article body as small HTML evidence")
    elif prefix_rows:
        print("RESOLUTION|SAME_DAY_NEIGHBORHOOD_FOUND_NO_EXACT_63271|inspect neighboring titles/URLs and alternate host topology")
    elif errors:
        print("RESOLUTION|PARTIAL_ARCHIVE_PROBE|retry only failed archive surfaces")
    else:
        print("RESOLUTION|NO_ARCHIVE_INDEX_ROWS|exact 63271 and tested same-day prefixes expose no CDX records")
    print("EVIDENCE_BOUNDARY|CDX capture metadata proves archival existence/topology only; article meaning requires body replay and independent source classification.")

if __name__=="__main__":
    main()
