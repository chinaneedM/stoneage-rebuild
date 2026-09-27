#!/usr/bin/env python3
"""Bind historical Yegame StoneAge product codes to detail-page metadata.

Known source-grounded product keys from the recovered 2001 game catalog:
  EN0ZGKJ0002 = 石器时代
  EZ0JHSD0003 = 石器时代-WGS620点会员卡

This probe:
1) enumerates exact Wayback captures for both detail pages;
2) replays a bounded set of distinct HTML captures;
3) extracts product-field text, links, and image URLs;
4) queries Wayback metadata for candidate product/cover images only.

No software payload or image body is downloaded.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
FROM = "20010201"
TO = "20011231"
FIELDS = "timestamp,original,statuscode,mimetype,digest,length,redirect"

PRODUCTS = (
    ("client-product", "EN0ZGKJ0002", "石器时代"),
    ("wgs-card", "EZ0JHSD0003", "石器时代-WGS620点会员卡"),
)

HOSTS = ("yegame.com", "www.yegame.com")
TOKENS = (
    "石器时代", "石器時代", "石器",
    "产品介质", "產品介質", "介质", "介質",
    "更新日期", "零售价", "零售價", "批发价", "批發價",
    "开发商", "開發商", "发行", "發行", "出版",
    "光盘", "光碟", "cd-rom", "cdrom", "cd",
    "客户端", "客戶端", "client",
    "华义", "華義", "waei", "智冠", "金海湾", "金海灣",
    "晶合", "jhpop", "wgs", "620",
)
FIELD_WORDS = (
    "产品名称", "產品名稱", "产品介质", "產品介質", "介质", "介質",
    "更新日期", "零售价", "零售價", "批发价", "批發價",
    "开发商", "開發商", "发行", "發行", "出版", "公司",
    "产品介绍", "產品介紹", "内容", "內容", "说明", "說明",
)


def clean(value, limit=8000):
    return " ".join(str(value if value is not None else "").split()).replace("|", "%7C")[:limit]


def fetch(url, timeout=60, max_bytes=4 * 1024 * 1024, attempts=3):
    last = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Accept": "application/json,text/html,*/*;q=0.2",
                    "Accept-Encoding": "identity",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                body = response.read(max_bytes + 1)
                if len(body) > max_bytes:
                    raise ValueError(f"response-too-large:{len(body)}")
                return int(getattr(response, "status", response.getcode())), response.geturl(), body
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1 + attempt)
    raise last


def cdx_url(url, match="exact", start=FROM, end=TO):
    params = [
        ("url", url), ("matchType", match), ("output", "json"),
        ("fl", FIELDS), ("from", start), ("to", end), ("limit", "50000"),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def parse_cdx(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, row)) for row in obj[1:] if isinstance(row, list))


def decode(body):
    for enc in ("gb18030", "gbk", "big5", "cp950", "utf-8", "latin1"):
        try:
            return enc, body.decode(enc)
        except UnicodeDecodeError:
            continue
    return "latin1", body.decode("latin1", "replace")


def visible_text(text):
    value = re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>", " ", text)
    value = re.sub(r"(?is)<[^>]+>", " ", value)
    return clean(html.unescape(value), 80000)


def title(text):
    m = re.search(r"(?is)<title\b[^>]*>(.*?)</title>", text)
    return clean(html.unescape(re.sub(r"(?is)<[^>]+>", " ", m.group(1)))) if m else ""


def hits(text):
    low = text.lower()
    return tuple(token for token in TOKENS if token.lower() in low)


def snippets(text, needles, radius=420, limit=24):
    low = text.lower()
    out = []
    seen = set()
    for needle in needles:
        nlow = needle.lower()
        start = 0
        while True:
            idx = low.find(nlow, start)
            if idx < 0:
                break
            frag = clean(text[max(0, idx-radius):min(len(text), idx+len(needle)+radius)], 1600)
            key = frag[:500]
            if key and key not in seen:
                seen.add(key)
                out.append((needle, frag))
            start = idx + max(1, len(needle))
            if len(out) >= limit:
                return tuple(out)
    return tuple(out)


def extract_refs(text, base):
    out = []
    seen = set()
    for attr in ("href", "src", "action"):
        pat = rf"(?is)\b{attr}\s*=\s*([\"'])(.*?)\1"
        for m in re.finditer(pat, text):
            raw = html.unescape(m.group(2)).strip()
            if not raw or raw.lower().startswith(("javascript:", "mailto:", "tel:", "#", "data:")):
                continue
            url = urllib.parse.urljoin(base, raw)
            key = (attr, url)
            if key not in seen:
                seen.add(key)
                out.append(key)
    return tuple(out)


def is_candidate_image(url):
    low = urllib.parse.unquote_plus(str(url or "")).lower()
    path = urllib.parse.urlsplit(low).path
    return (
        path.endswith((".jpg", ".jpeg", ".gif", ".png", ".bmp"))
        and any(token in low for token in ("product", "prod", "image", "cover", "pic"))
    )


def detail_url(host, code):
    return f"http://{host}:80/product/detail.asp?prodencode={code}"


def product_code(url):
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(str(url or "")).query)
    vals = q.get("prodencode") or q.get("ProdEncode") or ()
    return str(vals[0]) if vals else ""


def main():
    print("StoneAge Yegame product-detail binding — R1")
    print("SOURCE_CHAIN|JHPOP -> Yegame game catalog -> EN0ZGKJ0002/EZ0JHSD0003")
    print(f"SCOPE|exact product detail CDX + bounded HTML replay + image CDX metadata|{FROM}..{TO}|no software/image payload")

    errors = []
    product_rows = {}
    image_urls = set()

    for label, code, expected_name in PRODUCTS:
        for host in HOSTS:
            original = detail_url(host, code)
            try:
                status, final, body = fetch(cdx_url(original))
                rows = parse_cdx(body)
                print(
                    "QUERY|label={}|code={}|host={}|status={}|rows={}|bytes={}|sha256={}|final={}".format(
                        clean(label), clean(code), clean(host), status, len(rows), len(body),
                        hashlib.sha256(body).hexdigest(), clean(final)
                    )
                )
                for row in rows:
                    key = (
                        label, code, str(row.get("timestamp") or ""),
                        str(row.get("original") or ""), str(row.get("digest") or "")
                    )
                    product_rows[key] = row
            except Exception as exc:
                errors.append((f"{label}:{host}", "cdx", type(exc).__name__, str(exc)))

    ordered = sorted(
        product_rows.items(),
        key=lambda kv: (
            kv[0][1], str(kv[1].get("timestamp") or ""),
            str(kv[1].get("original") or "")
        ),
    )

    for (label, code, _ts, _orig, _digest), row in ordered:
        print(
            "ROW|label={}|code={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                clean(label), clean(code), clean(row.get("timestamp")), clean(row.get("statuscode")),
                clean(row.get("mimetype")), clean(row.get("length")), clean(row.get("digest")),
                clean(row.get("redirect")), clean(row.get("original"))
            )
        )

    # Replay up to 6 distinct successful HTML digests per product code.
    grouped = {}
    for key, row in ordered:
        label, code = key[0], key[1]
        grouped.setdefault((label, code), []).append(row)

    replayed = 0
    direct_name_pages = 0
    for label, code, expected_name in PRODUCTS:
        seen_digests = set()
        selected = []
        for row in grouped.get((label, code), ()):
            if str(row.get("statuscode") or "") != "200":
                continue
            if "html" not in str(row.get("mimetype") or "").lower():
                continue
            digest = str(row.get("digest") or "")
            if digest and digest in seen_digests:
                continue
            seen_digests.add(digest)
            selected.append(row)
            if len(selected) >= 6:
                break

        for row in selected:
            timestamp = str(row.get("timestamp") or "")
            original = str(row.get("original") or "")
            replay = f"https://web.archive.org/web/{timestamp}id_/{original}"
            try:
                status, final, body = fetch(replay)
                enc, text = decode(body)
                visible = visible_text(text)
                page_hits = hits(visible)
                refs = extract_refs(text, original)
                expected_hit = expected_name.lower() in visible.lower()
                if expected_hit:
                    direct_name_pages += 1
                print(
                    "PAGE|label={}|code={}|timestamp={}|status={}|bytes={}|sha256={}|encoding={}|title={}|expected_name_hit={}|token_hits={}|refs={}|original={}|final={}".format(
                        clean(label), clean(code), clean(timestamp), status, len(body),
                        hashlib.sha256(body).hexdigest(), clean(enc), clean(title(text)),
                        int(expected_hit), clean(",".join(page_hits), 3000), len(refs),
                        clean(original), clean(final)
                    )
                )
                needles = (expected_name,) + FIELD_WORDS + page_hits
                for token, frag in snippets(visible, needles):
                    print(
                        "SNIPPET|label={}|code={}|timestamp={}|token={}|text={}".format(
                            clean(label), clean(code), clean(timestamp), clean(token), clean(frag, 1800)
                        )
                    )
                for kind, url in refs:
                    candidate_image = int(is_candidate_image(url))
                    code2 = product_code(url)
                    if candidate_image:
                        image_urls.add(url)
                    if candidate_image or code2 or any(tok.lower() in url.lower() for tok in ("stone", "waei", "jhpop")):
                        print(
                            "REF|label={}|code={}|timestamp={}|kind={}|candidate_image={}|linked_prodencode={}|url={}".format(
                                clean(label), clean(code), clean(timestamp), clean(kind),
                                candidate_image, clean(code2), clean(url)
                            )
                        )
                replayed += 1
            except Exception as exc:
                errors.append((f"{label}:{code}:{timestamp}", "replay", type(exc).__name__, str(exc)))

    image_rows = 0
    for url in sorted(image_urls):
        try:
            status, final, body = fetch(cdx_url(url))
            rows = parse_cdx(body)
            print(
                "IMAGE_QUERY|status={}|rows={}|bytes={}|sha256={}|url={}|final={}".format(
                    status, len(rows), len(body), hashlib.sha256(body).hexdigest(),
                    clean(url), clean(final)
                )
            )
            for row in rows[:12]:
                print(
                    "IMAGE_ROW|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                        clean(row.get("timestamp")), clean(row.get("statuscode")), clean(row.get("mimetype")),
                        clean(row.get("length")), clean(row.get("digest")), clean(row.get("redirect")),
                        clean(row.get("original"))
                    )
                )
                image_rows += 1
        except Exception as exc:
            errors.append((url, "image-cdx", type(exc).__name__, str(exc)))

    print(f"COUNT|product_cdx_rows|{len(ordered)}")
    print(f"COUNT|replayed_pages|{replayed}")
    print(f"COUNT|direct_expected_name_pages|{direct_name_pages}")
    print(f"COUNT|candidate_image_urls|{len(image_urls)}")
    print(f"COUNT|image_cdx_rows_printed|{image_rows}")
    for label, scope, kind, message in errors:
        print(f"ERROR|label={clean(label)}|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")
    print(f"COUNT|errors|{len(errors)}")

    if direct_name_pages:
        print("RESOLUTION|STONEAGE_PRODUCT_DETAIL_BOUND|extract carrier/publisher/price/image metadata and compare to known Mainland media")
    elif ordered:
        print("RESOLUTION|PRODUCT_DETAIL_ARCHIVE_FOUND_NO_DIRECT_NAME|inspect template/linked product image metadata carefully")
    elif errors:
        print("RESOLUTION|PARTIAL_PRODUCT_DETAIL_PROBE|retry only failed exact surfaces")
    else:
        print("RESOLUTION|PRODUCT_DETAIL_ROUTE_BOUNDED|catalog product code remains factual but detail captures are not indexed")
    print("EVIDENCE_BOUNDARY|Product pages/images are used as catalog provenance only; no client installer or image body is downloaded.")


if __name__ == "__main__":
    main()
