#!/usr/bin/env python3
"""Fast CDX-only census of www9.waei.net during the StoneAge trial window."""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0";CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201";TO="20010112"
QUERIES=(("download","http://www9.waei.net/download.php","prefix"),("host","http://www9.waei.net/","prefix"))
BINARY=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z",".bin",".iso",".cue")

def clean(v,n=5000): return " ".join(str(v or "").split()).replace("|","%7C")[:n]
def fetch(url,timeout=70,max_bytes=16*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.1","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b
def url(u,m):
    p=[("url",u),("matchType",m),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from",FROM),("to",TO),("filter","statuscode:200"),("limit","30000"),("collapse","urlkey")]
    return CDX+"?"+urllib.parse.urlencode(p)
def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0];return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))
def binary(u):return urllib.parse.urlsplit(urllib.parse.unquote_plus(str(u)).lower()).path.endswith(BINARY)
def params(u):
    q=urllib.parse.parse_qs(urllib.parse.urlsplit(str(u)).query,keep_blank_values=True)
    return ",".join(f"{k}={';'.join(v)}" for k,v in sorted(q.items()))
def main():
    print("StoneAge Waei www9 trial-window CDX census — R1")
    print(f"SCOPE|CDX metadata only|{FROM}..{TO}|no HTML replay|no payload")
    rows={};errors=[]
    for label,u,m in QUERIES:
        try:
            st,final,b=fetch(url(u,m));rr=parse(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                k=(str(r.get("original") or ""),str(r.get("timestamp") or ""),str(r.get("digest") or ""));rows[k]=r
        except Exception as e:errors.append((label,type(e).__name__,str(e)))
    rr=sorted(rows.values(),key=lambda r:(str(r.get("timestamp") or ""),str(r.get("original") or "")))
    bins=[]
    for r in rr:
        orig=str(r.get("original") or "");isbin=binary(orig)
        if isbin:bins.append(r)
        print("ROW|timestamp={}|binary={}|params={}|status={}|mime={}|length={}|digest={}|original={}".format(
            clean(r.get("timestamp")),int(isbin),clean(params(orig),1000),clean(r.get("statuscode")),clean(r.get("mimetype")),
            clean(r.get("length")),clean(r.get("digest")),clean(orig)))
    print(f"COUNT|unique_rows|{len(rr)}")
    print(f"COUNT|binary_rows|{len(bins)}")
    print(f"COUNT|download_php_rows|{sum('download.php' in str(r.get('original') or '').lower() for r in rr)}")
    for label,k,m in errors:print(f"ERROR|label={label}|kind={k}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|"+("BINARY_URLS_FOUND" if bins else "URL_TOPOLOGY_ONLY"))
if __name__=="__main__":main()
