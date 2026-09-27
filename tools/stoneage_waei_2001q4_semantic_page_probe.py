#!/usr/bin/env python3
"""Inspect two evidence-linked Waei 2.0 launch pages for hidden download routing.

The broad launch-window replay found two official pages with StoneAge 2.0 and
download/install semantics but no ordinary binary href. This bounded follow-up
replays only those exact captures and inspects short token-context snippets plus
routing-bearing HTML attributes/JavaScript. No binary payload is downloaded.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
PAGES = (
    (
        "news-17",
        "20011027113916",
        "http://www.waei.com.cn:80/ZHUANQU/stoneage2/stnews/st_news_nr.asp?id=17",
    ),
    (
        "bulletin-311",
        "20011109212146",
        "http://www.waei.com.cn:80/ZHUANQU/stoneage2/stbulletin/st_bulletin_nr.asp?id=311",
    ),
)
TOKENS = (
    "石器时代2.0", "家族开拓史", "老手削暴包", "新手报到包",
    "完整升级版", "升级版", "客户端", "下载", "安装",
    "stoneage2.0setup", "setup.exe",
)
ROUTE_RE = re.compile(
    r"""(?is)(?:href|src|action)\s*=\s*["']([^"']+)["']"""
    r"""|(?:window\.open|location(?:\.href)?\s*=|window\.location\s*=)\s*"""
    r"""\(?\s*["']([^"']+)["']"""
)
URL_RE = re.compile(r"""(?i)https?://[^\s"'<>]+""")
TITLE_RE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")


def clean(v, n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]


def fetch(url, timeout=25, max_bytes=1024 * 1024):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,text/plain,*/*;q=0.2",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read(max_bytes + 1)
        if len(b) > max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r, "status", r.getcode())), r.geturl(), b


def replay_url(ts, orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode(b):
    for enc in ("gb18030", "big5", "utf-8", "latin1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("latin1", "replace")


def strip_html(text):
    t = re.sub(r"(?is)<script\b.*?</script>", " ", text)
    t = re.sub(r"(?is)<style\b.*?</style>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def title(text):
    m = TITLE_RE.search(text)
    if not m:
        return ""
    return clean(strip_html(m.group(1)), 500)


def contexts(text, radius=180):
    plain = strip_html(text)
    low = plain.lower()
    out = []
    seen = set()
    for tok in TOKENS:
        pos = 0
        t = tok.lower()
        while True:
            i = low.find(t, pos)
            if i < 0:
                break
            a = max(0, i - radius)
            b = min(len(plain), i + len(tok) + radius)
            snip = clean(plain[a:b], 500)
            if snip not in seen:
                seen.add(snip)
                out.append((tok, snip))
            pos = i + max(1, len(t))
            if len(out) >= 18:
                return tuple(out)
    return tuple(out)


def route_refs(text, base):
    out = []
    for m in ROUTE_RE.finditer(text):
        raw = (m.group(1) or m.group(2) or "").strip()
        if not raw or raw.startswith(("javascript:", "mailto:", "#")):
            continue
        out.append(urllib.parse.urljoin(base, html.unescape(raw)))
    for m in URL_RE.finditer(text):
        out.append(html.unescape(m.group(0)))
    dedup = []
    seen = set()
    for u in out:
        u = u.rstrip("),.;")
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return tuple(dedup)


def route_score(url):
    low = urllib.parse.unquote_plus(url).lower()
    score = 0
    for token in ("stone", "client", "download", "setup", "upgrade", ".exe", ".zip", ".cab", ".rar"):
        if token in low:
            score += 2
    host = urllib.parse.urlsplit(url).hostname or ""
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
        score += 4
    if host and host not in ("www.waei.com.cn", "waei.com.cn"):
        score += 1
    return score


def main():
    print("StoneAge Waei 2.0 semantic launch-page routing probe — R1")
    print("SCOPE|2 exact evidence-linked official captures|context+href/src/action+JS routing|HTML-only|no-payload")
    errors = []
    all_refs = {}
    for label, ts, orig in PAGES:
        try:
            st, final, body = fetch(replay_url(ts, orig))
            text = decode(body)
            refs = route_refs(text, orig)
            ctx = contexts(text)
            print(
                f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|orig={clean(orig)}|title={title(text)}|"
                f"contexts={len(ctx)}|route_refs={len(refs)}"
            )
            for tok, snip in ctx:
                print(f"CONTEXT|label={label}|token={clean(tok,100)}|text={clean(snip,500)}")
            ranked = sorted(((route_score(u), u) for u in refs), key=lambda x: (-x[0], x[1]))
            for score, u in ranked:
                if score <= 0:
                    continue
                all_refs[u] = max(all_refs.get(u, 0), score)
                print(f"ROUTE_REF|label={label}|score={score}|url={clean(u)}")
        except Exception as e:
            errors.append((label, type(e).__name__, str(e)))
    exact = [u for u in all_refs if "stoneage2.0setup" in urllib.parse.unquote_plus(u).lower()]
    binaries = [
        u for u in all_refs
        if urllib.parse.urlsplit(u).path.lower().endswith((".exe", ".zip", ".cab", ".rar"))
    ]
    external = [
        u for u in all_refs
        if (urllib.parse.urlsplit(u).hostname or "").lower() not in ("www.waei.com.cn", "waei.com.cn")
    ]
    print(f"COUNT|unique_scored_route_refs|{len(all_refs)}")
    print(f"COUNT|exact_setup_refs|{len(exact)}")
    print(f"COUNT|binary_refs|{len(binaries)}")
    print(f"COUNT|external_refs|{len(external)}")
    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:
        print("RESOLUTION|EXACT_SETUP_ROUTE_FOUND_IN_SEMANTIC_PAGE|classify/replay route before payload recovery")
    elif binaries:
        print("RESOLUTION|BINARY_ROUTE_FOUND_IN_SEMANTIC_PAGE|classify binary route against 2.0 client lineage")
    elif external:
        print("RESOLUTION|EXTERNAL_ROUTE_FOUND_IN_SEMANTIC_PAGE|expand only scored external routing target")
    elif errors:
        print("RESOLUTION|SEMANTIC_PAGE_ROUTING_INCOMPLETE|retry only failed exact capture(s)")
    else:
        print("RESOLUTION|NO_HIDDEN_DOWNLOAD_ROUTE_IN_TWO_SEMANTIC_PAGES|official direct-link path remains unresolved")
    print("EVIDENCE_BOUNDARY|Short context snippets and routing attributes are discovery evidence only; no linked binary is downloaded or promoted without byte verification.")


if __name__ == "__main__":
    main()
