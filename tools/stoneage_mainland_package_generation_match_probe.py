#!/usr/bin/env python3
"""Compare surviving Mainland StoneAge retail boxes against 1.82/2.0 package references.

Public web/image reads are transient in CI. Repository output contains only discovered
article/image URLs, hashes and SIFT/RANSAC metrics. No source image bodies are committed.
"""
from __future__ import annotations

import hashlib
import html.parser
import json
import urllib.parse

from tools.stoneage_ruten_early_carrier_probe import DETAIL, detail_rows, image_urls
from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    MAX_IMAGE_BYTES,
    ImageParser,
    fetch,
    normalize_image_url,
)
from tools.stoneage_sa25_disc_region_match_probe import load_sift, sift_match

BLOG_INDEXES = (
    "https://blog.shiqi.so/page2.htm",
    "https://blog.shiqi.so/sqcy5.htm",
    "https://blog.shiqi.so/sqcy4_2.htm",
)
BLOG_TITLES = (
    ("collector-1x", "石器时代1.82时期的客户端新手礼包"),
    ("collector-20", "石器时代2.0版客户端礼盒"),
)
PERIOD_20_PAGE = "https://news.17173.com/z/stoneage/banben/sa20-cq.htm"
RUTEN_TARGETS = (
    ("22636573895893", "mainland-retail-box"),
    ("22638643800877", "mainland-boxed-disc"),
    ("22631284715652", "beijing-waei-newbie-control"),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def discover_links(html_text, base, needles):
    p=ImageParser()
    p.feed(html_text)
    out=[]
    seen=set()
    for row in p.links:
        txt=row.get("text","")
        for label,needle in needles:
            if needle in txt:
                u=normalize_image_url(base,row.get("href"))
                key=(label,u)
                if u and key not in seen:
                    seen.add(key); out.append((label,needle,u))
    return tuple(out)

def candidate_images(html_text, base, *, dated_only=False):
    p=ImageParser()
    p.feed(html_text)
    out=[]; seen=set()
    for idx,row in enumerate(p.rows):
        u=normalize_image_url(base,row.get("url"))
        if not u.startswith(("http://","https://")):
            continue
        path=urllib.parse.urlsplit(u).path.lower()
        if not any(path.endswith(x) for x in (".jpg",".jpeg",".png",".gif",".webp")):
            continue
        if dated_only and not ("/2020/09/" in path or "/2020/9/" in path):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append({
            "index":idx,
            "url":u,
            "alt":row.get("alt",""),
            "title":row.get("title",""),
        })
    return tuple(out)

def ruten_images():
    out=[]
    for pid,role in RUTEN_TARGETS:
        q=urllib.parse.urlencode({"gno":pid,"level":"simple"})
        st,final,h,b=fetch(
            DETAIL+"?"+q,
            accept="application/json,*/*",
            referer="https://www.ruten.com.tw/",
            timeout=25,
            attempts=2,
        )
        data=json.loads(b.decode("utf-8","replace"))
        for row in detail_rows(data):
            for idx,u in enumerate(image_urls(row)):
                out.append({
                    "label":f"ruten:{pid}:{idx}",
                    "carrier":pid,
                    "role":role,
                    "url":u,
                    "referer":"https://www.ruten.com.tw/",
                })
    return tuple(out)

def main():
    print("StoneAge Mainland retail package generation match — R1")
    print("SCOPE|public-images-transient|1.x-vs-2.0-package-control|SIFT+RANSAC-derived-metrics-only|no-image-commit")
    errors=[]
    article_links=[]
    for index_url in BLOG_INDEXES:
        try:
            st,final,h,b=fetch(index_url,accept="text/html,*/*",timeout=20,attempts=2)
            links=discover_links(b.decode("utf-8","replace"),final,BLOG_TITLES)
            print(f"BLOG_INDEX|url={clean(index_url)}|status={st}|bytes={len(b)}|matched_links={len(links)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for label,title,u in links:
                article_links.append((label,title,u,index_url))
                print(f"ARTICLE_LINK|scope={label}|title={clean(title)}|url={clean(u)}")
        except Exception as e:
            errors.append((f"blog-index:{index_url}",type(e).__name__,str(e)))

    # Deduplicate discovered article URLs.
    dedup=[]; seen=set()
    for row in article_links:
        key=(row[0],row[2])
        if key not in seen:
            seen.add(key); dedup.append(row)
    article_links=dedup

    reference_meta=[]
    for label,title,u,index_url in article_links:
        try:
            st,final,h,b=fetch(u,accept="text/html,*/*",referer=index_url,timeout=20,attempts=2)
            imgs=candidate_images(b.decode("utf-8","replace"),final,dated_only=True)
            print(f"ARTICLE|scope={label}|title={clean(title)}|status={st}|bytes={len(b)}|images={len(imgs)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for row in imgs:
                reference_meta.append({
                    "label":f"{label}:{row['index']}",
                    "scope":label,
                    "url":row["url"],
                    "referer":final,
                    "alt":row["alt"],
                    "title":row["title"],
                })
                print(f"REFERENCE_URL|scope={label}|label={label}:{row['index']}|url={clean(row['url'])}|alt={clean(row['alt'])}|title={clean(row['title'])}")
        except Exception as e:
            errors.append((f"article:{u}",type(e).__name__,str(e)))

    # Contemporary 17173 2.0 product page: keep every image URL; dimension filtering happens after load.
    try:
        st,final,h,b=fetch(PERIOD_20_PAGE,accept="text/html,*/*",timeout=20,attempts=2)
        imgs=candidate_images(b.decode("utf-8","replace"),final,dated_only=False)
        print(f"PERIOD_20_PAGE|status={st}|bytes={len(b)}|images={len(imgs)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        for row in imgs:
            reference_meta.append({
                "label":f"period-20:{row['index']}",
                "scope":"period-20",
                "url":row["url"],
                "referer":final,
                "alt":row["alt"],
                "title":row["title"],
            })
            print(f"REFERENCE_URL|scope=period-20|label=period-20:{row['index']}|url={clean(row['url'])}|alt={clean(row['alt'])}|title={clean(row['title'])}")
    except Exception as e:
        errors.append(("period-20-page",type(e).__name__,str(e)))

    queries=[]
    try:
        metas=ruten_images()
    except Exception as e:
        metas=[]
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    for row in metas:
        try:
            f=load_sift(row["label"],row["url"],referer=row["referer"],carrier=row["carrier"],scope=row["role"])
            queries.append(f)
            print(f"QUERY_IMAGE|scope={clean(f['scope'])}|label={clean(f['label'])}|carrier={clean(f['carrier'])}|size={f['width']}x{f['height']}|keypoints={len(f['kp'])}|sha256={f['sha256']}|url={clean(f['url'])}")
        except Exception as e:
            errors.append((row["label"],type(e).__name__,str(e)))

    targets=[]
    for row in reference_meta:
        try:
            f=load_sift(row["label"],row["url"],referer=row["referer"],scope=row["scope"])
            if max(f["width"],f["height"]) < 250:
                print(f"REFERENCE_SKIP|scope={clean(row['scope'])}|label={clean(row['label'])}|reason=small|size={f['width']}x{f['height']}|sha256={f['sha256']}")
                continue
            targets.append(f)
            print(f"REFERENCE_IMAGE|scope={clean(f['scope'])}|label={clean(f['label'])}|size={f['width']}x{f['height']}|keypoints={len(f['kp'])}|sha256={f['sha256']}|url={clean(f['url'])}")
        except Exception as e:
            errors.append((row["label"],type(e).__name__,str(e)))

    rows=[]
    for q in queries:
        for t in targets:
            m=sift_match(q,t)
            rows.append((m["inliers"],m["good"],m["query_coverage"],q,t,m))
    rows.sort(key=lambda z:(z[0],z[1],z[2]),reverse=True)

    print(f"COUNT|article_links|{len(article_links)}")
    print(f"COUNT|queries|{len(queries)}")
    print(f"COUNT|reference_targets|{len(targets)}")
    print(f"COUNT|pairs|{len(rows)}")
    for _,_,_,q,t,m in rows[:160]:
        print(
            f"MATCH|query={clean(q['label'])}|query_carrier={clean(q.get('carrier'))}|query_scope={clean(q.get('scope'))}|"
            f"target_scope={clean(t.get('scope'))}|target={clean(t['label'])}|"
            f"good075={m['good']}|ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}|"
            f"query_coverage={m['query_coverage']:.4f}|target_coverage={m['target_coverage']:.4f}|"
            f"quad_ok={int(m['quad_ok'])}|quad_area_ratio={m['quad_area_ratio']:.4f}"
        )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    scopes=sorted({t.get("scope") for t in targets})
    print("REFERENCE_SCOPES|"+",".join(scopes))
    if rows:
        print("RESOLUTION|PACKAGE_GENERATION_METRICS_AVAILABLE|require source-labelled references and sane geometry before assigning 1.x or 2.0")
    else:
        print("RESOLUTION|NO_PACKAGE_GENERATION_METRICS|do not infer generation")
    print("EVIDENCE_BOUNDARY|shared artwork can produce feature overlap; generation attribution requires a source-labelled package reference with spatially coherent local match or exact identifier evidence. Price 29 yuan alone is not version evidence.")

if __name__=="__main__":
    main()
