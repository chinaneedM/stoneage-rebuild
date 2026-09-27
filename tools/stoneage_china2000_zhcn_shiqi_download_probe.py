#!/usr/bin/env python3
"""Recover source-derived China.com StoneAge/download routes from the archived Dec-2000 giveaway surface.

The archived China.com giveaway-results page directly contains:
  /zh_cn/hotspot/shiqi/index.html
  /zh_cn/download/index.html

This probe tests those exact paths and their bounded prefixes across the
Dec-2000 / Jan-2001 launch window, then replays only small archived HTML pages
to extract StoneAge/download/trial/client links. Candidate binary bodies are
never fetched.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"
TO="20010120"
MAX_REPLAYS=40
MAX_HTML=1024*1024

TARGETS=(
    ("shiqi-exact","http://game.china.com/zh_cn/hotspot/shiqi/index.html","exact"),
    ("shiqi-exact80","http://game.china.com:80/zh_cn/hotspot/shiqi/index.html","exact"),
    ("download-exact","http://game.china.com/zh_cn/download/index.html","exact"),
    ("download-exact80","http://game.china.com:80/zh_cn/download/index.html","exact"),
    ("shiqi-prefix","http://game.china.com/zh_cn/hotspot/shiqi/","prefix"),
    ("shiqi-prefix80","http://game.china.com:80/zh_cn/hotspot/shiqi/","prefix"),
    ("download-prefix","http://game.china.com/zh_cn/download/","prefix"),
    ("download-prefix80","http://game.china.com:80/zh_cn/download/","prefix"),
)
TOKENS=("石器时代","石器時代","stoneage","stone age","试玩","試玩","测试版","測試版","下载","下載","client","客户端","客戶端","setup","install")
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".msi",".arj",".lzh",".7z",".iso",".bin",".cue")

def clean(v,n=4000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=MAX_HTML):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url(url,kind):
    q=[
        ("url",url),("matchType",kind),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("limit","10000")
    ]
    return CDX+"?"+urllib.parse.urlencode(q)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))

def decode(body):
    for enc in ("gb18030","gbk","gb2312","big5","utf-8","latin1"):
        try:
            return enc,body.decode(enc)
        except UnicodeDecodeError:
            pass
    return "latin1",body.decode("latin1","replace")

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def hrefs(text,base):
    out=[]
    pat=re.compile(r"""(?is)<a\b[^>]*href\s*=\s*["']([^"']+)["'][^>]*>(.*?)</a>""")
    for m in pat.finditer(text):
        raw=html.unescape(m.group(1)).strip()
        label=html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2)))
        label=re.sub(r"\s+"," ",label).strip()
        if not raw or raw.lower().startswith(("javascript:","mailto:","#")):
            continue
        out.append((urllib.parse.urljoin(base,raw),label))
    return tuple(out)

def interesting(url,label=""):
    low=urllib.parse.unquote_plus((url+" "+label).lower())
    path=urllib.parse.urlsplit(url).path.lower()
    return any(t.lower() in low for t in TOKENS) or path.endswith(PAYLOAD_EXTS)

def is_payload(url):
    return urllib.parse.urlsplit(url.lower()).path.endswith(PAYLOAD_EXTS)

def main():
    print("StoneAge China.com source-derived shiqi/download route probe — R1")
    print(f"SCOPE|archived first-party links from 63271|window={FROM}..{TO}|exact+prefix CDX|bounded HTML replay|no payload")
    print("ANCHOR|/zh_cn/hotspot/shiqi/index.html + /zh_cn/download/index.html are directly present on archived China.com StoneAge giveaway-results page")
    errors=[]
    allrows={}

    def query(spec):
        label,url,kind=spec
        try:
            st,final,h,b=fetch(cdx_url(url,kind),timeout=45,max_bytes=8*1024*1024)
            rr=rows(b)
            return label,url,kind,st,final,b,rr,None
        except Exception as e:
            return label,url,kind,None,"",b"",(),(type(e).__name__,str(e))

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results=[f.result() for f in concurrent.futures.as_completed([ex.submit(query,t) for t in TARGETS])]

    for label,url,kind,st,final,b,rr,err in sorted(results):
        if err:
            errors.append((f"cdx:{label}",err[0],err[1]))
            print(f"QUERY_ERROR|label={label}|kind={err[0]}|message={clean(err[1])}")
            continue
        print(f"QUERY|label={label}|kind={kind}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        for r in rr:
            key=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
            allrows[key]=r

    print(f"COUNT|unique_rows|{len(allrows)}")
    for (ts,orig,digest),r in sorted(allrows.items()):
        print(f"ROW|timestamp={ts}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(digest)}|redirect={clean(r.get('redirect'))}|original={clean(orig)}")

    candidates=[]
    seen=set()
    for (ts,orig,digest),r in sorted(allrows.items()):
        if str(r.get("statuscode") or "")!="200":
            continue
        mt=str(r.get("mimetype") or "").lower()
        path=urllib.parse.urlsplit(orig).path.lower()
        if "html" not in mt and not path.endswith((".htm",".html",".asp",".shtml","/")):
            continue
        key=(ts,orig)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(key)
        if len(candidates)>=MAX_REPLAYS:
            break

    print(f"COUNT|selected_replays|{len(candidates)}")
    page_hits=0
    payload_links=set()
    route_links=set()
    for ts,orig in candidates:
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=35,max_bytes=MAX_HTML)
            enc,text=decode(b)
            plain=html.unescape(re.sub(r"(?s)<[^>]+>"," ",text))
            plain=re.sub(r"\s+"," ",plain)
            token_hits=[t for t in TOKENS if t.lower() in plain.lower()]
            links=hrefs(text,orig)
            hits=[(u,a) for u,a in links if interesting(u,a)]
            if token_hits or hits:
                page_hits+=1
            print(f"PAGE|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|tokens={clean(','.join(token_hits),800)}|links={len(links)}|interesting_links={len(hits)}|original={clean(orig)}")
            if token_hits:
                for token in token_hits:
                    idx=plain.lower().find(token.lower())
                    if idx>=0:
                        print(f"SNIPPET|timestamp={ts}|token={clean(token)}|text={clean(plain[max(0,idx-260):idx+520],1200)}")
            for u,a in hits:
                if is_payload(u):
                    payload_links.add(u)
                    kind="PAYLOAD"
                else:
                    route_links.add(u)
                    kind="ROUTE"
                print(f"{kind}_LINK|timestamp={ts}|anchor={clean(a,800)}|url={clean(u)}")
        except Exception as e:
            errors.append((f"replay:{ts}:{orig}",type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|pages_with_signal|{page_hits}")
    print(f"COUNT|payload_links|{len(payload_links)}")
    print(f"COUNT|route_links|{len(route_links)}")
    print(f"COUNT|errors|{len(errors)}")
    if payload_links:
        print("RESOLUTION|CHINACOM_STONEAGE_PAYLOAD_LINK_FOUND|validate exact archive metadata/redirect and provenance next")
    elif allrows and page_hits:
        print("RESOLUTION|CHINACOM_STONEAGE_ROUTE_SIGNAL_FOUND|follow only source-derived surviving routes next")
    elif allrows:
        print("RESOLUTION|CHINACOM_SOURCE_PATHS_RECOVERED_NO_STONEAGE_DOWNLOAD_SIGNAL|bound this route family")
    elif errors:
        print("RESOLUTION|CHINACOM_SOURCE_ROUTE_PROBE_PARTIAL|retry failed exact surfaces only")
    else:
        print("RESOLUTION|CHINACOM_ZHCN_SOURCE_ROUTES_UNINDEXED|switch to independent mirrors/carriers")
    print("EVIDENCE_BOUNDARY|Archive routing/HTML evidence does not authenticate a client build; no candidate binary body is fetched.")

if __name__=="__main__":
    main()
