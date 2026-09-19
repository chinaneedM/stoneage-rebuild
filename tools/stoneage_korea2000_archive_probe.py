#!/usr/bin/env python3
"""Probe public web-archive indexes for StoneAge Korea 2000 download-path metadata.

This tool stores only archive index metadata and extracted link targets.
It does not download or preserve client binaries.
"""

from __future__ import annotations

import argparse
import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass


UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
WAYBACK = "https://web.archive.org/web/{timestamp}id_/{url}"

DOWNLOAD_EXT = re.compile(
    r"(?i)\.(?:exe|zip|rar|cab|lzh|lha|arj|gz|tgz|bz2|msi)(?:$|[?#])"
)
INTEREST = re.compile(
    r"(?i)(stone\s*age|stoneage|client|download|setup|install|patch|update|"
    r"gameplus|게임플러스|스톤에이지|다운로드|설치|패치)"
)


@dataclass(frozen=True)
class Hit:
    surface: str
    timestamp: str
    original: str
    status: str
    mimetype: str
    digest: str
    length: str


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        attrs = dict(attrs)
        self._href = attrs.get("href")
        self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, "".join(self._text).strip()))
            self._href = None
            self._text = []


def request(url: str, *, timeout: int = 30) -> bytes:
    last = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"request failed: {url}: {last}")


def cdx_query(url_pattern: str, start: int, end: int, *, regex: str | None = None):
    params = [
        ("url", url_pattern),
        ("from", str(start)),
        ("to", str(end)),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length"),
        ("filter", "statuscode:200"),
        ("collapse", "urlkey"),
        ("limit", "10000"),
    ]
    if regex:
        params.append(("filter", "original:" + regex))
    url = CDX + "?" + urllib.parse.urlencode(params)
    raw = request(url)
    rows = json.loads(raw.decode("utf-8", "replace"))
    if not rows:
        return []
    header, *body = rows
    indexes = {name: i for i, name in enumerate(header)}
    out = []
    for row in body:
        if not isinstance(row, list) or len(row) < len(header):
            continue
        out.append(
            {
                key: row[idx]
                for key, idx in indexes.items()
            }
        )
    return out


def archive_links(timestamp: str, original: str):
    url = WAYBACK.format(
        timestamp=timestamp,
        url=urllib.parse.quote(original, safe=":/?&=%#+,;@[]!$'()*"),
    )
    try:
        body = request(url, timeout=45)
    except RuntimeError:
        return []
    text = body.decode("utf-8", "replace")
    parser = LinkParser()
    try:
        parser.feed(text)
    except Exception:
        return []
    found = []
    for href, anchor in parser.links:
        absolute = urllib.parse.urljoin(original, href)
        if DOWNLOAD_EXT.search(absolute) or INTEREST.search(absolute) or INTEREST.search(anchor):
            found.append((absolute, anchor))
    return found


def safe_token(value: str):
    # Keep URL/path token but normalize controls and cap pathological archive junk.
    value = "".join(ch for ch in value if ch >= " " and ch != "\x7f")
    return value[:500]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from-year", type=int, default=2000)
    p.add_argument("--to-year", type=int, default=2003)
    p.add_argument("--root-only", action="store_true")
    args = p.parse_args()

    surfaces = [
        # Operator site: the entire host is StoneAge-specific, so keep all indexed URLs.
        ("inium", "stoneage.enium.co.kr/*", None),
        # Portal/download surfaces: retain only URL-level StoneAge terms when possible.
        ("hananet-game", "game.hananet.net/*", r".*(?:[Ss][Tt][Oo][Nn][Ee]|[Aa][Gg][Ee]).*"),
        ("hananet-pds", "pds.hananet.net/*", r".*(?:[Ss][Tt][Oo][Nn][Ee]|[Aa][Gg][Ee]).*"),
        ("cnet-downloads", "korea.cnet.com/downloads/*", r".*(?:[Ss][Tt][Oo][Nn][Ee]|[Aa][Gg][Ee]).*"),
    ]
    roots = [
        ("inium-root", "stoneage.enium.co.kr/"),
        ("hananet-game-root", "game.hananet.net/"),
        ("hananet-pds-root", "pds.hananet.net/"),
        ("cnet-downloads-root", "korea.cnet.com/downloads/"),
    ]

    hits: list[Hit] = []
    errors = []

    if not args.root_only:
        for surface, pattern, regex in surfaces:
            try:
                rows = cdx_query(pattern, args.from_year, args.to_year, regex=regex)
            except Exception as exc:
                errors.append((surface, type(exc).__name__, str(exc)))
                continue
            for row in rows:
                hits.append(
                    Hit(
                        surface,
                        str(row.get("timestamp", "")),
                        str(row.get("original", "")),
                        str(row.get("statuscode", "")),
                        str(row.get("mimetype", "")),
                        str(row.get("digest", "")),
                        str(row.get("length", "")),
                    )
                )

    if args.root_only:
        roots = [x for x in roots if x[0] == "inium-root"]

    root_rows = []
    for surface, pattern in roots:
        try:
            rows = cdx_query(pattern, args.from_year, args.to_year)
        except Exception as exc:
            errors.append((surface, type(exc).__name__, str(exc)))
            continue
        if rows:
            # One collapsed root URL is enough to mine links from a period snapshot.
            row = rows[0]
            root_rows.append((surface, row))

    print("StoneAge Korea 2000 public-distribution archive probe — R1")
    print("SCOPE|metadata-and-link-targets-only|no-client-binary-download")
    print(f"YEARS|from={args.from_year}|to={args.to_year}")
    print(f"MODE|{'root-only' if args.root_only else 'full'}")
    for surface, kind, message in errors:
        print(f"ERROR|{surface}|{kind}|{safe_token(message)}")

    # Deterministic metadata listing.
    uniq = {}
    for hit in hits:
        key = (hit.surface, hit.original)
        uniq.setdefault(key, hit)
    print(f"COUNT|indexed_candidate_urls|{len(uniq)}")
    for hit in sorted(uniq.values(), key=lambda h: (h.surface, h.original.lower(), h.timestamp)):
        print(
            "URL|"
            + "|".join(
                safe_token(x)
                for x in (
                    hit.surface,
                    hit.timestamp,
                    hit.status,
                    hit.mimetype,
                    hit.length,
                    hit.digest,
                    hit.original,
                )
            )
        )

    extracted = set()
    for surface, row in root_rows:
        timestamp = str(row.get("timestamp", ""))
        original = str(row.get("original", ""))
        for target, anchor in archive_links(timestamp, original):
            if not target:
                continue
            if not (DOWNLOAD_EXT.search(target) or INTEREST.search(target) or INTEREST.search(anchor)):
                continue
            extracted.add((surface, timestamp, target, anchor))

    print(f"COUNT|root_snapshot_interesting_links|{len(extracted)}")
    for surface, timestamp, target, anchor in sorted(extracted):
        print(
            "LINK|"
            + "|".join(
                safe_token(x)
                for x in (surface, timestamp, target, anchor)
            )
        )


if __name__ == "__main__":
    main()
