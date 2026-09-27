#!/usr/bin/env python3
"""Recover 17173 StoneAge download-page routing around the Mainland launch window.

A surviving 2003 StoneAge article names the historical专区 download page
http://www.17173.com/shiqi/xiazai/xiazai.htm. A June-2001 player diary also
shows the StoneAge专区 had a 软件下栽/软件下载 navigation surface. This probe
asks Wayback for exact/prefix metadata in 2000-12..2001-02 and replays only
small archived HTML pages. It never fetches linked installer/client payloads.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
from collections import OrderedDict

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"
TO="20010228"
MAX_HTML=2*1024*1024

EXACT_URLS=(
    "http://www.17173.com/shiqi/xiazai/xiazai.htm",
    "http://www.17173.com/shiqi/xiazai/",
    "http://stoneage.17173.com/xiazai/xiazai.htm",
    "http://stoneage.17173.com/xiazai/",
    "http://www.17173.com/stoneage/xiazai/xiazai.htm",
    "http://www.17173.com/stoneage/xiazai/",
)
PREFIX_URLS=(
    "http://www.17173.com/shiqi/xiazai/",
    "http://stoneage.17173.com/xiazai/",
    "http://www.17173.com/stoneage/xiazai/",
)
TOKENS=("石器","stoneage","试玩","試玩","下载","下載","客户端","客戶端","华义","華義","waei","274","兆","mb","exe","zip","rar","ftp://","http://")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=30,max_bytes=MAX_HTML,accept="application/json,text/html,*/*;q=0.2"):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":accept,"Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url(url,match):
    q=[
        ("url",url),
        ("matchType",match),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("filter","statuscode:200"),("limit","2000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(q)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    h=obj[0]
    return tuple(dict(zip(h,r)) for r in obj[1:] if isinstance(r,list))

def decode(body,content_type=""):
    m=re.search(r"charset=([A-Za-z0-9._-]+)",content_type or "",re.I)
    candidates=[]
    if m:candidates.append(m.group(1))
    candidates += ["gb18030","big5","utf-8","latin1"]
    seen=set()
    for enc in candidates:
        if enc.lower() in seen:continue
        seen.add(enc.lower())
        try:return body.decode(enc),enc
        except Exception:pass
    return body.decode("latin1","replace"),"latin1-replace"

def visible(raw):
    s=re.sub(r"(?is)<script\b.*?</script>"," ",raw)
    s=re.sub(r"(?is)<style\b.*?</style>"," ",s)
    s=re.sub(r"(?s)<[^>]+>"," ",s)
    return clean(html.unescape(s),12000)

def links(raw,base):
    out=[]
    for m in re.finditer(r'''(?is)<a\b[^>]*?href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))[^>]*>(.*?)</a\s*>''',raw):
        href=m.group(1) or m.group(2) or m.group(3) or ""
        anchor=visible(m.group(4))
        if not href:continue
        href=html.unescape(href.strip())
        absolute=urllib.parse.urljoin(base,href)
        out.append((anchor,absolute))
    return out

def relevant(anchor,url):
    hay=(anchor+" "+url).lower()
    return any(t.lower() in hay for t in TOKENS)

def main():
    print("StoneAge 17173 launch-window download-page archive probe — R1")
    print(f"SCOPE|17173 StoneAge download HTML/routing only|window={FROM}..{TO}|no installer/client payload")
    print("ANCHOR|historical 17173 StoneAge专区 download path later cited as www.17173.com/shiqi/xiazai/xiazai.htm")
    errors=[]
    allrows=OrderedDict()

    for kind,urls,match in (("exact",EXACT_URLS,"exact"),("prefix",PREFIX_URLS,"prefix")):
        for idx,u in enumerate(urls,1):
            try:
                st,final,h,b=fetch(cdx_url(u,match),timeout=35,max_bytes=4*1024*1024)
                rr=rows(b)
                print(f"CDX|kind={kind}|index={idx}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|query={clean(u)}")
                for r in rr:
                    key=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
                    allrows[key]=r
            except Exception as exc:
                errors.append((f"cdx:{kind}:{idx}",type(exc).__name__,str(exc)))

    print(f"COUNT|unique_rows|{len(allrows)}")
    for (ts,orig,digest),r in sorted(allrows.items()):
        print(f"ROW|timestamp={ts}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(digest)}|original={clean(orig)}")

    # Replay one capture per unique original URL, earliest first. HTML only.
    earliest={}
    for (ts,orig,digest),r in sorted(allrows.items()):
        earliest.setdefault(orig,(ts,digest,r))
    replayed=0
    relcount=0
    for orig,(ts,digest,r) in sorted(earliest.items(),key=lambda kv:(kv[1][0],kv[0])):
        if replayed>=40:
            break
        mime=str(r.get("mimetype") or "").lower()
        if mime and "html" not in mime and mime not in ("text/plain",""):
            continue
        replay=f"https://web.archive.org/web/{ts}id_/{orig}"
        try:
            st,final,h,b=fetch(replay,timeout=35,max_bytes=MAX_HTML,accept="text/html,*/*;q=0.2")
            text,enc=decode(b,h.get("Content-Type",""))
            vis=visible(text)
            print(f"PAGE|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|original={clean(orig)}|final={clean(final)}")
            hits=[t for t in TOKENS if t.lower() in (vis+" "+text).lower()]
            print(f"TOKENS|timestamp={ts}|values={','.join(clean(x,80) for x in hits)}")
            if hits:
                print(f"VISIBLE|timestamp={ts}|text={clean(vis,12000)}")
            for anchor,url in links(text,orig):
                if relevant(anchor,url):
                    relcount+=1
                    print(f"LINK|timestamp={ts}|anchor={clean(anchor,500)}|url={clean(url,5000)}")
            replayed+=1
        except Exception as exc:
            errors.append((f"replay:{ts}:{orig}",type(exc).__name__,str(exc)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|relevant_links|{relcount}")
    print(f"COUNT|errors|{len(errors)}")
    if relcount:
        print("RESOLUTION|17173_LAUNCH_DOWNLOAD_ROUTING_RECOVERED|classify exact StoneAge/trial/client links before any payload recovery")
    elif replayed:
        print("RESOLUTION|17173_LAUNCH_PAGES_REPLAYED_NO_LINK|tested preserved HTML exposes no relevant client route")
    elif allrows:
        print("RESOLUTION|17173_LAUNCH_ROWS_UNREPLAYED|retry only preserved HTML rows")
    elif errors:
        print("RESOLUTION|17173_LAUNCH_PROBE_PARTIAL|retry failed archive metadata surfaces only")
    else:
        print("RESOLUTION|17173_LAUNCH_DOWNLOAD_SURFACE_UNINDEXED|switch to another contemporaneous portal/mirror token")
    print("EVIDENCE_BOUNDARY|A recovered page/link is routing evidence only; client identity requires preserved filename/size/hash or bytes.")

if __name__=="__main__":
    main()
