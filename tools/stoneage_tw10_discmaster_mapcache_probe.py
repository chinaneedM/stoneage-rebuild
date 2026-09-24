#!/usr/bin/env python3
"""Find provenance-relevant Taiwan v1 StoneAge installed-tree/map-cache carriers in DiscMaster.

The accepted retail disc itself has no ordinary field maps. This probe searches
DiscMaster's public file-level index for distinctive Taiwan-v1 client filenames,
groups hits by root carrier item, then looks inside multi-signature carriers for
map/*.dat-style cache files. Metadata/index access only; no indexed file payload
is downloaded.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import urllib.parse
import urllib.request
from collections import defaultdict

BASE="https://discmaster.textfiles.com/search"
UA="stoneage-rebuild-archaeology/1.0"

SIGNATURES=(
    ("runtime","sa_3.exe"),
    ("graphics-index","adrn_1.bin"),
    ("sprite-index","spradrn_1.bin"),
    ("battle-index","battletxt_1.txt"),
    ("sound-index","soundaddr_1.txt"),
    ("taiwan-marker","waei.bin"),
)

MAP_NAME_RE=re.compile(r"(?i)(?:^|[/\\])map[/\\](\d+)\.dat$")


def clean(value,limit=1200):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def search_url(*,q,qfields="name",itemid=None,extension=None,limit=100):
    params=[
        ("q",q),("qfields",qfields),("mode","deep"),
        ("limit",str(limit)),("outputAs","json"),("showItemName","showItemName"),
    ]
    if itemid is not None:
        params.append(("itemid",str(itemid)))
    if extension:
        params.append(("extension",extension))
    return BASE+"?"+urllib.parse.urlencode(params)


def fetch_json(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return (
            int(getattr(response,"status",response.getcode())),
            response.geturl(),
            body,
            json.loads(body.decode("utf-8")),
        )


def result_rows(value):
    rows=[]
    def walk(node):
        if isinstance(node,dict):
            if (
                ("itemid" in node or "itemName" in node)
                and ("fileid" in node or "filename" in node or "name" in node)
            ):
                rows.append(node)
            for child in node.values():
                walk(child)
        elif isinstance(node,list):
            for child in node:
                walk(child)
    walk(value)
    dedup={}
    for row in rows:
        key=(
            str(row.get("itemid","")),
            str(row.get("fileid","")),
            str(row.get("filename",row.get("name",""))),
        )
        dedup[key]=row
    return tuple(dedup.values())


def row_path(row):
    return str(row.get("fileid") or row.get("path") or row.get("filename") or row.get("name") or "")


def one_signature(entry):
    label,name=entry
    url=search_url(q=f'"{name}"',qfields="name")
    status,final,body,data=fetch_json(url)
    rows=result_rows(data)
    exact=[]
    target=name.lower()
    for row in rows:
        path=row_path(row).replace("\\","/").lower()
        leaf=path.rsplit("/",1)[-1]
        if leaf==target:
            exact.append(row)
    return label,name,url,status,final,body,tuple(exact)


def map_candidates_for_item(itemid):
    # Search by the stable cache leaf prefix inside one carrier, then enforce
    # exact map/<number>.dat shape locally.
    url=search_url(q="map",qfields="name",itemid=itemid,extension=".dat",limit=1000)
    status,final,body,data=fetch_json(url)
    rows=result_rows(data)
    matches=[]
    for row in rows:
        path=row_path(row).replace("\\","/")
        if MAP_NAME_RE.search(path):
            matches.append(row)
    return url,status,final,body,tuple(matches)


def main():
    print("StoneAge Taiwan v1 DiscMaster map-cache carrier probe — R1")
    print("SCOPE|public-file-index|tw1-signature-carriers+map-dat-followup|metadata-only|no-file-payload")

    sig_results=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures={executor.submit(one_signature,sig):sig for sig in SIGNATURES}
        for future in concurrent.futures.as_completed(futures):
            label,name=futures[future]
            try:
                sig_results.append(future.result())
            except Exception as exc:
                errors.append((label,type(exc).__name__,str(exc)))

    by_item=defaultdict(lambda:{"labels":set(),"rows":[],"itemName":""})
    for label,name,url,status,final,body,rows in sorted(sig_results):
        print(
            f"SIGNATURE_QUERY|label={label}|name={clean(name)}|status={status}|"
            f"bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"exact_rows={len(rows)}|final={clean(final)}"
        )
        for row in rows:
            itemid=str(row.get("itemid",""))
            if not itemid:
                continue
            rec=by_item[itemid]
            rec["labels"].add(label)
            rec["rows"].append(row)
            rec["itemName"]=str(row.get("itemName",rec["itemName"]))
            print(
                f"SIGNATURE_HIT|label={label}|itemid={clean(itemid)}|"
                f"itemName={clean(row.get('itemName'))}|path={clean(row_path(row),1800)}|"
                f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|"
                f"b3sum={clean(row.get('b3sum'))}"
            )

    candidates=[]
    for itemid,rec in sorted(by_item.items(),key=lambda kv:(-len(kv[1]["labels"]),kv[0])):
        score=len(rec["labels"])
        print(
            f"CARRIER|itemid={clean(itemid)}|itemName={clean(rec['itemName'])}|"
            f"signature_count={score}|labels={','.join(sorted(rec['labels']))}"
        )
        if score>=2:
            candidates.append((itemid,rec))

    map_total=0
    for itemid,rec in candidates:
        try:
            url,status,final,body,matches=map_candidates_for_item(itemid)
        except Exception as exc:
            errors.append((f"map:{itemid}",type(exc).__name__,str(exc)))
            continue
        map_total+=len(matches)
        print(
            f"MAP_QUERY|itemid={clean(itemid)}|status={status}|bytes={len(body)}|"
            f"sha256={hashlib.sha256(body).hexdigest()}|map_dat_rows={len(matches)}|"
            f"final={clean(final)}"
        )
        for row in matches[:200]:
            print(
                f"MAP_HIT|itemid={clean(itemid)}|itemName={clean(row.get('itemName'))}|"
                f"path={clean(row_path(row),1800)}|size={clean(row.get('size'))}|"
                f"ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
            )

    for label,kind,message in errors:
        print(f"ERROR|scope={clean(label)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|signature_queries|{len(SIGNATURES)}")
    print(f"COUNT|completed_signature_queries|{len(sig_results)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|unique_signature_carriers|{len(by_item)}")
    print(f"COUNT|multi_signature_carriers|{len(candidates)}")
    print(f"COUNT|map_dat_rows|{map_total}")

    if map_total:
        print("RESOLUTION|TW1_MAPCACHE_CARRIER_CANDIDATES_FOUND|verify carrier lineage and cache bytes before historical use")
    elif candidates:
        print("RESOLUTION|TW1_SIGNATURE_CARRIERS_NO_MAPCACHE_HIT|multi-signature carriers found but no indexed map/<n>.dat")
    elif len(sig_results)==len(SIGNATURES) and not errors:
        print("RESOLUTION|TW1_NO_MULTI_SIGNATURE_CARRIER|no provenance-grade installed-tree carrier in tested DiscMaster index")
    else:
        print("RESOLUTION|INCONCLUSIVE|DiscMaster Taiwan-v1 signature surface incomplete")


if __name__=="__main__":
    main()
