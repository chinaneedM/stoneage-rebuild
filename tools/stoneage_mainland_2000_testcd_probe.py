#!/usr/bin/env python3
"""Probe public preservation metadata for the Dec-2000 Mainland StoneAge official test CD.

Source-derived facts only:
- China.com calls the object a StoneAge game test disc.
- official test window: 2000-12-15 through 2001-01-10.
- Beijing pickup route: Jinghe Software sales points.
- an early Jinghe profile independently says Jinghe organized free distribution
  of StoneAge test-version software.

Metadata only. No optical/archive payload body is downloaded.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
IA = "https://archive.org/advancedsearch.php"
IAMETA = "https://archive.org/metadata/"
DISCM = "https://discmaster.textfiles.com/search"

DISC_EXTS = (".iso", ".bin", ".cue", ".img", ".nrg", ".mdf", ".mds", ".ccd", ".sub", ".toast")
ARCHIVE_EXTS = (".zip", ".rar", ".7z", ".exe", ".cab")

QUERIES = (
    ("cn-test-disc", "石器时代 测试光盘"),
    ("cn-test-version-disc", "石器时代 测试版 光盘"),
    ("cn-trial-disc", "石器时代 试玩版 光盘"),
    ("cn-jinghe-test", "石器时代 晶合 测试"),
    ("cn-jinghe", "石器时代 晶合"),
    ("latin-test-cd", "StoneAge test CD"),
    ("latin-beta-waei", "StoneAge beta Waei"),
    ("latin-trial-waei", "StoneAge trial Waei"),
    ("latin-jinghe", "StoneAge Jinghe"),
    ("latin-jhpop", "StoneAge jhpop"),
)

def clean(v, n=2400):
    return " ".join(str(v or "").split()).replace("|", "%7C")[:n]

def normalized(v):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", str(v or "").lower())

def row_blob(row):
    if not isinstance(row, dict):
        return ""
    return normalized(" ".join(str(v or "") for v in row.values()))

def strict(row):
    blob = row_blob(row)
    title = "石器时代" in blob or "stoneage" in blob
    test = any(tok in blob for tok in (
        "测试", "试玩", "test", "trial", "beta", "晶合", "jinghe", "jhpop"
    ))
    return title and test

def fetch_json(url, timeout=35):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
        return int(getattr(r, "status", r.getcode())), r.geturl(), body, json.loads(body.decode("utf-8"))

def ia_url(q):
    p = [
        ("q", f'"{q}"'),
        ("fl[]", "identifier"), ("fl[]", "title"), ("fl[]", "date"), ("fl[]", "year"),
        ("fl[]", "description"), ("fl[]", "collection"), ("fl[]", "mediatype"),
        ("rows", "100"), ("page", "1"), ("output", "json"),
    ]
    return IA + "?" + urllib.parse.urlencode(p)

def discm_url(q):
    p = [
        ("q", f'"{q}"'), ("qfields", "t"), ("mode", "deep"), ("dedup", "dedup"),
        ("limit", "200"), ("outputAs", "json"), ("showItemName", "showItemName"),
        ("tsMin", "1999"), ("tsMax", "2002"),
    ]
    return DISCM + "?" + urllib.parse.urlencode(p)

def ia_docs(v):
    return tuple(x for x in v.get("response", {}).get("docs", []) if isinstance(x, dict))

def discm_rows(v):
    rows = []
    def walk(n):
        if isinstance(n, dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n):
                rows.append(n)
            for c in n.values():
                walk(c)
        elif isinstance(n, list):
            for c in n:
                walk(c)
    walk(v)
    out = []
    seen = set()
    for row in rows:
        key = (str(row.get("itemid", "")), str(row.get("fileid", "")), str(row.get("href", "")))
        if key not in seen:
            seen.add(key)
            out.append(row)
    return tuple(out)

def interesting_files(meta):
    out = []
    for row in meta.get("files", []) if isinstance(meta, dict) else []:
        if not isinstance(row, dict):
            continue
        low = str(row.get("name") or "").lower()
        if low.endswith(DISC_EXTS + ARCHIVE_EXTS):
            out.append(row)
    return tuple(out)

def main():
    print("StoneAge Mainland Dec-2000 official test-CD preservation probe — R1")
    print("SOURCE_ANCHOR|China.com|test-CD giveaway|official-test=2000-12-15..2001-01-10|Beijing-pickup=Jinghe")
    print("SCOPE|source-derived title/test/channel identities|InternetArchive+DiscMaster|metadata-only|no-payload")
    errors = []
    ia_hits = {}
    dm_hits = {}

    def one(kind, label, q):
        url = ia_url(q) if kind == "ia" else discm_url(q)
        st, final, body, data = fetch_json(url)
        rows = ia_docs(data) if kind == "ia" else discm_rows(data)
        hits = [row for row in rows if strict(row)]
        return kind, label, q, st, final, body, rows, hits

    jobs = [(kind, label, q) for label, q in QUERIES for kind in ("ia", "discm")]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(one, *job): job for job in jobs}
        for fut in concurrent.futures.as_completed(futs):
            kind, label, q = futs[fut]
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append((f"{kind}:{label}", type(exc).__name__, str(exc)))

    for kind, label, q, st, final, body, rows, hits in sorted(results, key=lambda x: (x[1], x[0])):
        digest = hashlib.sha256(body).hexdigest()
        if kind == "ia":
            print(f"IA_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(body)}|sha256={digest}|items={len(rows)}|strict={len(hits)}|final={clean(final)}")
            for row in hits:
                ident = str(row.get("identifier") or "")
                ia_hits[ident] = row
                print(f"IA_HIT|label={label}|identifier={clean(ident)}|title={clean(row.get('title'))}|date={clean(row.get('date'))}|year={clean(row.get('year'))}|mediatype={clean(row.get('mediatype'))}|collection={clean(row.get('collection'))}")
        else:
            print(f"DISCM_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(body)}|sha256={digest}|rows={len(rows)}|strict={len(hits)}|final={clean(final)}")
            for row in hits:
                key = (str(row.get("itemid", "")), str(row.get("fileid", "")))
                dm_hits[key] = row
                print(f"DISCM_HIT|label={label}|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}")

    file_hits = 0
    for ident, row in sorted(ia_hits.items()):
        try:
            st, final, body, meta = fetch_json(IAMETA + urllib.parse.quote(ident, safe=""))
            files = interesting_files(meta)
            print(f"IA_META|identifier={clean(ident)}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|interesting_files={len(files)}|final={clean(final)}")
            for fr in files[:300]:
                file_hits += 1
                print(f"IA_FILE|identifier={clean(ident)}|name={clean(fr.get('name'))}|size={clean(fr.get('size'))}|md5={clean(fr.get('md5'))}|sha1={clean(fr.get('sha1'))}|source={clean(fr.get('source'))}|format={clean(fr.get('format'))}")
        except Exception as exc:
            errors.append((f"ia-meta:{ident}", type(exc).__name__, str(exc)))

    for scope, kind, msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|queries|{len(QUERIES)}")
    print(f"COUNT|strict_ia_items|{len(ia_hits)}")
    print(f"COUNT|strict_discm_hits|{len(dm_hits)}")
    print(f"COUNT|ia_interesting_files|{file_hits}")
    print(f"COUNT|errors|{len(errors)}")

    if file_hits:
        print("RESOLUTION|PUBLIC_MEDIA_METADATA_FOUND|authenticate candidate against Dec-2000 China.com/Jinghe provenance before payload recovery")
    elif ia_hits or dm_hits:
        print("RESOLUTION|STRICT_METADATA_FOUND|inspect candidate identity and media availability")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_STRICT_HIT|retry failed metadata surfaces only")
    else:
        print("RESOLUTION|NO_STRICT_PRESERVATION_HIT|tested source-derived test-CD/channel identities expose no indexed carrier")
    print("EVIDENCE_BOUNDARY|zero indexed hit does not negate the contemporaneously documented physical test CD; reopen from disc art, magazine identity, exact filename, catalogue token, matrix, volume label or file tree.")

if __name__ == "__main__":
    main()
