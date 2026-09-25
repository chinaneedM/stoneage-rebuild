#!/usr/bin/env python3
"""Discover Internet Archive optical siblings around known Mainland StoneAge discs.

Metadata/file-list only. No disc image or game payload bytes are downloaded.
The probe starts from known item Stoneage-5, learns its uploader when exposed,
then searches creator/title/collection/uploader surfaces for sibling CD images.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"
SEEDS=("Stoneage-5","sa-arena")
OPTICAL_EXTS=(".iso",".bin",".cue",".img",".ccd",".nrg",".mdf",".mds")
BASE_QUERIES=(
    'creator:"北京华义联合软件开发有限公司"',
    'title:("石器时代" OR Stoneage OR StoneAge) AND mediatype:software',
    'description:("石器时代" OR Stoneage OR StoneAge) AND mediatype:software',
    'collection:cdrom_contributions AND ("石器时代" OR Stoneage OR StoneAge)',
)


def clean(v,n=1200):
    if isinstance(v,list):
        v=",".join(str(x) for x in v)
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def get_json(url,timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.load(r)


def search(q,rows=200):
    params=[
        ("q",q),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","creator"),
        ("fl[]","date"),("fl[]","year"),("fl[]","collection"),
        ("fl[]","description"),("fl[]","mediatype"),
        ("rows",str(rows)),("page","1"),("output","json"),
    ]
    url=ADV+"?"+urllib.parse.urlencode(params)
    data=get_json(url)
    return url,data.get("response",{}).get("docs",[])


def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier,safe="")))


def optical_rows(files):
    out=[]
    for row in files or []:
        name=str(row.get("name") or "")
        if not name.lower().endswith(OPTICAL_EXTS):
            continue
        out.append({
            "name":name,
            "size":str(row.get("size") or ""),
            "md5":str(row.get("md5") or ""),
            "sha1":str(row.get("sha1") or ""),
            "crc32":str(row.get("crc32") or ""),
            "source":str(row.get("source") or ""),
            "format":str(row.get("format") or ""),
        })
    return tuple(out)


def relevant_doc(doc):
    text=" ".join(str(doc.get(k) or "") for k in ("identifier","title","description")).lower()
    return any(k in text for k in ("stoneage","stone age","石器时代","石器時代","sa_arena"))


def main():
    print("StoneAge Mainland Internet Archive optical-sibling discovery — R2")
    print("SCOPE|advancedsearch+item-filelist-metadata|no-disc-download|no-game-payload-read")

    docs={}
    query_hits={}
    metas={}
    errors=[]

    for seed in SEEDS:
        try:
            data=metadata(seed)
            metas[seed]=data
            md=data.get("metadata",{})
            docs[seed]={
                "identifier":seed,
                "title":md.get("title"),
                "creator":md.get("creator"),
                "date":md.get("date"),
                "collection":md.get("collection"),
                "description":md.get("description"),
            }
        except Exception as exc:
            errors.append(("seed",seed,type(exc).__name__,str(exc)))

    uploaders=set()
    for data in metas.values():
        md=data.get("metadata",{})
        uploader=str(md.get("uploader") or "").strip()
        if uploader:
            uploaders.add(uploader)

    queries=list(BASE_QUERIES)
    for uploader in sorted(uploaders):
        escaped=uploader.replace('"','\\\"')
        queries.append(f'uploader:"{escaped}"')

    for qi,q in enumerate(queries,1):
        try:
            url,rows=search(q)
            print(f"QUERY|n={qi}|results={len(rows)}|q={clean(q)}|url={clean(url,2200)}")
        except Exception as exc:
            errors.append(("search",str(qi),type(exc).__name__,str(exc)))
            continue
        for row in rows:
            ident=str(row.get("identifier") or "").strip()
            if not ident or not relevant_doc(row):
                continue
            docs.setdefault(ident,row)
            query_hits.setdefault(ident,set()).add(qi)

    for ident in sorted(docs):
        if ident in metas:
            continue
        try:
            metas[ident]=metadata(ident)
        except Exception as exc:
            errors.append(("metadata",ident,type(exc).__name__,str(exc)))

    optical_items=0
    for ident in sorted(metas,key=str.lower):
        data=metas[ident]
        md=data.get("metadata",{})
        files=optical_rows(data.get("files",[]))
        if not files:
            continue
        optical_items+=1
        uploader=clean(md.get("uploader"))
        print(
            f"ITEM|identifier={clean(ident)}|title={clean(md.get('title') or docs.get(ident,{}).get('title'))}|"
            f"date={clean(md.get('date') or md.get('year'))}|creator={clean(md.get('creator'))}|"
            f"uploader={uploader}|collection={clean(md.get('collection'))}|"
            f"queries={','.join(str(x) for x in sorted(query_hits.get(ident,set())))}|"
            f"optical_files={len(files)}"
        )
        for row in files:
            print(
                f"OPTICAL|identifier={clean(ident)}|name={clean(row['name'],2200)}|size={clean(row['size'])}|"
                f"md5={clean(row['md5'])}|sha1={clean(row['sha1'])}|crc32={clean(row['crc32'])}|"
                f"source={clean(row['source'])}|format={clean(row['format'])}"
            )

    for scope,key,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|key={clean(key)}|kind={clean(kind)}|message={clean(msg)}")

    print(f"COUNT|seed_items|{len(SEEDS)}")
    print(f"COUNT|seed_uploaders|{len(uploaders)}")
    print(f"COUNT|queries|{len(queries)}")
    print(f"COUNT|relevant_items|{len(docs)}")
    print(f"COUNT|metadata_fetched|{len(metas)}")
    print(f"COUNT|optical_items|{optical_items}")
    print(f"COUNT|errors|{len(errors)}")
    if optical_items>1:
        print("RESOLUTION|OPTICAL_SIBLINGS_FOUND|inspect StoneAge-version candidates with bounded filesystem probes")
    else:
        print("RESOLUTION|NO_ADDITIONAL_OPTICAL_SIBLINGS|tested current metadata surfaces expose no extra optical StoneAge carriers")
    print("EVIDENCE_BOUNDARY|IA title/date/creator/uploader fields are catalogue metadata; file hashes describe preserved objects only and do not establish original release date, pressing or clean-client provenance.")


if __name__=="__main__":
    main()
