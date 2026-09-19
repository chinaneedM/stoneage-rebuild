#!/usr/bin/env python3
"""Discover public Internet Archive Korean PC/game CD-ROM candidates from 1999-2002.

This is a corpus-discovery pass, not a StoneAge filename search. It emits only
item metadata and carrier-file metadata (ISO/BIN/IMG/etc.); no image payload is
downloaded.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"

QUERIES=[
    '"NetPower" AND mediatype:software',
    '"Net POWER" AND mediatype:software',
    '"PC Power" AND mediatype:software AND (Korea OR Korean)',
    '"Korean" AND "magazine" AND mediatype:software',
    '"Korean" AND "coverdisc" AND mediatype:software',
    '"Korea" AND "CD-ROM" AND mediatype:software AND year:[1999 TO 2002]',
    'description:("부록 CD" OR "부록CD") AND mediatype:software',
    'description:("게임 CD" OR "게임CD") AND mediatype:software AND year:[1999 TO 2002]',
    'title:"넷파워" AND mediatype:software',
    'creator:"제우미디어" AND mediatype:software',
    'title:"게임피아" AND mediatype:software',
    'title:"PC 게임 매거진" AND mediatype:software',
    'description:"로스트 미디어" AND mediatype:software',
    'description:"부록 CD 덤프" AND mediatype:software',
]
CARRIER=re.compile(r"(?i)\.(?:iso|bin|img|mdf|nrg|ccd|cue|toast|dmg)$")
KOREA=re.compile(r"(?i)(korea|korean|한국|대한민국|게임|net\s*power|pc\s*power|gamemeca)")
YEAR=re.compile(r"\b(?:1999|2000|2001|2002)\b")


def get_json(url,timeout=25):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.load(r)


def search(q):
    params=[
        ("q",q),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","description"),
        ("fl[]","date"),("fl[]","year"),("fl[]","mediatype"),
        ("fl[]","collection"),("fl[]","creator"),("fl[]","subject"),
        ("rows","100"),("page","1"),("output","json"),
    ]
    data=get_json(ADV+"?"+urllib.parse.urlencode(params),25)
    return data.get("response",{})


def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier,safe="")),25)


def clean(v,limit=700):
    if v is None:
        return ""
    if isinstance(v,list):
        v=",".join(str(x) for x in v)
    s=" ".join(str(v).split())
    return "".join(ch for ch in s if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def carrier_files(files):
    out=[]
    for f in files:
        name=str(f.get("name",""))
        if not CARRIER.search(name):
            continue
        out.append({
            "name":name,
            "size":str(f.get("size","")),
            "md5":str(f.get("md5","")),
            "sha1":str(f.get("sha1","")),
            "format":str(f.get("format","")),
            "source":str(f.get("source","")),
        })
    return out


def likely_period_korean(doc):
    blob=" ".join(clean(doc.get(k),1500) for k in ("title","description","creator","subject","collection"))
    date=clean(doc.get("date") or doc.get("year"),100)
    return bool(KOREA.search(blob)) and (bool(YEAR.search(date+" "+blob)) or not date)


def main():
    print("StoneAge Korean historical CD corpus discovery — R1")
    print("SCOPE|internet-archive-item-and-filelist-metadata-only|no-image-payload-download")
    docs={}
    errors=[]
    for idx,q in enumerate(QUERIES,1):
        try:
            response=search(q)
        except Exception as exc:
            errors.append(("search",str(idx),type(exc).__name__,str(exc)))
            continue
        rows=response.get("docs",[])
        print(f"QUERY|n={idx}|numFound={response.get('numFound',0)}|returned={len(rows)}|q={clean(q)}")
        for doc in rows:
            ident=str(doc.get("identifier","")).strip()
            if ident:
                docs.setdefault(ident,doc)

    selected={ident:doc for ident,doc in docs.items() if likely_period_korean(doc)}
    print(f"COUNT|unique_items|{len(docs)}")
    print(f"COUNT|selected_metadata_candidates|{len(selected)}")

    def one(ident):
        try:
            return ident,metadata(ident),None
        except Exception as exc:
            return ident,None,(type(exc).__name__,str(exc))

    metas={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for ident,data,error in ex.map(one,sorted(selected)):
            if error:
                errors.append(("metadata",ident,error[0],error[1]))
            else:
                metas[ident]=data

    candidates=[]
    for ident,data in metas.items():
        carriers=carrier_files(data.get("files",[]))
        if carriers:
            candidates.append((ident,selected[ident],carriers))

    print(f"COUNT|metadata_fetched|{len(metas)}")
    print(f"COUNT|carrier_items|{len(candidates)}")
    print(f"COUNT|errors|{len(errors)}")
    for phase,key,kind,msg in errors:
        print(f"ERROR|phase={clean(phase)}|key={clean(key)}|kind={clean(kind)}|message={clean(msg)}")

    for ident,doc,carriers in sorted(candidates,key=lambda x:x[0].lower()):
        print(
            "ITEM|"
            f"identifier={clean(ident)}|title={clean(doc.get('title'))}|date={clean(doc.get('date') or doc.get('year'))}|"
            f"creator={clean(doc.get('creator'))}|collection={clean(doc.get('collection'))}|"
            f"description={clean(doc.get('description'),900)}"
        )
        for f in sorted(carriers,key=lambda x:x["name"].lower()):
            print(
                "CARRIER|"
                f"identifier={clean(ident)}|name={clean(f['name'])}|size={clean(f['size'])}|"
                f"md5={clean(f['md5'])}|sha1={clean(f['sha1'])}|format={clean(f['format'])}|source={clean(f['source'])}"
            )


if __name__=="__main__":
    main()
