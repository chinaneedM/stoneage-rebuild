#!/usr/bin/env python3
"""Search Internet Archive metadata for the 2001 Korean StoneAge guide bonus CD.

Only public item metadata and file-list metadata are emitted.
No archive/CD payload is downloaded.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
ADV = "https://archive.org/advancedsearch.php"
META = "https://archive.org/metadata/{}"

QUERIES = [
    'identifier:9788995182123 OR identifier:8995182121',
    '"9788995182123" OR "8995182121"',
    'title:("스톤에이지" OR "스톤 에이지") AND ("게임타임" OR "GameTime")',
    'description:("스톤에이지" OR "StoneAge" OR "Stone Age") AND description:("게임타임" OR "GameTime")',
    '("스톤에이지 퍼펙트 가이드" OR "StoneAge Perfect Guide")',
]

INTEREST_EXT = re.compile(
    r"(?i)\.(?:iso|bin|cue|img|mdf|mds|nrg|ccd|sub|zip|rar|7z|exe|cab|msi)$"
)


def get_json(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def search(query):
    params = [
        ("q", query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "description"),
        ("fl[]", "date"),
        ("fl[]", "year"),
        ("fl[]", "mediatype"),
        ("fl[]", "collection"),
        ("fl[]", "creator"),
        ("rows", "100"),
        ("page", "1"),
        ("output", "json"),
    ]
    return get_json(ADV + "?" + urllib.parse.urlencode(params))


def clean(value):
    if value is None:
        return ""
    if isinstance(value, list):
        value = ",".join(str(x) for x in value)
    value = " ".join(str(value).split())
    return value.replace("|", "%7C")[:600]


def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier, safe="")))


def main():
    print("StoneAge GameTime 2001 bonus-CD Internet Archive metadata probe — R1")
    print("SCOPE|metadata-only|no-item-payload-download")

    docs = {}
    for idx, query in enumerate(QUERIES, 1):
        try:
            data = search(query)
        except Exception as exc:
            print(f"ERROR|query={idx}|{type(exc).__name__}|{clean(exc)}")
            continue
        response = data.get("response", {})
        found = response.get("numFound", 0)
        print(f"QUERY|{idx}|numFound={found}|q={clean(query)}")
        for doc in response.get("docs", []):
            ident = str(doc.get("identifier", "")).strip()
            if ident:
                docs.setdefault(ident, doc)

    print(f"COUNT|unique_items|{len(docs)}")
    for ident in sorted(docs, key=str.lower):
        doc = docs[ident]
        print(
            "ITEM|"
            + "|".join(
                [
                    f"identifier={clean(ident)}",
                    f"title={clean(doc.get('title'))}",
                    f"date={clean(doc.get('date') or doc.get('year'))}",
                    f"mediatype={clean(doc.get('mediatype'))}",
                    f"creator={clean(doc.get('creator'))}",
                    f"collection={clean(doc.get('collection'))}",
                ]
            )
        )
        try:
            meta = metadata(ident)
        except Exception as exc:
            print(f"META_ERROR|identifier={clean(ident)}|{type(exc).__name__}|{clean(exc)}")
            continue
        files = meta.get("files", [])
        interesting = []
        for f in files:
            name = str(f.get("name", ""))
            if INTEREST_EXT.search(name):
                interesting.append(
                    (
                        name,
                        f.get("size", ""),
                        f.get("md5", ""),
                        f.get("sha1", ""),
                        f.get("source", ""),
                    )
                )
        print(f"FILE_COUNT|identifier={clean(ident)}|interesting={len(interesting)}|total={len(files)}")
        for name, size, md5, sha1, source in sorted(interesting, key=lambda x: x[0].lower()):
            print(
                "FILE|"
                + "|".join(
                    [
                        f"identifier={clean(ident)}",
                        f"name={clean(name)}",
                        f"size={clean(size)}",
                        f"md5={clean(md5)}",
                        f"sha1={clean(sha1)}",
                        f"source={clean(source)}",
                    ]
                )
            )


if __name__ == "__main__":
    main()
