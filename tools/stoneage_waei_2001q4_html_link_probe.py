#!/usr/bin/env python3
"""Replay a bounded set of archived Waei StoneAge2 HTML pages and extract download links.

URL-name topology can miss a software link when the page itself has a neutral
name. This probe uses the Q4-2001 CDX prefix as an evidence-anchored page set,
selects shallow/relevant HTML pages, replays at their exact capture timestamp,
then extracts links whose href or anchor text indicates StoneAge client/download/
complete-upgrade semantics. HTML only; no binary payload is downloaded.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://www.waei.com.cn/ZHUANQU/stoneage2/"
MAX_PAGES=48
PAGE_HINTS=("index","default","main","news","new","notice","announce","guide","help","tyro","begin","start","home","stoneage2","sa2")
LINK_TOKENS=("下载","客户端","完整升级","升级版","更新版","安装","download","client","setup",".exe",".zip",".cab",".rar","stoneage2.0setup")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=35,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,application/json,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url():
    p=[
      ("url",PREFIX),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length"),
      ("from","20011001"),("to","20011231"),("collapse","urlkey"),("limit","20000"),
      ("filter","statuscode:200"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))

def decode(b):
    for enc in ("gb18030","big5","utf-8","latin1"):
        try:return b.decode(enc)
        except UnicodeDecodeError:pass
    return b.decode("latin1","replace")

def score_page(url):
    p=urllib.parse.urlsplit(url).path.lower()
    root=urllib.parse.urlsplit(PREFIX).path.lower().rstrip("/")+"/"
    rel=p
    if rel.startswith(root): rel=rel[len(root):]
    depth=rel.count("/")
    leaf=rel.rsplit("/",1)[-1]
    s=max(0,6-depth*2)
    if not leaf or leaf in ("index.htm","index.html","index.asp","default.asp","default.htm","main.asp","main.htm"):s+=10
    if any(h in rel for h in PAGE_HINTS):s+=4
    if leaf.endswith((".asp",".htm",".html",".shtml")):s+=2
    return s

def html_candidate(r):
    mt=str(r.get("mimetype") or "").lower()
    u=str(r.get("original") or "")
    p=urllib.parse.urlsplit(u).path.lower()
    return ("html" in mt or p.endswith((".asp",".htm",".html",".shtml")) or p.endswith("/"))

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def links(text,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',text):
        href=html.unescape(m.group(1)).strip()
        anchor=re.sub(r"(?s)<[^>]+>"," ",m.group(2))
        anchor=html.unescape(re.sub(r"\s+"," ",anchor)).strip()
        if not href or href.startswith(("javascript:","mailto:","#")):continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)

def targetish(href,anchor):
    low=(urllib.parse.unquote_plus(str(href))+" "+str(anchor)).lower()
    return any(t.lower() in low for t in LINK_TOKENS)

def main():
    print("StoneAge Beijing-Waei Q4-2001 archived HTML download-link probe — R1")
    print(f"SCOPE|official stoneage2 prefix|selected archived HTML pages|max_pages={MAX_PAGES}|link extraction only|no-payload")
    errors=[]
    try:
        st,final,b=fetch(cdx_url(),max_bytes=8*1024*1024)
        rr=rows(b)
        print(f"CDX|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
    except Exception as e:
        errors.append(("cdx",type(e).__name__,str(e)));rr=()
    candidates=[r for r in rr if html_candidate(r)]
    candidates.sort(key=lambda r:(score_page(str(r.get("original") or "")),str(r.get("timestamp") or "")),reverse=True)
    selected=candidates[:MAX_PAGES]
    print(f"COUNT|html_candidates|{len(candidates)}")
    print(f"COUNT|selected_pages|{len(selected)}")
    hits=[];replayed=0
    for i,r in enumerate(selected,1):
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),max_bytes=768*1024)
            replayed+=1
            txt=decode(b); ls=links(txt,orig)
            th=[(u,a) for u,a in ls if targetish(u,a)]
            print(f"PAGE|index={i}|score={score_page(orig)}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|orig={clean(orig)}|links={len(ls)}|target_links={len(th)}")
            for u,a in th:
                hits.append((orig,u,a))
                print(f"LINK_HIT|page={clean(orig)}|href={clean(u)}|anchor={clean(a,1200)}")
        except Exception as e:
            errors.append((f"page:{i}:{orig}",type(e).__name__,str(e)))
    uniq={}
    for page,u,a in hits:uniq[(u,a)]=page
    exact=[(u,a) for u,a in uniq if "stoneage2.0setup" in urllib.parse.unquote_plus(u).lower()]
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|unique_target_links|{len(uniq)}")
    print(f"COUNT|exact_sina_filename_links|{len(exact)}")
    for s,k,m in errors:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if exact:
        print("RESOLUTION|EXACT_SETUP_LINK_FOUND_ON_OFFICIAL_HTML|classify archived target route before any payload recovery")
    elif uniq:
        print("RESOLUTION|OFFICIAL_HTML_DOWNLOAD_LINKS_FOUND|classify links for 2.0 client/update relevance")
    elif errors and replayed==0:
        print("RESOLUTION|OFFICIAL_HTML_REPLAY_INCOMPLETE|do not close page-content route")
    else:
        print("RESOLUTION|NO_CLIENT_DOWNLOAD_LINK_ON_SELECTED_HTML|selected shallow/relevant official pages expose no client/download link")
    print("EVIDENCE_BOUNDARY|archived HTML links are routing/distribution evidence only; no linked binary is downloaded or promoted without separate byte verification.")

if __name__=="__main__":
    main()
