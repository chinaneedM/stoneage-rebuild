#!/usr/bin/env python3
"""Metadata-only probe of the current SourceForge ``stoneage`` ZIP files.

The probe never downloads archive members.  It requests one byte to learn the
remote object length, then only the ZIP tail and central-directory byte range.
If a server ignores Range, the response is rejected before its body is read.
"""

from __future__ import annotations

import re
import struct
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass

UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
PROJECT = "stoneage"
ARCHIVES = (
    "patch_0.zip",
    "patch_1.zip",
    "patch_2.zip",
    "patch_3.zip",
    "patch_4.zip",
    "patch_5.zip",
)
TAIL_BYTES = 128 * 1024
MAX_CENTRAL_DIRECTORY = 16 * 1024 * 1024
MAX_SAMPLE = 30
MAX_HITS = 250

EOCD_SIG = b"PK\x05\x06"
CENTRAL_SIG = b"PK\x01\x02"

EXACT_TARGET = re.compile(
    r"(?i)(?:^|[/\\])(?:"
    r"onlstoneage\.zip|stone_demo\.exe|sa_demo\.exe|stoneagebeta\.zip|"
    r"stoneage\.exe|sa\.exe|stoneage\.zip"
    r")$"
)
ARCHAEOLOGY = re.compile(
    r"(?i)(stone\s*age|stoneage|스톤에이지|"
    r"(?:^|[/\\])real\.bin$|(?:^|[/\\])adrn[^/\\]*\.bin$|"
    r"(?:^|[/\\])[^/\\]+\.spr$)"
)
CONTAMINATION = re.compile(
    r"(?i)(launcher|patcher|private|server[_-]?(?:list|ip|config)|"
    r"(?:^|[/\\])ip\.txt$|(?:^|[/\\])sa_[^/\\]*\.exe$)"
)


@dataclass(frozen=True)
class CentralEntry:
    name: str
    crc32: int
    compressed_size: int
    uncompressed_size: int
    method: int
    flags: int
    is_dir: bool


def clean(value, limit=900):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def candidate_urls(name):
    quoted = urllib.parse.quote(name)
    return (
        f"https://downloads.sourceforge.net/project/{PROJECT}/{quoted}",
        f"https://sourceforge.net/projects/{PROJECT}/files/{quoted}/download",
    )


def _open_range(url, start, end, timeout=25):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Range": f"bytes={start}-{end}",
            "Accept-Encoding": "identity",
        },
    )
    response = urllib.request.urlopen(req, timeout=timeout)
    status = getattr(response, "status", None)
    content_range = response.headers.get("Content-Range", "")
    if status != 206 or not content_range.lower().startswith("bytes "):
        response.close()
        raise RuntimeError(f"range-not-honored status={status} content-range={content_range!r}")
    return response


def discover_size(url, timeout=25):
    with _open_range(url, 0, 0, timeout) as response:
        content_range = response.headers.get("Content-Range", "")
        match = re.fullmatch(r"bytes\s+0-0/(\d+)", content_range.strip(), re.I)
        if not match:
            raise RuntimeError(f"unexpected-content-range {content_range!r}")
        total = int(match.group(1))
        one = response.read(1)
        if len(one) != 1:
            raise RuntimeError(f"short-size-probe bytes={len(one)}")
        return total, response.geturl(), dict(response.headers.items())


def range_bytes(url, start, end, timeout=25):
    if start < 0 or end < start:
        raise ValueError("invalid range")
    length = end - start + 1
    with _open_range(url, start, end, timeout) as response:
        data = response.read(length + 1)
        if len(data) != length:
            raise RuntimeError(f"short-range expected={length} got={len(data)}")
        return data, response.geturl(), dict(response.headers.items())


