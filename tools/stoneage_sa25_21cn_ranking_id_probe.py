#!/usr/bin/env python3
"""Recover the native 21CN catalogue ID behind the '石器时代2.5-精…' ranking link.

Replays one already-proven StoneAge-related 21CN HTML detail page transiently and
emits only matching anchor labels/hrefs. No linked software payload is fetched.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible

UA="stoneage-rebuild-archaeology/1.0"
TIMESTAMP="20030313042912"
ORIGINAL="http://download.21cn.com:80/list.php?id=22318"
REPLAY=f"https://web.archive.org/web/{TIMESTAMP}id_/{ORIGINAL}"
ANCHOR_RE=re.compile(r"""(?is)<a\b[^>]*?href\s*=\s*["']?([^"'\s>]+)["']?[^>]*>(.*?)</a>""")
TOKENS=("石器时代2.5","石器時代2.5","精灵王","精靈王","石器时代","石器時代")


def clean(v,limit=2400):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url=REPLAY,timeout=25,max_bytes=1_500_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b


def anchors(text):
    out=[]
    for href,label_html in ANCHOR_RE.findall(text):
        label=visible(html.unescape(label_html))
        href=html.unescape(href.strip())
        if label or href:
            out.append((label,href))
    return tuple(out)


def matching_anchors(text):
    out=[]
    for label,href in anchors(text):
        low=label.lower()
        if any(t.lower() in low for t in TOKENS):
            out.append((label,href))
    return tuple(out)


def catalogue_id(href):
    try:
        p=urllib.parse.urlsplit(href)
        q=urllib.parse.parse_qs(p.query)
        vals=q.get("id") or ()
        return str(vals[0]) if vals and str(vals[0]).isdigit() else ""
    except Exception:
        return ""


def main():
    print("StoneAge 2.5 21CN ranking-link ID recovery — R1")
    print("SCOPE|single-proven-native-21cn-page|anchor-metadata-only|no-linked-payload")
    try:
        st,final,body=fetch()
        enc,text=decode(body,declared_charset(body))
        rows=matching_anchors(text)
    except Exception as exc:
        print(f"ERROR|kind={type(exc).__name__}|message={clean(exc)}")
        print("RESOLUTION|RANKING_LINK_REPLAY_FAILED")
        return
    print(
        f"PAGE|timestamp={TIMESTAMP}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
        f"encoding={clean(enc)}|matching_anchors={len(rows)}|final={clean(final)}"
    )
    for n,(label,href) in enumerate(rows,1):
        print(
            f"MATCH|order={n}|label={clean(label,1400)}|href={clean(href,2000)}|"
            f"catalogue_id={clean(catalogue_id(href))}"
        )
    exact=[r for r in rows if "2.5" in r[0] and ("精灵王" in r[0] or "精靈王" in r[0])]
    print(f"COUNT|matching_anchors|{len(rows)}")
    print(f"COUNT|exact_25_spiritking_labels|{len(exact)}")
    if exact:
        print("RESOLUTION|NATIVE_21CN_SA25_CATALOGUE_ID_FOUND|trace exact list record and downit/file topology next")
    elif rows:
        print("RESOLUTION|STONEAGE_ANCHORS_FOUND_BUT_NO_EXACT_25_LABEL|inspect labels without promoting ID")
    else:
        print("RESOLUTION|NO_STONEAGE_RANKING_ANCHOR|tested page contains no recoverable matching anchor")
    print("EVIDENCE_BOUNDARY|a ranking anchor can identify a native catalogue record ID; it does not authenticate the downloadable payload bytes.")


if __name__=="__main__":
    main()
