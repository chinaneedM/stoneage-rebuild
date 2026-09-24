#!/usr/bin/env python3
"""Recover historical Sina download-link variants for StoneAge 4.0 map patch aid=61620.

The surviving 2002-11-08 download-center record exposes aid=61620 and the
source-derived filename. Earlier probes queried one exact CGI URL or broad
domains. This probe narrows Wayback to the source record and the exact CGI
path, allowing query-parameter order/encoding variants to surface. Metadata and
archived HTML only; no patch payload is downloaded.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
SOURCE_URL="http://games.sina.com.cn/downgames/updatex/11084599.shtml"
CGI_PREFIX="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl"
AID="61620"
BASENAME="shiqi4updatex_02_11_08.zip"
WINDOWS=(
    ("2002-post","20021108","20021231"),
    ("2003","20030101","20031231"),
    ("2004","20040101","20041231"),
    ("2005","20050101","20051231"),
)

def clean(value,limit=2400):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch_bytes(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return int(getattr(response,"status",response.getcode())),response.geturl(),response.read()

def parse_cdx(body):
    data=json.loads(body.decode("utf-8"))
    if not isinstance(data,list) or not data or not isinstance(data[0],list):
        return ()
    header=data[0]
    return tuple(dict(zip(header,row)) for row in data[1:] if isinstance(row,list))

def availability(date):
    endpoint=AVAIL+"?"+urllib.parse.urlencode({"url":SOURCE_URL,"timestamp":date})
    status,final,body=fetch_bytes(endpoint,timeout=25)
    data=json.loads(body.decode("utf-8"))
    closest=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return status,final,None
    return status,final,{
        "timestamp":str(closest.get("timestamp") or ""),
        "url":str(closest.get("url") or ""),
        "status":str(closest.get("status") or ""),
    }

def source_cdx_url():
    params=[
        ("url",SOURCE_URL),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from","2002"),("to","2005"),("filter","statuscode:200"),
        ("collapse","digest"),("limit","100"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def cgi_cdx_url(start,end):
    params=[
        ("url",CGI_PREFIX),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from",start),("to",end),("filter","statuscode:200"),
        ("collapse","urlkey"),("limit","2000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def relevant_cgi(rows):
    out=[]
    for row in rows:
        original=str(row.get("original") or "")
        low=urllib.parse.unquote_plus(original).lower()
        if f"aid={AID}" in low or BASENAME.lower() in low:
            out.append(row)
    return tuple(out)

def archived_html_url(timestamp,original):
    return f"https://web.archive.org/web/{timestamp}id_/{original}"

def href_candidates(html_bytes):
    text=html_bytes.decode("gb18030","replace")
    hrefs=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    out=[]
    for href in hrefs:
        decoded=urllib.parse.unquote_plus(href).lower()
        if f"aid={AID}" in decoded or BASENAME.lower() in decoded:
            out.append(href)
    return tuple(dict.fromkeys(out))

def main():
    print("StoneAge 4.0 Sina aid=61620 historical-link probe — R1")
    print("SCOPE|source-record-captures+exact-CGI-prefix|parameter-variant-recovery|archived-html+metadata-only|no-payload")
    print(f"TARGET|source={SOURCE_URL}|cgi_prefix={CGI_PREFIX}|aid={AID}|basename={BASENAME}")

    errors=[]
    source_rows=()
    source_hrefs=[]

    try:
        url=source_cdx_url()
        status,final,body=fetch_bytes(url)
        source_rows=parse_cdx(body)
        print(
            f"SOURCE_CDX|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"rows={len(source_rows)}|final={clean(final)}"
        )
        for row in source_rows[:20]:
            ts=str(row.get("timestamp") or "")
            original=str(row.get("original") or SOURCE_URL)
            print(
                f"SOURCE_CAPTURE|timestamp={clean(ts)}|original={clean(original)}|"
                f"digest={clean(row.get('digest'))}|length={clean(row.get('length'))}"
            )
            if not ts:
                continue
            try:
                replay=archived_html_url(ts,original)
                rstatus,rfinal,rbody=fetch_bytes(replay,timeout=30)
                hrefs=href_candidates(rbody)
                print(
                    f"SOURCE_REPLAY|timestamp={clean(ts)}|status={rstatus}|bytes={len(rbody)}|"
                    f"sha256={hashlib.sha256(rbody).hexdigest()}|candidate_hrefs={len(hrefs)}|final={clean(rfinal)}"
                )
                for href in hrefs:
                    source_hrefs.append((ts,href))
                    print(f"SOURCE_HREF|timestamp={clean(ts)}|href={clean(href)}")
            except Exception as exc:
                errors.append((f"source-replay:{ts}",type(exc).__name__,str(exc)))
    except Exception as exc:
        errors.append(("source-cdx",type(exc).__name__,str(exc)))

    availability_hits={}
    for date in ("20021108","20021201","20030101","20040101"):
        try:
            astatus,afinal,closest=availability(date)
            print(
                f"SOURCE_AVAIL|date={date}|status={astatus}|hit={int(closest is not None)}|"
                f"timestamp={clean(closest['timestamp'] if closest else '')}|"
                f"capture={clean(closest['url'] if closest else '')}|final={clean(afinal)}"
            )
            if closest and closest["timestamp"]:
                availability_hits[(closest["timestamp"],closest["url"])]=closest
        except Exception as exc:
            errors.append((f"source-availability:{date}",type(exc).__name__,str(exc)))

    for (ts,capture),closest in sorted(availability_hits.items()):
        try:
            replay=archived_html_url(ts,SOURCE_URL)
            rstatus,rfinal,rbody=fetch_bytes(replay,timeout=30)
            hrefs=href_candidates(rbody)
            print(
                f"SOURCE_AVAIL_REPLAY|timestamp={clean(ts)}|status={rstatus}|bytes={len(rbody)}|"
                f"sha256={hashlib.sha256(rbody).hexdigest()}|candidate_hrefs={len(hrefs)}|final={clean(rfinal)}"
            )
            for href in hrefs:
                source_hrefs.append((ts,href))
                print(f"SOURCE_HREF|timestamp={clean(ts)}|href={clean(href)}")
        except Exception as exc:
            errors.append((f"source-availability-replay:{ts}",type(exc).__name__,str(exc)))

    cgi_hits=[]
    for label,start,end in WINDOWS:
        try:
            url=cgi_cdx_url(start,end)
            status,final,body=fetch_bytes(url,timeout=45)
            rows=parse_cdx(body)
            hits=relevant_cgi(rows)
            cgi_hits.extend((label,row) for row in hits)
            print(
                f"CGI_CDX|window={label}|from={start}|to={end}|status={status}|bytes={len(body)}|"
                f"sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|relevant={len(hits)}|final={clean(final)}"
            )
            for row in hits:
                print(
                    f"CGI_HIT|window={label}|timestamp={clean(row.get('timestamp'))}|"
                    f"original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|"
                    f"mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|"
                    f"length={clean(row.get('length'))}"
                )
        except Exception as exc:
            errors.append((f"cgi-cdx:{label}",type(exc).__name__,str(exc)))

    for scope,kind,message in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(message)}")

    unique_hrefs=tuple(dict.fromkeys(href for _,href in source_hrefs))
    unique_cgi=tuple(dict.fromkeys(str(row.get("original") or "") for _,row in cgi_hits))
    print(f"COUNT|source_captures|{len(source_rows)}")
    print(f"COUNT|source_availability_captures|{len(availability_hits)}")
    print(f"COUNT|source_candidate_hrefs|{len(unique_hrefs)}")
    print(f"COUNT|cgi_relevant_urls|{len(unique_cgi)}")
    print(f"COUNT|errors|{len(errors)}")
    if unique_cgi:
        print("RESOLUTION|SINA_CGI_VARIANT_CAPTURE_FOUND|verify replay/redirect identity before any payload recovery")
    elif unique_hrefs:
        print("RESOLUTION|HISTORICAL_SOURCE_HREF_RECOVERED|use archived href variants for next exact archive probe")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|one or more narrowly scoped Wayback surfaces unavailable")
    else:
        print("RESOLUTION|NO_VARIANT_CAPTURE|source captures and exact CGI-prefix index expose no recoverable aid/filename variant")

if __name__=="__main__":
    main()
