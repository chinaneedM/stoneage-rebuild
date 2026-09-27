#!/usr/bin/env python3
"""Replay only the six archived Popsoft game-portal pages in the launch window.

Source is the prior CDX census. Extract visible text and navigation targets for
StoneAge/trial/download evidence. No linked payload is fetched.
"""
from __future__ import annotations
import hashlib,html,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CAPTURES=(
 ("root","20001110122600","http://game.popsoft.com.cn:80/"),
 ("guide","20010124064900","http://game.popsoft.com.cn:80/Guide/"),
 ("na","20010124065900","http://game.popsoft.com.cn:80/Na/"),
 ("new","20010124070400","http://game.popsoft.com.cn:80/New/"),
 ("review","20010124070500","http://game.popsoft.com.cn:80/Review/"),
 ("search","20010215020858","http://game.popsoft.com.cn:80/Search/FastSearch.asp"),
)
TOKENS=("石器时代","石器時代","石器","stoneage","stone age","试玩","試玩","测试","測試","下载","下載","download","ftp","客户端","客戶端","client","华义","華義","waei","晶合","光盘","光碟","cd-rom","cdrom")
HINTS=("stone","shiqi","download","down","demo","trial","test","client","setup","ftp","waei","jhpop","石器")

def clean(v,n=8000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=50,max_bytes=2*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def decode(b):
    for enc in ("gb18030","gbk","big5","cp950","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def visible(t):
    x=re.sub(r"(?is)<script\b.*?</script>|<style\b.*?</style>"," ",t)
    x=re.sub(r"(?is)<[^>]+>"," ",x)
    return clean(html.unescape(x),50000)

def title(t):
    m=re.search(r"(?is)<title\b[^>]*>(.*?)</title>",t)
    return clean(html.unescape(re.sub(r"(?is)<[^>]+>"," ",m.group(1)))) if m else ""

def hits(s):
    l=s.lower();return tuple(t for t in TOKENS if t.lower() in l)

def links(t,base):
    out=[];seen=set()
    for m in re.finditer(r"(?is)<a\b[^>]*href\s*=\s*([\"'])(.*?)\1[^>]*>(.*?)</a>",t):
        raw=html.unescape(m.group(2)).strip()
        if not raw or raw.lower().startswith(("javascript:","mailto:","#")):continue
        u=urllib.parse.urljoin(base,raw)
        a=clean(html.unescape(re.sub(r"(?is)<[^>]+>"," ",m.group(3))),1200)
        k=(u,a)
        if k not in seen:seen.add(k);out.append(k)
    return tuple(out)

def score(u,a=""):
    s=urllib.parse.unquote_plus((str(u)+" "+str(a)).lower())
    return sum(1 for h in HINTS if h in s)

def snippets(s,hs,r=300):
    low=s.lower();out=[];seen=set()
    for h in hs:
        p=0
        while True:
            i=low.find(h.lower(),p)
            if i<0:break
            f=clean(s[max(0,i-r):min(len(s),i+len(h)+r)],1200)
            if f[:350] not in seen:seen.add(f[:350]);out.append((h,f))
            p=i+max(1,len(h))
            if len(out)>=20:return tuple(out)
    return tuple(out)

def main():
    print("StoneAge Popsoft game-portal exact-page replay — R1")
    print("SCOPE|six exact archived HTML captures|visible text/navigation only|no linked payload")
    targets={};errors=[];stone_pages=0
    for label,ts,orig in CAPTURES:
        replay=f"https://web.archive.org/web/{ts}id_/{orig}"
        try:
            st,final,b=fetch(replay);enc,t=decode(b);v=visible(t);hs=hits(v);ls=links(t,orig)
            if any(x.lower() in v.lower() for x in ("石器时代","石器時代","stoneage","stone age")):stone_pages+=1
            print(f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={clean(title(t))}|token_hits={clean(','.join(hs),2500)}|links={len(ls)}|final={clean(final)}")
            for h,f in snippets(v,hs):print(f"SNIPPET|label={label}|token={clean(h)}|text={clean(f,1400)}")
            for u,a in ls:
                sc=score(u,a)
                targets.setdefault((u,a),set()).add(label)
                if sc:
                    print(f"TARGET|label={label}|score={sc}|anchor={clean(a)}|url={clean(u)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
            print(f"ERROR|label={label}|kind={type(e).__name__}|message={clean(e)}")
    ranked=sorted(targets.items(),key=lambda kv:(-score(kv[0][0],kv[0][1]),kv[0][0]))
    for (u,a),labs in ranked:
        sc=score(u,a)
        if sc:print(f"RANKED_TARGET|score={sc}|from={clean(','.join(sorted(labs)))}|anchor={clean(a)}|url={clean(u)}")
    print(f"COUNT|stone_pages|{stone_pages}")
    print(f"COUNT|unique_links|{len(targets)}")
    print(f"COUNT|errors|{len(errors)}")
    if stone_pages:
        print("RESOLUTION|POPSOFT_STONEAGE_TEXT_FOUND|bind exact linked page/download routes next")
    elif any(score(u,a) for u,a in targets):
        print("RESOLUTION|POPSOFT_DOWNLOAD_TARGETS_FOUND|probe only source-linked high-value routes next")
    elif errors:
        print("RESOLUTION|PARTIAL_POPSOFT_REPLAY|retry failed exact captures only")
    else:
        print("RESOLUTION|POPSOFT_LAUNCH_PAGES_BOUNDED_NO_STONEAGE|do not promote this portal as a client carrier without new token")
    print("EVIDENCE_BOUNDARY|HTML/navigation evidence only; linked software is not downloaded.")

if __name__=="__main__":main()
