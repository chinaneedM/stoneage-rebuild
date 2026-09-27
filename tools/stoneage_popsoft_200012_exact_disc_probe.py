#!/usr/bin/env python3
"""Bound the Dec-2000 Popsoft companion-disc hypothesis using exact image tokens.

Source-derived surviving catalogue metadata identifies Popsoft / 大众软件
2000.12 (issue 43) as a 2-CD set:
- popcd2k12_a.iso, 725,613,168 bytes,
  SHA1 1D674459E1EC61706A688AA73C94DFDC1802C074
- popcd2k12_b.iso, 722,513,232 bytes,
  SHA1 97CF4340916C39D9AA56278C6B86615E8D486DEC

The surviving catalogue description enumerates CD1 and CD2 contents and does
not name StoneAge. This probe independently searches public preservation
indexes by exact filename/hash. Metadata/indexes only: no ISO payload download.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DISCM="https://discmaster.textfiles.com/search"
YEAR_MIN="1999"; YEAR_MAX="2002"

IMAGES=(
    ("cd1","popcd2k12_a.iso","1D674459E1EC61706A688AA73C94DFDC1802C074",725_613_168),
    ("cd2","popcd2k12_b.iso","97CF4340916C39D9AA56278C6B86615E8D486DEC",722_513_232),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch_json(url,timeout=45,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8"))

def ia_url(term):
    p=[
        ("q",f'"{term}"'),
        ("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("fl[]","year"),
        ("fl[]","description"),("fl[]","collection"),("fl[]","mediatype"),
        ("rows","100"),("page","1"),("output","json"),
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(term,field):
    p=[
        ("q",f'"{term}"'),("qfields",field),("mode","deep"),("dedup","dedup"),
        ("limit","200"),("outputAs","json"),("showItemName","showItemName"),
        ("tsMin",YEAR_MIN),("tsMax",YEAR_MAX),
    ]
    return DISCM+"?"+urllib.parse.urlencode(p)

def ia_docs(data):
    return tuple(x for x in data.get("response",{}).get("docs",[]) if isinstance(x,dict))

def discm_rows(data):
    rows=[]
    def walk(n):
        if isinstance(n,dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n):
                rows.append(n)
            for v in n.values(): walk(v)
        elif isinstance(n,list):
            for v in n: walk(v)
    walk(data)
    out=[]; seen=set()
    for row in rows:
        key=(str(row.get("itemid","")),str(row.get("fileid","")),str(row.get("href","")))
        if key not in seen:
            seen.add(key); out.append(row)
    return tuple(out)

def main():
    print("StoneAge Popsoft Dec-2000 exact companion-disc preservation probe — R1")
    print("SCOPE|exact ISO filename+SHA1|InternetArchive+DiscMaster metadata only|no ISO payload")
    print("HYPOTHESIS_BOUNDARY|Popsoft is a candidate only; collector magazine-carrier claim does not name Popsoft.")
    for label,name,sha1,size in IMAGES:
        print(f"ANCHOR|label={label}|filename={name}|size={size}|sha1={sha1}")

    jobs=[]
    for label,name,sha1,size in IMAGES:
        jobs += [
            ("ia",label,"filename",name,""),
            ("ia",label,"sha1",sha1,""),
            ("discm",label,"filename",name,"name"),
            ("discm",label,"filename-text",name,"t"),
            ("discm",label,"sha1",sha1,"t"),
        ]

    errors=[]; ia_hits=[]; dm_hits=[]

    def one(kind,label,basis,term,field):
        url=ia_url(term) if kind=="ia" else discm_url(term,field)
        st,final,b,data=fetch_json(url,timeout=55)
        rows=ia_docs(data) if kind=="ia" else discm_rows(data)
        return kind,label,basis,term,field,st,final,b,rows

    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(one,*j):j for j in jobs}
        for fut in concurrent.futures.as_completed(futs):
            j=futs[fut]
            try: results.append(fut.result())
            except Exception as e: errors.append((f"{j[0]}:{j[1]}:{j[2]}",type(e).__name__,str(e)))

    for kind,label,basis,term,field,st,final,b,rows in sorted(results,key=lambda x:(x[1],x[0],x[2],x[4])):
        digest=hashlib.sha256(b).hexdigest()
        if kind=="ia":
            print(f"IA_QUERY|label={label}|basis={basis}|term={clean(term)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={digest}|final={clean(final)}")
            for row in rows:
                ia_hits.append((label,basis,row))
                print(f"IA_HIT|label={label}|basis={basis}|identifier={clean(row.get('identifier'))}|title={clean(row.get('title'))}|date={clean(row.get('date'))}|year={clean(row.get('year'))}|collection={clean(row.get('collection'))}|mediatype={clean(row.get('mediatype'))}")
        else:
            print(f"DISCM_QUERY|label={label}|basis={basis}|field={field}|term={clean(term)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={digest}|final={clean(final)}")
            for row in rows:
                dm_hits.append((label,basis,row))
                print(f"DISCM_HIT|label={label}|basis={basis}|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")

    print(f"COUNT|queries_planned={len(jobs)}")
    print(f"COUNT|queries_completed={len(results)}")
    print(f"COUNT|ia_hits={len(ia_hits)}")
    print(f"COUNT|discm_hits={len(dm_hits)}")
    print(f"COUNT|errors={len(errors)}")

    if ia_hits or dm_hits:
        print("RESOLUTION|POPSOFT_DEC2000_EXACT_IMAGE_INDEX_HIT|inspect exact preserved item/file tree for StoneAge signatures next")
    elif errors and len(results)<len(jobs):
        print("RESOLUTION|POPSOFT_DEC2000_EXACT_IMAGE_PARTIAL|retry only failed exact filename/hash surfaces")
    else:
        print("RESOLUTION|POPSOFT_DEC2000_EXACT_IMAGE_INDEX_BOUNDED|exact 2CD image tokens absent from tested independent indexes")
    print("EVIDENCE_BOUNDARY|Index absence does not prove disc contents; surviving catalogue content list and magazine OCR remain separate evidence. No ISO bytes are fetched.")

if __name__=="__main__":
    main()
