#!/usr/bin/env python3
"""Probe early Waei central-download routes without dropping redirects.

The earlier central-download census intentionally kept HTTP 200 rows and
collapsed URL keys. That is useful for preserved payload/listing inventory,
but it can hide router captures such as download.asp?fileid=133, whose
historical response is a 302. This probe keeps every status and every capture
in the Dec-2000/Feb-2001 trial-client window, and uses fileid=133 in June 2001
as a positive archive-method control.

Metadata only: no archived HTML body and no binary payload is replayed.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
FIELDS = "timestamp,original,statuscode,mimetype,digest,length,redirect"
EARLY_FROM = "20001215"
EARLY_TO = "20010228"
CONTROL_FROM = "20010601"
CONTROL_TO = "20010610"

TARGETS = (
    ("detail-id2", "http://www7.waei.net/download/dldetial.asp?ID=2", "exact", EARLY_FROM, EARLY_TO, "early"),
    ("detail-id2-port80", "http://www7.waei.net:80/download/dldetial.asp?ID=2", "exact", EARLY_FROM, EARLY_TO, "early"),
    ("router", "http://www7.waei.net/download/download.asp", "prefix", EARLY_FROM, EARLY_TO, "early"),
    ("router-port80", "http://www7.waei.net:80/download/download.asp", "prefix", EARLY_FROM, EARLY_TO, "early"),
    ("file-prefix", "http://www7.waei.net/download/file/", "prefix", EARLY_FROM, EARLY_TO, "early"),
    ("file-prefix-port80", "http://www7.waei.net:80/download/file/", "prefix", EARLY_FROM, EARLY_TO, "early"),
    ("control-fileid133", "http://www7.waei.net/download/download.asp?fileid=133", "exact", CONTROL_FROM, CONTROL_TO, "control"),
    ("control-fileid133-port80", "http://www7.waei.net:80/download/download.asp?fileid=133", "exact", CONTROL_FROM, CONTROL_TO, "control"),
)

STONE_TOKENS = ("stoneage", "stone_age", "stone-age", "shiqi", "stone")


def clean(value, limit=6000):
    return " ".join(str(value if value is not None else "").split()).replace("|", "%7C")[:limit]


def fetch(url, timeout=75, max_bytes=16 * 1024 * 1024):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json,text/plain,*/*;q=0.2",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise ValueError(f"response-too-large:{len(body)}")
        return int(getattr(response, "status", response.getcode())), response.geturl(), body


def cdx_url(url, match, start, end):
    # Deliberately NO status filter and NO collapse=urlkey.
    params = [
        ("url", url),
        ("matchType", match),
        ("output", "json"),
        ("fl", FIELDS),
        ("from", start),
        ("to", end),
        ("limit", "50000"),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def parse(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, row)) for row in obj[1:] if isinstance(row, list))


def fileid(url):
    text = str(url or "")
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(text).query)
    for key in ("fileid", "FileID", "FILEID", "id", "ID"):
        vals = q.get(key)
        if vals and str(vals[0]).isdigit():
            return str(vals[0])
    m = re.search(r"(?:[?&](?:fileid|id)=)(\d+)", text, flags=re.I)
    return m.group(1) if m else ""


def basename(url):
    path = urllib.parse.unquote(urllib.parse.urlsplit(str(url or "")).path)
    return path.rsplit("/", 1)[-1]


def is_router(url):
    return "/download/download.asp" in str(url or "").lower()


def is_file(url):
    return "/download/file/" in str(url or "").lower()


def stone_hint(*values):
    text = " ".join(urllib.parse.unquote_plus(str(v or "")).lower() for v in values)
    return any(token in text for token in STONE_TOKENS)


def main():
    print("StoneAge Waei early central-download redirect census — R1")
    print(
        "SCOPE|Wayback CDX metadata only|early={}..{}|control={}..{}|all statuses|no urlkey collapse|no archived-body|no binary payload".format(
            EARLY_FROM, EARLY_TO, CONTROL_FROM, CONTROL_TO
        )
    )
    row_map = {}
    errors = []
    query_counts = {}

    for label, url, match, start, end, scope in TARGETS:
        try:
            status, final, body = fetch(cdx_url(url, match, start, end))
            rows = parse(body)
            query_counts[label] = len(rows)
            print(
                "QUERY|label={}|scope={}|status={}|rows={}|bytes={}|sha256={}|final={}".format(
                    clean(label), clean(scope), status, len(rows), len(body),
                    hashlib.sha256(body).hexdigest(), clean(final)
                )
            )
            for row in rows:
                key = (
                    str(row.get("timestamp") or ""),
                    str(row.get("original") or ""),
                    str(row.get("statuscode") or ""),
                    str(row.get("digest") or ""),
                    str(row.get("redirect") or ""),
                )
                entry = row_map.setdefault(key, {"row": row, "scopes": set(), "labels": set()})
                entry["scopes"].add(scope)
                entry["labels"].add(label)
        except Exception as exc:
            errors.append((label, scope, type(exc).__name__, str(exc)))

    entries = sorted(
        row_map.values(),
        key=lambda e: (
            str(e["row"].get("timestamp") or ""),
            str(e["row"].get("original") or ""),
            ",".join(sorted(e["labels"])),
        ),
    )

    early = []
    control = []
    early_router = []
    early_redirects = []
    early_files = []
    hint_rows = []
    statuses = collections.Counter()

    for entry in entries:
        row = entry["row"]
        scopes = entry["scopes"]
        original = str(row.get("original") or "")
        redirect = str(row.get("redirect") or "")
        status = str(row.get("statuscode") or "")
        labels = ",".join(sorted(entry["labels"]))
        scope_text = ",".join(sorted(scopes))
        fid = fileid(original)
        hint = stone_hint(original, redirect)
        statuses[status] += 1

        if "early" in scopes:
            early.append(entry)
            if is_router(original):
                early_router.append(entry)
            if status.startswith("3"):
                early_redirects.append(entry)
            if is_file(original):
                early_files.append(entry)
        if "control" in scopes:
            control.append(entry)
        if hint:
            hint_rows.append(entry)

        print(
            "ROW|scope={}|labels={}|timestamp={}|status={}|fileid={}|stone_hint={}|basename={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                clean(scope_text), clean(labels), clean(row.get("timestamp")), clean(status),
                clean(fid), int(hint), clean(basename(original), 1200), clean(row.get("mimetype")),
                clean(row.get("length")), clean(row.get("digest")), clean(redirect), clean(original)
            )
        )

    for status, count in sorted(statuses.items()):
        print(f"STATUS_COUNT|status={clean(status)}|count={count}")
    for label in sorted(query_counts):
        print(f"QUERY_COUNT|label={clean(label)}|count={query_counts[label]}")

    control_133 = [
        e for e in control
        if fileid(e["row"].get("original")) == "133"
    ]
    control_302 = [
        e for e in control_133
        if str(e["row"].get("statuscode") or "").startswith("3")
    ]

    print(f"COUNT|unique_rows|{len(entries)}")
    print(f"COUNT|early_rows|{len(early)}")
    print(f"COUNT|early_router_rows|{len(early_router)}")
    print(f"COUNT|early_redirect_rows|{len(early_redirects)}")
    print(f"COUNT|early_file_rows|{len(early_files)}")
    print(f"COUNT|stone_hint_rows|{len(hint_rows)}")
    print(f"COUNT|control_rows|{len(control)}")
    print(f"COUNT|control_fileid133_rows|{len(control_133)}")
    print(f"COUNT|control_fileid133_redirect_rows|{len(control_302)}")
    for label, scope, kind, message in errors:
        print(
            "ERROR|label={}|scope={}|kind={}|message={}".format(
                clean(label), clean(scope), clean(kind), clean(message)
            )
        )
    print(f"COUNT|errors|{len(errors)}")

    if early_router:
        print("RESOLUTION|EARLY_ROUTER_ROWS_FOUND|inspect exact fileids/redirect targets next")
    elif early_files:
        print("RESOLUTION|EARLY_FILE_NAMESPACE_ROWS_FOUND|inspect exact filenames/captures next")
    elif control_302 and not errors:
        print("RESOLUTION|EARLY_ROUTER_ROUTE_BOUNDED|known 302 control is visible but no early router/file row is indexed in tested window")
    elif control_133 and not errors:
        print("RESOLUTION|CONTROL_FOUND_NO_302_METADATA|early route result remains archive-index-limited")
    elif errors:
        print("RESOLUTION|PARTIAL|retry only failed metadata surfaces")
    else:
        print("RESOLUTION|INCONCLUSIVE_CONTROL_MISSING|do not treat early zero as bounded")

    print("EVIDENCE_BOUNDARY|CDX length is archive-record metadata, not asserted original payload size; no archived body or game binary is fetched.")


if __name__ == "__main__":
    main()
