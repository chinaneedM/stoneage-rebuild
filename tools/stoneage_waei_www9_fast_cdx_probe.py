#!/usr/bin/env python3
"""Fast CDX-only census for Waei www9 trial-download timeline.

No archived HTML replay and no binary access. This exists to answer quickly:
1) whether Dcat_ID=2 has captures after 2000-12-06;
2) which downloading.php?ID=N router URLs were archived through 2001-01-12.
"""
from __future__ import annotations
import hashlib, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"; TO="20010112"
ID_RE=re.compile(r"(?:[?&]ID=)(\d+)",re.I)

TARGETS=(
 ("trial","http://www9.waei.net/download.php?Dcat_ID=2","exact"),
 ("trial80","http://www9.waei.net:80/download.php?Dcat_ID=2","exact"),
 ("root","http://www9.waei.net/download.php","exact"),
 ("root80","http://www9.waei.net:80/download.php","exact"),
 ("router","http://www9.waei.net/download/downloading.php?ID=","prefix"),
 ("router80","http://www9.waei.net:80/download/downloading.php?ID=","prefix"),
)

def clean(v,n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=55,max_bytes=16*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.1","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(original,match_type):
    params=[
      ("url",original),("matchType",match_type),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from",FROM),("to",TO),("limit","50000")
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    h=obj[0]
    return tuple(dict(zip(h,r)) for r in obj[1:] if isinstance(r,list))

def did(url):
    m=ID_RE.search(str(url or ""))
    return m.group(1) if m else ""

def main():
    print("StoneAge Waei www9 fast CDX timeline census — R1")
    print(f"SCOPE|CDX-only|window={FROM}..{TO}|no replay|no payload|no collapse")
    errors=[];trial=[];root=[];routers={}
    for label,url,kind in TARGETS:
        try:
            st,final,b=fetch(cdx_url(url,kind))
            rr=rows(b)
            print(f"QUERY|label={label}|kind={kind}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                rec=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("statuscode") or ""),str(r.get("mimetype") or ""),str(r.get("digest") or ""),str(r.get("length") or ""),str(r.get("redirect") or ""))
                if label.startswith("trial"): trial.append((label,rec))
                elif label.startswith("root"): root.append((label,rec))
                else:
                    i=did(r.get("original"))
                    if i: routers[(i,)+rec]=label
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))

    # de-duplicate cross-host variants
    def uniq(entries):
        seen=set();out=[]
        for label,rec in entries:
            k=rec
            if k in seen:continue
            seen.add(k);out.append((label,rec))
        return out
    trial=uniq(trial);root=uniq(root)

    for label,rec in sorted(trial,key=lambda x:x[1][0]):
        ts,orig,status,mime,digest,length,redirect=rec
        print(f"TRIAL_CAPTURE|label={label}|timestamp={clean(ts)}|status={clean(status)}|mime={clean(mime)}|length={clean(length)}|digest={clean(digest)}|redirect={clean(redirect)}|original={clean(orig)}")
    for label,rec in sorted(root,key=lambda x:x[1][0]):
        ts,orig,status,mime,digest,length,redirect=rec
        print(f"ROOT_CAPTURE|label={label}|timestamp={clean(ts)}|status={clean(status)}|mime={clean(mime)}|length={clean(length)}|digest={clean(digest)}|redirect={clean(redirect)}|original={clean(orig)}")
    for key,label in sorted(routers.items(),key=lambda kv:(int(kv[0][0]),kv[0][1])):
        i,ts,orig,status,mime,digest,length,redirect=key
        print(f"ROUTER_CAPTURE|label={label}|id={i}|timestamp={clean(ts)}|status={clean(status)}|mime={clean(mime)}|length={clean(length)}|digest={clean(digest)}|redirect={clean(redirect)}|original={clean(orig)}")

    trial_ts=sorted({r[1][0] for r in trial})
    root_ts=sorted({r[1][0] for r in root})
    ids=sorted({k[0] for k in routers},key=int)
    post_dec6=[t for t in trial_ts if t>"20001206235959"]
    print(f"COUNT|trial_captures|{len(trial)}")
    print(f"COUNT|trial_unique_timestamps|{len(trial_ts)}")
    print(f"COUNT|trial_post_dec6|{len(post_dec6)}")
    if trial_ts: print("TRIAL_TIMESTAMPS|"+";".join(trial_ts))
    if post_dec6: print("TRIAL_POST_DEC6|"+";".join(post_dec6))
    print(f"COUNT|root_captures|{len(root)}")
    if root_ts: print("ROOT_TIMESTAMPS|"+";".join(root_ts))
    print(f"COUNT|router_rows|{len(routers)}")
    print(f"COUNT|router_ids|{len(ids)}")
    if ids: print("ROUTER_IDS|"+",".join(ids))
    for label,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if post_dec6:
        print("RESOLUTION|POST_DEC6_TRIAL_CAPTURES_EXIST|target only those timestamps for semantic replay")
    elif ids:
        print("RESOLUTION|NO_LATE_TRIAL_CAPTURE_BUT_ROUTER_IDS_EXIST|classify post-Dec6 IDs and redirects")
    elif errors:
        print("RESOLUTION|PARTIAL_CDX_CENSUS|retry failed surfaces only")
    else:
        print("RESOLUTION|NO_POST_DEC6_TRIAL_OR_ROUTER_INDEX|switch to external mirrors/other Waei surfaces")
    print("EVIDENCE_BOUNDARY|CDX metadata establishes capture/routing topology only; no title or payload identity is inferred.")

if __name__=="__main__":main()
