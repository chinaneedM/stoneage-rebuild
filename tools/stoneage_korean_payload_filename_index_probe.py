#!/usr/bin/env python3
"""Probe preservation indexes for exact Korean StoneAge 2000-2001 payload filenames.

Sources are metadata/path indexes only: DiscMaster, Internet Archive item metadata,
and the public old-disc torrent path snapshot. No client/disc payload bytes are fetched.
"""
from __future__ import annotations

import hashlib
import io
import os
import zipfile

from tools.stoneage_sa25_exact_carrier_probe import (
    clean,
    discm_rows,
    discm_url,
    fetch_json,
    ia_docs,
    ia_metadata,
    ia_url,
    interesting_files,
    norm,
)
from tools.stoneage_sa25_old_disc_torrent_probe import (
    MAX_TORRENT,
    MAX_ZIP,
    URL,
    bdecode,
    fetch as fetch_zip,
    root_info_span,
    torrent_paths,
)

TARGETS = (
    ("gametime-formal", "onlStoneAge.zip", "distinctive"),
    ("gametime-trial", "stone_demo.exe", "distinctive"),
    ("hananet-trial", "sa_demo.exe", "distinctive"),
    ("gagamel-beta", "stoneagebeta.zip", "distinctive"),
    ("cnet-formal", "stoneage.zip", "ambiguous-large"),
    ("hananet-formal", "sa.exe", "ambiguous-large"),
)

CONTEXT = (
    "stoneage", "stone age", "스톤에이지", "enium", "inium",
    "hananet", "cnet", "gametime", "gagamel",
)
MIN_LARGE = 220 * 1024 * 1024
MAX_LARGE = 300 * 1024 * 1024


def basename(v):
    return str(v or "").replace("\\", "/").rstrip("/").split("/")[-1].lower()


def parse_size(v):
    try:
        s = str(v or "").strip().replace(",", "")
        if not s:
            return None
        return int(float(s))
    except Exception:
        return None


def has_context(blob):
    n = norm(blob)
    return any(norm(x) in n for x in CONTEXT)


def strict_candidate(target_name, mode, *, filename="", size=None, context=""):
    if basename(filename) != target_name.lower():
        return False
    if mode == "distinctive":
        return True
    return (
        size is not None
        and MIN_LARGE <= size <= MAX_LARGE
    ) or has_context(context)


