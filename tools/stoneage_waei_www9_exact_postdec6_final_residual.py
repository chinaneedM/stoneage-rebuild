#!/usr/bin/env python3
"""Final bounded retry for Waei www9 dynamic IDs 59 and 60.

R1+R2 established zero rows for IDs 35..58 except no remaining gaps.
Only IDs 59 and 60 timed out twice in R2. This pass checks both the literal
port-80 form preserved by the Dec-2000 catalogue and the equivalent no-port
form, after the earlier query burst has cooled down.

CDX metadata only; no archived payload body is fetched.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001207"
TO="20010112"
IDS=(59,60)
VARIANTS=("port80","noport")
ATTEMPTS=2

def clean(v,n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def original(fid,variant):
    host="http://www9.waei.net:80" if variant=="port80" else "http://www9.waei.net"
    return f"{host}/download/downloading.php?ID={fid}"

def cdx_url(fid,variant):
    q=[
        ("url",original(fid,variant)),
        ("matchType","exact"),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(q)

def fetch(url,timeout=32,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(max_bytes+1)
        if len(body)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),body

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,row)) for row in obj[1:] if isinstance(row,list))

def main():
    print("StoneAge Waei www9 exact-ID final residual — R3")
    print("PARENT|STONEAGE-WAEI-WWW9-EXACT-POSTDEC6-IDS-RESIDUAL-R2|IDs 59,60 timeout only")
    print(f"SCOPE|ids={','.join(map(str,IDS))}|variants={','.join(VARIANTS)}|window={FROM}..{TO}|CDX metadata only")
    results={}
    errors=[]
    allrows={}

    for fid in IDS:
        for variant in VARIANTS:
            last=None
            for attempt in range(1,ATTEMPTS+1):
                try:
                    st,final,body=fetch(cdx_url(fid,variant))
                    rr=rows(body)
                    results[(fid,variant)]=(st,final,body,rr,attempt)
                    break
                except Exception as exc:
                    last=(type(exc).__name__,str(exc))
                    print(f"RETRY_ERROR|id={fid}|variant={variant}|attempt={attempt}|kind={clean(last[0])}|message={clean(last[1])}")
                    if attempt<ATTEMPTS:
                        time.sleep(3)
            if (fid,variant) not in results and last:
                errors.append((fid,variant,last[0],last[1]))
            time.sleep(1)

    for fid in IDS:
        for variant in VARIANTS:
            key=(fid,variant)
            if key not in results:
                continue
            st,final,body,rr,attempt=results[key]
            print(
                f"CDX|id={fid}|variant={variant}|attempt={attempt}|status={st}|rows={len(rr)}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(final)}"
            )
            for r in rr:
                rk=(fid,str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                allrows[rk]=r

    for (fid,ts,orig,digest),r in sorted(allrows.items()):
        print(
            f"ROW|id={fid}|timestamp={ts}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|"
            f"length={clean(r.get('length'))}|digest={clean(digest)}|redirect={clean(r.get('redirect'))}|original={clean(orig)}"
        )

    for fid,variant,kind,msg in errors:
        print(f"ERROR|id={fid}|variant={variant}|kind={clean(kind)}|message={clean(msg)}")

    completed_ids=sorted({
        fid for fid in IDS
        if any((fid,v) in results for v in VARIANTS)
    })
    ids_with_rows=sorted({k[0] for k in allrows})
    print(f"COUNT|queries_planned|{len(IDS)*len(VARIANTS)}")
    print(f"COUNT|queries_completed|{len(results)}")
    print(f"COUNT|ids_completed|{len(completed_ids)}")
    print(f"IDS_COMPLETED|{','.join(map(str,completed_ids))}")
    print(f"COUNT|rows|{len(allrows)}")
    print(f"COUNT|ids_with_rows|{len(ids_with_rows)}")
    print(f"IDS_WITH_ROWS|{','.join(map(str,ids_with_rows))}")
    print(f"COUNT|errors|{len(errors)}")

    if allrows:
        print("RESOLUTION|EXACT_WWW9_FINAL_RESIDUAL_ROWS_FOUND|classify direct rows before any further search")
    elif len(completed_ids)==len(IDS):
        print("RESOLUTION|EXACT_WWW9_IDS35_60_BOUNDED|R1+R2+R3 provide successful exact-query coverage for every ID 35..60 with zero rows")
    else:
        print("RESOLUTION|EXACT_WWW9_IDS59_60_STILL_PARTIAL|do not infer absence from remaining transport failures")

    print("EVIDENCE_BOUNDARY|This closes only the tested Wayback exact-ID surface; it does not negate the independently documented Jan-2001 trial download.")

if __name__=="__main__":
    main()
