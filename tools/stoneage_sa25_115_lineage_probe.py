#!/usr/bin/env python3
"""Probe public preservation indexes for the 2011 StoneAge 2.5 115.com one-click token.

Metadata/index access only. The probe does not log in, bypass expired-host
controls, guess credentials, or download/execute game payloads.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
WAYBACK="https://web.archive.org/cdx/search/cdx"
ARQUIVO="https://arquivo.pt/wayback/cdx"
IA="https://archive.org/advancedsearch.php"

SOURCE_THREAD="https://www.iopq.net/thread-16731619-1-1.html"
SOURCE_DATE="2011-07-21"
TOKEN="clnrsbsc"
FILENAME="石器时代2.5精灵王的传说一键.zip"

TARGET_URLS=(
    ("u115-http","http://u.115.com/file/clnrsbsc"),
    ("u115-https","https://u.115.com/file/clnrsbsc"),
    ("115-http","http://115.com/file/clnrsbsc"),
    ("115-https","https://115.com/file/clnrsbsc"),
)
SEARCH_TERMS=(
    TOKEN,
    FILENAME,
    '"石器时代2.5精灵王的传说一键"',
)

def clean(v,n=1800):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=25,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,
                "Accept":"application/json,text/plain,*/*",
            })
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(3_000_001)
                if len(b)>3_000_000:
                    raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
        except Exception as e:
            last=e
            if i+1<attempts:
                time.sleep(1.5*(i+1))
    raise last

def parse_cdx(body):
    text=body.decode("utf-8","replace").strip()
    if not text:
        return []
    try:
        obj=json.loads(text)
    except Exception:
        rows=[]
        for line in text.splitlines():
            line=line.strip()
            if not line: continue
            if not line.startswith("{"):
                k=line.find("{")
                if k>=0: line=line[k:]
            try: item=json.loads(line)
            except Exception: continue
            if isinstance(item,dict): rows.append(item)
        return rows
    if isinstance(obj,list):
        if obj and isinstance(obj[0],list):
            h=[str(x) for x in obj[0]]
            return [dict(zip(h,row)) for row in obj[1:] if isinstance(row,list)]
        return [x for x in obj if isinstance(x,dict)]
    if isinstance(obj,dict):
        for key in ("results","captures","response","items"):
            v=obj.get(key)
            if isinstance(v,list):
                return [x for x in v if isinstance(x,dict)]
        if any(k in obj for k in ("url","original","timestamp")):
            return [obj]
    return []

def wayback_url(target,prefix=False):
    params={
        "url":target+("*" if prefix else ""),
        "output":"json",
        "fl":"timestamp,original,statuscode,mimetype,digest,length",
        "filter":"statuscode:200",
        "collapse":"digest",
        "from":"2010",
        "to":"2014",
        "limit":"200",
    }
    return WAYBACK+"?"+urllib.parse.urlencode(params)

def arquivo_url(target):
    params={
        "url":target,
        "from":"2010",
        "to":"2014",
        "limit":"200",
        "output":"json",
        "filter":"statuscode:200",
    }
    return ARQUIVO+"?"+urllib.parse.urlencode(params)

def ia_url(term):
    q=f'identifier:"{term}" OR title:"{term}" OR description:"{term}" OR filename:"{term}"'
    params={
        "q":q,
        "fl[]":["identifier","title","description"],
        "rows":"100",
        "page":"1",
        "output":"json",
    }
    return IA+"?"+urllib.parse.urlencode(params,doseq=True)

def norm_row(row):
    return {
        "timestamp":row.get("timestamp") or row.get("date") or "",
        "original":row.get("original") or row.get("url") or "",
        "status":row.get("statuscode") or row.get("status") or "",
        "mime":row.get("mimetype") or row.get("mime") or "",
        "digest":row.get("digest") or "",
        "length":row.get("length") or row.get("contentLength") or "",
    }

def probe_cdx(kind,label,target,url):
    try:
        st,final,h,b=fetch(url)
        rows=parse_cdx(b)
        return {
            "kind":kind,"label":label,"target":target,"status":st,
            "bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),
            "final":final,"rows":[norm_row(x) for x in rows],"error":None,
        }
    except Exception as e:
        return {"kind":kind,"label":label,"target":target,"rows":[],"error":f"{type(e).__name__}: {e}"}

def probe_ia(term):
    try:
        st,final,h,b=fetch(ia_url(term))
        obj=json.loads(b.decode("utf-8","replace"))
        docs=[]
        if isinstance(obj,dict):
            docs=(obj.get("response") or {}).get("docs") or []
        return {
            "kind":"ia-search","label":term,"target":term,"status":st,
            "bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),
            "final":final,"docs":[x for x in docs if isinstance(x,dict)],"error":None,
        }
    except Exception as e:
        return {"kind":"ia-search","label":term,"target":term,"docs":[],"error":f"{type(e).__name__}: {e}"}

def main():
    print("StoneAge 2.5 2011 115.com lineage preservation probe — R1")
    print("SCOPE|exact-115-token+filename|public-index-metadata-only|no-login|no-bypass|no-payload-download")
    print(f"SOURCE_THREAD|{SOURCE_THREAD}")
    print(f"SOURCE_DATE|{SOURCE_DATE}")
    print(f"SOURCE_TOKEN|{TOKEN}")
    print(f"SOURCE_FILENAME|{FILENAME}")
    jobs=[]
    for label,target in TARGET_URLS:
        jobs.append(("wayback-exact",label,target,wayback_url(target,False)))
        jobs.append(("wayback-prefix",label,target,wayback_url(target,True)))
        jobs.append(("arquivo-exact",label,target,arquivo_url(target)))
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futs=[ex.submit(probe_cdx,*j) for j in jobs]
        futs += [ex.submit(probe_ia,t) for t in SEARCH_TERMS]
        for f in futs:
            results.append(f.result())

    total_rows=0; wb_rows=0; arq_rows=0; ia_docs=0; errors=0
    for r in results:
        if r.get("error"):
            errors+=1
            print(f"ERROR|kind={clean(r['kind'])}|label={clean(r['label'])}|target={clean(r['target'])}|message={clean(r['error'])}")
            continue
        if r["kind"]=="ia-search":
            docs=r.get("docs",[])
            ia_docs+=len(docs)
            print(f"QUERY|kind=ia-search|term={clean(r['label'])}|status={r['status']}|bytes={r['bytes']}|sha256={r['sha256']}|docs={len(docs)}|final={clean(r['final'])}")
            for i,d in enumerate(docs[:100],1):
                print(f"IA_DOC|term={clean(r['label'])}|index={i}|identifier={clean(d.get('identifier'))}|title={clean(d.get('title'))}|description={clean(d.get('description'),2400)}")
            continue
        rows=r.get("rows",[])
        total_rows+=len(rows)
        if r["kind"].startswith("wayback"): wb_rows+=len(rows)
        if r["kind"].startswith("arquivo"): arq_rows+=len(rows)
        print(f"QUERY|kind={clean(r['kind'])}|label={clean(r['label'])}|target={clean(r['target'])}|status={r['status']}|bytes={r['bytes']}|sha256={r['sha256']}|rows={len(rows)}|final={clean(r['final'])}")
        for i,row in enumerate(rows[:200],1):
            print(
                "CDX_ROW|"
                f"kind={clean(r['kind'])}|label={clean(r['label'])}|index={i}|"
                f"timestamp={clean(row['timestamp'])}|original={clean(row['original'])}|"
                f"status={clean(row['status'])}|mime={clean(row['mime'])}|"
                f"digest={clean(row['digest'])}|length={clean(row['length'])}"
            )

    print(f"COUNT|targets|{len(TARGET_URLS)}")
    print(f"COUNT|search_terms|{len(SEARCH_TERMS)}")
    print(f"COUNT|wayback_rows|{wb_rows}")
    print(f"COUNT|arquivo_rows|{arq_rows}")
    print(f"COUNT|ia_docs|{ia_docs}")
    print(f"COUNT|errors|{errors}")
    if wb_rows or arq_rows or ia_docs:
        print("RESOLUTION|PUBLIC_PRESERVATION_CANDIDATE_FOUND|inspect metadata carefully; lineage is descendant one-click, not clean 2002 provenance")
    elif errors:
        print("RESOLUTION|NO_HIT_ON_SUCCESSFUL_SURFACES_WITH_PARTIAL_ERRORS|do not infer global absence")
    else:
        print("RESOLUTION|NO_PUBLIC_PRESERVATION_HIT_ON_TESTED_INDEXES|retain exact token/filename as lineage key")
    print("EVIDENCE_BOUNDARY|The 2011 one-click package is a descendant engineering distribution. Even a recovered archive would require byte comparison and cannot establish 2002 operator-disc provenance by title alone.")

if __name__=="__main__":
    main()
