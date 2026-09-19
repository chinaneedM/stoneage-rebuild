#!/usr/bin/env python3
"""Bounded Wayback identity probe for the 2000 Samsung PC-education operator Mentec.

Metadata/HTML only. Tests a small explicit candidate-domain set; no inference from
similar company names is accepted without period-page identity terms.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="1998"
TO="2002"
DOMAINS=[
    "mentec.co.kr",
    "mentech.co.kr",
    "mantech.co.kr",
    "man-tech.co.kr",
]
TERMS=re.compile(r"(?i)(삼성|PC\s*교육|교육센터|교육장|멘테크|맨테크|Mentec|Mentech|Mantech)")


def clean(v,limit=900):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=15,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,application/json,text/plain,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.status,r.geturl(),r.read()
        except Exception as exc:
            last=exc
            if i+1<attempts:
                time.sleep(0.5*(i+1))
    raise last


def cdx(domain):
    params=[
        ("url",domain+"/"),
        ("matchType","prefix"),
        ("from",FROM),("to",TO),
        ("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length"),
        ("filter","statuscode:200"),
        ("collapse","digest"),
        ("limit","200"),
    ]
    _,_,body=get(CDX+"?"+urllib.parse.urlencode(params),15,2)
    data=json.loads(body.decode("utf-8","replace") or "[]")
    if not isinstance(data,list) or not data:
        return []
    header=data[0]
    return [
        {str(header[i]):str(row[i]) if i<len(row) else "" for i in range(len(header))}
        for row in data[1:] if isinstance(row,list)
    ]


def replay(ts,url):
    errors=[]
    for candidate in (
        f"https://web.archive.org/web/{ts}id_/{url}",
        f"https://web.archive.org/web/{ts}/{url}",
    ):
        try:
            status,final,body=get(candidate,12,1)
            return status,final,body,candidate
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
    raise RuntimeError("; ".join(errors))


def decode(body):
    for enc in ("cp949","euc-kr","utf-8"):
        try:
            return body.decode(enc)
        except UnicodeDecodeError:
            pass
    return body.decode("latin-1","replace")


def snippets(text,radius=180):
    out=[]
    seen=set()
    for m in TERMS.finditer(text):
        s=clean(text[max(0,m.start()-radius):min(len(text),m.end()+radius)],500)
        if s not in seen:
            seen.add(s); out.append(s)
        if len(out)>=30: break
    return out


def domain_probe(domain):
    rows=cdx(domain)
    html_rows=[r for r in rows if "html" in r.get("mimetype","").lower() or r.get("original","").endswith("/")]
    # Prefer earliest distinct HTML-ish captures and cap replays.
    selected=sorted(html_rows,key=lambda r:r.get("timestamp",""))[:12]
    replays=[]
    errors=[]
    for row in selected:
        try:
            status,final,body,used=replay(row["timestamp"],row["original"])
            text=decode(body)
            hits=snippets(text)
            replays.append((row,status,used,hits))
        except Exception as exc:
            errors.append((row,type(exc).__name__,str(exc)))
    return domain,rows,replays,errors


def main():
    print("StoneAge Mentec historical-domain identity probe — R1")
    print("SCOPE|bounded-wayback-metadata-and-homepage-html-only|no-company-identity-inference-without-period-term-hit")
    print(f"WINDOW|from={FROM}|to={TO}")
    print(f"COUNT|candidate_domains|{len(DOMAINS)}")

    all_results=[]
    top_errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs={ex.submit(domain_probe,d):d for d in DOMAINS}
        for fut,d in futs.items():
            try:
                all_results.append(fut.result())
            except Exception as exc:
                top_errors.append((d,type(exc).__name__,str(exc)))

    total_rows=0; total_replays=0; total_hits=0
    for domain,rows,replays,errors in sorted(all_results):
        total_rows+=len(rows); total_replays+=len(replays)
        dhits=sum(len(x[3]) for x in replays); total_hits+=dhits
        print(f"DOMAIN|name={domain}|cdx_rows={len(rows)}|replays={len(replays)}|identity_snippets={dhits}|replay_errors={len(errors)}")
        for row,status,used,hits in replays:
            print(f"REPLAY|domain={domain}|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|status={status}|replay={clean(used)}|hits={len(hits)}")
            for hit in hits:
                print(f"HIT|domain={domain}|timestamp={clean(row.get('timestamp'))}|text={hit}")
        for row,kind,msg in errors:
            print(f"ERROR|phase=replay|domain={domain}|timestamp={clean(row.get('timestamp'))}|kind={clean(kind)}|message={clean(msg)}")

    for domain,kind,msg in top_errors:
        print(f"ERROR|phase=domain|domain={domain}|kind={clean(kind)}|message={clean(msg)}")

    print(f"COUNT|cdx_rows|{total_rows}")
    print(f"COUNT|replays|{total_replays}")
    print(f"COUNT|identity_snippets|{total_hits}")
    print(f"COUNT|top_errors|{len(top_errors)}")


if __name__=="__main__":
    main()
