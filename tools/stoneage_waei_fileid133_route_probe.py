#!/usr/bin/env python3
"""Bind Waei download.asp?fileid=133 to archived file metadata without fetching payload."""
from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
TARGETS=(
 ("route133","http://www7.waei.net/download/download.asp?fileid=133"),
 ("route133-port80","http://www7.waei.net:80/download/download.asp?fileid=133"),
 ("spr1","http://www7.waei.net/download/file/%AD%D7%B8%C9%B5%7b%A6%A1/spr_1.bin"),
 ("spr1-port80","http://www7.waei.net:80/download/file/%AD%D7%B8%C9%B5%7b%A6%A1/spr_1.bin"),
)
def clean(v,n=4000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]
def fetch(url,timeout=55,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.1","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes)
        return int(getattr(r,"status",r.getcode())),r.geturl(),b
def cdx_url(url):
    p=[("url",url),("matchType","exact"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from","2001"),("to","2002"),("limit","100")]
    return CDX+"?"+urllib.parse.urlencode(p)
def rows(b):
    obj=json.loads(b.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    h=obj[0]
    return tuple(dict(zip(h,r)) for r in obj[1:] if isinstance(r,list))
def main():
    print("StoneAge Waei fileid=133 route binding — R1")
    print("ANCHOR|catalog=石器隱形人無所遁形修正檔|date=2001-04-26|display_size_kb=2822|fileid=133")
    print("KNOWN_PAYLOAD|name=spr_1.bin|bytes=2889630|kib=2821.904296875|sha256=864fa3f6aaeb7d8d2dc9bdee46cecdc7dcee1af0c8f1ed949e09c0526e6aa17e")
    errors=[]
    allrows=[]
    for label,url in TARGETS:
        try:
            st,final,b=fetch(cdx_url(url))
            rr=rows(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                allrows.append((label,r))
                print("ROW|label={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                    label,clean(r.get("timestamp")),clean(r.get("statuscode")),clean(r.get("mimetype")),
                    clean(r.get("length")),clean(r.get("digest")),clean(r.get("redirect")),clean(r.get("original"))
                ))
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    for label,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    route=[r for label,r in allrows if label.startswith("route")]
    spr=[r for label,r in allrows if label.startswith("spr1")]
    print(f"COUNT|route_rows|{len(route)}")
    print(f"COUNT|spr1_rows|{len(spr)}")
    print(f"COUNT|errors|{len(errors)}")
    redirects=[str(r.get("redirect") or "") for r in route if r.get("redirect")]
    if any("spr_1.bin" in x.lower() for x in redirects):
        print("RESOLUTION|DIRECT_ROUTE_BINDING|fileid=133 redirects to spr_1.bin")
    elif route:
        print("RESOLUTION|ROUTE_CAPTURE_FOUND_NO_DIRECT_SPR_REDIRECT|inspect archived route headers/body metadata next")
    elif spr:
        print("RESOLUTION|SIZE_AND_CATALOG_BINDING_ONLY|route unarchived; retain exact size/fileid/catalog coincidence as strong inference")
    else:
        print("RESOLUTION|NO_ARCHIVE_BINDING_ROWS|retain catalog and payload as separate evidence")
    print("EVIDENCE_BOUNDARY|CDX metadata only; no game payload is fetched.")
if __name__=="__main__":main()
