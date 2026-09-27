#!/usr/bin/env python3
"""Inspect archived Sina download.pl neighbor HTML for historical file-server routing.

The existing aid=61620 neighborhood probe recovered several nearby download.pl
captures but only inspected HTTP headers. Those captures are HTML documents,
so this follow-up parses their bounded bodies for href/src/form/meta/JS URLs and
download-context snippets. It never fetches a linked payload.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
SAMPLES=(
    ("aid61002","20030118181435","http://games1.sina.com.cn:80/cgi-bin/games/downgames/download.pl?col=bizhi&aid=61002&title=%A1%B6XIII%A1%B7%B1%DA%D6%BD%BE%AB%D1%A1&filename=wallpaper_tron_20_03_1024.jpg&size=63"),
    ("aid60883","20030123093354","http://games1.sina.com.cn:80/cgi-bin/games/downgames/download.pl?col=bizhi&aid=60883&title=%A1%B6capcom+vs+snk%A1%B7%B1%DA%D6%BD%BE%AB%D1%A1&filename=capcom1029_800_2.jpg&size=43"),
    ("aid63173","20021219003322","http://games1.sina.com.cn:80/cgi-bin/games/downgames/download.pl?col=bizhi&aid=63173&title=%A1%B6%C4%A7%BD%A3%A1%B7%B1%DA%D6%BD%BE%AB%D1%A1&filename=taiwan_s5_800.jpg&size=46"),
    ("aid60043","20021216172436","http://games1.sina.com.cn:80/cgi-bin/games/downgames/download.pl?col=bizhi&aid=60043&title=%D6%DC%C4%A9%B1%DA%D6%BD%BE%AB%D1%A1%B7%EE%CF%D7&filename=bizhi1017_800_1.jpg&size=55"),
)
URLISH=re.compile(
    r'''(?is)(?:href|src|action)\s*=\s*["']([^"']+)["']'''
    r'''|(?:window\.open|location(?:\.href)?\s*=|window\.location\s*=)\s*\(?\s*["']([^"']+)["']'''
)
ABS=re.compile(r'''(?i)(?:https?|ftp)://[^\s"'<>]+''')
FILE_EXTS=(".exe",".zip",".rar",".cab",".jpg",".jpeg",".gif",".png",".bmp",".mid",".wav",".mp3")


def clean(v,n=4000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=25,max_bytes=128*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain,*/*;q=0.3","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b


def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode(b):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try:return b.decode(enc)
        except UnicodeDecodeError:pass
    return b.decode("latin1","replace")


def refs(text,base):
    out=[]
    for m in URLISH.finditer(text):
        raw=(m.group(1) or m.group(2) or "").strip()
        if raw and not raw.startswith(("javascript:","mailto:","#")):
            out.append(urllib.parse.urljoin(base,html.unescape(raw)))
    for m in ABS.finditer(text):
        out.append(html.unescape(m.group(0)).rstrip("),.;"))
    return tuple(dict.fromkeys(out))


def score(url,source_host="games1.sina.com.cn"):
    p=urllib.parse.urlsplit(url)
    low=urllib.parse.unquote_plus(url).lower()
    leaf=p.path.rsplit("/",1)[-1]
    s=0
    if (p.hostname or "").lower()!=source_host:s+=4
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}",p.hostname or ""):s+=6
    if leaf.lower().endswith(FILE_EXTS):s+=4
    if any(t in low for t in ("download","downfiles","/down/","file","soft","ftp","upload")):s+=3
    if "games1.sina.com.cn/cgi-bin/games/downgames/download.pl" in low:s-=8
    return s


def contexts(text,filename):
    plain=re.sub(r"(?s)<[^>]+>"," ",text)
    plain=html.unescape(re.sub(r"\s+"," ",plain))
    toks=(filename,"下载","download","本地下载","服务器","镜像","地址")
    out=[];seen=set();low=plain.lower()
    for tok in toks:
        pos=0;t=tok.lower()
        while True:
            i=low.find(t,pos)
            if i<0:break
            snip=clean(plain[max(0,i-160):min(len(plain),i+len(tok)+220)],500)
            if snip not in seen:
                seen.add(snip);out.append((tok,snip))
            pos=i+max(1,len(t))
            if len(out)>=12:return tuple(out)
    return tuple(out)


def main():
    print("StoneAge Sina download.pl neighbor-body routing probe — R1")
    print("SCOPE|4 exact archived neighbor CGI HTML bodies|href/src/form/JS/context only|no-linked-payload")
    errors=[];all_scored={}
    for label,ts,orig in SAMPLES:
        try:
            st,final,h,b=fetch(replay(ts,orig))
            text=decode(b)
            filename=dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(orig).query)).get("filename","")
            rr=refs(text,orig)
            ranked=sorted(((score(u),u) for u in rr if score(u)>0),key=lambda x:(-x[0],x[1]))
            print(f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|refs={len(rr)}|scored={len(ranked)}|final={clean(final)}")
            for tok,snip in contexts(text,filename):
                print(f"CONTEXT|label={label}|token={clean(tok,120)}|text={snip}")
            for s,u in ranked[:40]:
                all_scored[u]=max(all_scored.get(u,0),s)
                print(f"ROUTE_REF|label={label}|score={s}|url={clean(u)}")
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    hosts={}
    dirs={}
    for u,s in all_scored.items():
        p=urllib.parse.urlsplit(u)
        host=p.hostname or ""
        hosts[host]=hosts.get(host,0)+1
        if p.path:
            d=p.path.rsplit("/",1)[0]+"/"
            dirs[(p.scheme,host,d)]=dirs.get((p.scheme,host,d),0)+1
    for host,n in sorted(hosts.items(),key=lambda kv:(-kv[1],kv[0])):
        print(f"ROUTE_HOST|count={n}|host={clean(host)}")
    for (scheme,host,d),n in sorted(dirs.items(),key=lambda kv:(-kv[1],kv[0])):
        if n>=2:
            print(f"ROUTE_DIR|count={n}|url={clean(f'{scheme}://{host}{d}')}")
    print(f"COUNT|unique_scored_refs|{len(all_scored)}")
    print(f"COUNT|errors|{len(errors)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    strong=[(s,u) for u,s in all_scored.items() if s>=7]
    if strong:
        print("RESOLUTION|NEIGHBOR_BODY_DOWNLOAD_TOPOLOGY_FOUND|use repeated host/directory templates for bounded aid=61620 synthesis")
    elif all_scored:
        print("RESOLUTION|NEIGHBOR_BODY_WEAK_ROUTING_ONLY|do not synthesize target path without stronger repeated template")
    elif errors:
        print("RESOLUTION|NEIGHBOR_BODY_REPLAY_INCOMPLETE|retry only failed exact sample")
    else:
        print("RESOLUTION|NO_FILE_SERVER_ROUTE_IN_NEIGHBOR_BODIES|close body-template route")
    print("EVIDENCE_BOUNDARY|Archived neighbor HTML is topology evidence only; target-file identity requires an exact target capture or independently preserved bytes.")


if __name__=="__main__":
    main()
