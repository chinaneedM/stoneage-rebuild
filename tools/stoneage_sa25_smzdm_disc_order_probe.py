#!/usr/bin/env python3
"""Map image order inside the 2016 SMZDM StoneAge install-disc section.

HTML/text only. No image bodies and no game payloads are downloaded.
"""
from __future__ import annotations
import hashlib, html, re, urllib.parse, urllib.request

PAGE="https://post.smzdm.com/p/462347/"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
IMG_RE=re.compile(r"""(?is)<img\b[^>]*(?:src|data-src|data-original|data-lazy-src)\s*=\s*["']([^"']+)["'][^>]*>""")
TAG_RE=re.compile(r"(?is)<[^>]+>")

def clean(v,n=10000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*","Accept-Language":"zh-CN,zh;q=0.9,en;q=0.5"})
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(4_000_001)
        if len(b)>4_000_000: raise ValueError("page-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def visible(s):
    return html.unescape(TAG_RE.sub(" ",s)).replace("\u00a0"," ")

def section(text):
    start=text.find("游戏安装光盘")
    if start<0: start=text.find("遊戲安裝光碟")
    if start<0: return "",-1,-1
    ends=[x for x in (text.find("游戏说明书",start),text.find("遊戲說明書",start)) if x>=0]
    end=min(ends) if ends else min(len(text),start+30000)
    return text[start:end],start,end

def records(seg):
    out=[]; prev=0; seen=set()
    for m in IMG_RE.finditer(seg):
        u=html.unescape(m.group(1).strip())
        if u.startswith("//"): u="https:"+u
        u=urllib.parse.urljoin(PAGE,u)
        low=u.lower()
        if any(x in low for x in ("emotion","avatar","logo","icon","loading","blank")): continue
        if u in seen: continue
        seen.add(u)
        out.append((u,visible(seg[prev:m.start()]),visible(seg[m.end():m.end()+1200])))
        prev=m.end()
    return tuple(out)

def main():
    print("StoneAge 2.5 SMZDM install-disc image-order map — R1")
    print("SCOPE|2016-public-collector-post|html-order+local-context-only|no-image-body|no-game-payload")
    st,final,b=fetch(PAGE)
    text=b.decode("utf-8","replace")
    seg,start,end=section(text)
    rows=records(seg)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|section_start={start}|section_end={end}|images={len(rows)}|final={clean(final)}")
    print(f"SECTION_TEXT|value={clean(visible(seg),12000)}")
    for i,(u,pre,post) in enumerate(rows,1):
        print(f"IMAGE|order={i}|url={clean(u)}")
        print(f"PRECEDING|order={i}|value={clean(pre,5000)}")
        print(f"FOLLOWING|order={i}|value={clean(post,5000)}")
    print(f"COUNT|images|{len(rows)}")
    print("RESOLUTION|INSTALL_DISC_IMAGE_ORDER_MAPPED|assign version only when article text/order makes the association unambiguous")
    print("EVIDENCE_BOUNDARY|HTML order can map article-photo sequence; it does not establish disc bytes, pressing identity or clean-client provenance.")

if __name__=="__main__":
    main()
