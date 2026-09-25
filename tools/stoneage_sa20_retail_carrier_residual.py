#!/usr/bin/env python3
"""Close the one unresolved IA query from the StoneAge 2.0 retail-carrier census.

R1's unfielded short query for 老手削暴包 exceeded the bounded response size.
R2 uses title/description/identifier fields and software-media constraints so
the residual surface can be evaluated without truncation. Metadata only.
"""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
TOKENS=("老手削暴包","石器时代2.0老手削暴包","stoneage2.0setup")

QUERIES=(
 ("veteran-title",'title:"老手削暴包" AND mediatype:software'),
 ("veteran-description",'description:"老手削暴包" AND mediatype:software'),
 ("veteran-full-title",'title:"石器时代2.0老手削暴包" AND mediatype:software'),
 ("veteran-full-description",'description:"石器时代2.0老手削暴包" AND mediatype:software'),
 ("sina-title",'title:"stoneage2.0setup" AND mediatype:software'),
 ("sina-description",'description:"stoneage2.0setup" AND mediatype:software'),
 ("sina-identifier",'identifier:*stoneage2.0setup* AND mediatype:software'),
)

def clean(v,n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def norm(v):
    return urllib.parse.unquote_plus(str(v or "")).lower().replace(" ","")

def strict(d):
    text=" ".join(str(d.get(k) or "") for k in ("identifier","title","description"))
    low=norm(text)
    return any(norm(t) in low for t in TOKENS)

def fetch(url,timeout=40,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),b

def ia_url(q,rows=100):
    p=[
      ("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
      ("fl[]","year"),("fl[]","mediatype"),("fl[]","description"),
      ("rows",str(rows)),("page","1"),("output","json")
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def docs(body):
    return tuple(((json.loads(body.decode("utf-8")).get("response") or {}).get("docs") or []))

def main():
    print("StoneAge 2.0 retail client-disc residual census — R2")
    print("SCOPE|fielded IA residual queries|老手削暴包 + Sina setup stem|metadata-only|no-payload")
    errors=[];seen={}
    for label,q in QUERIES:
        try:
            st,b=fetch(ia_url(q))
            rr=docs(b)
            print(f"QUERY|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|q={clean(q)}")
            for d in rr:
                ident=str(d.get("identifier") or "")
                seen[ident]=d
                if strict(d):
                    print(
                      f"STRICT_HIT|label={label}|identifier={clean(ident)}|title={clean(d.get('title'))}|"
                      f"date={clean(d.get('date'))}|year={clean(d.get('year'))}|"
                      f"mediatype={clean(d.get('mediatype'))}|description={clean(d.get('description'),800)}"
                    )
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    strict_rows=[d for d in seen.values() if strict(d)]
    print(f"COUNT|unique_items|{len(seen)}")
    print(f"COUNT|strict_items|{len(strict_rows)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if strict_rows:
        print("RESOLUTION|STRICT_RESIDUAL_CANDIDATE_FOUND|inspect item and filesystem before provenance promotion")
    elif errors:
        print("RESOLUTION|RESIDUAL_SURFACE_INCOMPLETE|do not close retail-carrier IA route")
    else:
        print("RESOLUTION|NO_STRICT_RESIDUAL_HIT|fielded residual IA surface is bounded with no preserved retail-client candidate")
    print("EVIDENCE_BOUNDARY|metadata search is discovery evidence only; zero rows do not prove no physical disc survives elsewhere.")

if __name__=="__main__":
    main()
