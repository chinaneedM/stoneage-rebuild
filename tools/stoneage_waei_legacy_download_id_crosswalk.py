#!/usr/bin/env python3
"""Crosswalk legacy www9 Waei downloading.php IDs around StoneAge launch.

The preserved 2000-12-06 download root uses downloading.php?ID=N and exposes
IDs up through 34. This probe searches exact IDs 30..40 through 2001-06 for
archived router metadata and redirect Locations without following payloads.
It is intentionally separate from the later www7 download.asp?fileid=N system.
"""
from __future__ import annotations
import hashlib,json,urllib.error,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"; TO="20010630"; IDS=range(30,41)

def clean(v,n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=30,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl): return None

def nofollow(url,timeout=35):
    opener=urllib.request.build_opener(NoRedirect)
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*","Accept-Encoding":"identity"},method="GET")
    try:
        with opener.open(req,timeout=timeout) as r:
            r.read(1)
            return int(getattr(r,"status",r.getcode())),dict(r.headers.items())
    except urllib.error.HTTPError as e:
        return int(e.code),dict(e.headers.items())

def cdx(fid,port):
    host="http://www9.waei.net:80" if port else "http://www9.waei.net"
    orig=f"{host}/download/downloading.php?ID={fid}"
    q=[("url",orig),("matchType","exact"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from",FROM),("to",TO),("limit","5000")]
    return orig,CDX+"?"+urllib.parse.urlencode(q)

def rows(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def main():
    print("StoneAge Waei legacy www9 download-ID 30..40 crosswalk — R1")
    print("SCOPE|www9 downloading.php IDs|2000-12..2001-06|CDX + no-follow redirect header only|no payload")
    allrows={};errors=[]
    for fid in IDS:
        for port in (False,True):
            orig,url=cdx(fid,port)
            try:
                st,final,h,b=fetch(url)
                rr=rows(b)
                print(f"CDX|id={fid}|port80={int(port)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
                for r in rr:
                    key=(fid,str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                    allrows[key]=r
            except Exception as e:
                errors.append((f"cdx:{fid}:{int(port)}",type(e).__name__,str(e)))
    for (fid,ts,orig,dig),r in sorted(allrows.items()):
        print(f"ROW|id={fid}|timestamp={ts}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(dig)}|redirect_meta={clean(r.get('redirect'))}|original={clean(orig)}")
        if str(r.get("statuscode") or "") in ("301","302","303","307","308"):
            try:
                st,h=nofollow(f"https://web.archive.org/web/{ts}id_/{orig}")
                print(f"HEADER|id={fid}|timestamp={ts}|status={st}|location={clean(h.get('Location'))}|content_type={clean(h.get('Content-Type'))}|content_length={clean(h.get('Content-Length'))}")
            except Exception as e:
                errors.append((f"header:{fid}:{ts}",type(e).__name__,str(e)))
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={k}|message={clean(m)}")
    ids=sorted({k[0] for k in allrows})
    print(f"COUNT|rows|{len(allrows)}")
    print(f"COUNT|ids_with_rows|{len(ids)}")
    print(f"IDS_WITH_ROWS|{','.join(map(str,ids))}")
    print(f"COUNT|errors|{len(errors)}")
    if 35 in ids:
        print("RESOLUTION|LEGACY_ID35_ARCHIVE_ROW_FOUND|classify redirect target/title against StoneAge launch semantics")
    elif ids:
        print("RESOLUTION|LEGACY_NEIGHBOR_ROWS_FOUND|bound allocation chronology only; adjacency is not identity")
    elif errors:
        print("RESOLUTION|LEGACY_CROSSWALK_PARTIAL|retry failed exact IDs only")
    else:
        print("RESOLUTION|LEGACY_ID30_40_UNINDEXED_AFTER_20001206|root HTML remains the only current evidence for these IDs")
    print("EVIDENCE_BOUNDARY|Legacy www9 IDs and later www7 fileids are distinct namespaces unless direct evidence binds them; no payload is fetched.")

if __name__=="__main__":main()
