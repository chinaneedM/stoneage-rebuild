#!/usr/bin/env python3
"""Crop/region-aware visual comparison for surviving StoneAge 2.5 physical media.

The probe reads public marketplace/collector image bodies transiently in CI and emits
only derived SIFT/RANSAC geometry. It stores no seller/collector image bytes and makes
no purchase, login, message, or payload request.
"""
from __future__ import annotations

import hashlib
import math
import urllib.parse

from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    MAX_IMAGE_BYTES,
    WANFANG_PAGE,
    collector_reference_images,
    fetch,
    is_thumbnail,
    ruten_full_images,
    wanfang_page_images,
)

STANDALONE = {"21926883918096", "22242541948520", "22637629794063"}
BOXED = "22632305238624"


def clean(v, n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]


def bbox_coverage(points, width, height):
    """Normalized axis-aligned coverage for a sequence of (x, y) points."""
    if not points or width <= 0 or height <= 0:
        return 0.0
    xs = [float(p[0]) for p in points]
    ys = [float(p[1]) for p in points]
    if len(xs) < 2:
        return 0.0
    area = max(0.0, max(xs) - min(xs)) * max(0.0, max(ys) - min(ys))
    return min(1.0, area / float(width * height))


def polygon_area(points):
    """Shoelace area for a polygon represented as [(x, y), ...]."""
    if len(points) < 3:
        return 0.0
    total = 0.0
    for i, (x1, y1) in enumerate(points):
        x2, y2 = points[(i + 1) % len(points)]
        total += float(x1) * float(y2) - float(x2) * float(y1)
    return abs(total) * 0.5


def sane_quad(points, width, height):
    if len(points) != 4 or width <= 0 or height <= 0:
        return False, 0.0
    if any(not (math.isfinite(float(x)) and math.isfinite(float(y))) for x, y in points):
        return False, 0.0
    area = polygon_area(points)
    norm = area / float(width * height)
    # Permit partial off-frame projections but reject degenerate/exploded homographies.
    coord_limit = 3.0 * max(width, height)
    sane_coords = all(abs(float(x)) <= coord_limit and abs(float(y)) <= coord_limit for x, y in points)
    return sane_coords and 0.0005 <= norm <= 2.5, norm


