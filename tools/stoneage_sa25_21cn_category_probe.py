#!/usr/bin/env python3
"""Search archived 21CN category/listing pages for StoneAge records.

The 21CN host's CDX neighborhood contains a small second.php surface that can reveal
native list.php IDs without replaying every software-detail page. HTML only; no linked
software payload is downloaded.
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

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, title, visible

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://202.104.32.168/second.php"
TOKENS=("石器时代","石器時代","精灵王","精靈王","StoneAge","stone age","sa25")
HREF_RE=re.compile(r"""(?is)href\s*=\s*["']?([^"'\s>]+)""")
LIST_ID_RE=re.compile(r'''(?i)list\.php\?[^#"'<>]*?\bid=(\d+)''')


def clean(v,limit=1800):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=20,max_bytes=2_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),body


def cdx_url():
    p=[
        ("url",PREFIX),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from","2001"),("to","2004"),("filter","statuscode:200"),
        ("filter","mimetype:text/html"),("collapse","urlkey"),("limit","1000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    out=[]; seen=set()
    for row in data[1:]:
        if not isinstance(row,list):
            continue
        d=dict(zip(header,row))
        original=str(d.get("original") or "")
        if urllib.parse.urlsplit(original).path.lower()!="/second.php":
            continue
        if original in seen:
            continue
        seen.add(original); out.append(d)
    return tuple(out)


def replay_url(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"


def token_hits(body,text):
    low=text.lower()
    hits=[]
    for token in TOKENS:
        found=token.lower() in low
        if not found:
            for enc in ("gb2312","gbk","gb18030","big5","cp950","utf-8"):
                try:
                    if token.encode(enc) in body:
                        found=True; break
                except Exception:
                    pass
        if found:
            hits.append(token)
    return tuple(dict.fromkeys(hits))


def extract_list_ids(text):
    return tuple(dict.fromkeys(LIST_ID_RE.findall(html.unescape(text))))


def relevant_hrefs(text):
    out=[]; seen=set()
    for href in HREF_RE.findall(text):
        href=html.unescape(href.strip())
        low=href.lower()
        if "list.php" in low or "stoneage" in low or "sa25" in low:
            if href not in seen:
                seen.add(href); out.append(href)
    return tuple(out)


def context(text,tokens,radius=500):
    v=visible(text); low=v.lower()
    positions=[low.find(t.lower()) for t in tokens]
    positions=[i for i in positions if i>=0]
    if not positions:
        return ""
    i=min(positions)
    return v[max(0,i-radius):min(len(v),i+1000)]


def inspect(row):
    last=None
    for attempt in range(3):
        try:
            st,final,body=fetch(replay_url(row),15)
            enc,text=decode(body,declared_charset(body))
            hits=token_hits(body,text)
            return row,st,final,body,enc,text,hits,None
        except Exception as e:
            last=e
            if attempt<2:
                time.sleep(0.6*(attempt+1))
    return row,None,None,None,None,None,(),(type(last).__name__,str(last))


def main():
    print("StoneAge 2.5 21CN category-page scan — R1")
    print("SCOPE|wayback-second.php-html|category-to-detail-id-discovery|no-linked-software-payload")
    errors=[]

    try:
        st,final,body=fetch(cdx_url(),30,4_000_000)
        rows=parse_cdx(body)
        print(f"CDX|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}")
    except Exception as e:
        print(f"FATAL|cdx|{type(e).__name__}|{clean(e)}")
        return

    matches=[]; completed=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for row,st,final,pbody,enc,text,hits,error in ex.map(inspect,rows):
            if error:
                errors.append((str(row.get("timestamp") or ""),str(row.get("original") or ""),error[0],error[1]))
                continue
            completed+=1
            if not hits:
                continue
            ids=extract_list_ids(text)
            hrefs=relevant_hrefs(text)
            matches.append((row,st,final,pbody,enc,text,hits,ids,hrefs))

    for n,(row,st,final,pbody,enc,text,hits,ids,hrefs) in enumerate(matches,1):
        print(
            f"MATCH|order={n}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
            f"status={st}|bytes={len(pbody)}|sha256={hashlib.sha256(pbody).hexdigest()}|"
            f"encoding={clean(enc)}|title={clean(title(text),1000)}|tokens={clean(','.join(hits))}|list_ids={clean(','.join(ids))}|final={clean(final)}"
        )
        print(f"CONTEXT|order={n}|value={clean(context(text,hits),2600)}")
        for j,href in enumerate(hrefs[:100],1):
            print(f"HREF|match={n}|order={j}|value={clean(href,1800)}")

    for ts,original,kind,msg in errors[:100]:
        print(f"ERROR|timestamp={clean(ts)}|original={clean(original)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|category_rows|{len(rows)}")
    print(f"COUNT|completed_pages|{completed}")
    print(f"COUNT|matches|{len(matches)}")
    print(f"COUNT|errors|{len(errors)}")
    if matches:
        print("RESOLUTION|21CN_CATEGORY_STONEAGE_MATCH_FOUND|follow recovered list.php IDs and native download topology")
    elif completed==len(rows):
        print("RESOLUTION|NO_21CN_CATEGORY_STONEAGE_MATCH|tested archived second.php surface bounded")
    else:
        print("RESOLUTION|PARTIAL_21CN_CATEGORY_SCAN|retry failed category pages only")
    print("EVIDENCE_BOUNDARY|category-page text can recover native record IDs/topology but does not authenticate linked client bytes.")


if __name__=="__main__":
    main()
