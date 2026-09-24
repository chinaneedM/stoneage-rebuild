#!/usr/bin/env python3
"""Scan archived 21CN software-detail pages for a StoneAge 2.5 catalogue record.

Historical IP 202.104.32.168 is already identified as 21CN.COM download infrastructure.
This probe queries Wayback CDX for archived list.php?id=... HTML records and transiently
replays only those small HTML pages. It emits match metadata/context only and never
fetches any linked game/download payload.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

from tools.stoneage_sa25_host_identity_probe import (
    clean,
    decode,
    declared_charset,
    title,
    visible,
)

UA="stoneage-rebuild-archaeology/1.0"
HOST="202.104.32.168"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX=f"http://{HOST}/list.php"

TOKENS=(
    "石器时代",
    "石器時代",
    "精灵王传说",
    "精靈王傳說",
    "精灵王",
    "精靈王",
    "sa25up.zip",
    "stoneage",
    "stone age",
)
HREF_RE=re.compile(r"""(?is)href\s*=\s*["']?([^"'\s>]+)""")


def cdx_url():
    p=[
        ("url",PREFIX),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from","2001"),("to","2004"),("filter","statuscode:200"),
        ("filter","mimetype:text/html"),("collapse","urlkey"),("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def fetch_bytes(url,timeout=40,max_bytes=8_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),body


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    rows=[]
    seen=set()
    for row in data[1:]:
        if not isinstance(row,list):
            continue
        item=dict(zip(header,row))
        original=str(item.get("original") or "")
        p=urllib.parse.urlsplit(original)
        if p.path.lower()!="/list.php":
            continue
        q=urllib.parse.parse_qs(p.query)
        if "id" not in q:
            continue
        key=original
        if key in seen:
            continue
        seen.add(key)
        rows.append(item)
    return tuple(rows)


def replay_url(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"


def page_id(original):
    try:
        q=urllib.parse.parse_qs(urllib.parse.urlsplit(original).query)
        return str((q.get("id") or [""])[0])
    except Exception:
        return ""


def token_hits(text,raw):
    low=text.lower()
    rawlow=raw.lower()
    return tuple(t for t in TOKENS if t.lower() in low or t.lower().encode("ascii","ignore").decode("ascii") in rawlow if t)


def strong_match(text,raw):
    low=text.lower()
    rawlow=raw.lower()
    ascii_tokens=("sa25up.zip","stoneage","stone age")
    cjk_tokens=("石器时代","石器時代","精灵王传说","精靈王傳說","精灵王","精靈王")
    return any(t.lower() in low for t in ascii_tokens) or any(t in text for t in cjk_tokens) or "sa25up.zip" in rawlow


def contexts(text):
    v=visible(text)
    low=v.lower()
    out=[]
    seen=set()
    for token in TOKENS:
        i=low.find(token.lower())
        if i<0:
            continue
        c=v[max(0,i-280):min(len(v),i+len(token)+520)]
        c=" ".join(c.split())
        if c and c not in seen:
            seen.add(c); out.append((token,c))
    return tuple(out)


def interesting_hrefs(text):
    out=[]
    seen=set()
    for href in HREF_RE.findall(text):
        href=html.unescape(href.strip())
        low=href.lower()
        if any(x in low for x in ("stoneage","sa25","/file/game/","downit.php")):
            if href not in seen:
                seen.add(href); out.append(href)
    return tuple(out)


def inspect(row):
    try:
        st,final,body=fetch_bytes(replay_url(row),timeout=22,max_bytes=1_500_000)
        declared=declared_charset(body)
        enc,text=decode(body,declared)
        raw=body.decode("latin1","ignore")
        hit=strong_match(text,raw)
        return row,st,final,body,enc,text,hit,None
    except Exception as e:
        return row,None,None,None,None,None,False,(type(e).__name__,str(e))


def main():
    print("StoneAge 2.5 21CN catalogue-record scan — R1")
    print("SCOPE|wayback-21cn-list-html|derived-match-context-only|no-linked-game-payload")
    errors=[]
    try:
        st,final,body=fetch_bytes(cdx_url(),timeout=45,max_bytes=6_000_000)
        rows=parse_cdx(body)
        print(
            f"CDX|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"rows={len(rows)}|final={clean(final)}"
        )
    except Exception as e:
        print(f"FATAL|scope=cdx|kind={type(e).__name__}|message={clean(e)}")
        return

    hits=[]
    completed=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
        for row,st,final,pbody,enc,text,hit,error in ex.map(inspect,rows):
            if error:
                errors.append((page_id(str(row.get("original") or "")),type(error).__name__,str(error)))
                continue
            completed+=1
            if not hit:
                continue
            hits.append((row,st,final,pbody,enc,text))
            original=str(row.get("original") or "")
            pid=page_id(original)
            print(
                f"MATCH|id={clean(pid)}|timestamp={clean(row.get('timestamp'))}|original={clean(original)}|"
                f"status={st}|bytes={len(pbody)}|sha256={hashlib.sha256(pbody).hexdigest()}|"
                f"encoding={clean(enc)}|title={clean(title(text),1000)}|final={clean(final)}"
            )
            th=[]
            low=text.lower()
            for token in TOKENS:
                if token.lower() in low:
                    th.append(token)
            print(f"TOKENS|id={clean(pid)}|values={clean(','.join(th))}")
            for token,ctx in contexts(text)[:12]:
                print(f"CONTEXT|id={clean(pid)}|token={clean(token)}|value={clean(ctx,2200)}")
            for n,href in enumerate(interesting_hrefs(text)[:50],1):
                print(f"HREF|id={clean(pid)}|order={n}|value={clean(href,2000)}")

    # Keep error output bounded; individual archive failures do not erase successful scan evidence.
    by_kind={}
    for pid,kind,msg in errors:
        by_kind[kind]=by_kind.get(kind,0)+1
    for kind,count in sorted(by_kind.items()):
        print(f"ERROR_SUMMARY|kind={clean(kind)}|count={count}")
    for pid,kind,msg in errors[:30]:
        print(f"ERROR_SAMPLE|id={clean(pid)}|kind={clean(kind)}|message={clean(msg)}")

    print(f"COUNT|catalog_rows|{len(rows)}")
    print(f"COUNT|completed_pages|{completed}")
    print(f"COUNT|matched_pages|{len(hits)}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|21CN_STONEAGE_CATALOGUE_MATCH_FOUND|classify matched record fields and download topology before any payload claim")
    elif completed==len(rows):
        print("RESOLUTION|NO_21CN_STONEAGE_LIST_MATCH|tested archived list.php catalogue surface bounded")
    else:
        print("RESOLUTION|PARTIAL_21CN_CATALOGUE_SCAN|retry failed pages or narrow by newly recovered IDs/tokens")
    print(
        "EVIDENCE_BOUNDARY|a 21CN catalogue-page match can establish 21CN-native metadata and link topology; "
        "it cannot prove linked bytes were official, clean, complete, or successfully archived."
    )


if __name__=="__main__":
    main()
