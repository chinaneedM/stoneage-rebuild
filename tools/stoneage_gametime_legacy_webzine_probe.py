#!/usr/bin/env python3
"""Probe GameTime's pre-data-center online download pages for StoneAge records.

Archived HTML only; no client payload bytes are requested.
"""

from __future__ import annotations

import concurrent.futures
import re
import urllib.parse

from tools.stoneage_gametime_stoneage_record_probe import clean, decode, fetch_replay

ANCHORS=[
    ("legacy-bbs-page1","20001109185200","http://www.gametime.co.kr/webzine/online/down/bbs.asp"),
    ("legacy-bbs-page2","20010107182400","http://www.gametime.co.kr/webzine/online/down/bbs.asp?name=&page=2"),
    ("legacy-bbs-page3","20010107183300","http://www.gametime.co.kr/webzine/online/down/bbs.asp?name=&page=3"),
    ("legacy-bbs-page4","20010107184000","http://www.gametime.co.kr/webzine/online/down/bbs.asp?name=&page=4"),
    (
        "legacy-stoneage-beta-content",
        "20010107184000",
        "http://www.gametime.co.kr/webzine/online/down/content.asp?name=&num=10&ref=38&page=4",
    ),
    (
        "legacy-stoneage-beta-content-online",
        "20010107184000",
        "http://www.gametime.co.kr/webzine/online/down/content.asp?name=online&num=10&ref=38&page=4",
    ),
    ("legacy-download-bare","20001109191700","http://www.gametime.co.kr/webzine/online/download.asp"),
    (
        "legacy-download-stoneage",
        "20001208213500",
        "http://www.gametime.co.kr/webzine/online/download.asp?name="
        "%BD%BA%C5%E6%BF%A1%C0%CC%C1%F6",
    ),
]
STONE=re.compile(r"(?i)(스톤\s*에이지|스톤에이지|stone\s*age|stoneage)")
LINK=re.compile(r"""(?is)<a\b[^>]*href\s*=\s*["']?([^"' >]+)[^>]*>(.*?)</a>""")
CONTENT=re.compile(r'''(?i)(content\.asp\?[^\s"'<>]+)''')
SCRIPT_LOC=re.compile(r"""(?i)(?:location(?:\.href)?\s*=|window\.open\s*\()\s*["']([^"']+)""")
TAG=re.compile(r"(?is)<[^>]+>")
SPACE=re.compile(r"\s+")


def plain(s):
    return SPACE.sub(" ",TAG.sub(" ",s)).strip()


def analyze(label,ts,url):
    status,final,body,replay=fetch_replay(ts,url)
    html=decode(body)
    text=plain(html)
    links=[]
    for href,label_text in LINK.findall(html):
        absolute=urllib.parse.urljoin(url,href.replace("&amp;","&"))
        links.append((absolute,plain(label_text)))
    script_urls=[]
    for target in SCRIPT_LOC.findall(html):
        script_urls.append(urllib.parse.urljoin(url,target.replace("&amp;","&")))
    stone_links=[x for x in links if STONE.search(" ".join(x))]
    stone_context=[]
    for m in STONE.finditer(text):
        stone_context.append(clean(text[max(0,m.start()-280):min(len(text),m.end()+500)],900))
    content_pairs=[]
    seen_content=set()
    for m in CONTENT.finditer(html):
        absolute=urllib.parse.urljoin(url,m.group(1).replace("&amp;","&"))
        if absolute in seen_content:
            continue
        seen_content.add(absolute)
        context=clean(
            plain(html[max(0,m.start()-500):min(len(html),m.end()+700)]),
            1500,
        )
        content_pairs.append((absolute,context))
    return {
        "label":label,"timestamp":ts,"url":url,"status":status,"replay":replay,
        "bytes":len(body),"text":clean(text,2500),
        "links":links,"stone_links":stone_links,"stone_context":stone_context,
        "content_pairs":content_pairs,
        "content_urls":[x[0] for x in content_pairs],
        "script_urls":sorted(set(script_urls)),
    }


def main():
    print("StoneAge GameTime legacy webzine download probe — R1")
    print("SCOPE|archived-html-only|no-client-payload-download")
    print(f"COUNT|anchors|{len(ANCHORS)}")
    results=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(analyze,*a):a for a in ANCHORS}
        for fut,a in futs.items():
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append((a[0],a[2],type(exc).__name__,str(exc)))

    for r in sorted(results,key=lambda x:x["timestamp"]):
        print(
            f"ANCHOR|label={clean(r['label'])}|timestamp={r['timestamp']}|status={r['status']}|"
            f"bytes={r['bytes']}|links={len(r['links'])}|stone_links={len(r['stone_links'])}|"
            f"content_urls={len(r['content_urls'])}|script_urls={len(r['script_urls'])}|"
            f"replay={clean(r['replay'])}"
        )
        print(f"TEXT|anchor={clean(r['label'])}|text={r['text']}")
        for value in r["stone_context"]:
            print(f"STONE_CONTEXT|anchor={clean(r['label'])}|text={value}")
        for href,label_text in r["stone_links"]:
            print(f"STONE_LINK|anchor={clean(r['label'])}|href={clean(href)}|label={clean(label_text,500)}")
        for href,context in r["content_pairs"]:
            print(
                f"CONTENT_LINK|anchor={clean(r['label'])}|href={clean(href)}|"
                f"context={clean(context,1500)}"
            )
        for href in r["script_urls"]:
            print(f"SCRIPT_LINK|anchor={clean(r['label'])}|href={clean(href)}")

    print(f"COUNT|anchors_replayed|{len(results)}")
    print(f"COUNT|errors|{len(errors)}")
    for label,url,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|url={clean(url)}|kind={clean(kind)}|message={clean(msg)}")


if __name__=="__main__":
    main()
