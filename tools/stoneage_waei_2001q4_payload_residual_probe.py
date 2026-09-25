#!/usr/bin/env python3
"""Close timed-out residuals from the Waei Q4-2001 payload-domain census.

R1 completed 7/12 month+extension queries. The missing combinations include
the highest-value November EXE surface. R2 splits only those failed
month/extension combinations into smaller date windows to reduce CDX timeout
risk. Metadata only; no archived payload is downloaded.
"""
from __future__ import annotations
import hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
DOMAIN="waei.com.cn"
WINDOWS=(
 ("oct-a","20011001","20011015","rar"),
 ("oct-b","20011016","20011031","rar"),
 ("nov-a","20011101","20011110","exe"),
 ("nov-b","20011111","20011120","exe"),
 ("nov-c","20011121","20011130","exe"),
 ("nov-a","20011101","20011110","cab"),
 ("nov-b","20011111","20011120","cab"),
 ("nov-c","20011121","20011130","cab"),
 ("nov-a","20011101","20011110","rar"),
 ("nov-b","20011111","20011120","rar"),
 ("nov-c","20011121","20011130","rar"),
 ("dec-a","20011201","20011210","exe"),
 ("dec-b","20011211","20011220","exe"),
 ("dec-c","20011221","20011231","exe"),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=6*1024*1024):
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
    h=obj[0]
    return tuple(dict(zip(h,r)) for r in obj[1:] if isinstance(r,list))

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
    print("StoneAge Beijing-Waei Q4-2001 payload-domain residual census — R2")
    print("SCOPE|failed R1 month/extensions split into smaller windows|CDX-metadata-only|no-payload")
    errors=[];seen={};completed=0
    for label,start,end,ext in WINDOWS:
        try:
            st,final,b=fetch(cdx_url(start,end,ext))
            rr=rows(b);completed+=1
            print(f"CDX|window={label}|ext={ext}|from={start}|to={end}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                u=str(r.get("original") or "")
                seen[(u,str(r.get("digest") or ""))]=r
        except Exception as e:
            errors.append((f"{label}:{ext}:{start}-{end}",type(e).__name__,str(e)))
    cand=[]
    for r in seen.values():
        u=str(r.get("original") or "");s=score(u)
        if s>0:cand.append((s,u,r))
    cand.sort(key=lambda x:(x[0],x[1]),reverse=True)
    for s,u,r in cand:
        print(f"CANDIDATE|score={s}|timestamp={clean(r.get('timestamp'))}|original={clean(u)}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
    exact=[x for x in cand if "stoneage2.0setup" in urllib.parse.unquote_plus(x[1]).lower()]
    print(f"COUNT|queries|{len(WINDOWS)}")
    print(f"COUNT|completed_queries|{completed}")
    print(f"COUNT|unique_payload_urls|{len(seen)}")
    print(f"COUNT|stoneage_candidates|{len(cand)}")
    print(f"COUNT|exact_sina_filename_urls|{len(exact)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:
        print("RESOLUTION|EXACT_SINA_FILENAME_ON_WAEI_DOMAIN|inspect archived route/object before byte-equivalence claim")
    elif cand:
        print("RESOLUTION|WAEI_Q4_STONEAGE_PAYLOAD_TOKENS_FOUND|classify candidates against 2.0 client/update semantics")
    elif errors:
        print("RESOLUTION|WAEI_Q4_RESIDUAL_INCOMPLETE|do not close official payload-domain surface")
    else:
        print("RESOLUTION|NO_WAEI_Q4_STONEAGE_PAYLOAD_ROW_IN_RESIDUALS|combine with R1 completed windows to close the tested extension-index surface")
    print("EVIDENCE_BOUNDARY|CDX rows are archive URL metadata only; absence on tested indexes does not prove historical nonexistence.")

if __name__=="__main__":
    main()
