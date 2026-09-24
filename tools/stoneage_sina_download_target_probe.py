#!/usr/bin/env python3
"""Recover exact historical StoneAge download targets from Sina's 2003 hub.

The page is a contemporaneous media download index. This probe extracts hrefs
near three high-value labels:
- 7.0 installed package explicitly described as including fully-open maps;
- 6.0 "real fully-open MAP" download;
- StoneAge 1.82 client installer.

Only page HTML and a bounded 4 KiB prefix of candidate targets are requested.
No large client/map payload is retained or committed.
"""

from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

PAGE="https://games.sina.com.cn/zhqu/sta/download.shtml"
UA="stoneage-rebuild-archaeology/1.0"
MAX_PREFIX=4096

TARGETS=(
    ("70-installed-full-map","已安装含全开地图含注册表自解压文件"),
    ("60-full-map","真正全开MAP地图"),
    ("182-client","石器时代1.82"),
)


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch_page(url=PAGE,timeout=25):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),dict(response.headers),body


def decode_html(body,headers=None):
    header_ct=(headers or {}).get("Content-Type","")
    candidates=[]
    m=re.search(r"charset\s*=\s*([\w.-]+)",header_ct,re.I)
    if m:
        candidates.append(m.group(1))
    head=body[:8192].decode("ascii","ignore")
    m=re.search(r"charset\s*=\s*[\"']?([\w.-]+)",head,re.I)
    if m:
        candidates.append(m.group(1))
    candidates.extend(["gb18030","utf-8"])
    for encoding in candidates:
        try:
            return body.decode(encoding),encoding
        except (LookupError,UnicodeDecodeError):
            continue
    return body.decode("gb18030","replace"),"gb18030-replace"


HREF_RE=re.compile(r"<a\b[^>]*?href\s*=\s*([\"'])(.*?)\1",re.I|re.S)


def hrefs_near(text,label,window=1800):
    start=0
    rows=[]
    seen=set()
    while True:
        pos=text.find(label,start)
        if pos<0:
            break
        lo=max(0,pos-window)
        hi=min(len(text),pos+len(label)+window)
        chunk=text[lo:hi]
        for match in HREF_RE.finditer(chunk):
            href=html.unescape(match.group(2).strip())
            absolute=urllib.parse.urljoin(PAGE,href)
            key=(pos,absolute)
            if key not in seen:
                seen.add(key)
                rows.append((pos,absolute,match.start()+lo-pos))
        start=pos+len(label)
    return rows


def nearest_hrefs(text,label,limit=8):
    rows=hrefs_near(text,label)
    rows.sort(key=lambda row:(abs(row[2]),row[2],row[1]))
    return rows[:limit]


def probe_prefix(url,timeout=15):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Range":f"bytes=0-{MAX_PREFIX-1}","Accept":"*/*"},
    )
    try:
        with urllib.request.urlopen(req,timeout=timeout) as response:
            prefix=response.read(MAX_PREFIX)
            headers=dict(response.headers)
            return {
                "status":int(getattr(response,"status",response.getcode())),
                "final":response.geturl(),
                "content_type":headers.get("Content-Type",""),
                "content_length":headers.get("Content-Length",""),
                "content_range":headers.get("Content-Range",""),
                "prefix":prefix,
                "error":"",
            }
    except Exception as exc:
        return {
            "status":0,"final":url,"content_type":"","content_length":"",
            "content_range":"","prefix":b"",
            "error":f"{type(exc).__name__}:{exc}",
        }


def main():
    print("StoneAge Sina historical download-target probe — R1")
    print("SCOPE|2003-media-hub-link-recovery+bounded-target-prefix|no-large-payload-retained")

    try:
        status,final,headers,body=fetch_page()
    except Exception as exc:
        print(f"ERROR|phase=page|kind={type(exc).__name__}|message={clean(exc)}")
        print("RESOLUTION|INCONCLUSIVE|Sina page unavailable")
        return

    text,encoding=decode_html(body,headers)
    print(
        f"PAGE|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
        f"encoding={clean(encoding)}|final={clean(final)}"
    )

    all_urls={}
    resolved=0
    for label_key,label_text in TARGETS:
        occurrence_count=text.count(label_text)
        rows=nearest_hrefs(text,label_text)
        print(
            f"ANCHOR|label={label_key}|text_occurrences={occurrence_count}|near_hrefs={len(rows)}"
        )
        for order,(pos,url,delta) in enumerate(rows,1):
            all_urls.setdefault(url,set()).add(label_key)
            print(
                f"NEAR_HREF|label={label_key}|order={order}|delta_chars={delta}|url={clean(url)}"
            )
        if rows:
            resolved+=1

    # Probe only unique HTTP(S) targets and never follow file bodies beyond MAX_PREFIX.
    for url,labels in sorted(all_urls.items()):
        parsed=urllib.parse.urlparse(url)
        if parsed.scheme not in {"http","https"}:
            print(f"TARGET_SKIP|labels={','.join(sorted(labels))}|url={clean(url)}|reason=non-http")
            continue
        result=probe_prefix(url)
        print(
            f"TARGET|labels={','.join(sorted(labels))}|status={result['status']}|"
            f"prefix_bytes={len(result['prefix'])}|prefix_sha256={hashlib.sha256(result['prefix']).hexdigest() if result['prefix'] else ''}|"
            f"content_type={clean(result['content_type'])}|content_length={clean(result['content_length'])}|"
            f"content_range={clean(result['content_range'])}|final={clean(result['final'])}|"
            f"error={clean(result['error'])}"
        )

    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|labels_with_near_hrefs|{resolved}")
    print(f"COUNT|unique_near_urls|{len(all_urls)}")
    if resolved:
        print("RESOLUTION|SINA_DOWNLOAD_TARGETS_DERIVED|classify exact hrefs before any payload recovery")
    else:
        print("RESOLUTION|INCONCLUSIVE|target labels found without recoverable nearby hrefs")


if __name__=="__main__":
    main()