def load_sift(label, url, *, referer=None, carrier="", scope=""):
    import cv2
    import numpy as np

    st, final, h, body = fetch(
        url,
        accept="image/*,*/*",
        referer=referer,
        limit=MAX_IMAGE_BYTES,
        timeout=15,
        attempts=1,
    )
    arr = np.frombuffer(body, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("unsupported image body")
    height, width = img.shape[:2]
    max_dim = 1800
    scale = min(1.0, max_dim / float(max(width, height)))
    work = img
    if scale < 1.0:
        work = cv2.resize(
            img,
            (max(1, int(width * scale)), max(1, int(height * scale))),
            interpolation=cv2.INTER_AREA,
        )
    wh, ww = work.shape[:2]
    sift = cv2.SIFT_create(nfeatures=8000, contrastThreshold=0.02, edgeThreshold=14)
    kp, des = sift.detectAndCompute(work, None)
    return {
        "label": label,
        "scope": scope,
        "carrier": carrier,
        "url": final,
        "status": st,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "width": ww,
        "height": wh,
        "kp": kp or [],
        "des": des,
    }


def sift_match(query, target):
    import cv2
    import numpy as np

    dq, dt = query.get("des"), target.get("des")
    if dq is None or dt is None or len(dq) < 8 or len(dt) < 8:
        return {
            "knn": 0,
            "good": 0,
            "inliers": 0,
            "inlier_ratio": 0.0,
            "query_coverage": 0.0,
            "target_coverage": 0.0,
            "quad_ok": False,
            "quad_area_ratio": 0.0,
        }

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    pairs = matcher.knnMatch(dq, dt, k=2)
    good = []
    for pair in pairs:
        if len(pair) != 2:
            continue
        m, n = pair
        if m.distance < 0.75 * n.distance:
            good.append(m)

    inliers = 0
    qcov = 0.0
    tcov = 0.0
    quad_ok = False
    quad_ratio = 0.0
    if len(good) >= 6:
        src = np.float32([query["kp"][m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([target["kp"][m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        if mask is not None:
            mask1 = mask.ravel().astype(bool)
            inliers = int(mask1.sum())
            qpts = [tuple(p[0]) for p, keep in zip(src, mask1) if keep]
            tpts = [tuple(p[0]) for p, keep in zip(dst, mask1) if keep]
            qcov = bbox_coverage(qpts, query["width"], query["height"])
            tcov = bbox_coverage(tpts, target["width"], target["height"])
        if H is not None:
            corners = np.float32(
                [[0, 0], [query["width"] - 1, 0], [query["width"] - 1, query["height"] - 1], [0, query["height"] - 1]]
            ).reshape(-1, 1, 2)
            projected = cv2.perspectiveTransform(corners, H).reshape(-1, 2)
            points = [(float(x), float(y)) for x, y in projected]
            quad_ok, quad_ratio = sane_quad(points, target["width"], target["height"])

    return {
        "knn": len(pairs),
        "good": len(good),
        "inliers": inliers,
        "inlier_ratio": inliers / len(good) if good else 0.0,
        "query_coverage": qcov,
        "target_coverage": tcov,
        "quad_ok": quad_ok,
        "quad_area_ratio": quad_ratio,
    }


def main():
    print("StoneAge 2.5 physical-disc local-region match probe — R1")
    print("SCOPE|public-images-transient|SIFT+RANSAC-derived-metrics-only|no-login|no-purchase|no-image-commit")
    errors = []

    ruten_meta = ruten_full_images()
    query_meta = [x for x in ruten_meta if str(x.get("carrier")) in STANDALONE]
    boxed_meta = [x for x in ruten_meta if str(x.get("carrier")) == BOXED]

    try:
        _, _, wan_meta = wanfang_page_images()
    except Exception as e:
        wan_meta = []
        errors.append(("wanfang-page", type(e).__name__, str(e)))

    try:
        collector_pages, collector_meta = collector_reference_images()
        for index_url, status, links in collector_pages:
            print(f"COLLECTOR_INDEX|url={clean(index_url)}|status={clean(status)}|matched_links={len(links)}")
    except Exception as e:
        collector_meta = []
        errors.append(("collector-pages", type(e).__name__, str(e)))

    queries = []
    targets = []

    for row in query_meta:
        try:
            f = load_sift(
                row["label"],
                row["url"],
                referer="https://www.ruten.com.tw/",
                carrier=str(row.get("carrier") or ""),
                scope="ruten-standalone",
            )
            queries.append(f)
            print(
                f"IMAGE|scope={f['scope']}|label={clean(f['label'])}|carrier={clean(f['carrier'])}|"
                f"size={f['width']}x{f['height']}|keypoints={len(f['kp'])}|sha256={f['sha256']}"
            )
        except Exception as e:
            errors.append((row["label"], type(e).__name__, str(e)))

    for row in boxed_meta:
        try:
            f = load_sift(
                row["label"],
                row["url"],
                referer="https://www.ruten.com.tw/",
                carrier=BOXED,
                scope="ruten-boxed",
            )
            targets.append(f)
        except Exception as e:
            errors.append((row["label"], type(e).__name__, str(e)))

    for row in wan_meta[:60]:
        try:
            f = load_sift(
                row["label"],
                row["url"],
                referer=WANFANG_PAGE,
                scope="wanfang",
            )
            if max(f["width"], f["height"]) >= 300:
                targets.append(f)
        except Exception as e:
            errors.append((row["label"], type(e).__name__, str(e)))

    for row in collector_meta[:80]:
        try:
            f = load_sift(
                row["label"],
                row["url"],
                referer=row.get("article"),
                scope="collector",
            )
            if max(f["width"], f["height"]) >= 300:
                targets.append(f)
        except Exception as e:
            errors.append((row["label"], type(e).__name__, str(e)))

    # Add standalone-to-standalone as an internal positive-control relation.
    for q in queries:
        for t in queries:
            if q["label"] >= t["label"]:
                continue
            targets.append({
                **t,
                "label": "control:" + t["label"],
                "scope": "standalone-control",
            })

    rows = []
    for q in queries:
        for t in targets:
            if t["scope"] == "standalone-control" and t["carrier"] == q["carrier"]:
                continue
            m = sift_match(q, t)
            rows.append((m["inliers"], m["good"], m["query_coverage"], q, t, m))

    rows.sort(key=lambda z: (z[0], z[1], z[2]), reverse=True)
    print(f"COUNT|queries|{len(queries)}")
    print(f"COUNT|targets|{len(targets)}")
    print(f"COUNT|pairs|{len(rows)}")
    for _, _, _, q, t, m in rows[:120]:
        print(
            f"MATCH|query={clean(q['label'])}|query_carrier={clean(q.get('carrier'))}|"
            f"target_scope={clean(t['scope'])}|target={clean(t['label'])}|"
            f"target_carrier={clean(t.get('carrier'))}|knn={m['knn']}|good075={m['good']}|"
            f"ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}|"
            f"query_coverage={m['query_coverage']:.4f}|target_coverage={m['target_coverage']:.4f}|"
            f"quad_ok={int(m['quad_ok'])}|quad_area_ratio={m['quad_area_ratio']:.4f}"
        )

    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if rows:
        print("RESOLUTION|LOCAL_REGION_METRICS_AVAILABLE|interpret against standalone positive control; do not infer byte identity")
    else:
        print("RESOLUTION|NO_LOCAL_REGION_PAIRS|do not infer visual non-match")
    print(
        "EVIDENCE_BOUNDARY|local visual homography can support shared artwork/source-family hypotheses only; "
        "it cannot establish disc contents, mastering identity, official provenance, or clean-client status."
    )


if __name__ == "__main__":
    main()
