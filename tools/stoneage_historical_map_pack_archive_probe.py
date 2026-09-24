#!/usr/bin/env python3
"""Recover historical StoneAge 4.0/5.0/6.0 full-map package archive metadata.

Later map packs are descendant comparison carriers only. This probe extracts a
small, source-anchored target set from contemporaneous Sina pages, then queries
Wayback CDX and Internet Archive metadata in parallel. No client/map payload is
downloaded and no later map is promoted to Taiwan-v1 provenance.
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
IA="https://archive.org/advancedsearch.php"

PAGE_40="https://games.sina.com.cn/downgames/updatex/11084599.shtml"
PAGE_50="https://games.sina.com.cn/zhqu/sta/ltxs/sqxz.shtml"
PAGE_60="https://games.sina.com.cn/zhqu/sta/download.shtml"

# Independently recovered from the current Sina 6.0 page by the earlier target
# probe. These are source-derived exact targets, not guessed paths.
KNOWN_60_MAP_TARGETS=(
    "ftp://211.90.133.5/dowload/sa/map.exe",
    "http://www.wuxitianlong.com/sa/map.exe",
)

HREF_RE=re.compile(r"<a\b[^>]*?href\s*=\s*([\"'])(.*?)\1",re.I|re.S)


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch(url,timeout=18):
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
            continue
    return body.decode("gb18030","replace"),"gb18030-replace"


def anchors(text,base):
    rows=[]
    for match in HREF_RE.finditer(text):
        href=html.unescape(match.group(2).strip())
        if not href or href.lower().startswith(("javascript:","mailto:","#")):
            continue
        rows.append((match.start(),urllib.parse.urljoin(base,href)))
    return tuple(rows)


def basename_hint(url):
    parsed=urllib.parse.urlsplit(url)
    name=parsed.path.rsplit("/",1)[-1]
    if name.lower() in {"download.pl",""}:
        values=urllib.parse.parse_qs(parsed.query).get("filename",[])
        if values:
            name=values[0]
    return name


def extract_40(text,base):
    rows=[]
    for pos,url in anchors(text,base):
        low=url.lower()
        if "shiqi4updatex_02_11_08.zip" in low or "aid=61620" in low:
            rows.append(url)
    return tuple(dict.fromkeys(rows))


def extract_50(text,base):
    marker=text.find("完整地图档下载")
    if marker<0:
        return ()
    # The map row follows the heading. Restrict to forward anchors only and a
    # narrow region so nearby client/外挂 links do not explode archive queries.
    rows=[]
    for pos,url in anchors(text,base):
        delta=pos-marker
        if not (0<=delta<=1200):
            continue
        low=url.lower()
        name=basename_hint(url).lower()
        if "map" in low or "map" in name or ".exe" in low or "download" in low:
            rows.append((delta,url))
    rows.sort(key=lambda row:(row[0],row[1]))
    return tuple(dict.fromkeys(url for _,url in rows[:3]))


def extract_targets():
    pages=(
        ("40-map-patch",PAGE_40,extract_40),
        ("50-full-map",PAGE_50,extract_50),
        ("60-full-map",PAGE_60,None),
    )
    targets=[]
    page_rows=[]
    errors=[]
    for label,url,extractor in pages:
        try:
            result=fetch(url)
            text,encoding=decode_page(result["body"],result["headers"])
            page_rows.append((
                label,result["status"],len(result["body"]),
                hashlib.sha256(result["body"]).hexdigest(),encoding,result["final"],
            ))
            if extractor is not None:
                for target in extractor(text,result["final"]):
                    targets.append((label,target))
        except Exception as exc:
            errors.append((f"page:{label}",type(exc).__name__,str(exc)))
    for target in KNOWN_60_MAP_TARGETS:
        targets.append(("60-full-map",target))
    dedup={}
    for label,url in targets:
        dedup.setdefault(url,set()).add(label)
    return page_rows,dedup,errors


def cdx_query(target):
    params=[
        ("url",target),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("filter","statuscode:200"),("collapse","digest"),("limit","50"),
    ]
    url=CDX+"?"+urllib.parse.urlencode(params)
    result=fetch(url)
    rows=[]
    try:
        data=json.loads(result["body"].decode("utf-8"))
        if isinstance(data,list) and data:
            header=data[0]
            rows=[dict(zip(header,row)) for row in data[1:] if isinstance(row,list)]
    except Exception:
        pass
    return target,url,result,tuple(rows)


def ia_search(name):
    query=f'"{name}"'
    if name.lower()=="map.exe":
        query='("map.exe") AND (StoneAge OR "Stone Age" OR "石器时代")'
    params=[
        ("q",query),("fl[]","identifier"),("fl[]","title"),
        ("fl[]","date"),("fl[]","mediatype"),
        ("rows","50"),("page","1"),("output","json"),
    ]
    url=IA+"?"+urllib.parse.urlencode(params)
    result=fetch(url)
    docs=[]
    try:
        docs=json.loads(result["body"].decode("utf-8")).get("response",{}).get("docs",[])
    except Exception:
        pass
    return name,url,result,tuple(docs)


def main():
    print("StoneAge historical full-map package archive probe — R1")
    print("SCOPE|Sina-4.0-5.0-6.0-map-targets+Wayback-CDX+IA-metadata|no-payload-download|descendant-comparison-only")

    pages,grouped,errors=extract_targets()
    for label,status,size,sha,encoding,final in pages:
        print(
            f"PAGE|label={label}|status={status}|bytes={size}|sha256={sha}|"
            f"encoding={clean(encoding)}|final={clean(final)}"
        )
    for url,labels in sorted(grouped.items()):
        print(
            f"TARGET|labels={','.join(sorted(labels))}|url={clean(url)}|"
            f"basename={clean(basename_hint(url))}"
        )

    cdx_results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures={executor.submit(cdx_query,url):url for url in grouped}
        for future in concurrent.futures.as_completed(futures):
            target=futures[future]
            try:
                cdx_results.append(future.result())
            except Exception as exc:
                errors.append((f"cdx:{target}",type(exc).__name__,str(exc)))

    cdx_hits=0
    for target,qurl,result,rows in sorted(cdx_results,key=lambda row:row[0]):
        labels=grouped[target]
        cdx_hits+=len(rows)
        print(
            f"CDX|labels={','.join(sorted(labels))}|status={result['status']}|"
            f"bytes={len(result['body'])}|rows={len(rows)}|target={clean(target)}"
        )
        for row in rows:
            print(
                f"CDX_HIT|labels={','.join(sorted(labels))}|timestamp={clean(row.get('timestamp'))}|"
                f"original={clean(row.get('original'))}|mimetype={clean(row.get('mimetype'))}|"
                f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
            )

    names=sorted({
        basename_hint(url) for url in grouped
        if basename_hint(url) and basename_hint(url).lower() not in {"map","download.pl"}
    })
    ia_results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures={executor.submit(ia_search,name):name for name in names}
        for future in concurrent.futures.as_completed(futures):
            name=futures[future]
            try:
                ia_results.append(future.result())
            except Exception as exc:
                errors.append((f"ia:{name}",type(exc).__name__,str(exc)))

    ia_hits=0
    for name,qurl,result,docs in sorted(ia_results,key=lambda row:row[0]):
        relevant=[]
        for doc in docs:
            hay=" ".join(str(doc.get(k,"")) for k in ("identifier","title","date","mediatype")).lower()
            if name.lower()!="map.exe" or "stoneage" in hay or "stone age" in hay or "石器时代" in hay:
                relevant.append(doc)
        ia_hits+=len(relevant)
        print(
            f"IA_QUERY|basename={clean(name)}|status={result['status']}|"
            f"bytes={len(result['body'])}|items={len(docs)}|relevant_items={len(relevant)}"
        )
        for doc in relevant:
            print(
                f"IA_HIT|basename={clean(name)}|identifier={clean(doc.get('identifier'))}|"
                f"title={clean(doc.get('title'))}|date={clean(doc.get('date'))}|"
                f"mediatype={clean(doc.get('mediatype'))}"
            )

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|pages|{len(pages)}")
    print(f"COUNT|unique_targets|{len(grouped)}")
    print(f"COUNT|searched_basenames|{len(names)}")
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
