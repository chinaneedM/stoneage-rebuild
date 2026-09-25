#!/usr/bin/env python3
"""Recover Sina 2002 download-CGI neighborhood topology around aid=61620.

Unlike earlier probes, this intentionally keeps redirect status rows. The goal
is to learn historical Location/server/path templates from nearby preserved
Sina download records, then synthesize exact path candidates for the missing
StoneAge 4.0 map ZIP. No large payload is downloaded.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
CGI="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl"
TARGET_AID=61620
TARGET_FILE="shiqi4updatex_02_11_08.zip"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def clean(v,limit=5000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c >= " " and c!="\x7f").replace("|","%7C")[:limit]

def hget(headers,name):
    want=name.lower()
    for k,v in headers.items():
        if str(k).lower()==want:
            return v
    return ""

def fetch(url, timeout=50, follow=True, max_bytes=3*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    opener=urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req,timeout=timeout) as r:
            b=r.read(max_bytes+1)
            return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b
    except urllib.error.HTTPError as e:
        return int(e.code),e.geturl(),dict(e.headers.items()),e.read(max_bytes+1)

def cdx_prefix(start,end,limit=10000):
    params=[
        ("url",CGI),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",start),("to",end),("limit",str(limit)),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def cdx_exact(url,start="20020101",end="20051231"):
    params=[
        ("url",url),("matchType","exact"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",start),("to",end),("limit","100"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse_cdx(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or not obj or not isinstance(obj[0],list):
        return ()
    hdr=obj[0]
    return tuple(dict(zip(hdr,row)) for row in obj[1:] if isinstance(row,list))

def qparams(url):
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query,keep_blank_values=True))

def aid_of(url):
    try:
        v=qparams(url).get("aid","")
        return int(v) if str(v).isdigit() else None
    except Exception:
        return None

def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def location_from(row):
    r=str(row.get("redirect") or "")
    return "" if r in ("-","") else r

def candidate_urls(locations):
    out=[]
    for loc in locations:
        try:
            p=urllib.parse.urlsplit(loc)
        except Exception:
            continue
        if p.scheme not in ("http","https","ftp") or not p.netloc:
            continue
        # Same directory, exact target basename.
        directory=p.path.rsplit("/",1)[0]+"/" if "/" in p.path else "/"
        out.append(urllib.parse.urlunsplit((p.scheme,p.netloc,directory+TARGET_FILE,"","")))
        # If neighbor location is category/date-named, keep a queryless host-root guess
        # only when the filename itself is the leaf. Avoid broad brute force.
        if p.path:
            out.append(urllib.parse.urlunsplit((p.scheme,p.netloc,"/"+TARGET_FILE,"","")))
    return tuple(dict.fromkeys(out))

def main():
    print("StoneAge Sina aid=61620 neighborhood topology probe — R1")
    print("SCOPE|Wayback-download-CGI-all-statuses+nearest-aid-redirects+target-path-synthesis|no-large-payload")
    errors=[]
    all_rows=[]
    for label,start,end in (
        ("2002-oct","20021001","20021031"),
        ("2002-nov","20021101","20021130"),
        ("2002-dec","20021201","20021231"),
        ("2003-q1","20030101","20030331"),
    ):
        try:
            u=cdx_prefix(start,end)
            st,final,h,b=fetch(u,timeout=60)
            rows=parse_cdx(b)
            all_rows.extend(rows)
            status_counts={}
            for row in rows:
                sc=str(row.get("statuscode") or "")
                status_counts[sc]=status_counts.get(sc,0)+1
            print(
                f"CDX_WINDOW|label={label}|status={st}|rows={len(rows)}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}|status_counts={clean(status_counts)}|final={clean(final)}"
            )
        except Exception as exc:
            errors.append((f"cdx:{label}",type(exc).__name__,str(exc)))

    parsed=[]
    for row in all_rows:
        orig=str(row.get("original") or "")
        aid=aid_of(orig)
        if aid is None:
            continue
        qp=qparams(orig)
        parsed.append((abs(aid-TARGET_AID),aid,orig,qp,row))
    parsed.sort(key=lambda x:(x[0],x[1],str(x[4].get("timestamp") or "")))
    print(f"COUNT|rows_total|{len(all_rows)}")
    print(f"COUNT|rows_with_numeric_aid|{len(parsed)}")

    # Emit nearest distinct aid values.
    seen_aids=set(); nearest=[]
    for item in parsed:
        if item[1] in seen_aids: continue
        seen_aids.add(item[1]); nearest.append(item)
        if len(nearest)>=80: break
    for rank,(dist,aid,orig,qp,row) in enumerate(nearest,1):
        print(
            f"NEIGHBOR|rank={rank}|distance={dist}|aid={aid}|timestamp={clean(row.get('timestamp'))}|"
            f"statuscode={clean(row.get('statuscode'))}|redirect={clean(row.get('redirect'))}|"
            f"col={clean(qp.get('col'))}|filename={clean(qp.get('filename'))}|size={clean(qp.get('size'))}|"
            f"original={clean(orig)}"
        )

    # Prefer closest rows that are redirects or carry redirect metadata.
    replay_rows=[]
    used=set()
    for dist,aid,orig,qp,row in parsed:
        key=(str(row.get("timestamp") or ""),orig)
        sc=str(row.get("statuscode") or "")
        if key in used: continue
        if dist>500 and len(replay_rows)>=40: break
        if sc.startswith("3") or location_from(row) or len(replay_rows)<40:
            used.add(key); replay_rows.append((dist,aid,orig,row))
        if len(replay_rows)>=120: break

    locations=[]
    for dist,aid,orig,row in replay_rows:
        embedded=location_from(row)
        if embedded:
            locations.append(urllib.parse.urljoin(orig,embedded))
            print(f"REDIRECT_META|aid={aid}|distance={dist}|timestamp={clean(row.get('timestamp'))}|url={clean(urllib.parse.urljoin(orig,embedded))}")
        ts=str(row.get("timestamp") or "")
        if not ts: continue
        try:
            st,final,h,b=fetch(replay(ts,orig),timeout=25,follow=False,max_bytes=64*1024)
            loc=hget(h,"X-Archive-Orig-Location") or hget(h,"Location")
            print(
                f"REPLAY|aid={aid}|distance={dist}|timestamp={ts}|status={st}|"
                f"location={clean(hget(h,'Location'))}|orig_location={clean(hget(h,'X-Archive-Orig-Location'))}|"
                f"ctype={clean(hget(h,'Content-Type'))}|orig_ctype={clean(hget(h,'X-Archive-Orig-Content-Type'))}|"
                f"bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}"
            )
            if loc:
                locations.append(urllib.parse.urljoin(orig,loc))
        except Exception as exc:
            errors.append((f"replay:{aid}:{ts}",type(exc).__name__,str(exc)))

    locations=tuple(dict.fromkeys(locations))
    print(f"COUNT|historical_locations|{len(locations)}")
    hosts={}
    dirs={}
    for u in locations:
        p=urllib.parse.urlsplit(u)
        hosts[p.netloc]=hosts.get(p.netloc,0)+1
        d=p.path.rsplit("/",1)[0]+"/" if "/" in p.path else "/"
        dirs[(p.scheme,p.netloc,d)]=dirs.get((p.scheme,p.netloc,d),0)+1
    for host,n in sorted(hosts.items(),key=lambda x:(-x[1],x[0])):
        print(f"LOCATION_HOST|count={n}|host={clean(host)}")
    for (scheme,host,d),n in sorted(dirs.items(),key=lambda x:(-x[1],x[0])):
        print(f"LOCATION_DIR|count={n}|url={clean(f'{scheme}://{host}{d}')}")

    candidates=candidate_urls(locations)
    print(f"COUNT|synthesized_candidates|{len(candidates)}")
    hits=[]
    for i,u in enumerate(candidates[:100],1):
        print(f"CANDIDATE|index={i}|url={clean(u)}")
        if u.startswith("ftp:"):
            continue
        try:
            st,final,h,b=fetch(cdx_exact(u),timeout=35)
            rows=parse_cdx(b)
            print(f"CANDIDATE_CDX|index={i}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for row in rows[:20]:
                print(
                    f"CANDIDATE_HIT|index={i}|timestamp={clean(row.get('timestamp'))}|"
                    f"original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|"
                    f"mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|"
                    f"length={clean(row.get('length'))}|redirect={clean(row.get('redirect'))}"
                )
                hits.append((u,row))
        except Exception as exc:
            errors.append((f"candidate:{i}",type(exc).__name__,str(exc)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|candidate_cdx_hits|{len(hits)}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|SYNTHESIZED_TARGET_CAPTURE_FOUND|verify bytes/provenance before extraction")
    elif locations:
        print("RESOLUTION|HISTORICAL_DOWNLOAD_TOPOLOGY_RECOVERED|retain host/directory templates as new search tokens")
    elif parsed:
        print("RESOLUTION|NEIGHBOR_AIDS_RECOVERED_NO_LOCATION|CGI archive topology remains incomplete")
    else:
        print("RESOLUTION|NO_NUMERIC_AID_NEIGHBORHOOD_RECOVERED")


if __name__=="__main__":
    main()
