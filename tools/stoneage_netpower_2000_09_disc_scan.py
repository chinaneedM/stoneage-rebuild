#!/usr/bin/env python3
"""Remote directory scan of the public NetPower 2000-09 carrier set.

The issue is a high-value StoneAge-adjacent target because the surviving NetPower
contents index places StoneAge in the September 2000 issue. This probe reads only
ISO-9660/Joliet directory sectors through HTTP Range requests; it never downloads
or commits a complete carrier image.
"""

from __future__ import annotations

import concurrent.futures

from tools.stoneage_netpower_exact_target_disc_scan import select_images
from tools.stoneage_netpower_remote_iso_scan import clean, metadata, scan_one

TARGET_ITEM = "netpower_cd_2000_09"


def main():
    print("StoneAge NetPower 2000-09 remote directory scan — R1")
    print("SCOPE|http-range-directory-metadata-only|no-full-image-download|no-carrier-bytes-committed")
    print(f"TARGET_ITEM|{TARGET_ITEM}")

    try:
        data = metadata(TARGET_ITEM)
    except Exception as exc:
        print(
            f"ERROR|phase=metadata|identifier={clean(TARGET_ITEM)}|"
            f"kind={clean(type(exc).__name__)}|message={clean(exc)}"
        )
        print("COUNT|metadata_errors|1")
        print("COUNT|images_selected|0")
        print("COUNT|scan_errors|0")
        print("COUNT|images_scanned|0")
        print("COUNT|stoneage_hits|0")
        return

    doc = data.get("metadata", {})
    images = select_images(data)
    print(
        f"ITEM|identifier={clean(TARGET_ITEM)}|title={clean(doc.get('title'))}|"
        f"date={clean(doc.get('date') or doc.get('year'))}|"
        f"uploader={clean(doc.get('uploader'))}|selected_images={len(images)}"
    )
    for f in images:
        print(
            f"TARGET|identifier={clean(TARGET_ITEM)}|name={clean(f['name'])}|"
            f"size={f['size']}|md5={clean(f['md5'])}|sha1={clean(f['sha1'])}|"
            f"format={clean(f['format'])}"
        )

    jobs = [(TARGET_ITEM, doc, f) for f in images]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for result in executor.map(lambda args: scan_one(*args), jobs):
            results.append(result)

    hit_count = sum(
        len((r.get("primary") or {}).get("hits", []))
        + len((r.get("joliet") or {}).get("hits", []))
        for r in results
    )
    print("COUNT|metadata_errors|0")
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
            for path in r["primary"]["samples"][:16]:
                print(
                    f"SAMPLE|identifier={clean(r['identifier'])}|"
                    f"image={clean(r['name'])}|path={clean(path, 360)}"
                )


if __name__ == "__main__":
    main()
