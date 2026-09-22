#!/usr/bin/env python3
"""Probe Wayback CDX prefix neighborhoods around the Japan 1.74a launch payload.

This probe stores index metadata only. It does not replay or download the client.
The goal is to catch URL normalization, redirects, and sibling executable records
that exact-URL probes can miss.
"""

from __future__ import annotations

import concurrent.futures
import json
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX = "https://web.archive.org/cdx/search/cdx"
LIMIT = 2500

PREFIXES = (
    ("gamania-http", "http://hangame.gamania.co.jp/stoneage/"),
    ("gamania-http-www", "http://www.hangame.gamania.co.jp/stoneage/"),
    ("gamania-https", "https://hangame.gamania.co.jp/stoneage/"),
    ("gamania-https-www", "https://www.hangame.gamania.co.jp/stoneage/"),
    ("hangame-publish-http", "http://www.hangame.co.jp/publish/sa/"),
    ("hangame-publish-http-bare", "http://hangame.co.jp/publish/sa/"),
    ("hangame-publish-https", "https://www.hangame.co.jp/publish/sa/"),
    ("hangame-publish-https-bare", "https://hangame.co.jp/publish/sa/"),
)

PINNED = {
    "sa174hg.exe",
    "stoneage.exe",
    "sadl.asp",
    "sasetup.asp",
    "sasetup2.asp",
    "hgsa.cab",
}


def clean(value, limit=1200):
    value = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def get(url, timeout=18):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json,text/plain,*/*",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def parse_cdx(data):
    text = data.decode("utf-8", "replace").strip()
    if not text:
        return []
    obj = json.loads(text)
    if not isinstance(obj, list) or not obj:
        return []
    if isinstance(obj[0], list):
        header = [str(x) for x in obj[0]]
        return [
            {header[i]: str(row[i]) if i < len(row) else "" for i in range(len(header))}
            for row in obj[1:]
            if isinstance(row, list)
        ]
    return [row for row in obj if isinstance(row, dict)]


def query_url(prefix):
    params = [
        ("url", prefix),
        ("matchType", "prefix"),
        ("from", "2003"),
        ("to", "2005"),
        ("output", "json"),
        ("fl", "timestamp,original,mimetype,statuscode,digest,length,redirect"),
        ("limit", str(LIMIT)),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def query_one(label, prefix):
    try:
        rows = parse_cdx(get(query_url(prefix)))
        return label, prefix, rows, None
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 429, 502, 503, 504):
            return label, prefix, [], (type(exc).__name__, str(exc))
        raise
    except Exception as exc:
        return label, prefix, [], (type(exc).__name__, str(exc))


def basename(url):
    try:
        path = urllib.parse.urlsplit(str(url)).path
    except Exception:
        path = str(url).split("?", 1)[0]
    return path.rstrip("/").rsplit("/", 1)[-1].lower()


def is_exact_payload(url):
    return basename(url) == "sa174hg.exe"


def is_relevant(url):
    base = basename(url)
    return base in PINNED or base.endswith((".exe", ".cab"))


def normalize(row):
    return {
        "timestamp": str(row.get("timestamp", "")),
        "original": str(row.get("original", "")),
        "mime": str(row.get("mimetype", "")),
        "status": str(row.get("statuscode", "")),
        "digest": str(row.get("digest", "")),
        "length": str(row.get("length", "")),
        "redirect": str(row.get("redirect", "")),
    }


def resolution(exact_hits, errors, saturated):
    if exact_hits:
        return "EXACT_FILENAME_INDEXED"
    if errors or saturated:
        return "INCONCLUSIVE"
    return "BOUNDED_NO_PREFIX_INDEX_HIT"


def main():
    print("StoneAge Japan 1.74a Wayback prefix-neighborhood probe — R1")
    print("SCOPE|cdx-prefix-index-metadata-only|2003-2005|no-replay|no-client-download")
    print("PROVENANCE|exact payload name=sa174hg.exe|official launch page=sadl.asp@20031214051053")
    print(f"LIMIT|rows_per_prefix|{LIMIT}")

    results = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(query_one, label, prefix) for label, prefix in PREFIXES]
        for fut in futures:
            label, prefix, rows, error = fut.result()
            saturated = len(rows) >= LIMIT
            relevant = [normalize(row) for row in rows if is_relevant(row.get("original", ""))]
            exact = [row for row in relevant if is_exact_payload(row["original"])]
            results.append((label, prefix, len(rows), saturated, relevant, exact))
            if error:
                errors.append((label, prefix, error[0], error[1]))

    total_exact = sum(len(x[5]) for x in results)
    any_saturated = any(x[3] for x in results)

    print(f"COUNT|prefixes|{len(PREFIXES)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|raw_rows|{sum(x[2] for x in results)}")
    print(f"COUNT|relevant_rows|{sum(len(x[4]) for x in results)}")
    print(f"COUNT|exact_sa174hg_rows|{total_exact}")
    print(f"COUNT|saturated_prefixes|{sum(1 for x in results if x[3])}")

    for label, prefix, kind, message in sorted(errors):
        print(
            f"ERROR|target={clean(label)}|kind={clean(kind)}|prefix={clean(prefix)}|"
            f"message={clean(message)}"
        )

    emitted = set()
    for label, prefix, raw_count, saturated, relevant, exact in results:
        print(
            f"PREFIX|label={clean(label)}|raw_rows={raw_count}|saturated={int(saturated)}|"
            f"relevant_rows={len(relevant)}|exact_sa174hg_rows={len(exact)}|prefix={clean(prefix)}"
        )
        for row in relevant:
            rec = (
                label,
                row["timestamp"],
                row["status"],
                row["mime"],
                row["length"],
                row["digest"],
                row["original"],
                row["redirect"],
            )
            emitted.add(rec)

    for rec in sorted(emitted):
        label, timestamp, status, mime, length, digest, original, redirect = rec
        print(
            f"RESULT|prefix={clean(label)}|timestamp={clean(timestamp)}|status={clean(status)}|"
            f"mime={clean(mime)}|length={clean(length)}|digest={clean(digest)}|"
            f"original={clean(original)}|redirect={clean(redirect)}"
        )

    state = resolution(total_exact, errors, any_saturated)
    if state == "EXACT_FILENAME_INDEXED":
        print("RESOLUTION|EXACT_FILENAME_INDEXED|inspect returned capture metadata before any payload claim")
    elif state == "INCONCLUSIVE":
        print("RESOLUTION|INCONCLUSIVE|prefix surface incomplete; absence cannot be interpreted")
    else:
        print("RESOLUTION|BOUNDED_NO_PREFIX_INDEX_HIT|no indexed sa174hg.exe in completed prefixes; does not disprove an unindexed file or mirror")


if __name__ == "__main__":
    main()
