#!/usr/bin/env python3
"""Retry the sole China.com /zh_cn/download/ launch-window archive row.

Parent R1 found exactly one row in the source-derived China.com download prefix:
  2000-12-19 /zh_cn/download/pic/a_1.html
Its replay timed out. This residual retries only that exact archived page and
classifies visible text/links for StoneAge/download/client semantics.

No binary payload is fetched.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20001219123000"
ORIG="http://game.china.com:80/zh_cn/download/pic/a_1.html"
TOKENS=("石器时代","石器時代","stoneage","stone age","试玩","試玩","测试版","測試版","客户端","客戶端","download","下载","下載")
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".msi",".arj",".lzh",".7z",".iso",".bin",".cue")

def clean(v,n=4000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def replay_url():
    return f"https://web.archive.org/web/{TS}id_/{ORIG}"

def decode(body):
    for enc in ("gb18030","gbk","gb2312","big5","utf-8","latin1"):
        try:
            return enc,body.decode(enc)
        except UnicodeDecodeError:
            pass
    return "latin1",body.decode("latin1","replace")

def links(text):
    out=[]
    pat=re.compile(r"""(?is)<a\b[^>]*href\s*=\s*["']([^"']+)["'][^>]*>(.*?)</a>""")
    for m in pat.finditer(text):
        raw=html.unescape(m.group(1)).strip()
        label=html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2)))
        label=re.sub(r"\s+"," ",label).strip()
        if raw and not raw.lower().startswith(("javascript:","mailto:","#")):
            out.append((urllib.parse.urljoin(ORIG,raw),label))
    return tuple(out)

def interesting(url,label):
    low=urllib.parse.unquote_plus((url+" "+label).lower())
    path=urllib.parse.urlsplit(url).path.lower()
    return any(t.lower() in low for t in TOKENS) or path.endswith(PAYLOAD_EXTS)

def main():
    print("StoneAge China.com /zh_cn/download sole-row residual — R2")
    print(f"SCOPE|exact archived page only|timestamp={TS}|no payload")
    print(f"TARGET|{ORIG}")
    errors=[]
    replayed=0
    for attempt in range(1,4):
        try:
            st,final,h,b=fetch(replay_url(),timeout=45)
            replayed=1
            enc,text=decode(b)
            plain=html.unescape(re.sub(r"(?s)<[^>]+>"," ",text))
            plain=re.sub(r"\s+"," ",plain)
            token_hits=[t for t in TOKENS if t.lower() in plain.lower()]
            hrefs=links(text)
            hits=[(u,a) for u,a in hrefs if interesting(u,a)]
            print(f"PAGE|attempt={attempt}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|tokens={clean(','.join(token_hits),800)}|links={len(hrefs)}|interesting_links={len(hits)}|final={clean(final)}")
            print(f"VISIBLE|text={clean(plain,6000)}")
            for u,a in hits:
                print(f"LINK|anchor={clean(a,800)}|url={clean(u)}")
            print(f"COUNT|stoneage_tokens|{sum(1 for t in token_hits if 'stone' in t.lower() or '石器' in t)}")
            print(f"COUNT|interesting_links|{len(hits)}")
            if token_hits or hits:
                print("RESOLUTION|CHINACOM_DOWNLOAD_RESIDUAL_HAS_SIGNAL|classify exact link semantics next")
            else:
                print("RESOLUTION|CHINACOM_ZHCN_DOWNLOAD_ROUTE_BOUNDED|sole launch-window row is unrelated; no StoneAge/client signal")
            break
        except Exception as e:
            errors.append((attempt,type(e).__name__,str(e)))
            print(f"RETRY_ERROR|attempt={attempt}|kind={type(e).__name__}|message={clean(e)}")
    print(f"COUNT|replayed|{replayed}")
    print(f"COUNT|errors|{len(errors)}")
    if not replayed:
        print("RESOLUTION|CHINACOM_DOWNLOAD_RESIDUAL_OPEN|exact sole row remains unreplayed after bounded retries")
    print("EVIDENCE_BOUNDARY|This classifies only the archived China.com /zh_cn/download/ launch-window surface; absence does not negate other mirrors.")

if __name__=="__main__":
    main()
