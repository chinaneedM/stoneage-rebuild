#!/usr/bin/env python3
"""Probe the archival neighborhood around the historical StoneAge 2.5 sa25up.zip link.

Metadata only. The purpose is to recover timing, sibling paths, redirects, or source-page
anchors without downloading the historical StoneAge payload.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

from tools.stoneage_commoncrawl_exact_payload_probe import collections as cc_collections, query as cc_query
from tools.stoneage_exact_mirror_arquivopt_cdx_probe import fetch_bytes as arquivo_fetch_bytes, parse_rows as arquivo_parse_rows

UA="stoneage-rebuild-archaeology/1.0"
WAYBACK_CDX="https://web.archive.org/cdx/search/cdx"
WAYBACK_AVAILABLE="https://archive.org/wayback/available"
ARQUIVO="https://arquivo.pt/wayback/cdx"

PAYLOAD="http://202.104.32.168/file/game/maoxian/sa25up.zip"
DIR="http://202.104.32.168/file/game/maoxian/"
GAME_DIR="http://202.104.32.168/file/game/"
SOURCE="http://pcpc.idv.tw/soft/soft.htm"
SOURCE_WWW="http://www.pcpc.idv.tw/soft/soft.htm"
SOURCE_DATES=("20020101","20020701","20030101","20040101","20050101")
RELEVANT=re.compile(r"(?i)(sa25|stoneage|石器|\.zip$|\.exe$|maoxian)")


def clean(v,limit=1800):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b


def cdx_url(url,match="exact",limit=5000):
    p=[
        ("url",url),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2001"),("to","2006"),("collapse","urlkey"),("limit",str(limit)),
    ]
    return WAYBACK_CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    h=data[0]
    return tuple(dict(zip(h,row)) for row in data[1:] if isinstance(row,list))


def availability_url(url,date):
    return WAYBACK_AVAILABLE+"?"+urllib.parse.urlencode({"url":url,"timestamp":date})


def parse_available(body):
    obj=json.loads(body.decode("utf-8","replace"))
    c=(obj.get("archived_snapshots") or {}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):
        return None
    return {"timestamp":str(c.get("timestamp") or ""),"status":str(c.get("status") or ""),"url":str(c.get("url") or "")}


def arquivo_url(url,match=None):
    p={"url":url,"from":"2001","to":"2006","limit":"5000","output":"json"}
    if match:
        p["matchType"]=match
    return ARQUIVO+"?"+urllib.parse.urlencode(p)


def emit_rows(prefix,rows,only_relevant=False):
    emitted=0
    for row in rows:
        original=str(row.get("original") or row.get("url") or "")
        if only_relevant and not RELEVANT.search(urllib.parse.unquote(original)):
            continue
        emitted+=1
        print(
            f"{prefix}|timestamp={clean(row.get('timestamp') or row.get('date'))}|"
            f"original={clean(original)}|status={clean(row.get('statuscode') or row.get('status'))}|"
            f"mime={clean(row.get('mimetype') or row.get('mime'))}|length={clean(row.get('length') or row.get('contentLength'))}|"
            f"digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}"
        )
    return emitted


def main():
    print("StoneAge 2.5 sa25up archival-neighborhood probe — R1")
    print("SCOPE|archive-index-metadata-only|no-historical-payload-download")
    print(f"PAYLOAD|{PAYLOAD}")
    print(f"DIR|{DIR}")
    print(f"SOURCE|{SOURCE}")

    errors=[]
    hits=0

    # Wayback CDX exact source pages and bounded directory prefixes.
    for label,url,match,limit in (
        ("payload",PAYLOAD,"exact",200),
        ("source",SOURCE,"exact",200),
        ("source-www",SOURCE_WWW,"exact",200),
        ("maoxian-dir",DIR,"prefix",5000),
        ("game-dir",GAME_DIR,"prefix",5000),
    ):
        try:
            st,final,b=fetch(cdx_url(url,match,limit))
            rows=parse_cdx(b)
            rel=tuple(r for r in rows if RELEVANT.search(urllib.parse.unquote(str(r.get("original") or ""))))
            print(
                f"WAYBACK_CDX|label={label}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|"
                f"rows={len(rows)}|relevant={len(rel)}|final={clean(final)}"
            )
            for r in rel[:500]:
                hits+=1
                emit_rows("WAYBACK_HIT",(r,))
        except Exception as e:
            errors.append((f"wayback-cdx:{label}",type(e).__name__,str(e)))

    # Availability around likely early source-page dates.
    for src_label,src in (("source",SOURCE),("source-www",SOURCE_WWW)):
        for date in SOURCE_DATES:
            try:
                st,final,b=fetch(availability_url(src,date),20)
                row=parse_available(b)
                print(
                    f"WAYBACK_AVAILABLE|label={src_label}|requested={date}|status={st}|bytes={len(b)}|"
                    f"sha256={hashlib.sha256(b).hexdigest()}|available={1 if row else 0}|final={clean(final)}"
                )
                if row:
                    hits+=1
                    print(
                        f"AVAILABLE_HIT|label={src_label}|requested={date}|timestamp={clean(row['timestamp'])}|"
                        f"status={clean(row['status'])}|url={clean(row['url'])}"
                    )
            except Exception as e:
                errors.append((f"availability:{src_label}:{date}",type(e).__name__,str(e)))

    # Arquivo exact source/payload and directory prefix if supported.
    for label,url,match in (
        ("payload",PAYLOAD,None),
        ("source",SOURCE,None),
        ("source-www",SOURCE_WWW,None),
        ("maoxian-dir",DIR,"prefix"),
    ):
        try:
            b=arquivo_fetch_bytes(arquivo_url(url,match),timeout=15,attempts=2)
            rows=arquivo_parse_rows(b)
            rel=tuple(r for r in rows if RELEVANT.search(urllib.parse.unquote(str(r.get("original") or r.get("url") or ""))))
            print(f"ARQUIVO|label={label}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|relevant={len(rel)}")
            for r in rel[:500]:
                hits+=1
                emit_rows("ARQUIVO_HIT",(r,))
        except Exception as e:
            errors.append((f"arquivo:{label}",type(e).__name__,str(e)))

    # Common Crawl exact payload/source + bounded prefix neighborhood.
    try:
        indexes=cc_collections(limit=8)
        print("CC_INDEXES|"+",".join(i for i,_ in indexes))
        for index_id,api in indexes:
            for label,url,mode in (
                ("payload",PAYLOAD,"exact"),
                ("source",SOURCE,"exact"),
                ("source-www",SOURCE_WWW,"exact"),
                ("maoxian-dir",DIR,"prefix"),
            ):
                try:
                    rows=cc_query(api,url,mode)
                    rel=tuple(r for r in rows if RELEVANT.search(urllib.parse.unquote(str(r.get("url") or url))))
                    print(f"CC|index={clean(index_id)}|label={label}|mode={mode}|rows={len(rows)}|relevant={len(rel)}")
                    for r in rel[:200]:
                        hits+=1
                        print(
                            f"CC_HIT|index={clean(index_id)}|label={label}|timestamp={clean(r.get('timestamp'))}|"
                            f"url={clean(r.get('url') or url)}|status={clean(r.get('status'))}|mime={clean(r.get('mime'))}|"
                            f"length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|filename={clean(r.get('filename'))}|offset={clean(r.get('offset'))}"
                        )
                except Exception as e:
                    errors.append((f"cc:{index_id}:{label}",type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("cc:collinfo",type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|hits|{hits}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|ARCHIVAL_NEIGHBORHOOD_EVIDENCE_FOUND|classify source-page timing and sibling paths before any payload recovery claim")
    elif errors:
        print("RESOLUTION|PARTIAL_NEIGHBORHOOD_FAILURE|retry only failed archive surfaces")
    else:
        print("RESOLUTION|NO_ARCHIVAL_NEIGHBORHOOD_HIT|tested exact+prefix archive-index surfaces bounded")
    print(
        "EVIDENCE_BOUNDARY|directory/source-page index hits can date or contextualize the sa25up link, "
        "but they do not prove payload identity, size, clean-client status, or operator provenance."
    )


if __name__=="__main__":
    main()
