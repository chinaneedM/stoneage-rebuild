#!/usr/bin/env python3
"""Recover sparse metadata for the CNET Korea StoneAge download record.

The exact historical record id was recovered from preserved CNET download-index
snapshots: Software_Id=200009263856. Archived HTML is fetched transiently.
Only record metadata, short text snippets, and link targets are emitted.
"""

from __future__ import annotations

import html
import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
AVAILABLE = "https://archive.org/wayback/available"
SOFTWARE_ID = "200009263856"

URL_VARIANTS = [
    f"http://www.korea.cnet.com/downloads/File.asp?Platform_Id=1&Software_Id={SOFTWARE_ID}",
    f"http://korea.cnet.com/downloads/File.asp?Platform_Id=1&Software_Id={SOFTWARE_ID}",
    f"http://www.korea.cnet.com/DownLoads/File.asp?Platform_Id=1&Software_Id={SOFTWARE_ID}",
    f"http://korea.cnet.com/DownLoads/File.asp?Platform_Id=1&Software_Id={SOFTWARE_ID}",
    f"http://www.korea.cnet.com/downloads/File.asp?Software_Id={SOFTWARE_ID}",
    f"http://korea.cnet.com/downloads/File.asp?Software_Id={SOFTWARE_ID}",
]
DATES = ["20000926", "20001013", "20001110", "20001228", "20010124", "20010430"]

FILE_RE = re.compile(r"(?i)\b[a-z0-9][a-z0-9._-]{1,160}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)\b")
SIZE_RE = re.compile(r"(?i)\b\d{1,7}(?:[.,]\d{1,3})?\s*(?:bytes?|kb|mb|gb)\b")
KEY_RE = re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|"
    r"file|파일|size|용량|version|버전|homepage|홈페이지|"
    r"inium|enium|제작|등록|update|설치|setup)"
)
WAYBACK_PREFIX = re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/", re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.text = []
        self._anchor_href = None
        self._anchor_text = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self._anchor_href = attrs["href"]
            self._anchor_text = []
        for attr in ("src", "action", "href"):
            target = attrs.get(attr)
            if target and not (tag == "a" and attr == "href"):
                self.links.append((tag, attr, target, ""))

    def handle_data(self, data):
        if data.strip():
            self.text.append(data)
        if self._anchor_href is not None:
            self._anchor_text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._anchor_href is not None:
            self.links.append(("a", "href", self._anchor_href, " ".join(self._anchor_text).strip()))
            self._anchor_href = None
            self._anchor_text = []


def request(url: str, timeout: int = 15) -> bytes:
    last = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"request failed: {url}: {last}")


def decode(data: bytes) -> str:
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1", "replace")


def closest(payload: dict):
    c = payload.get("archived_snapshots", {}).get("closest")
    if not isinstance(c, dict) or not c.get("available"):
        return None
    return str(c.get("timestamp", "")), str(c.get("status", "")), str(c.get("url", ""))


def availability(original: str, requested: str):
    query = urllib.parse.urlencode({"url": original, "timestamp": requested})
    payload = json.loads(request(AVAILABLE + "?" + query, timeout=10).decode("utf-8", "replace"))
    return closest(payload)


def snapshot_url(timestamp: str, original: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def unwrap(target: str) -> str:
    return WAYBACK_PREFIX.sub("", target)


def normalize(base: str, target: str) -> str:
    target = html.unescape(target.strip())
    if not target or target.startswith(("javascript:", "mailto:", "#")):
        return ""
    return unwrap(urllib.parse.urljoin(base, target))


def safe(value: str, limit: int = 500) -> str:
    value = " ".join(value.split())
    value = "".join(ch for ch in value if ch >= " " and ch != "\x7f")
    return value[:limit]


def sparse_snippets(text_parts):
    lines = []
    seen = set()
    for raw in text_parts:
        line = safe(raw, 260)
        if not line or line in seen:
            continue
        if KEY_RE.search(line) or FILE_RE.search(line) or SIZE_RE.search(line):
            seen.add(line)
            lines.append(line)
    return lines


def main():
    print("StoneAge CNET Korea exact record probe — R1")
    print(f"RECORD|Software_Id={SOFTWARE_ID}")
    print("SCOPE|metadata-links-short-snippets-only|transient-html|no-client-binary-download")

    found = {}
    errors = []
    for original in URL_VARIANTS:
        for requested in DATES:
            try:
                hit = availability(original, requested)
            except Exception as exc:
                errors.append(("availability", requested, original, type(exc).__name__, str(exc)))
                continue
            if hit:
                timestamp, status, archived = hit
                found[(timestamp, original)] = (status, archived)

    print(f"COUNT|availability_queries|{len(URL_VARIANTS) * len(DATES)}")
    print(f"COUNT|availability_errors|{sum(1 for e in errors if e[0]=='availability')}")
    print(f"COUNT|unique_snapshots|{len(found)}")

    for (timestamp, original), (status, archived) in sorted(found.items()):
        print(
            f"SNAPSHOT|timestamp={timestamp}|status={safe(status)}|"
            f"original={safe(original)}|archived={safe(archived)}"
        )

    fetched = set()
    record_links = set()
    snippets = set()
    files = set()
    sizes = set()

    for timestamp, original in sorted(found):
        key = (timestamp, original)
        if key in fetched:
            continue
        fetched.add(key)
        try:
            body = request(snapshot_url(timestamp, original), timeout=20)
            text = decode(body)
            parser = Parser()
            parser.feed(text)
        except Exception as exc:
            errors.append(("snapshot", timestamp, original, type(exc).__name__, str(exc)))
            continue

        for snippet in sparse_snippets(parser.text):
            snippets.add((timestamp, snippet))
            files.update(FILE_RE.findall(snippet))
            sizes.update(SIZE_RE.findall(snippet))

        for tag, attr, target, label in parser.links:
            normalized = normalize(original, target)
            if not normalized:
                continue
            combined = f"{normalized} {label}"
            if SOFTWARE_ID in normalized or KEY_RE.search(combined) or FILE_RE.search(normalized):
                record_links.add((timestamp, tag, attr, normalized, safe(label, 180)))
            files.update(FILE_RE.findall(normalized))
            files.update(FILE_RE.findall(label))
            sizes.update(SIZE_RE.findall(label))

    for phase, marker, original, kind, message in errors:
        print(
            f"ERROR|phase={phase}|marker={safe(marker)}|kind={kind}|"
            f"original={safe(original)}|message={safe(message)}"
        )

    print(f"COUNT|snapshot_fetch_errors|{sum(1 for e in errors if e[0]=='snapshot')}")
    print(f"COUNT|interesting_links|{len(record_links)}")
    print(f"COUNT|snippets|{len(snippets)}")
    print(f"COUNT|file_tokens|{len(files)}")
    print(f"COUNT|size_tokens|{len(sizes)}")

    for token in sorted(files, key=str.lower):
        print(f"FILE|{safe(token)}")
    for token in sorted(sizes, key=str.lower):
        print(f"SIZE|{safe(token)}")
    for timestamp, snippet in sorted(snippets):
        print(f"TEXT|timestamp={timestamp}|value={safe(snippet,260)}")
    for timestamp, tag, attr, target, label in sorted(record_links):
        print(
            f"LINK|timestamp={timestamp}|tag={tag}|attr={attr}|"
            f"target={safe(target)}|label={safe(label,180)}"
        )


if __name__ == "__main__":
    main()
