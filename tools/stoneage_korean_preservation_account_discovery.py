#!/usr/bin/env python3
"""Discover Korean game-preservation uploader accounts from the existing IA carrier corpus.

This pass starts from the repository's already-vetted Korean historical CD corpus result,
resolves each carrier item's Internet Archive uploader metadata, ranks uploader accounts,
and runs exact StoneAge metadata searches inside each discovered uploader namespace.
Metadata/file-list only; no carrier payload bytes are downloaded.
"""

from __future__ import annotations

import concurrent.futures
import json
import pathlib
import re
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
ADV = "https://archive.org/advancedsearch.php"
META = "https://archive.org/metadata/{}"
CORPUS_PATH = pathlib.Path("research/recovered/STONEAGE-KOREAN-HISTORICAL-CD-CORPUS-R1.txt")

ITEM_RE = re.compile(r"^ITEM\|identifier=([^|]+)\|")
STONEAGE_QUERY = '(StoneAge OR "Stone Age" OR "스톤에이지")'
MAX_WORKERS = 8
MAX_UPLOADERS = 20


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


def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier, safe="")))


def search(query, rows=50):
    params = [
        ("q", query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "description"),
        ("fl[]", "date"),
        ("fl[]", "year"),
        ("fl[]", "uploader"),
        ("fl[]", "mediatype"),
        ("rows", str(rows)),
        ("page", "1"),
        ("output", "json"),
    ]
    return get_json(ADV + "?" + urllib.parse.urlencode(params)).get("response", {})


def parse_identifiers(text):
    out = []
    seen = set()
    for line in text.splitlines():
        match = ITEM_RE.match(line)
        if not match:
            continue
        identifier = match.group(1).strip()
        if identifier and identifier not in seen:
            seen.add(identifier)
            out.append(identifier)
    return out


def main():
    print("StoneAge Korean preservation-account discovery — R1")
    print("SCOPE|existing-vetted-IA-carrier-items-to-uploader-metadata|no-payload-download")
    print(f"CORPUS|path={CORPUS_PATH.as_posix()}")

    if not CORPUS_PATH.exists():
        raise SystemExit(f"missing corpus result: {CORPUS_PATH}")

    identifiers = parse_identifiers(CORPUS_PATH.read_text(encoding="utf-8"))
    print(f"COUNT|seed_items|{len(identifiers)}")

    errors = []
    rows = []

    def one(identifier):
        try:
            return identifier, metadata(identifier), None
        except Exception as exc:
            return identifier, None, (type(exc).__name__, str(exc))

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for identifier, data, error in executor.map(one, identifiers):
            if error:
                errors.append(("metadata", identifier, error[0], error[1]))
                continue
            meta = data.get("metadata", {})
            uploader = clean(meta.get("uploader"), 500)
            title = clean(meta.get("title"), 700)
            date = clean(meta.get("date") or meta.get("year"), 120)
            collection = clean(meta.get("collection"), 1200)
            rows.append((identifier, uploader, title, date, collection))
            print(
                f"SEED|identifier={clean(identifier)}|uploader={uploader}|"
                f"title={title}|date={date}|collection={collection}"
            )

    counts = Counter(uploader for _, uploader, _, _, _ in rows if uploader)
    examples = defaultdict(list)
    for identifier, uploader, title, date, collection in rows:
        if uploader and len(examples[uploader]) < 6:
            examples[uploader].append((identifier, title, date))

    ranked = counts.most_common(MAX_UPLOADERS)
    print(f"COUNT|metadata_resolved|{len(rows)}")
    print(f"COUNT|distinct_uploaders|{len(counts)}")
    print(f"COUNT|errors_so_far|{len(errors)}")

    for uploader, count in ranked:
        print(f"UPLOADER|name={clean(uploader)}|seed_items={count}")
        for identifier, title, date in examples[uploader]:
            print(
                f"UPLOADER_SAMPLE|uploader={clean(uploader)}|identifier={clean(identifier)}|"
                f"title={clean(title)}|date={clean(date)}"
            )

    stoneage_hits = []
    for uploader, count in ranked:
        query = f'uploader:"{uploader.replace(chr(34), chr(92)+chr(34))}" AND mediatype:software AND {STONEAGE_QUERY}'
        try:
            response = search(query, 50)
        except Exception as exc:
            errors.append(("uploader-search", uploader, type(exc).__name__, str(exc)))
            continue
        docs = response.get("docs", [])
        print(
            f"QUERY|uploader={clean(uploader)}|seed_items={count}|"
            f"numFound={response.get('numFound',0)}|returned={len(docs)}|q={clean(query)}"
        )
        for doc in docs:
            identifier = str(doc.get("identifier", "")).strip()
            if not identifier:
                continue
            stoneage_hits.append((uploader, doc))
            print(
                f"STONEAGE_HIT|uploader={clean(uploader)}|identifier={clean(identifier)}|"
                f"title={clean(doc.get('title'))}|date={clean(doc.get('date') or doc.get('year'))}"
            )

    print(f"COUNT|stoneage_metadata_hits|{len(stoneage_hits)}")
    print(f"COUNT|errors|{len(errors)}")
    for phase, key, kind, message in errors:
        print(
            f"ERROR|phase={clean(phase)}|key={clean(key)}|kind={clean(kind)}|"
            f"message={clean(message)}"
        )


if __name__ == "__main__":
    main()
