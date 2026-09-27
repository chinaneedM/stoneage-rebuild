#!/usr/bin/env python3
"""Census the historical Jinghe/JHPOP web namespace around StoneAge public test.

Source-driven rationale:
- contemporaneous StoneAge material identifies Jinghe as the Mainland test-CD
  pickup/distribution channel;
- a later period StoneAge page gives Jinghe's online store as www.jhpop.com.
The preservation-index keyword route is already bounded, but the historical
site's own Wayback URL namespace has not been enumerated.

This probe is metadata-only. It does not replay page bodies or fetch software.
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
FROM = "20001115"
TO = "20010228"
CONTROL_FROM = "20010101"
CONTROL_TO = "20020331"
TARGETS = (
    ("launch-domain", "jhpop.com", "domain", FROM, TO, "launch"),
    ("launch-www-prefix", "http://www.jhpop.com/", "prefix", FROM, TO, "launch"),
    ("root-control", "http://www.jhpop.com/", "exact", CONTROL_FROM, CONTROL_TO, "control"),
)
BINARY_EXTS = (
    ".exe", ".zip", ".rar", ".cab", ".arj", ".lzh", ".7z",
    ".iso", ".bin", ".cue", ".img", ".nrg",
)
TOKENS = (
    ("stoneage", 20), ("shiqi", 20), ("stone", 8),
    ("waei", 12), ("wayi", 12), ("wgs", 12),
    ("test", 8), ("beta", 8), ("demo", 8),
    ("download", 6), ("down", 3), ("game", 3),
    ("online", 3), ("product", 2), ("soft", 1),
)


def clean(value, limit=6000):
    return " ".join(str(value if value is not None else "").split()).replace("|", "%7C")[:limit]


def fetch(url, timeout=75, max_bytes=24 * 1024 * 1024):
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
    params = [
        ("url", url), ("matchType", match), ("output", "json"), ("fl", FIELDS),
        ("from", start), ("to", end), ("limit", "50000"), ("collapse", "urlkey"),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def parse(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, row)) for row in obj[1:] if isinstance(row, list))


def decoded(url):
    return urllib.parse.unquote_plus(str(url or "")).lower()


def is_binary(url):
    path = urllib.parse.urlsplit(decoded(url)).path
    return path.endswith(BINARY_EXTS)


def basename(url):
    path = urllib.parse.unquote(urllib.parse.urlsplit(str(url or "")).path)
    return path.rsplit("/", 1)[-1]


def score(url, redirect=""):
    text = decoded(url) + " " + decoded(redirect)
    value = 0
    matches = []
    for token, weight in TOKENS:
        if token in text:
            value += weight
            matches.append(token)
    if is_binary(url) or is_binary(redirect):
        value += 10
        matches.append("binary-ext")
    return value, tuple(matches)


def topdir(url):
    path = urllib.parse.urlsplit(str(url or "")).path.strip("/")
    return path.split("/", 1)[0].lower() if path else "/"


def main():
    print("StoneAge Jinghe/JHPOP launch-window Wayback namespace census — R1")
    print(
        f"SCOPE|CDX metadata only|launch={FROM}..{TO}|root-control={CONTROL_FROM}..{CONTROL_TO}|"
        "all statuses|collapse=urlkey|no archived-body|no software payload"
    )
    rows_by_key = {}
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
                    str(row.get("original") or ""),
                    str(row.get("timestamp") or ""),
                    str(row.get("statuscode") or ""),
                    str(row.get("digest") or ""),
                )
                entry = rows_by_key.setdefault(key, {"row": row, "labels": set(), "scopes": set()})
                entry["labels"].add(label)
                entry["scopes"].add(scope)
        except Exception as exc:
            errors.append((label, scope, type(exc).__name__, str(exc)))

    entries = sorted(
        rows_by_key.values(),
        key=lambda e: (str(e["row"].get("timestamp") or ""), str(e["row"].get("original") or "")),
    )
    launch = [e for e in entries if "launch" in e["scopes"]]
    control = [e for e in entries if "control" in e["scopes"]]
    binaries = []
    candidates = []
    dirs = collections.Counter()
    statuses = collections.Counter()

    for entry in launch:
        row = entry["row"]
        original = str(row.get("original") or "")
        redirect = str(row.get("redirect") or "")
        statuses[str(row.get("statuscode") or "")] += 1
        dirs[topdir(original)] += 1
        sc, matched = score(original, redirect)
        if is_binary(original) or is_binary(redirect):
            binaries.append(entry)
        if sc > 0:
            candidates.append((sc, matched, entry))

    # Emit every launch-window URL when the census is reasonably bounded.
    if len(launch) <= 2500:
        for entry in launch:
            row = entry["row"]
            original = str(row.get("original") or "")
            redirect = str(row.get("redirect") or "")
            sc, matched = score(original, redirect)
            print(
                "ROW|timestamp={}|status={}|score={}|tokens={}|basename={}|mime={}|length={}|redirect={}|original={}".format(
                    clean(row.get("timestamp")), clean(row.get("statuscode")), sc,
                    clean(",".join(matched)), clean(basename(original), 1200),
                    clean(row.get("mimetype")), clean(row.get("length")),
                    clean(redirect), clean(original)
                )
            )
    else:
        for sc, matched, entry in sorted(candidates, key=lambda x: (-x[0], str(x[2]["row"].get("original") or "")))[:500]:
            row = entry["row"]
            original = str(row.get("original") or "")
            print(
                "CANDIDATE|timestamp={}|status={}|score={}|tokens={}|basename={}|mime={}|length={}|redirect={}|original={}".format(
                    clean(row.get("timestamp")), clean(row.get("statuscode")), sc,
                    clean(",".join(matched)), clean(basename(original), 1200),
                    clean(row.get("mimetype")), clean(row.get("length")),
                    clean(row.get("redirect")), clean(original)
                )
            )

    for name, count in dirs.most_common():
        print(f"TOPDIR|name={clean(name)}|count={count}")
    for status, count in sorted(statuses.items()):
        print(f"STATUS_COUNT|status={clean(status)}|count={count}")
    for label in sorted(query_counts):
        print(f"QUERY_COUNT|label={clean(label)}|count={query_counts[label]}")

    print(f"COUNT|unique_rows|{len(entries)}")
    print(f"COUNT|launch_rows|{len(launch)}")
    print(f"COUNT|candidate_rows|{len(candidates)}")
    print(f"COUNT|binary_rows|{len(binaries)}")
    print(f"COUNT|root_control_rows|{len(control)}")
    for label, scope, kind, message in errors:
        print(
            "ERROR|label={}|scope={}|kind={}|message={}".format(
                clean(label), clean(scope), clean(kind), clean(message)
            )
        )
    print(f"COUNT|errors|{len(errors)}")

    strong = [x for x in candidates if x[0] >= 12]
    if strong:
        print("RESOLUTION|JHPOP_STRONG_URL_CANDIDATES_FOUND|replay only exact candidate pages/routes next")
    elif binaries:
        print("RESOLUTION|JHPOP_BINARY_NAMESPACE_FOUND|classify exact launch-window binary paths next")
    elif launch:
        print("RESOLUTION|JHPOP_LAUNCH_NAMESPACE_FOUND_NO_STRONG_TOKEN|use recovered directory/page topology for targeted replay")
    elif control and not errors:
        print("RESOLUTION|JHPOP_LAUNCH_WINDOW_NOT_INDEXED|later root control exists; seek external mirrors/carrier tokens")
    elif errors:
        print("RESOLUTION|PARTIAL|retry failed metadata surface only")
    else:
        print("RESOLUTION|JHPOP_ARCHIVE_CONTROL_MISSING|do not treat launch-window zero as bounded")

    print(
        "EVIDENCE_BOUNDARY|URL metadata can establish historical site topology only; it cannot authenticate a StoneAge disc/client or byte identity."
    )


if __name__ == "__main__":
    main()
