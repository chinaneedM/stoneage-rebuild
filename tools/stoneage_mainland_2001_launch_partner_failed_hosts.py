#!/usr/bin/env python3
"""Close the three failed narrow launch-partner hosts from R2 by day-scoped CDX queries.

R2 completed NetEase/Sohu/Sina-download-control but failed:
- games.sina.com.cn (IncompleteRead)
- game.china.com (timeout)
- download.21cn.com (timeout)

R3 splits 2001-01-15..19 into one-day queries, status=200 only, preserving URL
topology while keeping archive responses bounded. Metadata only, no replay/payload.
"""
from __future__ import annotations
import hashlib,json,time,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
DAYS=("20010115","20010116","20010117","20010118","20010119")
SURFACES=(
 ("sina-games","http://games.sina.com.cn/"),
 ("china-game","http://game.china.com/"),
 ("21cn-download","http://download.21cn.com/"),
)
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"
TOKENS=(("stoneage",50),("stone-age",50),("stone_age",50),("shiqi",50),
        ("%ca%af%c6%f7",45),("waei",25),("wayi",25),("wgs",18),
        ("download",12),("/down/",10),("client",12),("demo",10),("trial",10),("test",6),("beta",6))
EXTS=(".exe",".zip",".rar",".cab",".msi",".arj",".lzh",".7z",".iso",".bin",".cue")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=6*1024*1024,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(max_bytes+1)
                if len(b)>max_bytes:raise ValueError("response-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),b
        except Exception as e:
            last=e
            if i+1<attempts:time.sleep(2)
    raise last

def cdx_url(root,day):
    p=[("url",root),("matchType","prefix"),("output","json"),("fl",FIELDS),
       ("from",day),("to",day),("filter","statuscode:200"),("limit","8000"),("collapse","urlkey")]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def low(v):return urllib.parse.unquote_plus(str(v or "")).lower()

def score(r):
    orig=str(r.get("original") or ""); red=str(r.get("redirect") or "")
    p=urllib.parse.urlsplit(low(orig)); text=p.path+"?"+p.query+" "+low(red)
    s=0;hits=[]
    for t,w in TOKENS:
        if t in text:s+=w;hits.append(t)
    if p.path.endswith(EXTS) or urllib.parse.urlsplit(low(red)).path.endswith(EXTS):
        s+=25;hits.append("binary-ext")
    return s,tuple(hits)

def main():
    print("StoneAge Mainland Jan-2001 failed launch-partner hosts — R3")
    print("PARENT|STONEAGE-MAINLAND-2001-LAUNCH-PARTNERS-RESIDUAL-R2|failed hosts only")
    print("SCOPE|3 failed narrow hosts x 5 days|status=200|CDX metadata only|no replay|no payload")
    errors=[];rows={};completed=0
    for label,root in SURFACES:
        for day in DAYS:
            try:
                st,final,b=fetch(cdx_url(root,day))
                rr=parse(b);completed+=1
                print(f"QUERY|surface={label}|day={day}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
                for r in rr:
                    k=(label,str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                    rows[k]=r
            except Exception as e:
                errors.append((label,day,type(e).__name__,str(e)))
                print(f"QUERY_ERROR|surface={label}|day={day}|kind={type(e).__name__}|message={clean(e)}")

    candidates=[]
    for (label,ts,orig,digest),r in sorted(rows.items()):
        sc,h=score(r)
        if sc>0:
            candidates.append((sc,label,h,r))
    candidates.sort(key=lambda x:(-x[0],x[1],str(x[3].get("timestamp") or "")))
    for sc,label,h,r in candidates[:300]:
        print(f"CANDIDATE|surface={label}|score={sc}|tokens={clean(','.join(h))}|timestamp={clean(r.get('timestamp'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|original={clean(r.get('original'))}")

    for label,day,k,m in errors:
        print(f"ERROR|surface={label}|day={day}|kind={clean(k)}|message={clean(m)}")
    stone=[x for x in candidates if any(t in x[2] for t in ("stoneage","stone-age","stone_age","shiqi","%ca%af%c6%f7"))]
    bins=[x for x in candidates if "binary-ext" in x[2]]
    print(f"COUNT|queries_planned={len(SURFACES)*len(DAYS)}")
    print(f"COUNT|queries_completed={completed}")
    print(f"COUNT|unique_rows={len(rows)}")
    print(f"COUNT|candidate_rows={len(candidates)}")
    print(f"COUNT|stone_rows={len(stone)}")
    print(f"COUNT|binary_rows={len(bins)}")
    print(f"COUNT|errors={len(errors)}")
    if stone or bins:
        print("RESOLUTION|FAILED_HOST_EXACT_ROUTE_FOUND|replay only exact candidate URLs next")
    elif errors:
        print("RESOLUTION|FAILED_HOST_RESIDUAL_PARTIAL|retain only failed day/surface pairs as open")
    else:
        print("RESOLUTION|FAILED_NARROW_HOSTS_BOUNDED_FOR_HTTP200_URLS|no qualifying StoneAge URL token in tested launch days")
    print("EVIDENCE_BOUNDARY|HTTP-200 URL census does not cover unindexed or redirect-only objects and does not authenticate client bytes.")

if __name__=="__main__":main()
