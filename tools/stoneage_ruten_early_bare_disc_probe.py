#!/usr/bin/env python3
"""Probe a surviving early StoneAge bare-disc listing and compare carrier artwork.

Target:
- Ruten public item 22111215616086, indexed as a Waei StoneAge/STONEAGE
  Chinese PC online-game disc with one public disc-face image.

Method:
- read public Ruten JSON metadata only;
- transiently fetch public images;
- compare target image(s) against already tracked early carrier controls:
  Taiwan v1.0-style client box, Beijing-Waei newbie control, Mainland retail box;
- emit hashes and derived ORB/RANSAC metrics only.

No login, purchase, seller contact, personal data extraction, or image persistence.
"""
from __future__ import annotations

import json
import urllib.parse

from tools.stoneage_ruten_early_carrier_probe import DETAIL, detail_rows, image_urls
from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    clean,
    fetch,
    hamming_hex,
    load_image,
    match_features,
)

TARGET=("22111215616086","early-bare-disc")
CONTROLS=(
    ("22625938996449","taiwan-client-box"),
    ("22631284715652","beijing-waei-newbie-control"),
    ("22636573895893","mainland-retail-box"),
)

def item_rows(pid, level="simple"):
    q=urllib.parse.urlencode({"gno":pid,"level":level})
    st,final,h,b=fetch(
        DETAIL+"?"+q,
        accept="application/json,*/*",
        referer="https://www.ruten.com.tw/",
        timeout=30,
        attempts=3,
    )
    data=json.loads(b.decode("utf-8","replace"))
    return st,final,b,detail_rows(data)

def public_identity(row):
    return {
        "name":row.get("name"),
        "images":image_urls(row),
        "post_time":row.get("post_time"),
        "sold_num":row.get("sold_num"),
        "num":row.get("num"),
    }

def load_public_images(pid,role,rows):
    out=[]
    for row in rows:
        for idx,url in enumerate(image_urls(row)):
            f=load_image(
                f"ruten:{pid}:{idx}",
                url,
                referer="https://www.ruten.com.tw/",
                timeout=30,
                attempts=3,
            )
            f["carrier"]=pid
            f["role"]=role
            out.append(f)
    return out

def main():
    print("StoneAge early bare-disc public carrier probe — R1")
    print("SCOPE|public-ruten-json+transient-images|derived-metadata+visual-metrics-only|no-login|no-purchase|no-contact|no-image-commit")
    print(f"TARGET|id={TARGET[0]}|role={TARGET[1]}")
    errors=[]

    try:
        st,final,b,rows=item_rows(TARGET[0],"simple")
        print(f"DETAIL|id={TARGET[0]}|role={TARGET[1]}|status={st}|bytes={len(b)}|rows={len(rows)}|final={clean(final)}")
        for row in rows:
            ident=public_identity(row)
            print(
                f"ITEM|id={TARGET[0]}|role={TARGET[1]}|name={clean(ident['name'])}|"
                f"post_time={clean(ident['post_time'])}|sold={clean(ident['sold_num'])}|"
                f"stock={clean(ident['num'])}|image_count={len(ident['images'])}"
            )
        target_images=load_public_images(TARGET[0],TARGET[1],rows)
    except Exception as e:
        target_images=[]
        errors.append((TARGET[0],"target",type(e).__name__,str(e)))

    controls=[]
    for pid,role in CONTROLS:
        try:
            st,final,b,rows=item_rows(pid,"simple")
            print(f"CONTROL_DETAIL|id={pid}|role={role}|status={st}|bytes={len(b)}|rows={len(rows)}|final={clean(final)}")
            controls.extend(load_public_images(pid,role,rows))
        except Exception as e:
            errors.append((pid,"control",type(e).__name__,str(e)))

    for f in target_images:
        print(
            f"TARGET_IMAGE|label={clean(f['label'])}|bytes={f['bytes']}|sha256={f['sha256']}|"
            f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
        )
    for f in controls:
        print(
            f"CONTROL_IMAGE|label={clean(f['label'])}|carrier={clean(f['carrier'])}|role={clean(f['role'])}|"
            f"bytes={f['bytes']}|sha256={f['sha256']}|size={f['width']}x{f['height']}|"
            f"dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
        )

    pairs=[]
    for t in target_images:
        for c in controls:
            m=match_features(t,c)
            pairs.append((m["inliers"],m["good"],-hamming_hex(t["dhash"],c["dhash"]),t,c,m))
    pairs.sort(key=lambda z:(z[0],z[1],z[2]),reverse=True)

    for _,_,_,t,c,m in pairs[:80]:
        med="" if m["median"] is None else f"{m['median']:.1f}"
        print(
            f"MATCH|target={clean(t['label'])}|control={clean(c['label'])}|control_carrier={clean(c['carrier'])}|"
            f"control_role={clean(c['role'])}|dhash_hamming={hamming_hex(t['dhash'],c['dhash'])}|"
            f"orb_matches={m['matches']}|good_le64={m['good']}|median_top50={med}|"
            f"ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}"
        )

    for pid,scope,kind,msg in errors:
        print(f"ERROR|id={clean(pid)}|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|target_images={len(target_images)}")
    print(f"COUNT|control_images={len(controls)}")
    print(f"COUNT|pairs={len(pairs)}")
    print(f"COUNT|errors={len(errors)}")

    strong=[(c,m) for _,_,_,_,c,m in pairs if m["inliers"]>=20 and m["inlier_ratio"]>=0.20]
    if strong:
        print("RESOLUTION|BARE_DISC_CARRIER_FAMILY_MATCH_CANDIDATE|inspect top control role and disc-side identifiers before provenance upgrade")
        for c,m in strong[:10]:
            print(
                f"STRONG|control_carrier={clean(c['carrier'])}|control_role={clean(c['role'])}|"
                f"control={clean(c['label'])}|inliers={m['inliers']}|ratio={m['inlier_ratio']:.4f}"
            )
    elif target_images:
        print("RESOLUTION|BARE_DISC_IMAGE_RECOVERED_NO_STRONG_CONTROL_MATCH|retain as independent early physical carrier")
    else:
        print("RESOLUTION|BARE_DISC_TARGET_UNAVAILABLE|retry exact public item only")

    print("EVIDENCE_BOUNDARY|Marketplace titles and artwork are carrier evidence only; visual similarity cannot establish disc-byte identity, version, release date, or clean-client status.")

if __name__=="__main__":
    main()
