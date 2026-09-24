#!/usr/bin/env python3
"""Probe the archived Beijing Waei StoneAge section for 2.5 download links.

Contemporaneous 2001 evidence identifies the official StoneAge section as
http://www.waei.com.cn/zhuanqu/stoneage/. Contemporary 2002 Sina/17173
records say the 2.5 full client/upgrade and 8.25 MB delta were downloadable
from Beijing Waei. This probe searches only the Jan-Mar 2002 Wayback surface
for that grounded prefix, replays bounded HTML candidates, and extracts
download-link evidence. No binary payload is downloaded.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://www.waei.com.cn/zhuanqu/stoneage/"
DATE_FROM="20020101"
DATE_TO="20020315"
MAX_REPLAYS=300

TEXT_TERMS=(
    "石器时代2.5","石器2.5","精灵王传说","完整升级版","升级程序",
    "575兆","580兆","8.25兆","575mb","580mb","8.25mb",
)
URL_HINTS=(
    "down","download","update","upgrade","patch","2.5","25","sa25","stoneage",
)
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".001",".002",".vcd",".iso")

def clean(value,limit=2400):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch_bytes(url,timeout=35):
    req=urllib.request.Request(
        url,
        headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain;q=0.9,*/*;q=0.8"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),body

def cdx_url():
    params=[
        ("url",PREFIX),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from",DATE_FROM),("to",DATE_TO),("filter","statuscode:200"),
        ("collapse","urlkey"),("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse_cdx(body):
    data=json.loads(body.decode("utf-8"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))

def is_html_row(row):
    mime=str(row.get("mimetype") or "").lower()
    original=str(row.get("original") or "").lower()
    return (
        "html" in mime
        or original.endswith(("/",".htm",".html",".shtml",".asp",".aspx"))
        or "?" in original
    )

def url_score(original):
    low=urllib.parse.unquote_plus(str(original or "")).lower()
    score=sum(1 for hint in URL_HINTS if hint in low)
    if low.rstrip("/")==PREFIX.lower().rstrip("/"):
        score+=4
    if any(token in low for token in ("index","default","main","news","download","down")):
        score+=2
    return score

def select_replay_rows(rows):
    html_rows=[row for row in rows if is_html_row(row)]
    ranked=sorted(
        html_rows,
        key=lambda row:(-url_score(row.get("original")),str(row.get("original") or "")),
    )
    return tuple(ranked[:MAX_REPLAYS])

def replay_url(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"

def decode_html(body):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try:
            return body.decode(enc)
        except Exception:
            pass
    return body.decode("utf-8","replace")

def extract_evidence(body):
    text=decode_html(body)
    low=text.lower()
    terms=tuple(term for term in TEXT_TERMS if term.lower() in low)
    hrefs=[]
    for raw in re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text):
        value=html.unescape(raw).strip()
        decoded=urllib.parse.unquote_plus(value).lower()
        if (
            any(term.lower() in decoded for term in ("2.5","sa25","stoneage","精灵王"))
            or any(ext in decoded for ext in PAYLOAD_EXTS)
            or any(hint in decoded for hint in ("download","down","update","upgrade","patch"))
        ):
            hrefs.append(value)
    return terms,tuple(dict.fromkeys(hrefs))

def replay_one(row):
    url=replay_url(row)
    status,final,body=fetch_bytes(url,timeout=30)
    terms,hrefs=extract_evidence(body)
    return row,status,final,body,terms,hrefs

def main():
    print("StoneAge Beijing-Waei 2.5 official download-page probe — R1")
    print("SCOPE|grounded-official-stoneage-prefix|2002-01-01..2002-03-15|Wayback-CDX+bounded-HTML-replay|no-binary-payload")
    print(f"TARGET|prefix={PREFIX}|from={DATE_FROM}|to={DATE_TO}|max_replays={MAX_REPLAYS}")

    errors=[]
    rows=()
    try:
        url=cdx_url()
        status,final,body=fetch_bytes(url,timeout=45)
        rows=parse_cdx(body)
        print(
            f"CDX|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"rows={len(rows)}|html_rows={sum(is_html_row(row) for row in rows)}|final={clean(final)}"
        )
    except Exception as exc:
        errors.append(("cdx",type(exc).__name__,str(exc)))

    replay_rows=select_replay_rows(rows)
    url_hints=[row for row in rows if url_score(row.get("original"))>0]
    for row in url_hints[:300]:
        print(
            f"URL_HINT|score={url_score(row.get('original'))}|timestamp={clean(row.get('timestamp'))}|"
            f"original={clean(row.get('original'))}|mimetype={clean(row.get('mimetype'))}|"
            f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
        )

    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures={executor.submit(replay_one,row):row for row in replay_rows}
        for future in concurrent.futures.as_completed(futures):
            row=futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                errors.append((f"replay:{row.get('timestamp')}:{row.get('original')}",type(exc).__name__,str(exc)))

    evidence_pages=0
    unique_hrefs={}
    for row,status,final,body,terms,hrefs in sorted(
        results,key=lambda x:(str(x[0].get("timestamp") or ""),str(x[0].get("original") or ""))
    ):
        if not terms and not hrefs:
            continue
        evidence_pages+=1
        print(
            f"PAGE_EVIDENCE|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
            f"status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"terms={clean(','.join(terms))}|hrefs={len(hrefs)}|final={clean(final)}"
        )
        for href in hrefs:
            absolute=urllib.parse.urljoin(str(row.get("original") or PREFIX),href)
            key=absolute
            unique_hrefs[key]=(str(row.get("timestamp") or ""),str(row.get("original") or ""))
            print(
                f"DOWNLOAD_HREF|timestamp={clean(row.get('timestamp'))}|source={clean(row.get('original'))}|"
                f"href={clean(href)}|absolute={clean(absolute)}"
            )

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|cdx_rows|{len(rows)}")
    print(f"COUNT|url_hint_rows|{len(url_hints)}")
    print(f"COUNT|replay_attempts|{len(replay_rows)}")
    print(f"COUNT|replay_successes|{len(results)}")
    print(f"COUNT|evidence_pages|{evidence_pages}")
    print(f"COUNT|unique_candidate_hrefs|{len(unique_hrefs)}")
    print(f"COUNT|errors|{len(errors)}")
    if unique_hrefs:
        print("RESOLUTION|OFFICIAL_25_DOWNLOAD_HREF_CANDIDATES_FOUND|classify exact URLs and recover only provenance-safe candidates transiently")
    elif evidence_pages:
        print("RESOLUTION|OFFICIAL_25_PAGE_EVIDENCE_NO_HREF|page text survived but no candidate download href was extracted")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|official 2002 Waei page surface incomplete")
    else:
        print("RESOLUTION|NO_25_PAGE_HIT|bounded official Waei StoneAge archive surface contains no 2.5 download evidence")

if __name__=="__main__":
    main()
