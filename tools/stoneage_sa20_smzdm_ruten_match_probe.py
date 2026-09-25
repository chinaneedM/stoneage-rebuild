#!/usr/bin/env python3
"""Cross-check the source-mapped StoneAge 2.0 SMZDM disc photo against early Mainland carrier controls.

The 2016 SMZDM install-disc section maps photo #1 directly after the author's
statement that the first purchased package was the StoneAge 2.0 新手报到包.
This probe compares that exact public photo transiently with current public
Ruten early Mainland package/disc controls. Only derived hashes and SIFT/RANSAC
metrics are committed; no image or game payload is stored.
"""
from __future__ import annotations

from tools.stoneage_mainland_package_mirror_match_probe import ruten_meta, clean
from tools.stoneage_sa25_disc_region_match_probe import load_sift, sift_match

SMZDM_PAGE="https://post.smzdm.com/p/462347/"
SMZDM_20_IMAGE="https://am.zdmimg.com/201606/16/576276487bf54.jpg_e1080.jpg"
SMZDM_20_SHA256="98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3"
TARGET_CARRIERS={
    "22631284715652":"beijing-waei-newbie-control",
    "22636573895893":"mainland-retail-box",
    "22638643800877":"mainland-boxed-disc",
}

def main():
    print("StoneAge 2.0 SMZDM-to-Ruten physical-carrier visual cross-check — R2")
    print("SCOPE|source-mapped-2.0-disc-photo+public-early-mainland-controls|SIFT+RANSAC|transient-images|no-payload")
    print(f"REFERENCE|role=smzdm-2.0-newbie-disc|url={SMZDM_20_IMAGE}|expected_sha256={SMZDM_20_SHA256}")
    errors=[]
    try:
        ref=load_sift("smzdm:2.0:disc",SMZDM_20_IMAGE,referer=SMZDM_PAGE,scope="smzdm-2.0")
        print(
            f"REFERENCE_IMAGE|size={ref['width']}x{ref['height']}|sha256={ref['sha256']}|"
            f"keypoints={len(ref['kp'])}|hash_expected={int(ref['sha256']==SMZDM_20_SHA256)}"
        )
        if ref["sha256"]!=SMZDM_20_SHA256:
            errors.append(("smzdm-hash","HashMismatch",f"{ref['sha256']} != {SMZDM_20_SHA256}"))
    except Exception as e:
        ref=None
        errors.append(("smzdm-reference",type(e).__name__,str(e)))

    rows=[]
    try:
        meta=[r for r in ruten_meta() if str(r.get("carrier")) in TARGET_CARRIERS]
    except Exception as e:
        meta=[]
        errors.append(("ruten-meta",type(e).__name__,str(e)))

    loaded=[]
    for row in meta:
        try:
            q=load_sift(
                row["label"],row["url"],referer=row["referer"],
                carrier=row["carrier"],scope=row["scope"]
            )
            loaded.append(q)
            print(
                f"CONTROL|carrier={clean(q.get('carrier'))}|scope={clean(q.get('scope'))}|"
                f"label={clean(q['label'])}|size={q['width']}x{q['height']}|"
                f"sha256={q['sha256']}|keypoints={len(q['kp'])}|url={clean(q['url'])}"
            )
            if ref is not None:
                m=sift_match(q,ref)
                rows.append((m["inliers"],m["good"],m["query_coverage"],q,m))
        except Exception as e:
            errors.append((str(row.get("label")),type(e).__name__,str(e)))

    rows.sort(key=lambda z:(z[0],z[1],z[2]),reverse=True)
    for _,_,_,q,m in rows:
        print(
            f"MATCH|control={clean(q['label'])}|carrier={clean(q.get('carrier'))}|"
            f"scope={clean(q.get('scope'))}|good075={m['good']}|ransac_inliers={m['inliers']}|"
            f"inlier_ratio={m['inlier_ratio']:.4f}|query_coverage={m['query_coverage']:.4f}|"
            f"target_coverage={m['target_coverage']:.4f}|quad_ok={int(m['quad_ok'])}|"
            f"quad_area_ratio={m['quad_area_ratio']:.4f}"
        )

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|controls_loaded|{len(loaded)}")
    print(f"COUNT|pairs|{len(rows)}")
    print(f"COUNT|errors|{len(errors)}")
    if rows and rows[0][0] >= 80 and rows[0][4]["inlier_ratio"] >= 0.08:
        print("RESOLUTION|STRONG_VISUAL_FAMILY_CANDIDATE|inspect geometry and visible identifiers before any same-carrier inference")
    elif rows:
        print("RESOLUTION|NO_STRONG_VISUAL_CLOSURE|retain SMZDM photo as independent 2.0 physical-survival control only")
    else:
        print("RESOLUTION|VISUAL_CROSSCHECK_UNAVAILABLE|retain source-mapped 2.0 photo identity and retry only on new control")
    print("EVIDENCE_BOUNDARY|visual overlap cannot establish optical pressing, filesystem, installer build, same physical disc, or byte provenance.")

if __name__=="__main__":
    main()
