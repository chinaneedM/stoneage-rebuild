#!/usr/bin/env python3
"""Probe the newly recovered Japanese StoneAge sa174gm.exe Gamania mirror.

This tool records public index/page metadata only. If an exact Wayback payload
capture is publicly replayable, it may stream that one object transiently to
compute a size/hash/magic fingerprint; payload bytes are never committed.
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
GM_HTTP = "http://file2.gamania.co.jp/sa/sa174gm.exe"
GM_HTTPS = "https://file2.gamania.co.jp/sa/sa174gm.exe"
IPVE = "https://www.ipve.com/bbs/viewthread.php?extra=&page=5&tid=84383"
SHIQILA = "https://shiqi.la/forum.php?mod=viewthread&tid=16671"
CDX = "https://web.archive.org/cdx/search/cdx"
WAYBACK = "https://web.archive.org/web/{timestamp}id_/{original}"
AVAIL = "https://archive.org/wayback/available"
ARQUIVO = "https://arquivo.pt/wayback/cdx"
IA_SEARCH = "https://archive.org/advancedsearch.php"
MAX_REPLAY = 400 * 1024 * 1024

URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
ATTACH_RE = re.compile(
    r"""href=[\"']([^\"']*mod=attachment[^\"']*)[\"'][^>]*>(.*?)</a>""",
    re.I | re.S,
)
TAG_RE = re.compile(r"<[^>]+>", re.S)


def clean(v, n=1200):
    v = html.unescape(str(v if v is not None else "")).replace("\x00", " ")
    v = " ".join(v.split()).replace("|", "%7C")
    return v[:n]


def request(url, *, timeout=35, max_bytes=8_000_000, method=None):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/json,text/plain,*/*",
            "Accept-Language": "ja,zh-CN,zh;q=0.8,en;q=0.5",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = b"" if method == "HEAD" else r.read(max_bytes + 1)
            return {
                "ok": True,
                "status": int(getattr(r, "status", r.getcode())),
                "final": r.geturl(),
                "headers": dict(r.headers.items()),
                "body": body[:max_bytes],
                "truncated": len(body) > max_bytes,
            }
    except urllib.error.HTTPError as e:
        try:
            body = e.read(min(max_bytes, 500_000))
        except Exception:
            body = b""
        return {
            "ok": False,
            "status": e.code,
            "final": url,
            "headers": dict(e.headers.items()) if e.headers else {},
            "body": body,
            "error": "HTTPError",
        }
    except Exception as e:
        return {
            "ok": False,
            "status": "",
            "final": url,
            "headers": {},
            "body": b"",
            "error": type(e).__name__ + ": " + str(e),
        }


def decode_text(body):
    for enc in ("utf-8", "cp932", "shift_jis", "big5", "gb18030"):
        try:
            return body.decode(enc)
        except UnicodeDecodeError:
            pass
    return body.decode("utf-8", "replace")


def parse_cdx(body):
    text = body.decode("utf-8", "replace").strip()
    if not text:
        return []
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(obj, list) or not obj:
        return []
    if isinstance(obj[0], list):
        hdr = obj[0]
        return [dict(zip(hdr, row)) for row in obj[1:] if isinstance(row, list)]
    return [x for x in obj if isinstance(x, dict)]


def wayback_rows(target):
    params = [
        ("url", target),
        ("output", "json"),
        ("fl", "timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from", "2003"),
        ("to", "2026"),
        ("limit", "500"),
    ]
    u = CDX + "?" + urllib.parse.urlencode(params)
    r = request(u, timeout=45, max_bytes=12_000_000)
    return u, r, parse_cdx(r["body"]) if r.get("ok") else []


def arquivo_rows(target):
    params = {
        "url": target,
        "from": "2003",
        "to": "2026",
        "output": "json",
        "limit": "500",
    }
    u = ARQUIVO + "?" + urllib.parse.urlencode(params)
    r = request(u, timeout=35, max_bytes=8_000_000)
    rows = []
    if r.get("ok"):
        text = r["body"].decode("utf-8", "replace").strip()
        try:
            obj = json.loads(text)
        except json.JSONDecodeError:
            obj = None
        if isinstance(obj, list):
            if obj and isinstance(obj[0], list):
                hdr = obj[0]
                rows = [dict(zip(hdr, x)) for x in obj[1:] if isinstance(x, list)]
            else:
                rows = [x for x in obj if isinstance(x, dict)]
        elif isinstance(obj, dict):
            for key in ("results", "captures", "response", "items"):
                if isinstance(obj.get(key), list):
                    rows = [x for x in obj[key] if isinstance(x, dict)]
                    break
    return u, r, rows


def availability(target, stamp):
    u = AVAIL + "?" + urllib.parse.urlencode({"url": target, "timestamp": stamp})
    r = request(u, timeout=30, max_bytes=1_000_000)
    return u, r


def ia_search():
    query = '"sa174gm.exe" OR "sa174gm"'
    params = [
        ("q", query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "description"),
        ("rows", "100"),
        ("page", "1"),
        ("output", "json"),
    ]
    u = IA_SEARCH + "?" + urllib.parse.urlencode(params)
    r = request(u, timeout=35, max_bytes=8_000_000)
    docs = []
    if r.get("ok"):
        try:
            obj = json.loads(r["body"].decode("utf-8", "replace"))
            docs = obj.get("response", {}).get("docs", []) if isinstance(obj, dict) else []
        except Exception:
            pass
    return u, r, docs


def decode_discuz_aid(href):
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(html.unescape(href)).query)
    token = (q.get("aid") or [""])[0]
    if not token:
        return ""
    try:
        raw = base64.b64decode(token + ("=" * (-len(token) % 4))).decode("ascii", "replace")
    except Exception:
        return ""
    return raw


def stream_wayback(timestamp, original):
    u = WAYBACK.format(timestamp=timestamp, original=original)
    req = urllib.request.Request(
        u,
        headers={"User-Agent": UA, "Accept": "application/octet-stream,*/*"},
    )
    h = hashlib.sha256()
    total = 0
    prefix = b""
    with urllib.request.urlopen(req, timeout=60) as r:
        final = r.geturl()
        headers = dict(r.headers.items())
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            if total < 64:
                prefix += chunk[: 64 - total]
            total += len(chunk)
            if total > MAX_REPLAY:
                raise ValueError("replay exceeds 400 MiB safety cap")
            h.update(chunk)
    return {
        "url": u,
        "final": final,
        "bytes": total,
        "sha256": h.hexdigest(),
        "prefix": prefix.hex(),
        "headers": headers,
    }


