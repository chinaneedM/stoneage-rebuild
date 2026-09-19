#!/usr/bin/env python3
"""Probe archived Hananet StoneAge board endpoints exposed by 2_5.htm.

Only sparse matching text/link metadata is persisted. Historical HTML is fetched
transiently; no client binary is downloaded.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import html.parser
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
BOARDS = ("STAD", "STAF", "STAN")
TIMESTAMPS = (
    "20010118211100",
    "20010123223000",
    "20010126160100",
    "20010226182509",
    "20010226185448",
)
BASE = "http://www.hananet.net/cgi-bin/pkboard.cgi?k1=GAM2:"
KEY = re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|다운로드|자료|패치|patch|"
    r"update|업데이트|설치|setup|install|client|클라이언트|버전|version|"
    r"\.exe\b|\.zip\b|\.rar\b|\.cab\b|\.lzh\b|"
    r"\b\d+(?:\.\d+){1,3}\b|\b\d+(?:\.\d+)?\s*(?:kb|mb|gb)\b)"
)
FILE_RE = re.compile(r"(?i)\b[a-z0-9][a-z0-9._-]{1,180}\.(?:exe|zip|rar|cab|lzh|lha|msi)\b")
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
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self._href = a["href"]
            self._anchor = []
        elif a.get("href"):
            self.links.append((tag, "href", a["href"], a.get("alt") or a.get("title") or ""))
        for attr in ("src", "action"):
            if a.get(attr):
                self.links.append((tag, attr, a[attr], a.get("alt") or a.get("title") or ""))

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


def request(url, timeout=12):
    last = None
    for attempt in range(3):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), str(getattr(r, "url", url))
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code != 429 or attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = exc
            if attempt == 2:
                raise
            time.sleep(1 + attempt)
    raise RuntimeError(last)


def replay(ts, original):
    return f"https://web.archive.org/web/{ts}id_/{original}"


def decode(data):
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1", "replace")


def normalize(base, target):
    target = target.strip()
    if not target or target.startswith(("javascript:", "mailto:", "#")):
        return ""
    return WAYBACK_PREFIX.sub("", urllib.parse.urljoin(base, target))


def safe(v, limit=700):
    v = " ".join(str(v).split())
    return "".join(ch for ch in v if ch >= " " and ch != "\x7f")[:limit]


def analyze(board, ts):
    original = BASE + board
    data, resolved = request(replay(ts, original))
    p = Parser()
    p.feed(decode(data))
    texts = sorted({safe(x, 420) for x in p.text if KEY.search(x) or FILE_RE.search(x)})
    links = set()
    for tag, attr, target, anchor in p.links:
        n = normalize(original, target)
        if not n:
            continue
        combined = n + " " + anchor
        if KEY.search(combined) or FILE_RE.search(combined) or "pkboard.cgi" in n.lower():
            links.add((tag, attr, safe(n), safe(anchor, 240)))
    files = sorted(set(FILE_RE.findall("\n".join(p.text) + "\n" + "\n".join(x[2] + " " + x[3] for x in links))))
    return {
        "board": board,
        "requested": ts,
        "original": original,
        "resolved": resolved,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "texts": texts,
        "links": sorted(links),
        "files": files,
    }


def main():
    print("StoneAge Hananet board probe — R1")
    print("SCOPE|transient-html|hash-sparse-text-links-only|no-client-binary-download")
    results = []
    errors = []
    jobs = [(b, ts) for b in BOARDS for ts in TIMESTAMPS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(analyze, b, ts): (b, ts) for b, ts in jobs}
        for fut, meta in futs.items():
            b, ts = meta
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append((b, ts, type(exc).__name__, str(exc)))

    print(f"COUNT|jobs|{len(jobs)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|fetched|{len(results)}")

    for b, ts, kind, msg in sorted(errors):
        print(f"ERROR|board={b}|timestamp={ts}|kind={kind}|message={safe(msg)}")

    seen_pages = set()
    for row in sorted(results, key=lambda x: (x["board"], x["requested"])):
        page_key = (row["board"], row["sha256"])
        duplicate = "1" if page_key in seen_pages else "0"
        seen_pages.add(page_key)
        print(
            f"PAGE|board={row['board']}|requested={row['requested']}|duplicate={duplicate}|"
            f"bytes={row['bytes']}|sha256={row['sha256']}|resolved={safe(row['resolved'])}"
        )
        if duplicate == "1":
            continue
        for f in row["files"]:
            print(f"FILE|board={row['board']}|value={safe(f)}")
        for v in row["texts"]:
            print(f"TEXT|board={row['board']}|value={v}")
        for tag, attr, target, anchor in row["links"]:
            print(
                f"LINK|board={row['board']}|tag={tag}|attr={attr}|"
                f"target={target}|anchor={anchor}"
            )


if __name__ == "__main__":
    main()
