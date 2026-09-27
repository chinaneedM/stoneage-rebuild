#!/usr/bin/env python3
"""Probe the historical Yegame game-product catalog for StoneAge identifiers.

Source-grounded entry point:
    JHPOP root (2000-12-04) -> yegame.com
    Yegame Feb-2001 product pages -> /product/game/index.asp

This probe first inventories only the /product/game/ Wayback namespace for
2001, then replays a bounded set of archived HTML catalog pages. It never
fetches linked software payloads.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
FROM = "20010201"
TO = "20011231"
FIELDS = "timestamp,original,statuscode,mimetype,digest,length,redirect"

QUERIES = (
    ("game-prefix", "http://www.yegame.com/product/game/", "prefix"),
    ("game-prefix-port80", "http://www.yegame.com:80/product/game/", "prefix"),
    ("game-index", "http://www.yegame.com/product/game/index.asp", "exact"),
    ("game-index-port80", "http://www.yegame.com:80/product/game/index.asp", "exact"),
)

STONE_TOKENS = (
    "石器时代", "石器時代", "石器",
    "stoneage", "stone age",
    "华义", "華義", "waei",
    "北京华义", "北京華義",
    "智冠", "金海湾", "金海灣",
    "晶合", "jhpop",
    "测试", "測試", "试玩", "試玩",
    "光盘", "光碟", "cd-rom", "cdrom",
    "客户端", "客戶端", "client",
)

PAGE_NAMES = ("index.asp", "prod_secshow.asp", "detail.asp")


def clean(value, limit=7000):
    return " ".join(str(value if value is not None else "").split()).replace("|", "%7C")[:limit]


def fetch(url, timeout=60, max_bytes=4 * 1024 * 1024):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json,text/html,*/*;q=0.2",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError(f"response-too-large:{len(body)}")
        return int(getattr(response, "status", response.getcode())), response.geturl(), body


def cdx_url(url, match):
    params = [
        ("url", url),
        ("matchType", match),
        ("output", "json"),
        ("fl", FIELDS),
        ("from", FROM),
        ("to", TO),
        ("limit", "50000"),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def parse_cdx(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, row)) for row in obj[1:] if isinstance(row, list))


def decode(body):
    for enc in ("gb18030", "gbk", "big5", "cp950", "utf-8", "latin1"):
        try:
            return enc, body.decode(enc)
        except UnicodeDecodeError:
            continue
    return "latin1", body.decode("latin1", "replace")


def visible_text(text):
    value = re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>", " ", text)
    value = re.sub(r"(?is)<[^>]+>", " ", value)
    return clean(html.unescape(value), 60000)


def title(text):
    m = re.search(r"(?is)<title\b[^>]*>(.*?)</title>", text)
    if not m:
        return ""
    return clean(html.unescape(re.sub(r"(?is)<[^>]+>", " ", m.group(1))))


def token_hits(text):
    low = text.lower()
    return tuple(token for token in STONE_TOKENS if token.lower() in low)


def snippets(text, hits, radius=340):
    low = text.lower()
    out = []
    seen = set()
    for token in hits:
        token_low = token.lower()
        start = 0
        while True:
            idx = low.find(token_low, start)
            if idx < 0:
                break
            frag = clean(text[max(0, idx-radius):min(len(text), idx+len(token)+radius)], 1200)
            key = frag[:350]
            if key and key not in seen:
                seen.add(key)
                out.append((token, frag))
            start = idx + max(1, len(token))
            if len(out) >= 16:
                return tuple(out)
    return tuple(out)


def links(text, base):
    out = []
    seen = set()
    for m in re.finditer(r"(?is)<a\b[^>]*href\s*=\s*([\"'])(.*?)\1[^>]*>(.*?)</a>", text):
        raw = html.unescape(m.group(2)).strip()
        if not raw or raw.lower().startswith(("javascript:", "mailto:", "#")):
            continue
        url = urllib.parse.urljoin(base, raw)
        anchor = clean(html.unescape(re.sub(r"(?is)<[^>]+>", " ", m.group(3))), 1200)
        key = (url, anchor)
        if key not in seen:
            seen.add(key)
            out.append(key)
    return tuple(out)


def product_code(url):
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(str(url or "")).query)
    for key in ("prodencode", "ProdEncode", "PRODENCODE"):
        vals = q.get(key)
        if vals:
            return str(vals[0])
    m = re.search(r"(?:[?&]prodencode=)([^&#]+)", str(url or ""), flags=re.I)
    return urllib.parse.unquote_plus(m.group(1)) if m else ""


def candidate_page(original):
    path = urllib.parse.urlsplit(str(original or "")).path.lower()
    return path.endswith(PAGE_NAMES)


def main():
    print("StoneAge Yegame 2001 game-catalog archaeology — R1")
    print("SOURCE_CHAIN|JHPOP 20001204 -> Yegame -> /product/game/index.asp")
    print(f"SCOPE|Wayback CDX + bounded HTML replay|{FROM}..{TO}|game catalog only|no software payload")
    rows = {}
    errors = []

    for label, url, match in QUERIES:
        try:
            status, final, body = fetch(cdx_url(url, match))
            parsed = parse_cdx(body)
            print(
                "QUERY|label={}|status={}|rows={}|bytes={}|sha256={}|final={}".format(
                    clean(label), status, len(parsed), len(body),
                    hashlib.sha256(body).hexdigest(), clean(final)
                )
            )
            for row in parsed:
                key = (
                    str(row.get("timestamp") or ""),
                    str(row.get("original") or ""),
                    str(row.get("statuscode") or ""),
                    str(row.get("digest") or ""),
                )
                rows[key] = row
        except Exception as exc:
            errors.append((label, "cdx", type(exc).__name__, str(exc)))

    ordered = sorted(rows.values(), key=lambda r: (str(r.get("timestamp") or ""), str(r.get("original") or "")))
    for row in ordered:
        original = str(row.get("original") or "")
        print(
            "ROW|timestamp={}|status={}|mime={}|length={}|digest={}|prodencode={}|original={}".format(
                clean(row.get("timestamp")), clean(row.get("statuscode")), clean(row.get("mimetype")),
                clean(row.get("length")), clean(row.get("digest")), clean(product_code(original)),
                clean(original)
            )
        )

    # Replay only one earliest capture per original URL, capped.
    selected = []
    seen_originals = set()
    for row in ordered:
        original = str(row.get("original") or "")
        if original in seen_originals:
            continue
        if str(row.get("statuscode") or "") != "200":
            continue
        if "html" not in str(row.get("mimetype") or "").lower():
            continue
        if not candidate_page(original):
            continue
        seen_originals.add(original)
        selected.append(row)
        if len(selected) >= 24:
            break

    stone_pages = 0
    product_links = {}
    for row in selected:
        timestamp = str(row.get("timestamp") or "")
        original = str(row.get("original") or "")
        replay = f"https://web.archive.org/web/{timestamp}id_/{original}"
        try:
            status, final, body = fetch(replay)
            encoding, text = decode(body)
            visible = visible_text(text)
            hits = token_hits(visible)
            page_links = links(text, original)
            if any(t.lower() in visible.lower() for t in ("石器时代", "石器時代", "stoneage", "stone age")):
                stone_pages += 1
            print(
                "PAGE|timestamp={}|status={}|bytes={}|sha256={}|encoding={}|title={}|token_hits={}|links={}|original={}|final={}".format(
                    clean(timestamp), status, len(body), hashlib.sha256(body).hexdigest(),
                    clean(encoding), clean(title(text)), clean(",".join(hits), 2500),
                    len(page_links), clean(original), clean(final)
                )
            )
            for token, fragment in snippets(visible, hits):
                print(f"SNIPPET|timestamp={clean(timestamp)}|token={clean(token)}|text={clean(fragment, 1400)}")
            for url, anchor in page_links:
                code = product_code(url)
                if code:
                    product_links.setdefault((code, url, anchor), set()).add(timestamp)
                if code or any(t.lower() in (anchor + " " + url).lower() for t in STONE_TOKENS):
                    print(
                        "CATALOG_LINK|timestamp={}|prodencode={}|anchor={}|url={}".format(
                            clean(timestamp), clean(code), clean(anchor, 1600), clean(url)
                        )
                    )
        except Exception as exc:
            errors.append((original, "replay", type(exc).__name__, str(exc)))

    for (code, url, anchor), timestamps in sorted(product_links.items()):
        print(
            "PRODUCT|prodencode={}|captures={}|anchor={}|url={}".format(
                clean(code), clean(",".join(sorted(timestamps))), clean(anchor, 1600), clean(url)
            )
        )

    print(f"COUNT|unique_cdx_rows|{len(ordered)}")
    print(f"COUNT|replayed_pages|{len(selected)}")
    print(f"COUNT|stone_pages|{stone_pages}")
    print(f"COUNT|product_links|{len(product_links)}")
    for label, scope, kind, message in errors:
        print(f"ERROR|label={clean(label)}|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|errors|{len(errors)}")

    if stone_pages:
        print("RESOLUTION|STONEAGE_CATALOG_PAGE_FOUND|bind product code/detail route and carrier metadata next")
    elif selected and product_links:
        print("RESOLUTION|GAME_CATALOG_RECOVERED_NO_STONE_TOKEN|inspect product names/codes and adjacent captures next")
    elif ordered:
        print("RESOLUTION|GAME_NAMESPACE_FOUND_NO_REPLAYABLE_CATALOG|use exact archived URLs as next targets")
    elif errors:
        print("RESOLUTION|PARTIAL_GAME_CATALOG_PROBE|retry failed archive surfaces only")
    else:
        print("RESOLUTION|YEGAME_GAME_CATALOG_INDEX_BOUNDED|switch to linked game.popsoft historical surface")
    print("EVIDENCE_BOUNDARY|Catalog HTML can identify historical product/navigation metadata only; no linked installer/archive is fetched.")


if __name__ == "__main__":
    main()
