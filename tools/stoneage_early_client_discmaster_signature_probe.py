#!/usr/bin/env python3
"""Find early StoneAge client carriers in DiscMaster by Taiwan-v1.0 file signatures.

The filename signatures are byte-verified members of the accepted Taiwan v1.0
clean client. This probe searches DiscMaster file-index metadata only and
intersects hits by carrier item ID.

A carrier hit is a recovery lead, not proof of Mainland test-CD identity,
regional provenance, version equivalence, or clean bytes.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.parse
import urllib.request
from collections import defaultdict

BASE="https://discmaster.textfiles.com/search"
UA="stoneage-rebuild-archaeology/1.0"

SIGNATURES=(
    ("real1","real_1.bin","distinctive"),
    ("adrn1","adrn_1.bin","distinctive"),
    ("spr1","spr_1.bin","distinctive"),
    ("spradrn1","spradrn_1.bin","distinctive"),
    ("battletxt1","battletxt_1.txt","distinctive"),
    ("soundaddr1","soundaddr_1.txt","distinctive"),
    ("sa3","sa_3.exe","supporting"),
    ("stoneage-exe","StoneAge.exe","supporting"),
    ("setup-inx","setup.inx","supporting"),
)

def clean(v,limit=1800):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]

def search_url(name):
    p=[
        ("q",f'"{name}"'),("qfields","name"),("mode","deep"),
        ("dedup","dedup"),("limit","300"),("outputAs","json"),
        ("showItemName","showItemName"),("tsMin","1999"),("tsMax","2002"),
    ]
    return BASE+"?"+urllib.parse.urlencode(p)

def fetch_json(url,timeout=40):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),body,json.loads(body.decode("utf-8"))

def rows(value):
    out=[]
    def walk(node):
        if isinstance(node,dict):
            if ("itemid" in node or "itemName" in node) and ("fileid" in node or "filename" in node or "name" in node):
                out.append(node)
            for child in node.values():
                walk(child)
        elif isinstance(node,list):
            for child in node:
                walk(child)
    walk(value)
    dedup={}
    for row in out:
        key=(str(row.get("itemid") or ""),str(row.get("fileid") or row.get("filename") or row.get("name") or ""))
        dedup[key]=row
    return tuple(dedup.values())

def row_path(row):
    return str(row.get("fileid") or row.get("filename") or row.get("name") or "").replace("\\","/")

def exact_leaf(row,name):
    return row_path(row).rstrip("/").rsplit("/",1)[-1].lower()==name.lower()

def one_signature(sig):
    label,name,kind=sig
    url=search_url(name)
    st,final,body,data=fetch_json(url)
    exact=tuple(row for row in rows(data) if exact_leaf(row,name))
    return label,name,kind,st,final,body,exact

def main():
    print("StoneAge early-client DiscMaster file-signature carrier probe — R1")
    print("SCOPE|public-file-index|accepted-Taiwan-v1.0 filenames|1999..2002|metadata-only|no indexed-file payload")
    print("BOUNDARY|shared filenames only generate leads; regional/version/clean identity requires carrier provenance and byte-level comparison")
    errors=[]
    results=[]

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futures={ex.submit(one_signature,sig):sig for sig in SIGNATURES}
        for fut in concurrent.futures.as_completed(futures):
            sig=futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append((sig[0],type(exc).__name__,str(exc)))

    by_item=defaultdict(lambda:{"labels":set(),"distinctive":set(),"supporting":set(),"rows":[],"itemName":""})
    for label,name,kind,st,final,body,exact in sorted(results):
        print(
            f"QUERY|label={label}|name={clean(name)}|kind={kind}|status={st}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|exact_rows={len(exact)}|final={clean(final)}"
        )
        for row in exact:
            itemid=str(row.get("itemid") or "")
            print(
                f"HIT|label={label}|kind={kind}|itemid={clean(itemid)}|itemName={clean(row.get('itemName'))}|"
                f"path={clean(row_path(row))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
            )
            if not itemid:
                continue
            rec=by_item[itemid]
            rec["labels"].add(label)
            rec[kind].add(label)
            rec["rows"].append(row)
            rec["itemName"]=str(row.get("itemName") or rec["itemName"])

    candidates=[]
    for itemid,rec in sorted(by_item.items(),key=lambda kv:(-len(kv[1]["distinctive"]),-len(kv[1]["supporting"]),kv[0])):
        d=len(rec["distinctive"])
        s=len(rec["supporting"])
        total=len(rec["labels"])
        if d>=4 and s>=1:
            tier="STRONG"
        elif d>=3:
            tier="LEAD"
        else:
            tier="WEAK"
        print(
            f"CARRIER|tier={tier}|itemid={clean(itemid)}|itemName={clean(rec['itemName'])}|"
            f"distinctive={d}|supporting={s}|signature_count={total}|labels={','.join(sorted(rec['labels']))}"
        )
        if tier!="WEAK":
            candidates.append((tier,itemid,rec))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|signature_queries|{len(SIGNATURES)}")
    print(f"COUNT|completed_queries|{len(results)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|unique_carriers|{len(by_item)}")
    print(f"COUNT|candidate_carriers|{len(candidates)}")
    print(f"COUNT|strong_carriers|{sum(1 for tier,_,_ in candidates if tier=='STRONG')}")
    if candidates:
        print("RESOLUTION|EARLY_CLIENT_SIGNATURE_CARRIERS_FOUND|inspect carrier date,title,file-neighborhood and provenance; compare bytes before promotion")
    elif len(results)==len(SIGNATURES) and not errors:
        print("RESOLUTION|NO_EARLY_CLIENT_SIGNATURE_CARRIER|tested DiscMaster filename index exposes no multi-signal carrier")
    else:
        print("RESOLUTION|EARLY_CLIENT_SIGNATURE_SURFACE_PARTIAL|retry only failed signature queries")
    print("EVIDENCE_BOUNDARY|A multi-signature carrier can reveal a hidden client tree but cannot identify it as the Dec-2000 Mainland test CD without independent provenance.")

if __name__=="__main__":
    main()