def parse_eocd_tail(tail, total_size):
    pos = tail.rfind(EOCD_SIG)
    if pos < 0 or len(tail) - pos < 22:
        raise ValueError("EOCD not found in bounded tail")
    (
        sig,
        disk_number,
        central_disk,
        disk_entries,
        total_entries,
        central_size,
        central_offset,
        comment_length,
    ) = struct.unpack_from("<4s4H2LH", tail, pos)
    if sig != EOCD_SIG:
        raise ValueError("bad EOCD signature")
    if pos + 22 + comment_length > len(tail):
        raise ValueError "truncated EOCD comment")
    if disk_number != 0 or central_disk != 0 or disk_entries != total_entries:
        raise ValueError("multi-disk ZIP unsupported")
    if total_entries == 0xFFFF or central_size == 0xFFFFFFFF or central_offset == 0xFFFFFFFF:
        raise ValueError "ZIP64 central directory unsupported")
    if central_size > MAX_CENTRAL_DIRECTORY:
        raise ValueError(f"central directory too large: {central_size}")
    if central_offset + central_size > total_size:
        raise ValueError("central directory exceeds remote object size")
    return {
        "entries": total_entries,
        "central_size": central_size,
        "central_offset": central_offset,
        "comment_length": comment_length,
    }


def decode_name(raw, flags):
    if flags & 0x800:
        return raw.decode("utf-8", "replace")
    for encoding in ("cp949", "euc-kr"):
        try:
            text = raw.decode(encoding)
        except UnicodeDecodeError:
            continue
        if any("\uac00" <= ch <= "\ud7a3" for ch in text):
            return text
    return raw.decode("cp437", "replace")


def parse_central_directory(data, expected_entries=None):
    entries = []
    pos = 0
    while pos < len(data):
        if len(data) - pos < 46:
            raise ValueError(f"truncated central header at {pos}")
        if data[pos:pos + 4] != CENTRAL_SIG:
            raise ValueError(f"unexpected central signature at {pos}: {data[pos:pos+4]!r}")
        values = struct.unpack_from("<6H3L5H2L", data, pos + 4)
        (
            _version_made,
            _version_needed,
            flags,
            method,
            _mtime,
            _mdate,
            crc32,
            compressed_size,
            uncompressed_size,
            name_len,
            extra_len,
            comment_len,
            _disk_start,
            _internal_attr,
            _external_attr,
            _local_offset,
        ) = values
        end = pos + 46 + name_len + extra_len + comment_len
        if end > len(data):
            raise ValueError(f"truncated central record at {pos}")
        raw_name = data[pos + 46:pos + 46 + name_len]
        name = decode_name(raw_name, flags)
        entries.append(
            CentralEntry(
                name=name,
                crc32=crc32,
                compressed_size=compressed_size,
                uncompressed_size=uncompressed_size,
                method=method,
                flags=flags,
                is_dir=name.endswith("/"),
            )
        )
        pos = end
    if expected_entries is not None and len(entries) != expected_entries:
        raise ValueError(f"entry-count mismatch expected={expected_entries} parsed={len(entries)}")
    return entries


def classify(name):
    if EXACT_TARGET.search(name):
        return "exact-target"
    if ARCHAEOLOGY.search(name):
        return "archaeology"
    if CONTAMINATION.search(name):
        return "contamination-marker"
    return ""


def summarize_top(entries):
    counts = {}
    for entry in entries:
        stripped = entry.name.strip("/\\")
        if not stripped:
            continue
        top = re.split(r"[/\\]", stripped, maxsplit=1)[0]
        counts[top] = counts.get(top, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))[:20]


