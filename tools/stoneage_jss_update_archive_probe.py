#!/usr/bin/env python3
"""Probe first-party JSS StoneAge update-manifest/archive paths derived from the launcher.

The archived launcher exposes:
  update.gamersdream.ne.jp
  /~stoneage/newest.txt
  /~stoneage/%s
and resource-family names such as real_*.bin, adrn_*.bin, spr_*.bin,
spradrn_*.bin and sa_*.exe.

This probe reads Wayback index metadata and, only for exact newest.txt captures,
a bounded text response. It never downloads archived game/resource binaries.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX = "https://web.archive.org/cdx/search/cdx"
MAX_MANIFEST_BYTES = 256 * 1024
PREFIX_LIMIT = 5000

EXACT_MANIFESTS = (
    ("update-host", "http://update.gamersdream.ne.jp/~stoneage/newest.txt"),
    ("update-host-port80", "http://update.gamersdream.ne.jp:80/~stoneage/newest.txt"),
)

# The update-host prefix is directly composed from adjacent launcher strings.
# The titan prefix is retained only as a source-derived candidate because the
# launcher separately embeds http://www.titan.co.jp/ and /~stoneage/%s.
PREFIXES = (
    ("update-host", "http://update.gamersdream.ne.jp/~stoneage/"),
    ("update-host-port80", "http://update.gamersdream.ne.jp:80/~stoneage/"),
    ("titan-source-derived-candidate", "http://www.titan.co.jp/~stoneage/"),
    ("titan-source-derived-candidate-port80", "http://www.titan.co.jp:80/~stoneage/"),
)

FILE_RE = re.compile(
    r"(?i)(?:[A-Za-z]:)?[^\s\"'<>|]*?"
    r"(?:newest\.txt|sa_\d+\.exe|(?:real|adrn|spr|spradrn|battle|sound)_\d+\.bin|"
    r"(?:battletxt|soundaddr)_\d+\.txt|[\w./\\~-]*map[\w./\\~-]*\.(?:bin|dat|txt))"
)
URL_RE = re.compile(r"(?i)https?://[^\s\\\"'<>|]+")
RESOURCE_RE = re.compile(
    r"(?i)(newest\.txt$|sa_\d+\.exe$|(?:real|adrn|spr|spradrn|battle|sound)_\d+\.bin$|"
    r"(?:battletxt|soundaddr)_\d+\.txt$)"
)


def clean(value, limit=1200):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def request_bytes(url, timeout=18, limit=None):
    headers = {
        "User-Agent": UA,
        "Accept": "application/json,text/plain,*/*",
        "Accept-Encoding": "identity",
    }
    if limit is not None:
        headers["Range"] = f"bytes=0-{limit - 1}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read(None if limit is None else limit + 1)
        return {
            "status": int(getattr(response, "status", 200)),
            "final": response.geturl(),
            "headers": dict(response.headers),
            "body": data if limit is None else data[:limit],
            "truncated": bool(limit is not None and len(data) > limit),
        }


def parse_cdx(data):
    text = data.decode("utf-8", "replace").strip()
    if not text:
        return []
    obj = json.loads(text)
    if not isinstance(obj, list) or not obj:
        return []
    if not isinstance(obj[0], list):
        return [row for row in obj if isinstance(row, dict)]
    header = [str(x) for x in obj[0]]
    return [
        {header[i]: str(row[i]) if i < len(row) else "" for i in range(len(header))}
        for row in obj[1:]
        if isinstance(row, list)
    ]


def cdx_url(url, match_type, limit):
    params = [
        ("url", url),
        ("matchType", match_type),
        ("from", "1999"),
        ("to", "2002"),
        ("output", "json"),
        ("fl", "timestamp,original,mimetype,statuscode,digest,length,redirect"),
        ("limit", str(limit)),
    ]
    return CDX + "?" + urllib.parse.urlencode(params)


def query_cdx(label, url, match_type, limit):
    try:
        raw = request_bytes(cdx_url(url, match_type, limit), timeout=20)["body"]
        return label, url, parse_cdx(raw), None
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 429, 502, 503, 504):
            return label, url, [], (type(exc).__name__, str(exc))
        raise
    except Exception as exc:
        return label, url, [], (type(exc).__name__, str(exc))


def replay_url(timestamp, original):
    quoted = urllib.parse.quote(original, safe=":/?&=%#+,;@[]!$'()*")
    return f"https://web.archive.org/web/{timestamp}id_/{quoted}"


def normalized_path(original):
    try:
        return urllib.parse.urlsplit(str(original)).path.replace("\\", "/")
    except Exception:
        return str(original).replace("\\", "/")


def classify_archive_path(original):
    path = normalized_path(original)
    base = path.rsplit("/", 1)[-1].lower()
    return {
        "resource_family": bool(RESOURCE_RE.search(base)),
        "map_like": "map" in path.lower(),
        "executable": base.endswith(".exe"),
        "manifest": base == "newest.txt",
    }


def manifest_tokens(data):
    """Return derived file/URL tokens without retaining manifest prose."""
    text = data.decode("latin-1", "replace")
    files = []
    urls = []
    seen_files = set()
    seen_urls = set()
    for match in FILE_RE.finditer(text):
        token = match.group(0).strip(" \t\r\n,;()[]{}")
        key = token.lower()
        if token and key not in seen_files:
            seen_files.add(key)
            files.append(token)
    for match in URL_RE.finditer(text):
        token = match.group(0).rstrip(".,;)")
        key = token.lower()
        if token and key not in seen_urls:
            seen_urls.add(key)
            urls.append(token)
    return tuple(files), tuple(urls)


def resolution(manifest_replays, exact_rows, prefix_rows, errors, saturated):
    if manifest_replays:
        return "UPDATE_MANIFEST_RECOVERED"
    if exact_rows:
        return "MANIFEST_CAPTURE_INDEXED"
    if errors or saturated:
        return "INCONCLUSIVE"
    if prefix_rows:
        return "UPDATE_PREFIX_INDEXED_NO_MANIFEST"
    return "BOUNDED_NO_INDEX_ROWS"


def normalize_row(row):
    return {
        "timestamp": str(row.get("timestamp", "")),
        "original": str(row.get("original", "")),
        "mime": str(row.get("mimetype", "")),
        "status": str(row.get("statuscode", "")),
        "digest": str(row.get("digest", "")),
        "length": str(row.get("length", "")),
        "redirect": str(row.get("redirect", "")),
    }


def main():
    print("StoneAge JSS update archive probe — R1")
    print("SCOPE|launcher-derived-first-party-paths|1999-2002|cdx-metadata+bounded-newest-text|no-resource-binary-download")
    print("LAUNCHER_EVIDENCE|host=update.gamersdream.ne.jp|manifest=/~stoneage/newest.txt|payload_pattern=/~stoneage/%s")
    print("TITAN_PREFIX_BOUNDARY|source-derived-candidate-only|launcher-embeds-titan-root-separately")
    print(f"LIMIT|prefix_rows={PREFIX_LIMIT}|manifest_bytes={MAX_MANIFEST_BYTES}")

    exact_results = []
    prefix_results = []
    errors = []
    saturated = False

    jobs = []
    for label, url in EXACT_MANIFESTS:
        jobs.append((label, url, "exact", 100))
    for label, url in PREFIXES:
        jobs.append((label, url, "prefix", PREFIX_LIMIT))

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(query_cdx, *job) for job in jobs]
        for fut, job in zip(futures, jobs):
            label, url, rows, error = fut.result()
            mode = job[2]
            if error:
                errors.append((label, mode, url, error[0], error[1]))
            if mode == "exact":
                exact_results.append((label, url, rows))
            else:
                if len(rows) >= PREFIX_LIMIT:
                    saturated = True
                prefix_results.append((label, url, rows))

    exact_rows = [normalize_row(row) for _, _, rows in exact_results for row in rows]
    prefix_rows = [normalize_row(row) for _, _, rows in prefix_results for row in rows]

    print(f"COUNT|exact_targets|{len(EXACT_MANIFESTS)}")
    print(f"COUNT|prefix_targets|{len(PREFIXES)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|exact_rows|{len(exact_rows)}")
    print(f"COUNT|prefix_rows|{len(prefix_rows)}")
    print(f"COUNT|saturated_prefixes|{sum(1 for _,_,rows in prefix_results if len(rows) >= PREFIX_LIMIT)}")

    for label, mode, url, kind, message in sorted(errors):
        print(
            f"ERROR|label={clean(label)}|mode={mode}|kind={clean(kind)}|"
            f"url={clean(url)}|message={clean(message)}"
        )

    emitted = set()
    relevant_count = 0
    map_like_count = 0
    resource_count = 0
    for label, prefix, rows in prefix_results:
        relevant = []
        for raw in rows:
            row = normalize_row(raw)
            flags = classify_archive_path(row["original"])
            if not any(flags.values()):
                continue
            relevant.append((row, flags))
            relevant_count += 1
            map_like_count += int(flags["map_like"])
            resource_count += int(flags["resource_family"])
        print(
            f"PREFIX|label={clean(label)}|rows={len(rows)}|relevant={len(relevant)}|"
            f"saturated={int(len(rows)>=PREFIX_LIMIT)}|url={clean(prefix)}"
        )
        for row, flags in relevant:
            emitted.add((
                label, row["timestamp"], row["status"], row["mime"], row["length"],
                row["digest"], row["original"], row["redirect"],
                int(flags["resource_family"]), int(flags["map_like"]),
                int(flags["executable"]), int(flags["manifest"]),
            ))

    print(f"COUNT|relevant_prefix_rows|{relevant_count}")
    print(f"COUNT|resource_family_rows|{resource_count}")
    print(f"COUNT|map_like_rows|{map_like_count}")

    for rec in sorted(emitted):
        (
            label, timestamp, status, mime, length, digest, original, redirect,
            resource_family, map_like, executable, manifest,
        ) = rec
        print(
            f"INDEX|prefix={clean(label)}|timestamp={clean(timestamp)}|status={clean(status)}|"
            f"mime={clean(mime)}|length={clean(length)}|digest={clean(digest)}|"
            f"resource_family={resource_family}|map_like={map_like}|executable={executable}|"
            f"manifest={manifest}|original={clean(original)}|redirect={clean(redirect)}"
        )

    manifest_replays = []
    replay_seen = set()
    for label, _, rows in exact_results:
        for raw in rows:
            row = normalize_row(raw)
            key = (row["timestamp"], row["original"])
            if not row["timestamp"] or not row["original"] or key in replay_seen:
                continue
            replay_seen.add(key)
            if row["status"] and row["status"] != "200":
                continue
            try:
                result = request_bytes(
                    replay_url(row["timestamp"], row["original"]),
                    timeout=18,
                    limit=MAX_MANIFEST_BYTES,
                )
            except Exception as exc:
                print(
                    f"MANIFEST_FETCH_ERROR|label={clean(label)}|timestamp={clean(row['timestamp'])}|"
                    f"kind={type(exc).__name__}|message={clean(exc)}"
                )
                continue
            body = result["body"]
            # If a nominal newest.txt replay is actually binary, record only signature/hash.
            binary = body.startswith((b"MZ", b"PK\x03\x04", b"MSCF"))
            files, urls = ((), ()) if binary else manifest_tokens(body)
            manifest_replays.append((row, body, result, files, urls, binary))
            print(
                f"MANIFEST|label={clean(label)}|timestamp={clean(row['timestamp'])}|"
                f"status={result['status']}|bytes={len(body)}|truncated={int(result['truncated'])}|"
                f"binary={int(binary)}|sha256={hashlib.sha256(body).hexdigest()}|"
                f"file_tokens={len(files)}|url_tokens={len(urls)}|final={clean(result['final'])}"
            )
            for token in files:
                flags = classify_archive_path(token)
                print(
                    f"MANIFEST_FILE|timestamp={clean(row['timestamp'])}|"
                    f"resource_family={int(flags['resource_family'])}|map_like={int(flags['map_like'])}|"
                    f"executable={int(flags['executable'])}|manifest={int(flags['manifest'])}|"
                    f"value={clean(token)}"
                )
            for token in urls:
                print(f"MANIFEST_URL|timestamp={clean(row['timestamp'])}|value={clean(token)}")

    state = resolution(
        manifest_replays,
        exact_rows,
        prefix_rows,
        errors,
        saturated,
    )
    if state == "UPDATE_MANIFEST_RECOVERED":
        print("RESOLUTION|UPDATE_MANIFEST_RECOVERED|use derived tokens to target archived first-party resources without assuming payload identity")
    elif state == "MANIFEST_CAPTURE_INDEXED":
        print("RESOLUTION|MANIFEST_CAPTURE_INDEXED|manifest replay unavailable; retain metadata-only boundary")
    elif state == "UPDATE_PREFIX_INDEXED_NO_MANIFEST":
        print("RESOLUTION|UPDATE_PREFIX_INDEXED_NO_MANIFEST|use indexed first-party resource paths as bounded recovery leads")
    elif state == "INCONCLUSIVE":
        print("RESOLUTION|INCONCLUSIVE|archive query surface incomplete or saturated")
    else:
        print("RESOLUTION|BOUNDED_NO_INDEX_ROWS|no archive index rows in tested launcher-derived paths; does not disprove historical availability")


if __name__ == "__main__":
    main()
