#!/usr/bin/env python3
"""Scan Internet Archive item metadata/file lists for early Korean StoneAge payload traits.

No item payload is downloaded. Candidate items are found by metadata search; only
file-list metadata is inspected for recovered filenames and 200–300 MiB-scale files.
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

QUERIES=[
    '"스톤에이지" AND mediatype:software',
    '"StoneAge" AND mediatype:software',
    'title:(stoneage OR "stone age") AND mediatype:software',
    'description:(stoneage OR "stone age") AND mediatype:software',
]
EXACT_NAMES={"sa.exe","sa_demo.exe","stoneage.zip","stoneagebeta.zip"}
INTEREST_NAME=re.compile(r"(?i)(?:^|[/\\])(?:sa(?:_demo)?\.exe|stoneage(?:beta)?\.zip)$")
LOW=180*1024*1024
HIGH=320*1024*1024

def get_json(url,timeout=20):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def search(q):
    params=[
      ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","description"),
      ("fl[]","date"),("fl[]","year"),("fl[]","mediatype"),("fl[]","collection"),
      ("fl[]","creator"),("rows","100"),("page","1"),("output","json")
    ]
    data=get_json(ADV+"?"+urllib.parse.urlencode(params),timeout=20)
    return data.get("response",{}).get("docs",[])

def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier,safe="")),timeout=20)

def clean(v,limit=700):
    if v is None:return ""
    if isinstance(v,list):v=",".join(str(x) for x in v)
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def size_int(v):
    try:return int(v)
    except (TypeError,ValueError):return 0

def candidate_files(files):
    out=[]
    for f in files:
        name=str(f.get("name",""))
        size=size_int(f.get("size"))
        exact=bool(INTEREST_NAME.search(name.replace("\\","/")))
        size_match=LOW <= size <= HIGH
        if exact or size_match:
            out.append({
              "name":name,"size":size,"md5":str(f.get("md5","")),
              "sha1":str(f.get("sha1","")),"source":str(f.get("source","")),
              "format":str(f.get("format","")),"exact":exact,"size_match":size_match,
            })
    return out

def main():
    print("StoneAge Internet Archive candidate-file metadata scan — R1")
    print("SCOPE|item-and-filelist-metadata-only|no-payload-download")
    print("TRAITS|exact=sa.exe,sa_demo.exe,stoneage.zip,stoneagebeta.zip|size_window=180-320MiB")

    docs={}; errors=[]
    for idx,q in enumerate(QUERIES,1):
        try:rows=search(q)
        except Exception as exc:
            errors.append(("search",str(idx),type(exc).__name__,str(exc))); continue
        print(f"QUERY|n={idx}|results={len(rows)}|q={clean(q)}")
        for d in rows:
            ident=str(d.get("identifier","")).strip()
            if ident:docs.setdefault(ident,d)

    print(f"COUNT|unique_items|{len(docs)}")

    def one(ident):
        try:return ident,metadata(ident),None
        except Exception as exc:return ident,None,(type(exc).__name__,str(exc))

    metas={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for ident,data,error in ex.map(one,sorted(docs)):
            if error:errors.append(("metadata",ident,error[0],error[1]))
            else:metas[ident]=data

    matches=[]
    for ident,data in metas.items():
        files=candidate_files(data.get("files",[]))
        if not files:continue
        doc=docs[ident]
        for f in files:matches.append((ident,doc,f))

    print(f"COUNT|metadata_fetched|{len(metas)}")
    print(f"COUNT|errors|{len(errors)}")
    exact_count=sum(1 for _,_,f in matches if f["exact"])
    size_only_count=sum(1 for _,_,f in matches if f["size_match"] and not f["exact"])
    print(f"COUNT|candidate_files|{len(matches)}")
    print(f"COUNT|exact_name_matches|{exact_count}")
    print(f"COUNT|size_only_candidates|{size_only_count}")
    for phase,key,kind,msg in errors:
        print(f"ERROR|phase={clean(phase)}|key={clean(key)}|kind={clean(kind)}|message={clean(msg)}")
    for ident,doc,f in sorted(matches,key=lambda x:(x[0].lower(),x[2]["name"].lower())):
        print(
          "CANDIDATE|"
          f"identifier={clean(ident)}|title={clean(doc.get('title'))}|date={clean(doc.get('date') or doc.get('year'))}|"
          f"creator={clean(doc.get('creator'))}|collection={clean(doc.get('collection'))}|"
          f"name={clean(f['name'])}|size={f['size']}|exact_name={int(f['exact'])}|size_match={int(f['size_match'])}|"
          f"md5={clean(f['md5'])}|sha1={clean(f['sha1'])}|source={clean(f['source'])}|format={clean(f['format'])}"
        )

if __name__=="__main__":main()
