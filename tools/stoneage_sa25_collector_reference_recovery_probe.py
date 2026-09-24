#!/usr/bin/env python3
"""Recover/triangulate the Mainland StoneAge 2.5 collector disc reference.

Public web/Wayback images are read transiently. Only URLs, hashes, dimensions and
derived visual-match metrics are emitted; no image bytes are committed.
"""
from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request

from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    OFFICIAL_MAINLAND_REFERENCE, collector_reference_images, fetch,
    load_image, match_features, ruten_full_images,
)

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
MAX_BYTES=12*1024*1024
OFFICIAL_HTTP=OFFICIAL_MAINLAND_REFERENCE.replace("https://","http://",1)

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def cdx_url(target,match="exact"):
    return CDX+"?"+urllib.parse.urlencode([
        ("url",target),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2020"),("to","2026"),("limit","1000"),
    ])

def cdx_fetch(target,match="exact"):
    req=urllib.request.Request(cdx_url(target,match),headers={"User-Agent":UA,"Accept":"application/json,*/*"})
    with urllib.request.urlopen(req,timeout=30) as r:
        body=r.read(3_000_001)
        if len(body)>3_000_000:
            raise ValueError("cdx-too-large")
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return body,()
    head=data[0]
    return body,tuple(dict(zip(head,row)) for row in data[1:] if isinstance(row,list))

def archived_image(row):
    from tools.stoneage_sa25_physical_image_fingerprint_probe import decode_features
    url=f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"
    st,final,h,body=fetch(url,accept="image/*,*/*",timeout=30,attempts=2,limit=MAX_BYTES)
    f=decode_features(body)
    f.update({
        "label":"wayback-official-reference",
        "url":final,
        "status":st,
        "bytes":len(body),
        "sha256":hashlib.sha256(body).hexdigest(),
    })
    return f

def main():
    print("StoneAge 2.5 Mainland collector-disc reference recovery — R1")
    print("SCOPE|public-collector+wayback-images-transient|derived-metadata+visual-metrics-only|no-image-commit")
    print(f"OFFICIAL_REFERENCE|{OFFICIAL_MAINLAND_REFERENCE}")
    errors=[]
    collector=[]

    try:
        page_rows,meta=collector_reference_images()
        for index,status,links in page_rows:
            print(f"COLLECTOR_INDEX|url={clean(index)}|status={clean(status)}|matched_links={len(links)}")
            for link in links:
                print(f"COLLECTOR_ARTICLE|index={clean(index)}|value={clean(link)}")
        print(f"COLLECTOR_IMAGE_TARGETS|count={len(meta)}")
        for row in meta:
            print(
                f"COLLECTOR_IMAGE_URL|label={clean(row.get('label'))}|article={clean(row.get('article'))}|"
                f"url={clean(row.get('url'))}|alt={clean(row.get('alt'))}|title={clean(row.get('title'))}"
            )
        for row in meta[:80]:
            try:
                f=load_image(row["label"],row["url"],referer=row.get("article"),timeout=15,attempts=1)
                if max(f["width"],f["height"])<300:
                    continue
                collector.append(f)
                print(
                    f"COLLECTOR_IMAGE|label={clean(f['label'])}|bytes={f['bytes']}|sha256={f['sha256']}|"
                    f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
                )
            except Exception as e:
                errors.append((row.get("label"),type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("collector-pages",type(e).__name__,str(e)))

    archive_refs=[]
    for label,target,match in (
        ("official-https",OFFICIAL_MAINLAND_REFERENCE,"exact"),
        ("official-http",OFFICIAL_HTTP,"exact"),
        ("official-filename-prefix",OFFICIAL_MAINLAND_REFERENCE.rsplit("/",1)[0]+"/5fe128952732d","prefix"),
    ):
        try:
            body,rows=cdx_fetch(target,match)
            print(
                f"CDX|label={label}|target={clean(target)}|match={match}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}"
            )
            for row in rows:
                print(
                    f"CDX_ROW|label={label}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|"
                    f"status={clean(row.get('statuscode'))}|mime={clean(row.get('mimetype'))}|"
                    f"length={clean(row.get('length'))}|digest={clean(row.get('digest'))}|redirect={clean(row.get('redirect'))}"
                )
                if str(row.get("statuscode") or "")=="200" and "image" in str(row.get("mimetype") or "").lower():
                    archive_refs.append(row)
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))

    archived=[]
    seen=set()
    for row in archive_refs:
        key=(row.get("timestamp"),row.get("original"))
        if key in seen:
            continue
        seen.add(key)
        try:
            f=archived_image(row)
            archived.append(f)
            print(
                f"ARCHIVE_IMAGE|timestamp={clean(row.get('timestamp'))}|bytes={f['bytes']}|sha256={f['sha256']}|"
                f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
            )
        except Exception as e:
            errors.append((f"replay:{row.get('timestamp')}",type(e).__name__,str(e)))

    ruten=[]
    try:
        for row in ruten_full_images():
            if str(row.get("carrier")) not in {"21926883918096","22242541948520"}:
                continue
            try:
                f=load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=15,attempts=1)
                ruten.append(f)
            except Exception as e:
                errors.append((row.get("label"),type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    rows=[]
    if archived:
        for a in archived:
            for c in collector:
                m=match_features(a,c)
                rows.append((m["inliers"],m["good"],"archive-vs-collector",a,c,m))
            for r in ruten:
                m=match_features(a,r)
                rows.append((m["inliers"],m["good"],"archive-vs-ruten",a,r,m))
    else:
        for r in ruten:
            for c in collector:
                m=match_features(r,c)
                rows.append((m["inliers"],m["good"],"ruten-vs-collector",r,c,m))
    rows.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for _,_,kind,left,right,m in rows[:80]:
        print(
            f"MATCH|kind={kind}|left={clean(left['label'])}|right={clean(right['label'])}|"
            f"orb_matches={m['matches']}|good_le64={m['good']}|ransac_inliers={m['inliers']}|"
            f"inlier_ratio={m['inlier_ratio']:.4f}|right_url={clean(right.get('url'))}"
        )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|collector_large_loaded|{len(collector)}")
    print(f"COUNT|archived_official_loaded|{len(archived)}")
    print(f"COUNT|ruten_standalone_loaded|{len(ruten)}")
    print(f"COUNT|errors|{len(errors)}")
    if archived:
        print("RESOLUTION|OFFICIAL_REFERENCE_ARCHIVE_RECOVERED|use archived hash/image features as visual carrier control only")
    elif collector:
        print("RESOLUTION|OFFICIAL_ARCHIVE_MISSING_BUT_COLLECTOR_MIRRORS_RECOVERED|rank collector images and seek exact mirrored reference")
    else:
        print("RESOLUTION|REFERENCE_IMAGE_SURFACE_UNRECOVERED|retain visual-reference gap")
    print(
        "EVIDENCE_BOUNDARY|collector/marketplace image similarity can classify artwork/source families only; "
        "it cannot establish disc bytes, mastering identity, filesystem contents, or clean-client provenance."
    )

if __name__=="__main__":
    main()
