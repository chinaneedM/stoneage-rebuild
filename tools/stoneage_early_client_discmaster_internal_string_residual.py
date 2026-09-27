#!/usr/bin/env python3
"""Retry only failed DiscMaster full-text terms from early-client R1.

Parent R1 completed:
- stoneage.waei.net -> 0 rows
- StoneAge.exe -> 0 rows

Only these timed out and remain open:
- /saupdate/newest.txt
- spradrn_1.bin
- battletxt_1.txt
- soundaddr_1.txt

This residual runs sequentially with bounded retries to avoid reproducing
parallel timeout pressure. Metadata/indexed-text only; no payload is fetched.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request

BASE="https://discmaster.textfiles.com/search"
UA="stoneage-rebuild-archaeology/1.0"

TERMS=(
    ("update-manifest","/saupdate/newest.txt","anchor"),
    ("spradrn","spradrn_1.bin","distinctive"),
    ("battle-index","battletxt_1.txt","distinctive"),
    ("sound-index","soundaddr_1.txt","distinctive"),
)

def clean(v,limit=2200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]

def search_url(term):
    p=[
        ("q",f'"{term}"'),("qfields","t"),("mode","deep"),
        ("dedup","dedup"),("limit","300"),("outputAs","json"),
        ("showItemName","showItemName"),("tsMin","1999"),("tsMax","2002"),
    ]
    return BASE+"?"+urllib.parse.urlencode(p)

def fetch_json(url,timeout=55):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),body,json.loads(body.decode("utf-8"))

def rows(value):
    out=[]
    def walk(node):
        if isinstance(node,dict):
            if ("itemid" in node or "itemName" in node) and ("fileid" in node or "filename" in node or "name" in node or "href" in node):
                out.append(node)
            for child in node.values():
                walk(child)
        elif isinstance(node,list):
            for child in node:
                walk(child)
    walk(value)
    dedup={}
    for row in out:
        key=(str(row.get("itemid") or ""),str(row.get("fileid") or row.get("path") or row.get("filename") or row.get("name") or row.get("href") or ""))
        dedup[key]=row
    return tuple(dedup.values())

def row_path(row):
    return str(row.get("fileid") or row.get("path") or row.get("filename") or row.get("name") or row.get("href") or "").replace("\\","/")

def main():
    print("StoneAge early-client DiscMaster internal-string residual — R2")
    print("PARENT|STONEAGE-EARLY-CLIENT-DISCMASTER-INTERNAL-STRINGS-R1|failed-terms-only")
    print("SCOPE|four timed-out exact full-text terms|sequential bounded retries|1999..2002|metadata-only|no payload")
    errors=[]
    completed={}
    all_items={}

    for label,term,kind in TERMS:
        url=search_url(term)
        success=False
        for attempt in range(1,4):
            try:
                st,final,body,data=fetch_json(url,timeout=55)
                rr=rows(data)
                completed[label]=(term,kind,rr)
                success=True
                print(
                    f"QUERY|label={label}|term={clean(term)}|kind={kind}|attempt={attempt}|"
                    f"status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
                    f"rows={len(rr)}|final={clean(final)}"
                )
                for row in rr[:300]:
                    itemid=str(row.get("itemid") or "")
                    print(
                        f"HIT|label={label}|kind={kind}|itemid={clean(itemid)}|"
                        f"itemName={clean(row.get('itemName'))}|path={clean(row_path(row))}|"
                        f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
                    )
                    if itemid:
                        rec=all_items.setdefault(itemid,{"labels":set(),"itemName":str(row.get("itemName") or "")})
                        rec["labels"].add(label)
                        if not rec["itemName"]:
                            rec["itemName"]=str(row.get("itemName") or "")
                break
            except Exception as exc:
                print(f"RETRY_ERROR|label={label}|attempt={attempt}|kind={type(exc).__name__}|message={clean(exc)}")
                if attempt<3:
                    time.sleep(attempt*2)
                else:
                    errors.append((label,type(exc).__name__,str(exc)))
        if success:
            time.sleep(1)

    for itemid,rec in sorted(all_items.items(),key=lambda kv:(-len(kv[1]["labels"]),kv[0])):
        print(f"CARRIER|itemid={clean(itemid)}|itemName={clean(rec['itemName'])}|signature_count={len(rec['labels'])}|labels={','.join(sorted(rec['labels']))}")

    for label,kind,msg in errors:
        print(f"ERROR|scope={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|terms|{len(TERMS)}")
    print(f"COUNT|completed|{len(completed)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|unique_carriers|{len(all_items)}")

    manifest_rows=len(completed.get("update-manifest",("", "", ())) [2]) if "update-manifest" in completed else -1
    print(f"COUNT|update_manifest_rows|{manifest_rows}")
    if all_items:
        print("RESOLUTION|INTERNAL_STRING_RESIDUAL_HITS_FOUND|classify carrier co-occurrence and provenance before promotion")
    elif len(completed)==len(TERMS) and not errors:
        print("RESOLUTION|INTERNAL_STRING_RESIDUAL_BOUNDED|all R1 timeout terms completed with zero indexed carriers")
    else:
        print("RESOLUTION|INTERNAL_STRING_RESIDUAL_PARTIAL|retain only unresolved failed terms")
    print("EVIDENCE_BOUNDARY|Zero full-text rows bound only the tested DiscMaster index; they do not negate historical client existence.")

if __name__=="__main__":
    main()
