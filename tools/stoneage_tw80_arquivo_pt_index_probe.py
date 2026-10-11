"""Independent, read-only Arquivo.pt index fallback for a historical 2005 Wayi page.

Only HTTPS source-URL metadata queries. No historic HTML / game binary downloads.
A timeout or empty response is never evidence of missing original game files.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ORIGINAL_URL = "http://www.wayi.com.tw/stoneage/actives/940329/page_3.html"
BASE = "https://arquivo.pt/textsearch"
MAX_ITEMS = 12
MAX_RESPONSE_BYTES = 131072
TIMEOUT = 9


def build_query() -> str:
    return BASE + "?" + urlencode({
        "versionHistory": ORIGINAL_URL,
        "from": "2005",
        "to": "2007",
        "maxItems": str(MAX_ITEMS),
        "prettyPrint": "false",
    })


def normalize_url(url: str) -> str:
    if not isinstance(url, str):
        raise ValueError("Non-string archive origin")
    return url.replace("https://", "http://", 1).lower().rstrip("/")


def parse_index(document: object) -> list[dict]:
    if not isinstance(document, dict) or not isinstance(document.get("response_items"), list):
        raise ValueError("Expected response_items list missing")
    rows = document["response_items"]
    if len(rows) > MAX_ITEMS:
        raise ValueError("Too many index records")
    out = []
    for entry in rows:
        if not isinstance(entry, dict):
            raise ValueError("Invalid index entry")
        origin = entry.get("originalURL")
        if normalize_url(origin) != normalize_url(ORIGINAL_URL):
            raise ValueError("Unrelated archive original URL")
        stamp = entry.get("tstamp")
        if not isinstance(stamp, str) or not stamp.isascii() or len(stamp) != 14 or not stamp.isdecimal():
            raise ValueError("Malformed archived timestamp")
        datetime.strptime(stamp, "%Y%m%d%H%M%S")
        if not (2005 <= int(stamp[:4]) <= 2007):
            raise ValueError("Out-of-period archived capture")
        digest = entry.get("digest")
        if digest is not None and (not isinstance(digest, str) or len(digest) > 100):
            raise ValueError("Malformed archive digest")
        mime = entry.get("mimeType")
        if mime is not None and (not isinstance(mime, str) or len(mime) > 80):
            raise ValueError("Malformed MIME type")
        archive_url = entry.get("linkToArchive")
        if archive_url is not None and (not isinstance(archive_url, str) or not archive_url.startswith("https://arquivo.pt/wayback/")):
            raise ValueError("Non-provider archive reference")
        out.append({
            "archived_timestamp": stamp,
            "original_url": origin,
            "archive_index_digest": digest,
            "index_mimetype": mime,
            "archive_reference_not_fetched": archive_url,
        })
    return out


def summarize_response(raw: str | None = None, *, error: str | None = None) -> dict:
    result = {
        "schema": "stoneage-tw80-arquivo-pt-index-fallback-r1",
        "provider": "Arquivo.pt",
        "source_url": ORIGINAL_URL,
        "index_url": build_query(),
        "requested_years": [2005, 2006, 2007],
        "probe_status": "NOT_STARTED",
        "index_records": [],
        "original_page_body_obtained": False,
        "original_2005_taiwan_installer_obtained": False,
        "publisher_binary_sha256_verified": False,
        "native_pet_equipment_runtime_verified": False,
    }
    if error is not None:
        result.update(probe_status="NETWORK_INDETERMINATE", error_class=error)
        return result
    try:
        rows = parse_index(json.loads(raw))
    except (TypeError, ValueError) as exc:
        result.update(probe_status="INVALID_OR_UNEXPECTED_INDEX_RESPONSE", error_class=type(exc).__name__)
        return result
    result.update(
        probe_status="INDEX_METADATA_FOUND_PAGE_UNVERIFIED" if rows else "EMPTY_INDEX_NOT_PROOF_OF_ABSENCE",
        index_records=rows,
    )
    return result


def fetch_index() -> dict:
    req = Request(
        build_query(),
        headers={"Accept": "application/json", "User-Agent": "StoneAge-Research-Metadata-Only/1.0"},
    )
    try:
        with urlopen(req, timeout=TIMEOUT) as response:
            data = response.read(MAX_RESPONSE_BYTES + 1)
        if len(data) > MAX_RESPONSE_BYTES:
            return summarize_response(error="INDEX_RESPONSE_TOO_LARGE")
        return summarize_response(data.decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, UnicodeError) as exc:
        return summarize_response(error=type(exc).__name__)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--probe", action="store_true", help="Fetch a bounded read-only Arquivo.pt index")
    args = p.parse_args()
    if args.probe:
        print(json.dumps(fetch_index(), indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(json.dumps({
            "probe_status": "OFFLINE_READY",
            "source_url": ORIGINAL_URL,
            "index_url": build_query(),
            "original_page_body_obtained": False,
            "original_2005_taiwan_installer_obtained": False,
        }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
