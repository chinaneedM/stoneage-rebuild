#!/usr/bin/env python3
"""Probe a provisional visual transcription from the photographed early Mainland StoneAge disc.

The public Sohu mirror exposes a clearer copy of the 2016 disc photograph. The
disc line appears consistent with ISBN 7-900323-57-0 and a trailing TP·026-style
publication token. The publisher prefix 7-900323 is independently assigned to
Guangxi Jinhaiwan Electronic Audio-Visual Publishing House.

This script treats the full number as PROVISIONAL, never as a confirmed field.
It searches public preservation metadata only; no media payload is downloaded.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"

ISBN10="7900323570"
ISBN10_HYPHEN="7-900323-57-0"
ISBN13="9787900323576"
ISBN13_HYPHEN="978-7-900323-57-6"
AUX=("TP·026","TP.026","TP026")

QUERIES=(
    ("isbn10", ISBN10_HYPHEN),
    ("isbn10-compact", ISBN10),
    ("isbn13", ISBN13),
    ("isbn13-hyphen", ISBN13_HYPHEN),
    ("isbn10-stoneage", f"{ISBN10_HYPHEN} 石器时代"),
    ("isbn10-publisher", f"{ISBN10_HYPHEN} 广西金海湾"),
    ("aux-tp026-publisher", "TP026 广西金海湾 石器时代"),
)

def clean(v, n=2400):
    return " ".join(str(v or "").split()).replace("|","%7C")[:n]

def isbn10_valid(value):
    digits=re.sub(r"[^0-9Xx]","",value)
    if len(digits)!=10:
        return False
    vals=[10 if c in "Xx" else int(c) for c in digits]
    return sum((10-i)*d for i,d in enumerate(vals)) % 11 == 0

def isbn13_valid(value):
    digits=re.sub(r"[^0-9]","",value)
    if len(digits)!=13:
        return False
    return sum((1 if i%2==0 else 3)*int(d) for i,d in enumerate(digits)) % 10 == 0

def fetch_json(url, timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),body,json.loads(body.decode("utf-8"))

def ia_url(q):
    p=[("q",f'"{q}"'),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
       ("fl[]","year"),("fl[]","description"),("fl[]","collection"),("fl[]","mediatype"),
       ("rows","100"),("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(q):
    p=[("q",f'"{q}"'),("qfields","t"),("mode","deep"),("dedup","dedup"),("limit","200"),
       ("outputAs","json"),("showItemName","showItemName"),("tsMin","1999"),("tsMax","2004")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def ia_docs(v):
    return tuple(x for x in v.get("response",{}).get("docs",[]) if isinstance(x,dict))

def discm_rows(v):
    rows=[]
    def walk(n):
        if isinstance(n,dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n):
                rows.append(n)
            for c in n.values(): walk(c)
        elif isinstance(n,list):
            for c in n: walk(c)
    walk(v)
    out=[]; seen=set()
    for row in rows:
        k=(str(row.get("itemid","")),str(row.get("fileid","")),str(row.get("href","")))
        if k not in seen:
            seen.add(k); out.append(row)
    return tuple(out)

def normalized_blob(row):
    if not isinstance(row,dict):
        return ""
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+","", " ".join(str(v or "") for v in row.values()).lower())

def exact_candidate_hit(row):
    blob=normalized_blob(row)
    return ISBN10 in blob or ISBN13 in blob

def main():
    print("StoneAge early Mainland provisional ISBN preservation probe — R1")
    print("CLASSIFICATION|PROVISIONAL_VISUAL_TRANSCRIPTION|do-not-promote-without-higher-resolution-or-independent-record")
    print(f"CANDIDATE|isbn10={ISBN10_HYPHEN}|isbn13={ISBN13_HYPHEN}|aux={','.join(AUX)}")
    print(f"VALIDATION|isbn10_mod11={int(isbn10_valid(ISBN10_HYPHEN))}|isbn13_mod10={int(isbn13_valid(ISBN13_HYPHEN))}")
    print("PUBLISHER_PREFIX_CONTROL|7-900323|Guangxi-Jinhaiwan|independently-published-prefix-table")
    errors=[]; ia_hits={}; dm_hits={}

    def one(kind, label, q):
        url = ia_url(q) if kind == "ia" else discm_url(q)
        st, final, body, data = fetch_json(url)
        if kind == "ia":
            rows = ia_docs(data)
        else:
            rows = discm_rows(data)
        hits = [row for row in rows if exact_candidate_hit(row)]
        return kind, label, q, st, final, body, rows, hits

    jobs=[(kind,label,q) for label,q in QUERIES for kind in ("ia","discm")]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs={ex.submit(one,*job):job for job in jobs}
        for fut in concurrent.futures.as_completed(futs):
            kind,label,q=futs[fut]
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append((f"{kind}:{label}",type(exc).__name__,str(exc)))

    for kind,label,q,st,final,body,rows,hits in sorted(results,key=lambda x:(x[1],x[0])):
        if kind=="ia":
            print(f"IA_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|items={len(rows)}|exact_candidate_hits={len(hits)}|final={clean(final)}")
            for row in hits:
                ident=str(row.get("identifier") or "")
                ia_hits[ident]=row
                print(f"IA_HIT|identifier={clean(ident)}|title={clean(row.get('title'))}|date={clean(row.get('date'))}|year={clean(row.get('year'))}|mediatype={clean(row.get('mediatype'))}|collection={clean(row.get('collection'))}")
        else:
            print(f"DISCM_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|exact_candidate_hits={len(hits)}|final={clean(final)}")
            for row in hits:
                key=(str(row.get("itemid","")),str(row.get("fileid","")))
                dm_hits[key]=row
                print(f"DISCM_HIT|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|queries|{len(QUERIES)}")
    print(f"COUNT|strict_ia_items|{len(ia_hits)}")
    print(f"COUNT|strict_discm_hits|{len(dm_hits)}")
    print(f"COUNT|errors|{len(errors)}")
    if ia_hits or dm_hits:
        print("RESOLUTION|PROVISIONAL_IDENTIFIER_METADATA_FOUND|verify photograph transcription independently before promotion")
    elif errors:
        print("RESOLUTION|PARTIAL_PROVISIONAL_IDENTIFIER_SEARCH|retry failed metadata surfaces only")
    else:
        print("RESOLUTION|NO_PRESERVATION_HIT_FOR_PROVISIONAL_IDENTIFIER|retain only as search token pending better visual evidence")
    print("EVIDENCE_BOUNDARY|checksum validity and publisher-prefix agreement strengthen plausibility but do not independently prove the photographed suffix/item number.")

if __name__=="__main__":
    main()
