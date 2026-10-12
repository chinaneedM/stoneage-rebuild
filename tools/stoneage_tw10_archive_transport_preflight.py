#!/usr/bin/env python3
"""Bounded Internet Archive transport preflight for one accepted Taiwan 1.0 disc.

Never downloads/stores an archive or executable and never prints source bytes.
HTTP signals alone must never be promoted to accepted original binary evidence.
"""
from __future__ import annotations

import argparse
import json
import re
import socket
import time
from dataclasses import asdict, dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ITEM = "stoneage_tw_2000_win"
FILE = "CD_DIC.rar"
ARCHIVE_MD5 = "b37a4a47f4eb608cac67e4ddf7a1621a"
ARCHIVE_SHA1 = "b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded"
ORIGIN = "https://archive.org"
META_LIMIT = 262144
RANGE_LIMIT = 4096
ALLOWED_HOST = re.compile(r"^ia[0-9]{3,9}\.us\.archive\.org$")
ALLOWED_STORAGE_DIR = re.compile(r"^/[0-9]{1,3}/items/stoneage_tw_2000_win$")
USER_AGENT = "stoneage-reconstruction-static-source-preflight/1.0"


@dataclass(frozen=True)
class Signal:
    name: str
    outcome: str
    status: int = 0
    bytes_read: int = 0
    capped: bool = False
    content_length: str = ""
    content_range: str = ""
    accept_ranges: str = ""
    elapsed_ms: int = 0


def _safe_header(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"[^a-zA-Z0-9 /._:*;-]", "", value[:120])


def probe(name: str, url: str, method: str, cap: int = RANGE_LIMIT,
          opener=urlopen, timeout: int = 12) -> tuple[Signal, bytes]:
    """Close the connection after at most cap+1 bytes regardless of HTTP Range."""
    if method not in ("GET", "HEAD"):
        raise ValueError("unsupported method")
    if cap < 1 or cap > META_LIMIT:
        raise ValueError("probe cap out of bounds")
    headers = {"User-Agent": USER_AGENT}
    if name.endswith("_range"):
        headers["Range"] = f"bytes=0-{RANGE_LIMIT - 1}"
        if cap != RANGE_LIMIT:
            raise ValueError("range probe size mismatch")
    request = Request(url, headers=headers, method=method)
    started = time.monotonic()
    try:
        with opener(request, timeout=timeout) as response:
            status = int(getattr(response, "status", 200))
            body = response.read(cap + 1) if method == "GET" else b""
            safe_body = body[:cap]
            h = response.headers
            signal = Signal(name=name, outcome="responded", status=status,
                            bytes_read=len(safe_body), capped=len(body) > cap,
                            content_length=_safe_header(h.get("Content-Length")),
                            content_range=_safe_header(h.get("Content-Range")),
                            accept_ranges=_safe_header(h.get("Accept-Ranges")),
                            elapsed_ms=int((time.monotonic() - started) * 1000))
            return signal, safe_body
    except HTTPError as e:
        # Headers on 4xx/5xx may help isolate auth/range/origin problems.
        return Signal(name, "http_error", status=int(e.code),
                      elapsed_ms=int((time.monotonic() - started) * 1000)), b""
    except (URLError, TimeoutError, socket.timeout, OSError) as e:
        # No URLs, remote response bodies, or exception strings in the report.
        return Signal(name, "transport_error",
                      elapsed_ms=int((time.monotonic() - started) * 1000)), b""


def metadata_summary(data: bytes, *, capped: bool = False) -> dict:
    """Do not trust metadata as original byte-content verification."""
    result = {
        "parse_ok": False, "file_found": False, "file_size": "",
        "md5_matches_pinned": False, "sha1_matches_pinned": False,
        "candidate_server_count": 0, "server": "",
        "valid_storage_directory": False, "storage_directory": "",
    }
    if capped:
        return result
    try:
        obj = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeError):
        return result
    if not isinstance(obj, dict) or not isinstance(obj.get("files"), list):
        return result
    result["parse_ok"] = True
    for entry in obj["files"]:
        if isinstance(entry, dict) and entry.get("name") == FILE:
            result["file_found"] = True
            size = str(entry.get("size", ""))
            result["file_size"] = size if size.isdecimal() else ""
            result["md5_matches_pinned"] = entry.get("md5", "").lower() == ARCHIVE_MD5
            result["sha1_matches_pinned"] = entry.get("sha1", "").lower() == ARCHIVE_SHA1
            break
    hosts = [obj.get("server"), *obj.get("workable_servers", [])] \
        if isinstance(obj.get("workable_servers", []), list) else [obj.get("server")]
    safe_hosts = list(dict.fromkeys(x for x in hosts if isinstance(x, str)
                                    and ALLOWED_HOST.fullmatch(x)))
    directory = obj.get("dir", "")
    if isinstance(directory, str) and ALLOWED_STORAGE_DIR.fullmatch(directory):
        result["valid_storage_directory"] = True
        result["storage_directory"] = directory
    result["candidate_server_count"] = len(safe_hosts)
    if safe_hosts:
        result["server"] = safe_hosts[0]
    return result


def range_class(signal: Signal) -> str:
    if signal.outcome != "responded":
        return "UNKNOWN"
    if signal.status == 206 and signal.content_range.startswith("bytes 0-"):
        return "PARTIAL_CONFIRMED"
    if signal.status == 200:
        return "RANGE_IGNORED"
    return "UNRESOLVED"


def run(opener=urlopen) -> dict:
    m, data = probe("metadata", f"{ORIGIN}/metadata/{ITEM}", "GET",
                    cap=META_LIMIT, opener=opener)
    meta = metadata_summary(data, capped=m.capped or m.outcome != "responded")
    canonical = f"{ORIGIN}/download/{ITEM}/{FILE}"
    head, _ = probe("canonical_head", canonical, "HEAD", opener=opener)
    sliced, _ = probe("canonical_range", canonical, "GET", opener=opener)
    records = [asdict(m), asdict(head), asdict(sliced)]
    if meta["server"] and meta["valid_storage_directory"]:
        dynamic = f"https://{meta['server']}{meta['storage_directory']}/{FILE}"
        sub, _ = probe("storage_server_range", dynamic, "GET", opener=opener)
        records.append(asdict(sub))
    return {
        "schema": "tw10-savedata-archive-transport-preflight-r1",
        "artifact_identity": {"item": ITEM, "filename": FILE,
                              "pinned_md5": ARCHIVE_MD5, "pinned_sha1": ARCHIVE_SHA1},
        "metadata": {k: v for k, v in meta.items()
                     if k not in ("server", "storage_directory")},
        "probes": records,
        "canonical_range_capability": range_class(sliced),
        "admission": "TRANSPORT_SIGNALS_ONLY",
        "original_archive_downloaded": False,
        "original_client_hash_verified": False,
        "savedata_instruction_boundaries_verified": False,
        "caveat": "Headers, sampled transport bytes and archive.org metadata do not prove original artifact identity.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Write derived JSON (no remote body) to this file")
    args = parser.parse_args()
    output = json.dumps(run(), ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
