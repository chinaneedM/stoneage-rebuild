#!/usr/bin/env python3
"""Census Beijing-Waei's Q4-2001 payload URL surface for StoneAge 2.0.

Period sources place the official StoneAge site at /zhuanqu/stoneage/ by
2001-08, while a preserved 2001-12-04 official page exists under
/ZHUANQU/stoneage2/. Earlier Waei payload-domain work covered 2002 Q1 only.
This probe closes the missing 2001-10..12 domain-family EXE/ZIP/CAB/RAR index
window and emits StoneAge-relevant URL metadata only. No payload download.
"""
from __future__ import annotations
import hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
DOMAIN="waei.com.cn"
WINDOWS=(("oct","20011001","20011031"),("nov","20011101","20011130"),("dec","20011201","20011231"))
EXTS=("exe","zip","cab","rar")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(start,end,ext):
    p=[
      ("url",DOMAIN),("matchType","domain"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length"),
      ("from",start),("to",end),("collapse","urlkey"),("limit","10000"),
      ("filter",rf"original:.*[.]{ext}(?:[?].*)?$"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    header=obj[0]
    return tuple(dict(zip(header,r)) for r in obj[1:] if isinstance(r,list))

def score(url):
    low=urllib.parse.unquote_plus(str(url or "")).lower()
    s=0
    if "stoneage2" in low:s+=8
    elif "stoneage" in low:s+=6
    if "2.0" in low or "20" in low:s+=2
    if any(k in low for k in ("setup","client","upgrade","update","patch")):s+=5
    if any(k in low for k in ("download","down/","/down","accessories")):s+=2
    if "stoneage2.0setup" in low:s+=20
    if re.search(r"(?:^|[/_.-])sa(?:20|2)[^/]*[.](?:exe|zip|cab|rar)(?:[?]|$)",low):s+=4
    return s

def main():
    print("StoneAge Beijing-Waei Q4-2001 payload-domain census — R1")
    print("SCOPE|waei.com.cn domain family|2001-10..12|EXE+ZIP+CAB+RAR|CDX-metadata-only|no-payload")
    print("TOPOLOGY|2001-08=/zhuanqu/stoneage/|2001-12-04=/ZHUANQU/stoneage2/")
    errors=[];seen={};completed=0
    for label,start,end in WINDOWS:
        for ext in EXTS:
            try:
                st,final,b=fetch(cdx_url(start,end,ext))
                rr=rows(b); completed+=1
                print(f"CDX|window={label}|ext={ext}|from={start}|to={end}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
                for r in rr:
                    u=str(r.get("original") or "")
                    seen[(u,str(r.get("digest") or ""))]=r
            except Exception as e:
                errors.append((f"{label}:{ext}",type(e).__name__,str(e)))
    cand=[]
    for r in seen.values():
        u=str(r.get("original") or ""); s=score(u)
        if s>0:cand.append((s,u,r))
    cand.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for s,u,r in cand:
        print(
          f"CANDIDATE|score={s}|timestamp={clean(r.get('timestamp'))}|original={clean(u)}|"
          f"statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|"
          f"digest={clean(r.get('digest'))}|length={clean(r.get('length'))}"
        )
    exact=[x for x in cand if "stoneage2.0setup" in urllib.parse.unquote_plus(x[1]).lower()]
    print(f"COUNT|queries|{len(WINDOWS)*len(EXTS)}")
    print(f"COUNT|completed_queries|{completed}")
    print(f"COUNT|unique_payload_urls|{len(seen)}")
    print(f"COUNT|stoneage_candidates|{len(cand)}")
    print(f"COUNT|exact_sina_filename_urls|{len(exact)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:
        print("RESOLUTION|EXACT_SINA_FILENAME_ON_WAEI_DOMAIN|inspect archived route/object before any byte-equivalence claim")
    elif cand:
        print("RESOLUTION|WAEI_Q4_STONEAGE_PAYLOAD_TOKENS_FOUND|classify candidates against 2.0 client/update semantics")
    elif errors:
        print("RESOLUTION|WAEI_Q4_SURFACE_INCOMPLETE|do not close official download topology")
    else:
        print("RESOLUTION|NO_WAEI_Q4_STONEAGE_PAYLOAD_ROW|tested Q4 extension index exposes no StoneAge payload URL")
    print("EVIDENCE_BOUNDARY|CDX rows prove archived URL metadata only; filenames/routes do not prove payload identity or operator-distributed client bytes.")

if __name__=="__main__":
    main()
