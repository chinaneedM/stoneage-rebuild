#!/usr/bin/env python3
"""Probe preservation carriers for the contemporaneously distributed StoneAge 2.5 client.

A 2002 Sina report states that the full 2.5 upgrade/client and the 8.25 MB
upgrade were distributed both from Waei and on a list of January/February 2002
magazine/book cover discs. This probe searches public preservation indexes for
the version/title terms and named periodical carriers. Metadata only.
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
DISCM="https://discmaster.textfiles.com/search"
IA="https://archive.org/advancedsearch.php"

DISCM_QUERIES=(
    ("stoneage25-name",'"stoneage2.5"',"name"),
    ("stoneage25-alt-name",'"stoneage25"',"name"),
    ("stoneage25-content",'"stoneage 2.5"',"t"),
    ("cn-version-content",'"石器时代2.5"',"t"),
    ("spirit-king-content",'"精灵王传说"',"t"),
    ("stoneage-2002-content","StoneAge","t"),
)

IA_QUERIES=(
    ("stoneage25",'"StoneAge 2.5"'),
    ("cn-version",'"石器时代2.5"'),
    ("spirit-king",'"精灵王传说"'),
    ("popular-software-2002",'"大众软件" AND year:2002'),
    ("computer-fan-2002",'"电脑爱好者" AND year:2002'),
    ("chip-cn-2002",'"CHIP新电脑" AND year:2002'),
    ("pc-free-2002",'"PC任我行" AND year:2002'),
    ("computer-world-2002",'"家庭电脑世界" AND year:2002'),
)

def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch_json(url,timeout=45):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return (
            int(getattr(response,"status",response.getcode())),
            response.geturl(),
            body,
            json.loads(body.decode("utf-8")),
        )

def discmaster_url(query,field):
    params=[
        ("q",query),("qfields",field),("mode","deep"),("dedup","dedup"),
        ("limit","200"),("outputAs","json"),("showItemName","showItemName"),
        ("tsMin","2000"),("tsMax","2003"),
    ]
    return DISCM+"?"+urllib.parse.urlencode(params)

def discmaster_rows(value):
    rows=[]
    def walk(node):
        if isinstance(node,dict):
            if (
                ("itemid" in node or "itemName" in node)
                and ("fileid" in node or "filename" in node or "href" in node)
            ):
                rows.append(node)
            for child in node.values():
                walk(child)
        elif isinstance(node,list):
            for child in node:
                walk(child)
    walk(value)
    seen=set()
    out=[]
    for row in rows:
        key=(
            str(row.get("itemid","")),
            str(row.get("fileid","")),
            str(row.get("href","")),
        )
        if key not in seen:
            seen.add(key)
            out.append(row)
    return tuple(out)

def ia_url(query):
    params=[
        ("q",query),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
        ("fl[]","year"),("fl[]","description"),("fl[]","collection"),
        ("rows","100"),("page","1"),("output","json"),
    ]
    return IA+"?"+urllib.parse.urlencode(params)

def ia_docs(value):
    response=value.get("response",{}) if isinstance(value,dict) else {}
    docs=response.get("docs",[]) if isinstance(response,dict) else []
    return tuple(row for row in docs if isinstance(row,dict))

def likely_stoneage(row):
    blob=" ".join(
        str(row.get(k) or "")
        for k in ("itemName","fileid","filename","href","text","title")
    ).lower()
    markers=("stoneage","stone age","石器时代","精灵王")
    return any(marker.lower() in blob for marker in markers)

def main():
    print("StoneAge 2.5 contemporaneous distribution carrier probe — R1")
    print("SCOPE|2002-Waei-full-client+upgrade+named-cover-disc-carriers|DiscMaster+InternetArchive|metadata-only|no-payload")
    print("SOURCE_ANCHOR|retail_date=2002-01-20|server_upgrade_start=2002-02-04|full_upgrade=575MB-Sina/580MB-17173|delta_upgrade=8.25MB")
    print("CARRIER_PERIOD|2002-01-to-2002-02|magazine-and-guide-cover-discs")

    errors=[]
    disc_candidates=[]
    ia_candidates=[]

    for label,query,field in DISCM_QUERIES:
        try:
            url=discmaster_url(query,field)
            status,final,body,data=fetch_json(url)
            rows=discmaster_rows(data)
            relevant=[row for row in rows if likely_stoneage(row)]
            disc_candidates.extend(relevant)
            print(
                f"DISCM_QUERY|label={label}|field={field}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|"
                f"stoneage_candidates={len(relevant)}|final={clean(final)}"
            )
            for row in relevant[:100]:
                print(
                    f"DISCM_HIT|label={label}|itemid={clean(row.get('itemid'))}|"
                    f"itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|"
                    f"filename={clean(row.get('filename'))}|family={clean(row.get('family'))}|"
                    f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|"
                    f"href={clean(row.get('href'))}|b3sum={clean(row.get('b3sum'))}"
                )
        except Exception as exc:
            errors.append((f"discmaster:{label}",type(exc).__name__,str(exc)))

    for label,query in IA_QUERIES:
        try:
            url=ia_url(query)
            status,final,body,data=fetch_json(url)
            docs=ia_docs(data)
            ia_candidates.extend(docs)
            print(
                f"IA_QUERY|label={label}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|items={len(docs)}|final={clean(final)}"
            )
            for row in docs[:100]:
                print(
                    f"IA_HIT|label={label}|identifier={clean(row.get('identifier'))}|"
                    f"title={clean(row.get('title'))}|date={clean(row.get('date'))}|"
                    f"year={clean(row.get('year'))}|collection={clean(row.get('collection'))}|"
                    f"description={clean(row.get('description'))}"
                )
        except Exception as exc:
            errors.append((f"ia:{label}",type(exc).__name__,str(exc)))

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    disc_keys={
        (str(row.get("itemid","")),str(row.get("fileid","")))
        for row in disc_candidates
    }
    ia_keys={str(row.get("identifier","")) for row in ia_candidates if row.get("identifier")}
    print(f"COUNT|discm_unique_candidates|{len(disc_keys)}")
    print(f"COUNT|ia_unique_items|{len(ia_keys)}")
    print(f"COUNT|errors|{len(errors)}")
    if disc_keys:
        print("RESOLUTION|DISCM_STONEAGE_CARRIER_CANDIDATES_FOUND|inspect item provenance and file tree before payload recovery")
    elif ia_keys:
        print("RESOLUTION|IA_CARRIER_CANDIDATES_FOUND|inspect item metadata/files before payload recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|one or more carrier indexes unavailable")
    else:
        print("RESOLUTION|NO_INDEXED_CARRIER_HIT|tested preservation indexes expose no candidate")

if __name__=="__main__":
    main()
