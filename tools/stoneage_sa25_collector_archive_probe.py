#!/usr/bin/env python3
"""Recover archived copies of dead StoneAge 2.5 collector-reference images.

Known collector article image URLs only. Image bodies are read transiently from
Wayback; the report stores URLs, hashes, dimensions and visual match metrics only.
"""
from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request

from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    collector_reference_images, decode_features, fetch, load_image,
    match_features, ruten_full_images,
)

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
MAX_BYTES=12*1024*1024

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def cdx_url(target):
    return CDX+"?"+urllib.parse.urlencode([
        ("url",target),("matchType","exact"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","2016"),("to","2026"),("limit","1000"),
    ])

def cdx_fetch(target):
    req=urllib.request.Request(cdx_url(target),headers={"User-Agent":UA,"Accept":"application/json,*/*"})
    with urllib.request.urlopen(req,timeout=30) as r:
        body=r.read(3_000_001)
        if len(body)>3_000_000:
            raise ValueError("cdx-too-large")
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return body,()
    head=data[0]
    return body,tuple(dict(zip(head,row)) for row in data[1:] if isinstance(row,list))

def archived_image(row,label):
    url=f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"
    st,final,h,body=fetch(url,accept="image/*,*/*",timeout=30,attempts=2,limit=MAX_BYTES)
    f=decode_features(body)
    f.update({
        "label":label,
        "url":final,
        "status":st,
        "bytes":len(body),
        "sha256":hashlib.sha256(body).hexdigest(),
    })
    return f

def main():
    print("StoneAge 2.5 collector-image Wayback recovery — R1")
    print("SCOPE|known-collector-image-urls|wayback-exact-replay-transient|derived-metadata-only|no-image-commit")
    errors=[]
    page_rows,meta=collector_reference_images()
    print(f"TARGETS|count={len(meta)}")
    recovered=[]
    for row in meta:
        label=str(row.get("label") or "")
        target=str(row.get("url") or "")
        try:
            body,rows=cdx_fetch(target)
            ok=[r for r in rows if str(r.get("statuscode") or "")=="200" and "image" in str(r.get("mimetype") or "").lower()]
            print(
                f"CDX|label={clean(label)}|target={clean(target)}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|image200={len(ok)}"
            )
            for r in rows[:40]:
                print(
                    f"CDX_ROW|label={clean(label)}|timestamp={clean(r.get('timestamp'))}|"
                    f"status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|"
                    f"length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}"
                )
            seen_digest=set()
            for r in ok:
                dg=str(r.get("digest") or "")
                if dg and dg in seen_digest:
                    continue
                if dg:
                    seen_digest.add(dg)
                try:
                    f=archived_image(r,f"archive:{label}:{r.get('timestamp')}")
                    recovered.append(f)
                    print(
                        f"ARCHIVE_IMAGE|source_label={clean(label)}|timestamp={clean(r.get('timestamp'))}|"
                        f"bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|"
                        f"dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
                    )
                except Exception as e:
                    errors.append((f"replay:{label}:{r.get('timestamp')}",type(e).__name__,str(e)))
                if len(seen_digest)>=3:
                    break
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))

    ruten=[]
    try:
        for row in ruten_full_images():
            if str(row.get("carrier")) not in {"22632305238624","21926883918096","22242541948520"}:
                continue
            try:
                f=load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=15,attempts=1)
                ruten.append(f)
            except Exception as e:
                errors.append((row.get("label"),type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    matches=[]
    for a in recovered:
        for r in ruten:
            m=match_features(a,r)
            matches.append((m["inliers"],m["good"],a,r,m))
    matches.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for _,_,a,r,m in matches[:100]:
        print(
            f"MATCH|archive={clean(a['label'])}|ruten={clean(r['label'])}|"
            f"orb_matches={m['matches']}|good_le64={m['good']}|ransac_inliers={m['inliers']}|"
            f"inlier_ratio={m['inlier_ratio']:.4f}|archive_url={clean(a.get('url'))}|ruten_url={clean(r.get('url'))}"
        )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|archive_images_recovered|{len(recovered)}")
    print(f"COUNT|ruten_images_loaded|{len(ruten)}")
    print(f"COUNT|match_pairs|{len(matches)}")
    print(f"COUNT|errors|{len(errors)}")
    if recovered:
        print("RESOLUTION|COLLECTOR_ARCHIVE_IMAGES_RECOVERED|inspect high-confidence visual matches and visible carrier identity")
    else:
        print("RESOLUTION|COLLECTOR_ARCHIVE_IMAGE_ROUTE_BOUNDED|no archived image bodies recovered from known URLs")
    print("EVIDENCE_BOUNDARY|archived collector photographs can support physical-carrier/artwork identity only; they cannot prove disc filesystem or byte provenance.")

if __name__=="__main__":
    main()
