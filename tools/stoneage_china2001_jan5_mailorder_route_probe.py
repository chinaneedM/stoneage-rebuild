#!/usr/bin/env python3
"""Recover the original China.com Jan-2001 StoneAge mail-order article route.

Source-driven anchors:
- archived Dec-2000 StoneAge giveaway/result article proves China.com route form:
  /zh_cn/news/news1/444/YYYYMMDD/<numeric-id>.html
- a later preserved mirror reproduces an article dated 2001-01-05 titled
  "中华网游戏频道 特别推出《石器时代》的邮购服务".
- that text mentions a StoneAge topic site and registered participants of the
  trial-version giveaway; original HTML may preserve historical hrefs.

Probe only Jan-04..Jan-06 under the proven news1/444 route family. Replay only
small HTML pages. No binary payload is fetched.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
DATES=("20010104","20010105","20010106")
HOSTS=("game.china.com","game.china.com:80","www.china.com","www.china.com:80")
TOKENS=("石器时代","石器時代","邮购","郵購","试玩版","試玩版","赠送","贈送","名单","名單","专题","專題","下载","下載")
MAX_REPLAY=120

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=2*1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,text/plain,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:
            raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def prefix(host,date):
    return f"http://{host}/zh_cn/news/news1/444/{date}/"

def cdx_url(host,date):
    p=[
        ("url",prefix(host,date)),("matchType","prefix"),("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
        ("from","20010101"),("to","20010331"),
        ("limit","5000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:
        return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))

def decode(body):
    for enc in ("gb18030","gbk","gb2312","big5","utf-8","latin1"):
        try:
            return enc,body.decode(enc)
        except UnicodeDecodeError:
            pass
    return "latin1",body.decode("latin1","replace")

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def plain_text(text):
    t=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    t=re.sub(r"(?is)<style\b.*?</style>"," ",t)
    t=html.unescape(re.sub(r"(?s)<[^>]+>"," ",t))
    return re.sub(r"\s+"," ",t).strip()

def links(text,base):
    out=[]
    pat=re.compile(r"""(?is)<a\b[^>]*href\s*=\s*["']([^"']+)["'][^>]*>(.*?)</a>""")
    for m in pat.finditer(text):
        href=html.unescape(m.group(1)).strip()
        label=html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2)))
        label=re.sub(r"\s+"," ",label).strip()
        if not href or href.lower().startswith(("javascript:","mailto:","#")):
            continue
        out.append((urllib.parse.urljoin(base,href),label))
    return tuple(out)

def score(text):
    low=text.lower()
    points=0
    if "石器时代" in text or "石器時代" in text:
        points+=20
    if "邮购" in text or "郵購" in text:
        points+=15
    if "试玩版" in text or "試玩版" in text:
        points+=12
    if "赠送" in text or "贈送" in text:
        points+=6
    if "中华网游戏频道" in text or "中華網遊戲頻道" in text:
        points+=4
    if "1月12" in text or "1月12日" in text:
        points+=3
    return points

def article_id(url):
    base=urllib.parse.urlsplit(url).path.rsplit("/",1)[-1]
    if base.lower().endswith(".html"):
        base=base[:-5]
    return base if base.isdigit() else ""

def main():
    print("StoneAge China.com Jan-2001 mail-order original-route recovery — R1")
    print("SCOPE|proven news1/444 route family|2001-01-04..06 date prefixes|CDX + bounded HTML replay|no payload")
    print("TARGET_TITLE|中华网游戏频道 特别推出《石器时代》的邮购服务")
    errors=[];allrows={}

    def one(host,date):
        try:
            st,final,h,b=fetch(cdx_url(host,date),timeout=45,max_bytes=8*1024*1024)
            return host,date,st,final,b,rows(b),None
        except Exception as e:
            return host,date,None,"",b"",(),(type(e).__name__,str(e))

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures=[ex.submit(one,h,d) for h in HOSTS for d in DATES]
        results=[f.result() for f in concurrent.futures.as_completed(futures)]

    for host,date,st,final,b,rr,err in sorted(results):
        if err:
            errors.append((f"cdx:{host}:{date}",err[0],err[1]))
            print(f"QUERY_ERROR|host={clean(host)}|date={date}|kind={err[0]}|message={clean(err[1])}")
            continue
        print(f"QUERY|host={clean(host)}|date={date}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        for r in rr:
            key=(str(r.get("timestamp") or ""),str(r.get("original") or ""),str(r.get("digest") or ""))
            allrows[key]=r

    print(f"COUNT|unique_rows|{len(allrows)}")
    for (ts,orig,digest),r in sorted(allrows.items()):
        print(f"ROW|timestamp={ts}|article_id={article_id(orig)}|status={clean(r.get('statuscode'))}|mime={clean(r.get('mimetype'))}|length={clean(r.get('length'))}|digest={clean(digest)}|original={clean(orig)}")

    candidates=[]
    seen=set()
    for (ts,orig,digest),r in sorted(allrows.items()):
        if str(r.get("statuscode") or "")!="200":
            continue
        if (ts,orig) in seen:
            continue
        seen.add((ts,orig))
        candidates.append((ts,orig))
        if len(candidates)>=MAX_REPLAY:
            break

    print(f"COUNT|selected_replays|{len(candidates)}")
    matches=[]
    for ts,orig in candidates:
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=40,max_bytes=2*1024*1024)
            enc,text=decode(b)
            plain=plain_text(text)
            sc=score(plain)
            token_hits=[t for t in TOKENS if t.lower() in plain.lower()]
            hrefs=links(text,orig)
            print(f"PAGE|timestamp={ts}|article_id={article_id(orig)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|score={sc}|tokens={clean(','.join(token_hits),1000)}|links={len(hrefs)}|original={clean(orig)}")
            if sc>=20:
                matches.append((sc,ts,orig,plain,hrefs))
                for tok in ("石器时代","石器時代","邮购","郵購","试玩版","試玩版"):
                    i=plain.lower().find(tok.lower())
                    if i>=0:
                        print(f"SNIPPET|timestamp={ts}|article_id={article_id(orig)}|token={clean(tok)}|text={clean(plain[max(0,i-320):i+900],1800)}")
                for href,label in hrefs:
                    blob=(href+" "+label).lower()
                    if any(t.lower() in blob for t in ("石器","stoneage","shiqi","试玩","試玩","名单","名單","专题","專題","download","下载","下載")):
                        print(f"LINK|timestamp={ts}|article_id={article_id(orig)}|anchor={clean(label,1000)}|url={clean(href)}")
        except Exception as e:
            errors.append((f"replay:{ts}:{orig}",type(e).__name__,str(e)))

    matches.sort(reverse=True,key=lambda x:x[0])
    print(f"COUNT|matching_pages|{len(matches)}")
    for sc,ts,orig,plain,hrefs in matches:
        print(f"MATCH|score={sc}|timestamp={ts}|article_id={article_id(orig)}|original={clean(orig)}")

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if matches:
        print("RESOLUTION|CHINACOM_JAN5_STONEAGE_ARTICLE_RECOVERED|classify original hrefs and reopen only exact historical routes")
    elif allrows:
        print("RESOLUTION|CHINACOM_JAN5_ROUTE_NEIGHBORHOOD_FOUND_NO_MATCH|expand only if date/title evidence justifies adjacent route family")
    elif errors:
        print("RESOLUTION|CHINACOM_JAN5_ROUTE_PARTIAL|retry failed date-host prefixes only")
    else:
        print("RESOLUTION|CHINACOM_JAN5_PROVEN_ROUTE_UNINDEXED|seek alternate China.com namespace or preserved mirror source metadata")
    print("EVIDENCE_BOUNDARY|The modern mirror supplies title/date text only; recovered Wayback HTML is required before historical hrefs are treated as first-party routing evidence.")

if __name__=="__main__":
    main()
