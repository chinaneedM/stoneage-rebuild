#!/usr/bin/env python3
"""Bounded Internet Archive uploader-neighborhood probe for missing Korean NetPower carriers.

Starting from already-known public Korean magazine/CD items, resolve their IA uploader
identities, search only those uploader neighborhoods plus a small exact NetPower/month
query set, and inspect item file lists for carrier images. No carrier payload bytes are
read or committed.
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

ANCHORS = (
    "pcgm-cd-dump",
    "GAMEPIA_cd_dump",
    "20230716_20230716_0953",
)

TARGET_MONTHS = (
    "2000-11",
    "2000-12",
    "2001-01",
    "2001-02",
)

CARRIER = re.compile(r"(?i)\.(?:iso|img|bin|mdf|nrg|ccd|cue)$")
NETPOWER = re.compile(r"(?i)(net\s*power|netpower|넷\s*파워|넷파워)")
MONTH_PATTERNS = {
    "2000-11": re.compile(r"(?i)(2000[-_./ ]?11|2000년\s*11월|0011(?:\D|$))"),
    "2000-12": re.compile(r"(?i)(2000[-_./ ]?12|2000년\s*12월|0012(?:\D|$))"),
    "2001-01": re.compile(r"(?i)(2001[-_./ ]?0?1|2001년\s*1월|0101(?:\D|$))"),
    "2001-02": re.compile(r"(?i)(2001[-_./ ]?0?2|2001년\s*2월|0102(?:\D|$))"),
}

MAX_ROWS = 200
MAX_METADATA = 120


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


def search(query):
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
        ("rows", str(MAX_ROWS)),
        ("page", "1"),
        ("output", "json"),
    ]
    return get_json(ADV + "?" + urllib.parse.urlencode(params)).get("response", {})


def month_hits(text):
    return [month for month, pattern in MONTH_PATTERNS.items() if pattern.search(text)]


def carrier_rows(data):
    out = []
    for file_row in data.get("files", []):
        name = str(file_row.get("name", ""))
        if not CARRIER.search(name):
            continue
        out.append(
            {
                "name": name,
                "size": int(file_row.get("size") or 0),
                "md5": str(file_row.get("md5", "")),
                "sha1": str(file_row.get("sha1", "")),
                "format": str(file_row.get("format", "")),
                "source": str(file_row.get("source", "")),
            }
        )
    return out


def candidate_score(doc, carriers):
    blob = " ".join(
        [
            clean(doc.get("identifier"), 500),
            clean(doc.get("title"), 1200),
            clean(doc.get("description"), 2200),
            clean(doc.get("date") or doc.get("year"), 200),
            " ".join(clean(row["name"], 1000) for row in carriers),
        ]
    )
    months = month_hits(blob)
    has_netpower = bool(NETPOWER.search(blob))
    score = (2 if has_netpower else 0) + len(months)
    return score, has_netpower, months


def exact_queries():
    queries = []
    for month in TARGET_MONTHS:
        year, mm = month.split("-")
        month_num = str(int(mm))
        queries.extend(
            [
                f'(title:"NetPower" OR title:"Net Power" OR title:"넷파워") AND ({year} AND {month_num})',
                f'(description:"NetPower" OR description:"Net Power" OR description:"넷파워") AND ({year} AND {month_num})',
            ]
        )
    return tuple(queries)


def main():
    print("StoneAge NetPower IA uploader-neighborhood probe — R1")
    print("SCOPE|internet-archive-metadata-and-file-lists-only|no-carrier-payload-download")
    print("TARGET|months=" + ",".join(TARGET_MONTHS))
    print("ANCHORS|" + ",".join(ANCHORS))

    errors = []
    anchor_meta = {}
    uploaders = set()

    for identifier in ANCHORS:
        try:
            data = metadata(identifier)
        except Exception as exc:
            errors.append(("anchor-metadata", identifier, type(exc).__name__, str(exc)))
            continue
        meta = data.get("metadata", {})
        uploader = clean(meta.get("uploader"), 500)
        anchor_meta[identifier] = {
            "title": clean(meta.get("title"), 500),
            "uploader": uploader,
        }
        if uploader:
            uploaders.add(uploader)
        print(
            f"ANCHOR|identifier={clean(identifier)}|title={clean(meta.get('title'))}|"
            f"uploader={uploader}|files={len(data.get('files', []))}"
        )

    queries = []
    for uploader in sorted(uploaders):
        quoted = uploader.replace('"', '\\"')
        queries.extend(
            [
                ("uploader-netpower", uploader, f'uploader:"{quoted}" AND (NetPower OR "Net Power" OR 넷파워)'),
                ("uploader-period", uploader, f'uploader:"{quoted}" AND mediatype:software AND year:[2000 TO 2001]'),
            ]
        )
    for query in exact_queries():
        queries.append(("global-exact", "", query))

    docs = {}
    for index, (kind, uploader, query) in enumerate(queries, 1):
        try:
            response = search(query)
        except Exception as exc:
            errors.append(("search", str(index), type(exc).__name__, str(exc)))
            continue
        rows = response.get("docs", [])
        print(
            f"QUERY|n={index}|kind={kind}|uploader={clean(uploader)}|"
            f"numFound={response.get('numFound', 0)}|returned={len(rows)}|q={clean(query)}"
        )
        for doc in rows:
            identifier = str(doc.get("identifier", "")).strip()
            if identifier:
                docs.setdefault(identifier, doc)

    print(f"COUNT|uploaders|{len(uploaders)}")
    print(f"COUNT|unique_search_items|{len(docs)}")

    selected_ids = list(sorted(docs))[:MAX_METADATA]

    def one(identifier):
        try:
            return identifier, metadata(identifier), None
        except Exception as exc:
            return identifier, None, (type(exc).__name__, str(exc))

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for identifier, data, error in executor.map(one, selected_ids):
            if error:
                errors.append(("metadata", identifier, error[0], error[1]))
                continue
            carriers = carrier_rows(data)
            meta = data.get("metadata", {})
            merged = dict(docs.get(identifier, {}))
            merged.update(meta)
            score, has_netpower, months = candidate_score(merged, carriers)
            if score > 0:
                results.append((score, identifier, merged, carriers, has_netpower, months))

    results.sort(key=lambda row: (-row[0], row[1].lower()))
    print(f"COUNT|metadata_inspected|{len(selected_ids)}")
    print(f"COUNT|target_candidates|{len(results)}")
    print(f"COUNT|errors|{len(errors)}")

    for phase, key, kind, message in errors:
        print(
            f"ERROR|phase={clean(phase)}|key={clean(key)}|kind={clean(kind)}|"
            f"message={clean(message)}"
        )

    for score, identifier, meta, carriers, has_netpower, months in results:
        print(
            f"CANDIDATE|score={score}|identifier={clean(identifier)}|"
            f"title={clean(meta.get('title'))}|date={clean(meta.get('date') or meta.get('year'))}|"
            f"uploader={clean(meta.get('uploader'))}|netpower={int(has_netpower)}|"
            f"months={','.join(months)}|carrier_count={len(carriers)}"
        )
        for row in sorted(carriers, key=lambda x: x["name"].lower()):
            file_months = month_hits(row["name"])
            if file_months or NETPOWER.search(row["name"]):
                print(
                    f"CARRIER|identifier={clean(identifier)}|name={clean(row['name'])}|"
                    f"months={','.join(file_months)}|size={row['size']}|"
                    f"md5={clean(row['md5'])}|sha1={clean(row['sha1'])}|"
                    f"format={clean(row['format'])}|source={clean(row['source'])}"
                )


if __name__ == "__main__":
    main()
