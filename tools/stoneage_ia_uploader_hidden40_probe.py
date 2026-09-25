#!/usr/bin/env python3
"""Second-pass scan of the known Stoneage-5 uploader's entire IA catalogue.

R3 intentionally filtered the uploader's 741 items by obvious StoneAge title/
description text. This pass looks for less-obvious 4.0 package names, abbreviations
and optical filenames before deciding whether a candidate deserves a bounded
filesystem probe. Metadata/file-list only.
"""
from __future__ import annotations
import json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"
UPLOADER="994467746@qq.com"
TERMS=(
    "石器","stoneage","stone age","waei","华义","華義",
    "新九大家族","九大家族","新高采烈","新满意足","新滿意足",
    "sta4","sta 4","sa4","sa 4","4.0",
)
OPTICAL_EXTS=(".iso",".bin",".cue",".img",".ccd",".nrg",".mdf",".mds")

def clean(v,n=2200):
    if isinstance(v,list): v=",".join(str(x) for x in v)
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def get_json(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r: return json.load(r)

def search_page(page,rows=200):
    params=[
        ("q",f'uploader:"{UPLOADER}"'),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","creator"),("fl[]","date"),
        ("fl[]","year"),("fl[]","description"),("fl[]","collection"),("fl[]","mediatype"),
        ("rows",str(rows)),("page",str(page)),("output","json"),
    ]
    u=ADV+"?"+urllib.parse.urlencode(params)
    o=get_json(u); resp=o.get("response",{})
    return u,int(resp.get("numFound") or 0),resp.get("docs",[])

def norm(v):
    if isinstance(v,list): v=" ".join(map(str,v))
    return str(v or "").lower().replace("_"," ").replace("-"," ")

def hit_terms(doc):
    text=" ".join(norm(doc.get(k)) for k in ("identifier","title","creator","description"))
    return tuple(t for t in TERMS if t.lower() in text)

def optical(files):
    return [r for r in files or [] if str(r.get("name") or "").lower().endswith(OPTICAL_EXTS)]

def file_hits(files):
    out=[]
    for r in files or []:
        name=str(r.get("name") or "")
        low=name.lower().replace("_"," ").replace("-"," ")
        terms=[t for t in TERMS if t.lower() in low]
        if terms:
            out.append((r,terms))
    return out

def main():
    print("StoneAge IA uploader hidden-4.0 candidate scan — R1")
    print("SCOPE|all-uploader-items+package-keywords+optical-filenames|metadata-only|no-payload")
    docs=[]; errors=[]
    total=0
    for page in range(1,10):
        try:
            u,n,batch=search_page(page)
            if page==1: total=n
            print(f"PAGE|page={page}|rows={len(batch)}|total={n}|url={clean(u)}")
            docs.extend(batch)
            if not batch or len(docs)>=n: break
        except Exception as exc:
            errors.append((f"search:{page}",type(exc).__name__,str(exc))); break
    print(f"COUNT|catalogue_docs|{len(docs)}")
    candidates=[]
    for d in docs:
        hits=hit_terms(d)
        if hits:
            candidates.append((d,hits))
            print(
                f"DOC_HIT|identifier={clean(d.get('identifier'))}|title={clean(d.get('title'))}|"
                f"creator={clean(d.get('creator'))}|date={clean(d.get('date') or d.get('year'))}|"
                f"terms={clean(','.join(hits))}|description={clean(d.get('description'))}"
            )
    print(f"COUNT|doc_candidates|{len(candidates)}")

    meta_checked=0; optical_candidates=0; file_term_candidates=0
    for d,hits in candidates:
        ident=str(d.get("identifier") or "")
        if not ident: continue
        try:
            o=get_json(META.format(urllib.parse.quote(ident,safe="")))
            meta_checked+=1
            md=o.get("metadata",{})
            opts=optical(o.get("files",[]))
            fh=file_hits(o.get("files",[]))
            if opts or fh:
                print(
                    f"ITEM|identifier={clean(ident)}|title={clean(md.get('title'))}|"
                    f"creator={clean(md.get('creator'))}|date={clean(md.get('date') or md.get('year'))}|"
                    f"optical_files={len(opts)}|file_term_hits={len(fh)}"
                )
            if opts: optical_candidates+=1
            if fh: file_term_candidates+=1
            for r in opts:
                print(
                    f"OPTICAL|identifier={clean(ident)}|name={clean(r.get('name'))}|size={clean(r.get('size'))}|"
                    f"md5={clean(r.get('md5'))}|sha1={clean(r.get('sha1'))}|format={clean(r.get('format'))}"
                )
            for r,terms in fh[:80]:
                print(
                    f"FILE_HIT|identifier={clean(ident)}|name={clean(r.get('name'))}|size={clean(r.get('size'))}|"
                    f"md5={clean(r.get('md5'))}|sha1={clean(r.get('sha1'))}|terms={clean(','.join(terms))}"
                )
        except Exception as exc:
            errors.append((f"metadata:{ident}",type(exc).__name__,str(exc)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|metadata_checked|{meta_checked}")
    print(f"COUNT|optical_candidate_items|{optical_candidates}")
    print(f"COUNT|file_term_candidate_items|{file_term_candidates}")
    print(f"COUNT|errors|{len(errors)}")
    print("EVIDENCE_BOUNDARY|catalogue and file-list metadata are discovery evidence only; item names, uploader dates and creator labels do not establish pressing or version provenance.")

if __name__=="__main__": main()
