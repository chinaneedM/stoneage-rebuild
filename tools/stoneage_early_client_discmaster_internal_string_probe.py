#!/usr/bin/env python3
"""Search DiscMaster full-text indexes for early StoneAge client-internal strings.

These strings are byte-verified from the accepted Taiwan v1.0 client. The two
updater-route strings are especially distinctive because they are embedded in
StoneAge.exe:
  stoneage.waei.net
  /saupdate/newest.txt

Resource-name strings are supporting structural signals. Search is metadata /
indexed-text only; no file payload is fetched. A hit is a discovery lead, not
regional/version provenance.
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
    ("waei-host","stoneage.waei.net","anchor"),
    ("update-manifest","/saupdate/newest.txt","anchor"),
    ("spradrn","spradrn_1.bin","distinctive"),
    ("battle-index","battletxt_1.txt","distinctive"),
    ("sound-index","soundaddr_1.txt","distinctive"),
    ("stoneage-exe","StoneAge.exe","supporting"),
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

def fetch_json(url,timeout=45):
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

def one(sig):
    label,term,kind=sig
    url=search_url(term)
    st,final,body,data=fetch_json(url)
    return label,term,kind,st,final,body,rows(data)

def main():
    print("StoneAge early-client DiscMaster internal-string probe — R1")
    print("SCOPE|public full-text index|accepted-Taiwan-v1.0 internal strings|1999..2002|metadata-only|no payload")
    print("BOUNDARY|text-index hits can reveal packed/hidden client files but do not establish Mainland test-CD or clean-client provenance")
    results=[];errors=[]

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(one,s):s for s in SIGNATURES}
        for fut in concurrent.futures.as_completed(futs):
            s=futs[fut]
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append((s[0],type(exc).__name__,str(exc)))

    by_item=defaultdict(lambda:{"anchors":set(),"distinctive":set(),"supporting":set(),"labels":set(),"itemName":"","rows":[]})
    for label,term,kind,st,final,body,rr in sorted(results):
        print(
            f"QUERY|label={label}|term={clean(term)}|kind={kind}|status={st}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rr)}|final={clean(final)}"
        )
        for row in rr[:300]:
            itemid=str(row.get("itemid") or "")
            print(
                f"HIT|label={label}|kind={kind}|itemid={clean(itemid)}|itemName={clean(row.get('itemName'))}|"
                f"path={clean(row_path(row))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
            )
            if not itemid:
                continue
            rec=by_item[itemid]
            rec["labels"].add(label)
            if kind=="anchor":
                rec["anchors"].add(label)
            elif kind=="distinctive":
                rec["distinctive"].add(label)
            else:
                rec["supporting"].add(label)
            rec["itemName"]=str(row.get("itemName") or rec["itemName"])
            rec["rows"].append(row)

    candidates=[]
    for itemid,rec in sorted(by_item.items(),key=lambda kv:(-len(kv[1]["anchors"]),-len(kv[1]["distinctive"]),-len(kv[1]["supporting"]),kv[0])):
        a=len(rec["anchors"]);d=len(rec["distinctive"]);s=len(rec["supporting"])
        if a>=1 and (d+s)>=1:
            tier="STRONG"
        elif a>=1 or d>=2:
            tier="LEAD"
        else:
            tier="WEAK"
        print(
            f"CARRIER|tier={tier}|itemid={clean(itemid)}|itemName={clean(rec['itemName'])}|"
            f"anchors={a}|distinctive={d}|supporting={s}|signature_count={len(rec['labels'])}|"
            f"labels={','.join(sorted(rec['labels']))}"
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
        print("RESOLUTION|EARLY_CLIENT_INTERNAL_STRING_CARRIERS_FOUND|inspect carrier file neighborhood/provenance and verify bytes before promotion")
    elif len(results)==len(SIGNATURES) and not errors:
        print("RESOLUTION|NO_EARLY_CLIENT_INTERNAL_STRING_CARRIER|tested DiscMaster full-text index exposes no anchor/multi-signal early-client carrier")
    else:
        print("RESOLUTION|EARLY_CLIENT_INTERNAL_STRING_SURFACE_PARTIAL|retry failed exact terms only")
    print("EVIDENCE_BOUNDARY|A content-index match is discovery metadata only; exact client identity requires byte-level verification.")

if __name__=="__main__":
    main()
