#!/usr/bin/env python3
"""Probe preservation indexes for the exact historical StoneAge 2.5 token sa25up.zip.

This is metadata-first archaeology. It queries archive/index services for the exact
URL/filename and does not download or commit the historical client/update payload.
"""
from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

from tools.stoneage_sa25_exact_carrier_probe import (
    clean,
    discm_rows,
    discm_url,
    fetch_json,
    ia_docs,
    ia_metadata,
    ia_url,
)
from tools.stoneage_commoncrawl_exact_payload_probe import collections as cc_collections, query as cc_query
from tools.stoneage_exact_mirror_arquivopt_cdx_probe import (
    fetch_bytes as arquivo_fetch_bytes,
    parse_rows as arquivo_parse_rows,
)

UA = "stoneage-rebuild-archaeology/1.0"
TOKEN = "sa25up.zip"
HISTORICAL_URL = "http://202.104.32.168/file/game/maoxian/sa25up.zip"
SOURCE_PAGE = "https://www.geocities.ws/kk00000099/link.html"
WAYBACK_AVAILABLE = "https://archive.org/wayback/available"
ARQUIVO_CDX = "https://arquivo.pt/wayback/cdx"
WAYBACK_DATES = ("20020120", "20020205", "20021231", "20031231")


def wayback_url(timestamp: str) -> str:
    return WAYBACK_AVAILABLE + "?" + urllib.parse.urlencode(
        {"url": HISTORICAL_URL, "timestamp": timestamp}
    )


def parse_wayback(payload: dict) -> dict | None:
    snaps = payload.get("archived_snapshots")
    if not isinstance(snaps, dict):
        return None
    closest = snaps.get("closest")
    if not isinstance(closest, dict) or not closest.get("available"):
        return None
    return {
        "timestamp": str(closest.get("timestamp") or ""),
        "status": str(closest.get("status") or ""),
        "url": str(closest.get("url") or ""),
    }


def arquivo_url() -> str:
    return ARQUIVO_CDX + "?" + urllib.parse.urlencode(
        {
            "url": HISTORICAL_URL,
            "from": "2001",
            "to": "2005",
            "limit": "200",
            "output": "json",
            "filter": "statuscode:200",
        }
    )


