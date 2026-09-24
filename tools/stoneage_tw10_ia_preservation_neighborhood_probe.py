#!/usr/bin/env python3
"""Probe the preservation neighborhood of the accepted Taiwan v1 IA item.

The seed is the S-grade public preservation item stoneage_tw_2000_win. The
probe derives its public uploader/creator/collection context, searches only
metadata for closely related StoneAge/Shiqi/Waei items, and checks candidate
file lists for Taiwan-v1 signatures and map/<n>.dat caches.

No item payload is downloaded. The uploader value is used for querying but is
not emitted verbatim; only a SHA-256 fingerprint is retained in the report.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
SEED="stoneage_tw_2000_win"
META="https://archive.org/metadata/{}"
ADV="https://archive.org/advancedsearch.php"

SIGNATURES=frozenset({
    "sa_3.exe",
    "adrn_1.bin",
    "spradrn_1.bin",
    "battletxt_1.txt",
    "soundaddr_1.txt",
    "waei.bin",
})
MAP_RE=re.compile(r"(?i)(?:^|[/\\])map[/\\](\d+)\.dat$")


def clean(value,limit=1200):
    if isinstance(value,list):
        value=",".join(str(x) for x in value)
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def get_json(url,timeout=25):
    request=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(request,timeout=timeout) as response:
        return json.load(response)


def item_metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier,safe="")))


def advanced_search(query,rows=200):
    params=[
        ("q",query),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","description"),
        ("fl[]","creator"),("fl[]","date"),("fl[]","year"),
        ("fl[]","mediatype"),("fl[]","collection"),
        ("rows",str(rows)),("page","1"),("output","json"),
    ]
    url=ADV+"?"+urllib.parse.urlencode(params)
    data=get_json(url)
    return url,data.get("response",{}).get("docs",[])


def quote_term(value):
    return '"' + str(value).replace('"','\\"') + '"'


def leaf(path):
    return str(path).replace("\\","/").rstrip("/").rsplit("/",1)[-1].lower()


def inspect_files(files):
    signatures=[]
    maps=[]
    for entry in files:
        name=str(entry.get("name",""))
        if leaf(name) in SIGNATURES:
            signatures.append(entry)
        if MAP_RE.search(name.replace("\\","/")):
            maps.append(entry)
    return signatures,maps


def related_text(doc):
    values=[
        doc.get("identifier",""),doc.get("title",""),doc.get("description",""),
        doc.get("creator",""),
    ]
    return " ".join(clean(v,5000).lower() for v in values)


def main():
    print("StoneAge Taiwan v1 Internet Archive preservation-neighborhood probe — R1")
    print("SCOPE|seed-uploader+creator+collection-neighborhood|item-filelist-metadata|no-payload-download")

    try:
        seed=item_metadata(SEED)
    except Exception as exc:
        print(f"ERROR|phase=seed|kind={type(exc).__name__}|message={clean(exc)}")
        print("RESOLUTION|INCONCLUSIVE|seed metadata unavailable")
        return

    meta=seed.get("metadata",{})
    uploader=str(meta.get("uploader","")).strip()
    creator=meta.get("creator","")
    collections=meta.get("collection",[])
    if not isinstance(collections,list):
        collections=[collections] if collections else []

    uploader_sha=hashlib.sha256(uploader.encode("utf-8")).hexdigest() if uploader else ""
    print(
        f"SEED|identifier={SEED}|title={clean(meta.get('title'))}|date={clean(meta.get('date') or meta.get('year'))}|"
        f"uploader_present={int(bool(uploader))}|uploader_sha256={uploader_sha}|"
        f"creator={clean(creator)}|collections={clean(collections)}|files={len(seed.get('files',[]))}"
    )

    queries=[]
    if uploader:
        uq=quote_term(uploader)
        for token in ("StoneAge","Shiqi","石器","Waei","華義"):
            queries.append((f"uploader-{token}",f"uploader:{uq} AND ({quote_term(token)})"))
    if creator:
        creator_value=creator[0] if isinstance(creator,list) and creator else creator
        if creator_value:
            cq=quote_term(creator_value)
            for token in ("StoneAge","Shiqi","石器","Waei","華義"):
                queries.append((f"creator-{token}",f"creator:{cq} AND ({quote_term(token)})"))
    for collection in collections[:8]:
        if collection:
            collection_q=quote_term(collection)
            queries.append((f"collection-{collection}-stoneage",f"collection:{collection_q} AND {quote_term('StoneAge')}"))
            queries.append((f"collection-{collection}-shiqi",f"collection:{collection_q} AND {quote_term('Shiqi')}"))

    docs={SEED:{
        "identifier":SEED,
        "title":meta.get("title",""),
        "description":meta.get("description",""),
        "creator":meta.get("creator",""),
        "date":meta.get("date") or meta.get("year",""),
        "collection":collections,
    }}
    query_labels={SEED:{"seed"}}
    errors=[]

    def one_search(entry):
        label,query=entry
        try:
            url,rows=advanced_search(query)
            return label,query,url,rows,None
        except Exception as exc:
            return label,query,"",[],(type(exc).__name__,str(exc))

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for label,query,url,rows,error in executor.map(one_search,queries):
            if error:
                errors.append((f"search:{label}",error[0],error[1]))
                continue
            print(f"QUERY|label={clean(label)}|results={len(rows)}|url={clean(url)}")
            for doc in rows:
                identifier=str(doc.get("identifier","")).strip()
                if identifier:
                    docs.setdefault(identifier,doc)
                    query_labels.setdefault(identifier,set()).add(label)

    # Keep only documents whose item-level metadata actually looks relevant.
    tokens=("stoneage","stone age","shiqi","石器","waei","華義")
    relevant={
        identifier:doc for identifier,doc in docs.items()
        if identifier==SEED or any(token in related_text(doc) for token in tokens)
    }

    def one_meta(identifier):
        try:
            return identifier,item_metadata(identifier),None
        except Exception as exc:
            return identifier,None,(type(exc).__name__,str(exc))

    metas={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for identifier,data,error in executor.map(one_meta,sorted(relevant)):
            if error:
                errors.append((f"metadata:{identifier}",error[0],error[1]))
            else:
                metas[identifier]=data

    qualified=0
    related_items=0
    map_items=0
    for identifier,data in sorted(metas.items()):
        m=data.get("metadata",{})
        doc=relevant.get(identifier,{})
        signatures,maps=inspect_files(data.get("files",[]))
        text=related_text({
            "identifier":identifier,
            "title":m.get("title",doc.get("title","")),
            "description":m.get("description",doc.get("description","")),
            "creator":m.get("creator",doc.get("creator","")),
        })
        is_related=identifier==SEED or any(token in text for token in tokens)
        if not is_related:
            continue
        related_items+=1
        map_items+=int(bool(maps))
        if len({leaf(x.get("name","")) for x in signatures})>=2 and maps:
            qualified+=1
        print(
            f"ITEM|identifier={clean(identifier)}|title={clean(m.get('title',doc.get('title')))}|"
            f"date={clean(m.get('date') or m.get('year') or doc.get('date') or doc.get('year'))}|"
            f"labels={clean(sorted(query_labels.get(identifier,set())))}|"
            f"files={len(data.get('files',[]))}|signatures={len(signatures)}|map_dat={len(maps)}"
        )
        for entry in signatures[:30]:
            print(
                f"SIGNATURE_HIT|identifier={clean(identifier)}|path={clean(entry.get('name'),1800)}|"
                f"size={clean(entry.get('size'))}|md5={clean(entry.get('md5'))}|sha1={clean(entry.get('sha1'))}"
            )
        for entry in maps[:100]:
            print(
                f"MAP_HIT|identifier={clean(identifier)}|path={clean(entry.get('name'),1800)}|"
                f"size={clean(entry.get('size'))}|md5={clean(entry.get('md5'))}|sha1={clean(entry.get('sha1'))}"
            )

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|queries|{len(queries)}")
    print(f"COUNT|query_items|{len(docs)}")
    print(f"COUNT|relevant_items|{related_items}")
    print(f"COUNT|metadata_fetched|{len(metas)}")
    print(f"COUNT|items_with_map_dat|{map_items}")
    print(f"COUNT|qualified_signature_plus_map|{qualified}")
    print(f"COUNT|errors|{len(errors)}")

    if qualified:
        print("RESOLUTION|PRESERVATION_NEIGHBORHOOD_MAP_CANDIDATES_FOUND|verify version identity before bytes are used")
    elif not errors:
        print("RESOLUTION|PRESERVATION_NEIGHBORHOOD_NO_QUALIFIED_MAP_CARRIER|seed neighborhood contains no multi-signature installed-tree map carrier")
    else:
        print("RESOLUTION|INCONCLUSIVE|preservation-neighborhood surface partially failed")


if __name__=="__main__":
    main()
