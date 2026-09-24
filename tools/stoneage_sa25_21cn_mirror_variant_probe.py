#!/usr/bin/env python3
"""Probe Wayback prefix variants of evidence-derived 21CN sa25up.zip mirror URLs.

Historical pages sometimes emitted the target with trailing spaces. Wayback may index
those requests as distinct URL keys. This probe discovers variants and transiently
inspects only plausible HTTP-200 ZIP-sized captures. ZIP bytes are never committed.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.parse

from tools.stoneage_sa25_21cn_mirror_recovery_probe import (
    TARGETS, EXPECTED_MIN, EXPECTED_MAX, MAX_FETCH, clean, fetch, inventory_zip
)

CDX="https://web.archive.org/cdx/search/cdx"


def cdx_prefix_url(url):
    p=[
        ("url",url),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2002"),("to","2006"),("limit","3000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def parse(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    h=data[0]
    return tuple(dict(zip(h,row)) for row in data[1:] if isinstance(row,list))


def intish(v):
    try:
        return int(str(v or "").strip())
    except Exception:
        return None


def plausible(row):
    if str(row.get("statuscode") or "")!="200":
        return False
    n=intish(row.get("length"))
    return n is None or EXPECTED_MIN <= n <= EXPECTED_MAX


def replay_url(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"


def one_query(entry):
    label,url=entry
    try:
        st,final,hdr,b=fetch(cdx_prefix_url(url),28,4_000_000,2)
        return label,url,st,final,b,parse(b),None
    except Exception as exc:
        return label,url,None,None,None,(),(type(exc).__name__,str(exc))


def one_replay(pair):
    label,row=pair
    try:
        st,final,hdr,b=fetch(replay_url(row),45,MAX_FETCH,2)
        return label,row,st,final,hdr,b,None
    except Exception as exc:
        return label,row,None,None,None,None,(type(exc).__name__,str(exc))


def main():
    print("StoneAge 2.5 21CN sa25up URL-variant recovery — R1")
    print("SCOPE|evidence-derived-url-prefixes|trailing-space-query-variant-discovery|transient-replay-only")
    errors=[]; all_rows=[]

    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
        for label,url,st,final,b,rows,error in ex.map(one_query,TARGETS):
            if error:
                errors.append((f"cdx:{label}",error[0],error[1]))
                continue
            print(
                f"CDX_PREFIX|label={label}|base={clean(url)}|status={st}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for r in rows:
                print(
                    f"ROW|label={label}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|"
                    f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
                    f"digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}|"
                    f"plausible={1 if plausible(r) else 0}"
                )
                all_rows.append((label,r))

    candidates=[]; seen=set()
    for label,r in all_rows:
        if not plausible(r):
            continue
        k=(str(r.get("digest") or ""),str(r.get("original") or ""))
        if k in seen:
            continue
        seen.add(k)
        candidates.append((label,r))

    recovered=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for label,r,st,final,hdr,b,error in ex.map(one_replay,candidates):
            ts=str(r.get("timestamp") or "")
            if error:
                errors.append((f"replay:{label}:{ts}",error[0],error[1]))
                continue
            is_zip=b.startswith((b"PK\x03\x04",b"PK\x05\x06",b"PK\x07\x08"))
            print(
                f"REPLAY|label={label}|timestamp={clean(ts)}|original={clean(r.get('original'))}|"
                f"status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|"
                f"md5={hashlib.md5(b).hexdigest()}|content_type={clean(hdr.get('Content-Type'))}|"
                f"magic={b[:4].hex()}|zip={1 if is_zip else 0}|final={clean(final)}"
            )
            if not is_zip:
                continue
            try:
                inv=inventory_zip(b)
            except Exception as exc:
                errors.append((f"zip:{label}:{ts}",type(exc).__name__,str(exc)))
                continue
            recovered.append((label,r,b,inv))
            print(
                f"ZIP|label={label}|timestamp={clean(ts)}|files={sum(not x['is_dir'] for x in inv)}|"
                f"dirs={sum(x['is_dir'] for x in inv)}|uncompressed_bytes={sum(x['size'] for x in inv if not x['is_dir'])}|"
                f"sha256={hashlib.sha256(b).hexdigest()}"
            )
            for n,x in enumerate(inv,1):
                print(
                    f"ENTRY|label={label}|timestamp={clean(ts)}|order={n}|name={clean(x['name'],3000)}|"
                    f"size={x['size']}|compressed={x['compressed']}|crc32={x['crc']}|date={x['date']}|dir={1 if x['is_dir'] else 0}"
                )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|prefix_rows|{len(all_rows)}")
    print(f"COUNT|plausible_200_candidates|{len(candidates)}")
    print(f"COUNT|recovered_zip_captures|{len(recovered)}")
    print(f"COUNT|errors|{len(errors)}")
    if recovered:
        print("RESOLUTION|SA25UP_VARIANT_ZIP_RECOVERED|compare contents against known baselines")
    elif candidates:
        print("RESOLUTION|SA25UP_VARIANT_200_NOT_ZIP_OR_REPLAY_FAILED|inspect candidate metadata")
    elif errors:
        print("RESOLUTION|PARTIAL_VARIANT_SCAN_FAILURE|retry failed prefixes only")
    else:
        print("RESOLUTION|NO_ARCHIVED_200_SA25UP_VARIANT|evidence-derived 21CN prefix variants bounded")
    print("EVIDENCE_BOUNDARY|URL-variant recovery can establish 21CN-distributed bytes only; operator-master equivalence remains separate.")


if __name__=="__main__":
    main()
