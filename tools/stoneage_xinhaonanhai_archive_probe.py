#!/usr/bin/env python3
"""Probe xinhaonanhai historical surfaces for the 2000/2001 StoneAge map packages.

The 2001 Sina record directly attributes its package to xinhaonanhai.  The newly
recovered 2000 Sina token is attributed to ``游民部落``; a 2002 Sina StoneAge
map page explicitly labels xinhaonanhai as ``游民部落网``, making the same domain
a bounded lineage hypothesis worth testing.  This probe enumerates archived URLs
and selected home-page captures only; it does not fetch large binary payloads.
"""
from __future__ import annotations
import hashlib, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
DOMAINS=("http://www.xinhaonanhai.com/","http://xinhaonanhai.com/")
TARGETS=("samap_1220.zip","Estoneage2.0map_1127.exe")

def clean(v,limit=5000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=45,max_bytes=4*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cdx_url(root):
    p=[
      ("url",root),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length"),
      ("from","2000"),("to","2003"),("filter","statuscode:200"),
      ("collapse","urlkey"),("limit","20000")
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def availability(root,date):
    u=AVAIL+"?"+urllib.parse.urlencode({"url":root,"timestamp":date})
    st,final,h,b=fetch(u,timeout=25)
    d=json.loads(b.decode("utf-8")); c=(d.get("archived_snapshots") or {}).get("closest") or {}
    return st,c if c.get("available") else None

def relevant_url(u):
    s=urllib.parse.unquote_plus(str(u)).lower()
    return (
      any(t.lower() in s for t in TARGETS) or
      any(x in s for x in ("stoneage","shiqi","shi_qi","1220","samap_1220","1127","2.0map","map_1127","/sa/","/stone/")) or
      (("map" in s or "ditu" in s) and any(s.endswith(ext) for ext in (".exe",".zip",".rar",".cab")))
    )

def hrefs(body,base):
    text=body.decode("gb18030","replace")
    raw=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    out=[]
    for x in raw:
        u=urllib.parse.urljoin(base,x.replace("&amp;","&"))
        if relevant_url(u): out.append(u)
    return tuple(dict.fromkeys(out))

def main():
    print("StoneAge xinhaonanhai archive probe — R2")
    print("SCOPE|contributor-domain-CDX+selected-home-replays|metadata/html-only|no-large-payload")
    print(f"TARGET|filenames={','.join(TARGETS)}|source_role=2001 direct contributor + 2000 bounded 游民部落 lineage hypothesis")
    errors=[]; rows_all=[]; candidates=[]; replays=[]
    for root in DOMAINS:
        try:
            st,final,h,b=fetch(cdx_url(root),timeout=60)
            rows=parse_cdx(b); rows_all.extend(rows)
            print(f"CDX|root={root}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for row in rows:
                orig=str(row.get("original") or "")
                if relevant_url(orig):
                    candidates.append(row)
                    print(f"URL_HIT|timestamp={clean(row.get('timestamp'))}|original={clean(orig)}|mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|length={clean(row.get('length'))}")
        except Exception as e:
            errors.append((f"cdx:{root}",type(e).__name__,str(e)))
        for date in ("20001220","20010124","20011127","20011207","20011221","20020101","20021108","20030101"):
            try:
                st,c=availability(root,date)
                print(f"AVAIL|root={root}|date={date}|status={st}|hit={int(c is not None)}|timestamp={clean(c.get('timestamp') if c else '')}|capture={clean(c.get('url') if c else '')}")
                if c and c.get("timestamp"):
                    replays.append((str(c["timestamp"]),root))
            except Exception as e:
                errors.append((f"avail:{root}:{date}",type(e).__name__,str(e)))

    for ts,root in tuple(dict.fromkeys(replays))[:20]:
        try:
            u=f"https://web.archive.org/web/{ts}id_/{root}"
            st,final,h,b=fetch(u,timeout=35,max_bytes=1024*1024)
            hs=hrefs(b,root)
            print(f"REPLAY|timestamp={ts}|root={root}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|relevant_hrefs={len(hs)}")
            for x in hs:
                print(f"REPLAY_HREF|timestamp={ts}|url={clean(x)}")
        except Exception as e:
            errors.append((f"replay:{ts}:{root}",type(e).__name__,str(e)))

    uniq={(str(r.get("timestamp","")),str(r.get("original",""))) for r in candidates}
    print(f"COUNT|cdx_rows|{len(rows_all)}")
    print(f"COUNT|relevant_url_hits|{len(uniq)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if uniq:
        print("RESOLUTION|CONTRIBUTOR_ARCHIVE_CANDIDATES_FOUND|verify exact package identity before payload recovery")
    else:
        print("RESOLUTION|NO_CONTRIBUTOR_URL_HIT_YET|domain archive remains useful only if new historical path token appears")
    print("EVIDENCE_BOUNDARY|archived contributor-domain URLs/pages are discovery evidence; no binary is promoted without exact byte verification.")

if __name__=="__main__":
    main()
