#!/usr/bin/env python3
"""Retry only the unresolved sa_25.exe Wayback CDX exact target.

This closes the two transient timeout surfaces from the broader
runtime-generation census. Metadata only; no executable payload.
"""
from __future__ import annotations
import hashlib,json,time,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGET="http://stoneage.waei.net/saupdate/sa_25.exe"
CDX="https://web.archive.org/cdx/search/cdx"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def url():
    p=[("url",TARGET),("matchType","exact"),("output","json"),("fl",FIELDS),
       ("from","20000101"),("to","20021231"),("limit","5000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def fetch(attempts=4):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url(),headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
            with urllib.request.urlopen(req,timeout=75) as r:
                b=r.read(4*1024*1024)
                return int(getattr(r,"status",r.getcode())),r.geturl(),b,i+1
        except Exception as e:
            last=e
            if i+1<attempts: time.sleep(2+i*2)
    raise last

def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def main():
    print("StoneAge Waei sa_25 exact CDX residual — R1")
    print("PARENT|STONEAGE-WAEI-RUNTIME-GENERATIONS-R1|generation=25-timeouts-only")
    print("SCOPE|exact Wayback metadata retry|2000..2002|no payload")
    try:
        st,final,b,attempt=fetch()
        rr=parse(b)
        print(f"QUERY|status={st}|attempt={attempt}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        for r in rr:
            print("ROW|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                clean(r.get("timestamp")),clean(r.get("statuscode")),clean(r.get("mimetype")),
                clean(r.get("length")),clean(r.get("digest")),clean(r.get("redirect")),clean(r.get("original"))
            ))
        good=sum(1 for r in rr if str(r.get("statuscode") or "")=="200" and "octet-stream" in str(r.get("mimetype") or "").lower())
        print(f"COUNT|rows|{len(rr)}")
        print(f"COUNT|http200_octet|{good}")
        print("COUNT|errors|0")
        if good: print("RESOLUTION|SA25_RUNTIME_BYTES_INDEXED|fingerprint exact preserved payload next")
        else: print("RESOLUTION|SA25_EXACT_ROUTE_BOUNDED|no indexed executable payload on tested first-party path")
    except Exception as e:
        print(f"ERROR|kind={type(e).__name__}|message={clean(e)}")
        print("COUNT|errors|1")
        print("RESOLUTION|SA25_ARCHIVE_INTERFACE_RESIDUAL_OPEN|do not infer absence")
    print("EVIDENCE_BOUNDARY|SA_25 label is a historical update-generation token, not marketing version 2.5 by itself.")

if __name__=="__main__":main()
