#!/usr/bin/env python3
"""Bounded Internet Archive reverse-index probe for StoneAge in known Korean CD-preservation uploaders.

The probe enumerates software items from two already-confirmed public preservation uploaders,
then inspects item metadata and file-list names for exact StoneAge/GameTime/guide-ISBN signals.
It reads metadata only; no carrier or software payload bytes are downloaded.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
ADV = "https://archive.org/advancedsearch.php"
META = "https://archive.org/metadata/{}"

UPLOADERS = (
    "mirubackup1@gmail.com",
    "marty0837@naver.com",
)

GUIDE_ISBNS = (
    "8995182121",
    "9788995182123",
)

GLOBAL_QUERIES = (
    '("StoneAge" OR "Stone Age" OR "스톤에이지") AND mediatype:software',
    '"8995182121"',
    '"9788995182123"',
    '("GameTime" OR "게임타임") AND ("StoneAge" OR "Stone Age" OR "스톤에이지")',
)

ROWS_PER_PAGE = 200
MAX_PAGES_PER_UPLOADER = 3
MAX_ITEMS = 600
MAX_METADATA_WORKERS = 8

STONEAGE = re.compile(r"(?i)(stone\s*age|stoneage|스톤\s*에이지|스톤에이지)")
GAMETIME = re.compile(r"(?i)(gametime|game\s*time|게임\s*타임|게임타임)")
EXACT_FILES = re.compile(
    r"(?i)(?:^|[/\\])(?:"
    r"sa\.exe|sa_demo\.exe|stoneage\.exe|stone_demo\.exe|"
    r"onlstoneage\.zip|stoneagebeta\.zip|stoneage\.zip"
    r")$"
)
CARRIER = re.compile(r"(?i)\.(?:iso|img|bin|mdf|nrg|ccd|cue)$")


def clean(value, limit=900):
    if value is None:
        return ""
    if isinstance(value, list):
        value = ",".join(str(x) for x in value)
    text = " ".join(str(value).split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def get_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)


def search(query, page=1, rows=ROWS_PER_PAGE):
    params = [
        ("q", query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "description"),
        ("fl[]", "date"),
        ("fl[]", "year"),
        ("fl[]", "creator"),
        ("fl[]", "uploader"),
        ("fl[]", "mediatype"),
        ("rows", str(rows)),
        ("page", str(page)),
        ("output", "json"),
    ]
    return get_json(ADV + "?" + urllib.parse.urlencode(params)).get("response", {})


def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier, safe="")))


def metadata_blob(meta):
    return " ".join(
        clean(meta.get(key), 3000)
        for key in ("identifier", "title", "description", "subject", "creator", "date", "year", "uploader")
    )


def inspect_item(identifier, search_doc=None):
    data = metadata(identifier)
    meta = dict(search_doc or {})
    meta.update(data.get("metadata", {}))
    blob = metadata_blob(meta)
    files = data.get("files", [])

    metadata_stoneage = bool(STONEAGE.search(blob))
    metadata_gametime = bool(GAMETIME.search(blob))
    isbn_hits = [isbn for isbn in GUIDE_ISBNS if isbn in blob]
    exact_files = []
    stoneage_files = []
    carrier_files = []

    for row in files:
        name = str(row.get("name", ""))
        if EXACT_FILES.search(name):
            exact_files.append(row)
        if STONEAGE.search(name):
            stoneage_files.append(row)
        if CARRIER.search(name):
            carrier_files.append(row)

    hit = bool(metadata_stoneage or metadata_gametime and isbn_hits or isbn_hits or exact_files or stoneage_files)
    return {
        "identifier": identifier,
        "meta": meta,
        "files": files,
        "metadata_stoneage": metadata_stoneage,
        "metadata_gametime": metadata_gametime,
        "isbn_hits": isbn_hits,
        "exact_files": exact_files,
        "stoneage_files": stoneage_files,
        "carrier_files": carrier_files,
        "hit": hit,
    }


def main():
    print("StoneAge IA preservation-uploader reverse-index probe — R1")
    print("SCOPE|internet-archive-metadata-and-file-lists-only|no-payload-download")
    print("UPLOADERS|" + ",".join(UPLOADERS))
    print("GUIDE_ISBNS|" + ",".join(GUIDE_ISBNS))
    print(
        f"LIMIT|rows_per_page={ROWS_PER_PAGE}|max_pages_per_uploader={MAX_PAGES_PER_UPLOADER}|"
        f"max_items={MAX_ITEMS}"
    )

    docs = {}
    errors = []
    uploader_counts = {}

    for uploader in UPLOADERS:
        query = f'uploader:"{uploader}" AND mediatype:software'
        total = None
        returned = 0
        for page in range(1, MAX_PAGES_PER_UPLOADER + 1):
            try:
                response = search(query, page)
            except Exception as exc:
                errors.append(("uploader-search", f"{uploader}:page{page}", type(exc).__name__, str(exc)))
                break
            if total is None:
                total = int(response.get("numFound", 0) or 0)
            rows = response.get("docs", [])
            returned += len(rows)
            print(
                f"QUERY|kind=uploader-all|uploader={clean(uploader)}|page={page}|"
                f"numFound={response.get('numFound',0)}|returned={len(rows)}"
            )
            for doc in rows:
                identifier = str(doc.get("identifier", "")).strip()
                if identifier:
                    docs.setdefault(identifier, doc)
            if len(rows) < ROWS_PER_PAGE or len(docs) >= MAX_ITEMS:
                break
        uploader_counts[uploader] = (total or 0, returned)

    for index, query in enumerate(GLOBAL_QUERIES, 1):
        try:
            response = search(query, 1, ROWS_PER_PAGE)
        except Exception as exc:
            errors.append(("global-search", str(index), type(exc).__name__, str(exc)))
            continue
        rows = response.get("docs", [])
        print(
            f"QUERY|kind=global-exact|n={index}|numFound={response.get('numFound',0)}|"
            f"returned={len(rows)}|q={clean(query)}"
        )
        for doc in rows:
            identifier = str(doc.get("identifier", "")).strip()
            if identifier:
                docs.setdefault(identifier, doc)

    identifiers = sorted(docs)[:MAX_ITEMS]
    print(f"COUNT|unique_items_selected|{len(identifiers)}")

    def one(identifier):
        try:
            return inspect_item(identifier, docs.get(identifier)), None
        except Exception as exc:
            return None, (identifier, type(exc).__name__, str(exc))

    hits = []
    inspected = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_METADATA_WORKERS) as executor:
        for result, error in executor.map(one, identifiers):
            if error:
                errors.append(("metadata", error[0], error[1], error[2]))
                continue
            inspected += 1
            if result["hit"]:
                hits.append(result)

    print(f"COUNT|metadata_inspected|{inspected}")
    print(f"COUNT|hits|{len(hits)}")
    print(f"COUNT|errors|{len(errors)}")
    for uploader, (total, returned) in uploader_counts.items():
        print(f"UPLOADER_COUNT|uploader={clean(uploader)}|numFound={total}|enumerated={returned}")
    for phase, key, kind, message in errors:
        print(
            f"ERROR|phase={clean(phase)}|key={clean(key)}|kind={clean(kind)}|"
            f"message={clean(message)}"
        )

    for result in sorted(hits, key=lambda row: row["identifier"].lower()):
        meta = result["meta"]
        print(
            f"HIT|identifier={clean(result['identifier'])}|title={clean(meta.get('title'))}|"
            f"date={clean(meta.get('date') or meta.get('year'))}|uploader={clean(meta.get('uploader'))}|"
            f"metadata_stoneage={int(result['metadata_stoneage'])}|"
            f"metadata_gametime={int(result['metadata_gametime'])}|"
            f"isbn={','.join(result['isbn_hits'])}|exact_files={len(result['exact_files'])}|"
            f"stoneage_files={len(result['stoneage_files'])}|carrier_files={len(result['carrier_files'])}"
        )
        emitted = set()
        for kind, rows in (
            ("exact-target", result["exact_files"]),
            ("stoneage-name", result["stoneage_files"]),
        ):
            for row in rows:
                name = str(row.get("name", ""))
                key = (kind, name)
                if key in emitted:
                    continue
                emitted.add(key)
                print(
                    f"FILE|identifier={clean(result['identifier'])}|kind={kind}|name={clean(name)}|"
                    f"size={clean(row.get('size'))}|md5={clean(row.get('md5'))}|"
                    f"sha1={clean(row.get('sha1'))}|format={clean(row.get('format'))}|"
                    f"source={clean(row.get('source'))}"
                )
        if not emitted:
            for row in result["carrier_files"][:10]:
                print(
                    f"CARRIER|identifier={clean(result['identifier'])}|name={clean(row.get('name'))}|"
                    f"size={clean(row.get('size'))}|md5={clean(row.get('md5'))}|"
                    f"sha1={clean(row.get('sha1'))}|format={clean(row.get('format'))}"
                )


if __name__ == "__main__":
    main()
