#!/usr/bin/env python3
"""Audit exact Internet Archive StoneAge item leads without downloading full payloads.

Targets are deliberately bounded:
- stoneage_tw_2000_win: 2000 Taiwan StoneAge item lead
- Stoneage-5: 2002-12-27 宠物进化史 CD-ROM lead
- sa-arena: 2002 Stoneage Arena control

The probe records IA metadata/file hashes. For ISO/BIN/IMG/MDF carrier images it reuses
our HTTP-Range ISO/Joliet directory scanner. For ZIP files it reads only the ZIP tail and
central directory. Other archive formats are metadata-only pending a bounded parser.
"""

from __future__ import annotations

import concurrent.futures
import re
import urllib.parse

from tools.stoneage_netpower_remote_iso_scan import clean, metadata, scan_one
from tools.stoneage_sourceforge_zip_index_probe import (
    TAIL_BYTES,
    parse_central_directory,
    parse_eocd_tail,
    range_bytes,
)

TARGET_ITEMS = (
    "stoneage_tw_2000_win",
    "Stoneage-5",
    "sa-arena",
)

DISC = re.compile(r"(?i)\.(?:iso|img|bin|mdf)$")
ZIP = re.compile(r"(?i)\.zip$")
ARCHIVE = re.compile(r"(?i)\.(?:7z|rar|zip|tar|gz|bz2|xz|ecm|chd)$")
CUE = re.compile(r"(?i)\.(?:cue|ccd)$")
EXECUTABLE = re.compile(r"(?i)\.(?:exe|com|dll)$")
STONEAGE = re.compile(r"(?i)(stone\s*age|stoneage|石器時代|石器时代|스톤\s*에이지|스톤에이지)")
EXACT_CLIENT = re.compile(
    r"(?i)(?:^|[/\\])(?:"
    r"sa\.exe|sa_demo\.exe|stoneage\.exe|stone_demo\.exe|"
    r"onlstoneage\.zip|stoneagebeta\.zip|stoneage\.zip"
    r")$"
)
MIN_DISC_SIZE = 10 * 1024 * 1024
MAX_ZIP_CENTRAL = 16 * 1024 * 1024
MAX_ZIP_HITS = 300


def download_url(identifier, name):
    return "https://archive.org/download/{}/{}".format(
        urllib.parse.quote(identifier, safe=""),
        urllib.parse.quote(name, safe="/"),
    )


def source_kind(row):
    name = str(row.get("name", ""))
    source = str(row.get("source", ""))
    size = int(row.get("size") or 0)
    if DISC.search(name) and size >= MIN_DISC_SIZE:
        return "disc"
    if ZIP.search(name) and size > 0:
        return "zip"
    if ARCHIVE.search(name):
        return "archive-metadata-only"
    if CUE.search(name):
        return "cue"
    if EXECUTABLE.search(name):
        return "executable"
    if EXACT_CLIENT.search(name):
        return "exact-client-name"
    if STONEAGE.search(name):
        return "stoneage-name"
    if source == "original":
        return "original-other"
    return "derivative"


def file_record(row):
    return {
        "name": str(row.get("name", "")),
        "size": int(row.get("size") or 0),
        "md5": str(row.get("md5", "")),
        "sha1": str(row.get("sha1", "")),
        "crc32": str(row.get("crc32", "")),
        "format": str(row.get("format", "")),
        "source": str(row.get("source", "")),
    }


def inspect_zip(identifier, row):
    name = row["name"]
    total_size = row["size"]
    if total_size <= 0:
        raise ValueError("zip size unavailable")
    url = download_url(identifier, name)
    tail_start = max(0, total_size - TAIL_BYTES)
    tail, final_url, _headers = range_bytes(url, tail_start, total_size - 1)
    eocd = parse_eocd_tail(tail, total_size)
    if eocd["central_size"] > MAX_ZIP_CENTRAL:
        raise ValueError(f"central directory too large: {eocd['central_size']}")
    if eocd["central_size"]:
        start = eocd["central_offset"]
        central, _final, _headers = range_bytes(
            url, start, start + eocd["central_size"] - 1
        )
    else:
        central = b""
    entries = parse_central_directory(central, eocd["entries"])
    return {
        "final_url": final_url,
        "entries": entries,
        "central_size": eocd["central_size"],
        "bytes_read": len(tail) + len(central),
    }


def print_item_metadata(identifier, data):
    meta = data.get("metadata", {})
    print(
        "ITEM|"
        f"identifier={clean(identifier)}|title={clean(meta.get('title'))}|"
        f"date={clean(meta.get('date') or meta.get('year'))}|"
        f"creator={clean(meta.get('creator'))}|publisher={clean(meta.get('publisher'))}|"
        f"uploader={clean(meta.get('uploader'))}|collection={clean(meta.get('collection'),1400)}|"
        f"description={clean(meta.get('description'),1800)}"
    )


