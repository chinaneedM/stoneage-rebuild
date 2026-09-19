#!/usr/bin/env python3
"""Extract sparse link metadata from known Wayback snapshots of Korea 2000 StoneAge surfaces.

Archived HTML is fetched transiently. Only URLs, short anchor/form labels, and
classification metadata are emitted; page bodies and client binaries are not stored.
"""

from __future__ import annotations

import html.parser
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

UA = "stoneage-rebuild-archaeology/1.0"

SNAPSHOTS = [
    ("inium-20001109", "20001109153100", "http://stoneage.enium.co.kr:80/"),
    ("inium-20010201", "20010201072800", "http://stoneage.enium.co.kr:80/"),
    ("hananet-game-20001019", "20001019061522", "http://game.hananet.net:80/"),
    ("hananet-game-20010118", "20010118211100", "http://game.hananet.net:80/"),
    ("hananet-pds-20001018", "20001018214759", "http://pds.hananet.net:80/"),
    ("hananet-pds-20001019", "20001019044248", "http://pds.hananet.net:80/"),
    ("hananet-pds-20010506", "20010506010917", "http://pds.hananet.net:80/"),
    ("cnet-downloads-20001110", "20001110044200", "http://www.korea.cnet.com:80/downloads/"),
    ("cnet-downloads-20010124", "20010124064500", "http://www.korea.cnet.com:80/downloads/"),
]

INTEREST = re.compile(
    r"(?i)(stone\s*age|stoneage|enium|inium|hananet|cnet|download|client|"
    r"setup|install|installer|patch|update|gameplus|\.exe(?:$|[?#])|"
    r"\.zip(?:$|[?#])|\.rar(?:$|[?#])|\.cab(?:$|[?#])|\.lzh(?:$|[?#])|"
    r"스톤\s*에이지|다운로드|설치|패치)"
)
DOWNLOAD_EXT = re.compile(r"(?i)\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)(?:$|[?#])")
WAYBACK_PREFIX = re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/", re.I)


@dataclass(frozen=True)
class Link:
    tag: str
    attr: str
    target: str
    label: str


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[Link] = []
        self._anchor_target: str | None = None
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self._anchor_target = attrs["href"]
            self._anchor_text = []
        for attr in ("src", "action"):
            if attrs.get(attr):
                self.links.append(Link(tag, attr, attrs[attr], ""))

    def handle_data(self, data):
        if self._anchor_target is not None:
            self._anchor_text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._anchor_target is not None:
            self.links.append(
                Link("a", "href", self._anchor_target, " ".join(self._anchor_text).strip())
            )
            self._anchor_target = None
            self._anchor_text = []


def decode_html(data: bytes) -> str:
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1", "replace")


def request(url: str, *, timeout: int = 20) -> bytes:
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


def snapshot_url(timestamp: str, original: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def unwrap_wayback(target: str) -> str:
    return WAYBACK_PREFIX.sub("", target)


def normalize_target(original_page: str, target: str) -> str:
    target = target.strip()
    if not target or target.startswith(("javascript:", "mailto:", "#")):
        return ""
    absolute = urllib.parse.urljoin(original_page, target)
    return unwrap_wayback(absolute)


def classify_link(link: Link, normalized: str) -> str:
    combined = f"{normalized} {link.label}"
    if DOWNLOAD_EXT.search(normalized):
        return "download"
    if INTEREST.search(combined):
        return "interest"
    return "other"


def extract_links(body: bytes, original_page: str) -> list[tuple[str, Link, str]]:
    parser = LinkParser()
    parser.feed(decode_html(body))
    out = []
    seen = set()
    for link in parser.links:
        normalized = normalize_target(original_page, link.target)
        if not normalized:
            continue
        key = (link.tag, link.attr, normalized, " ".join(link.label.split())[:120])
        if key in seen:
            continue
        seen.add(key)
        kind = classify_link(link, normalized)
        out.append((kind, link, normalized))
    return out


def safe(value: str, limit: int = 500) -> str:
    value = " ".join(value.split())
    value = "".join(ch for ch in value if ch >= " " and ch != "\x7f")
    return value[:limit]


def main() -> None:
    print("StoneAge Korea 2000 Wayback snapshot link probe — R1")
    print("SCOPE|link-metadata-only|transient-html|no-page-body|no-client-binary-download")

    total = interest = downloads = 0
    errors = []
    emitted = []

    for surface, timestamp, original in SNAPSHOTS:
        url = snapshot_url(timestamp, original)
        try:
            body = request(url)
            links = extract_links(body, original)
        except Exception as exc:
            errors.append((surface, type(exc).__name__, str(exc)))
            continue
        total += len(links)
        for kind, link, normalized in links:
            if kind == "other":
                continue
            if kind == "download":
                downloads += 1
            interest += 1
            emitted.append(
                (
                    surface,
                    timestamp,
                    kind,
                    link.tag,
                    link.attr,
                    normalized,
                    safe(link.label, 160),
                )
            )

    for surface, kind, message in errors:
        print(f"ERROR|surface={surface}|kind={kind}|message={safe(message)}")
    print(f"COUNT|snapshots|{len(SNAPSHOTS)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|all_links|{total}")
    print(f"COUNT|interesting_links|{interest}")
    print(f"COUNT|download_links|{downloads}")

    for row in sorted(set(emitted)):
        surface, timestamp, kind, tag, attr, target, label = row
        print(
            "LINK|"
            f"surface={surface}|timestamp={timestamp}|kind={kind}|tag={tag}|attr={attr}|"
            f"target={safe(target)}|label={safe(label, 160)}"
        )


if __name__ == "__main__":
    main()
