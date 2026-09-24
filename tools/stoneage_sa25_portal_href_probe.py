#!/usr/bin/env python3
"""Recover historical portal hrefs for Mainland StoneAge 2.5 distribution pages.

This metadata-only probe replays contemporaneous Sina/17173 page captures and
extracts outbound/download-like hrefs. It never downloads a client payload.
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
SEEDS = (
    ("sina-sa25-upgrade", "http://games.sina.com.cn/newgames/0202/02057854.shtml"),
    ("sina-sa25-upgrade-https", "https://games.sina.com.cn/newgames/0202/02057854.shtml"),
    ("17173-stoneage-subdomain", "http://stoneage.17173.com/banben/sa25-up.htm"),
    ("17173-www-path", "http://www.17173.com/stoneage/banben/sa25-up.htm"),
    ("17173-news-path", "http://news.17173.com/z/stoneage/banben/sa25-up.htm"),
)
TERMS = (
    "指定网址", "指定網址", "完整升级版", "完整升級版", "升级程序", "升級程序",
    "575兆", "580兆", "8.25兆", "石器时代2.5", "石器2.5",
)
PAYLOAD_EXTS = (".exe", ".zip", ".rar", ".cab", ".msi", ".001", ".002", ".iso")
URL_HINTS = ("download", "down", "update", "upgrade", "patch", "setup", "client", "sa25")
NOISE_HINTS = ("/cgi-bin/comment/", "/comment/", "comment.cgi", "javascript:", "mailto:")
MAX_REPLAYS_PER_SEED = 3


def clean(value: object, limit: int = 2400) -> str:
    return " ".join(str(value or "").split()).replace("|", "%7C")[:limit]


def fetch_bytes(url: str, timeout: int = 12) -> tuple[int, str, bytes]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json,text/html,*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return int(getattr(r, "status", r.getcode())), r.geturl(), r.read()


def decode_html(body: bytes) -> tuple[str, str]:
    """Decode preserved Chinese portal HTML using its declared legacy charset."""
    head = body[:16384].lower()
    m = re.search(br"""charset\s*=\s*["']?\s*([a-z0-9._-]+)""", head)
    declared = m.group(1).decode("ascii", "ignore") if m else ""
    aliases = {
        "gb2312": "gb18030", "gbk": "gb18030", "gb_2312-80": "gb18030",
        "utf8": "utf-8", "utf-8": "utf-8", "big5": "big5", "big-5": "big5",
    }
    candidates = []
    if declared:
        candidates.append(aliases.get(declared, declared))
    for enc in ("utf-8", "gb18030", "big5"):
        if enc not in candidates:
            candidates.append(enc)
    best = None
    for enc in candidates:
        try:
            text = body.decode(enc, "replace")
        except LookupError:
            continue
        score = text.count("\ufffd")
        if best is None or score < best[0]:
            best = (score, enc, text)
        if score == 0 and declared:
            break
    if best is None:
        return body.decode("latin1", "replace"), "latin1"
    return best[2], best[1]


def is_candidate_url(absolute: str) -> bool:
    low = urllib.parse.unquote_plus(absolute).lower()
    if any(noise in low for noise in NOISE_HINTS):
        return False
    parsed = urllib.parse.urlsplit(low)
    pathish = parsed.netloc + parsed.path
    return (
        "waei.com.cn" in parsed.netloc
        or any(ext in parsed.path for ext in PAYLOAD_EXTS)
        or any(hint in pathish for hint in URL_HINTS)
    )


