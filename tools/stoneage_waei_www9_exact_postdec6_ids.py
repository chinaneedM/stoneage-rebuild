#!/usr/bin/env python3
"""Probe exact Waei www9 download IDs immediately after the Dec-2000 catalogue snapshot.

Source-derived anchor:
- preserved 2000-12-06 www9 download catalogue lists trial-download IDs 33 and 34;
- first-party Waei reporting says Mainland players were obtaining the StoneAge
  test client by long download by 2001-01-04;
- a later player diary describes the Jan-04 trial as roughly 274 MB.

Previous probes queried the downloading.php?ID= prefix and received zero rows.
This probe deliberately tests exact dynamic URLs, because old Wayback query-string
captures can be discoverable by exact URL even when a prefix query is empty.

Metadata/redirect headers only. Candidate payload bodies are never fetched.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
FROM = "20001207"
TO = "20010112"
IDS = range(35, 61)
WORKERS = 6


def clean(v, n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]


def fetch(url, timeout=18, max_bytes=1024 * 1024):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json,text/html,*/*;q=0.2",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r, "status", r.getcode())), r.geturl(), dict(r.headers.items()), body


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def nofollow(url, timeout=18):
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "*/*", "Accept-Encoding": "identity"},
        method="GET",
    )
    try:
        with opener.open(req, timeout=timeout) as r:
            r.read(1)
            return int(getattr(r, "status", r.getcode())), dict(r.headers.items()), r.geturl()
    except urllib.error.HTTPError as exc:
        return int(exc.code), dict(exc.headers.items()), url


def exact_original(fid):
    return f"http://www9.waei.net:80/download/downloading.php?ID={fid}"


def cdx_url(fid):
    params = [
        ("url", exact_original(fid)),
        ("matchType", "exact"),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from", FROM),
        ("to", TO),
        ("limit", "5000"),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def rows(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, row)) for row in obj[1:] if isinstance(row, list))


def replay_url(ts, orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def query_id(fid):
    status, final, headers, body = fetch(cdx_url(fid))
    return fid, status, final, body, rows(body)


def main():
    print("StoneAge Waei www9 exact post-Dec6 download-ID probe — R1")
    print(
        f"SCOPE|exact downloading.php IDs {min(IDS)}..{max(IDS)}|window={FROM}..{TO}|"
        f"parallel={WORKERS}|CDX + no-follow redirect headers|no target payload"
    )
    print("ANCHOR|2000-12-06 preserved trial catalogue uses IDs 33,34; StoneAge Mainland download confirmed by first-party 2001-01-04 report")
    print("SEARCH_RATIONALE|prefix-ID CDX was zero; exact dynamic query-string URLs remain untested")

    errors = []
    all_rows = {}
    completed = 0
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(query_id, fid): fid for fid in IDS}
        for future in concurrent.futures.as_completed(futures):
            fid = futures[future]
            try:
                results[fid] = future.result()
            except Exception as exc:
                errors.append((f"cdx:{fid}", type(exc).__name__, str(exc)))

    for fid in IDS:
        if fid not in results:
            continue
        _, status, final, body, rr = results[fid]
        completed += 1
        print(
            f"CDX|id={fid}|status={status}|rows={len(rr)}|bytes={len(body)}|"
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

    redirects = 0
    locations = []
    for (fid, ts, orig, digest), r in sorted(all_rows.items()):
        status = str(r.get("statuscode") or "")
        print(
            f"ROW|id={fid}|timestamp={ts}|status={clean(status)}|mime={clean(r.get('mimetype'))}|"
            f"length={clean(r.get('length'))}|digest={clean(digest)}|"
            f"redirect_meta={clean(r.get('redirect'))}|original={clean(orig)}"
        )
        if status in ("301", "302", "303", "307", "308"):
            redirects += 1
            try:
                st, hdrs, final = nofollow(replay_url(ts, orig))
                loc = hdrs.get("Location") or hdrs.get("location") or ""
                if loc:
                    locations.append((fid, ts, loc))
                print(
                    f"HEADER|id={fid}|timestamp={ts}|status={st}|location={clean(loc)}|"
                    f"content_type={clean(hdrs.get('Content-Type'))}|"
                    f"content_length={clean(hdrs.get('Content-Length'))}"
                )
            except Exception as exc:
                errors.append((f"header:{fid}:{ts}", type(exc).__name__, str(exc)))

    for scope, kind, msg in sorted(errors):
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")

    ids_with_rows = sorted({key[0] for key in all_rows})
    print(f"COUNT|ids_tested|{len(tuple(IDS))}")
    print(f"COUNT|queries_completed|{completed}")
    print(f"COUNT|rows|{len(all_rows)}")
    print(f"COUNT|ids_with_rows|{len(ids_with_rows)}")
    print(f"IDS_WITH_ROWS|{','.join(map(str, ids_with_rows))}")
    print(f"COUNT|redirect_rows|{redirects}")
    print(f"COUNT|locations_recovered|{len(locations)}")
    for fid, ts, loc in locations:
        print(f"LOCATION|id={fid}|timestamp={ts}|url={clean(loc)}")
    print(f"COUNT|errors|{len(errors)}")

    if locations:
        print("RESOLUTION|EXACT_WWW9_REDIRECT_TARGETS_RECOVERED|classify target filenames/sizes against StoneAge trial semantics")
    elif all_rows:
        print("RESOLUTION|EXACT_WWW9_ID_ROWS_RECOVERED|classify surviving rows before expanding ID range")
    elif errors and completed < len(tuple(IDS)):
        print("RESOLUTION|EXACT_WWW9_ID_PROBE_PARTIAL|retry failed exact IDs only")
    else:
        print("RESOLUTION|EXACT_WWW9_IDS35_60_BOUNDED|no indexed dynamic rows in tested launch window; switch to external mirror/index evidence")

    print("EVIDENCE_BOUNDARY|ID adjacency is a search heuristic only. No missing ID is assigned to StoneAge without direct title/route evidence.")


if __name__ == "__main__":
    main()
