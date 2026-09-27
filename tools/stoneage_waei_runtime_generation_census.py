#!/usr/bin/env python3
"""Exact Wayback census for source-grounded Waei StoneAge runtime generations.

Targets are not guessed marketing versions:
- sa_3.exe: accepted Taiwan v1.0 retail runtime filename;
- sa_23.exe: already observed 2001 archived 404 row;
- sa_24.exe: community chronology explicitly names SA_24 on 2001-04-24;
- sa_25.exe: later historical retrospective explicitly names a "sa_25" era;
- sa_40.exe / sa_42.exe: first-party archived byte controls;
- sa_41.exe: the single missing generation between two first-party byte controls.

Metadata only. No executable body is downloaded.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20000101"; TO="20021231"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"
GENERATIONS=(
 ("tw10-runtime-control",3),
 ("archive-neighbor",23),
 ("chronology-trade",24),
 ("chronology-fullscreen",25),
 ("byte-control",40),
 ("gap-between-controls",41),
 ("byte-control",42),
)
HOSTS=("stoneage.waei.net","stoneage.waei.net:80")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=60,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(original):
    p=[("url",original),("matchType","exact"),("output","json"),("fl",FIELDS),
       ("from",FROM),("to",TO),("limit","5000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def rows(body):
    o=json.loads(body.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def original(host,n):
    return f"http://{host}/saupdate/sa_{n}.exe"

def main():
    print("StoneAge Waei source-grounded runtime-generation exact census — R1")
    print(f"SCOPE|exact CDX metadata|{FROM}..{TO}|generations={','.join(str(n) for _,n in GENERATIONS)}|no payload")
    seen={}; errors=[]; per={}
    for reason,n in GENERATIONS:
        per[n]=0
        for host in HOSTS:
            u=original(host,n)
            try:
                st,final,b=fetch(cdx_url(u)); rr=rows(b)
                print(f"QUERY|generation={n}|reason={reason}|host={host}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
                for r in rr:
                    k=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("statuscode") or ""),str(r.get("digest") or ""),str(r.get("redirect") or ""))
                    seen[k]=(n,reason,r)
            except Exception as e:
                errors.append((n,host,type(e).__name__,str(e)))
    ordered=sorted(seen.values(),key=lambda x:(x[0],str(x[2].get("timestamp") or ""),str(x[2].get("original") or "")))
    for n,reason,r in ordered:
        per[n]+=1
        print("ROW|generation={}|reason={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
            n,reason,clean(r.get("timestamp")),clean(r.get("statuscode")),clean(r.get("mimetype")),
            clean(r.get("length")),clean(r.get("digest")),clean(r.get("redirect")),clean(r.get("original"))
        ))
    for reason,n in GENERATIONS:
        good=sum(1 for g,_,r in ordered if g==n and str(r.get("statuscode") or "")=="200" and "octet-stream" in str(r.get("mimetype") or "").lower())
        print(f"GENERATION|n={n}|reason={reason}|rows={per[n]}|http200_octet={good}")
    for n,host,k,m in errors:
        print(f"ERROR|generation={n}|host={clean(host)}|kind={clean(k)}|message={clean(m)}")
    new_good=[n for n,_,r in ordered if n not in (40,42) and str(r.get("statuscode") or "")=="200" and "octet-stream" in str(r.get("mimetype") or "").lower()]
    print(f"COUNT|unique_rows|{len(ordered)}")
    print(f"COUNT|new_http200_binary_generations|{len(set(new_good))}")
    print(f"COUNT|errors|{len(errors)}")
    if new_good:
        print("RESOLUTION|EARLIER_OR_GAP_RUNTIME_BYTES_INDEXED|transiently fingerprint the earliest newly recovered generation next")
    elif errors:
        print("RESOLUTION|PARTIAL_GENERATION_CENSUS|retry failed exact target only")
    else:
        print("RESOLUTION|SOURCE_GROUNDED_GENERATIONS_BOUNDED|only previously known controls survive on tested exact CDX routes")
    print("EVIDENCE_BOUNDARY|numeric sa_N suffix is treated as update/runtime generation, not marketing StoneAge version number.")

if __name__=="__main__":main()
