#!/usr/bin/env python3
"""Use public mirrors to recover source-labelled Mainland StoneAge 1.x/2.0 package images.

All image bodies are transient. Only URLs, hashes, dimensions and SIFT/RANSAC metrics
are emitted. This supplements the primary collector host when its image CDN refuses CI.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse

from tools.stoneage_ruten_early_carrier_probe import DETAIL, detail_rows, image_urls
from tools.stoneage_sa25_physical_image_fingerprint_probe import ImageParser, fetch, normalize_image_url
from tools.stoneage_sa25_disc_region_match_probe import load_sift, sift_match

DIRECT_MIRRORS=(
    ("mirror-20","https://www.sa85.com.cn/shiqi2710.html","石器时代周边收藏客户端礼包篇（五）2.0版本礼盒"),
)
DISCOVERY_MIRRORS=(
    ("mirror-1x","https://shiqi.ws/page_35.html","石器时代182时期的端游客户端新手礼包"),
)
RAW_IMAGE_RE=re.compile(r'''(?i)(?:https?:)?//[^\"'<>\\\s)]+?\.(?:jpe?g|png|gif|webp)(?:\?[^\"'<>\\\s)]*)?|(?:\.\.?/|/)[^\"'<>\\\s)]+?\.(?:jpe?g|png|gif|webp)(?:\?[^\"'<>\\\s)]*)?''')

RUTEN_TARGETS=(
    ("22636573895893","mainland-retail-box"),
    ("22638643800877","mainland-boxed-disc"),
    ("22631284715652","beijing-waei-newbie-control"),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def discover_article(html_text,base,needle):
    p=ImageParser(); p.feed(html_text)
    out=[]; seen=set()
    for row in p.links:
        text=row.get("text","")
        if needle in text:
            u=normalize_image_url(base,row.get("href"))
            if u and u not in seen:
                seen.add(u); out.append(u)
    return tuple(out)

def raw_image_urls(html_text,base):
    cooked=html.unescape(html_text).replace("\\/","/")
    out=[]; seen=set()
    for raw in RAW_IMAGE_RE.findall(cooked):
        u=normalize_image_url(base,raw)
        if not u.startswith(("http://","https://")):
            continue
        if u not in seen:
            seen.add(u); out.append(u)
    return tuple(out)

def page_images(html_text,base):
    p=ImageParser(); p.feed(html_text)
    out=[]; seen=set()
    for idx,row in enumerate(p.rows):
        u=normalize_image_url(base,row.get("url"))
        if not u.startswith(("http://","https://")):
            continue
        path=urllib.parse.urlsplit(u).path.lower()
        if not any(path.endswith(ext) for ext in (".jpg",".jpeg",".png",".gif",".webp")):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append({"index":idx,"url":u,"alt":row.get("alt",""),"title":row.get("title","")})
    for n,u in enumerate(raw_image_urls(html_text,base)):
        if u in seen:
            continue
        seen.add(u)
        out.append({"index":f"raw{n}","url":u,"alt":"","title":""})
    return tuple(out)

def ruten_meta():
    out=[]
    for pid,role in RUTEN_TARGETS:
        q=urllib.parse.urlencode({"gno":pid,"level":"simple"})
        st,final,h,b=fetch(DETAIL+"?"+q,accept="application/json,*/*",referer="https://www.ruten.com.tw/",timeout=25,attempts=2)
        data=json.loads(b.decode("utf-8","replace"))
        for row in detail_rows(data):
            for idx,u in enumerate(image_urls(row)):
                out.append({"label":f"ruten:{pid}:{idx}","carrier":pid,"scope":role,"url":u,"referer":"https://www.ruten.com.tw/"})
    return tuple(out)

def main():
    print("StoneAge Mainland package mirror visual match — R2")
    print("SCOPE|public-mirror-images-transient|source-labelled-1.x-vs-2.0|SIFT+RANSAC|no-image-commit")
    errors=[]
    pages=list(DIRECT_MIRRORS)

    for scope,index_url,needle in DISCOVERY_MIRRORS:
        try:
            st,final,h,b=fetch(index_url,accept="text/html,*/*",timeout=25,attempts=2)
            links=discover_article(b.decode("utf-8","replace"),final,needle)
            print(f"MIRROR_INDEX|scope={scope}|status={st}|bytes={len(b)}|links={len(links)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for u in links:
                pages.append((scope,u,needle))
                print(f"MIRROR_LINK|scope={scope}|title={clean(needle)}|url={clean(u)}")
        except Exception as e:
            errors.append((f"index:{index_url}",type(e).__name__,str(e)))

    references=[]
    seen_pages=set()
    for scope,url,title in pages:
        if (scope,url) in seen_pages:
            continue
        seen_pages.add((scope,url))
        try:
            st,final,h,b=fetch(url,accept="text/html,*/*",timeout=25,attempts=2)
            imgs=page_images(b.decode("utf-8","replace"),final)
            print(f"MIRROR_PAGE|scope={scope}|title={clean(title)}|status={st}|bytes={len(b)}|images={len(imgs)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for row in imgs:
                references.append({"label":f"{scope}:{row['index']}","scope":scope,"url":row["url"],"referer":final,"alt":row["alt"],"title":row["title"]})
                print(f"REFERENCE_URL|scope={scope}|label={scope}:{row['index']}|url={clean(row['url'])}|alt={clean(row['alt'])}|title={clean(row['title'])}")
        except Exception as e:
            errors.append((f"page:{url}",type(e).__name__,str(e)))

    queries=[]
    try:
        qmeta=ruten_meta()
    except Exception as e:
        qmeta=[]
        errors.append(("ruten-meta",type(e).__name__,str(e)))
    for row in qmeta:
        try:
            f=load_sift(row["label"],row["url"],referer=row["referer"],carrier=row["carrier"],scope=row["scope"])
            queries.append(f)
            print(f"QUERY|scope={clean(f['scope'])}|label={clean(f['label'])}|carrier={clean(f['carrier'])}|size={f['width']}x{f['height']}|sha256={f['sha256']}")
        except Exception as e:
            errors.append((row["label"],type(e).__name__,str(e)))

    targets=[]
    for row in references:
        try:
            f=load_sift(row["label"],row["url"],referer=row["referer"],scope=row["scope"])
            if max(f["width"],f["height"])<300:
                print(f"REFERENCE_SKIP|scope={row['scope']}|label={row['label']}|reason=small|size={f['width']}x{f['height']}|sha256={f['sha256']}")
                continue
            targets.append(f)
            print(f"REFERENCE|scope={clean(f['scope'])}|label={clean(f['label'])}|size={f['width']}x{f['height']}|keypoints={len(f['kp'])}|sha256={f['sha256']}|url={clean(f['url'])}")
        except Exception as e:
            errors.append((row["label"],type(e).__name__,str(e)))

    rows=[]
    for q in queries:
        for t in targets:
            m=sift_match(q,t)
            rows.append((m["inliers"],m["good"],m["query_coverage"],q,t,m))
    rows.sort(key=lambda z:(z[0],z[1],z[2]),reverse=True)
    print(f"COUNT|queries|{len(queries)}")
    print(f"COUNT|references|{len(targets)}")
    print(f"COUNT|pairs|{len(rows)}")
    for _,_,_,q,t,m in rows[:200]:
        print(
            f"MATCH|query={clean(q['label'])}|query_carrier={clean(q.get('carrier'))}|query_scope={clean(q.get('scope'))}|"
            f"target_scope={clean(t.get('scope'))}|target={clean(t['label'])}|good075={m['good']}|"
            f"ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}|query_coverage={m['query_coverage']:.4f}|"
            f"target_coverage={m['target_coverage']:.4f}|quad_ok={int(m['quad_ok'])}|quad_area_ratio={m['quad_area_ratio']:.4f}"
        )
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    print("REFERENCE_SCOPES|"+",".join(sorted({x.get("scope","") for x in targets})))
    if rows:
        print("RESOLUTION|MIRROR_PACKAGE_METRICS_AVAILABLE|only source-labelled coherent matches may narrow generation")
    else:
        print("RESOLUTION|NO_MIRROR_PACKAGE_METRICS|do not infer generation")
    print("EVIDENCE_BOUNDARY|mirror labels can recover package-generation context, but shared artwork is insufficient by itself; require coherent local geometry, exact identifiers, or an independent contemporaneous package record.")

if __name__=="__main__":
    main()
