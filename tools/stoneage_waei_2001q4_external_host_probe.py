#!/usr/bin/env python3
"""Census evidence-linked Waei external hosts around the mainland 2.0 launch.

Two official StoneAge launch pages link the Waei games/product roots, and later
archive evidence proves games.waei.com.cn carried executable downloads under
/accessories/download/. This probe inventories only those two hosts in the
2001-10-24..11-12 launch window and emits URL metadata with client/download/
StoneAge/binary semantics. No payload is downloaded.
"""
from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
FROM = "20011024"
TO = "20011112"
HOSTS = (
    ("games", "http://games.waei.com.cn/"),
    ("product", "http://product.waei.com.cn/"),
)
TOKENS = (
    "stoneage", "stone_age", "stone-age", "stone2", "sa2", "2.0",
    "client", "setup", "install", "download", "upgrade", "update", "patch",
    "accessories/download",
)
BINARY_EXTS = (".exe", ".zip", ".cab", ".rar")


def clean(v, n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]


def fetch(url, timeout=35, max_bytes=8 * 1024 * 1024):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/json,text/plain,*/*;q=0.5", "Accept-Encoding": "identity"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read(max_bytes + 1)
        if len(b) > max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r, "status", r.getcode())), r.geturl(), b


def cdx_url(prefix):
    p = [
        ("url", prefix),
        ("matchType", "prefix"),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from", FROM),
        ("to", TO),
        ("collapse", "urlkey"),
        ("limit", "20000"),
    ]
    return CDX + "?" + urllib.parse.urlencode(p)


def rows(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, row)) for row in obj[1:] if isinstance(row, list))


def binary_url(url):
    path = urllib.parse.urlsplit(urllib.parse.unquote_plus(str(url or ""))).path.lower()
    return path.endswith(BINARY_EXTS)


def targetish(url):
    low = urllib.parse.unquote_plus(str(url or "")).lower()
    return binary_url(url) or any(t in low for t in TOKENS)


def score(url):
    low = urllib.parse.unquote_plus(str(url or "")).lower()
    s = 0
    if binary_url(url):
        s += 5
    if "stoneage" in low or "stone2" in low or "sa2" in low:
        s += 7
    if "client" in low or "setup" in low or "install" in low:
        s += 5
    if "download" in low or "upgrade" in low or "update" in low or "patch" in low:
        s += 3
    if "accessories/download" in low:
        s += 3
    if "qqskin" in low:
        s -= 5
    return s


def main():
    print("StoneAge Waei evidence-linked external-host topology census — R1")
    print(f"SCOPE|games+product Waei roots|window={FROM}..{TO}|CDX URL metadata only|no-payload")
    errors = []
    hits = []
    completed = 0
    for label, prefix in HOSTS:
        try:
            st, final, body = fetch(cdx_url(prefix))
            rr = rows(body)
            completed += 1
            print(
                f"CDX|label={label}|prefix={prefix}|status={st}|rows={len(rr)}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}"
            )
            for r in rr:
                u = str(r.get("original") or "")
                if targetish(u):
                    hits.append((score(u), label, u, r))
        except Exception as e:
            errors.append((label, type(e).__name__, str(e)))
    hits.sort(key=lambda x: (-x[0], x[1], x[2]))
    for s, label, u, r in hits:
        print(
            f"TOPOLOGY_HIT|score={s}|label={label}|timestamp={clean(r.get('timestamp'))}|"
            f"original={clean(u)}|statuscode={clean(r.get('statuscode'))}|"
            f"mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|"
            f"length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}"
        )
    strong = [h for h in hits if h[0] >= 8]
    binary = [h for h in hits if binary_url(h[2])]
    exact = [h for h in hits if "stoneage2.0setup" in urllib.parse.unquote_plus(h[2]).lower()]
    print(f"COUNT|hosts|{len(HOSTS)}")
    print(f"COUNT|completed_hosts|{completed}")
    print(f"COUNT|topology_hits|{len(hits)}")
    print(f"COUNT|strong_hits|{len(strong)}")
    print(f"COUNT|binary_hits|{len(binary)}")
    print(f"COUNT|exact_setup_hits|{len(exact)}")
    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:
        print("RESOLUTION|EXACT_SETUP_PATH_FOUND_ON_EXTERNAL_WAEI_HOST|replay/classify route before payload recovery")
    elif strong:
        print("RESOLUTION|STRONG_EXTERNAL_HOST_TOPOLOGY_FOUND|replay only strong evidence-linked route(s)")
    elif hits:
        print("RESOLUTION|WEAK_EXTERNAL_HOST_TOPOLOGY_ONLY|do not promote without page/content corroboration")
    elif errors:
        print("RESOLUTION|EXTERNAL_HOST_CENSUS_INCOMPLETE|retry only failed host query")
    else:
        print("RESOLUTION|NO_LAUNCH_WINDOW_DOWNLOAD_TOPOLOGY_ON_TWO_EXTERNAL_HOSTS|bound this evidence-linked branch")
    print("EVIDENCE_BOUNDARY|CDX URL rows are routing metadata only and do not establish client identity, cleanliness or completeness.")


if __name__ == "__main__":
    main()
