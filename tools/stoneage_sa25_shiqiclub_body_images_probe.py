#!/usr/bin/env python3
"""Map article-body images for shiqi.club StoneAge 2.5 package article.

This is a text/HTML-only classifier: it fetches the known article, isolates the
main article body using literal body-text anchors, and emits only image URLs plus
nearby text. It does not download image bodies or game payloads.
"""
from __future__ import annotations
import hashlib, html, re, urllib.request
from tools.stoneage_sa25_host_identity_probe import declared_charset, decode, visible

URL="https://www.shiqi.club/shiqi2712.html"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"
START_TOKENS=("我又来更新","我又來更新")
END_TOKENS=("Tags：","Tags:","THE END")
IMG_RE=re.compile(r"""(?is)<img\b[^>]*(?:src|data-src|data-original)\s*=\s*["']([^"']+)["'][^>]*>""")

def clean(v,n=10000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":UA,"Accept":"text/html,*/*","Accept-Language":"zh-CN,zh;q=0.9"})
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(2_000_001)
        if len(b)>2_000_000: raise ValueError("page-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def body_slice(text):
    starts=[text.find(t) for t in START_TOKENS if text.find(t)>=0]
    if not starts:
        return "",-1,-1
    s=min(starts)
    ends=[text.find(t,s) for t in END_TOKENS if text.find(t,s)>s]
    e=min(ends) if ends else min(len(text),s+120000)
    return text[s:e],s,e

def body_images(fragment):
    out=[]; seen=set()
    for m in IMG_RE.finditer(fragment):
        u=html.unescape(m.group(1).strip())
        if u.startswith("//"): u="https:"+u
        elif u.startswith("/"): u="https://www.shiqi.club"+u
        elif not u.startswith(("http://","https://")): u="https://www.shiqi.club/"+u.lstrip("./")
        if u not in seen:
            seen.add(u); out.append((m.start(),u))
    return tuple(out)

def context(fragment,pos,radius=900):
    return visible(fragment[max(0,pos-radius):min(len(fragment),pos+radius)])

def main():
    print("StoneAge 2.5 shiqi.club article-body image map — R1")
    print("SCOPE|known-live-article|body-anchor+img-url-only|no-image-body|no-game-payload")
    st,final,b=fetch()
    enc,text=decode(b,declared_charset(b))
    frag,s,e=body_slice(text)
    imgs=body_images(frag)
    print(f"PAGE|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|body_start={s}|body_end={e}|body_chars={len(frag)}|images={len(imgs)}|final={clean(final)}")
    print(f"BODY_TEXT|value={clean(visible(frag),18000)}")
    for i,(pos,u) in enumerate(imgs,1):
        print(f"BODY_IMAGE|order={i}|url={clean(u)}")
        print(f"BODY_CONTEXT|order={i}|value={clean(context(frag,pos),5000)}")
    print(f"COUNT|body_images|{len(imgs)}")
    if imgs:
        print("RESOLUTION|ARTICLE_BODY_IMAGES_MAPPED|use exact body-image URLs as package visual recovery targets")
    else:
        print("RESOLUTION|ARTICLE_BODY_IMAGE_MAP_EMPTY|do not classify site-wide upload attrs as article images")
    print("EVIDENCE_BOUNDARY|body membership establishes article-photo association only; image contents and disc bytes require separate evidence.")

if __name__=="__main__":
    main()