def main():
    print("StoneAge Japan sa174gm Gamania mirror probe — R1")
    print("SCOPE|public-source+archive-index+optional-public-wayback-stream-hash|no-payload-commit")
    print(f"TARGET|gamania_http={GM_HTTP}")
    print(f"TARGET|gamania_https={GM_HTTPS}")
    print("EVIDENCE_RULE|sa174gm and sa174hg remain separate identities until byte comparison")

    # Public source pages that independently expose the token/carrier.
    for label, url in (("ipve-2008", IPVE), ("shiqila-2020", SHIQILA)):
        r = request(url, timeout=40, max_bytes=4_000_000)
        text = decode_text(r.get("body", b""))
        print(
            f"PAGE|label={label}|ok={int(r.get('ok',False))}|status={r.get('status','')}|"
            f"bytes={len(r.get('body',b''))}|sha256={hashlib.sha256(r.get('body',b'')).hexdigest() if r.get('body') else ''}|"
            f"final={clean(r.get('final',''))}|gm_token={int('sa174gm.exe' in text.lower())}|"
            f"official_url={int(GM_HTTP.lower() in text.lower())}|error={clean(r.get('error',''))}"
        )
        if label == "shiqila-2020" and text:
            for href, anchor_html in ATTACH_RE.findall(text):
                anchor = clean(TAG_RE.sub(" ", anchor_html), 1000)
                if "sa174gm" in anchor.lower() or "Stoneage.rar" in anchor:
                    print(
                        f"ATTACHMENT|name={anchor}|href={clean(href,1800)}|"
                        f"decoded_aid={clean(decode_discuz_aid(href),600)}"
                    )
            for needle in (
                "sa174gm[解压密码www.shiqi.la].rar",
                "Stoneage.rar",
                "194.24 MB",
                "174.72 MB",
                "2003年12月11日",
            ):
                print(f"PAGE_TOKEN|label={label}|token={clean(needle)}|count={text.count(needle)}")

    # Present-day direct endpoint metadata only.
    for target in (GM_HTTP, GM_HTTPS):
        r = request(target, timeout=20, max_bytes=1024, method="HEAD")
        h = r.get("headers", {})
        print(
            f"LIVE_HEAD|target={clean(target)}|ok={int(r.get('ok',False))}|status={r.get('status','')}|"
            f"final={clean(r.get('final',''))}|content_length={clean(h.get('Content-Length'))}|"
            f"content_type={clean(h.get('Content-Type'))}|last_modified={clean(h.get('Last-Modified'))}|"
            f"location={clean(h.get('Location'))}|error={clean(r.get('error',''))}"
        )

    all_rows = []
    for target in (GM_HTTP, GM_HTTPS):
        _, r, rows = wayback_rows(target)
        print(
            f"WAYBACK_CDX|target={clean(target)}|ok={int(r.get('ok',False))}|status={r.get('status','')}|"
            f"rows={len(rows)}|error={clean(r.get('error',''))}"
        )
        for row in rows:
            normalized = {
                "timestamp": row.get("timestamp", ""),
                "original": row.get("original", ""),
                "statuscode": row.get("statuscode", ""),
                "mimetype": row.get("mimetype", ""),
                "digest": row.get("digest", ""),
                "length": row.get("length", ""),
                "redirect": row.get("redirect", ""),
            }
            all_rows.append(normalized)
            print("WAYBACK_ROW|" + "|".join(f"{k}={clean(v)}" for k, v in normalized.items()))

        for stamp in ("20031211", "20031212", "20040101", "20080101"):
            _, ar = availability(target, stamp)
            snap = ""
            if ar.get("ok"):
                try:
                    obj = json.loads(ar["body"].decode("utf-8", "replace"))
                    closest = obj.get("archived_snapshots", {}).get("closest", {})
                    snap = json.dumps(closest, ensure_ascii=False, sort_keys=True)
                except Exception:
                    pass
            print(
                f"WAYBACK_AVAIL|target={clean(target)}|timestamp={stamp}|ok={int(ar.get('ok',False))}|"
                f"status={ar.get('status','')}|closest={clean(snap,1600)}|error={clean(ar.get('error',''))}"
            )

        _, rr, arows = arquivo_rows(target)
        print(
            f"ARQUIVO_CDX|target={clean(target)}|ok={int(rr.get('ok',False))}|status={rr.get('status','')}|"
            f"rows={len(arows)}|error={clean(rr.get('error',''))}"
        )
        for row in arows[:100]:
            print(f"ARQUIVO_ROW|target={clean(target)}|value={clean(json.dumps(row,ensure_ascii=False,sort_keys=True),2400)}")

    _, ia, docs = ia_search()
    print(
        f"IA_SEARCH|ok={int(ia.get('ok',False))}|status={ia.get('status','')}|docs={len(docs)}|"
        f"error={clean(ia.get('error',''))}"
    )
    for doc in docs[:100]:
        print(f"IA_DOC|{clean(json.dumps(doc,ensure_ascii=False,sort_keys=True),2400)}")

    # If Wayback indexes a 200 response for the exact object, try the earliest
    # public replay once and emit hash/size only.
    exact_200 = [
        row for row in all_rows
        if str(row.get("statuscode")) == "200"
        and str(row.get("original", "")).lower().rstrip("/") == GM_HTTP.lower()
    ]
    seen = set()
    exact_200 = [
        x for x in sorted(exact_200, key=lambda y: str(y.get("timestamp", "")))
        if not ((str(x.get("timestamp","")), str(x.get("digest",""))) in seen
                or seen.add((str(x.get("timestamp","")), str(x.get("digest","")))))
    ]
    if exact_200:
        row = exact_200[0]
        try:
            fp = stream_wayback(str(row["timestamp"]), str(row["original"]))
            print(
                f"PAYLOAD_REPLAY|timestamp={clean(row['timestamp'])}|bytes={fp['bytes']}|"
                f"sha256={fp['sha256']}|prefix_hex={clean(fp['prefix'])}|final={clean(fp['final'],1800)}|"
                f"content_type={clean(fp['headers'].get('Content-Type'))}"
            )
            print("RESOLUTION|PUBLIC_WAYBACK_PAYLOAD_RECOVERED|compare against sa174hg only at byte level")
        except Exception as e:
            print(f"PAYLOAD_REPLAY_ERROR|kind={type(e).__name__}|message={clean(e,1600)}")
            print("RESOLUTION|EXACT_GAMANIA_IDENTITY_FOUND_PAYLOAD_REPLAY_FAILED")
    else:
        print("RESOLUTION|EXACT_GAMANIA_MIRROR_IDENTITY_EXPANDED|payload bytes not recovered from tested public indexes")

    print("EVIDENCE_BOUNDARY|2008/2020 community sources corroborate the sa174gm identity; only first-party bytes or independently preserved payload can establish build identity or equality with sa174hg.")

if __name__ == "__main__":
    main()
