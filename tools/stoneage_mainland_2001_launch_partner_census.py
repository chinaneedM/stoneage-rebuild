#!/usr/bin/env python3
"""Census Jan-2001 StoneAge launch-partner archive surfaces.

Contemporaneous Sina coverage states that Mainland StoneAge launch promotion
was coordinated with ten Chinese web portals, with comprehensive StoneAge
coverage planned for 2001-01-16..18. This probe uses the confirmed portal
domains that can be identified confidently and performs a narrow CDX-only
census around that window.

No archived page body or software payload is fetched. URL/path tokens are
ranked only to recover exact historical routes for later bounded replay.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20010115"
TO="20010119"
LIMIT="30000"
FIELDS="timestamp,original,statuscode,mimetype,digest,length,redirect"

# Portal identities explicitly named in contemporaneous launch coverage.
# The historical domain mapping is restricted to well-established domains.
PORTALS=(
    ("sina","sina.com.cn"),
    ("netease","163.com"),
    ("sohu","sohu.com"),
    ("china","china.com"),
    ("elong","elong.com"),
    ("21cn","21cn.com"),
    ("enet","enet.com.cn"),
    ("21vianet","21vianet.com"),
    ("yesky","yesky.com"),
)

TOKENS=(
    ("stoneage",40),
    ("stone-age",40),
    ("stone_age",40),
    ("shiqi",40),
    ("shiqi",40),
    ("waei",25),
    ("wayi",25),
    ("wgs",18),
    ("onlinegame",12),
    ("online-game",12),
    ("/online/",8),
    ("/game/",6),
    ("/games/",6),
    ("download",10),
    ("/down/",8),
    ("client",10),
    ("demo",8),
    ("trial",8),
    ("test",5),
    ("beta",5),
    ("rpg",3),
)
BINARY_EXTS=(".exe",".zip",".rar",".cab",".msi",".arj",".lzh",".7z",".iso",".bin",".cue")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=60,max_bytes=16*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(domain):
    q=[
        ("url",domain),("matchType","domain"),("output","json"),("fl",FIELDS),
        ("from",FROM),("to",TO),("limit",LIMIT),("collapse","urlkey"),
    ]
    return CDX+"?"+urllib.parse.urlencode(q)

def parse(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,row)) for row in obj[1:] if isinstance(row,list))

def decoded(v):
    return urllib.parse.unquote_plus(str(v or "")).lower()

def is_binary(v):
    path=urllib.parse.urlsplit(decoded(v)).path
    return path.endswith(BINARY_EXTS)

def score(row):
    orig=str(row.get("original") or "")
    redir=str(row.get("redirect") or "")
    p=urllib.parse.urlsplit(decoded(orig))
    text=p.path+(" ?"+p.query if p.query else "")+" "+decoded(redir)
    s=0; hits=[]
    for token,w in TOKENS:
        if token in text:
            s+=w; hits.append(token)
    if is_binary(orig) or is_binary(redir):
        s+=20; hits.append("binary-ext")
    mt=str(row.get("mimetype") or "").lower()
    if "html" in mt:
        s+=1
    return s,tuple(hits)

def main():
    print("StoneAge Mainland Jan-2001 launch-partner CDX census — R1")
    print(f"SCOPE|confirmed launch-partner domains|window={FROM}..{TO}|CDX metadata only|collapse=urlkey|no replay|no payload")
    print("SOURCE_ANCHOR|contemporaneous Sina launch report names ten cooperating portals and Jan-16..18 coordinated StoneAge coverage")
    print("DOMAIN_BOUNDARY|Pulse/M-WEB is omitted here because its exact historical domain is not asserted without a source-derived mapping")

    errors=[]
    rows_by_portal={}

    def run(label,domain):
        try:
            st,final,b=fetch(cdx_url(domain),timeout=75)
            rr=parse(b)
            return label,domain,st,final,b,rr,None
        except Exception as e:
            return label,domain,None,"",b"",(),(type(e).__name__,str(e))

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results=[f.result() for f in concurrent.futures.as_completed([ex.submit(run,*p) for p in PORTALS])]

    all_candidates=[]
    for label,domain,st,final,b,rr,err in sorted(results):
        if err:
            errors.append((label,err[0],err[1]))
            print(f"QUERY_ERROR|portal={label}|domain={domain}|kind={clean(err[0])}|message={clean(err[1])}")
            continue
        rows_by_portal[label]=rr
        print(f"QUERY|portal={label}|domain={domain}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        cand=[]
        for row in rr:
            sc,hits=score(row)
            if sc>0:
                cand.append((sc,hits,row))
                all_candidates.append((sc,label,hits,row))
        cand.sort(key=lambda x:(-x[0],str(x[2].get("timestamp") or ""),str(x[2].get("original") or "")))
        print(f"COUNT_PORTAL|portal={label}|rows={len(rr)}|candidates={len(cand)}")
        for sc,hits,row in cand[:80]:
            print(
                "CANDIDATE|portal={}|score={}|tokens={}|timestamp={}|status={}|mime={}|length={}|digest={}|redirect={}|original={}".format(
                    label,sc,clean(",".join(hits)),clean(row.get("timestamp")),
                    clean(row.get("statuscode")),clean(row.get("mimetype")),clean(row.get("length")),
                    clean(row.get("digest")),clean(row.get("redirect")),clean(row.get("original"))
                )
            )

    for label,kind,msg in errors:
        print(f"ERROR|portal={clean(label)}|kind={clean(kind)}|message={clean(msg)}")

    strong=[x for x in all_candidates if x[0]>=20]
    stone=[x for x in all_candidates if any(t in x[2] for t in ("stoneage","stone-age","stone_age","shiqi","shiqi"))]
    binaries=[x for x in all_candidates if "binary-ext" in x[2]]
    print(f"COUNT|portals={len(PORTALS)}")
    print(f"COUNT|queries_completed={len(rows_by_portal)}")
    print(f"COUNT|total_rows={sum(len(v) for v in rows_by_portal.values())}")
    print(f"COUNT|candidate_rows={len(all_candidates)}")
    print(f"COUNT|strong_rows={len(strong)}")
    print(f"COUNT|stone_token_rows={len(stone)}")
    print(f"COUNT|binary_rows={len(binaries)}")
    print(f"COUNT|errors={len(errors)}")

    if stone or binaries:
        print("RESOLUTION|LAUNCH_PARTNER_EXACT_ROUTE_FOUND|replay only exact source-derived candidate URLs next")
    elif strong:
        print("RESOLUTION|LAUNCH_PARTNER_STRONG_ROUTE_SIGNAL|classify high-score exact URLs before any broader search")
    elif rows_by_portal:
        print("RESOLUTION|LAUNCH_PARTNER_WINDOW_CENSUSED_NO_EXACT_STONE_TOKEN|use portal-specific game-route tokens only if newly source-derived")
    elif errors:
        print("RESOLUTION|LAUNCH_PARTNER_CENSUS_PARTIAL|retry failed domains only")
    else:
        print("RESOLUTION|LAUNCH_PARTNER_CENSUS_EMPTY|switch to physical-media/carrier evidence")

    print("EVIDENCE_BOUNDARY|Portal cooperation and archived URL topology do not identify client bytes. No archived body or software payload is fetched.")

if __name__=="__main__":
    main()
