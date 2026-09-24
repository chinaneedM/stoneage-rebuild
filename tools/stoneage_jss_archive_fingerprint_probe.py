#!/usr/bin/env python3
"""High-precision Internet Archive metadata scan for original JSS StoneAge artifacts.

The scan is metadata-only. It searches item metadata and inspects Archive file lists;
it never downloads candidate payloads. The target fingerprint comes from the
hash-pinned archived JSS SaUpdate object already recovered by this project.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"

KNOWN_SIZE=217088
KNOWN_MD5="8a5dc8b64f57574ffdd139a762a41aaa"
KNOWN_SHA1="43d4f038aca05d055b0f59cac26fd7fae4dbc099"
KNOWN_SHA256="6795d9349168f77aa025d7c4ea05d005c5bbfe33dd4b227eb7731802fa7eb82b"

QUERIES=(
    '"SaUpdate.exe"',
    '"SaUpdate.EXE"',
    '"stoneage.exe" AND "StoneAge"',
    '"update.gamersdream.ne.jp"',
    '"/~stoneage/newest.txt"',
    '"newest.txt" AND "StoneAge"',
    '"日本システムサプライ" AND "StoneAge"',
    '"Japan System Supply" AND "StoneAge"',
    '"STONEAGE 起動プログラム"',
    f'"{KNOWN_MD5}"',
    f'"{KNOWN_SHA1}"',
    f'"{KNOWN_SHA256}"',
    '"StoneAge" AND mediatype:software',
    'title:(stoneage OR "stone age") AND mediatype:software',
)

RESOURCE_NAME_RE=re.compile(
    r"(?i)(?:^|[/\\])(?:"
    r"saupdate\.exe|stoneage\.exe|newest\.txt|sa_\d+\.exe|"
    r"(?:real|adrn|spr|spradrn|sound|battle)_\d+\.bin|"
    r"(?:soundaddr|battletxt)_\d+\.txt"
    r")$"
)


def clean(value,limit=900):
    if value is None:
        return ""
    if isinstance(value,list):
        value=",".join(str(x) for x in value)
    text=" ".join(str(value).split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def get_json(url,timeout=20):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return json.load(response)


def search(query):
    params=[
        ("q",query),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","description"),
        ("fl[]","date"),("fl[]","year"),("fl[]","mediatype"),
        ("fl[]","collection"),("fl[]","creator"),
        ("rows","150"),("page","1"),("output","json"),
    ]
    data=get_json(ADV+"?"+urllib.parse.urlencode(params),timeout=20)
    return data.get("response",{}).get("docs",[])


def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier,safe="")),timeout=20)


def size_int(value):
    try:
        return int(value)
    except (TypeError,ValueError):
        return 0


def file_fingerprint(row):
    name=str(row.get("name",""))
    size=size_int(row.get("size"))
    md5=str(row.get("md5","")).lower()
    sha1=str(row.get("sha1","")).lower()
    basename=name.replace("\\","/").rsplit("/",1)[-1].lower()
    return {
        "name":name,
        "basename":basename,
        "size":size,
        "md5":md5,
        "sha1":sha1,
        "format":str(row.get("format","")),
        "source":str(row.get("source","")),
        "known_md5":md5==KNOWN_MD5,
        "known_sha1":sha1==KNOWN_SHA1,
        "known_size":size==KNOWN_SIZE,
        "resource_name":bool(RESOURCE_NAME_RE.search(name.replace("\\","/"))),
    }


def candidate_files(files):
    out=[]
    for row in files:
        fp=file_fingerprint(row)
        if fp["known_md5"] or fp["known_sha1"] or fp["known_size"] or fp["resource_name"]:
            out.append(fp)
    return out


def strength(fp):
    if fp["known_md5"] or fp["known_sha1"]:
        return "HASH"
    if fp["known_size"] and fp["basename"] in {"saupdate.exe","stoneage.exe"}:
        return "NAME_SIZE"
    if fp["basename"]=="newest.txt":
        return "MANIFEST_NAME"
    if fp["resource_name"]:
        return "JSS_RESOURCE_NAME"
    if fp["known_size"]:
        return "SIZE_ONLY"
    return "OTHER"


def main():
    print("StoneAge JSS Internet Archive fingerprint scan — R1")
    print("SCOPE|item+filelist-metadata-only|no-payload-download")
    print(
        f"FINGERPRINT|size={KNOWN_SIZE}|md5={KNOWN_MD5}|sha1={KNOWN_SHA1}|"
        f"sha256={KNOWN_SHA256}|names=SaUpdate.exe,stoneage.exe,newest.txt,numbered-resource-families"
    )

    docs={}
    query_hits={}
    errors=[]

    def search_one(job):
        number,query=job
        try:
            return number,query,search(query),None
        except Exception as exc:
            return number,query,[],(type(exc).__name__,str(exc))

    search_jobs=list(enumerate(QUERIES,1))
    search_results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for result in ex.map(search_one,search_jobs):
            search_results.append(result)

    for number,query,rows,error in sorted(search_results,key=lambda x:x[0]):
        if error:
            errors.append(("search",str(number),error[0],error[1]))
            print(f"QUERY|n={number}|results=ERROR|q={clean(query)}")
            continue
        print(f"QUERY|n={number}|results={len(rows)}|q={clean(query)}")
        for doc in rows:
            ident=str(doc.get("identifier","")).strip()
            if not ident:
                continue
            docs.setdefault(ident,doc)
            query_hits.setdefault(ident,set()).add(number)

    def fetch_one(ident):
        try:
            return ident,metadata(ident),None
        except Exception as exc:
            return ident,None,(type(exc).__name__,str(exc))

    metas={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for ident,data,error in ex.map(fetch_one,sorted(docs)):
            if error:
                errors.append(("metadata",ident,error[0],error[1]))
            else:
                metas[ident]=data

    matches=[]
    for ident,data in metas.items():
        for fp in candidate_files(data.get("files",[])):
            matches.append((ident,docs[ident],fp))

    print(f"COUNT|queries={len(QUERIES)}")
    print(f"COUNT|unique_items={len(docs)}")
    print(f"COUNT|metadata_fetched={len(metas)}")
    print(f"COUNT|errors={len(errors)}")
    print(f"COUNT|candidate_files={len(matches)}")
    print(f"COUNT|hash_matches={sum(1 for _,_,x in matches if x['known_md5'] or x['known_sha1'])}")
    print(f"COUNT|exact_size_matches={sum(1 for _,_,x in matches if x['known_size'])}")
    print(f"COUNT|resource_name_matches={sum(1 for _,_,x in matches if x['resource_name'])}")
    print(f"COUNT|manifest_name_matches={sum(1 for _,_,x in matches if x['basename']=='newest.txt')}")

    # Only emit item-level metadata for hits from the JSS-specific query surface
    # (the first 12 queries), or items that contain a candidate file.
    candidate_ids={ident for ident,_,_ in matches}
    for ident,doc in sorted(docs.items()):
        hitset=sorted(query_hits.get(ident,set()))
        if not (any(n<=12 for n in hitset) or ident in candidate_ids):
            continue
        print(
            "ITEM|"
            f"identifier={clean(ident)}|queries={','.join(str(n) for n in hitset)}|"
            f"title={clean(doc.get('title'))}|date={clean(doc.get('date') or doc.get('year'))}|"
            f"creator={clean(doc.get('creator'))}|mediatype={clean(doc.get('mediatype'))}|"
            f"collection={clean(doc.get('collection'))}|description={clean(doc.get('description'))}"
        )

    for ident,doc,fp in sorted(matches,key=lambda x:(strength(x[2]),x[0].lower(),x[2]["name"].lower())):
        print(
            "CANDIDATE|"
            f"strength={strength(fp)}|identifier={clean(ident)}|queries={','.join(str(n) for n in sorted(query_hits.get(ident,set())))}|"
            f"title={clean(doc.get('title'))}|date={clean(doc.get('date') or doc.get('year'))}|"
            f"name={clean(fp['name'])}|size={fp['size']}|known_size={int(fp['known_size'])}|"
            f"resource_name={int(fp['resource_name'])}|md5={clean(fp['md5'])}|sha1={clean(fp['sha1'])}|"
            f"known_md5={int(fp['known_md5'])}|known_sha1={int(fp['known_sha1'])}|"
            f"format={clean(fp['format'])}|source={clean(fp['source'])}"
        )

    for phase,key,kind,message in errors:
        print(
            f"ERROR|phase={clean(phase)}|key={clean(key)}|kind={clean(kind)}|message={clean(message)}"
        )

    strong=sum(
        1 for _,_,fp in matches
        if strength(fp) in {"HASH","NAME_SIZE","MANIFEST_NAME","JSS_RESOURCE_NAME"}
    )
    if strong:
        print(f"RESOLUTION|CANDIDATES_FOUND|strong_or_named={strong}|inspect provenance before any payload retrieval")
    elif errors:
        print("RESOLUTION|INCONCLUSIVE|metadata surface has errors; no strong JSS candidate in completed queries")
    else:
        print("RESOLUTION|BOUNDED_NO_JSS_CANDIDATE|no hash/name/manifest/resource-family candidate in completed IA metadata surface")


if __name__=="__main__":
    main()
