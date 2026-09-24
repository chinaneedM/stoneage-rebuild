#!/usr/bin/env python3
"""Recover archived 21CN search-result surfaces for StoneAge keywords.

Uses Wayback CDX for the native 21CN forsearch.php endpoint, including legacy GB2312
query encodings. Replays only archived HTML search-result pages and extracts catalogue
IDs/labels. No software payload is requested.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
BASES=(
    "http://download.21cn.com/forsearch.php",
    "http://202.104.32.168/forsearch.php",
)
KEYWORDS=("石器时代","石器时代2.5","精灵王传说","StoneAge")
PARAMS=("s_keyword","word")
ANCHOR_RE=re.compile(r"""(?is)<a\b[^>]*?href\s*=\s*["']?([^"'\s>]+)["']?[^>]*>(.*?)</a>""")


def clean(v,limit=2600):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=24,max_bytes=3_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b


def cdx_url(url,match="exact",limit=3000):
    p=[
        ("url",url),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2001"),("to","2005"),("limit",str(limit)),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    h=data[0]
    return tuple(dict(zip(h,row)) for row in data[1:] if isinstance(row,list))


def encoded_query(base,param,keyword,encoding):
    raw=keyword.encode(encoding)
    value=urllib.parse.quote_from_bytes(raw,safe="")
    return f"{base}?{param}={value}"


def query_variants():
    out=[]; seen=set()
    for base in BASES:
        for param in PARAMS:
            for keyword in KEYWORDS:
                for enc in ("gb2312","utf-8"):
                    try:
                        url=encoded_query(base,param,keyword,enc)
                    except Exception:
                        continue
                    key=(url.lower(),)
                    if key in seen: continue
                    seen.add(key)
                    out.append((f"{urllib.parse.urlsplit(base).hostname}:{param}:{keyword}:{enc}",url))
    # Also enumerate the whole endpoint prefix once per host to catch forms not guessed above.
    for base in BASES:
        out.append((f"{urllib.parse.urlsplit(base).hostname}:prefix",base))
    return tuple(out)


def decode_query_original(url):
    try:
        q=urllib.parse.urlsplit(url).query
        raw=urllib.parse.unquote_to_bytes(q)
    except Exception:
        return ""
    texts=[]
    for enc in ("gb2312","gb18030","utf-8","latin1"):
        try:
            texts.append(raw.decode(enc))
        except Exception:
            pass
    return " || ".join(texts)


def catalogue_id(href):
    try:
        q=urllib.parse.parse_qs(urllib.parse.urlsplit(html.unescape(href)).query)
        vals=q.get("id") or ()
        return str(vals[0]) if vals and str(vals[0]).isdigit() else ""
    except Exception:
        return ""


def stoneage_anchors(text):
    out=[]; seen=set()
    for href,label_html in ANCHOR_RE.findall(text):
        label=visible(html.unescape(label_html))
        href=html.unescape(href.strip())
        low=(label+" "+href).lower()
        if any(k in low for k in ("石器","stoneage","精灵王","精靈王")):
            key=(label,href,catalogue_id(href))
            if key not in seen:
                seen.add(key); out.append(key)
    return tuple(out)


def one_cdx(item):
    label,url=item
    match="prefix" if label.endswith(":prefix") else "exact"
    try:
        st,final,b=fetch(cdx_url(url,match,10000 if match=="prefix" else 1000),30,5_000_000)
        return label,url,match,st,final,b,parse_cdx(b),None
    except Exception as exc:
        return label,url,match,None,None,None,(),(type(exc).__name__,str(exc))


def replay(row):
    return f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"


def one_page(row):
    try:
        st,final,b=fetch(replay(row),22,1_500_000)
        enc,text=decode(b,declared_charset(b))
        return row,st,final,b,enc,stoneage_anchors(text),visible(text),None
    except Exception as exc:
        return row,None,None,None,None,(),"",(type(exc).__name__,str(exc))


def main():
    print("StoneAge 2.5 21CN archived-search surface probe — R1")
    print("SCOPE|native-forsearch-cdx+archived-html|legacy-query-encodings|no-software-payload")
    errors=[]; all_rows={}; relevant_rows={}
    variants=query_variants()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for label,url,match,st,final,b,rows,error in ex.map(one_cdx,variants):
            if error:
                errors.append((f"cdx:{label}",error[0],error[1])); continue
            print(
                f"CDX|label={clean(label)}|match={match}|status={st}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for r in rows:
                key=(str(r.get("timestamp") or ""),str(r.get("original") or ""))
                all_rows[key]=r
                decoded=decode_query_original(str(r.get("original") or ""))
                if any(k.lower() in decoded.lower() for k in KEYWORDS) or any(
                    x in decoded for x in ("石器","精灵王","精靈王")
                ):
                    relevant_rows[key]=r
                    print(
                        f"SEARCH_ROW|label={clean(label)}|timestamp={clean(r.get('timestamp'))}|"
                        f"original={clean(r.get('original'))}|decoded_query={clean(decoded,2200)}|"
                        f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|"
                        f"length={clean(r.get('length'))}|digest={clean(r.get('digest'))}"
                    )

    # Prefer explicit keyword-query rows; replay unique HTTP-200 HTML rows only.
    selected=[
        r for r in relevant_rows.values()
        if str(r.get("statuscode") or "")=="200" and "html" in str(r.get("mimetype") or "").lower()
    ]
    selected=sorted(selected,key=lambda r:(str(r.get("timestamp") or ""),str(r.get("original") or "")))[:40]
    found={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for r,st,final,b,enc,anchors,vis,error in ex.map(one_page,selected):
            ts=str(r.get("timestamp") or "")
            if error:
                errors.append((f"replay:{ts}",error[0],error[1])); continue
            print(
                f"PAGE|timestamp={clean(ts)}|original={clean(r.get('original'))}|status={st}|"
                f"bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|"
                f"stoneage_anchors={len(anchors)}|final={clean(final)}"
            )
            if anchors:
                # concise local context around the first StoneAge token, not the full page
                low=vis.lower(); positions=[low.find(k.lower()) for k in ("石器","stoneage","精灵王","精靈王")]
                positions=[p for p in positions if p>=0]
                if positions:
                    i=min(positions)
                    print(f"CONTEXT|timestamp={clean(ts)}|value={clean(vis[max(0,i-700):i+2400],3600)}")
            for n,(label,href,cid) in enumerate(anchors,1):
                print(
                    f"MATCH|timestamp={clean(ts)}|order={n}|label={clean(label,1700)}|"
                    f"href={clean(href,2200)}|catalogue_id={clean(cid)}"
                )
                if cid:
                    found.setdefault(cid,set()).add(label)

    for cid,labels in sorted(found.items(),key=lambda kv:int(kv[0])):
        print(f"CATALOGUE_ID|id={cid}|labels={clean(' || '.join(sorted(labels)),3200)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|query_variants|{len(variants)}")
    print(f"COUNT|unique_cdx_rows|{len(all_rows)}")
    print(f"COUNT|relevant_query_rows|{len(relevant_rows)}")
    print(f"COUNT|selected_replays|{len(selected)}")
    print(f"COUNT|catalogue_ids|{len(found)}")
    print(f"COUNT|errors|{len(errors)}")
    external=[cid for cid in found if cid!="20165"]
    print(f"COUNT|external_catalogue_ids|{len(external)}")
    if external:
        print("RESOLUTION|STONEAGE_SEARCH_IDS_FOUND|trace external IDs for full-client/package classification")
    elif found:
        print("RESOLUTION|ONLY_KNOWN_20165_FOUND|21CN archived search surface bounded for additional StoneAge records")
    elif errors:
        print("RESOLUTION|PARTIAL_SEARCH_SURFACE_FAILURE|retry only failed search queries")
    else:
        print("RESOLUTION|NO_ARCHIVED_STONEAGE_SEARCH_PAGE|21CN forsearch surface yielded no recoverable StoneAge result page")
    print("EVIDENCE_BOUNDARY|archived search results are discovery metadata; every catalogue ID requires its own native-page verification.")


if __name__=="__main__":
    main()
