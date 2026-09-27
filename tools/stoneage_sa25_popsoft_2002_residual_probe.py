#!/usr/bin/env python3
"""Resolve the residual 2002 Popsoft carrier surface without downloading game payloads.

The earlier general carrier probe returned one Internet Archive metadata row for
'"大众软件" AND year:2002', but strict filtering hid its identity. This probe:
1) expands that residual metadata row;
2) inspects the known Popsoft magazine-scan family at file-list level;
3) transiently reads only the small IA OCR text derivatives for the February
   2002 A/B scans and records token counts/offsets, not copied article text.

No optical/game payload bodies are downloaded or committed.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
IA_ADV = "https://archive.org/advancedsearch.php"
IA_META = "https://archive.org/metadata/"
IA_DOWNLOAD = "https://archive.org/download/"

SEARCHES = (
    ("popular-software-2002", '"大众软件" AND year:2002'),
)
PINNED_IDENTIFIERS = ("popsoft-magazine_202403",)
OPTICAL_EXTENSIONS = (
    ".iso", ".bin", ".cue", ".img", ".mdf", ".mds", ".nrg", ".ccd", ".sub",
)
TARGET_FAMILY_MARKERS = ("大众软件", "大众游戏", "popsoft")
OCR_TOKENS = (
    "石器时代",
    "石器時代",
    "精灵王",
    "精靈王",
    "大众游戏",
    "大眾遊戲",
    "配套光盘",
    "配套光碟",
)
MAX_OCR_BYTES = 2_000_000


def clean(value, limit=2200):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def fetch_bytes(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read(MAX_OCR_BYTES + 1)
        if len(body) > MAX_OCR_BYTES:
            raise ValueError(f"body exceeds metadata/OCR limit: {len(body)}")
        return int(getattr(response, "status", response.getcode())), response.geturl(), body


def fetch_json(url, timeout=60):
    status, final, body = fetch_bytes_unbounded_json(url, timeout=timeout)
    return status, final, body, json.loads(body.decode("utf-8"))


def fetch_bytes_unbounded_json(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        return int(getattr(response, "status", response.getcode())), response.geturl(), body


def advanced_search_url(query):
    params = [
        ("q", query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "date"),
        ("fl[]", "year"),
        ("fl[]", "description"),
        ("fl[]", "collection"),
        ("fl[]", "mediatype"),
        ("fl[]", "creator"),
        ("rows", "100"),
        ("page", "1"),
        ("output", "json"),
    ]
    return IA_ADV + "?" + urllib.parse.urlencode(params)


def metadata_url(identifier):
    return IA_META + urllib.parse.quote(identifier, safe="")


def download_url(identifier, name):
    return (
        IA_DOWNLOAD
        + urllib.parse.quote(identifier, safe="")
        + "/"
        + urllib.parse.quote(name, safe="/")
    )


def ia_docs(value):
    response = value.get("response", {}) if isinstance(value, dict) else {}
    docs = response.get("docs", []) if isinstance(response, dict) else []
    return tuple(row for row in docs if isinstance(row, dict))


def file_name(row):
    return str(row.get("name") or "")


def source_original(row):
    return str(row.get("source") or "").lower() == "original"


def optical_file(row):
    return file_name(row).lower().endswith(OPTICAL_EXTENSIONS)


def target_family_item(identifier, metadata):
    blob = " ".join(
        str(value or "")
        for value in (
            identifier,
            metadata.get("title") if isinstance(metadata, dict) else "",
            metadata.get("creator") if isinstance(metadata, dict) else "",
        )
    ).lower()
    return any(marker.lower() in blob for marker in TARGET_FAMILY_MARKERS)


def feb_2002_file(row):
    name = file_name(row).lower()
    patterns = (
        r"2002[^0-9]{0,4}(?:0?2|二)月",
        r"2002[-_/ .]?0?2(?:[^0-9]|$)",
        r"200202",
    )
    return any(re.search(pattern, name, flags=re.IGNORECASE) for pattern in patterns)


def feb_ocr_file(row):
    low = file_name(row).lower()
    return feb_2002_file(row) and low.endswith("_djvu.txt")


def token_offsets(text, token, limit=12):
    out = []
    start = 0
    while len(out) < limit:
        pos = text.find(token, start)
        if pos < 0:
            break
        out.append(pos)
        start = pos + max(1, len(token))
    return out


def count_token(text, token):
    return text.count(token)


def strong_stoneage_offsets(text, limit=20):
    """Find StoneAge mentions with 2.5 or Spirit-King semantics nearby."""
    anchors = []
    for token in ("石器时代", "石器時代", "石器"):
        start = 0
        while True:
            pos = text.find(token, start)
            if pos < 0:
                break
            lo = max(0, pos - 180)
            hi = min(len(text), pos + 300)
            window = text[lo:hi]
            if (
                "2.5" in window
                or "精灵王" in window
                or "精靈王" in window
                or "StoneAge 2.5" in window
                or "StoneAge2.5" in window
            ):
                anchors.append(pos)
            start = pos + max(1, len(token))
    return sorted(set(anchors))[:limit]


def emit_ocr_probe(identifier, row):
    name = file_name(row)
    url = download_url(identifier, name)
    status, final, body = fetch_bytes(url)
    text = body.decode("utf-8", errors="replace")
    print(
        f"OCR_FETCH|identifier={clean(identifier)}|name={clean(name)}|status={status}|"
        f"bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}"
    )
    for token in OCR_TOKENS:
        count = count_token(text, token)
        if count:
            offsets = ",".join(str(x) for x in token_offsets(text, token))
            print(
                f"OCR_TOKEN|identifier={clean(identifier)}|name={clean(name)}|"
                f"token={clean(token)}|count={count}|first_offsets={offsets}"
            )
    strong = strong_stoneage_offsets(text)
    print(
        f"OCR_STRONG|identifier={clean(identifier)}|name={clean(name)}|"
        f"count={len(strong)}|first_offsets={','.join(str(x) for x in strong)}"
    )
    return len(strong)


def emit_metadata(identifier, data):
    metadata = data.get("metadata", {}) if isinstance(data, dict) else {}
    files = data.get("files", []) if isinstance(data, dict) else []
    files = [row for row in files if isinstance(row, dict)]
    target_family = target_family_item(identifier, metadata)

    originals = [row for row in files if source_original(row)]
    optical = [row for row in files if optical_file(row)]
    original_optical = [row for row in originals if optical_file(row)]
    feb = [row for row in files if feb_2002_file(row)]
    feb_ocr = [row for row in files if feb_ocr_file(row)]

    print(
        "IA_META|"
        f"identifier={clean(identifier)}|target_family={int(target_family)}|"
        f"title={clean(metadata.get('title'))}|date={clean(metadata.get('date'))}|"
        f"year={clean(metadata.get('year'))}|mediatype={clean(metadata.get('mediatype'))}|"
        f"collection={clean(metadata.get('collection'))}|creator={clean(metadata.get('creator'))}|"
        f"uploader={clean(metadata.get('uploader'))}|files={len(files)}|originals={len(originals)}|"
        f"optical={len(optical)}|original_optical={len(original_optical)}|"
        f"feb_2002_files={len(feb)}|feb_ocr_files={len(feb_ocr)}"
    )

    selected = []
    seen = set()
    for group, label in (
        (original_optical, "original-optical"),
        (feb, "feb-2002"),
    ):
        for row in group:
            key = file_name(row)
            if key in seen:
                continue
            seen.add(key)
            selected.append((label, row))

    for label, row in selected[:120]:
        print(
            "IA_FILE|"
            f"identifier={clean(identifier)}|class={label}|name={clean(row.get('name'))}|"
            f"source={clean(row.get('source'))}|format={clean(row.get('format'))}|"
            f"size={clean(row.get('size'))}|md5={clean(row.get('md5'))}|"
            f"sha1={clean(row.get('sha1'))}|crc32={clean(row.get('crc32'))}"
        )

    strong_hits = 0
    if target_family:
        for row in feb_ocr:
            strong_hits += emit_ocr_probe(identifier, row)

    target_optical = len(original_optical) if target_family else 0
    if not target_family:
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "UNRELATED_METADATA_COLLISION|do-not-promote-optical-files"
        )
    elif target_optical:
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "TARGET_FAMILY_OPTICAL_METADATA_PRESENT|inspect provenance before file-body recovery"
        )
    elif feb:
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "FEB_2002_MAGAZINE_SCAN_ONLY|no optical-image file exposed by current IA metadata"
        )
    else:
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "TARGET_FAMILY_NO_CARRIER_FILE_SIGNAL"
        )

    return {
        "target_optical": target_optical,
        "feb": len(feb) if target_family else 0,
        "ocr_strong": strong_hits,
        "target_family": int(target_family),
    }


def main():
    print("StoneAge 2.5 Popsoft 2002 residual carrier probe — R2")
    print("SCOPE|IA-residual+Popsoft-Feb2002-scan|metadata+file-list+transient-OCR-only|no-game-payload")
    print("TARGET|大众软件CD——大众游戏|issue=2002-02|role=possible-StoneAge-2.5-full-or-upgrade-carrier")

    errors = []
    identifiers = []
    query_rows = 0

    for label, query in SEARCHES:
        try:
            url = advanced_search_url(query)
            status, final, body, data = fetch_json(url)
            docs = ia_docs(data)
            query_rows += len(docs)
            print(
                f"IA_QUERY|label={label}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|items={len(docs)}|final={clean(final)}"
            )
            for row in docs:
                identifier = str(row.get("identifier") or "")
                if identifier:
                    identifiers.append(identifier)
                print(
                    f"IA_DOC|label={label}|identifier={clean(identifier)}|title={clean(row.get('title'))}|"
                    f"date={clean(row.get('date'))}|year={clean(row.get('year'))}|"
                    f"mediatype={clean(row.get('mediatype'))}|collection={clean(row.get('collection'))}|"
                    f"creator={clean(row.get('creator'))}"
                )
        except Exception as exc:
            errors.append((f"query:{label}", type(exc).__name__, str(exc)))

    identifiers.extend(PINNED_IDENTIFIERS)
    unique = []
    seen = set()
    for identifier in identifiers:
        if identifier and identifier not in seen:
            seen.add(identifier)
            unique.append(identifier)

    target_optical = 0
    feb_files = 0
    ocr_strong = 0
    target_items = 0
    for identifier in unique:
        try:
            status, final, body, data = fetch_json(metadata_url(identifier))
            print(
                f"IA_META_FETCH|identifier={clean(identifier)}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}"
            )
            counts = emit_metadata(identifier, data)
            target_optical += counts["target_optical"]
            feb_files += counts["feb"]
            ocr_strong += counts["ocr_strong"]
            target_items += counts["target_family"]
        except Exception as exc:
            errors.append((f"metadata:{identifier}", type(exc).__name__, str(exc)))

    for scope, kind, message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|query_rows|{query_rows}")
    print(f"COUNT|unique_items_inspected|{len(unique)}")
    print(f"COUNT|target_family_items|{target_items}")
    print(f"COUNT|target_original_optical_files|{target_optical}")
    print(f"COUNT|target_feb_2002_files|{feb_files}")
    print(f"COUNT|ocr_strong_stoneage25_offsets|{ocr_strong}")
    print(f"COUNT|errors|{len(errors)}")

    if target_optical:
        print("RESOLUTION|TARGET_FAMILY_OPTICAL_METADATA_FOUND|promote exact file identity for provenance inspection")
    elif errors:
        print("RESOLUTION|PARTIAL_RESIDUAL_UNRESOLVED|one or more target metadata/OCR surfaces failed")
    elif ocr_strong:
        print("RESOLUTION|FEB2002_SCAN_CORROBORATES_STONEAGE25|magazine text survives but no optical-image file is exposed")
    else:
        print("RESOLUTION|POPSOFT_2002_OPTICAL_RESIDUAL_BOUNDED|query collision rejected and scan family exposes no target optical image")


if __name__ == "__main__":
    main()
