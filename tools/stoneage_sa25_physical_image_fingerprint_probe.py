#!/usr/bin/env python3
"""Transient visual-fingerprint probe for surviving StoneAge 2.5 physical media.

Reads public image bodies only during the CI run and emits derived hashes/features.
No seller image bytes, game payload bytes, login, purchase, or messaging are persisted.
"""
from __future__ import annotations

import hashlib
import html.parser
import json
import ssl
import statistics
import time
import urllib.parse
import urllib.request

from tools.stoneage_sa25_ruten_physical_probe import IDS, DETAIL, detail_rows, image_urls

UA = "stoneage-rebuild-archaeology/1.0"
OFFICIAL_MAINLAND_REFERENCE = (
    "https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/"
    "5fe128952732d.jpg"
)
WANFANG_PAGE = "https://www.shiqi.me/pt_17.htm"
COLLECTOR_INDEXES = (
    ("https://blog.shiqi.so/author1.htm", ("回忆石器时代2.5游戏光盘",)),
    ("https://www.soshiqi.com/category-sqxc.html", ("2.5客户端礼包精灵王传说版", "2.5精灵王传说版用戶端產包")),
)
INSECURE_TLS_HOSTS = {"www.shiqi.me", "shiqi.me", "blog.shiqi.so", "www.soshiqi.com", "soshiqi.com"}
MAX_IMAGE_BYTES = 12 * 1024 * 1024


def clean(v, n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]


class ImageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.links = []
        self._anchor = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag.lower() == "a" and d.get("href"):
            self._anchor = {"href": d.get("href"), "text": []}
        if tag.lower() != "img":
            return
        for key in ("src", "data-src", "data-original", "data-lazy-src"):
            u = d.get(key)
            if u:
                self.rows.append(
                    {
                        "url": u,
                        "alt": d.get("alt", ""),
                        "title": d.get("title", ""),
                    }
                )

    def handle_data(self, data):
        if self._anchor is not None:
            self._anchor["text"].append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._anchor is not None:
            self.links.append({
                "href": self._anchor["href"],
                "text": " ".join("".join(self._anchor["text"]).split()),
            })
            self._anchor = None


def insecure_tls_allowed(url):
    return urllib.parse.urlsplit(url).hostname in INSECURE_TLS_HOSTS


def fetch(url, *, accept="*/*", referer=None, timeout=35, attempts=3, limit=None):
    last = None
    for i in range(attempts):
        try:
            headers = {"User-Agent": UA, "Accept": accept}
            if referer:
                headers["Referer"] = referer
            req = urllib.request.Request(url, headers=headers)
            ctx = ssl._create_unverified_context() if insecure_tls_allowed(url) else None
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                if limit is None:
                    body = r.read()
                else:
                    body = r.read(limit + 1)
                    if len(body) > limit:
                        raise ValueError(f"body exceeds limit {limit}")
                return int(getattr(r, "status", r.getcode())), r.geturl(), dict(r.headers.items()), body
        except Exception as e:
            last = e
            if i + 1 < attempts:
                time.sleep(2 * (i + 1))
    raise last


def json_fetch(url):
    st, final, h, b = fetch(url, accept="application/json,*/*", referer="https://www.ruten.com.tw/")
    return st, final, h, b, json.loads(b.decode("utf-8", "replace"))


def is_thumbnail(url):
    path = urllib.parse.urlsplit(url).path.lower()
    stem = path.rsplit("/", 1)[-1]
    return "_m." in stem or stem.endswith("_m")


def normalize_image_url(base, url):
    if not url:
        return ""
    return urllib.parse.urljoin(base, str(url).strip())


def ruten_full_images():
    out = []
    seen = set()
    for pid in IDS:
        q = urllib.parse.urlencode({"gno": pid, "level": "simple"})
        _, _, _, _, data = json_fetch(DETAIL + "?" + q)
        for row in detail_rows(data):
            for idx, url in enumerate(image_urls(row)):
                if is_thumbnail(url):
                    continue
                key = (pid, url)
                if key in seen:
                    continue
                seen.add(key)
                out.append({"label": f"ruten:{pid}:{idx}", "url": url, "carrier": pid})
    return out


