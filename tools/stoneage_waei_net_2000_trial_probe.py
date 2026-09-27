#!/usr/bin/env python3
"""Probe the early official Waei.net StoneAge site for the Jan-2001 trial download.

Source anchors:
- contemporary/near-contemporary references identify
  http://www7.waei.net/wgs/stoneage/ as the official StoneAge site;
- the accepted Taiwan-v1.0 client also exposes stoneage.waei.net as a historical
  operator host token;
- a 17173 diary says a StoneAge trial version of roughly 274 MB was visible on
  Waei's homepage on 2001-01-04.

The probe uses Wayback CDX + archived HTML only. It never downloads candidate
game binaries.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
FROM="20001201"
TO="20010112"
MAX_ROWS=30000
MAX_HTML=80
MAX_BODY=1024*1024

PREFIXES=(
    ("official-www7","http://www7.waei.net/wgs/stoneage/"),
    ("client-host","http://stoneage.waei.net/"),
)
DOMAIN="waei.net"

STONE=("stoneage","stone age","石器时代","石器時代","shiqi")
DOWNLOAD=("download","down","下载","下載","trial","试玩","試玩","test","测试","測試","demo","client","客户端","客戶端","setup","install","安裝","安装")
BINARY_EXTS=(".exe",".zip",".rar",".cab",".arj",".lzh",".7z")
NOISE=("wallpaper","screen","screenshot","image","images/","forum","bbs","banner","logo","music","mp3")


def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=45,max_bytes=MAX_BODY):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b


def cdx_url(url,match):
    params=[
        ("url",url),("matchType",match),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from",FROM),("to",TO),("limit",str(MAX_ROWS)),("collapse","urlkey"),
    ]
    return CDX+"?"+urllib.parse.urlencode(params)


def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))


def unquote(url):
    return urllib.parse.unquote_plus(str(url or "")).lower()


def is_binary(url):
    return urllib.parse.urlsplit(unquote(url)).path.endswith(BINARY_EXTS)


def relevant_url(url):
    low=unquote(url)
    p=urllib.parse.urlsplit(low)
    host=(p.hostname or "").lower()
    path=p.path
    if any(n in low for n in NOISE):
        return False
    return (
        "stoneage" in host
        or "/wgs/stoneage" in path
        or any(t in low for t in ("stoneage","shiqi"))
    )


def score(row):
    url=str(row.get("original") or "")
    low=unquote(url)
    s=0
    if relevant_url(url): s+=20
    if any(t in low for t in DOWNLOAD): s+=15
    if is_binary(url): s+=20
    mt=str(row.get("mimetype") or "").lower()
    if "html" in mt: s+=3
    if str(row.get("timestamp") or "").startswith("20010104"): s+=8
    return s


def html_candidate(row):
    url=str(row.get("original") or "")
    if not relevant_url(url):
        return False
    p=urllib.parse.urlsplit(url).path.lower()
    mt=str(row.get("mimetype") or "").lower()
    return "html" in mt or p.endswith((".htm",".html",".asp",".shtml",".php")) or p.endswith("/")


def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode(body):
    for enc in ("gb18030","big5","gbk","gb2312","utf-8","latin1"):
        try:
            return enc,body.decode(enc)
        except UnicodeDecodeError:
            pass
    return "latin1",body.decode("latin1","replace")


def extract_links(text,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',text):
        href=html.unescape(m.group(1)).strip()
        anchor=re.sub(r"(?s)<[^>]+>"," ",m.group(2))
        anchor=html.unescape(re.sub(r"\s+"," ",anchor)).strip()
        if not href or href.lower().startswith(("javascript:","mailto:","#")):
            continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)


def semantics(text):
    plain=html.unescape(re.sub(r"(?s)<[^>]+>"," ",text))
    plain=re.sub(r"\s+"," ",plain)
    low=plain.lower()
    stones=[t for t in STONE if t.lower() in low]
    downs=[t for t in DOWNLOAD if t.lower() in low]
    size274=bool(re.search(r"274\s*(?:m|mb|兆)",low,re.I))
    return stones,downs,size274,bool(stones and downs)


def target_link(href,anchor):
    low=unquote(href+" "+anchor)
    if any(n in low for n in NOISE):
        return False
    return is_binary(href) or any(t in low for t in STONE) or any(t in low for t in DOWNLOAD)


def main():
    print("StoneAge Waei.net 2000/2001 trial-download archive probe — R1")
    print(f"SCOPE|official-www7+stoneage-host+waei.net-domain|window={FROM}..{TO}|CDX+HTML-links|no-binary-payload")
    print("EVIDENCE_ANCHOR|official-site=http://www7.waei.net/wgs/stoneage/|client-host=stoneage.waei.net|17173-2001-01-04-trial~274MB")
    errors=[]
    collected=[]
    completed=0

    queries=[*(("prefix:"+label,url,"prefix") for label,url in PREFIXES),("domain",DOMAIN,"domain")]
    for label,url,match in queries:
        try:
            st,final,h,b=fetch(cdx_url(url,match),timeout=60,max_bytes=10*1024*1024)
            rr=rows(b);completed+=1
            print(f"CDX|label={label}|url={clean(url)}|match={match}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for r in rr:
                collected.append((label,r))
        except Exception as exc:
            errors.append((f"cdx:{label}",type(exc).__name__,str(exc)))

    uniq={}
    for label,r in collected:
        key=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
        uniq[key]=(label,r)

    rel=[(label,r) for label,r in uniq.values() if relevant_url(str(r.get("original") or ""))]
    rel.sort(key=lambda x:(score(x[1]),str(x[1].get("timestamp") or "")),reverse=True)
    binaries=[(label,r) for label,r in rel if is_binary(str(r.get("original") or ""))]
    print(f"COUNT|queries_completed|{completed}")
    print(f"COUNT|unique_rows|{len(uniq)}")
    print(f"COUNT|relevant_rows|{len(rel)}")
    print(f"COUNT|binary_rows|{len(binaries)}")

    for label,r in rel[:220]:
        print(
            f"ROW|score={score(r)}|source={label}|timestamp={clean(r.get('timestamp'))}|"
            f"original={clean(r.get('original'))}|status={clean(r.get('statuscode'))}|"
            f"mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|"
            f"digest={clean(r.get('digest'))}|redirect={clean(r.get('redirect'))}|binary={int(is_binary(str(r.get('original') or '')))}"
        )

    selected=[]
    seen=set()
    for label,r in rel:
        if not html_candidate(r):
            continue
        orig=str(r.get("original") or "")
        if orig in seen:
            continue
        seen.add(orig)
        selected.append((label,r))
        if len(selected)>=MAX_HTML:
            break

    print(f"COUNT|selected_html|{len(selected)}")
    replayed=0
    semantic_pages=0
    size274_pages=0
    links={}
    for i,(label,r) in enumerate(selected,1):
        ts=str(r.get("timestamp") or "")
        orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=40,max_bytes=MAX_BODY)
            replayed+=1
            enc,text=decode(b)
            stones,downs,s274,sem=semantics(text)
            semantic_pages+=int(sem)
            size274_pages+=int(s274)
            ls=extract_links(text,orig)
            hits=[(u,a) for u,a in ls if target_link(u,a)]
            print(
                f"PAGE|index={i}|source={label}|timestamp={ts}|status={st}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|semantic={int(sem)}|"
                f"size274={int(s274)}|stone={clean(','.join(stones),600)}|download={clean(','.join(downs),600)}|"
                f"links={len(ls)}|target_links={len(hits)}|orig={clean(orig)}"
            )
            for u,a in hits:
                links[(u,a)]=orig
                print(f"LINK|page={clean(orig)}|href={clean(u)}|anchor={clean(a,1000)}|binary={int(is_binary(u))}")
        except Exception as exc:
            errors.append((f"page:{i}:{orig}",type(exc).__name__,str(exc)))

    binary_links=[(u,a,p) for (u,a),p in links.items() if is_binary(u)]
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|semantic_pages|{semantic_pages}")
    print(f"COUNT|size274_pages|{size274_pages}")
    print(f"COUNT|unique_target_links|{len(links)}")
    print(f"COUNT|binary_link_hits|{len(binary_links)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")

    if binary_links or binaries:
        print("RESOLUTION|EARLY_WAEI_NET_BINARY_ROUTE_FOUND|classify exact archived URL/redirect and expected size before byte recovery")
    elif semantic_pages or size274_pages or links or rel:
        print("RESOLUTION|EARLY_WAEI_NET_TOPOLOGY_FOUND|follow exact source-derived paths/captures next")
    elif errors and completed<len(queries):
        print("RESOLUTION|EARLY_WAEI_NET_SURFACE_INCOMPLETE|retry only failed archive queries")
    else:
        print("RESOLUTION|EARLY_WAEI_NET_ROUTE_BOUNDED|tested source-backed Waei.net surfaces expose no launch-window route")
    print("EVIDENCE_BOUNDARY|URL and archived-HTML evidence cannot prove client bytes/build. Candidate binaries are not downloaded by this probe.")

if __name__=="__main__":
    main()
