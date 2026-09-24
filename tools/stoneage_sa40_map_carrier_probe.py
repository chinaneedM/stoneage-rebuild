#!/usr/bin/env python3
"""Probe public preservation indexes for the dated StoneAge 4.0 full-map ZIP.

The contemporaneous Sina page exposes the exact source-derived basename
shiqi4updatex_02_11_08.zip. This probe searches DiscMaster's file-level index
and Internet Archive item metadata/search surfaces for that filename or its
source-derived stem. Metadata only; no candidate payload is downloaded.
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
BASENAME="shiqi4updatex_02_11_08.zip"
STEM="shiqi4updatex_02_11_08"
DISCM="https://discmaster.textfiles.com/search"
IA_SEARCH="https://archive.org/advancedsearch.php"

def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

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

def discmaster_url(query):
    params=[
        ("q",query),("qfields","name"),("mode","deep"),("limit","200"),
        ("outputAs","json"),("showItemName","showItemName"),
    ]
    return DISCM+"?"+urllib.parse.urlencode(params)

def discmaster_rows(value):
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

def exact_or_stem_hits(rows):
    exact=[]
    stem=[]
    for row in rows:
        path=row_path(row).replace("\\","/")
        leaf=path.rsplit("/",1)[-1].lower()
        if leaf==BASENAME.lower():
            exact.append(row)
        elif STEM.lower() in leaf:
            stem.append(row)
    return tuple(exact),tuple(stem)

def ia_url(query):
    params=[
        ("q",query),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
        ("fl[]","description"),("fl[]","collection"),
        ("rows","100"),("page","1"),("output","json"),
    ]
    return IA_SEARCH+"?"+urllib.parse.urlencode(params)

def ia_docs(value):
    response=value.get("response",{}) if isinstance(value,dict) else {}
    docs=response.get("docs",[]) if isinstance(response,dict) else []
    return tuple(row for row in docs if isinstance(row,dict))

def main():
    print("StoneAge 4.0 full-map patch preservation-carrier probe — R1")
    print("SCOPE|exact-source-basename+stem|DiscMaster-file-index+InternetArchive-item-search|metadata-only|no-payload")
    print(f"TARGET|basename={BASENAME}|stem={STEM}|published_date=20021108")

    errors=[]
    exact_total=0
    stem_total=0
    ia_total=0

    for label,query in (("exact",f'"{BASENAME}"'),("stem",f'"{STEM}"')):
        try:
            url=discmaster_url(query)
            status,final,body,data=fetch_json(url)
            rows=discmaster_rows(data)
            exact,stem=exact_or_stem_hits(rows)
            exact_total+=len(exact)
            stem_total+=len(stem)
            print(
                f"DISCM_QUERY|label={label}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|"
                f"exact_hits={len(exact)}|stem_hits={len(stem)}|final={clean(final)}"
            )
            for kind,subset in (("exact",exact),("stem",stem)):
                for row in subset:
                    print(
                        f"DISCM_HIT|kind={kind}|itemid={clean(row.get('itemid'))}|"
                        f"itemName={clean(row.get('itemName'))}|path={clean(row_path(row))}|"
                        f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|"
                        f"b3sum={clean(row.get('b3sum'))}"
                    )
        except Exception as exc:
            errors.append((f"discmaster:{label}",type(exc).__name__,str(exc)))

    ia_queries=(
        ("exact-filename",f'"{BASENAME}"'),
        ("stem",f'"{STEM}"'),
        ("stoneage-stem",f'stoneage AND "{STEM}"'),
    )
    for label,query in ia_queries:
        try:
            url=ia_url(query)
            status,final,body,data=fetch_json(url)
            docs=ia_docs(data)
            ia_total+=len(docs)
            print(
                f"IA_QUERY|label={label}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|items={len(docs)}|final={clean(final)}"
            )
            for row in docs[:100]:
                print(
                    f"IA_HIT|label={label}|identifier={clean(row.get('identifier'))}|"
                    f"title={clean(row.get('title'))}|date={clean(row.get('date'))}|"
                    f"collection={clean(row.get('collection'))}|description={clean(row.get('description'))}"
                )
        except Exception as exc:
            errors.append((f"ia:{label}",type(exc).__name__,str(exc)))

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|discm_exact_hits|{exact_total}")
    print(f"COUNT|discm_stem_hits|{stem_total}")
    print(f"COUNT|ia_items|{ia_total}")
    print(f"COUNT|errors|{len(errors)}")

    if exact_total:
        print("RESOLUTION|EXACT_FILENAME_CARRIER_FOUND|inspect carrier provenance and recover candidate transiently before comparison")
    elif stem_total or ia_total:
        print("RESOLUTION|RELATED_CARRIER_CANDIDATES_FOUND|verify filename identity before any payload recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|one or more preservation-index surfaces unavailable")
    else:
        print("RESOLUTION|NO_CARRIER_HIT|tested preservation indexes contain no exact/stem carrier")

if __name__=="__main__":
    main()
