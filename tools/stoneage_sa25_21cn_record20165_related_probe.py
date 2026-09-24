#!/usr/bin/env python3
"""Extract StoneAge-related native 21CN catalogue links from record 20165 snapshots.

This searches related/ranking anchor labels on the proven StoneAge 2.5 updater page for
other catalogue IDs, especially a possible full-client record. HTML only; no payload.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import re
import urllib.parse
import urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible

UA="stoneage-rebuild-archaeology/1.0"
CAPTURES=(
    ("2002-02-12","20020212010502"),
    ("2002-06-13","20020613074744"),
    ("2002-08-12","20020812171832"),
    ("2002-10-03","20021003143013"),
    ("2002-12-18","20021218050518"),
)
ORIGINAL="http://download.21cn.com:80/list.php?id=20165"
ANCHOR_RE=re.compile(r"""(?is)<a\b[^>]*?href\s*=\s*["']?([^"'\s>]+)["']?[^>]*>(.*?)</a>""")
TOKENS=("石器时代","石器時代","精灵王","精靈王","stoneage","sa2.5","2.5")


def clean(v,limit=2200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(ts,timeout=20):
    url=f"https://web.archive.org/web/{ts}id_/{ORIGINAL}"
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(1_500_001)
        if len(b)>1_500_000:
            raise ValueError("page-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b


def catalogue_id(href):
    try:
        p=urllib.parse.urlsplit(html.unescape(href))
        q=urllib.parse.parse_qs(p.query)
        vals=q.get("id") or ()
        return str(vals[0]) if vals and str(vals[0]).isdigit() else ""
    except Exception:
        return ""


def anchors(text):
    out=[]
    for href,label_html in ANCHOR_RE.findall(text):
        label=visible(html.unescape(label_html))
        href=html.unescape(href.strip())
        if label or href:
            out.append((label,href,catalogue_id(href)))
    return tuple(out)


def related(text):
    out=[]; seen=set()
    for label,href,cid in anchors(text):
        low=label.lower()
        if any(token.lower() in low for token in TOKENS):
            key=(label,href,cid)
            if key not in seen:
                seen.add(key); out.append(key)
    return tuple(out)


def one(cap):
    label,ts=cap
    try:
        st,final,b=fetch(ts)
        enc,text=decode(b,declared_charset(b))
        return label,ts,st,final,b,enc,related(text),None
    except Exception as exc:
        return label,ts,None,None,None,None,(),(type(exc).__name__,str(exc))


def main():
    print("StoneAge 2.5 native 21CN record-20165 related-catalogue probe — R1")
    print("SCOPE|dated-native-html|stoneage-labelled-anchor-extraction|no-software-payload")
    errors=[]; ids={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for label,ts,st,final,b,enc,rows,error in ex.map(one,CAPTURES):
            if error:
                errors.append((label,error[0],error[1]))
                continue
            print(
                f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|"
                f"matches={len(rows)}|final={clean(final)}"
            )
            for n,(text_label,href,cid) in enumerate(rows,1):
                print(
                    f"MATCH|page={label}|order={n}|label={clean(text_label,1600)}|"
                    f"href={clean(href,2200)}|catalogue_id={clean(cid)}"
                )
                if cid:
                    ids.setdefault(cid,set()).add(text_label)
    for cid,labels in sorted(ids.items(),key=lambda kv:int(kv[0])):
        print(f"CATALOGUE_ID|id={cid}|labels={clean(' || '.join(sorted(labels)),3000)}")
    for label,kind,msg in errors:
        print(f"ERROR|page={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|unique_catalogue_ids|{len(ids)}")
    print(f"COUNT|errors|{len(errors)}")
    external=[cid for cid in ids if cid!="20165"]
    print(f"COUNT|external_stoneage_ids|{len(external)}")
    if external:
        print("RESOLUTION|RELATED_STONEAGE_CATALOGUE_IDS_FOUND|trace each ID for package class,size,date and download topology")
    elif errors:
        print("RESOLUTION|PARTIAL_RELATED_LINK_FAILURE|retry failed captures only")
    else:
        print("RESOLUTION|NO_OTHER_STONEAGE_CATALOGUE_ID|record-20165 related/ranking surface bounded")
    print("EVIDENCE_BOUNDARY|related catalogue links are discovery tokens only until their own native pages are replayed.")


if __name__=="__main__":
    main()