def scan_archive(name):
    errors = []
    chosen = None
    total = None
    headers = {}
    final_url = ""
    for url in candidate_urls(name):
        try:
            total, final_url, headers = discover_size(url)
            chosen = url
            break
        except Exception as exc:
            errors.append(f"{url} -> {type(exc).__name__}:{exc}")
            time.sleep(0.5)
    if chosen is None:
        raise RuntimeError("; ".join(errors))

    tail_start = max(0, total - TAIL_BYTES)
    tail, tail_final, _ = range_bytes(chosen, tail_start, total - 1)
    eocd = parse_eocd_tail(tail, total)
    if eocd["central_size"] == 0:
        central = b""
    else:
        start = eocd["central_offset"]
        central, _, _ = range_bytes(chosen, start, start + eocd["central_size"] - 1)
    entries = parse_central_directory(central, eocd["entries"])
    return {
        "name": name,
        "request_url": chosen,
        "final_url": tail_final or final_url,
        "size": total,
        "etag": headers.get("ETag", ""),
        "last_modified": headers.get("Last-Modified", ""),
        "central_size": eocd["central_size"],
        "entries": entries,
        "fallback_errors": errors,
        "bytes_requested": 1 + len(tail) + len(central),
    }


def main():
    print("StoneAge SourceForge ZIP central-directory probe — R1")
    print("SCOPE|bounded-http-range-metadata-only|no-archive-member-download|no-carrier-bytes-committed")
    print(f"PROJECT|sourceforge_project={PROJECT}|archive_candidates={len(ARCHIVES)}")
    print(f"LIMIT|tail_bytes={TAIL_BYTES}|max_central_directory={MAX_CENTRAL_DIRECTORY}")

    ok = 0
    exact = 0
    archaeology = 0
    contamination = 0
    total_requested = 0
    for name in ARCHIVES:
        try:
            result = scan_archive(name)
        except Exception as exc:
            print(f"ARCHIVE_ERROR|name={clean(name)}|kind={type(exc).__name__}|message={clean(exc)}")
            continue
        ok += 1
        total_requested += result["bytes_requested"]
        entries = result["entries"]
        hits = [(classify(e.name), e) for e in entries]
        hits = [(kind, e) for kind, e in hits if kind]
        exact += sum(kind == "exact-target" for kind, _ in hits)
        archaeology += sum(kind == "archaeology" for kind, _ in hits)
        contamination += sum(kind == "contamination-marker" for kind, _ in hits)
        print(
            f"ARCHIVE|name={clean(name)}|size={result['size']}|entries={len(entries)}|"
            f"central_size={result['central_size']}|bytes_requested={result['bytes_requested']}|"
            f"etag={clean(result['etag'])}|last_modified={clean(result['last_modified'])}|"
            f"request_url={clean(result['request_url'])}|final_url={clean(result['final_url'])}|"
            f"fallback_errors={len(result['fallback_errors'])}"
        )
        for err in result["fallback_errors"]:
            print(f"FALLBACK|archive={clean(name)}|message={clean(err)}")
        for top, count in summarize_top(entries):
            print(f"TOP|archive={clean(name)}|name={clean(top)}|entries={count}")
        for entry in entries[:MAX_SAMPLE]:
            print(
                f"SAMPLE|archive={clean(name)}|path={clean(entry.name)}|"
                f"usize={entry.uncompressed_size}|csize={entry.compressed_size}|crc32={entry.crc32:08x}"
            )
        for kind, entry in hits[:MAX_HITS]:
            print(
                f"HIT|archive={clean(name)}|kind={kind}|path={clean(entry.name)}|"
                f"usize={entry.uncompressed_size}|csize={entry.compressed_size}|"
                f"crc32={entry.crc32:08x}|method={entry.method}"
            )
        if len(hits) > MAX_HITS:
            print(f"HIT_TRUNCATED|archive={clean(name)}|shown={MAX_HITS}|total={len(hits)}")

    print(f"COUNT|archives_scanned|{ok}")
    print(f"COUNT|archives_failed|{len(ARCHIVES)-ok}")
    print(f"COUNT|exact_target_hits|{exact}")
    print(f"COUNT|archaeology_hits|{archaeology}")
    print(f"COUNT|contamination_marker_hits|{contamination}")
    print(f"COUNT|bytes_requested_total|{total_requested}")


if __name__ == "__main__":
    main()
