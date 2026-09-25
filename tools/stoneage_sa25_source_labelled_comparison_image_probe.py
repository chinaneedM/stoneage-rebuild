#!/usr/bin/env python3
"""Recover exact source-labelled StoneAge 2.5 Mainland/Taiwan comparison images.

Public image/archive bodies are read transiently. Only URLs, archive metadata,
hashes, dimensions and derived feature-match metrics are emitted. No image or
game payload body is retained.
"""
from __future__ import annotations

import hashlib
import json
import urllib.parse

from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    fetch,
    load_image,
    match_features,
    ruten_full_images,
)

TARGETS=(
    {
        "label":"blog-mainland-taiwan-25",
        "url":"https://shiqifabu.fszye.com/zb_users/upload/2020/12/20201222082537160859673711005.jpg",
        "referer":"https://blog.shiqi.so/shiqi273.htm",
    },
    {
        "label":"bahamut-mainland-taiwan-25",
        "url":"https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/5fe128b2e6b0a.jpg",
        "referer":"https://forum.gamer.com.tw/C.php?bsn=1571&snA=81429",
    },
)
WAYBACK_CDX="https://web.archive.org/cdx/search/cdx"
WAYBACK_RAW="https://web.archive.org/web/{timestamp}id_/{url}"

def clean(v,n=3500):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def cdx_url(url):
    q=urllib.parse.urlencode({
        "url":url,
        "output":"json",
        "fl":"timestamp,original,statuscode,mimetype,digest,length",
        "filter":["statuscode:200"],
        "collapse":"digest",
    },doseq=True)
    return WAYBACK_CDX+"?"+q

def parse_cdx(body):
    data=json.loads(body.decode("utf-8","replace"))
    if not isinstance(data,list) or not data:
        return ()
    header=[str(x) for x in data[0]]
    out=[]
    for row in data[1:]:
        if not isinstance(row,list):
            continue
        d={header[i]:row[i] if i<len(row) else "" for i in range(len(header))}
        out.append(d)
    return tuple(out)

def fetch_cdx(url):
    q=cdx_url(url)
    st,final,h,b=fetch(q,accept="application/json,*/*",timeout=35,attempts=2,limit=2_000_000)
    return st,final,b,parse_cdx(b)

def image_from_body(label,url,body):
    from tools.stoneage_sa25_physical_image_fingerprint_probe import decode_features
    f=decode_features(body)
    f.update({
        "label":label,
        "url":url,
        "bytes":len(body),
        "sha256":hashlib.sha256(body).hexdigest(),
    })
    return f

def transient_get_image(label,url,referer=None):
    st,final,h,b=fetch(
        url,accept="image/*,*/*",referer=referer,timeout=35,attempts=2,
        limit=12*1024*1024,
    )
    f=image_from_body(label,final,b)
    f["status"]=st
    f["content_type"]=h.get("Content-Type","")
    return f

def main():
    print("StoneAge 2.5 source-labelled comparison-image recovery probe — R1")
    print("SCOPE|exact-source-labelled-images|direct+Wayback-CDX/replay|transient-image-body|derived-metadata-only|no-image-commit")
    errors=[]
    recovered=[]
    for target in TARGETS:
        label=target["label"]; url=target["url"]; referer=target["referer"]
        print(f"TARGET|label={label}|url={clean(url)}|referer={clean(referer)}")
        try:
            f=transient_get_image(label+":direct",url,referer)
            recovered.append(f)
            print(f"DIRECT_IMAGE|label={label}|status={f['status']}|bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|dhash={f['dhash']}|url={clean(f['url'])}")
        except Exception as e:
            errors.append((label+":direct",type(e).__name__,str(e)))
            print(f"DIRECT_ERROR|label={label}|kind={type(e).__name__}|message={clean(e,1800)}")

        variants=tuple(dict.fromkeys([
            url,
            url.replace("https://","http://",1),
        ]))
        seen_digest=set()
        for variant in variants:
            try:
                st,final,b,rows=fetch_cdx(variant)
                print(f"CDX|label={label}|query={clean(variant)}|status={st}|bytes={len(b)}|rows={len(rows)}|sha256={hashlib.sha256(b).hexdigest()}")
                for i,row in enumerate(rows[:40],1):
                    print(f"CDX_ROW|label={label}|index={i}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|length={clean(row.get('length'))}")
                    digest=str(row.get("digest") or "")
                    if digest and digest in seen_digest:
                        continue
                    if digest: seen_digest.add(digest)
                    ts=str(row.get("timestamp") or "")
                    original=str(row.get("original") or variant)
                    if not ts:
                        continue
                    replay=WAYBACK_RAW.format(timestamp=ts,url=original)
                    try:
                        f=transient_get_image(label+f":wayback:{ts}",replay)
                        recovered.append(f)
                        print(f"WAYBACK_IMAGE|label={label}|timestamp={ts}|bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|dhash={f['dhash']}|url={clean(f['url'])}")
                    except Exception as e:
                        errors.append((label+f":wayback:{ts}",type(e).__name__,str(e)))
            except Exception as e:
                errors.append((label+":cdx:"+variant,type(e).__name__,str(e)))
                print(f"CDX_ERROR|label={label}|query={clean(variant)}|kind={type(e).__name__}|message={clean(e,1800)}")

    # Deduplicate recovered image bodies before comparison.
    uniq=[]; seen_hash=set()
    for f in recovered:
        if f["sha256"] in seen_hash: continue
        seen_hash.add(f["sha256"]); uniq.append(f)

    controls=[]
    try:
        for row in ruten_full_images():
            try:
                controls.append(load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=18,attempts=1))
            except Exception as e:
                errors.append((str(row.get("label")),type(e).__name__,str(e)))
    except Exception as e:
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    matches=[]
    for a in uniq:
        for b in controls:
            m=match_features(a,b)
            matches.append((m["inliers"],m["good"],a,b,m))
    matches.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for _,_,a,b,m in matches[:120]:
        print(f"MATCH|source={clean(a['label'])}|control={clean(b['label'])}|orb_matches={m['matches']}|good_le64={m['good']}|ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}|source_url={clean(a.get('url'))}|control_url={clean(b.get('url'))}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg,1800)}")
    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|unique_recovered_images|{len(uniq)}")
    print(f"COUNT|ruten_controls|{len(controls)}")
    print(f"COUNT|errors|{len(errors)}")
    if uniq:
        print("RESOLUTION|SOURCE_LABELLED_COMPARISON_IMAGE_RECOVERED|use source text + image body as visual carrier-family control only")
    else:
        print("RESOLUTION|SOURCE_LABELLED_COMPARISON_IMAGE_BODY_UNRECOVERED|retain exact URLs and source-text mapping; do not use sidebar images as substitutes")
    print("EVIDENCE_BOUNDARY|collector comparison imagery can distinguish artwork families but cannot establish pressing/mastering, disc bytes, filesystem contents, package-to-disc chain or clean-client provenance.")

if __name__=="__main__":
    main()
