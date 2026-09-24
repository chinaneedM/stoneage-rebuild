#!/usr/bin/env python3
"""Recover historical StoneAge 4.0/5.0/6.0 full-map package targets and archive indexes.

These later map packs are descendant comparison carriers only. The probe
extracts exact download hrefs from contemporaneous Sina pages, queries Wayback
CDX and Internet Archive metadata for target basenames/URLs, and retains only
metadata. It does not download map/client payloads and does not promote later
maps to Taiwan-v1 provenance.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
IA="https://archive.org/advancedsearch.php"

PAGES=(
    (
        "40-map-patch",
        "https://games.sina.com.cn/downgames/updatex/11084599.shtml",
        ("shiqi4updatex_02_11_08.zip","新浪本地下载"),
    ),
    (
        "50-full-map",
        "https://games.sina.com.cn/zhqu/sta/ltxs/sqxz.shtml",
        ("完整地图档下载","MAP"),
    ),
    (
        "60-full-map",
        "https://games.sina.com.cn/zhqu/sta/download.shtml",
        ("真正全开MAP地图",),
    ),
)

HREF_RE=re.compile(r"<a\b[^>]*?href\s*=\s*([\"'])(.*?)\1",re.I|re.S)


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch(url,timeout=25):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return {
            "status":int(getattr(response,"status",response.getcode())),
            "final":response.geturl(),
            "headers":dict(response.headers),
            "body":body,
        }


def decode_page(body,headers=None):
    ct=(headers or {}).get("Content-Type","")
    candidates=[]
    m=re.search(r"charset\s*=\s*([\w.-]+)",ct,re.I)
    if m:
        candidates.append(m.group(1))
    head=body[:16384].decode("ascii","ignore")
    m=re.search(r"charset\s*=\s*[\"']?([\w.-]+)",head,re.I)
    if m:
        candidates.append(m.group(1))
    candidates.extend(["gb18030","utf-8"])
    for enc in candidates:
        try:
            return body.decode(enc),enc
        except (LookupError,UnicodeDecodeError):
            pass
    return body.decode("gb18030","replace"),"gb18030-replace"


def anchors(text,base):
    rows=[]
    for match in HREF_RE.finditer(text):
        href=html.unescape(match.group(2).strip())
        if not href or href.lower().startswith(("javascript:","mailto:","#")):
            continue
        rows.append((match.start(),urllib.parse.urljoin(base,href)))
    return rows


def target_hrefs(text,base,tokens,window=1600):
    all_anchors=anchors(text,base)
    out=[]
    seen=set()
    for token in tokens:
        start=0
        while True:
            pos=text.find(token,start)
            if pos<0:
                break
            nearby=sorted(
                (
                    (abs(anchor_pos-pos),anchor_pos-pos,url)
                    for anchor_pos,url in all_anchors
                    if abs(anchor_pos-pos)<=window
                ),
                key=lambda row:(row[0],row[1],row[2]),
            )
            for distance,delta,url in nearby[:12]:
                key=(token,url)
                if key in seen:
                    continue
                seen.add(key)
                out.append((token,delta,url))
            start=pos+len(token)
    return tuple(out)


def basename_hint(url):
    parsed=urllib.parse.urlsplit(url)
    name=parsed.path.rsplit("/",1)[-1]
    if name.lower() in {"download.pl",""}:
        qs=urllib.parse.parse_qs(parsed.query)
        values=qs.get("filename",[])
        if values:
            name=values[0]
    return name


def cdx_query(target,timeout=25):
    params=[
        ("url",target),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("filter","statuscode:200"),("collapse","digest"),("limit","50"),
    ]
    url=CDX+"?"+urllib.parse.urlencode(params)
    result=fetch(url,timeout=timeout)
    rows=[]
    try:
        data=json.loads(result["body"].decode("utf-8"))
        if isinstance(data,list) and data:
            header=data[0]
            for row in data[1:]:
                if isinstance(row,list):
                    rows.append(dict(zip(header,row)))
    except Exception:
        pass
    return url,result,tuple(rows)


def ia_search(term,timeout=25):
    q=f'"{term}"'
    params=[
        ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
        ("fl[]","mediatype"),("rows","50"),("page","1"),("output","json"),
    ]
    url=IA+"?"+urllib.parse.urlencode(params)
    result=fetch(url,timeout=timeout)
    docs=[]
    try:
        data=json.loads(result["body"].decode("utf-8"))
        docs=data.get("response",{}).get("docs",[])
    except Exception:
        pass
    return url,result,tuple(docs)


def main():
    print("StoneAge historical full-map package archive probe — R1")
    print("SCOPE|Sina-4.0-5.0-6.0-map-targets+Wayback-CDX+IA-metadata|no-payload-download|descendant-comparison-only")

    target_rows=[]
    errors=[]
    for label,page,tokens in PAGES:
        try:
            result=fetch(page)
        except Exception as exc:
            errors.append((f"page:{label}",type(exc).__name__,str(exc)))
            continue
        text,encoding=decode_page(result["body"],result["headers"])
        print(
            f"PAGE|label={label}|status={result['status']}|bytes={len(result['body'])}|"
            f"sha256={hashlib.sha256(result['body']).hexdigest()}|encoding={clean(encoding)}|"
            f"final={clean(result['final'])}"
        )
        rows=target_hrefs(text,result["final"],tokens)
        for token,delta,url in rows:
            name=basename_hint(url)
            # Keep only plausible download/package targets and the exact 4.0 CGI.
            low=url.lower()
            plausible=(
                any(x in low for x in (".zip",".exe",".rar",".vcd","download.pl","/map"))
                or "map" in name.lower()
            )
            if not plausible:
                continue
            target_rows.append((label,token,delta,url,name))
            print(
                f"TARGET|label={label}|anchor={clean(token)}|delta_chars={delta}|"
                f"url={clean(url)}|basename={clean(name)}"
            )

    # Deduplicate URLs while preserving every source label.
    grouped={}
    for label,token,delta,url,name in target_rows:
        rec=grouped.setdefault(url,{"labels":set(),"names":set()})
        rec["labels"].add(label)
        if name:
            rec["names"].add(name)

    cdx_hits=0
    ia_hits=0
    searched_names=set()
    for url,rec in sorted(grouped.items()):
        try:
            qurl,result,rows=cdx_query(url)
            cdx_hits+=len(rows)
            print(
                f"CDX|labels={','.join(sorted(rec['labels']))}|status={result['status']}|"
                f"bytes={len(result['body'])}|rows={len(rows)}|target={clean(url)}"
            )
            for row in rows:
                print(
                    f"CDX_HIT|labels={','.join(sorted(rec['labels']))}|"
                    f"timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
                    f"statuscode={clean(row.get('statuscode'))}|mimetype={clean(row.get('mimetype'))}|"
                    f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
                )
        except Exception as exc:
            errors.append((f"cdx:{url}",type(exc).__name__,str(exc)))

        for name in sorted(rec["names"]):
            if not name or name.lower() in {"map","download.pl"} or name in searched_names:
                continue
            searched_names.add(name)
            try:
                qurl,result,docs=ia_search(name)
                ia_hits+=len(docs)
                print(
                    f"IA_QUERY|basename={clean(name)}|status={result['status']}|"
                    f"bytes={len(result['body'])}|items={len(docs)}"
                )
                for doc in docs:
                    print(
                        f"IA_HIT|basename={clean(name)}|identifier={clean(doc.get('identifier'))}|"
                        f"title={clean(doc.get('title'))}|date={clean(doc.get('date'))}|"
                        f"mediatype={clean(doc.get('mediatype'))}"
                    )
            except Exception as exc:
                errors.append((f"ia:{name}",type(exc).__name__,str(exc)))

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|pages|{len(PAGES)}")
    print(f"COUNT|unique_targets|{len(grouped)}")
    print(f"COUNT|searched_basenames|{len(searched_names)}")
    print(f"COUNT|cdx_rows|{cdx_hits}")
    print(f"COUNT|ia_items|{ia_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if cdx_hits or ia_hits:
        print("RESOLUTION|HISTORICAL_MAP_PACK_ARCHIVE_CANDIDATES_FOUND|verify version and package contents before comparison")
    elif grouped and not errors:
        print("RESOLUTION|HISTORICAL_MAP_PACK_TARGETS_NO_ARCHIVE_HIT|exact targets recovered but tested archive indexes have no hit")
    elif grouped:
        print("RESOLUTION|PARTIAL|exact targets recovered but archive-index probing incomplete")
    else:
        print("RESOLUTION|INCONCLUSIVE|no exact map-package targets recovered")


if __name__=="__main__":
    main()
