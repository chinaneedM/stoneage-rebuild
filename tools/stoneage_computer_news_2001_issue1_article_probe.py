#!/usr/bin/env python3
"""Replay the contemporaneous Computer Newspaper StoneAge article from 2001 issue 1.

The software-archive mirror exposes issue 2001/01 with article 63220 titled
"进军石器时代". This is a narrowly scoped contemporaneous textual source.
The probe extracts visible text, links and distribution-related snippets only.
No software or image payload is fetched.
"""
from __future__ import annotations
import hashlib, html, re, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
URL="https://software-archive.tifan.la/%E7%94%B5%E8%84%91%E6%8A%A5/2001/01/63220.html"
TOKENS=("石器时代","测试","试玩","光盘","下载","华义","北京华义","赠送","杂志","客户端","安装","WGS","晶合","1.0")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=2*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def decode(body):
    for enc in ("utf-8","gb18030","gbk","big5"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "utf-8",body.decode("utf-8","replace")

def visible(text):
    text=re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>"," ",text)
    text=re.sub(r"(?s)<[^>]+>"," ",text)
    return re.sub(r"\s+"," ",html.unescape(text)).strip()

def main():
    print("StoneAge Computer Newspaper 2001/01 article replay — R1")
    print("SCOPE|single contemporaneous article|visible text+hrefs only|no image/software payload")
    print(f"TARGET|{URL}")
    try:
        st,final,h,b=fetch(URL)
        enc,raw=decode(b)
        vis=visible(raw)
        title=""
        m=re.search(r"(?is)<title[^>]*>(.*?)</title>",raw)
        if m:title=clean(visible(m.group(1)),1000)
        hrefs=[html.unescape(x) for x in re.findall(r'''(?is)href\s*=\s*["']([^"']+)["']''',raw)]
        print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={title}|hrefs={len(hrefs)}|visible_chars={len(vis)}|final={clean(final)}")
        hits=0
        low=vis.lower()
        for token in TOKENS:
            start=0
            while True:
                idx=low.find(token.lower(),start)
                if idx<0:break
                hits+=1
                print(f"SNIPPET|token={clean(token)}|text={clean(vis[max(0,idx-260):idx+700],1400)}")
                start=idx+len(token)
                if hits>=80:break
            if hits>=80:break
        for href in hrefs:
            lo=href.lower()
            if any(x in lo for x in ("stone","shiqi","download","waei","wayi","game","soft")):
                print(f"LINK|url={clean(href)}")
        print(f"COUNT|token_hits={hits}")
        dist=any(t in vis for t in ("测试","试玩","光盘","下载","赠送","客户端","安装"))
        if dist:
            print("RESOLUTION|CONTEMPORANEOUS_DISTRIBUTION_SIGNAL_FOUND|classify exact wording and route before using as carrier evidence")
        else:
            print("RESOLUTION|CONTEMPORANEOUS_ARTICLE_NO_DISTRIBUTION_SIGNAL|retain gameplay/context source only")
    except Exception as e:
        print(f"ERROR|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|ARTICLE_REPLAY_FAILED|retry exact page only")
    print("EVIDENCE_BOUNDARY|This is a later public archive/mirror of contemporaneous print text; it does not by itself authenticate a magazine disc or client bytes.")

if __name__=="__main__":
    main()
