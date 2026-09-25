#!/usr/bin/env python3
"""Recover the archived 2001 xinhaonanhai site topology around the StoneAge map.

The Sina 2001-11-27 full-map record explicitly attributes the package to
xinhaonanhai and links www.xinhaonanhai.com. Wayback has a root capture only
six days later (2001-12-03). This probe replays only small same-domain HTML at
bounded depth, extracting href/src/frame/meta-refresh paths. No binaries.
"""
from __future__ import annotations
import hashlib,html,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20011203002610"
ROOT="http://www.xinhaonanhai.com/"
TARGET="Estoneage2.0map_1127.exe"
MAX_PAGES=24
MAX_BYTES=384*1024

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=MAX_BYTES):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def replay(orig):
    return f"https://web.archive.org/web/{TS}id_/{orig}"

def decode(body):
    for enc in ("gb18030","big5","utf-8","latin1"):
        try:return body.decode(enc)
        except UnicodeDecodeError:pass
    return body.decode("latin1","replace")

def extract_urls(body,base):
    text=decode(body);vals=[]
    patterns=(
      r'(?is)href\s*=\s*["\']([^"\']+)["\']',
      r'(?is)src\s*=\s*["\']([^"\']+)["\']',
      r'(?is)action\s*=\s*["\']([^"\']+)["\']',
      r'(?is)<meta[^>]+http-equiv\s*=\s*["\']?refresh["\']?[^>]+content\s*=\s*["\'][^"\']*url\s*=\s*([^"\';>]+)',
      r'(?i)(?:https?|ftp)://[^\s"\'<>]+',
    )
    for pat in patterns:vals.extend(re.findall(pat,text))
    out=[]
    for raw in vals:
        raw=html.unescape(str(raw)).strip()
        if not raw or raw.startswith(("javascript:","mailto:","#")):continue
        u=urllib.parse.urljoin(base,raw)
        out.append(u)
    return tuple(dict.fromkeys(out))

def same_domain(url):
    try:
        h=urllib.parse.urlsplit(url).hostname or ""
        return h.lower() in ("xinhaonanhai.com","www.xinhaonanhai.com")
    except Exception:return False

def html_candidate(url):
    try:
        p=urllib.parse.urlsplit(url).path.lower()
    except Exception:return False
    leaf=p.rsplit("/",1)[-1]
    if not leaf:return True
    if any(leaf.endswith(ext) for ext in (".exe",".zip",".rar",".cab",".jpg",".jpeg",".gif",".png",".bmp",".mp3",".wav",".avi",".rm",".swf")):
        return False
    return "." not in leaf or any(leaf.endswith(ext) for ext in (".htm",".html",".shtm",".shtml",".asp",".php",".jsp",".txt"))

def targetish(url):
    low=urllib.parse.unquote_plus(str(url)).lower()
    return any(k in low for k in (
      TARGET.lower(),"stoneage","shiqi","2.0map","1127","map","download","down","soft","game"
    ))

def main():
    print("StoneAge 2001 xinhaonanhai site-topology probe — R1")
    print("SCOPE|2001-12-03 root capture + bounded same-domain HTML BFS depth<=2|no-binary")
    print(f"TARGET|filename={TARGET}|root={ROOT}|timestamp={TS}")
    queue=[(0,ROOT)];seen=set();errors=[];interesting=[];pages=0
    while queue and pages<MAX_PAGES:
        depth,orig=queue.pop(0)
        key=orig.lower()
        if key in seen:continue
        seen.add(key)
        if depth>2 or not same_domain(orig) or not html_candidate(orig):continue
        try:
            st,final,h,b=fetch(replay(orig),timeout=35,max_bytes=MAX_BYTES)
            pages+=1
            urls=extract_urls(b,orig)
            print(f"PAGE|depth={depth}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|orig={clean(orig)}|links={len(urls)}")
            for u in urls:
                relation="internal" if same_domain(u) else "external"
                flag=int(targetish(u))
                print(f"LINK|depth={depth}|relation={relation}|targetish={flag}|url={clean(u)}")
                if flag:interesting.append(u)
                if depth<2 and same_domain(u) and html_candidate(u):
                    queue.append((depth+1,u))
            text=decode(b)
            for line in re.split(r'[\r\n]+',text):
                s=" ".join(line.split());low=urllib.parse.unquote_plus(s).lower()
                if TARGET.lower() in low or any(k in low for k in ("stoneage","石器","地图","下載","下载")):
                    print(f"TEXT_HIT|depth={depth}|orig={clean(orig)}|text={clean(s,1800)}")
        except Exception as e:
            errors.append((f"page:{depth}:{orig}",type(e).__name__,str(e)))
    uniq=tuple(dict.fromkeys(interesting))
    print(f"COUNT|pages_replayed|{pages}")
    print(f"COUNT|interesting_links|{len(uniq)}")
    for i,u in enumerate(uniq,1):print(f"INTERESTING|index={i}|url={clean(u)}")
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if any(TARGET.lower() in urllib.parse.unquote_plus(u).lower() for u in uniq):
        print("RESOLUTION|TARGET_URL_FOUND_ON_CONTRIBUTOR_SITE|probe exact archive object without assuming Sina byte identity")
    elif uniq:
        print("RESOLUTION|CONTRIBUTOR_SITE_TOPOLOGY_RECOVERED|use discovered StoneAge/download paths for bounded archive queries")
    else:
        print("RESOLUTION|NO_RELEVANT_SITE_PATH|root/linked HTML exposes no usable StoneAge/download route at tested depth")
    print("EVIDENCE_BOUNDARY|same-domain navigation proves site topology only; package identity requires exact archived bytes.")

if __name__=="__main__":
    main()
