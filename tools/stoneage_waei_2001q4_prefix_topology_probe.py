#!/usr/bin/env python3
"""Census official Waei StoneAge site prefixes in Q4 2001 for download topology.

Contemporaneous evidence anchors /zhuanqu/stoneage/ by 2001-08 and a preserved
official capture anchors /ZHUANQU/stoneage2/ by 2001-12-04. This probe queries
only those two prefixes for 2001-10..12 and emits URL rows whose path/query
contains download/client/update/setup/patch semantics. Metadata only.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIXES=(
 ("stoneage-old","http://www.waei.com.cn/zhuanqu/stoneage/"),
 ("stoneage2","http://www.waei.com.cn/ZHUANQU/stoneage2/"),
)
TOKENS=("download","down/","/down","setup","client","upgrade","update","patch","install","soft","software","stoneage2.0setup")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(prefix):
    p=[
      ("url",prefix),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from","20011001"),("to","20011231"),("collapse","urlkey"),("limit","20000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))

def targetish(url):
    low=urllib.parse.unquote_plus(str(url or "")).lower()
    return any(t in low for t in TOKENS)

def main():
    print("StoneAge Beijing-Waei Q4-2001 official-prefix topology census — R1")
    print("SCOPE|two evidence-anchored official prefixes|2001-10..12|CDX URL metadata|no-payload")
    errors=[];seen={};completed=0
    for label,prefix in PREFIXES:
        try:
            st,final,b=fetch(cdx_url(prefix))
            rr=rows(b);completed+=1
            print(f"CDX|label={label}|prefix={prefix}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                u=str(r.get("original") or "")
                seen[(u,str(r.get("digest") or ""))]=(label,r)
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    hits=[]
    for (label,r) in seen.values():
        u=str(r.get("original") or "")
        if targetish(u):hits.append((label,u,r))
    hits.sort(key=lambda x:(x[0],x[1]))
    for label,u,r in hits:
        print(
          f"TOPOLOGY_HIT|label={label}|timestamp={clean(r.get('timestamp'))}|original={clean(u)}|"
          f"statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|"
          f"digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}"
        )
    exact=[h for h in hits if "stoneage2.0setup" in urllib.parse.unquote_plus(h[1]).lower()]
    print(f"COUNT|prefixes|{len(PREFIXES)}")
    print(f"COUNT|completed_prefixes|{completed}")
    print(f"COUNT|unique_rows|{len(seen)}")
    print(f"COUNT|topology_hits|{len(hits)}")
    print(f"COUNT|exact_sina_filename_hits|{len(exact)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:
        print("RESOLUTION|EXACT_SETUP_PATH_FOUND_IN_OFFICIAL_PREFIX|replay source page/redirect before payload inference")
    elif hits:
        print("RESOLUTION|OFFICIAL_Q4_DOWNLOAD_TOPOLOGY_FOUND|replay bounded HTML/redirect candidates next")
    elif errors:
        print("RESOLUTION|OFFICIAL_Q4_PREFIX_SURFACE_INCOMPLETE|do not close topology")
    else:
        print("RESOLUTION|NO_OFFICIAL_Q4_DOWNLOAD_TOPOLOGY_ROW|tested evidence-anchored prefixes expose no URL-name download clue")
    print("EVIDENCE_BOUNDARY|CDX URL rows are routing metadata only and do not establish binary identity, cleanliness or completeness.")

if __name__=="__main__":
    main()
