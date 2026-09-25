#!/usr/bin/env python3
"""Recover the exact Sina 2002-11-08 StoneAge 4.0 map-patch download href
and probe Wayback for the CGI response/redirect target.

The key improvement over R1 is using the complete href still exposed by the
surviving source page, including col/filename/size/title/author parameters.
No patch payload is downloaded.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
SOURCE="https://games.sina.com.cn/downgames/updatex/11084599.shtml"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
TARGET_FILE="shiqi4updatex_02_11_08.zip"
AID="61620"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def clean(v,limit=5000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c >= " " and c != "\x7f").replace("|","%7C")[:limit]

def hget(headers,name):
    want=name.lower()
    for k,v in headers.items():
        if str(k).lower()==want:
            return v
    return ""

def fetch(url, timeout=40, follow=True, max_bytes=2*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"text/html,application/json,text/plain,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    opener=urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req,timeout=timeout) as r:
            body=r.read(max_bytes+1)
            return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),body
    except urllib.error.HTTPError as e:
        body=e.read(max_bytes+1)
        return int(e.code),e.geturl(),dict(e.headers.items()),body

def source_hrefs(body):
    # Current surviving Sina page is legacy Chinese HTML. Extract from bytes first
    # so query octets survive character-decoding ambiguity.
    text=body.decode("gb18030","replace")
    hrefs=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    out=[]
    for href in hrefs:
        href=html.unescape(href)
        low=urllib.parse.unquote_plus(href).lower()
        if f"aid={AID}" in low and TARGET_FILE.lower() in low:
            out.append(urllib.parse.urljoin(SOURCE,href))
    return tuple(dict.fromkeys(out))

def cdx_url(target, match="exact", start="20021101", end="20051231"):
    params=[
        ("url",target),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",start),("to",end),("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def parse_cdx(body):
    data=json.loads(body.decode("utf-8"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    hdr=data[0]
    return tuple(dict(zip(hdr,row)) for row in data[1:] if isinstance(row,list))

def availability(target,date):
    u=AVAIL+"?"+urllib.parse.urlencode({"url":target,"timestamp":date})
    st,final,h,b=fetch(u,timeout=30)
    obj=json.loads(b.decode("utf-8"))
    c=(obj.get("archived_snapshots") or {}).get("closest") or {}
    return st,final,c if c.get("available") else None

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def emit_response(label,status,final,headers,body):
    print(
        f"{label}|status={status}|final={clean(final)}|bytes={len(body)}|"
        f"sha256={hashlib.sha256(body).hexdigest()}|"
        f"location={clean(hget(headers,'Location'))}|"
        f"orig_location={clean(hget(headers,'X-Archive-Orig-Location'))}|"
        f"content_type={clean(hget(headers,'Content-Type'))}|"
        f"orig_content_type={clean(hget(headers,'X-Archive-Orig-Content-Type'))}|"
        f"content_length={clean(hget(headers,'Content-Length'))}|"
        f"orig_content_length={clean(hget(headers,'X-Archive-Orig-Content-Length'))}|"
        f"memento={clean(hget(headers,'Memento-Datetime'))}"
    )

def main():
    print("StoneAge 4.0 exact Sina href / redirect recovery — R2")
    print("SCOPE|surviving-source-exact-href+Wayback-exact-CDX+redirect-headers|no-payload")
    errors=[]
    hrefs=()
    try:
        st,final,h,b=fetch(SOURCE,timeout=30)
        print(f"SOURCE|status={st}|final={clean(final)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        hrefs=source_hrefs(b)
        print(f"COUNT|source_exact_hrefs|{len(hrefs)}")
        for i,u in enumerate(hrefs,1):
            p=urllib.parse.urlsplit(u)
            q=urllib.parse.parse_qsl(p.query,keep_blank_values=True)
            print(f"HREF|index={i}|url={clean(u)}")
            for k,v in q:
                print(f"HREF_PARAM|index={i}|key={clean(k)}|value={clean(v)}")
    except Exception as exc:
        errors.append(("source",type(exc).__name__,str(exc)))

    candidates=[]
    for u in hrefs:
        candidates.append(u)
        p=urllib.parse.urlsplit(u)
        if p.scheme=="https":
            candidates.append(urllib.parse.urlunsplit(("http",p.netloc,p.path,p.query,p.fragment)))
        elif p.scheme=="http":
            candidates.append(urllib.parse.urlunsplit(("https",p.netloc,p.path,p.query,p.fragment)))
    candidates=tuple(dict.fromkeys(candidates))

    # Probe current CGI only for redirect metadata. Never read beyond tiny response.
    for i,u in enumerate(candidates,1):
        try:
            st,final,h,b=fetch(u,timeout=15,follow=False,max_bytes=64*1024)
            emit_response(f"LIVE_CGI|index={i}",st,final,h,b)
        except Exception as exc:
            errors.append((f"live:{i}",type(exc).__name__,str(exc)))

    all_rows=[]
    for i,u in enumerate(candidates,1):
        for match in ("exact","prefix"):
            try:
                cu=cdx_url(u,match)
                st,final,h,b=fetch(cu,timeout=50)
                rows=parse_cdx(b)
                all_rows.extend(rows)
                print(
                    f"CDX|index={i}|match={match}|status={st}|rows={len(rows)}|"
                    f"bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}"
                )
                for row in rows[:100]:
                    print(
                        f"CDX_ROW|index={i}|match={match}|timestamp={clean(row.get('timestamp'))}|"
                        f"original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|"
                        f"mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|"
                        f"length={clean(row.get('length'))}|redirect={clean(row.get('redirect'))}"
                    )
            except Exception as exc:
                errors.append((f"cdx:{i}:{match}",type(exc).__name__,str(exc)))

    # Availability around publication and later hub dates.
    avail=[]
    for i,u in enumerate(candidates,1):
        for date in ("20021108","20021109","20021115","20021201","20030116","20030403","20030610"):
            try:
                st,final,c=availability(u,date)
                print(
                    f"AVAIL|index={i}|date={date}|status={st}|hit={int(c is not None)}|"
                    f"timestamp={clean(c.get('timestamp') if c else '')}|"
                    f"capture={clean(c.get('url') if c else '')}|"
                    f"http_status={clean(c.get('status') if c else '')}"
                )
                if c and c.get("timestamp"):
                    avail.append((str(c["timestamp"]),u))
            except Exception as exc:
                errors.append((f"avail:{i}:{date}",type(exc).__name__,str(exc)))

    # Replay every distinct exact row / availability timestamp without following
    # redirect so the historical Location header can surface.
    replay_targets=[]
    for row in all_rows:
        ts=str(row.get("timestamp") or "")
        orig=str(row.get("original") or "")
        if ts and orig:
            replay_targets.append((ts,orig))
    replay_targets.extend(avail)
    replay_targets=tuple(dict.fromkeys(replay_targets))[:60]
    locations=[]
    for ts,orig in replay_targets:
        try:
            ru=replay_url(ts,orig)
            st,final,h,b=fetch(ru,timeout=35,follow=False,max_bytes=128*1024)
            emit_response(f"REPLAY|timestamp={ts}",st,final,h,b)
            loc=hget(h,"X-Archive-Orig-Location") or hget(h,"Location")
            if loc:
                locations.append(urllib.parse.urljoin(orig,loc))
        except Exception as exc:
            errors.append((f"replay:{ts}",type(exc).__name__,str(exc)))

    locations=tuple(dict.fromkeys(locations))
    print(f"COUNT|cdx_rows_total|{len(all_rows)}")
    print(f"COUNT|replay_targets|{len(replay_targets)}")
    print(f"COUNT|historical_locations|{len(locations)}")
    for i,u in enumerate(locations,1):
        print(f"HISTORICAL_LOCATION|index={i}|url={clean(u)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if locations:
        print("RESOLUTION|HISTORICAL_REDIRECT_TARGET_RECOVERED|probe exact target preservation next")
    elif all_rows or avail:
        print("RESOLUTION|CGI_CAPTURE_WITHOUT_REDIRECT_TARGET|inspect archived body/response metadata next")
    elif hrefs:
        print("RESOLUTION|EXACT_HREF_RECOVERED_NO_ARCHIVED_CGI_YET|retain full query as new recovery token")
    else:
        print("RESOLUTION|SOURCE_HREF_NOT_RECOVERED")


if __name__=="__main__":
    main()
