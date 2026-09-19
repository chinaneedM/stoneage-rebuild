#!/usr/bin/env python3
"""Resolve GameTime GW_IDX=9 and nearby StoneAge records from archived online-list pages.

Reads archived HTML only. No client payload bytes are requested.
"""

from __future__ import annotations

import concurrent.futures
import re
import urllib.parse

from tools.stoneage_gametime_stoneage_record_probe import clean, decode, fetch_replay

ANCHORS=[
    (
        "stoneage-search-20010701",
        "20010701053412",
        "http://www.gametime.co.kr/data/data_list.asp?"
        "search_word=%bd%ba%c5%e6%bf%a1%c0%cc%c1%f6&category=online",
    ),
    (
        "online-page2-20010809",
        "20010809014939",
        "http://www.gametime.co.kr/data/data_list.asp?search_word=&category=online&page=2",
    ),
    (
        "online-page3-20010820",
        "20010820034814",
        "http://www.gametime.co.kr/data/data_list.asp?search_word=&category=online&page=3",
    ),
    (
        "online-page4-20010907",
        "20010907233615",
        "http://www.gametime.co.kr/data/data_list.asp?search_word=&category=online&page=4",
    ),
]

DOWNLOAD_RE=re.compile(
    r"""(?is)<a\s+href=["']?download\.asp\?GW_IDX=(\d+)&GW_Name=Online["']?[^>]*>(.*?)</a>"""
)
TITLE_RE=re.compile(r"""(?is)class=["']?sfont1["']?[^>]*>\s*([^<]{1,180})\s*</td>""")
DESC_RE=re.compile(r"""(?is)<table[^>]+title\s*=\s*["']([^"']{1,1600})["']""")
TAG_RE=re.compile(r"(?is)<[^>]+>")
SPACE_RE=re.compile(r"\s+")
STONE_RE=re.compile(r"(?i)(스톤\s*에이지|스톤에이지|stone\s*age|stoneage|stone_demo\.exe|sa\.exe)")


def plain(value):
    return SPACE_RE.sub(" ",TAG_RE.sub(" ",value)).strip()


def extract_records(html):
    records=[]
    for m in DOWNLOAD_RE.finditer(html):
        idx=m.group(1)
        filename=plain(m.group(2))
        start=max(0,m.start()-2400)
        end=min(len(html),m.end()+2400)
        context=html[start:end]

        titles=TITLE_RE.findall(html[max(0,m.start()-1800):m.start()+200])
        title=plain(titles[-1]) if titles else ""

        descs=DESC_RE.findall(html[max(0,m.start()-1800):m.end()+1800])
        desc=plain(descs[-1]) if descs else ""

        records.append({
            "idx":idx,
            "filename":filename,
            "title":title,
            "description":desc,
            "stoneage":bool(STONE_RE.search(" ".join((filename,title,desc,plain(context))))),
            "context":clean(plain(context),1200),
        })
    # stable de-duplication by id+filename
    out=[]
    seen=set()
    for r in records:
        key=(r["idx"],r["filename"])
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def scan_anchor(anchor):
    label,ts,url=anchor
    status,final,body,replay=fetch_replay(ts,url)
    html=decode(body)
    records=extract_records(html)
    return {
        "label":label,
        "timestamp":ts,
        "url":url,
        "status":status,
        "replay":replay,
        "records":records,
        "has_idx9":any(r["idx"]=="9" for r in records),
        "stoneage_records":[r for r in records if r["stoneage"]],
    }


def main():
    print("StoneAge GameTime online-index record probe — R1")
    print("SCOPE|archived-html-only|no-client-payload-download")
    print(f"COUNT|anchors|{len(ANCHORS)}")

    results=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        future_map={ex.submit(scan_anchor,a):a for a in ANCHORS}
        for fut,a in future_map.items():
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append((a[0],a[2],type(exc).__name__,str(exc)))

    total=0
    idx9=[]
    stone=[]
    for result in sorted(results,key=lambda r:r["timestamp"]):
        rows=result["records"]
        total+=len(rows)
        print(
            f"ANCHOR|label={clean(result['label'])}|timestamp={result['timestamp']}|"
            f"status={result['status']}|records={len(rows)}|"
            f"has_idx9={int(result['has_idx9'])}|stoneage_records={len(result['stoneage_records'])}|"
            f"replay={clean(result['replay'])}"
        )
        for row in rows:
            if row["idx"]=="9":
                idx9.append((result,row))
            if row["stoneage"]:
                stone.append((result,row))
            if row["idx"]=="9" or row["stoneage"] or row["idx"] in {"34","76"}:
                print(
                    f"RECORD|anchor={clean(result['label'])}|timestamp={result['timestamp']}|"
                    f"gw_idx={row['idx']}|filename={clean(row['filename'])}|"
                    f"title={clean(row['title'])}|stoneage={int(row['stoneage'])}|"
                    f"description={clean(row['description'],1500)}"
                )
                print(
                    f"CONTEXT|anchor={clean(result['label'])}|gw_idx={row['idx']}|"
                    f"text={clean(row['context'],1200)}"
                )

    print(f"COUNT|anchors_replayed|{len(results)}")
    print(f"COUNT|records_parsed|{total}")
    print(f"COUNT|idx9_records|{len(idx9)}")
    print(f"COUNT|stoneage_records|{len(stone)}")
    print(f"COUNT|errors|{len(errors)}")
    for label,url,kind,msg in errors:
        print(
            f"ERROR|label={clean(label)}|url={clean(url)}|kind={clean(kind)}|message={clean(msg)}"
        )


if __name__=="__main__":
    main()
