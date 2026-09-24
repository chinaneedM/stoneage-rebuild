#!/usr/bin/env python3
"""Probe preservation indexes for the 21CN router-derived sa25up mirror.

The exact images.21cn.com URL comes from the archived 2002-10-17 download
router for native catalogue record 20165. This probe is metadata-only and
never fetches the historical ZIP payload.
"""
from __future__ import annotations

import hashlib
import urllib.parse
import urllib.request

from tools.stoneage_sa25_21cn_record20165_probe import cdx_url, clean, parse
from tools.stoneage_commoncrawl_exact_payload_probe import collections as cc_collections, query as cc_query
from tools.stoneage_exact_mirror_arquivopt_cdx_probe import (
    fetch_bytes as arquivo_fetch_bytes,
    parse_rows as arquivo_parse_rows,
)

UA="stoneage-rebuild-archaeology/1.0"
ZIP_URL="http://images.21cn.com/download/file/game/maoxian/sa25up.zip"
JPG_URL="http://images.21cn.com/download/file/game/maoxian/sa25up.jpg"
ARQUIVO_CDX="https://arquivo.pt/wayback/cdx"


def fetch(url,timeout=25,max_bytes=3_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),body


def arquivo_url(target):
    return ARQUIVO_CDX+"?"+urllib.parse.urlencode({
        "url":target,
        "from":"2001",
        "to":"2005",
        "limit":"200",
        "output":"json",
    })


def main():
    print("StoneAge 2.5 21CN images-host sa25up mirror preservation probe — R1")
    print("SCOPE|router-derived-exact-url|archive-index-metadata-only|no-historical-payload-download")
    print(f"TARGET|zip={ZIP_URL}|jpg={JPG_URL}")
    errors=[]
    hits=0

    for label,target in (("zip",ZIP_URL),("jpg",JPG_URL)):
        try:
            st,final,body=fetch(cdx_url(target,"exact",1000),30)
            rows=parse(body)
            print(
                f"WAYBACK_CDX|label={label}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for row in rows:
                hits+=1
                print(
                    f"WAYBACK_HIT|label={label}|timestamp={clean(row.get('timestamp'))}|"
                    f"original={clean(row.get('original'))}|status={clean(row.get('statuscode'))}|"
                    f"mime={clean(row.get('mimetype'))}|length={clean(row.get('length'))}|"
                    f"digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}"
                )
        except Exception as exc:
            errors.append((f"wayback:{label}",type(exc).__name__,str(exc)))

    try:
        body=arquivo_fetch_bytes(arquivo_url(ZIP_URL),timeout=18,attempts=2)
        rows=arquivo_parse_rows(body)
        print(
            f"ARQUIVO|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}"
        )
        for row in rows:
            hits+=1
            print(
                f"ARQUIVO_HIT|timestamp={clean(row.get('timestamp') or row.get('date'))}|"
                f"original={clean(row.get('original') or row.get('url'))}|"
                f"status={clean(row.get('statuscode') or row.get('status'))}|"
                f"mime={clean(row.get('mimetype') or row.get('mime'))}|"
                f"length={clean(row.get('length') or row.get('contentLength'))}|"
                f"digest={clean(row.get('digest'))}"
            )
    except Exception as exc:
        errors.append(("arquivo",type(exc).__name__,str(exc)))

    try:
        indexes=cc_collections(limit=8)
        print("CC_INDEXES|"+",".join(index_id for index_id,_ in indexes))
        for index_id,api in indexes:
            try:
                rows=cc_query(api,ZIP_URL,"exact")
                print(f"CC_QUERY|index={clean(index_id)}|rows={len(rows)}")
                for row in rows:
                    hits+=1
                    print(
                        f"CC_HIT|index={clean(index_id)}|timestamp={clean(row.get('timestamp'))}|"
                        f"url={clean(row.get('url') or ZIP_URL)}|status={clean(row.get('status'))}|"
                        f"mime={clean(row.get('mime'))}|length={clean(row.get('length'))}|"
                        f"digest={clean(row.get('digest'))}|filename={clean(row.get('filename'))}|"
                        f"offset={clean(row.get('offset'))}"
                    )
            except Exception as exc:
                errors.append((f"commoncrawl:{index_id}",type(exc).__name__,str(exc)))
    except Exception as exc:
        errors.append(("commoncrawl:collinfo",type(exc).__name__,str(exc)))

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|hits|{hits}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|ROUTER_DERIVED_MIRROR_INDEX_HIT|inspect status,size,digest and seek independently recoverable copy")
    elif errors:
        print("RESOLUTION|PARTIAL_ROUTER_DERIVED_MIRROR_INDEX_FAILURE|retry failed metadata surfaces only")
    else:
        print("RESOLUTION|NO_ROUTER_DERIVED_MIRROR_INDEX_HIT|tested exact mirror URL surface bounded")
    print(
        "EVIDENCE_BOUNDARY|the 2002 downit router proves this mirror URL was emitted by 21CN; "
        "index metadata alone does not recover or authenticate ZIP bytes."
    )


if __name__=="__main__":
    main()
