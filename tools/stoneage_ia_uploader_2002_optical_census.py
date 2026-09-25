#!/usr/bin/env python3
"""Enumerate every optical item from Stoneage-5 uploader in the 4.0/5.0 era.

This intentionally ignores StoneAge text relevance. It is designed to catch
generic item titles whose BIN/CUE filenames or volume labels may expose a hidden
STA4/SA4 carrier. Metadata/file-list only.
"""
from __future__ import annotations
import json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"
UPLOADER="994467746@qq.com"
OPTICAL_EXTS=(".iso",".bin",".cue",".img",".ccd",".nrg",".mdf",".mds")

def clean(v,n=2200):
    if isinstance(v,list): v=",".join(str(x) for x in v)
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def get_json(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def search():
    q=f'uploader:"{UPLOADER}" AND date:[2002-01-01 TO 2003-03-01]'
    params=[
      ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","creator"),
      ("fl[]","date"),("fl[]","year"),("fl[]","description"),("fl[]","collection"),
      ("fl[]","mediatype"),("rows","200"),("page","1"),("output","json"),
    ]
    u=ADV+"?"+urllib.parse.urlencode(params)
    o=get_json(u);r=o.get("response",{})
    return u,int(r.get("numFound") or 0),r.get("docs",[])

def optical(files):
    return [x for x in files or [] if str(x.get("name") or "").lower().endswith(OPTICAL_EXTS)]

def main():
    print("StoneAge IA uploader 2002-era optical census — R1")
    print("SCOPE|uploader+2002-to-2003Q1-date-range+all-optical-filelists|no-text-relevance-filter|no-payload")
    errors=[]
    try:
        u,total,docs=search()
        print(f"SEARCH|total={total}|rows={len(docs)}|url={clean(u)}")
    except Exception as exc:
        print(f"ERROR|scope=search|kind={type(exc).__name__}|message={clean(exc)}")
        return
    optical_items=0
    for d in docs:
        ident=str(d.get("identifier") or "")
        if not ident: continue
        try:
            o=get_json(META.format(urllib.parse.quote(ident,safe="")))
            md=o.get("metadata",{})
            rows=optical(o.get("files",[]))
            if not rows:
                continue
            optical_items+=1
            print(
                f"ITEM|identifier={clean(ident)}|title={clean(md.get('title') or d.get('title'))}|"
                f"creator={clean(md.get('creator') or d.get('creator'))}|"
                f"date={clean(md.get('date') or md.get('year') or d.get('date') or d.get('year'))}|"
                f"description={clean(md.get('description') or d.get('description'))}|optical_files={len(rows)}"
            )
            for r in rows:
                print(
                    f"OPTICAL|identifier={clean(ident)}|name={clean(r.get('name'))}|size={clean(r.get('size'))}|"
                    f"md5={clean(r.get('md5'))}|sha1={clean(r.get('sha1'))}|crc32={clean(r.get('crc32'))}|format={clean(r.get('format'))}"
                )
        except Exception as exc:
            errors.append((ident,type(exc).__name__,str(exc)))
    for ident,kind,msg in errors:
        print(f"ERROR|scope=metadata|identifier={clean(ident)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|date_range_docs|{len(docs)}")
    print(f"COUNT|optical_items|{optical_items}")
    print(f"COUNT|errors|{len(errors)}")
    print("EVIDENCE_BOUNDARY|IA date/title/creator fields are catalogue metadata. This census discovers candidate carriers only and does not establish original release or pressing identity.")

if __name__=="__main__":main()
