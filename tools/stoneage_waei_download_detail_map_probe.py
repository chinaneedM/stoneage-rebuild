#!/usr/bin/env python3
"""Map Waei central-download detail IDs 1..6 to titles and file links.

Uses only archived HTML pages from www7.waei.net/download/dldetial.asp.
No binary payload is downloaded.
"""
from __future__ import annotations
import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://www7.waei.net/download/dldetial.asp"
FROM="20010101"; TO="20010630"
MAX_BODY=1024*1024
STONE=("stoneage","stone age","石器時代","石器时代","石器")
FILE_HINTS=("spr_1.bin","adrn_1.bin","real_1.bin","spradrn_1.bin","stoneage.exe")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=MAX_BODY):
    req=urllib.request.Request(url,headers={
      "User-Agent":UA,
      "Accept":"application/json,text/html,text/plain,*/*;q=0.2",
      "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def cdx_url():
    params=[
      ("url",PREFIX),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from",FROM),("to",TO),("filter","statuscode:200"),("limit","5000")
    ]
    return CDX+"?"+urllib.parse.urlencode(params)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    h=obj[0]
    return tuple(dict(zip(h,r)) for r in obj[1:] if isinstance(r,list))

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def decode(body):
    for enc in ("big5","gb18030","gbk","utf-8","latin1"):
        try:return enc,body.decode(enc)
        except UnicodeDecodeError:pass
    return "latin1",body.decode("latin1","replace")

def plain(text):
    p=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",text)
    p=html.unescape(re.sub(r"(?s)<[^>]+>"," ",p))
    return re.sub(r"\s+"," ",p)

def title(text):
    m=re.search(r"(?is)<title[^>]*>(.*?)</title>",text)
    return clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(1))) if m else "",500)

def params(url):
    q=urllib.parse.parse_qs(urllib.parse.urlsplit(str(url)).query.replace("%26","&"))
    i=(q.get("ID") or q.get("id") or [""])[0]
    xp=(q.get("xPage") or q.get("xpage") or [""])[0]
    order=(q.get("order") or [""])[0]
    return str(i),str(xp),str(order)

def links(text,base):
    out=[]
    for m in re.finditer(r'(?is)<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',text):
        href=html.unescape(m.group(1)).strip()
        anchor=clean(html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2))),1200)
        if not href or href.lower().startswith(("javascript:","mailto:","#")):continue
        out.append((urllib.parse.urljoin(base,href),anchor))
    return tuple(out)

def is_file_link(url):
    p=urllib.parse.urlsplit(str(url)).path.lower()
    return "/download/file/" in p or p.endswith((".exe",".zip",".rar",".cab",".bin",".dat",".doc",".wmv",".avi"))

def stone_hits(text):
    l=plain(text).lower()
    return tuple(t for t in STONE if t.lower() in l)

def hint_hits(text):
    l=text.lower()
    return tuple(h for h in FILE_HINTS if h.lower() in l)

def snippets(text):
    p=plain(text);low=p.lower();out=[]
    for n in list(STONE)+list(FILE_HINTS):
        start=0;nl=n.lower()
        while True:
            i=low.find(nl,start)
            if i<0:break
            s=clean(p[max(0,i-240):min(len(p),i+520)],1400)
            if s not in out:out.append(s)
            start=i+max(1,len(n))
    return tuple(out[:16])

def main():
    print("StoneAge Waei central-download detail map — R1")
    print(f"SCOPE|{FROM}..{TO}|detail IDs 1..6|archived HTML only|no binary payload")
    errors=[]
    try:
        st,final,h,b=fetch(cdx_url(),timeout=60,max_bytes=8*1024*1024)
        rr=rows(b)
        print(f"CDX|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
    except Exception as e:
        rr=();errors.append(("cdx",type(e).__name__,str(e)))

    selected=[]
    seen=set()
    for r in rr:
        i,xp,order=params(r.get("original"))
        if i not in {"1","2","3","4","5","6"}:continue
        if "html" not in str(r.get("mimetype") or "").lower():continue
        key=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
        if key in seen:continue
        seen.add(key);selected.append((i,xp,order,r))
    selected.sort(key=lambda x:(int(x[0]),x[1],x[2],str(x[3].get("timestamp") or "")))
    print(f"COUNT|selected_pages|{len(selected)}")

    replayed=0;stone_pages=0;file_links={}
    for idx,(i,xp,order,r) in enumerate(selected,1):
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=35,max_bytes=MAX_BODY)
            enc,text=decode(b);replayed+=1
            sh=stone_hits(text);hh=hint_hits(text);ls=links(text,orig)
            fl=[(u,a) for u,a in ls if is_file_link(u)]
            if sh:stone_pages+=1
            print(f"PAGE|index={idx}|id={i}|xpage={clean(xp)}|order={clean(order)}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|title={title(text)}|stone={clean(','.join(sh),500)}|hints={clean(','.join(hh),500)}|links={len(ls)}|file_links={len(fl)}|original={clean(orig)}")
            for u,a in fl:
                file_links[(u,a)]=(i,ts,orig)
                print(f"FILE_LINK|id={i}|timestamp={ts}|href={clean(u)}|anchor={clean(a,1000)}")
            if sh or hh:
                for s in snippets(text):
                    print(f"SNIPPET|id={i}|timestamp={ts}|text={s}")
        except Exception as e:
            errors.append((f"page:{i}:{ts}:{orig}",type(e).__name__,str(e)))

    # summarize files per detail ID
    per={}
    for (u,a),(i,ts,orig) in file_links.items():
        per.setdefault(i,set()).add(u)
    for i in sorted(per,key=int):
        print(f"ID_FILES|id={i}|count={len(per[i])}|files={';'.join(sorted(per[i]))}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|pages_replayed|{replayed}")
    print(f"COUNT|stone_pages|{stone_pages}")
    print(f"COUNT|unique_file_links|{len(file_links)}")
    print(f"COUNT|errors|{len(errors)}")
    if stone_pages:
        print("RESOLUTION|STONEAGE_DETAIL_PAGE_FOUND|bind exact file links and version semantics next")
    elif replayed:
        print("RESOLUTION|DETAIL_MAP_RECOVERED_NO_STONEAGE_TEXT|use file-name/directory crosswalk and neighboring page captures")
    else:
        print("RESOLUTION|DETAIL_REPLAY_INCOMPLETE|retry only failed exact captures")
    print("EVIDENCE_BOUNDARY|Detail-page text and links establish catalogue association only; linked binary payloads are not fetched by this probe.")

if __name__=="__main__":main()
