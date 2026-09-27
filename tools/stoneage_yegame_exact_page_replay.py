#!/usr/bin/env python3
"""Replay the exact historical yegame.com pages exposed by the launch-window census.

This is a narrow follow-up to the JHPOP -> yegame.com first-hop recovery. It
replays only the seven exact captures already enumerated by
STONEAGE-YEGAME-2000-TEST-CD-ARCHIVE-R1.txt, extracts navigation and
archaeology-relevant text, and does not fetch any linked software payload.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"

CAPTURES = (
    ("root", "20010202023100", "http://www.yegame.com:80/"),
    ("business-login", "20010205004600", "http://www.yegame.com:80/business/login.asp"),
    ("default", "20010207160624", "http://www.yegame.com:80/default.htm"),
    ("product-empolder", "20010207164059", "http://www.yegame.com:80/product/empolder/index.asp"),
    ("product-study", "20010207201258", "http://www.yegame.com:80/product/study/index.asp"),
    ("product-tools", "20010207202054", "http://www.yegame.com:80/product/tools/index.asp"),
    ("product-system", "20010207202723", "http://www.yegame.com:80/product/system/index.asp"),
)

TOKENS = (
    "石器时代", "石器時代", "石器", "stoneage", "stone age",
    "游戏", "遊戲", "game", "下载", "下載", "download", "试玩", "試玩",
    "晶合", "jhpop", "华义", "華義", "waei", "客户端", "客戶端", "client",
    "光盘", "光碟", "cd-rom", "cdrom", "测试", "測試", "test", "beta",
)

TARGET_HINTS = (
    "stone", "game", "download", "soft", "product", "demo", "trial",
    "client", "cd", "jhpop", "waei", "yegame",
)


def clean(value, limit=6000):
    return " ".join(str(value if value is not None else "").split()).replace("|", "%7C")[:limit]


def fetch(url, timeout=45, max_bytes=2 * 1024 * 1024):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,*/*;q=0.2",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError(f"response-too-large:{len(body)}")
        return int(getattr(response, "status", response.getcode())), response.geturl(), body


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
    return clean(html.unescape(value), 30000)


def title(text):
    m = re.search(r"(?is)<title\b[^>]*>(.*?)</title>", text)
    return clean(html.unescape(re.sub(r"(?is)<[^>]+>", " ", m.group(1)))) if m else ""


def token_hits(text):
    low = text.lower()
    return tuple(token for token in TOKENS if token.lower() in low)


def snippets(text, hits, radius=260):
    low = text.lower()
    out = []
    seen = set()
    for token in hits:
        start = 0
        token_low = token.lower()
        while True:
            idx = low.find(token_low, start)
            if idx < 0:
                break
            a = max(0, idx - radius)
            b = min(len(text), idx + len(token) + radius)
            fragment = clean(text[a:b], 900)
            key = fragment[:300]
            if key and key not in seen:
                seen.add(key)
                out.append((token, fragment))
            start = idx + max(1, len(token))
            if len(out) >= 12:
                return tuple(out)
    return tuple(out)


def raw_targets(text, base):
    candidates = []

    for attr in ("href", "src", "action"):
        pattern = rf"(?is)\b{attr}\s*=\s*([\"'])(.*?)\1"
        for m in re.finditer(pattern, text):
            candidates.append((attr, html.unescape(m.group(2)).strip()))

    for pattern, kind in (
        (r"(?is)\b(?:window\.)?location(?:\.href)?\s*=\s*([\"'])(.*?)\1", "js-nav"),
        (r"(?is)\bwindow\.open\s*\(\s*([\"'])(.*?)\1", "js-open"),
    ):
        for m in re.finditer(pattern, text):
            candidates.append((kind, html.unescape(m.group(2)).strip()))

    for m in re.finditer(r"(?is)<meta\b[^>]*http-equiv\s*=\s*([\"'])refresh\1[^>]*content\s*=\s*([\"'])(.*?)\2", text):
        content = html.unescape(m.group(3))
        u = re.search(r"(?is)\burl\s*=\s*([^;]+)", content)
        if u:
            candidates.append(("meta-refresh", u.group(1).strip(" \"'")))

    out = []
    seen = set()
    for kind, raw in candidates:
        if not raw:
            continue
        low = raw.lower()
        if low.startswith(("javascript:", "mailto:", "tel:", "#", "data:")):
            continue
        absolute = urllib.parse.urljoin(base, raw)
        if absolute in seen:
            continue
        seen.add(absolute)
        out.append((kind, absolute))
    return tuple(out)


def score_target(url):
    low = urllib.parse.unquote_plus(url).lower()
    return sum(1 for hint in TARGET_HINTS if hint in low)


def same_domain(url):
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host in {"yegame.com", "www.yegame.com"}


def main():
    print("StoneAge historical Yegame exact-page replay — R1")
    print("SOURCE_CHAIN|JHPOP root 20001204160300 -> http://www.yegame.com")
    print("SCOPE|7 exact archived HTML captures|navigation/text only|no linked software payload")
    errors = []
    all_targets = {}

    for label, timestamp, original in CAPTURES:
        replay = f"https://web.archive.org/web/{timestamp}id_/{original}"
        try:
            status, final, body = fetch(replay)
            encoding, text = decode(body)
            visible = visible_text(text)
            hits = token_hits(visible)
            targets = raw_targets(text, original)
            print(
                "PAGE|label={}|timestamp={}|status={}|bytes={}|sha256={}|encoding={}|title={}|token_hits={}|targets={}|final={}".format(
                    clean(label), clean(timestamp), status, len(body),
                    hashlib.sha256(body).hexdigest(), clean(encoding), clean(title(text)),
                    clean(",".join(hits), 2000), len(targets), clean(final)
                )
            )
            for token, fragment in snippets(visible, hits):
                print(
                    "SNIPPET|label={}|token={}|text={}".format(
                        clean(label), clean(token), clean(fragment, 1000)
                    )
                )
            for kind, target in targets:
                score = score_target(target)
                on_domain = int(same_domain(target))
                key = (target, kind)
                all_targets.setdefault(key, set()).add(label)
                print(
                    "TARGET|label={}|kind={}|on_yegame={}|score={}|url={}".format(
                        clean(label), clean(kind), on_domain, score, clean(target)
                    )
                )
        except Exception as exc:
            errors.append((label, type(exc).__name__, str(exc)))
            print(
                "ERROR|label={}|kind={}|message={}".format(
                    clean(label), clean(type(exc).__name__), clean(str(exc))
                )
            )

    ranked = sorted(
        all_targets.items(),
        key=lambda item: (-score_target(item[0][0]), item[0][0], item[0][1]),
    )
    for (target, kind), labels in ranked:
        print(
            "RANKED_TARGET|score={}|on_yegame={}|kind={}|from={}|url={}".format(
                score_target(target), int(same_domain(target)), clean(kind),
                clean(",".join(sorted(labels))), clean(target)
            )
        )

    print(f"COUNT|unique_targets|{len(all_targets)}")
    print(f"COUNT|errors|{len(errors)}")
    if errors:
        print("RESOLUTION|PARTIAL_YEGAME_REPLAY|retry failed exact captures only")
    elif any(score_target(target) >= 2 for target, _kind in all_targets):
        print("RESOLUTION|YEGAME_TARGETS_FOUND|probe only highest-scoring historical targets next")
    elif all_targets:
        print("RESOLUTION|YEGAME_NAVIGATION_FOUND_NO_STRONG_CLIENT_TOKEN|follow source-grounded navigation only")
    else:
        print("RESOLUTION|YEGAME_CAPTURE_SURFACE_BOUNDED|no navigation target recovered from tested exact pages")
    print("EVIDENCE_BOUNDARY|Archived page text/navigation is historical web evidence only; no linked executable/archive is fetched or authenticated.")


if __name__ == "__main__":
    main()
