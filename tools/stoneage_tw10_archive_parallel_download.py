#!/usr/bin/env python3
"""Parallel, strictly bounded and hash-pinned transient acquisition of a TW1.0 disc.

All workers receive disjoint HTTP byte ranges and write only to a temporary
file. Original bytes never appear in logs or Actions artifact uploads. The
whole file must pass both pinned MD5 and SHA1 before the static R3 analyzer
can run; per-chunk HTTP integrity is necessary, never sufficient.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from tools.stoneage_tw10_archive_chunk_download import (
    ARCHIVE_MD5, ARCHIVE_SHA1, ARCHIVE_SIZE, ITEM, FILE,
    USER_AGENT, ALLOWED_HOST, _verify_response, approved_source,
)

DEFAULT_WORKERS = 12
DEFAULT_CHUNK = 8 * 1024 * 1024
MAX_CHUNK = 16 * 1024 * 1024
DEFAULT_DEADLINE = 540


def ranges(size: int, chunk_size: int):
    return [(start, min(start + chunk_size, size) - 1)
            for start in range(0, size, chunk_size)]


def _allowed_source(url: str):
    parsed = urlsplit(url)
    if (parsed.scheme != "https"
            or not ALLOWED_HOST.fullmatch(parsed.hostname or "")
            or not re.fullmatch(
                rf"/[0-9]{{1,3}}/items/{re.escape(ITEM)}/{re.escape(FILE)}",
                parsed.path)
            or parsed.username or parsed.password or parsed.port
            or parsed.query or parsed.fragment):
        raise ValueError("source URL failed archive host/path gate")


def _fetch_chunk(url: str, fd: int, start: int, end: int, total: int,
                 deadline: float, opener, attempts: int = 2) -> int:
    length = end - start + 1
    for attempt in range(attempts):
        if time.monotonic() >= deadline:
            raise TimeoutError("parallel download deadline")
        try:
            req = Request(url, headers={
                "User-Agent": USER_AGENT,
                "Range": f"bytes={start}-{end}",
            })
            with opener(req, timeout=25) as res:
                _verify_response(res, url, start, end, total)
                remaining = length
                offset = start
                while remaining:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("parallel download deadline")
                    block = res.read(min(512 * 1024, remaining))
                    if not block or len(block) > remaining:
                        raise OSError("truncated or excess HTTP body")
                    if os.pwrite(fd, block, offset) != len(block):
                        raise OSError("short positional disk write")
                    offset += len(block)
                    remaining -= len(block)
                return length
        except (HTTPError, URLError, OSError, TimeoutError):
            if attempt == attempts - 1:
                raise ValueError("range transport failed after bounded retry") from None
            if time.monotonic() >= deadline:
                raise TimeoutError("parallel download deadline") from None
            time.sleep(0.5)
    raise AssertionError("unreachable")


def download_parallel(url: str, output: Path, *,
                      size: int = ARCHIVE_SIZE,
                      md5: str = ARCHIVE_MD5, sha1: str = ARCHIVE_SHA1,
                      chunk_size: int = DEFAULT_CHUNK,
                      max_seconds: int = DEFAULT_DEADLINE,
                      workers: int = DEFAULT_WORKERS,
                      opener=urlopen) -> dict:
    if (not (1 <= size <= ARCHIVE_SIZE)
            or not (1 <= chunk_size <= MAX_CHUNK)
            or not (1 <= max_seconds <= 900)
            or not (1 <= workers <= 16)):
        raise ValueError("download configuration bounds")
    _allowed_source(url)
    if output.exists():
        raise ValueError("refusing existing output path")
    if not (re.fullmatch(r"[0-9a-f]{32}", md5)
            and re.fullmatch(r"[0-9a-f]{40}", sha1)):
        raise ValueError("digest pin format")
    deadline = time.monotonic() + max_seconds
    windows = ranges(size, chunk_size)
    completed = 0
    fd = None
    try:
        fd = os.open(output, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        os.ftruncate(fd, size)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            pending = [executor.submit(_fetch_chunk, url, fd, start, end, size,
                                       deadline, opener)
                       for start, end in windows]
            for future in as_completed(pending):
                completed += future.result()
                if completed % (64 * 1024 * 1024) < chunk_size or completed == size:
                    print(f"PARALLEL_TRANSFER|complete_range_bytes={completed}|total={size}",
                          flush=True)
        os.fsync(fd)
        os.close(fd)
        fd = None
        if time.monotonic() >= deadline:
            raise TimeoutError("parallel transfer exceeded deadline")
        dig_md5 = hashlib.md5(usedforsecurity=False)
        dig_sha1 = hashlib.sha1(usedforsecurity=False)
        with output.open("rb") as src:
            while True:
                block = src.read(2 * 1024 * 1024)
                if not block:
                    break
                dig_md5.update(block)
                dig_sha1.update(block)
        if output.stat().st_size != size:
            raise ValueError("archive size mismatch")
        if dig_md5.hexdigest() != md5 or dig_sha1.hexdigest() != sha1:
            raise ValueError("full-file original archive hash mismatch")
        return {
            "status": "PINNED_ORIGINAL_ARCHIVE_BYTES_MATCH",
            "verified": True, "size": size,
            "md5": md5, "sha1": sha1,
            "range_count": len(windows), "parallel_workers": workers,
            "original_data_published": False,
        }
    except BaseException:
        if fd is not None:
            os.close(fd)
        output.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/tmp/CD_DIC.rar"))
    parser.add_argument("--deadline", type=int, default=DEFAULT_DEADLINE)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--chunk", type=int, default=DEFAULT_CHUNK)
    args = parser.parse_args()
    url = approved_source()
    print("SOURCE|archive_catalog_identity=PINNED|storage_path=CATALOG_VALIDATED",
          flush=True)
    print(json.dumps(download_parallel(url, args.output,
                                      max_seconds=args.deadline,
                                      workers=args.workers,
                                      chunk_size=args.chunk), sort_keys=True))


if __name__ == "__main__":
    main()
