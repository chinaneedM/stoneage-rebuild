#!/usr/bin/env python3
"""Preservation-index probe for a photographed Mainland StoneAge retail box.

The small printed identifier is not yet readable with enough confidence for a FACT.
This probe preserves the initial transcription separately from checksum-consistent
final-digit hypotheses. Metadata search only: DiscMaster + Internet Archive.
No candidate payload download.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
DISCM="https://discmaster.textfiles.com/search"
IA="https://archive.org/advancedsearch.php"
TRANSCRIBED_QUERIES=(
    "7-900032-57-0",
    "7900032570",
    "9787900032570",
)
HYPOTHESIS_QUERIES=(
    "7-900032-57-6",
    "7900032576",
    "9787900032577",
)
CONTEXT_QUERIES=(
    "石器时代 网络游戏 华义",
    "StoneAge 北京华义 WAEI",
)
QUERIES=TRANSCRIBED_QUERIES+HYPOTHESIS_QUERIES+CONTEXT_QUERIES

def query_kind(q):
    if q in TRANSCRIBED_QUERIES:
        return "initial-photo-transcription"
    if q in HYPOTHESIS_QUERIES:
        return "checksum-consistent-hypothesis"
    return "context"

def clean(v,n=1800):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch_json(url,timeout=45,attempts=3):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read()
                return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8","replace"))
        except Exception as e:
            last=e
            if i+1<attempts:
                time.sleep(2*(i+1))
    raise last

def norm(s):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+","",str(s or "").lower())

def discm_url(q):
    p=[("q",f'"{q}"'),("qfields","t"),("mode","deep"),("dedup","dedup"),
       ("limit","100"),("outputAs","json"),("showItemName","showItemName"),
       ("tsMin","1999"),("tsMax","2006")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def ia_url(q):
    p=[("q",f'"{q}"'),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
       ("fl[]","year"),("fl[]","description"),("fl[]","collection"),
       ("rows","100"),("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_rows(v):
    rows=[]
    def walk(n):
        if isinstance(n,dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n):
                rows.append(n)
            for x in n.values():
                walk(x)
        elif isinstance(n,list):
            for x in n:
                walk(x)
    walk(v)
    out=[]; seen=set()
    for r in rows:
        key=(str(r.get("itemid","")),str(r.get("fileid","")),str(r.get("href","")))
        if key not in seen:
            seen.add(key); out.append(r)
    return tuple(out)

def ia_docs(v):
    r=v.get("response",{}) if isinstance(v,dict) else {}
    d=r.get("docs",[]) if isinstance(r,dict) else []
    return tuple(x for x in d if isinstance(x,dict))

def strict_match(blob):
    n=norm(blob)
    exact=any(norm(x) in n for x in TRANSCRIBED_QUERIES+HYPOTHESIS_QUERIES)
    title=norm("石器时代") in n or norm("StoneAge") in n
    operator=norm("华义") in n or norm("WAEI") in n
    return exact or (title and operator)

def query_one(q):
    out={"q":q,"errors":[]}
    try:
        u=discm_url(q); out["discm"]=fetch_json(u)
    except Exception as e:
        out["errors"].append(("discm",type(e).__name__,str(e)))
    try:
        u=ia_url(q); out["ia"]=fetch_json(u)
    except Exception as e:
        out["errors"].append(("ia",type(e).__name__,str(e)))
    return out

def main():
    print("StoneAge Mainland photographed retail-box preservation probe — R2")
    print("SCOPE|initial-photo-transcription+checksum-hypotheses|DiscMaster+IA-metadata|no-payload")
    print("ANCHOR|ruten=22636573895893|initial=7-900032-57-0,9787900032570|hypothesis=7-900032-57-6,9787900032577|visible_context=WAEI+WGS+StoneAge")
    print("IDENTIFIER_BOUNDARY|initial transcription fails ISBN-10/EAN-13 checksum; checksum-consistent final digits are hypotheses only, not confirmed photograph readings")
    errors=[]; strict_d={}; strict_i={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        results=list(ex.map(query_one,QUERIES))
    for res in results:
        q=res["q"]
        print(f"QUERY_KIND|query={clean(q)}|kind={query_kind(q)}")
        for scope,kind,msg in res["errors"]:
            errors.append((scope+":"+q,kind,msg))
        if "discm" in res:
            st,final,b,data=res["discm"]; rows=discm_rows(data)
            strict=[]
            for row in rows:
                blob=" ".join(str(row.get(k) or "") for k in ("itemName","fileid","filename","href","text","title"))
                if strict_match(blob): strict.append(row)
            print(f"DISCM_QUERY|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|strict={len(strict)}|final={clean(final)}")
            for row in strict:
                key=(str(row.get("itemid","")),str(row.get("fileid","")))
                strict_d[key]=row
                print(f"DISCM_HIT|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}")
        if "ia" in res:
            st,final,b,data=res["ia"]; docs=ia_docs(data)
            strict=[]
            for row in docs:
                blob=" ".join(str(row.get(k) or "") for k in ("identifier","title","description","date","year"))
                if strict_match(blob): strict.append(row)
            print(f"IA_QUERY|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|items={len(docs)}|strict={len(strict)}|final={clean(final)}")
            for row in strict:
                ident=str(row.get("identifier") or "")
                strict_i[ident]=row
                print(f"IA_HIT|identifier={clean(ident)}|title={clean(row.get('title'))}|date={clean(row.get('date'))}|year={clean(row.get('year'))}|collection={clean(row.get('collection'))}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|queries|{len(QUERIES)}")
    print(f"COUNT|strict_discm_hits|{len(strict_d)}")
    print(f"COUNT|strict_ia_items|{len(strict_i)}")
    print(f"COUNT|errors|{len(errors)}")
    if strict_d or strict_i:
        print("RESOLUTION|STRICT_PRESERVATION_METADATA_FOUND|inspect exact object and provenance next")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_STRICT_HIT|retry failed exact surfaces only")
    else:
        print("RESOLUTION|NO_STRICT_PRESERVATION_HIT|tested initial-transcription and checksum-hypothesis surfaces are bounded")
    print("EVIDENCE_BOUNDARY|neither the initial transcription nor checksum-consistent hypotheses are confirmed printed identifiers; preservation-index matches would be search leads only, not disc contents, mastering, release version, or byte relationship to any recovered client.")

if __name__=="__main__":
    main()
