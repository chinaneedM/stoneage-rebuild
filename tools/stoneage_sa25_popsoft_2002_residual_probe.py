#!/usr/bin/env python3
"""Expand the residual 2002 Popsoft carrier surface without downloading payloads.

The general StoneAge 2.5 carrier probe found exactly one Internet Archive
metadata row for '"大众软件" AND year:2002', but its strict title filter did not
print the object. This probe resolves that residual object and the already-known
Popsoft magazine-scan family at metadata/file-list level only.

No file bodies are downloaded.
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

SEARCHES = (
    ("popular-software-2002", '"大众软件" AND year:2002'),
)
PINNED_IDENTIFIERS = ("popsoft-magazine_202403",)
OPTICAL_EXTENSIONS = (
    ".iso", ".bin", ".cue", ".img", ".mdf", ".mds", ".nrg", ".ccd", ".sub",
)
ARCHIVE_EXTENSIONS = (".zip", ".rar", ".7z", ".tar", ".gz")
PERIOD_MARKERS = (
    "2002", "大众软件", "大众游戏", "popsoft", "2002年2", "2002-02", "200202",
)


def clean(value, limit=2200):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def fetch_json(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        return (
            int(getattr(response, "status", response.getcode())),
            response.geturl(),
            body,
            json.loads(body.decode("utf-8")),
        )


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


def ia_docs(value):
    response = value.get("response", {}) if isinstance(value, dict) else {}
    docs = response.get("docs", []) if isinstance(response, dict) else []
    return tuple(row for row in docs if isinstance(row, dict))


def file_name(row):
    return str(row.get("name") or "")


def source_original(row):
    return str(row.get("source") or "").lower() == "original"


def optical_file(row):
    low = file_name(row).lower()
    return low.endswith(OPTICAL_EXTENSIONS)


def archive_file(row):
    low = file_name(row).lower()
    return low.endswith(ARCHIVE_EXTENSIONS)


def period_relevant_file(row):
    name = file_name(row)
    low = name.lower()
    return any(marker.lower() in low for marker in PERIOD_MARKERS)


def feb_2002_file(row):
    name = file_name(row).lower()
    patterns = (
        r"2002[^0-9]{0,4}(?:0?2|二)月",
        r"2002[-_/ .]?0?2(?:[^0-9]|$)",
        r"200202",
    )
    return any(re.search(pattern, name, flags=re.IGNORECASE) for pattern in patterns)


def emit_metadata(identifier, data):
    metadata = data.get("metadata", {}) if isinstance(data, dict) else {}
    files = data.get("files", []) if isinstance(data, dict) else []
    files = [row for row in files if isinstance(row, dict)]

    originals = [row for row in files if source_original(row)]
    optical = [row for row in files if optical_file(row)]
    original_optical = [row for row in originals if optical_file(row)]
    archives = [row for row in files if archive_file(row)]
    period = [row for row in files if period_relevant_file(row)]
    feb = [row for row in files if feb_2002_file(row)]

    print(
        "IA_META|"
        f"identifier={clean(identifier)}|title={clean(metadata.get('title'))}|"
        f"date={clean(metadata.get('date'))}|year={clean(metadata.get('year'))}|"
        f"mediatype={clean(metadata.get('mediatype'))}|collection={clean(metadata.get('collection'))}|"
        f"creator={clean(metadata.get('creator'))}|uploader={clean(metadata.get('uploader'))}|"
        f"files={len(files)}|originals={len(originals)}|optical={len(optical)}|"
        f"original_optical={len(original_optical)}|archives={len(archives)}|"
        f"period_files={len(period)}|feb_2002_files={len(feb)}"
    )

    selected = []
    seen = set()
    for group, label in (
        (original_optical, "original-optical"),
        (optical, "optical"),
        (feb, "feb-2002"),
        (period, "period"),
        (originals, "original"),
    ):
        for row in group:
            name = file_name(row)
            key = (name, str(row.get("size") or ""), str(row.get("md5") or ""), str(row.get("sha1") or ""))
            if key in seen:
                continue
            seen.add(key)
            selected.append((label, row))

    for label, row in selected[:400]:
        print(
            "IA_FILE|"
            f"identifier={clean(identifier)}|class={label}|name={clean(row.get('name'))}|"
            f"source={clean(row.get('source'))}|format={clean(row.get('format'))}|"
            f"size={clean(row.get('size'))}|md5={clean(row.get('md5'))}|"
            f"sha1={clean(row.get('sha1'))}|crc32={clean(row.get('crc32'))}"
        )

    if original_optical:
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "PUBLIC_OPTICAL_METADATA_PRESENT|inspect provenance before any file-body recovery"
        )
    elif feb and any(archive_file(row) for row in feb):
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "FEB_2002_ARCHIVE_METADATA_PRESENT|inspect archive role before payload recovery"
        )
    elif period:
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "PERIOD_SCAN_OR_METADATA_ONLY|no optical-image file exposed by current IA metadata"
        )
    else:
        print(
            f"IA_ITEM_RESOLUTION|identifier={clean(identifier)}|"
            "NO_2002_CARRIER_FILE_SIGNAL|metadata object does not expose the target carrier"
        )

    return {
        "original_optical": len(original_optical),
        "feb": len(feb),
        "period": len(period),
    }


def main():
    print("StoneAge 2.5 Popsoft 2002 residual carrier probe — R1")
    print("SCOPE|IA-advancedsearch-residual+known-Popsoft-scan-family|metadata+file-list-only|no-file-body")
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
                    f"creator={clean(row.get('creator'))}|description={clean(row.get('description'))}"
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

    total_optical = 0
    total_feb = 0
    total_period = 0
    for identifier in unique:
        try:
            status, final, body, data = fetch_json(metadata_url(identifier))
            print(
                f"IA_META_FETCH|identifier={clean(identifier)}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}"
            )
            counts = emit_metadata(identifier, data)
            total_optical += counts["original_optical"]
            total_feb += counts["feb"]
            total_period += counts["period"]
        except Exception as exc:
            errors.append((f"metadata:{identifier}", type(exc).__name__, str(exc)))

    for scope, kind, message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|query_rows|{query_rows}")
    print(f"COUNT|unique_items_inspected|{len(unique)}")
    print(f"COUNT|original_optical_files|{total_optical}")
    print(f"COUNT|feb_2002_files|{total_feb}")
    print(f"COUNT|period_relevant_files|{total_period}")
    print(f"COUNT|errors|{len(errors)}")

    if total_optical:
        print("RESOLUTION|PUBLIC_OPTICAL_METADATA_FOUND|promote exact item/file identity for provenance inspection")
    elif errors:
        print("RESOLUTION|PARTIAL_RESIDUAL_UNRESOLVED|one or more metadata surfaces failed")
    else:
        print("RESOLUTION|POPSOFT_2002_RESIDUAL_BOUNDED|no public optical-image file exposed by inspected IA residual objects")


if __name__ == "__main__":
    main()
