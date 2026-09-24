#!/usr/bin/env python3
"""Resolve the single timed-out IA item from the Taiwan-v1 installed-tree scan."""

from __future__ import annotations

import time

from tools.stoneage_tw10_archive_installed_tree_probe import (
    clean,
    inspect_files,
    metadata,
)

TARGET="NPWK19720801"
ATTEMPTS=4


def main():
    print("StoneAge Taiwan v1 Internet Archive timeout retry — R1")
    print("SCOPE|single-item-metadata-retry|completes-installed-tree-scan-boundary|no-payload-download")
    data=None
    errors=[]
    for attempt in range(1,ATTEMPTS+1):
        try:
            data=metadata(TARGET)
            print(f"ATTEMPT|n={attempt}|status=success")
            break
        except Exception as exc:
            errors.append((type(exc).__name__,str(exc)))
            print(f"ATTEMPT|n={attempt}|status=error|kind={type(exc).__name__}|message={clean(exc)}")
            if attempt<ATTEMPTS:
                time.sleep(1)

    if data is None:
        print(f"COUNT|attempts|{ATTEMPTS}")
        print("RESOLUTION|INCONCLUSIVE|timed-out item remains unavailable")
        return

    meta=data.get("metadata",{})
    signatures,maps=inspect_files(data.get("files",[]))
    title=clean(meta.get("title"))
    description=clean(meta.get("description"),2000)
    mediatype=clean(meta.get("mediatype"))
    print(
        f"ITEM|identifier={TARGET}|title={title}|mediatype={mediatype}|"
        f"files={len(data.get('files',[]))}|signatures={len(signatures)}|map_dat={len(maps)}"
    )
    print(f"DESCRIPTION_FINGERPRINT|sha256={__import__('hashlib').sha256(description.encode('utf-8')).hexdigest()}|chars={len(description)}")
    for entry in signatures:
        print(
            f"SIGNATURE_HIT|path={clean(entry.get('name'),1800)}|size={clean(entry.get('size'))}|"
            f"md5={clean(entry.get('md5'))}|sha1={clean(entry.get('sha1'))}"
        )
    for entry in maps[:200]:
        print(
            f"MAP_HIT|path={clean(entry.get('name'),1800)}|size={clean(entry.get('size'))}|"
            f"md5={clean(entry.get('md5'))}|sha1={clean(entry.get('sha1'))}"
        )
    print(f"COUNT|attempts_used|{len(errors)+1}")
    if signatures or maps:
        print("RESOLUTION|TIMED_OUT_ITEM_HAS_TARGET_TRAITS|inspect provenance before use")
    else:
        print("RESOLUTION|TIMED_OUT_ITEM_CLEARED|no Taiwan-v1 signatures or map/<n>.dat in file list")


if __name__=="__main__":
    main()