def main():
    print("StoneAge Korean 2000-2001 exact payload filename preservation probe — R1")
    print("SCOPE|DiscMaster+IA-metadata+old-disc-torrent-paths|no-client-or-disc-payload")
    for label, name, mode in TARGETS:
        print(f"TARGET|label={label}|filename={name}|mode={mode}")

    errors = []
    dm_hits = {}
    ia_hits = {}
    torrent_hits = []

    # DiscMaster file/path index.
    for label, name, mode in TARGETS:
        try:
            st, final, body, data = fetch_json(discm_url(name))
            rows = discm_rows(data)
            strict = []
            for row in rows:
                fn = row.get("filename") or row.get("fileid") or row.get("text") or ""
                size = parse_size(row.get("size"))
                ctx = " ".join(str(row.get(k) or "") for k in ("itemName", "href", "text", "title"))
                if strict_candidate(name, mode, filename=fn, size=size, context=ctx):
                    strict.append(row)
            print(
                f"DISCM_QUERY|label={label}|filename={name}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|strict={len(strict)}|final={clean(final)}"
            )
            for row in strict:
                key = (label, str(row.get("itemid") or ""), str(row.get("fileid") or row.get("filename") or ""))
                dm_hits[key] = row
                print(
                    f"DISCM_HIT|label={label}|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|"
                    f"fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|"
                    f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
                )
        except Exception as e:
            errors.append((f"discm:{label}", type(e).__name__, str(e)))

    # IA item metadata search. Search exact token; only promote file-list matches.
    for label, name, mode in TARGETS:
        try:
            st, final, body, data = fetch_json(ia_url(name))
            docs = ia_docs(data)
            print(
                f"IA_QUERY|label={label}|filename={name}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|items={len(docs)}|final={clean(final)}"
            )
            for doc in docs:
                ident = str(doc.get("identifier") or "")
                if not ident:
                    continue
                try:
                    mst, mfinal, mbody, meta = ia_metadata(ident)
                    strict_files = []
                    for f in meta.get("files", []) if isinstance(meta, dict) else []:
                        fn = str(f.get("name") or "")
                        size = parse_size(f.get("size"))
                        ctx = " ".join(
                            str(meta.get("metadata", {}).get(k) or "")
                            for k in ("title", "description", "creator", "subject")
                        )
                        if strict_candidate(name, mode, filename=fn, size=size, context=ctx):
                            strict_files.append(f)
                    if strict_files:
                        ia_hits[(label, ident)] = strict_files
                        print(
                            f"IA_ITEM|label={label}|identifier={clean(ident)}|title={clean(doc.get('title'))}|"
                            f"candidate_files={len(strict_files)}|meta_status={mst}|meta_sha256={hashlib.sha256(mbody).hexdigest()}"
                        )
                        for f in strict_files:
                            print(
                                f"IA_FILE|label={label}|identifier={clean(ident)}|name={clean(f.get('name'))}|"
                                f"size={clean(f.get('size'))}|md5={clean(f.get('md5'))}|sha1={clean(f.get('sha1'))}"
                            )
                except Exception as e:
                    errors.append((f"ia-meta:{label}:{ident}", type(e).__name__, str(e)))
        except Exception as e:
            errors.append((f"ia:{label}", type(e).__name__, str(e)))

    # Current old-disc torrent metadata snapshot: exact basenames only.
    try:
        st, final, h, zbytes = fetch_zip()
        print(
            f"TORRENT_ZIP|status={st}|bytes={len(zbytes)}|sha256={hashlib.sha256(zbytes).hexdigest()}|"
            f"last_modified={clean(h.get('Last-Modified'))}|final={clean(final)}"
        )
        by_name = {name.lower():(label,name,mode) for label,name,mode in TARGETS}
        with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
            for entry in z.namelist():
                if not entry.lower().endswith(".torrent"):
                    continue
                zi=z.getinfo(entry)
                if zi.file_size > MAX_TORRENT:
                    continue
                raw=z.read(entry)
                meta,_=bdecode(raw,0)
                paths=torrent_paths(meta)
                matches=[]
                for path in paths:
                    key=basename(path)
                    target=by_name.get(key)
                    if not target:
                        continue
                    label,name,mode=target
                    # Torrent metadata has no trustworthy uncompressed file size in this helper.
                    # Ambiguous sa.exe/stoneage.zip require contextual path evidence.
                    if strict_candidate(name,mode,filename=path,size=None,context=path):
                        matches.append((label,path))
                if matches:
                    try:
                        s,e=root_info_span(raw)
                        infohash=hashlib.sha1(raw[s:e]).hexdigest()
                    except Exception:
                        infohash=""
                    for label,path in matches:
                        torrent_hits.append((entry,infohash,label,path))
                        print(
                            f"TORRENT_HIT|entry={clean(entry)}|infohash={infohash}|"
                            f"label={label}|path={clean(path)}"
                        )
    except Exception as e:
        errors.append(("old-disc-torrent", type(e).__name__, str(e)))

    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|discm_strict_hits|{len(dm_hits)}")
    print(f"COUNT|ia_items_with_strict_files|{len(ia_hits)}")
    print(f"COUNT|torrent_strict_hits|{len(torrent_hits)}")
    print(f"COUNT|errors|{len(errors)}")

    if dm_hits or ia_hits or torrent_hits:
        print("RESOLUTION|KOREAN_PAYLOAD_FILENAME_CANDIDATE|verify provenance,size,and internal file tree before recovery promotion")
    elif errors:
        print("RESOLUTION|PARTIAL_FILENAME_INDEX_FAILURE|retry failed index only")
    else:
        print("RESOLUTION|NO_KOREAN_PAYLOAD_FILENAME_HIT|tested file-level/index surfaces bounded for exact tokens")
    print(
        "EVIDENCE_BOUNDARY|distinctive filename hits are recovery candidates, not clean-client proof; "
        "stoneage.zip and sa.exe require Korean StoneAge context or 220-300MB scale because their basenames are ambiguous."
    )


if __name__ == "__main__":
    main()
