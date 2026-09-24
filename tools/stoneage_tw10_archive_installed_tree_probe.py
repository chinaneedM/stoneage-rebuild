#!/usr/bin/env python3
"""Probe Internet Archive item/file-list metadata for Taiwan v1 installed-tree remnants.

The accepted Taiwan v1 retail disc has no ordinary field-map cache. This probe
searches public IA metadata for distinctive Taiwan-v1 client traits and then
checks returned item file lists for multiple signature files plus map/<n>.dat.
No item payload is downloaded.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import urllib.parse
import urllib.request
from collections import defaultdict

UA="stoneage-rebuild-archaeology/1.0"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"

SIGNATURES=(
    "sa_3.exe",
    "adrn_1.bin",
    "spradrn_1.bin",
    "battletxt_1.txt",
    "soundaddr_1.txt",
    "waei.bin",
)
QUERIES=tuple(f'"{name}"' for name in SIGNATURES)+(
    '"StoneAge" AND mediatype:software',
    '"Stone Age" AND mediatype:software',
    '"石器時代" AND mediatype:software',
    '"石器时代" AND mediatype:software',
    '"華義" AND "石器時代"',
    '"Waei" AND "StoneAge"',
)
MAP_RE=re.compile(r"(?i)(?:^|[/\\])map[/\\](\d+)\.dat$")


def clean(value,limit=1200):
    if isinstance(value,list):
        value=",".join(str(x) for x in value)
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def get_json(url,timeout=25):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.load(response)


def search(query):
    params=[
        ("q",query),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","description"),
        ("fl[]","creator"),("fl[]","date"),("fl[]","year"),
        ("fl[]","mediatype"),("fl[]","collection"),
        ("rows","100"),("page","1"),("output","json"),
    ]
    url=ADV+"?"+urllib.parse.urlencode(params)
    data=get_json(url)
    return url,data.get("response",{}).get("docs",[])


def metadata(identifier):
    url=META.format(urllib.parse.quote(identifier,safe=""))
    return url,get_json(url)


def leaf(path):
    return str(path).replace("\\","/").rstrip("/").rsplit("/",1)[-1].lower()


def inspect_files(files):
    sig_hits=defaultdict(list)
    maps=[]
    for entry in files:
        name=str(entry.get("name",""))
        lower_leaf=leaf(name)
        if lower_leaf in SIGNATURES:
            sig_hits[lower_leaf].append(entry)
        if MAP_RE.search(name.replace("\\","/")):
            maps.append(entry)
    return sig_hits,maps


def main():
    print("StoneAge Taiwan v1 Internet Archive installed-tree probe — R1")
    print("SCOPE|advancedsearch+item-filelist-metadata|tw1-signatures+map-cache|no-payload-download")

    docs={}
    query_hits=defaultdict(set)
    errors=[]
    for index,query in enumerate(QUERIES,1):
        try:
            url,rows=search(query)
        except Exception as exc:
            errors.append((f"search:{index}",type(exc).__name__,str(exc)))
            continue
        print(f"QUERY|n={index}|results={len(rows)}|q={clean(query)}|url={clean(url)}")
        for row in rows:
            identifier=str(row.get("identifier","")).strip()
            if identifier:
                docs.setdefault(identifier,row)
                query_hits[identifier].add(index)

    def one(identifier):
        try:
            url,data=metadata(identifier)
            return identifier,url,data,None
        except Exception as exc:
            return identifier,"",None,(type(exc).__name__,str(exc))

    metas={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for identifier,url,data,error in executor.map(one,sorted(docs)):
            if error:
                errors.append((f"metadata:{identifier}",error[0],error[1]))
            else:
                metas[identifier]=(url,data)

    carrier_count=0
    multi_count=0
    map_carriers=0
    map_rows=0
    for identifier,(url,data) in sorted(metas.items()):
        sig_hits,maps=inspect_files(data.get("files",[]))
        if not sig_hits and not maps:
            continue
        carrier_count+=1
        if len(sig_hits)>=2:
            multi_count+=1
        if maps:
            map_carriers+=1
            map_rows+=len(maps)
        doc=docs.get(identifier,{})
        print(
            f"CARRIER|identifier={clean(identifier)}|title={clean(doc.get('title'))}|"
            f"date={clean(doc.get('date') or doc.get('year'))}|creator={clean(doc.get('creator'))}|"
            f"queries={','.join(str(x) for x in sorted(query_hits.get(identifier,set())))}|"
            f"signature_count={len(sig_hits)}|signatures={','.join(sorted(sig_hits))}|"
            f"map_dat_rows={len(maps)}|metadata={clean(url)}"
        )
        for sig,rows in sorted(sig_hits.items()):
            for entry in rows[:20]:
                print(
                    f"SIGNATURE_HIT|identifier={clean(identifier)}|name={clean(sig)}|"
                    f"path={clean(entry.get('name'),1800)}|size={clean(entry.get('size'))}|"
                    f"md5={clean(entry.get('md5'))}|sha1={clean(entry.get('sha1'))}|"
                    f"format={clean(entry.get('format'))}"
                )
        for entry in maps[:200]:
            print(
                f"MAP_HIT|identifier={clean(identifier)}|path={clean(entry.get('name'),1800)}|"
                f"size={clean(entry.get('size'))}|md5={clean(entry.get('md5'))}|"
                f"sha1={clean(entry.get('sha1'))}|format={clean(entry.get('format'))}"
            )

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|queries|{len(QUERIES)}")
    print(f"COUNT|unique_items|{len(docs)}")
    print(f"COUNT|metadata_fetched|{len(metas)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|carriers_with_signature_or_map|{carrier_count}")
    print(f"COUNT|multi_signature_carriers|{multi_count}")
    print(f"COUNT|map_carriers|{map_carriers}")
    print(f"COUNT|map_dat_rows|{map_rows}")

    qualified=0
    for identifier,(url,data) in metas.items():
        sig_hits,maps=inspect_files(data.get("files",[]))
        if len(sig_hits)>=2 and maps:
            qualified+=1
    print(f"COUNT|qualified_signature_plus_map_carriers|{qualified}")

    if qualified:
        print("RESOLUTION|TW1_IA_INSTALLED_TREE_CANDIDATES_FOUND|verify hashes/lineage and map-cache bytes before use")
    elif not errors:
        print("RESOLUTION|TW1_IA_NO_QUALIFIED_INSTALLED_TREE|no item file list combines multiple v1 signatures with map/<n>.dat")
    else:
        print("RESOLUTION|INCONCLUSIVE|Internet Archive metadata surface partially failed")


if __name__=="__main__":
    main()
