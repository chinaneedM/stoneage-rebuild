#!/usr/bin/env python3
"""Remote directory scan of exact NetPower StoneAge-adjacent target issues on Internet Archive.

Reads only ISO-9660/Joliet directory sectors with HTTP Range requests using the existing
scanner. No complete disc image is downloaded or committed.
"""

from __future__ import annotations

import concurrent.futures
import re

from tools.stoneage_netpower_remote_iso_scan import clean, metadata, scan_one

TARGET_ITEMS = (
    "netpower_cd_2000_11",
    "netpower_cd_2001_02",
)

IMAGE = re.compile(r"(?i)\.(?:iso|img|bin|mdf)$")
MIN_SIZE = 10 * 1024 * 1024
MAX_IMAGES_PER_ITEM = 8


def select_images(data):
    rows = []
    seen = set()
    for f in data.get("files", []):
        name = str(f.get("name", ""))
        if not IMAGE.search(name):
            continue
        size = int(f.get("size") or 0)
        if size < MIN_SIZE:
            continue
        digest = str(f.get("sha1") or f.get("md5") or "")
        if digest and digest in seen:
            continue
        if digest:
            seen.add(digest)
        rows.append(
            {
                "name": name,
                "size": size,
                "md5": str(f.get("md5", "")),
                "sha1": str(f.get("sha1", "")),
                "format": str(f.get("format", "")),
            }
        )
    return sorted(rows, key=lambda row: row["name"].lower())[:MAX_IMAGES_PER_ITEM]


def main():
    print("StoneAge exact NetPower target-disc remote directory scan — R1")
    print("SCOPE|http-range-directory-metadata-only|no-full-image-download|no-carrier-bytes-committed")
    print("TARGET_ITEMS|" + ",".join(TARGET_ITEMS))

    jobs = []
    metadata_errors = []
    for identifier in TARGET_ITEMS:
        try:
            data = metadata(identifier)
        except Exception as exc:
            metadata_errors.append((identifier, type(exc).__name__, str(exc)))
            continue
        doc = data.get("metadata", {})
        images = select_images(data)
        print(
            f"ITEM|identifier={clean(identifier)}|title={clean(doc.get('title'))}|"
            f"date={clean(doc.get('date') or doc.get('year'))}|"
            f"uploader={clean(doc.get('uploader'))}|selected_images={len(images)}"
        )
        for f in images:
            print(
                f"TARGET|identifier={clean(identifier)}|name={clean(f['name'])}|"
                f"size={f['size']}|md5={clean(f['md5'])}|sha1={clean(f['sha1'])}|"
                f"format={clean(f['format'])}"
            )
            jobs.append((identifier, doc, f))

    for identifier, kind, message in metadata_errors:
        print(
            f"ERROR|phase=metadata|identifier={clean(identifier)}|kind={clean(kind)}|"
            f"message={clean(message)}"
        )

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for result in executor.map(lambda args: scan_one(*args), jobs):
            results.append(result)

    hit_count = sum(
        len((r.get("primary") or {}).get("hits", []))
        + len((r.get("joliet") or {}).get("hits", []))
        for r in results
    )
    print(f"COUNT|metadata_errors|{len(metadata_errors)}")
    print(f"COUNT|images_selected|{len(jobs)}")
    print(f"COUNT|scan_errors|{sum(bool(r['error']) for r in results)}")
    print(f"COUNT|images_scanned|{sum(not r['error'] for r in results)}")
    print(f"COUNT|stoneage_hits|{hit_count}")

    for r in results:
        base = (
            f"identifier={clean(r['identifier'])}|name={clean(r['name'])}|size={r['size']}|"
            f"md5={clean(r['md5'])}|sha1={clean(r['sha1'])}"
        )
        if r["error"]:
            print(f"SCAN_ERROR|{base}|message={clean(r['error'])}")
            continue
        print(
            f"IMAGE|{base}|layout={clean(r['layout'])}|volume={clean(r['volume'])}|"
            f"requests={r['requests']}|bytes_read={r['bytes_read']}|"
            f"primary_entries={r['primary']['entries']}|primary_dirs={r['primary']['dirs']}|"
            f"joliet={int(r['joliet'] is not None)}|"
            f"joliet_entries={(r['joliet'] or {}).get('entries', 0)}|"
            f"truncated={int(r['primary']['truncated'] or bool((r['joliet'] or {}).get('truncated', False)))}"
        )
        emitted = 0
        for namespace in ("primary", "joliet"):
            tree = r.get(namespace)
            if not tree:
                continue
            for path, size, is_dir in tree["hits"]:
                print(
                    f"HIT|namespace={namespace}|identifier={clean(r['identifier'])}|"
                    f"image={clean(r['name'])}|path={clean(path)}|size={size}|directory={int(is_dir)}"
                )
                emitted += 1
        if emitted == 0:
            for path in r["primary"]["samples"][:12]:
                print(
                    f"SAMPLE|identifier={clean(r['identifier'])}|"
                    f"image={clean(r['name'])}|path={clean(path, 360)}"
                )


if __name__ == "__main__":
    main()
