#!/usr/bin/env python3
"""Bounded metadata audit of the Taiwan 2000 StoneAge disc preservation lead.

Two independent surfaces are checked:
1. Redump disc 104630 public metadata.
2. Internet Archive item stoneage_tw_2000_win / CD_DIC.rar member headers.

RAR listing uses a seekable HTTP Range reader. It never extracts members and enforces
strict request/byte budgets so a server that ignores Range cannot trigger a full download.
No proprietary payload bytes are committed.
"""

from __future__ import annotations

import html
from html.parser import HTMLParser
import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
IA_META = "https://archive.org/metadata/{}"
IA_DOWNLOAD = "https://archive.org/download/{}/{}"
REDUMP_URL = "http://redump.org/disc/104630/"

ITEM = "stoneage_tw_2000_win"
RAR_NAME = "CD_DIC.rar"
EXPECTED_RAR_MD5 = "b37a4a47f4eb608cac67e4ddf7a1621a"
EXPECTED_RAR_SHA1 = "b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded"

MAX_TOTAL_RANGE_BYTES = 32 * 1024 * 1024
MAX_SINGLE_RANGE = 4 * 1024 * 1024
MAX_REQUESTS = 500


def clean(value, limit=1200):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def get_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)


def get_text(url, timeout=30):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.geturl(), response.read(4 * 1024 * 1024).decode("utf-8", "replace")


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.cell_tag = ""
        self.cell_parts = []
        self.row = []
        self.rows = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        low = tag.lower()
        if low in ("th", "td"):
            self.in_cell = True
            self.cell_tag = low
            self.cell_parts = []
        elif low == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

    def handle_data(self, data):
        if self.in_cell:
            self.cell_parts.append(data)

    def handle_endtag(self, tag):
        low = tag.lower()
        if self.in_cell and low == self.cell_tag:
            value = clean(html.unescape(" ".join(self.cell_parts)), 2000)
            self.row.append((self.cell_tag, value))
            self.in_cell = False
            self.cell_tag = ""
            self.cell_parts = []
        elif low == "tr":
            if self.row:
                self.rows.append(self.row)
            self.row = []


