#!/usr/bin/env python3
"""Census historical yegame.com URLs reached from Jinghe/JHPOP in Dec 2000.

Evidence chain:
- Wayback capture 2000-12-04 16:03:00 UTC of www.jhpop.com contains
  window.location="http://www.yegame.com".
- Therefore yegame.com is a source-derived first-hop historical surface for
  Jinghe's launch-window web presence.

This probe uses only Wayback CDX metadata. It does not replay page bodies and
does not fetch software payloads. Modern yegame.com ownership/registration is
outside scope and must not be conflated with these timestamped captures.
"""
from __future__ import annotations

import collections
import hashlib
import json
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
FIELDS = "timestamp,original,statuscode,mimetype,digest,length,redirect"

FROM = "20001115"
TO = "20010228"
ROOT_FROM = "20001201"
ROOT_TO = "20010131"

TARGETS = (
    ("launch-domain", "yegame.com", "domain", FROM, TO, "launch"),
    ("launch-www-prefix", "http://www.yegame.com/", "prefix", FROM, TO, "launch"),
    ("launch-bare-prefix", "http://yegame.com/", "prefix", FROM, TO, "launch"),
    ("root-www", "http://www.yegame.com/", "exact", ROOT_FROM, ROOT_TO, "control"),
    ("root-bare", "http://yegame.com/", "exact", ROOT_FROM, ROOT_TO, "control"),
)

BINARY_EXTS = (
    ".exe", ".zip", ".rar", ".cab", ".arj", ".lzh", ".7z",
    ".iso", ".bin", ".cue", ".img", ".nrg", ".msi",
)

# Score only path/query/redirect tokens; do not score "game" from the yegame host.
TOKENS = (
    ("stoneage", 30),
    ("stone_age", 30),
    ("stone-age", 30),
    ("shiqi", 30),
    ("%ca%af%c6%f7", 25),  # possible GB2312 URL-encoded 石器
    ("wgs", 18),
    ("waei", 18),
    ("wayi", 18),
    ("test", 12),
    ("beta", 12),
    ("demo", 12),
    ("trial", 12),
    ("download", 9),
    ("down", 4),
    ("client", 8),
    ("online", 4),
    ("product", 3),
    ("soft", 2),
)


def clean(value, limit=8000):
    return " ".join(str(value if value is not None else "").split()).replace("|", "%7C")[:limit]


def fetch(url, timeout=90, max_bytes=32 * 1024 * 1024):
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
        ("url", url),
        ("matchType", match),
        ("output", "json"),
        ("fl", FIELDS),
        ("from", start),
        ("to", end),
        ("limit", "50000"),
        ("collapse", "urlkey"),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def parse(body):
    obj = json.loads(body.decode("utf-8"))
    if not isinstance(obj, list) or len(obj) < 2:
        return ()
    head = obj[0]
    return tuple(dict(zip(head, row)) for row in obj[1:] if isinstance(row, list))


def decoded(value):
    return urllib.parse.unquote_plus(str(value or "")).lower()


def path_query(value):
    raw = str(value or "")
    parts = urllib.parse.urlsplit(raw)
    return decoded(parts.path + ("?" + parts.query if parts.query else ""))


def is_binary(value):
    path = urllib.parse.urlsplit(decoded(value)).path
    return path.endswith(BINARY_EXTS)


def basename(value):
    path = urllib.parse.unquote(urllib.parse.urlsplit(str(value or "")).path)
    return path.rsplit("/", 1)[-1]


def score(original, redirect=""):
    text = path_query(original) + " " + decoded(redirect)
    value = 0
    matches = []
    for token, weight in TOKENS:
        if token in text:
            value += weight
            matches.append(token)
    if is_binary(original) or is_binary(redirect):
        value += 15
        matches.append("binary-ext")
    return value, tuple(matches)


def topdir(value):
    path = urllib.parse.urlsplit(str(value or "")).path.strip("/")
    return path.split("/", 1)[0].lower() if path else "/"


