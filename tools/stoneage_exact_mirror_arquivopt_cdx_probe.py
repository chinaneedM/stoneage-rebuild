#!/usr/bin/env python3
"""Probe Arquivo.pt CDX API for exact early Korean StoneAge mirror targets.

Only CDX index metadata is stored. No archived page or client payload is downloaded.
"""

from __future__ import annotations

import concurrent.futures
import json
import time
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://arquivo.pt/wayback/cdx"

TARGETS = [
    ("cnet-stoneage-zip", "http://korea.cnet.com/pc/games/online/stoneage.zip"),
    ("cnet-stoneage-zip-www", "http://www.korea.cnet.com/pc/games/online/stoneage.zip"),
    ("hananet-sa-exe", "http://stoneage.hananet.net/down/sa.exe"),
    ("hananet-sa-exe-www", "http://www.stoneage.hananet.net/down/sa.exe"),
    ("hananet-sa-demo-exe", "http://stoneage.hananet.net/down/sa_demo.exe"),
    ("hananet-sa-demo-exe-www", "http://www.stoneage.hananet.net/down/sa_demo.exe"),
    ("gagamel-stoneagebeta", "http://www.gagamel.com/web_data/download/stoneagebeta.zip"),
    ("gagamel-stoneagebeta-bare", "http://gagamel.com/web_data/download/stoneagebeta.zip"),
    ("hananet-pds-record", "http://pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"),
    ("hananet-pds-record-www", "http://www.pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"),
    ("gametime-gw9", "http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("gametime-gw9-bare", "http://gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("gametime-early", "http://www.gametime.co.kr/webzine/online/download.asp?name=스톤에이지"),
    ("gametime-early-bare", "http://gametime.co.kr/webzine/online/download.asp?name=스톤에이지"),
]


def fetch_bytes(url: str, timeout: int = 12, attempts: int = 2) -> bytes:
    last = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": UA, "Accept": "application/json,text/plain,*/*"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1.5)
    raise last


def parse_rows(data: bytes):
    text = data.decode("utf-8", "replace").strip()
    if not text:
        return []

    # Arquivo.pt CDX commonly returns JSON arrays, but some deployments expose
    # newline-delimited CDXJ objects. Accept both so the probe remains robust.
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        rows = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if not line.startswith("{"):
                brace = line.find("{")
                if brace >= 0:
                    line = line[brace:]
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict):
                rows.append(item)
        return rows

    if isinstance(obj, list):
        if obj and isinstance(obj[0], list):
            header = obj[0]
            return [dict(zip(header, row)) for row in obj[1:] if isinstance(row, list)]
        return [x for x in obj if isinstance(x, dict)]

    if isinstance(obj, dict):
        # Different CDX-server wrappers use one of these list keys.
        for key in ("results", "captures", "response", "items"):
            val = obj.get(key)
            if isinstance(val, list):
                return [x for x in val if isinstance(x, dict)]
        return [obj] if any(k in obj for k in ("url", "original", "timestamp")) else []

    return []


def query_url(original: str) -> str:
    params = {
        "url": original,
        "from": "2000",
        "to": "2005",
        "limit": "200",
        "output": "json",
        "filter": "statuscode:200",
    }
    return CDX + "?" + urllib.parse.urlencode(params)


def query_one(label: str, original: str):
    url = query_url(original)
    try:
        rows = parse_rows(fetch_bytes(url))
        return label, original, rows, None
    except Exception as exc:
        return label, original, [], (type(exc).__name__, str(exc))


def clean(value, limit=900):
    value = "" if value is None else str(value)
    value = " ".join(value.split())
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def normalize_row(row):
    return {
        "timestamp": row.get("timestamp") or row.get("date") or row.get("datetime") or "",
        "original": row.get("original") or row.get("url") or row.get("originalURL") or "",
        "status": row.get("statuscode") or row.get("status") or "",
        "mime": row.get("mimetype") or row.get("mime") or row.get("mimeType") or "",
        "digest": row.get("digest") or "",
        "length": row.get("length") or row.get("contentLength") or "",
        "filename": row.get("filename") or "",
        "offset": row.get("offset") or "",
        "collection": row.get("collection") or "",
    }


def main():
    print("StoneAge exact-mirror Arquivo.pt CDX probe — R1")
    print("SCOPE|cdx-index-metadata-only|no-archived-page-download|no-client-binary-download")
    print("YEARS|2000-2005")

    results = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(query_one, label, original) for label, original in TARGETS]
        for fut in futures:
            label, original, rows, error = fut.result()
            if error:
                errors.append((label, original, error[0], error[1]))
                continue
            for row in rows:
                results.append((label, original, normalize_row(row)))

    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|raw_results|{len(results)}")

    for label, original, kind, message in sorted(errors):
        print(
            f"ERROR|target={clean(label)}|kind={clean(kind)}|"
            f"original={clean(original)}|message={clean(message)}"
        )

    emitted = set()
    for label, original, row in results:
        record = (
            clean(label),
            clean(row["timestamp"]),
            clean(row["status"]),
            clean(row["mime"]),
            clean(row["length"]),
            clean(row["digest"]),
            clean(row["filename"]),
            clean(row["offset"]),
            clean(row["collection"]),
            clean(row["original"] or original),
        )
        emitted.add(record)

    print(f"COUNT|unique_results|{len(emitted)}")
    for record in sorted(emitted):
        print("RESULT|" + "|".join(record))


if __name__ == "__main__":
    main()
