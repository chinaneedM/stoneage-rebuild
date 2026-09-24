#!/usr/bin/env python3
"""Search archived native 21CN software-detail pages for StoneAge 2.5 records.

The historical IP host is independently identified as 21CN download infrastructure.
This probe enumerates archived HTTP-200 list.php?id=... records via CDX, replays those
small HTML detail pages, and emits only metadata/context for StoneAge-related matches.
It does not download any linked software/game payload.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://202.104.32.168/list.php?id="
DATE_FROM="2001"
DATE_TO="2004"
MAX_ROWS=3000
MAX_BODY=1_500_000
WORKERS=8

TOKENS=(
    "石器时代",
    "石器時代",
    "精灵王",
    "精靈王",
    "StoneAge",
    "stone age",
    "sa25up",
    "sa25",
)
HREF_RE=re.compile(r"""(?is)href\s*=\s*["']?([^"'\s>]+)""")
TITLE_RE=re.compile(r"(?is)<title[^>]*>(.*?)</title>")
CHARSET_RE=re.compile(br"(?i)charset\s*=\s*['\"]?([a-z0-9._-]+)")


def clean(v,limit=1800):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(MAX_BODY+1)
        if len(body)>MAX_BODY:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),body


def cdx_url():
    p=[
        ("url",PREFIX),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from",DATE_FROM),("to",DATE_TO),("filter","statuscode:200"),
        ("collapse","urlkey"),("limit",str(MAX_ROWS)),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    rows=[]
    for row in data[1:]:
        if not isinstance(row,list):
            continue
        d=dict(zip(header,row))
        original=str(d.get("original") or "")
        if re.search(r"(?i)/list\.php\?id=\d+(?:$|&)",original):
            rows.append(d)
    return tuple(rows)


def replay_url(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"


def declared_charset(body):
    m=CHARSET_RE.search(body[:100_000])
    return m.group(1).decode("ascii","ignore").lower() if m else ""


def decode(body):
    declared=declared_charset(body)
    order=[]
    for enc in (declared,"gb2312","gbk","gb18030","big5","cp950","utf-8","latin1"):
        if enc and enc not in order:
            order.append(enc)
    best=None
    for enc in order:
        try:
            text=body.decode(enc,errors="replace")
        except LookupError:
            continue
        repl=text.count("\ufffd")
        # Prefer declared encoding when replacement counts are close; archived
        # native 21CN detail pages consistently declare GB2312.
        declared_penalty=0 if enc==declared and declared else 1
        score=(repl,declared_penalty,order.index(enc))
        if best is None or score<best[0]:
            best=(score,enc,text)
    return ("binary","") if best is None else (best[1],best[2])


def visible(text):
    t=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    t=re.sub(r"(?is)<style\b.*?</style>"," ",t)
    t=re.sub(r"(?is)<[^>]+>"," ",t)
    return " ".join(html.unescape(t).split())


def title(text):
    m=TITLE_RE.search(text)
    return visible(m.group(1)) if m else ""


def matching_tokens(body,text):
    hits=[]
    low=text.lower()
    raw_ascii=body.lower()
    for token in TOKENS:
        found=token.lower() in low
        if not found:
            for enc in ("gb2312","gbk","gb18030","big5","cp950","utf-8"):
                try:
                    if token.encode(enc).lower() in raw_ascii:
                        found=True
                        break
                except Exception:
                    pass
        if found:
            hits.append(token)
    return tuple(dict.fromkeys(hits))


def context(text,tokens,radius=500):
    v=visible(text)
    low=v.lower()
    positions=[low.find(t.lower()) for t in tokens]
    positions=[i for i in positions if i>=0]
    if not positions:
        return ""
    i=min(positions)
    return v[max(0,i-radius):min(len(v),i+radius*2)]


def relevant_hrefs(text):
    out=[]
    seen=set()
    for raw in HREF_RE.findall(text):
        href=html.unescape(raw.strip())
        low=href.lower()
        if (
            "downit.php" in low
            or "sa25" in low
            or "stoneage" in low
            or "/file/game/" in low
            or "download.21cn.com" in low
            or "202.104.32.168" in low
        ):
            if href not in seen:
                seen.add(href); out.append(href)
    return tuple(out)


def inspect(row):
    url=replay_url(row)
    last=None
    for attempt in range(2):
        try:
            st,final,body=fetch(url,12)
            enc,text=decode(body)
            hits=matching_tokens(body,text)
            if not hits:
                return {"kind":"miss","row":row}
            return {
                "kind":"hit","row":row,"status":st,"final":final,
                "body":body,"encoding":enc,"title":title(text),
                "tokens":hits,"context":context(text,hits),
                "hrefs":relevant_hrefs(text),
            }
        except Exception as e:
            last=e
            if attempt==0:
                time.sleep(0.25)
    return {"kind":"error","row":row,"error":(type(last).__name__,str(last))}


def main():
    print("StoneAge 2.5 native 21CN software-detail scan — R1")
    print("SCOPE|wayback-native-list-pages|html-only|no-linked-software-payload")
    print(f"WINDOW|{DATE_FROM}-{DATE_TO}|prefix={PREFIX}|workers={WORKERS}")
    errors=[]

    try:
        st,final,body=fetch(cdx_url(),30)
        rows=parse_cdx(body)
        print(
            f"CDX|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"rows={len(rows)}|final={clean(final)}"
        )
    except Exception as e:
        print(f"FATAL|cdx|{type(e).__name__}|{clean(e)}")
        return

    hits=[]
    misses=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for result in ex.map(inspect,rows):
            if result["kind"]=="miss":
                misses+=1
                continue
            if result["kind"]=="error":
                row=result["row"]; kind,msg=result["error"]
                errors.append((str(row.get("timestamp") or ""),str(row.get("original") or ""),kind,msg))
                continue
            hits.append(result)

    hits.sort(key=lambda x:(str(x["row"].get("timestamp") or ""),str(x["row"].get("original") or "")))
    for n,result in enumerate(hits,1):
        row=result["row"]; body=result["body"]
        print(
            f"MATCH|order={n}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
            f"archive_digest={clean(row.get('digest'))}|archive_length={clean(row.get('length'))}|"
            f"replay_status={result['status']}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"encoding={clean(result['encoding'])}|title={clean(result['title'],900)}|tokens={clean(','.join(result['tokens']))}"
        )
        print(f"CONTEXT|order={n}|value={clean(result['context'],2600)}")
        for j,href in enumerate(result["hrefs"][:100],1):
            print(f"HREF|match={n}|order={j}|value={clean(href,2000)}")

    for ts,original,kind,msg in errors[:300]:
        print(f"ERROR|timestamp={clean(ts)}|original={clean(original)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|cdx_rows|{len(rows)}")
    print(f"COUNT|replay_misses|{misses}")
    print(f"COUNT|matches|{len(hits)}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|NATIVE_21CN_STONEAGE_RECORD_CANDIDATES_FOUND|classify exact record/date/size/download topology before provenance promotion")
    elif errors:
        print("RESOLUTION|PARTIAL_NATIVE_21CN_SCAN|retry failed rows only or reduce concurrency")
    else:
        print("RESOLUTION|NO_NATIVE_21CN_STONEAGE_RECORD|tested archived list.php corpus bounded")
    print(
        "EVIDENCE_BOUNDARY|a matching 21CN detail page can establish catalogue metadata and download topology; "
        "it cannot prove linked payload integrity or operator provenance without bytes/cross-source evidence."
    )


if __name__=="__main__":
    main()
