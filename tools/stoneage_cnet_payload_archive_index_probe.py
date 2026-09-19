#!/usr/bin/env python3
"""Probe exact archive indexes for the recovered CNET Korea StoneAge payload path.

This stores only archive-index/search metadata. It does not download the client.
"""

from __future__ import annotations

import concurrent.futures
import json
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
ARQUIVO = "https://arquivo.pt/textsearch"

EXACT_URLS = [
    "http://korea.cnet.com/pc/games/online/stoneage.zip",
    "http://www.korea.cnet.com/pc/games/online/stoneage.zip",
]
CDX_PATTERNS = EXACT_URLS + [
    "korea.cnet.com/*stoneage.zip",
    "www.korea.cnet.com/*stoneage.zip",
]
ARQUIVO_QUERIES = [
    '"http://korea.cnet.com/pc/games/online/stoneage.zip"',
    '"/pc/games/online/stoneage.zip"',
    '"stoneage.zip" "korea.cnet.com"',
    '"stoneage.zip" "스톤에이지"',
]


def fetch_json(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def cdx_query(pattern: str):
    params = {
        "url": pattern,
        "from": "2000",
        "to": "2003",
        "output": "json",
        "fl": "timestamp,original,statuscode,mimetype,digest,length",
        "filter": "statuscode:200",
        "collapse": "digest",
        "limit": "500",
    }
    rows = fetch_json(CDX + "?" + urllib.parse.urlencode(params), timeout=10)
    if not rows:
        return []
    header, *body = rows
    out = []
    for row in body:
        if not isinstance(row, list) or len(row) < len(header):
            continue
        out.append(dict(zip(header, row)))
    return out


def arquivo_query(query: str):
    params = {
        "q": query,
        "from": "2000",
        "to": "2003",
        "maxItems": "50",
        "prettyPrint": "false",
    }
    data = fetch_json(ARQUIVO + "?" + urllib.parse.urlencode(params), timeout=10)
    return list(data.get("response_items", []))


def clean(value, limit=800):
    value = "" if value is None else str(value)
    value = " ".join(value.split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f")[:limit]


def main():
    print("StoneAge CNET payload exact archive-index probe — R1")
    print("PAYLOAD|/pc/games/online/stoneage.zip|detail_page_size_label=257MB")
    print("SCOPE|archive-index-metadata-only|no-client-binary-download")

    jobs = [("cdx", x) for x in CDX_PATTERNS] + [("arquivo", x) for x in ARQUIVO_QUERIES]

    def one(job):
        kind, query = job
        try:
            rows = cdx_query(query) if kind == "cdx" else arquivo_query(query)
            return kind, query, rows, None
        except Exception as exc:
            return kind, query, [], (type(exc).__name__, str(exc))

    results = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for kind, query, rows, error in ex.map(one, jobs):
            if error:
                errors.append((kind, query, error[0], error[1]))
            for row in rows:
                results.append((kind, query, row))

    print(f"COUNT|queries|{len(jobs)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|raw_results|{len(results)}")

    for kind, query, errkind, message in sorted(errors):
        print(
            f"ERROR|source={kind}|query={clean(query)}|kind={errkind}|message={clean(message)}"
        )

    emitted = set()
    for kind, query, row in results:
        if kind == "cdx":
            record = (
                "CDX",
                clean(query),
                clean(row.get("timestamp")),
                clean(row.get("original")),
                clean(row.get("statuscode")),
                clean(row.get("mimetype")),
                clean(row.get("digest")),
                clean(row.get("length")),
            )
        else:
            record = (
                "ARQUIVO",
                clean(query),
                clean(row.get("timestamp") or row.get("date")),
                clean(row.get("originalURL")),
                clean(row.get("title")),
                clean(row.get("mimeType")),
                clean(row.get("contentLength")),
                clean(row.get("linkToArchive")),
            )
        emitted.add(record)

    print(f"COUNT|unique_results|{len(emitted)}")
    for record in sorted(emitted):
        print("RESULT|" + "|".join(record))


if __name__ == "__main__":
    main()
