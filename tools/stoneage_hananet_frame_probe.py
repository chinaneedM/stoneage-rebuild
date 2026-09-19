#!/usr/bin/env python3
"""Probe preserved Hananet/GamePlus frame pages for StoneAge download-path tokens.

Only hashes, sparse matching text, and matching link targets are committed.
Historical HTML bodies are fetched transiently.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import html.parser
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"

CANDIDATES = [
    ("game-20001019-mainbody", "20001019061522", "http://game.hananet.net:80/gamenet/mainbody.html"),
    ("game-20001019-maintop", "20001019061522", "http://game.hananet.net:80/gamenet/maintop.html"),
    ("game-20010118-mainbody", "20010118211100", "http://game.hananet.net:80/gamenet/mainbody.html"),
    ("game-20010118-maintop", "20010118211100", "http://game.hananet.net:80/gamenet/maintop.html"),
    ("game-20010118-mapstoneage", "20010118211100", "http://game.hananet.net:80/gamenet/sitemap/map/mapstoneage.html"),
    ("game-20010118-frstoneage", "20010118211100", "http://game.hananet.net:80/gamenet/newframe/frstoneage.html"),
    ("pds-20001018-index2", "20001018214759", "http://pds.hananet.net:80/index2.html"),
    ("pds-20001018-topfrm", "20001018214759", "http://pds.hananet.net:80/topfrm.html"),
    ("pds-20001019-index2", "20001019044248", "http://pds.hananet.net:80/index2.html"),
    ("pds-20001019-topfrm", "20001019044248", "http://pds.hananet.net:80/topfrm.html"),
    ("pds-20010506-index2", "20010506010917", "http://pds.hananet.net:80/index2.html"),
    ("pds-20010506-topfrm", "20010506010917", "http://pds.hananet.net:80/topfrm.html"),
]

INTEREST = re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|"
    r"client|setup|install|patch|update|gameplus|\.exe(?:$|[?#])|"
    r"\.zip(?:$|[?#])|\.rar(?:$|[?#])|\.cab(?:$|[?#]))"
)
WAYBACK_PREFIX = re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/", re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.text = []
        self._href = None
        self._anchor = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self._href = attrs["href"]
            self._anchor = []
        for attr in ("src", "action"):
            if attrs.get(attr):
                self.links.append((tag, attr, attrs[attr], ""))

    def handle_data(self, data):
        if data.strip():
            self.text.append(data)
        if self._href is not None:
            self._anchor.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.links.append(("a", "href", self._href, " ".join(self._anchor).strip()))
            self._href = None
            self._anchor = []


def request(url: str, timeout: int = 12):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def replay(timestamp: str, original: str):
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def decode(data: bytes):
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1", "replace")


def normalize(base: str, target: str):
    target = target.strip()
    if not target or target.startswith(("javascript:", "mailto:", "#")):
        return ""
    target = urllib.parse.urljoin(base, target)
    return WAYBACK_PREFIX.sub("", target)


def safe(value: str, limit: int = 500):
    value = " ".join(value.split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f")[:limit]


def analyze(label: str, timestamp: str, original: str):
    data = request(replay(timestamp, original))
    parser = Parser()
    parser.feed(decode(data))
    snippets = sorted({
        safe(x, 260)
        for x in parser.text
        if INTEREST.search(x)
    })
    links = set()
    for tag, attr, target, anchor in parser.links:
        normalized = normalize(original, target)
        if not normalized:
            continue
        if INTEREST.search(normalized + " " + anchor):
            links.add((tag, attr, safe(normalized), safe(anchor, 180)))
    return {
        "label": label,
        "timestamp": timestamp,
        "original": original,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "snippets": snippets,
        "links": sorted(links),
    }


def main():
    print("StoneAge Hananet frame-path recovery probe — R1")
    print("SCOPE|transient-html|hash-sparse-text-matching-links-only|no-client-binary-download")

    results = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {
            ex.submit(analyze, label, ts, original): (label, ts, original)
            for label, ts, original in CANDIDATES
        }
        for future, meta in futures.items():
            label, ts, original = meta
            try:
                results.append(future.result())
            except Exception as exc:
                errors.append((label, ts, original, type(exc).__name__, str(exc)))

    print(f"COUNT|candidates|{len(CANDIDATES)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|fetched_pages|{len(results)}")
    print(f"COUNT|matching_snippets|{sum(len(x['snippets']) for x in results)}")
    print(f"COUNT|matching_links|{sum(len(x['links']) for x in results)}")

    for label, ts, original, kind, message in sorted(errors):
        print(
            f"ERROR|label={safe(label)}|timestamp={ts}|kind={kind}|"
            f"original={safe(original)}|message={safe(message)}"
        )

    for row in sorted(results, key=lambda x: x["label"]):
        print(
            f"PAGE|label={row['label']}|timestamp={row['timestamp']}|"
            f"bytes={row['bytes']}|sha256={row['sha256']}|original={safe(row['original'])}"
        )
        for value in row["snippets"]:
            print(f"TEXT|label={row['label']}|value={value}")
        for tag, attr, target, anchor in row["links"]:
            print(
                f"LINK|label={row['label']}|tag={tag}|attr={attr}|"
                f"target={target}|anchor={anchor}"
            )


if __name__ == "__main__":
    main()