def main():
    print("StoneAge historical yegame.com launch-window Wayback census — R1")
    print(
        f"SOURCE_CHAIN|JHPOP root 20001204160300 -> http://www.yegame.com|"
        f"launch={FROM}..{TO}|root-control={ROOT_FROM}..{ROOT_TO}"
    )
    print("SCOPE|CDX metadata only|all statuses|collapse=urlkey|no archived-body|no software payload")
    print("PROVENANCE_BOUNDARY|Only timestamped historical captures are in scope; modern yegame.com identity is not inferred.")

    row_map = {}
    query_counts = {}
    errors = []

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
                entry = row_map.setdefault(key, {"row": row, "labels": set(), "scopes": set()})
                entry["labels"].add(label)
                entry["scopes"].add(scope)
        except Exception as exc:
            errors.append((label, scope, type(exc).__name__, str(exc)))

    entries = sorted(
        row_map.values(),
        key=lambda e: (str(e["row"].get("timestamp") or ""), str(e["row"].get("original") or "")),
    )
    launch = [e for e in entries if "launch" in e["scopes"]]
    controls = [e for e in entries if "control" in e["scopes"]]
    candidates = []
    binaries = []
    dirs = collections.Counter()
    statuses = collections.Counter()

    for entry in launch:
        row = entry["row"]
        original = str(row.get("original") or "")
        redirect = str(row.get("redirect") or "")
        statuses[str(row.get("statuscode") or "")] += 1
        dirs[topdir(original)] += 1
        sc, tokens = score(original, redirect)
        if sc:
            candidates.append((sc, tokens, entry))
        if is_binary(original) or is_binary(redirect):
            binaries.append(entry)

    if len(launch) <= 3000:
        emit = [(score(str(e["row"].get("original") or ""), str(e["row"].get("redirect") or "")), e) for e in launch]
        for (sc, tokens), entry in emit:
            row = entry["row"]
            original = str(row.get("original") or "")
            print(
                "ROW|timestamp={}|status={}|score={}|tokens={}|basename={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                    clean(row.get("timestamp")), clean(row.get("statuscode")), sc,
                    clean(",".join(tokens)), clean(basename(original), 1200),
                    clean(row.get("mimetype")), clean(row.get("length")), clean(row.get("digest")),
                    clean(row.get("redirect")), clean(original)
                )
            )
    else:
        for sc, tokens, entry in sorted(candidates, key=lambda x: (-x[0], str(x[2]["row"].get("original") or "")))[:750]:
            row = entry["row"]
            original = str(row.get("original") or "")
            print(
                "CANDIDATE|timestamp={}|status={}|score={}|tokens={}|basename={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                    clean(row.get("timestamp")), clean(row.get("statuscode")), sc,
                    clean(",".join(tokens)), clean(basename(original), 1200),
                    clean(row.get("mimetype")), clean(row.get("length")), clean(row.get("digest")),
                    clean(row.get("redirect")), clean(original)
                )
            )

    for name, count in dirs.most_common():
        print(f"TOPDIR|name={clean(name)}|count={count}")
    for status, count in sorted(statuses.items()):
        print(f"STATUS_COUNT|status={clean(status)}|count={count}")
    for label in sorted(query_counts):
        print(f"QUERY_COUNT|label={clean(label)}|count={query_counts[label]}")

    strong = [x for x in candidates if x[0] >= 12]
    print(f"COUNT|unique_rows|{len(entries)}")
    print(f"COUNT|launch_rows|{len(launch)}")
    print(f"COUNT|root_control_rows|{len(controls)}")
    print(f"COUNT|candidate_rows|{len(candidates)}")
    print(f"COUNT|strong_candidate_rows|{len(strong)}")
    print(f"COUNT|binary_rows|{len(binaries)}")
    for label, scope, kind, message in errors:
        print(
            "ERROR|label={}|scope={}|kind={}|message={}".format(
                clean(label), clean(scope), clean(kind), clean(message)
            )
        )
    print(f"COUNT|errors|{len(errors)}")

    if strong:
        print("RESOLUTION|YEGAME_STRONG_URL_CANDIDATES_FOUND|replay only exact high-value pages/routes next")
    elif binaries:
        print("RESOLUTION|YEGAME_BINARY_NAMESPACE_FOUND|classify exact historical binary paths next")
    elif launch:
        print("RESOLUTION|YEGAME_LAUNCH_NAMESPACE_FOUND|inspect root/topdirs and exact captures next")
    elif controls and not errors:
        print("RESOLUTION|YEGAME_ROOT_ONLY|launch domain enumeration empty but root control exists")
    elif errors:
        print("RESOLUTION|PARTIAL|retry only failed archive surfaces")
    else:
        print("RESOLUTION|YEGAME_LAUNCH_ARCHIVE_EMPTY|source-derived redirect survives but tested historical target namespace is not indexed")

    print("EVIDENCE_BOUNDARY|CDX metadata proves archival URL topology only; it cannot authenticate StoneAge client bytes or physical test-CD provenance.")


if __name__ == "__main__":
    main()
