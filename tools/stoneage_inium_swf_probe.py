#!/usr/bin/env python3
"""Probe archived Inium StoneAge main.swf for sparse recovery tokens.

The SWF is fetched transiently from a period Wayback snapshot and is never
committed. The report stores only hashes/container metadata and sparse ASCII
URL/path/file tokens useful for clean-client recovery.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import struct
import urllib.parse
import urllib.request
import zlib

UA = "stoneage-rebuild-archaeology/1.0"
AVAILABLE = "https://archive.org/wayback/available"

URLS = [
    "http://stoneage.enium.co.kr/main.swf",
    "http://www.stoneage.enium.co.kr/main.swf",
]
DATES = ["20001109", "20001201", "20010201", "20010401"]

ASCII_TOKEN = re.compile(
    rb"""(?ix)
    (?:
        https?://[a-z0-9][a-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{3,}
      | ftp://[a-z0-9][a-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{3,}
      | www\.[a-z0-9][a-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{3,}
      | [a-z0-9_./-]{1,180}\.(?:exe|zip|rar|cab|lzh|lha|msi|html?|asp|php|swf)
    )
    """
)
KEY = re.compile(rb"(?i)(stoneage|enium|inium|download|setup|install|patch|update|client)")


def request(url: str, timeout: int = 12) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def availability(original: str, requested: str):
    q = urllib.parse.urlencode({"url": original, "timestamp": requested})
    data = json.loads(request(AVAILABLE + "?" + q, timeout=8).decode("utf-8", "replace"))
    c = data.get("archived_snapshots", {}).get("closest")
    if not isinstance(c, dict) or not c.get("available"):
        return None
    return str(c.get("timestamp", "")), str(c.get("status", "")), str(c.get("url", ""))


def id_url(timestamp: str, original: str):
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def unpack_swf(data: bytes):
    if len(data) < 8:
        raise ValueError("SWF too short")
    sig = data[:3]
    version = data[3]
    declared = struct.unpack("<I", data[4:8])[0]
    if sig == b"FWS":
        body = data
    elif sig == b"CWS":
        body = b"FWS" + data[3:8] + zlib.decompress(data[8:])
    else:
        # ZWS/LZMA is not decompressed here; raw bytes may still expose strings.
        body = data
    return sig.decode("ascii", "replace"), version, declared, body


def tokens(data: bytes):
    found = set()
    for m in ASCII_TOKEN.finditer(data):
        value = m.group(0).decode("latin-1", "replace").strip(" .,:;\"'()[]{}")
        if value:
            found.add(("path", value))
    # Also retain short printable keyword-bearing chunks when no extension is present.
    for chunk in re.findall(rb"[\x20-\x7e]{4,220}", data):
        if KEY.search(chunk):
            value = chunk.decode("latin-1", "replace").strip()
            if value:
                found.add(("keyword_chunk", value))
    return found


def safe(value: str, limit: int = 500):
    value = " ".join(value.split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f")[:limit]


def main():
    print("StoneAge Inium main.swf archive token probe — R1")
    print("SCOPE|transient-swf-analysis|hash-container-sparse-tokens-only|no-swf-bytes-committed")

    jobs = [(u, d) for u in URLS for d in DATES]

    def one(job):
        u, d = job
        try:
            hit = availability(u, d)
            return u, d, hit, None
        except Exception as exc:
            return u, d, None, (type(exc).__name__, str(exc))

    hits = {}
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for u, d, hit, err in ex.map(one, jobs):
            if err:
                errors.append(("availability", u, d, err[0], err[1]))
            elif hit:
                ts, status, archived = hit
                hits[(ts, u)] = (status, archived)

    print(f"COUNT|availability_queries|{len(jobs)}")
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|unique_snapshots|{len(hits)}")

    all_tokens = set()
    for (ts, original), (status, archived) in sorted(hits.items()):
        print(
            f"SNAPSHOT|timestamp={ts}|status={safe(status)}|original={safe(original)}|archived={safe(archived)}"
        )
        try:
            data = request(id_url(ts, original), timeout=15)
            sig, version, declared, unpacked = unpack_swf(data)
        except Exception as exc:
            errors.append(("snapshot", original, ts, type(exc).__name__, str(exc)))
            continue
        print(
            f"SWF|timestamp={ts}|original={safe(original)}|sha256={hashlib.sha256(data).hexdigest()}|"
            f"bytes={len(data)}|signature={sig}|version={version}|declared_uncompressed_bytes={declared}|"
            f"analyzed_bytes={len(unpacked)}"
        )
        for kind, value in tokens(unpacked):
            all_tokens.add((ts, original, kind, safe(value)))

    for phase, original, marker, kind, message in errors:
        print(
            f"ERROR|phase={phase}|marker={safe(marker)}|kind={kind}|"
            f"original={safe(original)}|message={safe(message)}"
        )

    print(f"COUNT|snapshot_errors|{sum(1 for e in errors if e[0]=='snapshot')}")
    print(f"COUNT|tokens|{len(all_tokens)}")
    for ts, original, kind, value in sorted(all_tokens):
        print(f"TOKEN|timestamp={ts}|kind={kind}|original={safe(original)}|value={value}")


if __name__ == "__main__":
    main()
