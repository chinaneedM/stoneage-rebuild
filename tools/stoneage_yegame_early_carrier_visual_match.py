#!/usr/bin/env python3
"""Compare archived Yegame StoneAge product image with surviving early physical-carrier photos.

The exact archived Yegame image is source-bound to product code EN0ZGKJ0002.
This probe transiently compares that image against the existing public early
Ruten carrier set and emits only derived hashes/feature metrics. No image body
is committed and no seller interaction occurs.
"""
from __future__ import annotations

import json
import urllib.parse

from tools.stoneage_ruten_early_carrier_probe import TARGETS, DETAIL, detail_rows, image_urls
from tools.stoneage_sa25_physical_image_fingerprint_probe import fetch, load_image, match_features, hamming_hex, clean

YEGAME_TS="20010828031151"
YEGAME_ORIG="http://yegame.com:80/product_images/EN0ZGKJ0002.jpg"
YEGAME_URL=f"https://web.archive.org/web/{YEGAME_TS}id_/{YEGAME_ORIG}"

def ruten_images():
    out=[]
    for pid,role in TARGETS:
        q=urllib.parse.urlencode({"gno":pid,"level":"simple"})
        st,final,h,b=fetch(DETAIL+"?"+q,accept="application/json,*/*",referer="https://www.ruten.com.tw/",timeout=25,attempts=2)
        data=json.loads(b.decode("utf-8","replace"))
        for row in detail_rows(data):
            for idx,url in enumerate(image_urls(row)):
                out.append({"label":f"ruten:{pid}:{idx}","carrier":pid,"role":role,"url":url})
    return out

def main():
    print("StoneAge Yegame EN0ZGKJ0002 vs early physical carriers — R1")
    print("SCOPE|archived-source-image-vs-public-carrier-images|derived-visual-metrics-only|no-image-commit|no-login|no-contact")
    print(f"YEGAME|timestamp={YEGAME_TS}|product_code=EN0ZGKJ0002|url={YEGAME_URL}")
    errors=[]

    try:
        y=load_image("yegame:EN0ZGKJ0002",YEGAME_URL,timeout=45,attempts=3)
        print(f"REFERENCE|label={y['label']}|bytes={y['bytes']}|sha256={y['sha256']}|size={y['width']}x{y['height']}|dhash={y['dhash']}|keypoints={len(y['kp'])}|url={clean(y['url'])}")
    except Exception as e:
        print(f"ERROR|scope=yegame-reference|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|YEGAME_REFERENCE_UNAVAILABLE|retry exact archived image only")
        return

    try:
        meta=ruten_images()
    except Exception as e:
        meta=[]
        errors.append(("ruten-metadata",type(e).__name__,str(e)))

    loaded=[]
    for row in meta:
        try:
            f=load_image(row["label"],row["url"],referer="https://www.ruten.com.tw/",timeout=25,attempts=2)
            f["carrier"]=row["carrier"]; f["role"]=row["role"]
            loaded.append(f)
            print(f"QUERY|label={clean(f['label'])}|carrier={clean(f['carrier'])}|role={clean(f['role'])}|bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}")
        except Exception as e:
            errors.append((row["label"],type(e).__name__,str(e)))

    rows=[]
    for f in loaded:
        m=match_features(y,f)
        rows.append((m["inliers"],m["good"],-hamming_hex(y["dhash"],f["dhash"]),f,m))
    rows.sort(key=lambda z:(z[0],z[1],z[2]),reverse=True)

    for _,_,_,f,m in rows:
        med="" if m["median"] is None else f"{m['median']:.1f}"
        print(
            f"MATCH|carrier={clean(f['carrier'])}|role={clean(f['role'])}|target={clean(f['label'])}|"
            f"dhash_hamming={hamming_hex(y['dhash'],f['dhash'])}|orb_matches={m['matches']}|good_le64={m['good']}|"
            f"median_top50={med}|ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}"
        )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|carrier_images={len(loaded)}")
    print(f"COUNT|pairs={len(rows)}")
    print(f"COUNT|errors={len(errors)}")

    strong=[(f,m) for _,_,_,f,m in rows if m["inliers"]>=12 and m["inlier_ratio"]>=0.25]
    if strong:
        print("RESOLUTION|YEGAME_PRODUCT_IMAGE_CARRIER_MATCH_CANDIDATE|inspect matched carrier identifiers/disc photos before provenance upgrade")
        for f,m in strong[:8]:
            print(f"STRONG|carrier={clean(f['carrier'])}|role={clean(f['role'])}|target={clean(f['label'])}|inliers={m['inliers']}|ratio={m['inlier_ratio']:.4f}")
    elif rows:
        print("RESOLUTION|NO_STRONG_YEGAME_CARRIER_MATCH|do not infer physical non-identity; archived image is small/cropped")
    else:
        print("RESOLUTION|NO_COMPARABLE_CARRIER_IMAGES")

    print("EVIDENCE_BOUNDARY|Visual similarity can bind artwork/carrier hypotheses only; it cannot establish disc-byte identity or clean-client status.")

if __name__=="__main__":
    main()
