#!/usr/bin/env python3
"""Scan GamePia legacy disc issues around the Korean StoneAge 2000-2001 transition.

Reads only remote ISO-9660/Joliet directory sectors via HTTP Range requests.
No complete disc image is downloaded or committed.
"""

from __future__ import annotations

import concurrent.futures
import re

from tools.stoneage_netpower_remote_iso_scan import clean, metadata, scan_one

IDENTIFIER="GAMEPIA_cd_dump"
ISSUE=re.compile(r"(?i)(?:^|/)No\.(?:58|59|60|61|62|63|64|65|66|67|68|69|70|71|72|73|74)(?:/|$)")
IMAGE=re.compile(r"(?i)\.(?:iso|img|bin|mdf)$")
MAX_IMAGES=40


def selected_name(name):
    return bool(ISSUE.search(name) and IMAGE.search(name))


def select_files(data):
    rows=[]
    for f in data.get("files",[]):
        name=str(f.get("name",""))
        if not selected_name(name):
            continue
        size=int(f.get("size") or 0)
        if size<10*1024*1024:
            continue
        rows.append({
            "name":name,
            "size":size,
            "md5":str(f.get("md5","")),
            "sha1":str(f.get("sha1","")),
            "format":str(f.get("format","")),
        })
    return sorted(rows,key=lambda x:x["name"].lower())[:MAX_IMAGES]


def main():
    print("StoneAge GamePia transition-window directory scan — R1")
    print("SCOPE|http-range-directory-metadata-only|no-full-image-download|no-carrier-bytes-committed")
    print("WINDOW|legacy-issues=No.58..No.74|through-2001-12-public-corpus")
    data=metadata(IDENTIFIER)
    doc=data.get("metadata",{})
    rows=select_files(data)
    print(f"ITEM|identifier={IDENTIFIER}|title={clean(doc.get('title'))}|selected_images={len(rows)}")
    for f in rows:
        print(
            f"TARGET|name={clean(f['name'])}|size={f['size']}|md5={clean(f['md5'])}|"
            f"sha1={clean(f['sha1'])}|format={clean(f['format'])}"
        )

    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(lambda f:scan_one(IDENTIFIER,doc,f),rows):
            results.append(res)

    hits=sum(
        len((r.get("primary") or {}).get("hits",[]))+
        len((r.get("joliet") or {}).get("hits",[]))
        for r in results
    )
    print(f"COUNT|scan_errors|{sum(bool(r['error']) for r in results)}")
    print(f"COUNT|images_scanned|{sum(not r['error'] for r in results)}")
    print(f"COUNT|stoneage_hits|{hits}")

    for r in results:
        base=(
            f"name={clean(r['name'])}|size={r['size']}|md5={clean(r['md5'])}|"
            f"sha1={clean(r['sha1'])}"
        )
        if r["error"]:
            print(f"SCAN_ERROR|{base}|message={clean(r['error'])}")
            continue
        print(
            f"IMAGE|{base}|layout={clean(r['layout'])}|volume={clean(r['volume'])}|"
            f"requests={r['requests']}|bytes_read={r['bytes_read']}|"
            f"primary_entries={r['primary']['entries']}|primary_dirs={r['primary']['dirs']}|"
            f"joliet={int(r['joliet'] is not None)}|"
            f"joliet_entries={(r['joliet'] or {}).get('entries',0)}|"
            f"truncated={int(r['primary']['truncated'] or bool((r['joliet'] or {}).get('truncated',False)))}"
        )
        emitted=0
        for namespace in ("primary","joliet"):
            tree=r.get(namespace)
            if not tree:
                continue
            for path,size,is_dir in tree["hits"]:
                print(
                    f"HIT|namespace={namespace}|image={clean(r['name'])}|"
                    f"path={clean(path)}|size={size}|directory={int(is_dir)}"
                )
                emitted+=1
        if emitted==0:
            for path in r["primary"]["samples"][:8]:
                print(f"SAMPLE|image={clean(r['name'])}|path={clean(path,360)}")


if __name__=="__main__":
    main()
