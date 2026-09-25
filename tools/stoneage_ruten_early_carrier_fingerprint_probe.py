#!/usr/bin/env python3
"""Transient visual deduplication for early StoneAge Ruten carrier photographs.

Uses only public listing images. Image bodies are transient in CI; repository
output contains only hashes/features and cross-listing match metrics.
"""
from __future__ import annotations

import hashlib
import json
import urllib.parse

from tools.stoneage_ruten_early_carrier_probe import (
    DETAIL, TARGETS, detail_rows, fetch, image_urls, clean
)
from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    decode_features, hamming_hex, match_features
)

def metadata():
    out=[]
    for pid,role in TARGETS:
        q=urllib.parse.urlencode({"gno":pid,"level":"simple"})
        st,final,h,b=fetch(DETAIL+"?"+q,accept="application/json,*/*")
        data=json.loads(b.decode("utf-8","replace"))
        for row in detail_rows(data):
            for idx,url in enumerate(image_urls(row)):
                out.append({"id":pid,"role":role,"index":idx,"url":url})
    return out

def main():
    print("StoneAge early Ruten carrier transient visual fingerprint — R1")
    print("SCOPE|public-image-read-transient|derived-metrics-only|cross-listing-dedup|no-image-commit")
    errors=[]; loaded=[]
    for row in metadata():
        try:
            st,final,h,b=fetch(row["url"],accept="image/*,*/*",limit=12*1024*1024)
            f=decode_features(b)
            f.update(row)
            f["sha256"]=hashlib.sha256(b).hexdigest()
            loaded.append(f)
            print(
                f"IMAGE|id={row['id']}|role={row['role']}|index={row['index']}|bytes={len(b)}|"
                f"sha256={f['sha256']}|size={f['width']}x{f['height']}|dhash={f['dhash']}|"
                f"keypoints={len(f['kp'])}|url={clean(final,5000)}"
            )
        except Exception as e:
            errors.append((row["id"],row["index"],type(e).__name__,str(e)))
    pairs=[]
    for i,a in enumerate(loaded):
        for b in loaded[i+1:]:
            if a["id"]==b["id"]:
                continue
            m=match_features(a,b)
            pairs.append((m["inliers"],m["good"],-hamming_hex(a["dhash"],b["dhash"]),a,b,m))
    pairs.sort(key=lambda x:(x[0],x[1],x[2]),reverse=True)
    print(f"PAIR_COUNT|{len(pairs)}")
    for _,_,_,a,b,m in pairs[:100]:
        print(
            f"MATCH|left={a['id']}:{a['index']}|left_role={a['role']}|"
            f"right={b['id']}:{b['index']}|right_role={b['role']}|"
            f"dhash_hamming={hamming_hex(a['dhash'],b['dhash'])}|orb_matches={m['matches']}|"
            f"good_le64={m['good']}|ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}"
        )
    for pid,idx,kind,msg in errors:
        print(f"ERROR|id={pid}|index={idx}|kind={kind}|message={clean(msg)}")
    print(f"COUNT|loaded|{len(loaded)}")
    print(f"COUNT|errors|{len(errors)}")
    if pairs:
        print("RESOLUTION|EARLY_CARRIER_VISUAL_METRICS_AVAILABLE|deduplicate photograph families before counting independent carrier evidence")
    else:
        print("RESOLUTION|NO_CROSS_LISTING_PAIRS|do not infer visual independence")
    print("EVIDENCE_BOUNDARY|visual similarity can identify reused photographs or shared artwork families; it cannot establish same physical carrier, pressing, mastering, client contents, or release version.")

if __name__=="__main__":
    main()
