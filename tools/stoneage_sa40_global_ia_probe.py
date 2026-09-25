#!/usr/bin/env python3
"""Global Internet Archive metadata search for StoneAge 4.0 physical/client carriers.

Uses contemporaneously grounded product names (新九大家族, 新满意足, 新高采烈)
plus bounded identifier/version variants. Metadata and file-list only.
"""
from __future__ import annotations
import json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"
QUERIES=(
  'title:("石器时代4.0" OR "石器时代 4.0" OR "StoneAge 4.0" OR "Stone Age 4.0")',
  '"新九大家族"',
  '"新9大家族"',
  '"新满意足"',
  '"新滿意足"',
  '"新高采烈"',
  'identifier:(Stoneage4* OR Stoneage-4* OR StoneAge4* OR STA4*)',
)
OPT=(".iso",".bin",".cue",".img",".ccd",".nrg",".mdf",".mds")

def clean(v,n=2600):
    if isinstance(v,list):v=",".join(map(str,v))
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def get(url,timeout=40):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def search(q,page=1):
    params=[("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","creator"),("fl[]","date"),
      ("fl[]","year"),("fl[]","description"),("fl[]","mediatype"),("rows","200"),("page",str(page)),("output","json")]
    u=ADV+"?"+urllib.parse.urlencode(params);o=get(u);r=o.get("response",{})
    return u,int(r.get("numFound") or 0),r.get("docs",[])

def main():
    print("StoneAge 4.0 global IA physical-carrier search — R1")
    print("SCOPE|product-names+version-identifiers+all-IA-metadata+optical-filelists|no-payload")
    errors=[];docs={}
    for q in QUERIES:
        try:
            u,n,rows=search(q)
            print(f"QUERY|q={clean(q)}|total={n}|rows={len(rows)}|url={clean(u)}")
            for d in rows:
                ident=str(d.get("identifier") or "")
                if ident:docs[ident]=d
        except Exception as exc:errors.append(("search:"+q,type(exc).__name__,str(exc)))
    print(f"COUNT|unique_docs|{len(docs)}")
    optical_items=0
    for ident,d in sorted(docs.items()):
        try:
            o=get(META.format(urllib.parse.quote(ident,safe="")));md=o.get("metadata",{})
            opts=[r for r in o.get("files",[]) if str(r.get("name") or "").lower().endswith(OPT)]
            print(
              f"ITEM|identifier={clean(ident)}|title={clean(md.get('title') or d.get('title'))}|"
              f"creator={clean(md.get('creator') or d.get('creator'))}|date={clean(md.get('date') or md.get('year') or d.get('date'))}|"
              f"optical_files={len(opts)}|description={clean(md.get('description') or d.get('description'))}"
            )
            if opts:optical_items+=1
            for r in opts:
                print(f"OPTICAL|identifier={clean(ident)}|name={clean(r.get('name'))}|size={clean(r.get('size'))}|md5={clean(r.get('md5'))}|sha1={clean(r.get('sha1'))}|crc32={clean(r.get('crc32'))}|format={clean(r.get('format'))}")
        except Exception as exc:errors.append(("meta:"+ident,type(exc).__name__,str(exc)))
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|optical_items|{optical_items}");print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|"+("GLOBAL_IA_OPTICAL_CANDIDATE_FOUND|classify candidate before bounded filesystem probe" if optical_items else "NO_GLOBAL_IA_OPTICAL_CANDIDATE|tested product/version names expose no optical carrier"))
    print("EVIDENCE_BOUNDARY|IA catalogue metadata is discovery evidence; title/date/creator fields do not establish pressing or historical release provenance.")
if __name__=="__main__":main()
