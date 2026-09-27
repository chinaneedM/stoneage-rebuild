#!/usr/bin/env python3
"""Replay the single indexed JHPOP launch-window root capture.

The launch-window CDX census found exactly one historical JHPOP URL:
http://www.jhpop.com:80/ at 2000-12-04 16:03:00 UTC.  This probe replays only
that exact small HTML object and extracts first-hop navigation targets.
No software payload is fetched.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
TIMESTAMP = "20001204160300"
ORIGINAL = "http://www.jhpop.com:80/"
MAX_BODY = 256 * 1024
TOKENS = (
    "石器时代", "石器時代", "华义", "華義", "测试", "測試", "试玩", "試玩",
    "StoneAge", "WGS", "download", "game",
)


def clean(value, limit=5000):
    return " ".join(str(value if value is not None else "").split()).replace("|", "%7C")[:limit]


def replay_url(timestamp=TIMESTAMP, original=ORIGINAL):
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def fetch(url, timeout=35, max_bytes=MAX_BODY):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,text/plain,*/*;q=0.1",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError(f"response-too-large:{len(body)}")
        return int(getattr(response, "status", response.getcode())), response.geturl(), body


def decode(body):
    for enc in ("gb18030", "gbk", "big5", "utf-8", "latin1"):
        try:
            return enc, body.decode(enc)
        except UnicodeDecodeError:
            pass
    return "latin1", body.decode("latin1", "replace")


def title(text):
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", text)
    if not m:
        return ""
    return clean(html.unescape(re.sub(r"(?s)<[^>]+>", " ", m.group(1))), 500)


def plain(text):
    value = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", text)
    value = html.unescape(re.sub(r"(?s)<[^>]+>", " ", value))
    return re.sub(r"\s+", " ", value).strip()


def targets(text, base=ORIGINAL):
    found = []
    patterns = (
        ("href", r"(?is)\bhref\s*=\s*[\"']([^\"']+)[\"']"),
        ("frame", r"(?is)<(?:frame|iframe)\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']"),
        ("script", r"(?is)<script\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']"),
        ("img", r"(?is)<img\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']"),
    )
    for kind, pattern in patterns:
        for m in re.finditer(pattern, text):
            raw = html.unescape(m.group(1)).strip()
            if not raw or raw.lower().startswith(("javascript:", "mailto:", "#")):
                continue
            found.append((kind, urllib.parse.urljoin(base, raw)))
    for m in re.finditer(
        r"(?is)<meta\b[^>]*http-equiv\s*=\s*[\"']?refresh[\"']?[^>]*content\s*=\s*[\"']([^\"']+)[\"']",
        text,
    ):
        content = html.unescape(m.group(1))
        mm = re.search(r"(?i)url\s*=\s*(.+)$", content)
        if mm:
            found.append(("meta-refresh", urllib.parse.urljoin(base, mm.group(1).strip(" \"'"))))
    # Handle reversed meta attribute order.
    for m in re.finditer(
        r"(?is)<meta\b[^>]*content\s*=\s*[\"']([^\"']+)[\"'][^>]*http-equiv\s*=\s*[\"']?refresh[\"']?",
        text,
    ):
        content = html.unescape(m.group(1))
        mm = re.search(r"(?i)url\s*=\s*(.+)$", content)
        if mm:
            found.append(("meta-refresh", urllib.parse.urljoin(base, mm.group(1).strip(" \"'"))))
    out = []
    seen = set()
    for item in found:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return tuple(out)


def token_hits(text):
    low = text.lower()
    return tuple(token for token in TOKENS if token.lower() in low)


def main():
    print("StoneAge Jinghe/JHPOP Dec-2000 root replay — R1")
    print(f"TARGET|timestamp={TIMESTAMP}|original={ORIGINAL}|exact-single-capture|no software payload")
    try:
        status, final, body = fetch(replay_url())
        encoding, text = decode(body)
        nav = targets(text)
        hits = token_hits(text)
        body_text = plain(text)
        print(
            "PAGE|status={}|bytes={}|sha256={}|encoding={}|title={}|token_hits={}|targets={}|final={}".format(
                status, len(body), hashlib.sha256(body).hexdigest(), encoding,
                title(text), clean(",".join(hits), 1000), len(nav), clean(final)
            )
        )
        for kind, url in nav:
            print(f"TARGET_LINK|kind={clean(kind)}|url={clean(url)}")
        if body_text:
            print(f"TEXT|{clean(body_text, 2000)}")
        print(f"COUNT|targets|{len(nav)}")
        print(f"COUNT|token_hits|{len(hits)}")
        if nav:
            print("RESOLUTION|JHPOP_ROOT_TARGETS_FOUND|CDX/replay only exact first-hop targets next")
        elif hits:
            print("RESOLUTION|JHPOP_ROOT_SEMANTIC_ONLY|preserve tokens; seek archived sibling URLs externally")
        else:
            print("RESOLUTION|JHPOP_ROOT_STUB|root capture exposes neither semantic token nor first-hop target")
    except Exception as exc:
        print(f"ERROR|kind={clean(type(exc).__name__)}|message={clean(exc)}")
        print("RESOLUTION|JHPOP_ROOT_REPLAY_FAILED|retry this exact archived object only")
    print("EVIDENCE_BOUNDARY|This replay establishes only the content/navigation of one archived root HTML object.")


if __name__ == "__main__":
    main()
