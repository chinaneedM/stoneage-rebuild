#!/usr/bin/env python3
"""Retry high-relevance Waei launch pages that timed out in the broad replay.

Only the failed news/bulletin pages are revisited. For each target URL, CDX is
queried for a successful capture in the 2.0 launch window, then one selected
capture is replayed and inspected for download/client routing. No payloads.
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
FROM="20011024"
TO="20011112"
TARGET_DAY=20011102
TARGETS=(
 ("bulletin-296","http://www.waei.com.cn:80/zhuanqu/stoneage2/stbulletin/st_bulletin_nr.asp?id=296"),
 ("bulletin-277","http://www.waei.com.cn:80/zhuanqu/stoneage2/stbulletin/st_bulletin_nr.asp?id=277"),
 ("news-16","http://www.waei.com.cn:80/ZHUANQU/stoneage2/stnews/st_news_nr.asp?id=16"),
 ("news-22","http://www.waei.com.cn:80/ZHUANQU/stoneage2/stnews/st_news_nr.asp?id=22"),
 ("news-20","http://www.waei.com.cn:80/ZHUANQU/stoneage2/stnews/st_news_nr.asp?id=20"),
 ("news-index","http://www.waei.com.cn:80/ZHUANQU/stoneage2/stnews/st_news_nr.asp"),
 ("bulletin-index","http://www.waei.com.cn:80/ZHUANQU/stoneage2/stbulletin/st_bulletin_nr.asp"),
)
TOKENS=("石器时代2.0","家族开拓史","完整升级版","升级版","客户端","下载","安装","stoneage2.0setup","setup.exe")
ROUTE_RE=re.compile(
 r"""(?is)(?:href|src|action)\s*=\s*["']([^"']+)["']"""
 r"""|(?:window\.open|location(?:\.href)?\s*=|window\.location\s*=)\s*\(?\s*["']([^"']+)["']"""
)
URL_RE=re.compile(r"""(?i)https?://[^\s"'<>]+""")


def clean(v,n=3000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=22,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b


def cdx_url(url):
    p=[
      ("url",url),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length"),
      ("from",FROM),("to",TO),("filter","statuscode:200"),("limit","20"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))


def day_distance(ts):
    try:
        n=int(str(ts)[:8]); y=n//10000; m=(n//100)%100; d=n%100
        t=TARGET_DAY; ty=t//10000; tm=(t//100)%100; td=t%100
        return abs(((y*372)+(m*31)+d)-((ty*372)+(tm*31)+td))
    except Exception:
        return 9999


def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode(b):
    for enc in ("gb18030","big5","utf-8","latin1"):
        try:return b.decode(enc)
        except UnicodeDecodeError:pass
    return b.decode("latin1","replace")


def strip_html(text):
    t=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    t=re.sub(r"(?is)<style\b.*?</style>"," ",t)
    t=re.sub(r"(?s)<[^>]+>"," ",t)
    return re.sub(r"\s+"," ",html.unescape(t)).strip()


def contexts(text,radius=130):
    plain=strip_html(text); low=plain.lower(); out=[]; seen=set()
    for tok in TOKENS:
        pos=0
        while True:
            i=low.find(tok.lower(),pos)
            if i<0:break
            sn=clean(plain[max(0,i-radius):min(len(plain),i+len(tok)+radius)],360)
            if sn not in seen:
                seen.add(sn);out.append((tok,sn))
            pos=i+max(1,len(tok))
            if len(out)>=10:return tuple(out)
    return tuple(out)


def refs(text,base):
    out=[]
    for m in ROUTE_RE.finditer(text):
        raw=(m.group(1) or m.group(2) or "").strip()
        if raw and not raw.startswith(("javascript:","mailto:","#")):
            out.append(urllib.parse.urljoin(base,html.unescape(raw)))
    for m in URL_RE.finditer(text):out.append(html.unescape(m.group(0)))
    return tuple(dict.fromkeys(u.rstrip("),.;") for u in out))


def route_score(url):
    low=urllib.parse.unquote_plus(url).lower(); s=0
    for tok,w in (("stoneage",5),("client",4),("setup",4),("download",3),("upgrade",3),(".exe",5),(".zip",4),(".cab",4),(".rar",4)):
        if tok in low:s+=w
    host=urllib.parse.urlsplit(url).hostname or ""
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}",host):s+=4
    return s


def main():
    print("StoneAge Waei Q4-2001 high-relevance launch residual probe — R1")
    print(f"SCOPE|{len(TARGETS)} previously timed-out news/bulletin targets|{FROM}..{TO}|HTML-only|no-payload")
    errors=[]; routes={}; replayed=0; semantic=0
    for label,url in TARGETS:
        try:
            st,final,b=fetch(cdx_url(url),max_bytes=512*1024)
            rr=rows(b)
            rr=sorted(rr,key=lambda r:(day_distance(r.get("timestamp")),str(r.get("timestamp") or "")))
            print(f"CDX|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|url={clean(url)}")
            if not rr:
                continue
            r=rr[0]; ts=str(r.get("timestamp") or ""); orig=str(r.get("original") or url)
            st2,final2,body=fetch(replay_url(ts,orig),max_bytes=768*1024)
            replayed+=1; txt=decode(body); ctx=contexts(txt)
            if ctx: semantic+=1
            print(f"PAGE|label={label}|timestamp={ts}|status={st2}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|orig={clean(orig)}|contexts={len(ctx)}")
            for tok,sn in ctx:print(f"CONTEXT|label={label}|token={clean(tok,80)}|text={clean(sn,360)}")
            for u in refs(txt,orig):
                sc=route_score(u)
                if sc>=4:
                    routes[u]=max(routes.get(u,0),sc)
                    print(f"ROUTE_REF|label={label}|score={sc}|url={clean(u)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    exact=[u for u in routes if "stoneage2.0setup" in urllib.parse.unquote_plus(u).lower()]
    binary=[u for u in routes if urllib.parse.urlsplit(u).path.lower().endswith((".exe",".zip",".cab",".rar"))]
    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|semantic_pages|{semantic}")
    print(f"COUNT|scored_routes|{len(routes)}")
    print(f"COUNT|binary_routes|{len(binary)}")
    print(f"COUNT|exact_setup_refs|{len(exact)}")
    for scope,kind,msg in errors:print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:print("RESOLUTION|EXACT_SETUP_ROUTE_FOUND_IN_RESIDUAL|classify/replay before payload recovery")
    elif binary:print("RESOLUTION|BINARY_ROUTE_FOUND_IN_RESIDUAL|classify against 2.0 client lineage")
    elif errors:print("RESOLUTION|HIGH_RELEVANCE_RESIDUAL_INCOMPLETE|retain only failed exact target(s)")
    else:print("RESOLUTION|HIGH_RELEVANCE_LAUNCH_RESIDUAL_CLOSED_NO_CLIENT_ROUTE|official news/bulletin retry surface yields no client-download route")
    print("EVIDENCE_BOUNDARY|CDX/HTML routing evidence only; no binary payload downloaded.")


if __name__=="__main__":
    main()
