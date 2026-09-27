#!/usr/bin/env python3
"""Focused replay of Waei central-download category IDs 1 and 2 only.

ID 1 and ID 2 are the highest-value categories for the current StoneAge work:
the archived namespace shows patch files under ID-family pages, while the old
www9 system used category 2 for game trials. This probe replays only known
captured pages and extracts text/file links. No binary payload is fetched.
"""
from __future__ import annotations
import hashlib, html, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
MAX_BODY=1024*1024
TARGETS=(
 ("id1-base","20010126021700","http://www7.waei.net:80/download/dldetial.asp?ID=1"),
 ("id1-page1","20010428120220","http://www7.waei.net:80/download/dldetial.asp?ID=1&xPage=1"),
 ("id1-page2","20010619204044","http://www7.waei.net:80/download/dldetial.asp?ID=1&xPage=2"),
 ("id1-page3","20010619204359","http://www7.waei.net:80/download/dldetial.asp?ID=1&xPage=3"),
 ("id2-base","20010419152808","http://www7.waei.net:80/download/dldetial.asp?ID=2"),
 ("id2-page1","20010502102920","http://www7.waei.net:80/download/dldetial.asp?ID=2&xPage=1"),
 ("id2-page2","20010428093726","http://www7.waei.net:80/download/dldetial.asp?ID=2&xPage=2"),
 ("id2-page3","20010619162832","http://www7.waei.net:80/download/dldetial.asp?ID=2&xPage=3"),
 ("id2-page4","20010428094354","http://www7.waei.net:80/download/dldetial.asp?ID=2&xPage=4"),
)
STONE=("stoneage","stone age","石器時代","石器时代","石器")
HINTS=("spr_1.bin","adrn_1.bin","real_1.bin","spradrn_1.bin","stoneage.exe","試玩版","试玩版")

def clean(v,n=6000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def fetch(url,timeout=35,max_bytes=MAX_BODY):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,*/*;q=0.1","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def decode(b):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,b.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",b.decode("latin1","replace")

def plain(t):
    p=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",t)
    p=html.unescape(re.sub(r"(?s)<[^>]+>"," ",p))
    return re.sub(r"\s+"," ",p)

def title(t):
    m=re.search(r"(?is)<title[^>]*>(.*?)</title>",t)
    return clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(1))) if m else "",500)

def links(t,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',t):
        href=html.unescape(m.group(1)).strip()
        anchor=clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2))),1200)
        if not href or href.lower().startswith(("javascript:","mailto:","#")):continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)

def isfile(u):
    p=urllib.parse.urlsplit(str(u)).path.lower()
    return "/download/file/" in p or p.endswith((".exe",".zip",".rar",".cab",".bin",".dat",".doc",".wmv",".avi"))

def hits(t,terms):
    l=plain(t).lower()
    return tuple(x for x in terms if x.lower() in l)

def snippets(t):
    p=plain(t);l=p.lower();out=[]
    for n in STONE+HINTS:
        i=l.find(n.lower())
        if i>=0:
            s=clean(p[max(0,i-300):min(len(p),i+800)],1800)
            if s not in out:out.append(s)
    return tuple(out[:12])

def main():
    print("StoneAge Waei central-download ID1/ID2 focused replay — R1")
    print("SCOPE|9 known archived HTML pages|ID1+ID2 only|no binary payload")
    errors=[];files={};stone_pages=0
    for label,ts,orig in TARGETS:
        try:
            st,final,b=fetch(replay(ts,orig))
            enc,t=decode(b);sh=hits(t,STONE);hh=hits(t,HINTS);ls=links(t,orig)
            fl=[(u,a) for u,a in ls if isfile(u)]
            if sh:stone_pages+=1
            print(f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={title(t)}|stone={clean(','.join(sh),500)}|hints={clean(','.join(hh),500)}|links={len(ls)}|file_links={len(fl)}|final={clean(final)}")
            for u,a in fl:
                files[(u,a)]=label
                print(f"FILE_LINK|label={label}|href={clean(u)}|anchor={clean(a,1200)}")
            if sh or hh:
                for s in snippets(t):
                    print(f"SNIPPET|label={label}|text={s}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    for (u,a),label in sorted(files.items()):
        print(f"FILE_SUMMARY|source={label}|href={clean(u)}|anchor={clean(a,1200)}")
    for label,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|stone_pages|{stone_pages}")
    print(f"COUNT|unique_file_links|{len(files)}")
    print(f"COUNT|errors|{len(errors)}")
    if stone_pages:
        print("RESOLUTION|STONEAGE_ID1_ID2_BINDING_FOUND|promote exact category/file association")
    elif len(errors)<len(TARGETS):
        print("RESOLUTION|ID1_ID2_REPLAY_NO_STONEAGE_TEXT|use filenames and archive directory relation only")
    else:
        print("RESOLUTION|ID1_ID2_REPLAY_FAILED|retry failed exact pages only")
    print("EVIDENCE_BOUNDARY|Archived HTML establishes catalogue association only. Linked binaries are not fetched.")

if __name__=="__main__":main()
