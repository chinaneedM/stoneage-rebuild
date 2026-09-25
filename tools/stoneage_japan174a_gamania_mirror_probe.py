#!/usr/bin/env python3
"""Probe public preservation indexes for Japanese StoneAge sa174gm.exe.

The historical/source identity is documented elsewhere in the repository.
This probe focuses on exact/prefix preservation metadata. It never executes a
client and never commits payload bytes. If one exact public Wayback HTTP-200
object is replayable, it may be streamed transiently only to derive size/hash
and magic bytes, under a 400 MiB cap.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
GM_HTTP = "http://file2.gamania.co.jp/sa/sa174gm.exe"
GM_HTTPS = "https://file2.gamania.co.jp/sa/sa174gm.exe"
GM_PREFIX = "file2.gamania.co.jp/sa/*"
CDX = "https://web.archive.org/cdx/search/cdx"
AVAIL = "https://archive.org/wayback/available"
ARQUIVO = "https://arquivo.pt/wayback/cdx"
IA_SEARCH = "https://archive.org/advancedsearch.php"
WAYBACK = "https://web.archive.org/web/{timestamp}id_/{original}"
MAX_REPLAY = 400 * 1024 * 1024


def clean(value, limit=1600):
    value = "" if value is None else str(value)
    value = " ".join(value.replace("\x00", " ").split())
    return value.replace("|", "%7C")[:limit]


def fetch(url, *, timeout=14, max_bytes=12_000_000, method=None):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json,text/plain,text/html,*/*",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = b"" if method == "HEAD" else response.read(max_bytes + 1)
            return {
                "ok": True,
                "status": int(getattr(response, "status", response.getcode())),
                "final": response.geturl(),
                "headers": dict(response.headers.items()),
                "body": body[:max_bytes],
                "truncated": len(body) > max_bytes,
            }
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read(min(max_bytes, 500_000))
        except Exception:
            body = b""
        return {
            "ok": False,
            "status": exc.code,
            "final": url,
            "headers": dict(exc.headers.items()) if exc.headers else {},
            "body": body,
            "error": "HTTPError",
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": "",
            "final": url,
            "headers": {},
            "body": b"",
            "error": type(exc).__name__ + ": " + str(exc),
        }


def parse_json_rows(body):
    text = body.decode("utf-8", "replace").strip()
    if not text:
        return []
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return []
    if isinstance(obj, list):
        if obj and isinstance(obj[0], list):
            header = obj[0]
            return [dict(zip(header, row)) for row in obj[1:] if isinstance(row, list)]
        return [row for row in obj if isinstance(row, dict)]
    if isinstance(obj, dict):
        for key in ("results", "captures", "items", "response"):
            rows = obj.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


def wayback_url(target, *, prefix=False):
    params = [
        ("url", target),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from", "2003"),
        ("to", "2026"),
        ("limit", "2000" if prefix else "500"),
    ]
    if prefix:
        params.append(("matchType", "prefix"))
    return CDX + "?" + urllib.parse.urlencode(params)


def arquivo_url(target):
    params = {
        "url": target,
        "from": "2003",
        "to": "2026",
        "output": "json",
        "limit": "500",
    }
    return ARQUIVO + "?" + urllib.parse.urlencode(params)


def availability_url(target, stamp):
    return AVAIL + "?" + urllib.parse.urlencode({"url": target, "timestamp": stamp})


def ia_url():
    params = [
        ("q", '"sa174gm.exe" OR "sa174gm"'),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "description"),
        ("rows", "100"),
        ("page", "1"),
        ("output", "json"),
    ]
    return IA_SEARCH + "?" + urllib.parse.urlencode(params)


def live_head(target):
    return ("LIVE_HEAD", target, fetch(target, timeout=10, max_bytes=0, method="HEAD"))


def wayback_exact(target):
    url = wayback_url(target)
    response = fetch(url, timeout=16)
    rows = parse_json_rows(response["body"]) if response.get("ok") else []
    return ("WAYBACK_CDX", target, response, rows)


def wayback_prefix():
    url = wayback_url(GM_PREFIX, prefix=True)
    response = fetch(url, timeout=18)
    rows = parse_json_rows(response["body"]) if response.get("ok") else []
    return ("WAYBACK_PREFIX", GM_PREFIX, response, rows)


def availability(target, stamp):
    url = availability_url(target, stamp)
    response = fetch(url, timeout=12, max_bytes=1_000_000)
    closest = {}
    if response.get("ok"):
        try:
            obj = json.loads(response["body"].decode("utf-8", "replace"))
            closest = obj.get("archived_snapshots", {}).get("closest", {})
        except Exception:
            closest = {}
    return ("WAYBACK_AVAIL", target, stamp, response, closest)


def arquivo(target):
    url = arquivo_url(target)
    response = fetch(url, timeout=14)
    rows = parse_json_rows(response["body"]) if response.get("ok") else []
    return ("ARQUIVO_CDX", target, response, rows)


def ia_search():
    response = fetch(ia_url(), timeout=16)
    docs = []
    if response.get("ok"):
        try:
            obj = json.loads(response["body"].decode("utf-8", "replace"))
            docs = obj.get("response", {}).get("docs", []) if isinstance(obj, dict) else []
        except Exception:
            docs = []
    return ("IA_SEARCH", response, docs)


def stream_wayback(timestamp, original):
    url = WAYBACK.format(timestamp=timestamp, original=original)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/octet-stream,*/*"},
    )
    digest = hashlib.sha256()
    total = 0
    prefix = b""
    with urllib.request.urlopen(request, timeout=60) as response:
        final = response.geturl()
        headers = dict(response.headers.items())
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            if total < 64:
                prefix += chunk[: 64 - total]
            total += len(chunk)
            if total > MAX_REPLAY:
                raise ValueError("replay exceeds 400 MiB safety cap")
            digest.update(chunk)
    return {
        "final": final,
        "bytes": total,
        "sha256": digest.hexdigest(),
        "prefix_hex": prefix.hex(),
        "headers": headers,
    }


def main():
    print("StoneAge Japan sa174gm Gamania mirror probe — R2")
    print("SCOPE|exact+prefix-public-preservation-index|optional-one-object-transient-hash|no-payload-commit")
    print(f"TARGET|gamania_http={GM_HTTP}")
    print(f"TARGET|gamania_https={GM_HTTPS}")
    print(f"TARGET|gamania_prefix={GM_PREFIX}")
    print("SOURCE_ANCHOR|2008-community-post=http://file2.gamania.co.jp/sa/sa174gm.exe")
    print("SOURCE_ANCHOR|2020-survival-carrier=sa174gm[password-www.shiqi.la].rar|visible_size=194.24MB|attachment_id=675")
    print("EVIDENCE_RULE|sa174gm and first-party sa174hg remain separate identities until byte comparison")

    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for target in (GM_HTTP, GM_HTTPS):
            tasks.append(executor.submit(live_head, target))
            tasks.append(executor.submit(wayback_exact, target))
            tasks.append(executor.submit(arquivo, target))
            for stamp in ("20031211", "20031212", "20040101", "20080101"):
                tasks.append(executor.submit(availability, target, stamp))
        tasks.append(executor.submit(wayback_prefix))
        tasks.append(executor.submit(ia_search))
        results = [future.result() for future in tasks]

    exact_rows = []
    prefix_rows = []
    errors = 0
    for result in results:
        kind = result[0]
        if kind == "LIVE_HEAD":
            _, target, response = result
            h = response.get("headers", {})
            if not response.get("ok"):
                errors += 1
            print(
                f"LIVE_HEAD|target={clean(target)}|ok={int(response.get('ok',False))}|"
                f"status={response.get('status','')}|final={clean(response.get('final',''))}|"
                f"content_length={clean(h.get('Content-Length'))}|content_type={clean(h.get('Content-Type'))}|"
                f"last_modified={clean(h.get('Last-Modified'))}|location={clean(h.get('Location'))}|"
                f"error={clean(response.get('error',''))}"
            )
        elif kind == "WAYBACK_CDX":
            _, target, response, rows = result
            if not response.get("ok"):
                errors += 1
            exact_rows.extend(rows)
            print(
                f"WAYBACK_CDX|target={clean(target)}|ok={int(response.get('ok',False))}|"
                f"status={response.get('status','')}|rows={len(rows)}|error={clean(response.get('error',''))}"
            )
            for row in rows:
                print("WAYBACK_ROW|" + "|".join(
                    f"{key}={clean(row.get(key,''))}"
                    for key in ("timestamp","original","statuscode","mimetype","digest","length","redirect")
                ))
        elif kind == "WAYBACK_PREFIX":
            _, target, response, rows = result
            if not response.get("ok"):
                errors += 1
            prefix_rows.extend(rows)
            gm_rows = [
                row for row in rows
                if "sa174gm" in str(row.get("original","")).lower()
            ]
            print(
                f"WAYBACK_PREFIX|target={clean(target)}|ok={int(response.get('ok',False))}|"
                f"status={response.get('status','')}|rows={len(rows)}|gm_rows={len(gm_rows)}|"
                f"error={clean(response.get('error',''))}"
            )
            for row in gm_rows:
                print("WAYBACK_PREFIX_GM|" + "|".join(
                    f"{key}={clean(row.get(key,''))}"
                    for key in ("timestamp","original","statuscode","mimetype","digest","length","redirect")
                ))
        elif kind == "WAYBACK_AVAIL":
            _, target, stamp, response, closest = result
            if not response.get("ok"):
                errors += 1
            print(
                f"WAYBACK_AVAIL|target={clean(target)}|timestamp={stamp}|"
                f"ok={int(response.get('ok',False))}|status={response.get('status','')}|"
                f"closest={clean(json.dumps(closest,ensure_ascii=False,sort_keys=True),1800)}|"
                f"error={clean(response.get('error',''))}"
            )
        elif kind == "ARQUIVO_CDX":
            _, target, response, rows = result
            if not response.get("ok"):
                errors += 1
            print(
                f"ARQUIVO_CDX|target={clean(target)}|ok={int(response.get('ok',False))}|"
                f"status={response.get('status','')}|rows={len(rows)}|error={clean(response.get('error',''))}"
            )
            for row in rows[:100]:
                print(f"ARQUIVO_ROW|target={clean(target)}|value={clean(json.dumps(row,ensure_ascii=False,sort_keys=True),2400)}")
        elif kind == "IA_SEARCH":
            _, response, docs = result
            if not response.get("ok"):
                errors += 1
            print(
                f"IA_SEARCH|ok={int(response.get('ok',False))}|status={response.get('status','')}|"
                f"docs={len(docs)}|error={clean(response.get('error',''))}"
            )
            for doc in docs:
                print(f"IA_DOC|{clean(json.dumps(doc,ensure_ascii=False,sort_keys=True),2400)}")

    # Deduplicate exact rows, and replay at most the earliest exact HTTP-200 object.
    candidates = {}
    for row in exact_rows + prefix_rows:
        original = str(row.get("original",""))
        if "sa174gm.exe" not in original.lower():
            continue
        if str(row.get("statuscode","")) != "200":
            continue
        key = (str(row.get("timestamp","")), original, str(row.get("digest","")))
        candidates[key] = row

    ordered = [candidates[key] for key in sorted(candidates)]
    print(f"COUNT|exact_or_prefix_http200_candidates|{len(ordered)}")
    print(f"COUNT|probe_errors|{errors}")

    if ordered:
        row = ordered[0]
        try:
            fingerprint = stream_wayback(
                str(row.get("timestamp","")),
                str(row.get("original","")),
            )
            prefix = fingerprint["prefix_hex"].lower()
            signature = "mz" if prefix.startswith("4d5a") else (
                "html" if prefix.startswith("3c") else "other"
            )
            print(
                f"PAYLOAD_REPLAY|timestamp={clean(row.get('timestamp',''))}|"
                f"original={clean(row.get('original',''))}|bytes={fingerprint['bytes']}|"
                f"sha256={fingerprint['sha256']}|signature={signature}|"
                f"prefix_hex={clean(fingerprint['prefix_hex'])}|final={clean(fingerprint['final'])}|"
                f"content_type={clean(fingerprint['headers'].get('Content-Type'))}"
            )
            if signature == "mz":
                print("RESOLUTION|PUBLIC_WAYBACK_EXECUTABLE_RECOVERED|requires separate clean-client and installer inventory analysis")
            else:
                print("RESOLUTION|PUBLIC_WAYBACK_OBJECT_REPLAYED_NOT_CONFIRMED_EXECUTABLE|do not promote to client bytes")
        except Exception as exc:
            print(f"PAYLOAD_REPLAY_ERROR|kind={type(exc).__name__}|message={clean(exc,1800)}")
            print("RESOLUTION|EXACT_GAMANIA_ARCHIVE_IDENTITY_FOUND_REPLAY_UNRESOLVED")
    else:
        print("RESOLUTION|GAMANIA_SA174GM_PUBLIC_INDEX_SURFACE_BOUNDED|no exact HTTP-200 payload in tested indexes")

    print("EVIDENCE_BOUNDARY|community sources establish the historical sa174gm identity; only recovered provenance-preserving bytes can establish build/version/date or equality with sa174hg.")


if __name__ == "__main__":
    main()