def cdx_url(original: str) -> str:
    params = [
        ("url", original),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length"),
        ("filter", "statuscode:200"),
        ("from", "2002"),
        ("to", "2004"),
        ("collapse", "digest"),
        ("limit", "100"),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def parse_cdx(body: bytes) -> list[dict[str, str]]:
    data = json.loads(body.decode("utf-8", "replace"))
    if not isinstance(data, list) or not data:
        return []
    header = data[0]
    return [dict(zip(header, row)) for row in data[1:] if isinstance(row, list)]


def replay_url(timestamp: str, original: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original}"


def extract_hrefs(raw: str, base: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for raw_href in re.findall(r"""(?is)href\s*=\s*["']([^"']+)["']""", raw):
        href = html.unescape(raw_href).strip()
        absolute = urllib.parse.urljoin(base, href)
        if is_candidate_url(absolute):
            out.append((href, absolute))
    return list(dict.fromkeys(out))


def anchor_hrefs(raw: str, base: str) -> list[tuple[str, str, str]]:
    """Return hrefs attached to or immediately surrounded by 2.5 distribution wording."""
    out: list[tuple[str, str, str]] = []
    anchor_re = re.compile(
        r"""(?is)<a\b[^>]*href\s*=\s*["']([^"']+)["'][^>]*>(.*?)</a>"""
    )
    for m in anchor_re.finditer(raw):
        href = html.unescape(m.group(1)).strip()
        absolute = urllib.parse.urljoin(base, href)
        if any(noise in urllib.parse.unquote_plus(absolute).lower() for noise in NOISE_HINTS):
            continue
        inner = html.unescape(re.sub(r"(?s)<[^>]+>", " ", m.group(2)))
        around = raw[max(0, m.start() - 360): min(len(raw), m.end() + 520)]
        context = html.unescape(re.sub(r"(?s)<[^>]+>", " ", around))
        context = " ".join(context.split())
        probe = inner + " " + context
        if any(term.lower() in probe.lower() for term in TERMS):
            out.append((href, absolute, context))
    seen = set()
    dedup = []
    for row in out:
        key = row[1]
        if key not in seen:
            seen.add(key)
            dedup.append(row)
    return dedup


def text_contexts(raw: str) -> list[str]:
    plain = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    plain = html.unescape(re.sub(r"(?s)<[^>]+>", " ", plain))
    plain = " ".join(plain.split())
    low = plain.lower()
    out: list[str] = []
    for term in TERMS:
        idx = low.find(term.lower())
        if idx >= 0:
            out.append(plain[max(0, idx - 180): idx + 520])
    return list(dict.fromkeys(out))


def anchor_contexts(raw: str) -> list[str]:
    out: list[str] = []
    for term in ("指定网址", "指定網址", "完整升级版", "完整升級版", "8.25"):
        for m in re.finditer(re.escape(term), raw, re.I):
            fragment = raw[max(0, m.start() - 500): m.end() + 900]
            if "href" in fragment.lower():
                out.append(fragment)
    return list(dict.fromkeys(out))


def main() -> None:
    print("StoneAge 2.5 historical portal href probe — R1")
    print("SCOPE|Sina+17173|2002-2004-Wayback|HTML-href-recovery|no-client-payload")
    errors: list[tuple[str, str, str]] = []
    all_hrefs: dict[str, tuple[str, str, str, str]] = {}
    anchor_targets: set[str] = set()
    replay_count = 0

    for label, original in SEEDS:
        try:
            status, final, body = fetch_bytes(cdx_url(original))
            rows = parse_cdx(body)
            print(
                f"CDX|label={label}|original={clean(original)}|status={status}|"
                f"bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
                f"rows={len(rows)}|final={clean(final)}"
            )
        except Exception as e:
            errors.append((label + ":cdx", type(e).__name__, str(e)))
            print(f"CDX_ERROR|label={label}|kind={type(e).__name__}|message={clean(e)}")
            continue

        for row in rows[:MAX_REPLAYS_PER_SEED]:
            ts = str(row.get("timestamp") or "")
            src = str(row.get("original") or original)
            if not ts:
                continue
            try:
                status, final, body = fetch_bytes(replay_url(ts, src))
                replay_count += 1
                raw, encoding = decode_html(body)
                hrefs = extract_hrefs(raw, src)
                direct = anchor_hrefs(raw, src)
                contexts = text_contexts(raw)
                anchors = anchor_contexts(raw)
                print(
                    f"REPLAY|label={label}|timestamp={ts}|source={clean(src)}|"
                    f"status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
                    f"encoding={encoding}|hrefs={len(hrefs)}|anchor_hrefs={len(direct)}|contexts={len(contexts)}|anchor_contexts={len(anchors)}|"
                    f"final={clean(final)}"
                )
                for ctx in contexts[:12]:
                    print(f"TEXT_CONTEXT|label={label}|timestamp={ts}|text={clean(ctx)}")
                for frag in anchors[:8]:
                    print(f"ANCHOR_CONTEXT|label={label}|timestamp={ts}|html={clean(frag, 4000)}")
                for href, absolute, context in direct:
                    anchor_targets.add(absolute)
                    all_hrefs[absolute] = (label, ts, src, href)
                    print(f"ANCHOR_HREF|label={label}|timestamp={ts}|href={clean(href)}|absolute={clean(absolute)}|context={clean(context, 3000)}")
                for href, absolute in hrefs:
                    all_hrefs[absolute] = (label, ts, src, href)
                    print(
                        f"HREF|label={label}|timestamp={ts}|source={clean(src)}|"
                        f"href={clean(href)}|absolute={clean(absolute)}"
                    )
            except Exception as e:
                errors.append((f"{label}:replay:{ts}", type(e).__name__, str(e)))
                print(
                    f"REPLAY_ERROR|label={label}|timestamp={ts}|kind={type(e).__name__}|"
                    f"message={clean(e)}"
                )

    strong = []
    for absolute, meta in all_hrefs.items():
        low = urllib.parse.unquote_plus(absolute).lower()
        parsed = urllib.parse.urlsplit(low)
        if (
            absolute in anchor_targets
            or "waei.com.cn" in parsed.netloc
            or any(ext in parsed.path for ext in PAYLOAD_EXTS)
            or any(hint in (parsed.netloc + parsed.path) for hint in URL_HINTS)
        ):
            if not any(noise in low for noise in NOISE_HINTS):
                strong.append((absolute, meta))

    for absolute, (label, ts, src, href) in sorted(strong):
        print(
            f"STRONG_HREF|label={label}|timestamp={ts}|source={clean(src)}|"
            f"href={clean(href)}|absolute={clean(absolute)}"
        )

    for scope, kind, message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|seeds|{len(SEEDS)}")
    print(f"COUNT|replays|{replay_count}")
    print(f"COUNT|unique_relevant_hrefs|{len(all_hrefs)}")
    print(f"COUNT|strong_hrefs|{len(strong)}")
    print(f"COUNT|errors|{len(errors)}")
    if strong:
        print("RESOLUTION|PORTAL_HREF_TARGETS_FOUND|classify exact historical targets before any payload attempt")
    elif replay_count:
        print("RESOLUTION|PORTAL_PAGES_RECOVERED_NO_TARGET_HREF|historical snapshots expose no relevant href on tested variants")
    else:
        print("RESOLUTION|PORTAL_CAPTURE_UNRECOVERED|tested historical portal variants did not replay")


if __name__ == "__main__":
    main()