def main():
    print("StoneAge exact IA artifact audit — R1")
    print("SCOPE|ia-metadata-plus-bounded-http-range-structure|no-full-payload-download")
    print("TARGET_ITEMS|" + ",".join(TARGET_ITEMS))

    metadata_errors = []
    item_data = {}
    for identifier in TARGET_ITEMS:
        try:
            data = metadata(identifier)
        except Exception as exc:
            metadata_errors.append((identifier, type(exc).__name__, str(exc)))
            continue
        item_data[identifier] = data
        print_item_metadata(identifier, data)

    disc_jobs = []
    zip_jobs = []
    exact_name_count = 0
    original_count = 0

    for identifier, data in item_data.items():
        for raw in data.get("files", []):
            row = file_record(raw)
            kind = source_kind(raw)
            if row["source"] == "original":
                original_count += 1
            if EXACT_CLIENT.search(row["name"]):
                exact_name_count += 1
            if row["source"] == "original" or kind in (
                "disc",
                "zip",
                "archive-metadata-only",
                "cue",
                "executable",
                "exact-client-name",
                "stoneage-name",
            ):
                print(
                    f"FILE|identifier={clean(identifier)}|kind={kind}|"
                    f"name={clean(row['name'])}|size={row['size']}|"
                    f"md5={clean(row['md5'])}|sha1={clean(row['sha1'])}|"
                    f"crc32={clean(row['crc32'])}|format={clean(row['format'])}|"
                    f"source={clean(row['source'])}"
                )
            if kind == "disc":
                disc_jobs.append((identifier, data.get("metadata", {}), row))
            elif kind == "zip":
                zip_jobs.append((identifier, row))

    for identifier, kind, message in metadata_errors:
        print(
            f"ERROR|phase=metadata|identifier={clean(identifier)}|kind={clean(kind)}|"
            f"message={clean(message)}"
        )

    disc_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for result in executor.map(lambda args: scan_one(*args), disc_jobs):
            disc_results.append(result)

    for result in disc_results:
        base = (
            f"identifier={clean(result['identifier'])}|name={clean(result['name'])}|"
            f"size={result['size']}|md5={clean(result['md5'])}|sha1={clean(result['sha1'])}"
        )
        if result["error"]:
            print(f"DISC_ERROR|{base}|message={clean(result['error'])}")
            continue
        hit_count = (
            len((result.get("primary") or {}).get("hits", []))
            + len((result.get("joliet") or {}).get("hits", []))
        )
        print(
            f"DISC|{base}|layout={clean(result['layout'])}|volume={clean(result['volume'])}|"
            f"requests={result['requests']}|bytes_read={result['bytes_read']}|"
            f"primary_entries={result['primary']['entries']}|"
            f"primary_dirs={result['primary']['dirs']}|joliet={int(result['joliet'] is not None)}|"
            f"joliet_entries={(result['joliet'] or {}).get('entries',0)}|"
            f"truncated={int(result['primary']['truncated'] or bool((result['joliet'] or {}).get('truncated',False)))}|"
            f"stoneage_hits={hit_count}"
        )
        for namespace in ("primary", "joliet"):
            tree = result.get(namespace)
            if not tree:
                continue
            for path, size, is_dir in tree["hits"]:
                print(
                    f"DISC_HIT|identifier={clean(result['identifier'])}|"
                    f"image={clean(result['name'])}|namespace={namespace}|"
                    f"path={clean(path)}|size={size}|directory={int(is_dir)}"
                )
        for path in result["primary"]["samples"][:20]:
            print(
                f"DISC_SAMPLE|identifier={clean(result['identifier'])}|"
                f"image={clean(result['name'])}|path={clean(path,500)}"
            )

    zip_ok = 0
    zip_errors = 0
    for identifier, row in zip_jobs:
        try:
            result = inspect_zip(identifier, row)
        except Exception as exc:
            zip_errors += 1
            print(
                f"ZIP_ERROR|identifier={clean(identifier)}|name={clean(row['name'])}|"
                f"kind={type(exc).__name__}|message={clean(exc)}"
            )
            continue
        zip_ok += 1
        entries = result["entries"]
        hits = [
            entry
            for entry in entries
            if EXACT_CLIENT.search(entry.name) or STONEAGE.search(entry.name)
        ]
        print(
            f"ZIP|identifier={clean(identifier)}|name={clean(row['name'])}|"
            f"entries={len(entries)}|central_size={result['central_size']}|"
            f"bytes_read={result['bytes_read']}|hits={len(hits)}|"
            f"final_url={clean(result['final_url'])}"
        )
        for entry in entries[:30]:
            print(
                f"ZIP_SAMPLE|identifier={clean(identifier)}|archive={clean(row['name'])}|"
                f"path={clean(entry.name)}|usize={entry.uncompressed_size}|"
                f"csize={entry.compressed_size}|crc32={entry.crc32:08x}"
            )
        for entry in hits[:MAX_ZIP_HITS]:
            print(
                f"ZIP_HIT|identifier={clean(identifier)}|archive={clean(row['name'])}|"
                f"path={clean(entry.name)}|usize={entry.uncompressed_size}|"
                f"csize={entry.compressed_size}|crc32={entry.crc32:08x}"
            )

    print(f"COUNT|items_resolved|{len(item_data)}")
    print(f"COUNT|metadata_errors|{len(metadata_errors)}")
    print(f"COUNT|original_files|{original_count}")
    print(f"COUNT|exact_client_filename_hits|{exact_name_count}")
    print(f"COUNT|disc_candidates|{len(disc_jobs)}")
    print(f"COUNT|disc_scanned|{sum(not r['error'] for r in disc_results)}")
    print(f"COUNT|disc_errors|{sum(bool(r['error']) for r in disc_results)}")
    print(f"COUNT|zip_candidates|{len(zip_jobs)}")
    print(f"COUNT|zip_scanned|{zip_ok}")
    print(f"COUNT|zip_errors|{zip_errors}")


if __name__ == "__main__":
    main()
