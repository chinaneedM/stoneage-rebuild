#!/usr/bin/env python3
"""Fetch metadata/file-list only for Internet Archive item Stoneage-5."""
from __future__ import annotations
import json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
IDENTIFIER="Stoneage-5"
URL="https://archive.org/metadata/"+urllib.parse.quote(IDENTIFIER,safe="")
EXTS=(".iso",".bin",".cue",".img",".ccd",".nrg",".mdf",".mds")

def clean(v,n=1600):
    if isinstance(v,list): v=",".join(str(x) for x in v)
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def main():
    print("StoneAge Stoneage-5 IA metadata probe — R1")
    print("SCOPE|single-item-metadata+filelist-only|no-payload-download")
    req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=30) as r:
        data=json.load(r)
    md=data.get("metadata",{})
    print(
        f"ITEM|identifier={clean(md.get('identifier') or IDENTIFIER)}|title={clean(md.get('title'))}|"
        f"date={clean(md.get('date') or md.get('year'))}|creator={clean(md.get('creator'))}|"
        f"uploader={clean(md.get('uploader'))}|collection={clean(md.get('collection'))}|"
        f"mediatype={clean(md.get('mediatype'))}|description={clean(md.get('description'),2400)}"
    )
    rows=[]
    for f in data.get("files",[]):
        name=str(f.get("name") or "")
        if name.lower().endswith(EXTS):
            rows.append(f)
    print(f"COUNT|optical_files|{len(rows)}")
    for f in rows:
        print(
            f"OPTICAL|name={clean(f.get('name'),2200)}|size={clean(f.get('size'))}|"
            f"md5={clean(f.get('md5'))}|sha1={clean(f.get('sha1'))}|crc32={clean(f.get('crc32'))}|"
            f"source={clean(f.get('source'))}|format={clean(f.get('format'))}"
        )
    print("EVIDENCE_BOUNDARY|catalogue fields are IA metadata; file hashes describe preserved objects and do not alone establish original release date, pressing, version or clean-client provenance.")

if __name__=="__main__":
    main()
