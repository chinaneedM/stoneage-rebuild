#!/usr/bin/env python3
"""Replay launch-window Waei StoneAge2 HTML pages to recover client-download topology.

This probe narrows the official Beijing-Waei StoneAge2 archive surface around
the 2001-11-01/02 2.0 launch and prioritizes news/bulletin pages over unrelated
download-heavy subtrees such as QQ skins. It extracts routing metadata only;
binary payloads are never downloaded.
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
PREFIX = "http://www.waei.com.cn/ZHUANQU/stoneage2/"
FROM = "20011024"
TO = "20011112"
TARGET_TS = "20011102"
MAX_PAGES = 40
MAX_CHILDREN = 12

PATH_HINTS = (
    "stnews", "stbulletin", "news", "bulletin", "notice", "announce",
    "index", "default", "main", "begin", "start", "download", "client",
    "upgrade", "update",
)
NOISE_HINTS = (
    "/qqskin/", "/service/", "/storyexp/", "/stpic/", "/wallpaper/",
    "/screen/", "/poster/", "/pet/", "/strategy/",
)
STONE_TOKENS = (
    "石器时代2.0", "石器时代 2.0", "家族开拓史", "stoneage2.0",
    "stoneage 2.0", "老手削暴包", "新手报到包",
)
DOWNLOAD_TOKENS = (
    "客户端下载", "客户端程序", "完整升级版", "升级版", "下载",
    "download", "client", "setup", "安装",
)
CHILD_TOKENS = (
    "石器时代2.0", "家族开拓史", "客户端", "完整升级版", "升级",
    "下载", "老手", "新手", "download", "client", "upgrade", "setup",
)
BINARY_EXTS = (".exe", ".zip", ".cab", ".rar")


def clean(v, n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]


def fetch(url, timeout=18, max_bytes=1024 * 1024):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,text/plain,application/json,*/*;q=0.2",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read(max_bytes + 1)
        if len(b) > max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r, "status", r.getcode())), r.geturl(), dict(r.headers.items()), b


def cdx_url():
    p = [
        ("url", PREFIX),
        ("matchType", "prefix"),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length"),
        ("from", FROM),
        ("to", TO),
        ("collapse", "urlkey"),
        ("limit", "20000"),
        ("filter", "statuscode:200"),
    ]
    return CDX + "?" + urllib.parse.urlencode(p)


def rows(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, r)) for r in obj[1:] if isinstance(r, list))


def decode(b):
    for enc in ("gb18030", "big5", "utf-8", "latin1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("latin1", "replace")


def is_html_candidate(r):
    mt = str(r.get("mimetype") or "").lower()
    u = str(r.get("original") or "")
    p = urllib.parse.urlsplit(u).path.lower()
    return "html" in mt or p.endswith((".asp", ".htm", ".html", ".shtml")) or p.endswith("/")


def score_page(r):
    url = str(r.get("original") or "")
    ts = str(r.get("timestamp") or "")
    low = urllib.parse.unquote_plus(url).lower()
    p = urllib.parse.urlsplit(low).path
    root = urllib.parse.urlsplit(PREFIX.lower()).path.rstrip("/") + "/"
    rel = p[len(root):] if p.startswith(root) else p
    depth = rel.count("/")
    leaf = rel.rsplit("/", 1)[-1]

    score = max(0, 8 - depth * 2)
    if any(h in rel for h in PATH_HINTS):
        score += 8
    if any(n in low for n in NOISE_HINTS):
        score -= 30
    if leaf in ("", "index.asp", "index.htm", "index.html", "default.asp", "main.asp"):
        score += 8
    if leaf.endswith((".asp", ".htm", ".html", ".shtml")):
        score += 2

    if len(ts) >= 8 and ts[:8].isdigit():
        try:
            day = int(ts[6:8])
            month = int(ts[4:6])
            tday = int(TARGET_TS[6:8])
            tmonth = int(TARGET_TS[4:6])
            delta = abs((month * 31 + day) - (tmonth * 31 + tday))
            score += max(0, 14 - delta)
        except ValueError:
            pass
    return score


def replay_url(ts, orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def extract_links(text, base):
    out = []
    pat = re.compile(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>')
    for m in pat.finditer(text):
        href = html.unescape(m.group(1)).strip()
        anchor = re.sub(r"(?s)<[^>]+>", " ", m.group(2))
        anchor = html.unescape(re.sub(r"\s+", " ", anchor)).strip()
        if not href or href.startswith(("javascript:", "mailto:", "#")):
            continue
        out.append((urllib.parse.urljoin(base, href), anchor))
    return tuple(out)


def semantic_match(text):
    low = urllib.parse.unquote_plus(str(text or "")).lower()
    return any(t.lower() in low for t in STONE_TOKENS) and any(
        t.lower() in low for t in DOWNLOAD_TOKENS
    )


def noisy_url(url):
    low = urllib.parse.unquote_plus(str(url or "")).lower()
    return any(n in low for n in NOISE_HINTS)


def candidate_ref(href, anchor):
    if noisy_url(href):
        return False
    parsed = urllib.parse.urlsplit(href)
    low = urllib.parse.unquote_plus(href).lower()
    path = parsed.path.lower()
    text = f"{href} {anchor}"
    is_binary = path.endswith(BINARY_EXTS)
    is_ip_host = bool(re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", parsed.hostname or ""))
    exact = "stoneage2.0setup" in low
    return exact or is_ip_host or is_binary or semantic_match(text)


def child_link(href, anchor):
    if noisy_url(href):
        return False
    p = urllib.parse.urlsplit(href)
    host = (p.hostname or "").lower()
    if host not in ("www.waei.com.cn", "waei.com.cn"):
        return False
    if p.path.lower().endswith(BINARY_EXTS):
        return False
    text = urllib.parse.unquote_plus(f"{href} {anchor}").lower()
    return any(t.lower() in text for t in CHILD_TOKENS)


def page_semantics(text, orig):
    plain = html.unescape(re.sub(r"(?s)<[^>]+>", " ", text))
    plain = re.sub(r"\s+", " ", plain)
    matched_stone = [t for t in STONE_TOKENS if t.lower() in plain.lower()]
    matched_down = [t for t in DOWNLOAD_TOKENS if t.lower() in plain.lower()]
    return plain, matched_stone, matched_down, bool(matched_stone and matched_down)


def main():
    print("StoneAge Beijing-Waei 2.0 launch-window HTML topology probe — R1")
    print(
        f"SCOPE|official stoneage2 prefix|window={FROM}..{TO}|target={TARGET_TS}|"
        f"max_pages={MAX_PAGES}|max_children={MAX_CHILDREN}|HTML-only|no-payload"
    )
    errors = []
    try:
        st, final, hdrs, body = fetch(cdx_url(), max_bytes=8 * 1024 * 1024)
        rr = rows(body)
        print(
            f"CDX|status={st}|rows={len(rr)}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}"
        )
    except Exception as e:
        errors.append(("cdx", type(e).__name__, str(e)))
        rr = ()

    candidates = [r for r in rr if is_html_candidate(r) and not noisy_url(str(r.get("original") or ""))]
    candidates.sort(key=lambda r: (score_page(r), str(r.get("timestamp") or "")), reverse=True)
    selected = candidates[:MAX_PAGES]
    print(f"COUNT|html_candidates|{len(candidates)}")
    print(f"COUNT|selected_pages|{len(selected)}")

    replayed = 0
    semantic_pages = []
    route_hits = []
    child_queue = []
    seen_pages = set()

    def inspect_page(kind, index, ts, orig, score):
        nonlocal replayed
        key = (ts, orig)
        if key in seen_pages:
            return
        seen_pages.add(key)
        try:
            st, final, hdrs, b = fetch(replay_url(ts, orig), max_bytes=768 * 1024)
            replayed += 1
            txt = decode(b)
            plain, stone_hits, down_hits, sem = page_semantics(txt, orig)
            ls = extract_links(txt, orig)
            routes = [(u, a) for u, a in ls if candidate_ref(u, a)]
            children = [(u, a) for u, a in ls if child_link(u, a)]

            print(
                f"PAGE|kind={kind}|index={index}|score={score}|timestamp={ts}|status={st}|"
                f"bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|orig={clean(orig)}|"
                f"semantic={int(sem)}|links={len(ls)}|routes={len(routes)}|children={len(children)}"
            )
            if sem:
                semantic_pages.append((ts, orig))
                print(
                    f"SEMANTIC_PAGE|timestamp={ts}|orig={clean(orig)}|"
                    f"stone={clean(','.join(stone_hits),600)}|download={clean(','.join(down_hits),600)}"
                )
            for u, a in routes:
                route_hits.append((ts, orig, u, a))
                print(
                    f"ROUTE_HIT|timestamp={ts}|page={clean(orig)}|href={clean(u)}|"
                    f"anchor={clean(a,1200)}"
                )
            for u, a in children:
                child_queue.append((ts, u, a, score))
        except Exception as e:
            errors.append((f"{kind}:{index}:{orig}", type(e).__name__, str(e)))

    for i, r in enumerate(selected, 1):
        inspect_page(
            "selected",
            i,
            str(r.get("timestamp") or ""),
            str(r.get("original") or ""),
            score_page(r),
        )

    uniq_children = []
    seen_child_urls = set()
    for ts, u, a, parent_score in child_queue:
        if u in seen_child_urls:
            continue
        seen_child_urls.add(u)
        uniq_children.append((ts, u, a, parent_score))
        if len(uniq_children) >= MAX_CHILDREN:
            break

    print(f"COUNT|selected_child_links|{len(uniq_children)}")
    for i, (ts, u, a, parent_score) in enumerate(uniq_children, 1):
        inspect_page("child", i, ts, u, parent_score)

    uniq_routes = {}
    for ts, page, u, a in route_hits:
        uniq_routes[(u, a)] = (ts, page)
    host_counts = {}
    for u, a in uniq_routes:
        host = urllib.parse.urlsplit(u).hostname or ""
        host_counts[host] = host_counts.get(host, 0) + 1
    for host, count in sorted(host_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"ROUTE_HOST|host={clean(host)}|count={count}")

    exact = [
        (u, a) for (u, a) in uniq_routes
        if "stoneage2.0setup" in urllib.parse.unquote_plus(u).lower()
    ]
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|semantic_pages|{len(set(semantic_pages))}")
    print(f"COUNT|unique_route_hits|{len(uniq_routes)}")
    print(f"COUNT|exact_setup_refs|{len(exact)}")
    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if exact:
        print("RESOLUTION|EXACT_SETUP_ROUTE_FOUND|replay/classify target route before any payload inference")
    elif uniq_routes:
        print("RESOLUTION|LAUNCH_WINDOW_BINARY_ROUTES_FOUND|classify routes for 2.0 client lineage")
    elif semantic_pages:
        print("RESOLUTION|LAUNCH_WINDOW_SEMANTIC_PAGES_FOUND_NO_BINARY_ROUTE|expand only evidence-linked child routes")
    elif errors and replayed == 0:
        print("RESOLUTION|LAUNCH_WINDOW_REPLAY_INCOMPLETE|do not close official page-content route")
    else:
        print("RESOLUTION|NO_CLIENT_ROUTE_IN_BOUNDED_LAUNCH_WINDOW|reopen only from new official page/path token")
    print(
        "EVIDENCE_BOUNDARY|Archived HTML and links establish routing/distribution evidence only; "
        "no linked binary is downloaded or promoted without separate byte verification."
    )


if __name__ == "__main__":
    main()
