#!/usr/bin/env python3
"""Probe the first-party StoneAge Waei subdomain for launch-window client artifacts.

The accepted Taiwan v1.0 StoneAge.exe directly contains:
  stoneage.waei.net
  /saupdate/newest.txt
  /saupdate/%s

Earlier trial-client work focused on www9/www7 download-center surfaces. This
probe closes the source-derived StoneAge-specific host gap using Wayback CDX
metadata only.
"""
from __future__ import annotations
import hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"
LAUNCH_FROM="20001201"; LAUNCH_TO="20010112"
UPDATE_FROM="20000101"; UPDATE_TO="20011231"
BINARY=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z",".iso",".bin",".cue",".txt")
HINTS=("stoneage","saupdate","newest","download","trial","demo","test","beta","client","setup","install","update","patch","sa_")

TARGETS=(
 ("launch-host","http://stoneage.waei.net/","prefix",LAUNCH_FROM,LAUNCH_TO,True,True),
 ("launch-host80","http://stoneage.waei.net:80/","prefix",LAUNCH_FROM,LAUNCH_TO,True,True),
 ("update-prefix","http://stoneage.waei.net/saupdate/","prefix",UPDATE_FROM,UPDATE_TO,False,False),
 ("update-prefix80","http://stoneage.waei.net:80/saupdate/","prefix",UPDATE_FROM,UPDATE_TO,False,False),
 ("newest","http://stoneage.waei.net/saupdate/newest.txt","exact",UPDATE_FROM,UPDATE_TO,False,False),
 ("newest80","http://stoneage.waei.net:80/saupdate/newest.txt","exact",UPDATE_FROM,UPDATE_TO,False,False),
)

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=75,max_bytes=32*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(url,match,start,end,status200,collapse):
    p=[("url",url),("matchType",match),("output","json"),("fl",FIELDS),
       ("from",start),("to",end),("limit","50000")]
    if status200:p.append(("filter","statuscode:200"))
    if collapse:p.append(("collapse","urlkey"))
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0];return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def decoded(u):return urllib.parse.unquote_plus(str(u or "")).lower()
def ext(u):
    p=urllib.parse.urlsplit(decoded(u)).path
    m=re.search(r"(\.[a-z0-9]{1,8})$",p)
    return m.group(1) if m else ""
def is_binary(u):return ext(u) in BINARY
def score(u):
    s=decoded(u);return sum(1 for h in HINTS if h in s)

def main():
    print("StoneAge Waei first-party subdomain launch/update CDX census — R1")
    print(f"SOURCE|Taiwan-v1 StoneAge.exe strings|host=stoneage.waei.net|paths=/saupdate/newest.txt,/saupdate/%s")
    print(f"SCOPE|launch={LAUNCH_FROM}..{LAUNCH_TO}|update={UPDATE_FROM}..{UPDATE_TO}|CDX metadata only|no body/payload")
    rows={};errors=[]
    for label,url,match,start,end,s200,collapse in TARGETS:
        try:
            q=cdx_url(url,match,start,end,s200,collapse)
            st,final,b=fetch(q);rr=parse(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                k=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("statuscode") or ""),str(r.get("digest") or ""),str(r.get("redirect") or ""))
                e=rows.setdefault(k,{"row":r,"labels":set()});e["labels"].add(label)
        except Exception as ex:
            errors.append((label,type(ex).__name__,str(ex)))
    ordered=sorted(rows.values(),key=lambda e:(str(e["row"].get("timestamp") or ""),str(e["row"].get("original") or "")))
    candidates=[];bins=[];manifest=[]
    for e in ordered:
        r=e["row"];u=str(r.get("original") or "");sc=score(u);ib=is_binary(u)
        if ib:bins.append(e)
        if "newest.txt" in decoded(u):manifest.append(e)
        if sc or ib:candidates.append((sc,ib,e))
        print("ROW|labels={}|timestamp={}|status={}|score={}|binary={}|ext={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
            clean(",".join(sorted(e["labels"]))),clean(r.get("timestamp")),clean(r.get("statuscode")),sc,int(ib),clean(ext(u)),
            clean(r.get("mimetype")),clean(r.get("length")),clean(r.get("digest")),clean(r.get("redirect")),clean(u)
        ))
    for sc,ib,e in sorted(candidates,key=lambda x:(-x[0],-int(x[1]),str(x[2]["row"].get("original") or ""))):
        r=e["row"]
        print("CANDIDATE|score={}|binary={}|labels={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
            sc,int(ib),clean(",".join(sorted(e["labels"]))),clean(r.get("timestamp")),clean(r.get("statuscode")),
            clean(r.get("mimetype")),clean(r.get("length")),clean(r.get("digest")),clean(r.get("redirect")),clean(r.get("original"))
        ))
    for l,k,m in errors:print(f"ERROR|label={clean(l)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|unique_rows|{len(ordered)}")
    print(f"COUNT|candidate_rows|{len(candidates)}")
    print(f"COUNT|binary_like_rows|{len(bins)}")
    print(f"COUNT|newest_rows|{len(manifest)}")
    print(f"COUNT|errors|{len(errors)}")
    if manifest:
        print("RESOLUTION|WAEI_UPDATE_MANIFEST_CAPTURE_FOUND|replay exact newest.txt next and enumerate named payloads")
    elif bins:
        print("RESOLUTION|WAEI_SUBDOMAIN_BINARY_ROWS_FOUND|classify exact launch/update artifacts next")
    elif ordered:
        print("RESOLUTION|WAEI_SUBDOMAIN_ARCHIVE_FOUND_NO_BINARY|replay only source-linked launch/navigation pages next")
    elif errors:
        print("RESOLUTION|PARTIAL_WAEI_SUBDOMAIN_CENSUS|retry only failed CDX surfaces")
    else:
        print("RESOLUTION|WAEI_SUBDOMAIN_ROUTE_BOUNDED|tested first-party host/path exposes no indexed launch/update rows")
    print("EVIDENCE_BOUNDARY|CDX metadata only; no historical page, manifest or client payload is downloaded.")

if __name__=="__main__":main()
