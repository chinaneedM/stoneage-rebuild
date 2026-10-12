#!/usr/bin/env python3
"""Bounded, hash-pinned recovery of one TW1.0 archive into ephemeral CI disk.

The payload is never logged/uploaded. Each range must match 206 plus exact
Content-Range, and all bytes are MD5/SHA1 checked before any static analysis.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from tools.stoneage_tw10_archive_transport_preflight import (
    ALLOWED_HOST, ARCHIVE_MD5, ARCHIVE_SHA1, FILE, ITEM,
    META_LIMIT, ORIGIN, USER_AGENT, metadata_summary, probe,
)

ARCHIVE_SIZE = 842125501
DEFAULT_RANGE = 16 * 1024 * 1024
DEFAULT_DEADLINE = 540
MAX_RANGE = 32 * 1024 * 1024


def approved_source(opener=urlopen) -> str:
    info, raw = probe("metadata", f"{ORIGIN}/metadata/{ITEM}", "GET",
                      cap=META_LIMIT, opener=opener, timeout=15)
    if info.outcome != "responded" or info.status != 200 or info.capped:
        raise ValueError("archive metadata unavailable or truncated")
    meta = metadata_summary(raw)
    if not (meta["parse_ok"] and meta["file_found"]
            and meta["file_size"] == str(ARCHIVE_SIZE)
            and meta["md5_matches_pinned"] and meta["sha1_matches_pinned"]
            and meta["valid_storage_directory"] and meta["server"]):
        raise ValueError("accepted archive metadata identity/path mismatch")
    return f"https://{meta['server']}{meta['storage_directory']}/{FILE}"


def _verify_response(response, url: str, start: int, end: int, total: int):
    expected_range = f"bytes {start}-{end}/{total}"
    status = int(getattr(response, "status", 200))
    if status != 206 or response.headers.get("Content-Range") != expected_range:
        raise ValueError("remote server did not honor pinned byte range")
    final = urlsplit(response.geturl() if hasattr(response, "geturl") else url)
    if (final.scheme != "https" or not ALLOWED_HOST.fullmatch(final.hostname or "")
            or not final.path.endswith(f"/items/{ITEM}/{FILE}")):
        raise ValueError("untrusted archive storage redirect")


def download_pinned(url: str, output: Path, *,
                    size: int = ARCHIVE_SIZE, md5: str = ARCHIVE_MD5,
                    sha1: str = ARCHIVE_SHA1, chunk_size: int = DEFAULT_RANGE,
                    max_seconds: int = DEFAULT_DEADLINE, opener=urlopen) -> dict:
    if not (1 <= size <= ARCHIVE_SIZE and 1 <= chunk_size <= MAX_RANGE
            and 1 <= max_seconds <= 900):
        raise ValueError("invalid transfer bounds")
    if output.exists():
        raise ValueError("refuse to overwrite an existing archive")
    if not (re.fullmatch(r"[a-f0-9]{32}", md5)
            and re.fullmatch(r"[a-f0-9]{40}", sha1)):
        raise ValueError("invalid hash pins")
    origin = urlsplit(url)
    if (origin.scheme != "https" or not ALLOWED_HOST.fullmatch(origin.hostname or "")
            or not origin.path.endswith(f"/items/{ITEM}/{FILE}")):
        raise ValueError("unapproved source")
    digest_md5 = hashlib.md5(usedforsecurity=False)
    digest_sha1 = hashlib.sha1(usedforsecurity=False)
    deadline = time.monotonic() + max_seconds
    total_read = 0
    errors = 0
    calls = 0
    try:
        with output.open("xb") as output_file:
            while total_read < size:
                if time.monotonic() > deadline:
                    raise TimeoutError("bounded archive deadline reached")
                last = min(total_read + chunk_size - 1, size - 1)
                req = Request(url, headers={
                    "User-Agent": USER_AGENT,
                    "Range": f"bytes={total_read}-{last}",
                })
                calls += 1
                try:
                    with opener(req, timeout=20) as response:
                        _verify_response(response, url, total_read, last, size)
                        remaining = last - total_read + 1
                        while remaining:
                            if time.monotonic() > deadline:
                                raise TimeoutError("bounded archive deadline reached")
                            block = response.read(min(1024 * 1024, remaining))
                            if not block:
                                raise OSError("truncated range")
                            if len(block) > remaining:
                                raise ValueError("server delivered excess bytes")
                            output_file.write(block)
                            digest_md5.update(block)
                            digest_sha1.update(block)
                            remaining -= len(block)
                            total_read += len(block)
                        errors = 0
                        print(f"TRANSFER|bytes_verified_in_stream={total_read}|total={size}",
                              flush=True)
                except (HTTPError, URLError, OSError, TimeoutError):
                    errors += 1
                    if errors >= 3:
                        raise ValueError("archive transport exhausted 3 consecutive attempts")
                    if time.monotonic() > deadline:
                        raise TimeoutError("bounded archive deadline reached")
                    time.sleep(2)
        if digest_md5.hexdigest() != md5 or digest_sha1.hexdigest() != sha1:
            raise ValueError("downloaded original archive hash mismatch")
        if output.stat().st_size != size:
            raise ValueError("downloaded archive size mismatch")
        return {"verified": True, "size": size, "md5": md5, "sha1": sha1,
                "requests": calls, "status": "PINNED_ORIGINAL_ARCHIVE_BYTES_MATCH"}
    except BaseException:
        output.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/tmp/CD_DIC.rar"))
    parser.add_argument("--deadline", type=int, default=DEFAULT_DEADLINE)
    args = parser.parse_args()
    url = approved_source()
    print("SOURCE|archive_catalog_identity=PINNED|storage_path=CATALOG_VALIDATED",
          flush=True)
    result = download_pinned(url, args.output, max_seconds=args.deadline)
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