def wanfang_page_images():
    st, final, h, body = fetch(WANFANG_PAGE, accept="text/html,*/*")
    p = ImageParser()
    p.feed(body.decode("utf-8", "replace"))
    out = []
    seen = set()
    for i, row in enumerate(p.rows):
        u = normalize_image_url(final, row["url"])
        if not u.startswith(("http://", "https://")):
            continue
        path = urllib.parse.urlsplit(u).path.lower()
        if not any(path.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif")):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append(
            {
                "label": f"wanfang-page:{i}",
                "url": u,
                "alt": row.get("alt", ""),
                "title": row.get("title", ""),
            }
        )
    return st, final, out


def collector_reference_images():
    """Resolve mirrored collector article pages and return their public image candidates."""
    out = []
    seen = set()
    page_rows = []
    for index_url, needles in COLLECTOR_INDEXES:
        try:
            st, final, h, body = fetch(index_url, accept="text/html,*/*")
            p = ImageParser()
            p.feed(body.decode("utf-8", "replace"))
            links = []
            for row in p.links:
                text = row.get("text", "")
                if any(n in text for n in needles):
                    links.append(normalize_image_url(final, row.get("href")))
            page_rows.append((index_url, st, tuple(links)))
            for article_url in links[:6]:
                ast, afinal, ah, abody = fetch(article_url, accept="text/html,*/*", referer=index_url)
                ap = ImageParser()
                ap.feed(abody.decode("utf-8", "replace"))
                for i, img in enumerate(ap.rows):
                    u = normalize_image_url(afinal, img.get("url"))
                    if not u.startswith(("http://", "https://")) or u in seen:
                        continue
                    path = urllib.parse.urlsplit(u).path.lower()
                    if not any(path.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif")):
                        continue
                    seen.add(u)
                    out.append({
                        "label": f"collector-mirror:{len(out)}",
                        "url": u,
                        "article": afinal,
                        "alt": img.get("alt", ""),
                        "title": img.get("title", ""),
                    })
        except Exception as e:
            page_rows.append((index_url, "ERROR", (type(e).__name__ + ":" + str(e),)))
    return page_rows, out


def decode_features(body):
    import cv2
    import numpy as np

    arr = np.frombuffer(body, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("unsupported image body")
    h, w = img.shape[:2]
    max_dim = 1800
    scale = min(1.0, max_dim / float(max(h, w)))
    work = img
    if scale < 1.0:
        work = cv2.resize(
            img,
            (max(1, int(w * scale)), max(1, int(h * scale))),
            interpolation=cv2.INTER_AREA,
        )
    gray = cv2.cvtColor(work, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (9, 8), interpolation=cv2.INTER_AREA)
    bits = (small[:, 1:] > small[:, :-1]).flatten()
    dhash = 0
    for bit in bits:
        dhash = (dhash << 1) | int(bool(bit))
    orb = cv2.ORB_create(nfeatures=5000, fastThreshold=8)
    kp, des = orb.detectAndCompute(gray, None)
    return {
        "width": w,
        "height": h,
        "dhash": f"{dhash:016x}",
        "kp": kp or [],
        "des": des,
    }


def hamming_hex(a, b):
    return (int(a, 16) ^ int(b, 16)).bit_count()


def match_features(a, b):
    import cv2
    import numpy as np

    da, db = a.get("des"), b.get("des")
    if da is None or db is None or len(da) < 4 or len(db) < 4:
        return {"matches": 0, "good": 0, "median": None, "inliers": 0, "inlier_ratio": 0.0}
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = sorted(matcher.match(da, db), key=lambda m: m.distance)
    good = [m for m in matches if m.distance <= 64]
    inliers = 0
    if len(good) >= 8:
        src = np.float32([a["kp"][m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([b["kp"][m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        if mask is not None:
            inliers = int(mask.ravel().sum())
    med = statistics.median(m.distance for m in matches[: min(50, len(matches))]) if matches else None
    return {
        "matches": len(matches),
        "good": len(good),
        "median": med,
        "inliers": inliers,
        "inlier_ratio": (inliers / len(good)) if good else 0.0,
    }


def load_image(label, url, referer=None):
    st, final, h, body = fetch(
        url,
        accept="image/*,*/*",
        referer=referer,
        limit=MAX_IMAGE_BYTES,
    )
    ctype = h.get("Content-Type", "")
    f = decode_features(body)
    f.update(
        {
            "label": label,
            "url": final,
            "status": st,
            "content_type": ctype,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
        }
    )
    return f


def metric_line(kind, left, right, m):
    med = "" if m["median"] is None else f"{m['median']:.1f}"
    return (
        f"MATCH|kind={kind}|left={clean(left['label'])}|right={clean(right['label'])}|"
        f"dhash_hamming={hamming_hex(left['dhash'], right['dhash'])}|"
        f"orb_matches={m['matches']}|good_le64={m['good']}|median_top50={med}|"
        f"ransac_inliers={m['inliers']}|inlier_ratio={m['inlier_ratio']:.4f}"
    )


def main():
    print("StoneAge 2.5 physical-media transient visual fingerprint probe — R3")
    print("SCOPE|public-image-read-transient|derived-metrics-only|no-login|no-purchase|no-image-commit")
    print(f"OFFICIAL_REFERENCE|{OFFICIAL_MAINLAND_REFERENCE}")
    print(f"WANFANG_PAGE|{WANFANG_PAGE}")
    print("TLS_EXCEPTION_MODE|verification-disabled-only-for-known-expired-collector-hosts")
    errors = []

    ruten_meta = []
    try:
        ruten_meta = ruten_full_images()
        print(f"RUTEN_IMAGE_TARGETS|count={len(ruten_meta)}")
    except Exception as e:
        errors.append(("ruten-metadata", type(e).__name__, str(e)))

    try:
        st, final, wan_meta = wanfang_page_images()
        print(f"WANFANG_PAGE_IMAGES|status={st}|count={len(wan_meta)}|final={clean(final)}")
        for row in wan_meta:
            print(
                f"WANFANG_IMAGE_URL|label={clean(row['label'])}|url={clean(row['url'])}|"
                f"alt={clean(row.get('alt'))}|title={clean(row.get('title'))}"
            )
    except Exception as e:
        wan_meta = []
        errors.append(("wanfang-page", type(e).__name__, str(e)))

    try:
        collector_pages, collector_meta = collector_reference_images()
        for index_url, status, links in collector_pages:
            print(f"COLLECTOR_INDEX|url={clean(index_url)}|status={clean(status)}|matched_links={len(links)}")
            for link in links:
                print(f"COLLECTOR_ARTICLE|index={clean(index_url)}|value={clean(link)}")
        print(f"COLLECTOR_IMAGE_TARGETS|count={len(collector_meta)}")
    except Exception as e:
        collector_meta = []
        errors.append(("collector-mirror", type(e).__name__, str(e)))

    loaded = {}
    try:
        ref = load_image("official-mainland-2.5-collector-reference", OFFICIAL_MAINLAND_REFERENCE)
        loaded[ref["label"]] = ref
        print(
            f"IMAGE|label={clean(ref['label'])}|bytes={ref['bytes']}|sha256={ref['sha256']}|"
            f"size={ref['width']}x{ref['height']}|dhash={ref['dhash']}|keypoints={len(ref['kp'])}|url={clean(ref['url'])}"
        )
    except Exception as e:
        ref = None
        errors.append(("official-reference", type(e).__name__, str(e)))

    ruten = []
    for row in ruten_meta:
        try:
            f = load_image(row["label"], row["url"], referer="https://www.ruten.com.tw/")
            f["carrier"] = row["carrier"]
            loaded[f["label"]] = f
            ruten.append(f)
            print(
                f"IMAGE|label={clean(f['label'])}|bytes={f['bytes']}|sha256={f['sha256']}|"
                f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
            )
        except Exception as e:
            errors.append((row["label"], type(e).__name__, str(e)))

    wanfang = []
    for row in wan_meta[:60]:
        try:
            f = load_image(row["label"], row["url"], referer=WANFANG_PAGE)
            # Ignore tiny page chrome while preserving all photograph-scale candidates.
            if max(f["width"], f["height"]) < 300:
                continue
            loaded[f["label"]] = f
            wanfang.append(f)
            print(
                f"IMAGE|label={clean(f['label'])}|bytes={f['bytes']}|sha256={f['sha256']}|"
                f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
            )
        except Exception as e:
            errors.append((row["label"], type(e).__name__, str(e)))

    collector = []
    for row in collector_meta[:100]:
        try:
            f = load_image(row["label"], row["url"], referer=row.get("article"))
            if max(f["width"], f["height"]) < 300:
                continue
            loaded[f["label"]] = f
            collector.append(f)
            print(
                f"IMAGE|label={clean(f['label'])}|bytes={f['bytes']}|sha256={f['sha256']}|"
                f"size={f['width']}x{f['height']}|dhash={f['dhash']}|keypoints={len(f['kp'])}|url={clean(f['url'])}"
            )
        except Exception as e:
            errors.append((row["label"], type(e).__name__, str(e)))

    rows = []
    # Cross-listing Ruten comparison is independent of external collector mirrors.
    for i, x in enumerate(ruten):
        for y in ruten[i + 1:]:
            if x.get("carrier") == y.get("carrier"):
                continue
            m = match_features(x, y)
            rows.append((m["inliers"], m["good"], -hamming_hex(x["dhash"], y["dhash"]), "ruten-cross-listing", x, y, m))
    if ref:
        for x in ruten:
            m = match_features(x, ref)
            rows.append((m["inliers"], m["good"], -hamming_hex(x["dhash"], ref["dhash"]), "ruten-vs-official", x, ref, m))
        for x in wanfang:
            m = match_features(x, ref)
            rows.append((m["inliers"], m["good"], -hamming_hex(x["dhash"], ref["dhash"]), "wanfang-vs-official", x, ref, m))
    for x in ruten:
        for y in wanfang:
            m = match_features(x, y)
            rows.append((m["inliers"], m["good"], -hamming_hex(x["dhash"], y["dhash"]), "ruten-vs-wanfang", x, y, m))

    for x in ruten:
        for y in collector:
            m = match_features(x, y)
            rows.append((m["inliers"], m["good"], -hamming_hex(x["dhash"], y["dhash"]), "ruten-vs-collector", x, y, m))
    for x in wanfang:
        for y in collector:
            m = match_features(x, y)
            rows.append((m["inliers"], m["good"], -hamming_hex(x["dhash"], y["dhash"]), "wanfang-vs-collector", x, y, m))

    rows.sort(key=lambda z: (z[0], z[1], z[2]), reverse=True)
    print(f"PAIR_COUNT|{len(rows)}")
    for _, _, _, kind, left, right, m in rows[:80]:
        print(metric_line(kind, left, right, m))

    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|ruten_loaded|{len(ruten)}")
    print(f"COUNT|wanfang_large_loaded|{len(wanfang)}")
    print(f"COUNT|collector_large_loaded|{len(collector)}")
    print(f"COUNT|errors|{len(errors)}")
    if rows:
        print("RESOLUTION|DERIVED_VISUAL_MATCH_METRICS_AVAILABLE|manual evidentiary interpretation required")
    else:
        print("RESOLUTION|NO_COMPARABLE_IMAGE_PAIRS|do not infer visual non-match")
    print(
        "EVIDENCE_BOUNDARY|feature similarity can prioritize carrier-family hypotheses but cannot establish disc-byte identity, "
        "official provenance, filesystem contents, or clean-client status."
    )


if __name__ == "__main__":
    main()