class HTTPRangeFile:
    """Minimal seekable read-only file object backed by HTTP Range requests."""

    def __init__(self, url, size):
        self.url = url
        self.size = int(size)
        self.pos = 0
        self.closed = False
        self.requests = 0
        self.bytes_read = 0
        self.final_url = url

    def tell(self):
        return self.pos

    def seekable(self):
        return True

    def readable(self):
        return True

    def seek(self, offset, whence=0):
        if whence == 0:
            new_pos = offset
        elif whence == 1:
            new_pos = self.pos + offset
        elif whence == 2:
            new_pos = self.size + offset
        else:
            raise ValueError("unsupported whence")
        if new_pos < 0:
            raise ValueError("negative seek")
        self.pos = min(new_pos, self.size)
        return self.pos

    def read(self, size=-1):
        if self.closed:
            raise ValueError("I/O operation on closed range reader")
        if self.pos >= self.size:
            return b""
        if size is None or size < 0:
            size = self.size - self.pos
        size = min(int(size), self.size - self.pos)
        if size <= 0:
            return b""
        if size > MAX_SINGLE_RANGE:
            raise RuntimeError(f"single range too large: {size}")
        if self.requests >= MAX_REQUESTS:
            raise RuntimeError(f"range request budget exceeded: {MAX_REQUESTS}")
        if self.bytes_read + size > MAX_TOTAL_RANGE_BYTES:
            raise RuntimeError(
                f"range byte budget exceeded: {self.bytes_read + size}>{MAX_TOTAL_RANGE_BYTES}"
            )

        start = self.pos
        end = start + size - 1
        req = urllib.request.Request(
            self.url,
            headers={
                "User-Agent": UA,
                "Range": f"bytes={start}-{end}",
                "Accept-Encoding": "identity",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            status = getattr(response, "status", 200)
            content_range = response.headers.get("Content-Range", "")
            if status != 206 or not content_range.lower().startswith("bytes "):
                raise RuntimeError(
                    f"range not honored status={status} content-range={content_range!r}"
                )
            data = response.read(size + 1)
            if len(data) != size:
                raise RuntimeError(f"short range expected={size} got={len(data)}")
            self.final_url = response.geturl()

        self.pos += len(data)
        self.requests += 1
        self.bytes_read += len(data)
        return data

    def close(self):
        self.closed = True


def redump_probe():
    try:
        final_url, body = get_text(REDUMP_URL)
    except Exception as exc:
        print(
            f"REDUMP_ERROR|url={clean(REDUMP_URL)}|kind={type(exc).__name__}|"
            f"message={clean(exc)}"
        )
        return

    parser = TableParser()
    parser.feed(body)
    print(
        f"REDUMP|requested={clean(REDUMP_URL)}|final={clean(final_url)}|"
        f"html_bytes={len(body.encode('utf-8'))}|rows={len(parser.rows)}|links={len(parser.links)}"
    )

    keywords = re.compile(
        r"(?i)(title|system|media|category|region|languages?|serial|version|edition|"
        r"ring|barcode|crc|md5|sha-?1|size|track|dump|date|status|comments?|exe|"
        r"石器|stone)"
    )
    emitted = 0
    for row in parser.rows:
        text = " | ".join(value for _tag, value in row if value)
        if text and keywords.search(text):
            print(f"REDUMP_ROW|text={clean(text,3000)}")
            emitted += 1
    print(f"REDUMP_COUNT|matched_rows={emitted}")

    for href in parser.links:
        if re.search(r"(?i)(dat|cue|sbi|log|download|disc/104630|stone)", href):
            print(f"REDUMP_LINK|href={clean(href,1800)}")


def rar_probe():
    meta = get_json(IA_META.format(urllib.parse.quote(ITEM, safe="")))
    target = None
    for row in meta.get("files", []):
        if str(row.get("name", "")) == RAR_NAME:
            target = row
            break
    if not target:
        print(f"RAR_ERROR|kind=NotFound|message={RAR_NAME} missing from IA metadata")
        return

    size = int(target.get("size") or 0)
    md5 = str(target.get("md5") or "")
    sha1 = str(target.get("sha1") or "")
    print(
        f"RAR_SOURCE|item={ITEM}|name={RAR_NAME}|size={size}|md5={clean(md5)}|"
        f"sha1={clean(sha1)}|format={clean(target.get('format'))}|source={clean(target.get('source'))}|"
        f"expected_md5_match={int(md5.lower()==EXPECTED_RAR_MD5)}|"
        f"expected_sha1_match={int(sha1.lower()==EXPECTED_RAR_SHA1)}"
    )

    url = IA_DOWNLOAD.format(
        urllib.parse.quote(ITEM, safe=""),
        urllib.parse.quote(RAR_NAME, safe="/"),
    )
    reader = HTTPRangeFile(url, size)

    try:
        import rarfile
        with rarfile.RarFile(reader, mode="r", crc_check=False, errors="strict") as rf:
            infos = list(rf.infolist())
            print(
                f"RAR|members={len(infos)}|needs_password={int(rf.needs_password())}|"
                f"solid={int(rf.is_solid())}|requests={reader.requests}|bytes_read={reader.bytes_read}|"
                f"final_url={clean(reader.final_url)}"
            )
            for info in infos:
                dt = getattr(info, "date_time", None)
                crc = getattr(info, "CRC", None)
                compress_size = getattr(info, "compress_size", None)
                volume = getattr(info, "volume_file", None)
                print(
                    f"RAR_MEMBER|name={clean(info.filename,1800)}|"
                    f"file_size={getattr(info,'file_size',0)}|"
                    f"compress_size={compress_size if compress_size is not None else ''}|"
                    f"crc={crc if crc is not None else ''}|"
                    f"date_time={clean(dt)}|is_dir={int(info.is_dir())}|"
                    f"password={int(info.needs_password())}|volume={clean(volume)}"
                )
    except Exception as exc:
        print(
            f"RAR_ERROR|kind={type(exc).__name__}|message={clean(exc,1800)}|"
            f"requests={reader.requests}|bytes_read={reader.bytes_read}|"
            f"position={reader.tell()}|final_url={clean(reader.final_url)}"
        )
    finally:
        reader.close()


def main():
    print("StoneAge Taiwan 2000 preservation audit — R1")
    print(
        "SCOPE|redump-public-metadata-plus-rar-header-range-reads|"
        "no-rar-member-extraction|no-full-payload-download"
    )
    print(
        f"LIMIT|max_total_range_bytes={MAX_TOTAL_RANGE_BYTES}|"
        f"max_single_range={MAX_SINGLE_RANGE}|max_requests={MAX_REQUESTS}"
    )
    redump_probe()
    rar_probe()


if __name__ == "__main__":
    main()
