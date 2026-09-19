#!/usr/bin/env python3
"""Check exact Wayback capture status for recovered GameTime StoneAge payload URLs.

The probe uses CDX/Availability metadata first. If a 200 capture exists, it reads
at most the first 4096 replay bytes to validate ZIP/PE signatures; it never
downloads the full client payload.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
TARGETS=[
    (
        "gw9-onlStoneAge",
        "http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip",
        ["20010614","20010806","20011215","20020208"],
    ),
    (
        "gw76-stone-demo",
        "http://www.gametime.co.kr/images/Online/pds/2001/02/stone_demo.exe",
        ["20010706","20010805","20011106","20011215"],
    ),
]
MAX_PREFIX=4096


def clean(v,limit=1400):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=20,headers=None):
    h={"User-Agent":UA,"Accept":"*/*","Accept-Encoding":"identity"}
    if headers:
        h.update(headers)
    req=urllib.request.Request(url,headers=h)
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.status,r.geturl(),dict(r.headers),r.read(MAX_PREFIX)


def get_json(url,timeout=20):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.load(r)


def cdx(url):
    params=[
        ("url",url),("matchType","exact"),("from","2000"),("to","2003"),
        ("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length,redirect"),
        ("limit","100"),
    ]
    endpoint=CDX+"?"+urllib.parse.urlencode(params)
    status,final,headers,body=get(endpoint)
    text=body.decode("utf-8","replace").strip()
    if not text:
        return []
    data=json.loads(text)
    if not isinstance(data,list) or not data:
        return []
    header=data[0]
    return [
        {str(header[i]):str(row[i]) if i<len(row) else "" for i in range(len(header))}
        for row in data[1:] if isinstance(row,list)
    ]


def availability(url,date):
    params=urllib.parse.urlencode({"url":url,"timestamp":date})
    data=get_json(AVAIL+"?"+params)
    c=data.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):
        return None
    return {
        "timestamp":str(c.get("timestamp","")),
        "status":str(c.get("status","")),
        "url":str(c.get("url","")),
    }


def signature(data):
    if data.startswith(b"PK\x03\x04"):
        return "zip-local-header"
    if data.startswith(b"MZ"):
        return "pe-mz"
    if data.startswith(b"<!DOCTYPE") or data.startswith(b"<html") or data.startswith(b"<HTML"):
        return "html"
    return "other:"+data[:16].hex()


def prefix_probe(url,ts):
    replay=f"https://web.archive.org/web/{ts}id_/{url}"
    try:
        status,final,headers,body=get(
            replay,
            timeout=20,
            headers={"Range":f"bytes=0-{MAX_PREFIX-1}"},
        )
        return {
            "ok":True,"status":status,"replay":replay,"final":final,
            "content_type":headers.get("Content-Type",""),
            "content_length":headers.get("Content-Length",""),
            "content_range":headers.get("Content-Range",""),
            "bytes":len(body),
            "signature":signature(body),
            "prefix_sha256":hashlib.sha256(body).hexdigest(),
            "error":"",
        }
    except Exception as exc:
        return {
            "ok":False,"status":"","replay":replay,"final":"",
            "content_type":"","content_length":"","content_range":"",
            "bytes":0,"signature":"","prefix_sha256":"",
            "error":f"{type(exc).__name__}:{exc}",
        }


def host_variants(url):
    p=urllib.parse.urlsplit(url)
    host=p.hostname or ""
    variants=[url]
    if host.startswith("www."):
        variants.append(urllib.parse.urlunsplit((p.scheme,host[4:]+(f":{p.port}" if p.port else ""),p.path,p.query,p.fragment)))
    else:
        variants.append(urllib.parse.urlunsplit((p.scheme,"www."+host+(f":{p.port}" if p.port else ""),p.path,p.query,p.fragment)))
    return variants


def main():
    print("StoneAge GameTime exact payload capture probe — R1")
    print("SCOPE|cdx+availability+max-4096-byte-signature|no-full-payload-download")

    cdx_results=[]
    avail_results=[]
    for label,url,dates in TARGETS:
        for variant in host_variants(url):
            try:
                rows=cdx(variant)
                cdx_results.append((label,variant,rows,None))
            except Exception as exc:
                cdx_results.append((label,variant,[],f"{type(exc).__name__}:{exc}"))
        for date in dates:
            try:
                cap=availability(url,date)
                avail_results.append((label,url,date,cap,None))
            except Exception as exc:
                avail_results.append((label,url,date,None,f"{type(exc).__name__}:{exc}"))

    print(f"COUNT|cdx_queries|{len(cdx_results)}")
    print(f"COUNT|cdx_errors|{sum(bool(x[3]) for x in cdx_results)}")
    print(f"COUNT|cdx_rows|{sum(len(x[2]) for x in cdx_results)}")
    print(f"COUNT|availability_queries|{len(avail_results)}")
    print(f"COUNT|availability_errors|{sum(bool(x[4]) for x in avail_results)}")
    print(f"COUNT|availability_hits|{sum(x[3] is not None for x in avail_results)}")

    for label,url,rows,error in cdx_results:
        print(f"CDX|label={clean(label)}|url={clean(url)}|rows={len(rows)}|error={clean(error)}")
        for row in rows:
            print(
                f"CDX_ROW|label={clean(label)}|timestamp={clean(row.get('timestamp'))}|"
                f"url={clean(row.get('original'))}|status={clean(row.get('statuscode'))}|"
                f"mime={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|"
                f"length={clean(row.get('length'))}|redirect={clean(row.get('redirect'))}"
            )

    captures={}
    for label,url,date,cap,error in avail_results:
        if error:
            print(f"AVAIL_ERROR|label={clean(label)}|date={date}|url={clean(url)}|message={clean(error)}")
        elif cap is None:
            print(f"AVAIL|label={clean(label)}|date={date}|available=0|url={clean(url)}")
        else:
            print(
                f"AVAIL|label={clean(label)}|date={date}|available=1|"
                f"timestamp={clean(cap['timestamp'])}|status={clean(cap['status'])}|"
                f"url={clean(cap['url'])}"
            )
            if cap["status"]=="200" and cap["timestamp"]:
                captures[(label,url,cap["timestamp"])]=None

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        keys=list(captures)
        vals=list(ex.map(lambda k:prefix_probe(k[1],k[2]),keys))
    for key,res in zip(keys,vals):
        label,url,ts=key
        print(
            f"PREFIX|label={clean(label)}|timestamp={ts}|ok={int(res['ok'])}|"
            f"status={clean(res['status'])}|url={clean(url)}|replay={clean(res['replay'])}|"
            f"final={clean(res['final'])}|content_type={clean(res['content_type'])}|"
            f"content_length={clean(res['content_length'])}|content_range={clean(res['content_range'])}|"
            f"bytes={res['bytes']}|signature={clean(res['signature'])}|"
            f"prefix_sha256={clean(res['prefix_sha256'])}|error={clean(res['error'])}"
        )


if __name__=="__main__":
    main()
