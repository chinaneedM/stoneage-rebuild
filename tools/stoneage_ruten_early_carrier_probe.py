#!/usr/bin/env python3
"""Probe public Ruten StoneAge physical-carrier listings useful for early regional attribution.

Public Ruten item JSON + transient public image reads only.
No login, purchase, seller contact, or image/payload persistence.
The report keeps product metadata, public image URLs, byte hashes and dimensions so
surviving packages can be compared against provenance-preserving baselines.
"""
from __future__ import annotations

import hashlib
import json
import struct
import time
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
DETAIL = "https://rapi.ruten.com.tw/api/items/v2/list"
TARGETS = (
    ("22625938996449", "taiwan-client-box"),
    ("22631285251243", "taiwan-client-box-control"),
    ("22631285248430", "qingjie-package-control"),
    ("22631284715652", "beijing-waei-newbie-control"),
    ("22636573895893", "mainland-retail-box"),
    ("22638643800877", "mainland-boxed-disc"),
)
BASELINE = {
    "name": "Taiwan Waei/JSS StoneAge v1.0 Redump 104630",
    "model": "P-RPG-0008",
    "barcode": "4710739350098",
    "mastering": "華義國際股份有限公司 石器時代 V1.0 P-RPG-0008",
}

def clean(v, n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]

def fetch(url, *, accept="*/*", referer="https://www.ruten.com.tw/", timeout=35, attempts=3, limit=12*1024*1024):
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": accept,
                "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.5",
                "Referer": referer,
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                b = r.read(limit + 1)
                if len(b) > limit:
                    raise ValueError("response-too-large")
                return int(getattr(r, "status", r.getcode())), r.geturl(), dict(r.headers.items()), b
        except Exception as e:
            last = e
            if i + 1 < attempts:
                time.sleep(2 * (i + 1))
    raise last

def detail_rows(data):
    if isinstance(data, dict):
        rows = data.get("data")
        if isinstance(rows, list):
            return [x for x in rows if isinstance(x, dict)]
        if isinstance(rows, dict):
            return [rows]
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    return []

def image_urls(row):
    out, seen = [], set()
    images = row.get("images") if isinstance(row, dict) else None
    if isinstance(images, dict):
        vals = images.get("url")
        if isinstance(vals, list):
            candidates = vals
        elif vals:
            candidates = [vals]
        else:
            candidates = []
        for raw in candidates:
            u = str(raw)
            if u.startswith("//"):
                u = "https:" + u
            elif u.startswith("/"):
                u = "https://a.rimg.com.tw" + u
            if u and u not in seen:
                seen.add(u)
                out.append(u)
    return out

def image_dimensions(body):
    if body.startswith(b"\x89PNG\r\n\x1a\n") and len(body) >= 24:
        return struct.unpack(">II", body[16:24])
    if body.startswith((b"GIF87a", b"GIF89a")) and len(body) >= 10:
        return struct.unpack("<HH", body[6:10])
    if body.startswith(b"\xff\xd8"):
        i = 2
        while i + 9 < len(body):
            if body[i] != 0xFF:
                i += 1
                continue
            while i < len(body) and body[i] == 0xFF:
                i += 1
            if i >= len(body):
                break
            marker = body[i]
            i += 1
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                continue
            if i + 2 > len(body):
                break
            seglen = int.from_bytes(body[i:i+2], "big")
            if seglen < 2 or i + seglen > len(body):
                break
            if marker in {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF} and seglen >= 7:
                h = int.from_bytes(body[i+3:i+5], "big")
                w = int.from_bytes(body[i+5:i+7], "big")
                return w, h
            i += seglen
    return None, None

def main():
    print("StoneAge early Ruten physical-carrier probe — R1")
    print("SCOPE|public-item-json+transient-public-images|derived-metadata-only|no-login|no-purchase|no-contact|no-image-commit")
    print("BASELINE|name={}|model={}|barcode={}|mastering={}".format(
        clean(BASELINE["name"]), clean(BASELINE["model"]), clean(BASELINE["barcode"]), clean(BASELINE["mastering"])
    ))
    print("TARGETS|" + ",".join(pid for pid, _ in TARGETS))
    errors = []
    image_count = 0
    for pid, role in TARGETS:
        try:
            q = urllib.parse.urlencode({"gno": pid, "level": "simple"})
            st, final, headers, body = fetch(DETAIL + "?" + q, accept="application/json,*/*")
            data = json.loads(body.decode("utf-8", "replace"))
            rows = detail_rows(data)
            print(f"DETAIL|id={pid}|role={role}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}")
            for row in rows:
                imgs = image_urls(row)
                print(
                    f"ITEM|id={pid}|role={role}|name={clean(row.get('name'))}|post_time={clean(row.get('post_time'))}|"
                    f"store={clean(row.get('store_name'))}|stock={clean(row.get('num'))}|sold={clean(row.get('sold_num'))}|"
                    f"image_count={len(imgs)}|image_filenames={clean((row.get('images') or {}).get('filename') if isinstance(row.get('images'), dict) else '')}"
                )
                for idx, url in enumerate(imgs):
                    try:
                        ist, ifinal, ih, ib = fetch(url, accept="image/*,*/*", limit=12*1024*1024)
                        w, h = image_dimensions(ib)
                        image_count += 1
                        print(
                            f"IMAGE|id={pid}|role={role}|index={idx}|status={ist}|bytes={len(ib)}|"
                            f"sha256={hashlib.sha256(ib).hexdigest()}|size={clean(w)}x{clean(h)}|"
                            f"content_type={clean(ih.get('Content-Type'))}|url={clean(ifinal,5000)}"
                        )
                    except Exception as e:
                        errors.append((pid, f"image:{idx}", type(e).__name__, str(e)))
        except Exception as e:
            errors.append((pid, "detail", type(e).__name__, str(e)))
    for pid, scope, kind, msg in errors:
        print(f"ERROR|id={pid}|scope={scope}|kind={kind}|message={clean(msg)}")
    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|images|{image_count}")
    print(f"COUNT|errors|{len(errors)}")
    if image_count:
        print("RESOLUTION|EARLY_CARRIER_IMAGE_SET_RECOVERED|inspect exact model/barcode/operator text before assigning package lineage")
    elif errors:
        print("RESOLUTION|PUBLIC_RUTEN_READ_INCOMPLETE|do not infer absence")
    else:
        print("RESOLUTION|NO_PUBLIC_IMAGES_ON_TESTED_ITEMS")
    print("EVIDENCE_BOUNDARY|seller titles and package photographs are carrier-attribution evidence only; matching artwork or identifiers does not by itself establish disc-byte identity, mastering identity, client cleanliness, or historical release date.")

if __name__ == "__main__":
    main()
