#!/usr/bin/env python3
"""Residual census of narrow game hosts from Jan-2001 StoneAge launch partners.

R1 queried whole portal domains and 8/9 requests failed (mostly Wayback 504),
so its no-token resolution is explicitly not a negative result. R2 uses only
narrow game/download hosts supported independently by project evidence or
contemporaneous/near-contemporaneous web evidence.

Window stays 2001-01-15..19. CDX metadata only; no page or payload replay.
"""
from __future__ import annotations
import concurrent.futures, hashlib, json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20010115"; TO="20010119"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"

SURFACES=(
    ("sina-games","http://games.sina.com.cn/","prefix","repo-confirmed historical game host"),
    ("sina-games1","http://games1.sina.com.cn/","prefix","repo-confirmed historical download CGI host"),
    ("china-game","http://game.china.com/","prefix","repo-confirmed historical game host"),
    ("sohu-games","http://games.sohu.com/","prefix","documented active game host in Apr-2001"),
    ("netease-game","http://game.163.com/","prefix","NetEase game host tied to 2001 game division"),
    ("21cn-download","http://download.21cn.com/","prefix","repo-confirmed historical download host"),
)
TOKENS=(
    ("stoneage",50),("stone-age",50),("stone_age",50),("shiqi",50),
    ("%ca%af%c6%f7",45),("waei",25),("wayi",25),("wgs",18),
    ("download",12),("/down/",10),("client",12),("demo",10),("trial",10),
    ("test",6),("beta",6),("online",3),
)
EXTS=(".exe",".zip",".rar",".cab",".msi",".arj",".lzh",".7z",".iso",".bin",".cue")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=50,max_bytes=12*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(root,kind):
    p=[("url",root),("matchType",kind),("output","json"),("fl",FIELDS),
       ("from",FROM),("to",TO),("limit","15000"),("collapse","urlkey")]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse(b):
    o=json.loads(b.decode("utf-8"))
    if not isinstance(o,list) or len(o)<2:return ()
    h=o[0]
    return tuple(dict(zip(h,r)) for r in o[1:] if isinstance(r,list))

def low(v):return urllib.parse.unquote_plus(str(v or "")).lower()

def score(r):
    orig=str(r.get("original") or ""); red=str(r.get("redirect") or "")
    p=urllib.parse.urlsplit(low(orig))
    text=p.path+"?"+p.query+" "+low(red)
    s=0;hits=[]
    for t,w in TOKENS:
        if t in text:s+=w;hits.append(t)
    if p.path.endswith(EXTS) or urllib.parse.urlsplit(low(red)).path.endswith(EXTS):
        s+=25;hits.append("binary-ext")
    return s,tuple(hits)

def main():
    print("StoneAge Mainland Jan-2001 launch-partner narrow-host residual — R2")
    print(f"PARENT|STONEAGE-MAINLAND-2001-LAUNCH-PARTNERS-R1|R1 had 8/9 failed broad-domain queries")
    print(f"SCOPE|narrow game/download hosts|window={FROM}..{TO}|CDX metadata only|no replay|no payload")
    errors=[];results={};candidates=[]

    def one(spec):
        label,root,kind,basis=spec
        try:
            st,final,b=fetch(cdx_url(root,kind),timeout=60)
            return label,root,kind,basis,st,final,b,parse(b),None
        except Exception as e:
            return label,root,kind,basis,None,"",b"",(),(type(e).__name__,str(e))

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        rr=[f.result() for f in concurrent.futures.as_completed([ex.submit(one,s) for s in SURFACES])]

    for label,root,kind,basis,st,final,b,rows,err in sorted(rr):
        if err:
            errors.append((label,err[0],err[1]))
            print(f"QUERY_ERROR|surface={label}|basis={clean(basis)}|kind={clean(err[0])}|message={clean(err[1])}")
            continue
        results[label]=rows
        print(f"QUERY|surface={label}|basis={clean(basis)}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        local=[]
        for r in rows:
            sc,h=score(r)
            if sc>0:
                local.append((sc,h,r));candidates.append((sc,label,h,r))
        local.sort(key=lambda x:(-x[0],str(x[2].get("timestamp") or ""),str(x[2].get("original") or "")))
        print(f"COUNT_SURFACE|surface={label}|rows={len(rows)}|candidates={len(local)}")
        for sc,h,r in local[:100]:
            print(f"CANDIDATE|surface={label}|score={sc}|tokens={clean(','.join(h))}|timestamp={clean(r.get('timestamp'))}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}|original={clean(r.get('original'))}")

    for label,k,m in errors:
        print(f"ERROR|surface={label}|kind={clean(k)}|message={clean(m)}")
    strong=[x for x in candidates if x[0]>=25]
    stone=[x for x in candidates if any(t in x[2] for t in ("stoneage","stone-age","stone_age","shiqi","%ca%af%c6%f7"))]
    bins=[x for x in candidates if "binary-ext" in x[2]]
    print(f"COUNT|surfaces={len(SURFACES)}")
    print(f"COUNT|completed={len(results)}")
    print(f"COUNT|failed={len(errors)}")
    print(f"COUNT|rows={sum(len(v) for v in results.values())}")
    print(f"COUNT|candidate_rows={len(candidates)}")
    print(f"COUNT|strong_rows={len(strong)}")
    print(f"COUNT|stone_rows={len(stone)}")
    print(f"COUNT|binary_rows={len(bins)}")
    if stone or bins:
        print("RESOLUTION|NARROW_LAUNCH_PARTNER_EXACT_ROUTE_FOUND|replay only exact candidate URLs next")
    elif errors:
        print("RESOLUTION|NARROW_LAUNCH_PARTNER_PARTIAL|do not infer absence; retry failed narrow hosts or use newly source-derived paths")
    elif results:
        print("RESOLUTION|NARROW_LAUNCH_PARTNER_HOSTS_BOUNDED_IN_WINDOW|no qualifying StoneAge URL token in completed narrow hosts")
    else:
        print("RESOLUTION|NARROW_LAUNCH_PARTNER_NO_COMPLETED_SURFACE")
    print("CORRECTION|R1 no-token resolution is superseded by this residual classification; broad-domain failures were not negative evidence")
    print("EVIDENCE_BOUNDARY|Archived URL topology cannot authenticate client bytes; no page or binary body is fetched.")

if __name__=="__main__":main()
