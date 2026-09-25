#!/usr/bin/env python3
"""Bounded census of Sina's late-2001 download-server directory families.

A 2001-11-20 archived CGI replay exposes:
  http://202.106.184.242/tools_1004/bleem16b_0822.zip

This probe tests whether the same contemporaneous host has archived map_* or
demo_* directory families, and whether exact StoneAge target filenames appear
anywhere on that host. Metadata only; no payload bodies.
"""
from __future__ import annotations
import hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
HOSTS=(
    "202.106.184.242",
    "202.106.184.193",
    "202.106.185.221",
)
TARGETS=("Estoneage2.0map_1127.exe","stoneage2.0setup.exe")
FILTERS=(
    ("map-dir",r".*/map_[0-9]+/.*"),
    ("demo-dir",r".*/demo_[0-9]+/.*"),
    ("estoneage",r".*[Ee]stoneage.*"),
    ("stoneage",r".*stoneage.*"),
)

def clean(v,n=8000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=60,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cdx_url(host,pattern,start="2001",end="2002"):
    p=[
      ("url",f"http://{host}/"),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from",start),("to",end),("filter",f"original:{pattern}"),
      ("collapse","urlkey"),("limit","10000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def directory_of(url):
    try:
        p=urllib.parse.urlsplit(str(url))
        return p.path.rsplit("/",1)[0]+"/"
    except Exception:return ""

def is_target(url):
    low=urllib.parse.unquote_plus(str(url)).lower()
    return any(t.lower() in low for t in TARGETS)

def main():
    print("StoneAge 2001 Sina server-family probe — R1")
    print("SCOPE|late-2001 candidate Sina download IPs + map/demo directory-family CDX metadata|no-payload")
    errors=[];target_rows=[];dirs={}
    for host in HOSTS:
        for label,pat in FILTERS:
            try:
                st,final,h,b=fetch(cdx_url(host,pat),timeout=65)
                rows=parse_cdx(b)
                print(f"CDX|host={host}|label={label}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
                for r in rows[:1000]:
                    u=str(r.get("original") or "")
                    directory=directory_of(u)
                    if label in ("map-dir","demo-dir") and directory:
                        key=(host,directory)
                        dirs[key]=dirs.get(key,0)+1
                    if is_target(u):
                        target_rows.append(r)
                        print(f"TARGET_ROW|host={host}|label={label}|timestamp={clean(r.get('timestamp'))}|original={clean(u)}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
            except Exception as e:
                errors.append((f"{host}:{label}",type(e).__name__,str(e)))
    for (host,directory),count in sorted(dirs.items(),key=lambda kv:(kv[0][0],kv[0][1])):
        print(f"DIRECTORY|host={host}|path={clean(directory)}|rows={count}")
    # Only after a directory family is independently observed, test exact target
    # filenames inside that observed directory.
    tested=set()
    for (host,directory),count in sorted(dirs.items()):
        low=directory.lower()
        role="map" if "/map_" in low else ("demo" if "/demo_" in low else "")
        if not role:continue
        filename=TARGETS[0] if role=="map" else TARGETS[1]
        u=f"http://{host}{directory}{filename}"
        if u in tested:continue
        tested.add(u)
        try:
            p=[
              ("url",u),("matchType","exact"),("output","json"),
              ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
              ("from","2001"),("to","2006"),("limit","100"),
            ]
            st,final,h,b=fetch(CDX+"?"+urllib.parse.urlencode(p),timeout=45)
            rows=parse_cdx(b)
            print(f"SYNTH|role={role}|url={clean(u)}|status={st}|rows={len(rows)}|directory_evidence_rows={count}")
            for r in rows:
                print(f"SYNTH_ROW|role={role}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
        except Exception as e:
            errors.append((f"synth:{u}",type(e).__name__,str(e)))
    print(f"COUNT|directory_families|{len(dirs)}")
    print(f"COUNT|target_rows|{len(target_rows)}")
    print(f"COUNT|synthesized_exact_urls|{len(tested)}")
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if target_rows:
        print("RESOLUTION|TARGET_FILENAME_ON_CANDIDATE_HOST|verify exact archived object before any byte claim")
    elif dirs:
        print("RESOLUTION|SERVER_DIRECTORY_FAMILIES_RECOVERED|use observed map/demo directories only as bounded target hypotheses")
    else:
        print("RESOLUTION|NO_MAP_DEMO_DIRECTORY_FAMILY|candidate late-2001 server hosts expose no tested category directories")
    print("EVIDENCE_BOUNDARY|directory-family coexistence does not prove a target package used that directory; exact target rows or recovered bytes are required.")

if __name__=="__main__":
    main()