def get_json(url: str, timeout: int = 20):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json,text/plain,*/*"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        return int(getattr(response, "status", response.getcode())), response.geturl(), body, json.loads(body.decode("utf-8", "replace"))


def main():
    print("StoneAge 2.5 sa25up.zip exact-token preservation probe — R1")
    print("SCOPE|exact-url+exact-filename|archive-index-metadata-only|no-historical-payload-download")
    print(f"SOURCE_PAGE|{SOURCE_PAGE}")
    print(f"TARGET|token={TOKEN}|url={HISTORICAL_URL}")

    errors = []
    hits = 0

    # Wayback Availability: nearest-capture metadata only.
    for requested in WAYBACK_DATES:
        try:
            st, final, body, payload = get_json(wayback_url(requested))
            closest = parse_wayback(payload)
            print(
                f"WAYBACK_QUERY|requested={requested}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}|available={1 if closest else 0}"
            )
            if closest:
                hits += 1
                print(
                    f"WAYBACK_HIT|requested={requested}|timestamp={clean(closest['timestamp'])}|"
                    f"status={clean(closest['status'])}|url={clean(closest['url'])}"
                )
        except Exception as exc:
            errors.append((f"wayback:{requested}", type(exc).__name__, str(exc)))

    # Arquivo.pt exact URL CDX metadata.
    try:
        url = arquivo_url()
        body = arquivo_fetch_bytes(url, timeout=15, attempts=2)
        rows = arquivo_parse_rows(body)
        print(
            f"ARQUIVO_QUERY|status=ok|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}"
        )
        for row in rows:
            hits += 1
            print(
                f"ARQUIVO_HIT|timestamp={clean(row.get('timestamp') or row.get('date'))}|"
                f"original={clean(row.get('original') or row.get('url'))}|"
                f"status={clean(row.get('statuscode') or row.get('status'))}|"
                f"mime={clean(row.get('mimetype') or row.get('mime'))}|"
                f"length={clean(row.get('length') or row.get('contentLength'))}|"
                f"digest={clean(row.get('digest'))}"
            )
    except Exception as exc:
        errors.append(("arquivo", type(exc).__name__, str(exc)))

    # Common Crawl exact URL index metadata across the bounded recent index set.
    try:
        indexes = cc_collections(limit=8)
        print(f"CC_INDEXES|{','.join(index_id for index_id, _ in indexes)}")
        for index_id, api in indexes:
            try:
                rows = cc_query(api, HISTORICAL_URL, "exact")
                print(f"CC_QUERY|index={clean(index_id)}|rows={len(rows)}")
                for row in rows:
                    hits += 1
                    print(
                        f"CC_HIT|index={clean(index_id)}|timestamp={clean(row.get('timestamp'))}|"
                        f"url={clean(row.get('url') or HISTORICAL_URL)}|status={clean(row.get('status'))}|"
                        f"mime={clean(row.get('mime'))}|length={clean(row.get('length'))}|"
                        f"digest={clean(row.get('digest'))}|filename={clean(row.get('filename'))}|"
                        f"offset={clean(row.get('offset'))}"
                    )
            except Exception as exc:
                errors.append((f"commoncrawl:{index_id}", type(exc).__name__, str(exc)))
    except Exception as exc:
        errors.append(("commoncrawl:collinfo", type(exc).__name__, str(exc)))

    # DiscMaster exact filename index.
    try:
        st, final, body, data = fetch_json(discm_url(TOKEN))
        rows = discm_rows(data)
        strict = [
            row for row in rows
            if str(row.get("filename") or row.get("fileid") or "").replace("\\", "/").lower().endswith("/" + TOKEN)
            or str(row.get("filename") or row.get("fileid") or "").lower() == TOKEN
        ]
        print(
            f"DISCM_QUERY|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"rows={len(rows)}|strict={len(strict)}|final={clean(final)}"
        )
        for row in strict:
            hits += 1
            print(
                f"DISCM_HIT|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|"
                f"filename={clean(row.get('filename'))}|fileid={clean(row.get('fileid'))}|"
                f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
            )
    except Exception as exc:
        errors.append(("discmaster", type(exc).__name__, str(exc)))

    # Internet Archive item discovery; only promote exact file-list matches.
    try:
        st, final, body, data = fetch_json(ia_url(TOKEN))
        docs = ia_docs(data)
        print(
            f"IA_QUERY|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"items={len(docs)}|final={clean(final)}"
        )
        for doc in docs:
            ident = str(doc.get("identifier") or "")
            if not ident:
                continue
            try:
                mst, mfinal, mbody, meta = ia_metadata(ident)
                exact = [
                    f for f in meta.get("files", []) if isinstance(meta, dict)
                    if str(f.get("name") or "").replace("\\", "/").split("/")[-1].lower() == TOKEN
                ]
                if not exact:
                    continue
                print(
                    f"IA_ITEM|identifier={clean(ident)}|title={clean(doc.get('title'))}|"
                    f"exact_files={len(exact)}|meta_status={mst}|meta_sha256={hashlib.sha256(mbody).hexdigest()}"
                )
                for f in exact:
                    hits += 1
                    print(
                        f"IA_FILE|identifier={clean(ident)}|name={clean(f.get('name'))}|"
                        f"size={clean(f.get('size'))}|md5={clean(f.get('md5'))}|sha1={clean(f.get('sha1'))}"
                    )
            except Exception as exc:
                errors.append((f"ia-meta:{ident}", type(exc).__name__, str(exc)))
    except Exception as exc:
        errors.append(("internet-archive", type(exc).__name__, str(exc)))

    for scope, kind, message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|hits|{hits}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|SA25UP_PRESERVATION_CANDIDATE_FOUND|verify capture provenance,size,and archive identity before any payload classification")
    elif errors:
        print("RESOLUTION|PARTIAL_SA25UP_INDEX_FAILURE|retry only failed index surfaces")
    else:
        print("RESOLUTION|NO_SA25UP_INDEX_HIT|tested exact-url/file-index surfaces bounded")
    print(
        "EVIDENCE_BOUNDARY|the historical link page establishes an exact token/URL lead only; "
        "the basename sa25up.zip does not establish whether the file is the 8.25MB updater, "
        "the 575/580MB full package, or another repack without recovered metadata/bytes."
    )


if __name__ == "__main__":
    main()
