#!/usr/bin/env python3
"""Crosswalk early Waei central-download file IDs around StoneAge launch.

Queries fileid 30..40 across Dec-2000..Jun-2001 and, for archived redirect
captures only, replays headers without following Location. No target payload
body is fetched.
"""
from __future__ import annotations
import hashlib,json,urllib.error,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201";TO="20010630"
IDS=range(30,41)

def clean(v,n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=30,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl): return None

def head_nofollow(url,timeout=35):
    opener=urllib.request.build_opener(NoRedirect)
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*","Accept-Encoding":"identity"},method="GET")
    try:
        with opener.open(req,timeout=timeout) as r:
            # Read at most one byte; this path is expected to be redirect metadata.
            r.read(1)
            return int(getattr(r,"status",r.getcode())),dict(r.headers.items()),r.geturl()
    except urllib.error.HTTPError as e:
        return int(e.code),dict(e.headers.items()),url

def cdx(fid,port):
    host="http://www7.waei.net:80" if port else "http://www7.waei.net"
    orig=f"{host}/download/download.asp?fileid={fid}"
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
    print("StoneAge Waei early fileid 30..40 crosswalk — R1")
    print("SCOPE|central download exact fileids|2000-12..2001-06|CDX + no-follow redirect headers|no target payload")
    errors=[];allrows={}
    for fid in IDS:
        for port in (False,True):
            orig,url=cdx(fid,port)
            try:
                st,final,h,b=fetch(url)
                rr=rows(b)
                print(f"CDX|fileid={fid}|port80={int(port)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
                for r in rr:
                    key=(fid,str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                    allrows[key]=r
            except Exception as e:
                errors.append((f"cdx:{fid}:{int(port)}",type(e).__name__,str(e)))
    for (fid,ts,orig,digest),r in sorted(allrows.items()):
        print(f"ROW|fileid={fid}|timestamp={ts}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(digest)}|redirect_meta={clean(r.get('redirect'))}|original={clean(orig)}")
        if str(r.get("statuscode") or "") in ("301","302","303","307","308"):
            try:
                u=f"https://web.archive.org/web/{ts}id_/{orig}"
                st,h,final=head_nofollow(u)
                print(f"HEADER|fileid={fid}|timestamp={ts}|status={st}|location={clean(h.get('Location'))}|content_type={clean(h.get('Content-Type'))}|content_length={clean(h.get('Content-Length'))}")
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
        print("RESOLUTION|FILEID35_ARCHIVE_ROW_FOUND|classify redirect target against StoneAge trial/client semantics")
    elif ids:
        print("RESOLUTION|NEIGHBOR_FILEID_ROWS_FOUND|use surviving neighbors to bound launch-era allocation; do not infer missing ID identity")
    elif errors:
        print("RESOLUTION|FILEID_CROSSWALK_PARTIAL|retry failed exact IDs only")
    else:
        print("RESOLUTION|FILEID30_40_UNINDEXED|numbering hypothesis remains unsupported by archive rows")
    print("EVIDENCE_BOUNDARY|Sequential IDs are only a search heuristic; adjacency never proves StoneAge identity. Redirect target bodies are not fetched.")

if __name__=="__main__":main()
