#!/usr/bin/env python3
"""Probe the preserved 17173 StoneAge 2.5 page topology for real payload hrefs.

R2 found a same-site route from sa25-up.htm to sa25.htm. This R3 probe treats
HTML routes separately from payload candidates and inspects the 2.5 page family
without downloading any client bytes.
"""
from __future__ import annotations
import concurrent.futures, hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
AVAIL="https://archive.org/wayback/available"
HOST="stoneage.17173.com"
PATHS=(
    "/banben/sa25.htm",
    "/banben/sa25-up.htm",
    "/banben/sa25-cp.htm",
)
DATES=("20040115","20040811","20041201")
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".msi",".001",".002",".iso",".bin",".cue")
NOISE=("comment.cgi","/comment/","javascript:","mailto:")
HINTS=("download","/down/","update","upgrade","patch","setup","client")


def clean(v,limit=2400):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b


def decode_html(body):
    head=body[:16384].lower()
    m=re.search(br"""charset\s*=\s*["']?\s*([a-z0-9._-]+)""",head)
    declared=m.group(1).decode("ascii","ignore") if m else ""
    aliases={"gb2312":"gb18030","gbk":"gb18030","utf8":"utf-8","utf-8":"utf-8","big5":"big5"}
    candidates=[]
    if declared: candidates.append(aliases.get(declared,declared))
    for enc in ("gb18030","utf-8","big5"):
        if enc not in candidates: candidates.append(enc)
    best=None
    for enc in candidates:
        try: text=body.decode(enc,"replace")
        except LookupError: continue
        score=text.count("\ufffd")
        if best is None or score<best[0]: best=(score,enc,text)
    return (best[2],best[1]) if best else (body.decode("latin1","replace"),"latin1")


def avail(path,date):
    original=f"http://{HOST}{path}"
    url=AVAIL+"?"+urllib.parse.urlencode({"url":original,"timestamp":date})
    try:
        st,final,b=fetch(url,12)
        obj=json.loads(b.decode("utf-8","replace"))
        c=(obj.get("archived_snapshots") or {}).get("closest") or {}
        return path,date,st,b,c,None
    except Exception as e:
        return path,date,None,b"",{},(type(e).__name__,str(e))


def classify_href(base,href):
    absolute=urllib.parse.urljoin(base,html.unescape(href).strip())
    low=urllib.parse.unquote_plus(absolute).lower()
    if any(n in low for n in NOISE):
        return absolute,"noise"
    p=urllib.parse.urlsplit(low)
    path=p.path
    if p.netloc.endswith("17173.com") and path.lower().endswith((".htm",".html",".asp",".shtml")):
        return absolute,"route"
    if "waei.com.cn" in p.netloc:
        return absolute,"payload_candidate"
    if any(path.endswith(ext) for ext in PAYLOAD_EXTS):
        return absolute,"payload_candidate"
    if any(h in p.netloc+p.path for h in HINTS):
        return absolute,"payload_candidate"
    if p.netloc and not p.netloc.endswith("17173.com") and p.scheme in ("http","https","ftp"):
        return absolute,"external"
    return absolute,"other"


def main():
    print("StoneAge 2.5 17173 historical topology probe — R3")
    print("SCOPE|17173-sa25-page-family|Availability+replay|route-vs-payload-classification|no-client-payload")
    print("R2_CORRECTION|sa25.htm is an HTML route, not a client payload; R3 classifies it separately.")
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        futs=[ex.submit(avail,p,d) for p in PATHS for d in DATES]
        rows=[f.result() for f in concurrent.futures.as_completed(futs)]
    captures={}
    errors=[]
    for path,date,st,b,c,err in sorted(rows):
        if err:
            errors.append((f"{path}:{date}",err[0],err[1]))
            print(f"AVAIL_ERROR|path={path}|requested={date}|kind={clean(err[0])}|message={clean(err[1])}")
            continue
        ts=str(c.get("timestamp") or "")
        url=str(c.get("url") or "")
        status=str(c.get("status") or "")
        available=bool(c.get("available"))
        bounded=bool(ts and ts[:4] in ("2002","2003","2004"))
        print(f"AVAIL|path={path}|requested={date}|available={int(available)}|capture_ts={clean(ts)}|capture_status={clean(status)}|bounded={int(bounded)}|capture_url={clean(url)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        if available and status=="200" and bounded:
            m=re.search(r"/web/\d+(?:id_)?/(.+)$",url)
            original=m.group(1) if m else f"http://{HOST}{path}"
            captures[(ts,original)]=path
    print(f"COUNT|unique_captures|{len(captures)}")
    route_set=set()
    payload_set=set()
    external_set=set()
    replay_errors=[]
    for (ts,original),path in sorted(captures.items()):
        u=f"https://web.archive.org/web/{ts}id_/{original}"
        try:
            st,final,b=fetch(u,15)
            raw,enc=decode_html(b)
            hrefs=re.findall(r"""(?is)href\s*=\s*["']([^"']+)["']""",raw)
            counts={"route":0,"payload_candidate":0,"external":0,"other":0,"noise":0}
            classified=[]
            for href in hrefs:
                absolute,kind=classify_href(original,href)
                counts[kind]=counts.get(kind,0)+1
                if kind in ("route","payload_candidate","external"):
                    classified.append((href,absolute,kind))
                    if kind=="route": route_set.add(absolute)
                    elif kind=="payload_candidate": payload_set.add(absolute)
                    elif kind=="external": external_set.add(absolute)
            print(f"REPLAY|path={path}|timestamp={ts}|source={clean(original)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|hrefs={len(hrefs)}|routes={counts['route']}|payload_candidates={counts['payload_candidate']}|external={counts['external']}|final={clean(final)}")
            for href,absolute,kind in classified:
                print(f"{kind.upper()}_HREF|path={path}|timestamp={ts}|href={clean(href)}|absolute={clean(absolute)}")
        except Exception as e:
            replay_errors.append((f"{path}:{ts}",type(e).__name__,str(e)))
            print(f"REPLAY_ERROR|path={path}|timestamp={ts}|kind={type(e).__name__}|message={clean(e)}")
    for scope,kind,msg in errors+replay_errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|routes|{len(route_set)}")
    print(f"COUNT|payload_candidates|{len(payload_set)}")
    print(f"COUNT|external_links|{len(external_set)}")
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|replay_errors|{len(replay_errors)}")
    if payload_set:
        print("RESOLUTION|PAYLOAD_TARGET_FOUND|validate exact target archive/bytes next")
    elif captures:
        print("RESOLUTION|PAGE_FAMILY_RECOVERED_NO_PAYLOAD_HREF|17173 topology yields navigation/external references but no qualifying client payload")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_CAPTURE|archive service incomplete")
    else:
        print("RESOLUTION|NO_BOUNDED_CAPTURE|no 2002-2004 page-family capture found")


if __name__=="__main__":
    main()
