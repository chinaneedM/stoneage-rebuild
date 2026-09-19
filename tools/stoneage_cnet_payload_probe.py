#!/usr/bin/env python3
"""Probe archive availability and prefix metadata for the recovered CNET StoneAge payload.

Known historical CNET payload path:
    /pc/games/online/stoneage.zip
Known detail-page size label:
    257MB

This probe never downloads the complete archive. If an archived capture is found,
it reads at most 64 response-body bytes to identify container magic and records
response metadata only.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
AVAILABLE = "https://archive.org/wayback/available"
DATES = ["20000926", "20001004", "20001013", "20001110", "20001201", "20001211", "20010109", "20010418"]
PAYLOADS = [
    "http://korea.cnet.com/pc/games/online/stoneage.zip",
    "http://www.korea.cnet.com/pc/games/online/stoneage.zip",
]


def request(url: str, *, timeout: int = 10, headers: dict | None = None, read_limit: int | None = None):
    merged = {"User-Agent": UA}
    if headers:
        merged.update(headers)
    req = urllib.request.Request(url, headers=merged)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read() if read_limit is None else response.read(read_limit)
        return response, body


def closest(payload: dict):
    c = payload.get("archived_snapshots", {}).get("closest")
    if not isinstance(c, dict) or not c.get("available"):
        return None
    return {
        "timestamp": str(c.get("timestamp", "")),
        "status": str(c.get("status", "")),
        "url": str(c.get("url", "")),
    }


def availability(original: str, requested: str):
    q = urllib.parse.urlencode({"url": original, "timestamp": requested})
    _, body = request(AVAILABLE + "?" + q, timeout=8)
    return closest(json.loads(body.decode("utf-8", "replace")))


def id_url(timestamp: str, original: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def prefix_probe(timestamp: str, original: str):
    url = id_url(timestamp, original)
    response, body = request(
        url,
        timeout=15,
        headers={"Range": "bytes=0-63", "Accept-Encoding": "identity"},
        read_limit=64,
    )
    return {
        "http_status": str(getattr(response, "status", "")),
        "content_type": str(response.headers.get("Content-Type", "")),
        "content_length": str(response.headers.get("Content-Length", "")),
        "content_range": str(response.headers.get("Content-Range", "")),
        "magic_hex": body[:16].hex(),
        "prefix_len": str(len(body)),
        "prefix_sha256": hashlib.sha256(body).hexdigest(),
    }


def safe(value: str, limit: int = 700) -> str:
    value = " ".join(str(value).split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f")[:limit]


def main():
    print("StoneAge CNET Korea payload availability probe — R1")
    print("PAYLOAD|path=/pc/games/online/stoneage.zip|detail_page_size_label=257MB")
    print("SCOPE|archive-metadata-and-64-byte-prefix-only|no-complete-binary-download")

    jobs = [(original, date) for original in PAYLOADS for date in DATES]

    def one(job):
        original, date = job
        try:
            hit = availability(original, date)
        except Exception as exc:
            return ("error", original, date, type(exc).__name__, str(exc))
        if not hit:
            return ("miss", original, date, "", "")
        return ("hit", original, date, hit["timestamp"], hit["status"], hit["url"])

    hits = {}
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        for result in ex.map(one, jobs):
            if result[0] == "error":
                _, original, date, kind, message = result
                errors.append(("availability", original, date, kind, message))
            elif result[0] == "hit":
                _, original, date, timestamp, status, archived = result
                hits[(timestamp, original)] = (status, archived)

    print(f"COUNT|availability_queries|{len(jobs)}")
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|unique_available_snapshots|{len(hits)}")

    for phase, original, date, kind, message in errors:
        print(
            f"ERROR|phase={phase}|requested={date}|kind={kind}|"
            f"original={safe(original)}|message={safe(message)}"
        )

    for (timestamp, original), (status, archived) in sorted(hits.items()):
        print(
            f"SNAPSHOT|timestamp={timestamp}|status={safe(status)}|"
            f"original={safe(original)}|archived={safe(archived)}"
        )

    prefix_rows = []
    for timestamp, original in sorted(hits):
        try:
            meta = prefix_probe(timestamp, original)
        except Exception as exc:
            print(
                f"ERROR|phase=prefix|timestamp={timestamp}|kind={type(exc).__name__}|"
                f"original={safe(original)}|message={safe(exc)}"
            )
            continue
        prefix_rows.append((timestamp, original, meta))

    print(f"COUNT|prefix_probes|{len(prefix_rows)}")
    for timestamp, original, meta in prefix_rows:
        print(
            "PREFIX|"
            f"timestamp={timestamp}|original={safe(original)}|"
            f"http_status={safe(meta['http_status'])}|content_type={safe(meta['content_type'])}|"
            f"content_length={safe(meta['content_length'])}|content_range={safe(meta['content_range'])}|"
            f"prefix_len={safe(meta['prefix_len'])}|magic_hex={safe(meta['magic_hex'])}|"
            f"prefix_sha256={safe(meta['prefix_sha256'])}"
        )


if __name__ == "__main__":
    main()
