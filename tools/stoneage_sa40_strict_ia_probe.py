#!/usr/bin/env python3
"""Strict Internet Archive preservation search for the StoneAge 4.0 map lineage.

The previous global carrier workflow was too broad and timed out while walking
unrelated metadata. This replacement keeps only exact/period-bounded software
queries and reads file lists only for records whose metadata itself contains a
StoneAge-4.0, package-name, exact-filename, or xinhaonanhai marker.
"""
from __future__ import annotations
import json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
ADV="https://archive.org/advancedsearch.php"
META="https://archive.org/metadata/{}"
QUERIES=(
 ('exact-file','"shiqi4updatex_02_11_08.zip"'),
 ('exact-stem','"shiqi4updatex_02_11_08"'),
 ('title-40','title:("石器时代4.0" OR "石器时代 4.0" OR "StoneAge 4.0" OR "Stone Age 4.0") AND mediatype:software AND year:[2002 TO 2004]'),
 ('new-nine','"新九大家族" AND mediatype:software AND year:[2002 TO 2004]'),
 ('satisfied','("新满意足" OR "新滿意足") AND mediatype:software AND year:[2002 TO 2004]'),
 ('happy','"新高采烈" AND mediatype:software AND year:[2002 TO 2004]'),
 ('contributor','"xinhaonanhai" AND mediatype:software AND year:[2001 TO 2004]'),
)
MARKERS=(
 'shiqi4updatex_02_11_08','石器时代4.0','石器时代 4.0','stoneage 4.0','stone age 4.0',
 '新九大家族','新9大家族','新满意足','新滿意足','新高采烈','xinhaonanhai',
)
FILE_EXTS=(".iso",".bin",".cue",".img",".ccd",".nrg",".mdf",".mds",".zip",".exe",".rar",".cab")

def clean(v,n=3500):
    if isinstance(v,list):v=",".join(map(str,v))
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def get(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def search(q):
    p=[("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","creator"),("fl[]","date"),
       ("fl[]","year"),("fl[]","description"),("fl[]","mediatype"),("rows","100"),("page","1"),("output","json")]
    u=ADV+"?"+urllib.parse.urlencode(p);o=get(u);r=o.get("response",{})
    return u,int(r.get("numFound") or 0),r.get("docs",[])

def text_of(d):
    vals=[]
    for k in ("identifier","title","creator","description","date","year"):
        v=d.get(k)
        if isinstance(v,list):vals.extend(map(str,v))
        elif v is not None:vals.append(str(v))
    return " ".join(vals).lower()

def strict(d):
    t=text_of(d)
    return any(m.lower() in t for m in MARKERS)

def main():
    print("StoneAge 4.0 strict IA preservation search — R1")
    print("SCOPE|period-bounded exact metadata queries|strict candidate file lists only|no-payload")
    errors=[];docs={}
    for label,q in QUERIES:
        try:
            u,n,rows=search(q)
            print(f"QUERY|label={label}|total={n}|rows={len(rows)}|url={clean(u)}")
            for d in rows:
                ident=str(d.get("identifier") or "")
                if ident and strict(d):
                    docs[ident]=d
                    print(f"STRICT_META|label={label}|identifier={clean(ident)}|title={clean(d.get('title'))}|date={clean(d.get('date') or d.get('year'))}|description={clean(d.get('description'))}")
        except Exception as e:errors.append((label,type(e).__name__,str(e)))
    print(f"COUNT|strict_items|{len(docs)}")
    file_hits=0
    for ident,d in sorted(docs.items()):
        try:
            o=get(META.format(urllib.parse.quote(ident,safe="")),timeout=35)
            md=o.get("metadata",{})
            for f in o.get("files",[]):
                name=str(f.get("name") or "")
                low=name.lower()
                if not low.endswith(FILE_EXTS):continue
                relevant=any(m.lower() in low for m in MARKERS) or low.endswith((".iso",".bin",".img",".nrg",".mdf"))
                if not relevant:continue
                file_hits+=1
                print(f"FILE|identifier={clean(ident)}|title={clean(md.get('title') or d.get('title'))}|name={clean(name)}|size={clean(f.get('size'))}|md5={clean(f.get('md5'))}|sha1={clean(f.get('sha1'))}|crc32={clean(f.get('crc32'))}")
        except Exception as e:errors.append(("meta:"+ident,type(e).__name__,str(e)))
    print(f"COUNT|candidate_files|{file_hits}")
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if file_hits:
        print("RESOLUTION|STRICT_IA_FILE_CANDIDATE_FOUND|classify carrier provenance before bounded filesystem inspection")
    elif docs:
        print("RESOLUTION|STRICT_IA_METADATA_ONLY|candidate metadata exists but exposes no relevant archived file")
    elif errors:
        print("RESOLUTION|STRICT_IA_SURFACE_INCOMPLETE|retry failed exact query only")
    else:
        print("RESOLUTION|NO_STRICT_IA_CANDIDATE|bounded 2002-2004 software metadata surface has no matching preservation item")
    print("EVIDENCE_BOUNDARY|IA metadata/file-list search is discovery evidence; absence from this bounded index is not proof that no physical or private copy survives.")

if __name__=="__main__":
    main()
