#!/usr/bin/env python3
"""Recover sparse attachment/download metadata from Hananet STAD StoneAge posts 8119/8120.

Known board rows:
  8119 = 정식 버전, 260 M
  8120 = 체험 버전, 240 M

Archived HTML is fetched transiently. Only short relevant text, attributes and URL/file
tokens are emitted; no client binary is downloaded.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import html.parser
import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
AVAIL = "https://archive.org/wayback/available"
KNOWN_TS = "20010814230641"
DATES = ["20010210", "20010215", "20010401", "20010814", "20011231"]

POSTS = [
    (
        "8119-formal-260M",
        "8119",
        "http://www.hananet.net/cgi-bin/pkboard.cgi?"
        "k1=GAM2:STAD:4:2000000000:0:12:1:2:1&k2=8119:1:0:0&k3=0::",
    ),
    (
        "8120-trial-240M",
        "8120",
        "http://www.hananet.net/cgi-bin/pkboard.cgi?"
        "k1=GAM2:STAD:4:2000000000:0:12:1:2:1&k2=8120:2:0:0&k3=0::",
    ),
]

FILE_RE = re.compile(r"(?i)\b[a-z0-9][a-z0-9._-]{1,180}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)\b")
URL_RE = re.compile(r"(?i)(?:https?|ftp)://[^\s\"'<>]+")
INTEREST_RE = re.compile(
    r"(?i)(download|down/|attach|file|save|받기|다운|첨부|파일|"
    r"stoneage|스톤\s*에이지|\.exe|\.zip|8119|8120)"
)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs = []
        self.text = []
        self._anchor_href = None
        self._anchor_text = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        amap = dict(attrs)
        if tag == "a" and amap.get("href"):
            self._anchor_href = amap["href"]
            self._anchor_text = []
        for name, value in attrs:
            if value and name.lower() in (
                "href", "src", "action", "onclick", "onmousedown",
                "onmouseup", "value", "name", "id"
            ):
                self.attrs.append((tag, name.lower(), value))

    def handle_data(self, data):
        if data.strip():
            self.text.append(data)
        if self._anchor_href is not None:
            self._anchor_text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._anchor_href is not None:
            self.attrs.append(("a", "anchor", " ".join(self._anchor_text).strip()))
            self._anchor_href = None
            self._anchor_text = []


def request(url: str, timeout: int = 15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), str(getattr(r, "url", url)), str(getattr(r, "status", ""))


def decode(data: bytes):
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1", "replace")


def availability(url: str, date: str):
    q = urllib.parse.urlencode({"url": url, "timestamp": date})
    body, _, _ = request(AVAIL + "?" + q, timeout=8)
    obj = json.loads(body.decode("utf-8", "replace"))
    c = obj.get("archived_snapshots", {}).get("closest")
    if not isinstance(c, dict) or not c.get("available"):
        return None
    return str(c.get("timestamp", "")), str(c.get("status", "")), str(c.get("url", ""))


def replay(ts: str, url: str):
    return f"https://web.archive.org/web/{ts}id_/{url}"


def safe(v, limit=800):
    v = " ".join(str(v).split())
    return "".join(ch for ch in v if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def normalize(base: str, target: str):
    target = target.strip()
    if not target:
        return ""
    if target.lower().startswith(("javascript:", "mailto:", "#")):
        return target
    return urllib.parse.urljoin(base, target)


def relevant_text(parts):
    out = []
    seen = set()
    for part in parts:
        line = safe(part, 300)
        if line and INTEREST_RE.search(line) and line not in seen:
            seen.add(line)
            out.append(line)
    return out


def extract(label, post_id, original, ts, body, resolved, status):
    text = decode(body)
    p = Parser()
    p.feed(text)

    attrs = []
    for tag, attr, value in p.attrs:
        if INTEREST_RE.search(value) or FILE_RE.search(value) or URL_RE.search(value):
            attrs.append((tag, attr, normalize(original, value)))

    # Catch URLs/file tokens embedded in inline JS/text that are not normal attributes.
    raw_tokens = set(URL_RE.findall(text))
    raw_tokens.update(FILE_RE.findall(text))
    for m in re.finditer(r"(?i)[^\"'\s<>]{0,80}(?:download|attach|down/)[^\"'\s<>]{0,180}", text):
        raw_tokens.add(m.group(0))

    return {
        "label": label,
        "post_id": post_id,
        "timestamp": ts,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "resolved": resolved,
        "status": status,
        "attrs": sorted(set(attrs)),
        "text": relevant_text(p.text),
        "tokens": sorted(safe(x, 500) for x in raw_tokens if x),
    }


def main():
    print("StoneAge Hananet STAD detail/attachment probe — R1")
    print("SCOPE|transient-html|sparse-attachment-metadata-only|no-client-binary-download")

    candidates = {}
    errors = []

    # Known list-page snapshot may replay detail URLs even if Availability is sparse.
    for label, post_id, original in POSTS:
        candidates[(label, post_id, KNOWN_TS, original)] = "known-parent-snapshot"

    jobs = [(label, post_id, original, date) for label, post_id, original in POSTS for date in DATES]

    def one(job):
        label, post_id, original, date = job
        try:
            hit = availability(original, date)
        except Exception as exc:
            return ("error", label, post_id, original, date, type(exc).__name__, str(exc))
        if not hit:
            return ("miss", label, post_id, original, date, "", "")
        ts, status, archived = hit
        return ("hit", label, post_id, original, date, ts, status)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for row in ex.map(one, jobs):
            if row[0] == "error":
                _, label, post_id, original, date, kind, msg = row
                errors.append(("availability", label, post_id, date, kind, msg))
            elif row[0] == "hit":
                _, label, post_id, original, date, ts, status = row
                candidates[(label, post_id, ts, original)] = f"availability:{date}:{status}"

    results = []
    for (label, post_id, ts, original), source in sorted(candidates.items()):
        try:
            body, resolved, status = request(replay(ts, original), timeout=15)
            results.append((source, extract(label, post_id, original, ts, body, resolved, status)))
        except Exception as exc:
            errors.append(("replay", label, post_id, ts, type(exc).__name__, str(exc)))

    print(f"COUNT|availability_queries|{len(jobs)}")
    print(f"COUNT|candidate_snapshots|{len(candidates)}")
    print(f"COUNT|replayed|{len(results)}")
    print(f"COUNT|errors|{len(errors)}")

    for phase, label, post_id, marker, kind, msg in errors:
        print(
            f"ERROR|phase={phase}|post={safe(post_id)}|label={safe(label)}|"
            f"marker={safe(marker)}|kind={safe(kind)}|message={safe(msg)}"
        )

    for source, row in results:
        print(
            f"PAGE|post={row['post_id']}|label={safe(row['label'])}|timestamp={row['timestamp']}|"
            f"source={safe(source)}|status={safe(row['status'])}|bytes={row['bytes']}|"
            f"sha256={row['sha256']}|resolved={safe(row['resolved'])}"
        )
        for text in row["text"]:
            print(f"TEXT|post={row['post_id']}|timestamp={row['timestamp']}|value={safe(text,300)}")
        for tag, attr, value in row["attrs"]:
            print(
                f"ATTR|post={row['post_id']}|timestamp={row['timestamp']}|"
                f"tag={safe(tag)}|attr={safe(attr)}|value={safe(value,700)}"
            )
        for token in row["tokens"]:
            if INTEREST_RE.search(token) or FILE_RE.search(token):
                print(f"TOKEN|post={row['post_id']}|timestamp={row['timestamp']}|value={safe(token,700)}")


if __name__ == "__main__":
    main()
