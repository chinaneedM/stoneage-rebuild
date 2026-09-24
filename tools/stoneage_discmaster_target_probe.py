#!/usr/bin/env python3
"""Probe DiscMaster's public file index for exact StoneAge Japan carrier traits.

Metadata/search results only. This does not fetch indexed file payloads.
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

BASE="https://discmaster.textfiles.com/search"
UA="stoneage-rebuild-archaeology/1.0"

TARGETS=(
    ("sa174hg-exact-name","name",'"sa174hg.exe"',{}),
    ("sa174hg-stem-name","name",'"sa174hg"',{}),
    ("sa174hg-content","t",'"sa174hg.exe"',{}),
    ("japanese-title-content","t",'"ストーンエイジ"',{"tsMin":"2003","tsMax":"2004"}),
    ("hangame-stoneage-content","t",'Hangame AND StoneAge',{"tsMin":"2003","tsMax":"2004"}),
    ("gamania-stoneage-content","t",'Gamania AND StoneAge',{"tsMin":"2003","tsMax":"2004"}),
    ("package-model-content","t",'"WR-04156"',{}),
    ("package-jan-content","t",'"4988609011565"',{}),
)


def clean(value,limit=1200):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def query_url(field,query,extra=None):
    params=[
        ("q",query),
        ("qfields",field),
        ("mode","deep"),
        ("dedup","dedup"),
        ("limit","100"),
        ("outputAs","json"),
        ("showItemName","showItemName"),
    ]
    for key,value in (extra or {}).items():
        params.append((key,value))
    return BASE+"?"+urllib.parse.urlencode(params)


def fetch(url,timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return {
            "status":int(getattr(response,"status",response.getcode())),
            "final":response.geturl(),
            "body":response.read(),
            "content_type":response.headers.get("Content-Type",""),
        }


def walk_candidate_dicts(value):
    out=[]
    def walk(node):
        if isinstance(node,dict):
            keys={str(k).lower() for k in node}
            if keys & {"name","path","filename","itemid","fileid","url","href"}:
                out.append(node)
            for child in node.values():
                walk(child)
        elif isinstance(node,list):
            for child in node:
                walk(child)
    walk(value)
    return out


def compact_candidate(row):
    wanted=("itemid","item","itemName","fileid","name","filename","path","family","format","size","ts","url","href","b3sum")
    parts=[]
    for key in wanted:
        if key in row and row[key] not in (None,"",[],{}):
            parts.append(f"{key}={clean(row[key],500)}")
    return ";".join(parts)


def main():
    print("StoneAge Japan DiscMaster target probe — R1")
    print("SCOPE|public-file-index|filename+content-search|deep-mode|metadata-only|no-file-payload")
    completed=0
    errors=0
    positive=0
    total_candidates=0

    for label,field,query,extra in TARGETS:
        url=query_url(field,query,extra)
        try:
            result=fetch(url)
        except Exception as exc:
            errors+=1
            print(f"ERROR|label={label}|kind={type(exc).__name__}|message={clean(exc)}")
            continue
        completed+=1
        body=result["body"]
        try:
            parsed=json.loads(body.decode("utf-8"))
        except Exception as exc:
            errors+=1
            print(
                f"QUERY|label={label}|status={result['status']}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|content_type={clean(result['content_type'])}|"
                f"json=0|final={clean(result['final'])}"
            )
            print(f"ERROR|label={label}|kind=JSONDecodeError|message={clean(exc)}")
            continue

        candidates=walk_candidate_dicts(parsed)
        compact=[]
        seen=set()
        for row in candidates:
            text=compact_candidate(row)
            if not text or text in seen:
                continue
            seen.add(text)
            compact.append(text)
        target_fold=query.replace('"',"").lower()
        body_fold=body.decode("utf-8","replace").lower()
        literal_hits=body_fold.count(target_fold) if target_fold else 0
        if compact:
            positive+=1
        total_candidates+=len(compact)
        top_keys=",".join(sorted(str(k) for k in parsed.keys())) if isinstance(parsed,dict) else type(parsed).__name__
        print(
            f"QUERY|label={label}|field={field}|status={result['status']}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|json=1|top={clean(top_keys)}|"
            f"candidate_dicts={len(compact)}|literal_hits={literal_hits}|final={clean(result['final'])}"
        )
        for n,text in enumerate(compact[:30],1):
            print(f"CANDIDATE|label={label}|order={n}|{text}")

    print(f"COUNT|queries|{len(TARGETS)}")
    print(f"COUNT|completed|{completed}")
    print(f"COUNT|errors|{errors}")
    print(f"COUNT|positive_queries|{positive}")
    print(f"COUNT|candidate_dicts|{total_candidates}")
    if positive:
        print("RESOLUTION|DISCMaster_CANDIDATES_FOUND|inspect carrier/item provenance before promotion")
    elif completed==len(TARGETS) and errors==0:
        print("RESOLUTION|DISCMaster_NO_TARGET_HIT|no matching indexed file metadata in tested exact/deep searches")
    else:
        print("RESOLUTION|INCONCLUSIVE|DiscMaster target surface incomplete")


if __name__=="__main__":
    main()
