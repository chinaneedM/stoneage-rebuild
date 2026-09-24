#!/usr/bin/env python3
"""Find StoneAge 2.5-family client carriers in DiscMaster by verified file signatures.

The signatures come from the recovered 2.5 bridge resource tree. This probe uses
DiscMaster file-index metadata only; it does not fetch indexed proprietary files.
A hit is a recovery candidate, not proof that the carrier is a clean 2002 client.
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

# Distinctive names are byte-verified as present in the recovered 2.5-family bridge.
# Generic runtime/install names are supporting signals only.
SIGNATURES=(
    ("adrn15","adrn_15.bin","distinctive"),
    ("real15","real_15.bin","distinctive"),
    ("spradrn5","spradrn_5.bin","distinctive"),
    ("stoneage-exe","StoneAge.exe","supporting"),
    ("startup-exe","Startup.exe","supporting"),
    ("unwise-exe","UNWISE.EXE","supporting"),
)


def clean(v,limit=1600):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def search_url(name):
    p=[
        ("q",f'"{name}"'),("qfields","name"),("mode","deep"),
        ("dedup","dedup"),("limit","100"),("outputAs","json"),
        ("showItemName","showItemName"),("tsMin","2000"),("tsMax","2006"),
    ]
    return BASE+"?"+urllib.parse.urlencode(p)


def fetch_json(url,timeout=30):
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
    print("StoneAge 2.5-family DiscMaster client-signature carrier probe — R1")
    print("SCOPE|public-file-index|verified-bridge-filenames|metadata-only|no-indexed-file-payload")
    print("BOUNDARY|bridge signatures can locate related client trees but cannot by themselves date or authenticate a carrier as 2002/clean")

    results=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futures={ex.submit(one_signature,sig):sig for sig in SIGNATURES}
        for fut in concurrent.futures.as_completed(futures):
            sig=futures[fut]
            try:
                results.append(fut.result())
            except Exception as e:
                errors.append((sig[0],type(e).__name__,str(e)))

    by_item=defaultdict(lambda:{"labels":set(),"distinctive":set(),"rows":[],"itemName":""})
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
            if kind=="distinctive":
                rec["distinctive"].add(label)
            rec["rows"].append(row)
            rec["itemName"]=str(row.get("itemName") or rec["itemName"])

    candidates=[]
    for itemid,rec in sorted(by_item.items(),key=lambda kv:(-len(kv[1]["distinctive"]),-len(kv[1]["labels"]),kv[0])):
        d=len(rec["distinctive"]); total=len(rec["labels"])
        tier="STRONG" if d>=2 else ("LEAD" if d>=1 and total>=2 else "WEAK")
        print(
            f"CARRIER|tier={tier}|itemid={clean(itemid)}|itemName={clean(rec['itemName'])}|"
            f"distinctive={d}|signature_count={total}|labels={','.join(sorted(rec['labels']))}"
        )
        if tier!="WEAK":
            candidates.append((tier,itemid,rec))

    for label,kind,msg in errors:
        print(f"ERROR|scope={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|signature_queries|{len(SIGNATURES)}")
    print(f"COUNT|completed_queries|{len(results)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|unique_carriers|{len(by_item)}")
    print(f"COUNT|candidate_carriers|{len(candidates)}")
    print(f"COUNT|strong_carriers|{sum(1 for tier,_,_ in candidates if tier=='STRONG')}")
    if candidates:
        print("RESOLUTION|SA25_FAMILY_CARRIER_CANDIDATES_FOUND|inspect carrier title,date,file-neighborhood,and provenance before recovery promotion")
    elif len(results)==len(SIGNATURES) and not errors:
        print("RESOLUTION|NO_SA25_SIGNATURE_CARRIER|tested DiscMaster filename index has no multi-signal 2.5-family carrier")
    else:
        print("RESOLUTION|INCONCLUSIVE|DiscMaster signature surface incomplete")


if __name__=="__main__":
    main()
