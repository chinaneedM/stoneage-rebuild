#!/usr/bin/env python3
"""Retry only failed exact Waei www9 launch-window IDs from R1.

Parent R1 completed IDs 35..49 and 51..54 with zero rows. Only
50 and 55..60 failed due transient Wayback timeout/connection refusal.
This residual probe retries exactly those seven identities, serially and
with bounded backoff. Metadata/redirect headers only; no payload bodies.
"""
from __future__ import annotations

import hashlib
import time

from tools.stoneage_waei_www9_exact_postdec6_ids import (
    clean,
    fetch,
    cdx_url,
    rows,
    replay_url,
    nofollow,
)

IDS = (50, 55, 56, 57, 58, 59, 60)
ATTEMPTS = 2


def main():
    print("StoneAge Waei www9 exact post-Dec6 download-ID residual — R2")
    print("PARENT|STONEAGE-WAEI-WWW9-EXACT-POSTDEC6-IDS-R1|retry failed IDs only")
    print(f"SCOPE|exact IDs={','.join(map(str, IDS))}|attempts={ATTEMPTS}|serial bounded retry|no target payload")
    errors = []
    results = {}
    all_rows = {}

    for fid in IDS:
        last = None
        for attempt in range(1, ATTEMPTS + 1):
            try:
                status, final, headers, body = fetch(cdx_url(fid), timeout=22)
                rr = rows(body)
                results[fid] = (status, final, body, rr, attempt)
                break
            except Exception as exc:
                last = (type(exc).__name__, str(exc))
                print(f"RETRY_ERROR|id={fid}|attempt={attempt}|kind={clean(last[0])}|message={clean(last[1])}")
                if attempt < ATTEMPTS:
                    time.sleep(2)
        if fid not in results and last:
            errors.append((fid, last[0], last[1]))

    for fid in IDS:
        if fid not in results:
            continue
        status, final, body, rr, attempt = results[fid]
        print(
            f"CDX|id={fid}|attempt={attempt}|status={status}|rows={len(rr)}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}"
        )
        for r in rr:
            key = (
                fid,
                str(r.get("timestamp") or ""),
                str(r.get("original") or ""),
                str(r.get("digest") or ""),
            )
            all_rows[key] = r

    locations = []
    for (fid, ts, orig, digest), r in sorted(all_rows.items()):
        status = str(r.get("statuscode") or "")
        print(
            f"ROW|id={fid}|timestamp={ts}|status={clean(status)}|mime={clean(r.get('mimetype'))}|"
            f"length={clean(r.get('length'))}|digest={clean(digest)}|"
            f"redirect_meta={clean(r.get('redirect'))}|original={clean(orig)}"
        )
        if status in ("301", "302", "303", "307", "308"):
            try:
                st, hdrs, final = nofollow(replay_url(ts, orig), timeout=22)
                loc = hdrs.get("Location") or hdrs.get("location") or ""
                if loc:
                    locations.append((fid, ts, loc))
                print(
                    f"HEADER|id={fid}|timestamp={ts}|status={st}|location={clean(loc)}|"
                    f"content_type={clean(hdrs.get('Content-Type'))}|"
                    f"content_length={clean(hdrs.get('Content-Length'))}"
                )
            except Exception as exc:
                errors.append((fid, type(exc).__name__, str(exc)))

    ids_with_rows = sorted({key[0] for key in all_rows})
    for fid, kind, msg in errors:
        print(f"ERROR|id={fid}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|ids_tested|{len(IDS)}")
    print(f"COUNT|queries_completed|{len(results)}")
    print(f"COUNT|rows|{len(all_rows)}")
    print(f"COUNT|ids_with_rows|{len(ids_with_rows)}")
    print(f"IDS_WITH_ROWS|{','.join(map(str, ids_with_rows))}")
    print(f"COUNT|locations_recovered|{len(locations)}")
    for fid, ts, loc in locations:
        print(f"LOCATION|id={fid}|timestamp={ts}|url={clean(loc)}")
    print(f"COUNT|errors|{len(errors)}")

    if locations:
        print("RESOLUTION|EXACT_WWW9_RESIDUAL_REDIRECTS_RECOVERED|classify target filenames and sizes")
    elif all_rows:
        print("RESOLUTION|EXACT_WWW9_RESIDUAL_ROWS_RECOVERED|classify rows before any range expansion")
    elif len(results) == len(IDS):
        print("RESOLUTION|EXACT_WWW9_IDS35_60_BOUNDED|R1 plus R2 completed all exact IDs with zero rows; switch to external mirror/index evidence")
    else:
        print("RESOLUTION|EXACT_WWW9_RESIDUAL_PARTIAL|retain only still-failed IDs as open")

    print("EVIDENCE_BOUNDARY|Zero indexed rows bound this exact Wayback route only; they do not negate the documented Jan-2001 trial download.")


if __name__ == "__main__":
    main()
