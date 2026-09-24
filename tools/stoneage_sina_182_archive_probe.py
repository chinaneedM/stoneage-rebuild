#!/usr/bin/env python3
"""Probe public archive indexes for Sina's historical sa1.82.exe target.

The Sina label is TARGET-B only: recovered bytes must be identified by file-level
analysis before any version claim. This probe performs metadata/index lookups
only and downloads no client payload.
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="ftp://211.90.133.5/dowload/sa/sa1.82.exe"
BASENAME="sa1.82.exe"
CDX="https://web.archive.org/cdx/search/cdx"
IA="https://archive.org/advancedsearch.php"
DISCMASTER="https://discmaster.textfiles.com/search"


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch(url,timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return int(getattr(response,"status",response.getcode())),response.geturl(),dict(response.headers),body


def cdx_url(target,wildcard=False):
    params=[
        ("url",target+("*" if wildcard else "")),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("filter","statuscode:200"),
        ("collapse","digest"),
        ("limit","200"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def parse_cdx(body):
    try:
        data=json.loads(body.decode("utf-8"))
    except Exception:
        return ()
    if not isinstance(data,list) or not data:
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))


def ia_url(term):
    params=[
        ("q",f'"{term}"'),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
        ("fl[]","mediatype"),("rows","100"),("page","1"),("output","json"),
    ]
    return IA+"?"+urllib.parse.urlencode(params)


def discmaster_url():
    params=[
        ("q",f'"{BASENAME}"'),("qfields","name"),("mode","deep"),
        ("dedup","dedup"),("limit","100"),("outputAs","json"),("showItemName","showItemName"),
    ]
    return DISCMASTER+"?"+urllib.parse.urlencode(params)


def nested_file_rows(value):
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
        key=(str(row.get("itemid","")),str(row.get("fileid","")),str(row.get("filename",row.get("name",""))))
        dedup[key]=row
    return tuple(dedup.values())


def main():
    print("StoneAge Sina-labelled 1.82 client archive probe — R1")
    print("SCOPE|TARGET-B-exact-filename+archive-indexes|metadata-only|no-client-payload")
    print(f"TARGET|url={clean(TARGET)}|basename={BASENAME}|version_claim=UNVERIFIED_UNTIL_BYTES")

    errors=0
    hits=0

    for label,target,wildcard in (
        ("exact-ftp",TARGET,False),
        ("ftp-directory",TARGET.rsplit("/",1)[0]+"/",True),
        ("host-filename","http://211.90.133.5/dowload/sa/"+BASENAME,False),
    ):
        url=cdx_url(target,wildcard=wildcard)
        try:
            status,final,headers,body=fetch(url)
            rows=parse_cdx(body)
            if label=="ftp-directory":
                rows=tuple(row for row in rows if BASENAME.lower() in str(row.get("original","")).lower())
            hits+=len(rows)
            print(
                f"CDX|label={label}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}"
            )
            for row in rows:
                print(
                    f"CDX_HIT|label={label}|timestamp={clean(row.get('timestamp'))}|"
                    f"original={clean(row.get('original'))}|mimetype={clean(row.get('mimetype'))}|"
                    f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
                )
        except Exception as exc:
            errors+=1
            print(f"ERROR|scope=cdx:{label}|kind={type(exc).__name__}|message={clean(exc)}")

    url=ia_url(BASENAME)
    try:
        status,final,headers,body=fetch(url)
        data=json.loads(body.decode("utf-8"))
        docs=data.get("response",{}).get("docs",[])
        hits+=len(docs)
        print(
            f"IA_QUERY|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"items={len(docs)}|final={clean(final)}"
        )
        for doc in docs:
            print(
                f"IA_HIT|identifier={clean(doc.get('identifier'))}|title={clean(doc.get('title'))}|"
                f"date={clean(doc.get('date'))}|mediatype={clean(doc.get('mediatype'))}"
            )
    except Exception as exc:
        errors+=1
        print(f"ERROR|scope=ia|kind={type(exc).__name__}|message={clean(exc)}")

    url=discmaster_url()
    try:
        status,final,headers,body=fetch(url)
        data=json.loads(body.decode("utf-8"))
        rows=tuple(
            row for row in nested_file_rows(data)
            if str(row.get("filename",row.get("name",""))).lower()==BASENAME.lower()
            or str(row.get("fileid","")).replace("\\","/").lower().endswith("/"+BASENAME.lower())
        )
        hits+=len(rows)
        print(
            f"DISCMASTER|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"exact_rows={len(rows)}|final={clean(final)}"
        )
        for row in rows:
            print(
                f"DISCMASTER_HIT|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|"
                f"fileid={clean(row.get('fileid'),1800)}|filename={clean(row.get('filename',row.get('name')))}|"
                f"size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}"
            )
    except Exception as exc:
        errors+=1
        print(f"ERROR|scope=discmaster|kind={type(exc).__name__}|message={clean(exc)}")

    print(f"COUNT|hits|{hits}")
    print(f"COUNT|errors|{errors}")
    if hits:
        print("RESOLUTION|SINA_182_ARCHIVE_CANDIDATES_FOUND|recover and identify bytes before any 1.82 build claim")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|tested surfaces incomplete")
    else:
        print("RESOLUTION|SINA_182_NO_INDEX_HIT|no exact indexed target on tested public surfaces")


if __name__=="__main__":
    main()
