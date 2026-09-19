#!/usr/bin/env python3
"""Locate Inium's archived trial-client menu/page without downloading client binaries."""

from __future__ import annotations

import concurrent.futures
import html.parser
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
AVAIL="https://archive.org/wayback/available"
DATES=["20010413","20010614","20010801"]
PAGES=[
    "sitemap.htm","main_1.htm","main_2.htm","main_3.htm","main_3_2.htm","main_3_3.htm",
    "main_4.htm","main_4_2.htm","main_4_3.htm","main_5.htm","main_6.htm","main_7.htm",
    "main_8.htm","main_9.htm","main_hot.htm",
]
ROOT="http://stoneage.enium.co.kr/"
KEY=re.compile(r"(?i)(체험|trial|demo|다운로드|download|sa_demo|\.exe|\.zip)")
PAGE_EXT=(".htm",".html",".asp",".cgi")
MAX_CHILDREN=160


class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.text=[]
        self._href=None
        self._a=[]

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        tag=tag.lower()
        if tag=="a" and a.get("href"):
            self._href=a["href"]
            self._a=[]
        for k in ("src","action","onclick"):
            if a.get(k):
                self.links.append((tag,k,a[k],""))

    def handle_data(self,d):
        if d.strip():
            self.text.append(d)
        if self._href is not None:
            self._a.append(d)

    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.links.append(("a","href",self._href," ".join(self._a).strip()))
            self._href=None
            self._a=[]


def get(url,timeout=12,attempts=3):
    last=None
    for attempt in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last=exc
            if attempt+1<attempts:
                time.sleep(0.6*(attempt+1))
    raise last


def availability(url,date):
    q=urllib.parse.urlencode({"url":url,"timestamp":date})
    o=json.loads(get(AVAIL+"?"+q,8).decode("utf-8","replace"))
    c=o.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):
        return None
    ts=str(c.get("timestamp",""))
    if not ts:
        return None
    return {
        "timestamp":ts,
        "archive_url":str(c.get("url","")),
        "status":str(c.get("status","")),
    }


def replay_urls(ts,url,archive_url=""):
    out=[]
    if archive_url:
        normalized=archive_url.replace("http://web.archive.org/","https://web.archive.org/",1)
        out.append(normalized)
    out.extend([
        f"https://web.archive.org/web/{ts}id_/{url}",
        f"https://web.archive.org/web/{ts}/{url}",
    ])
    dedup=[]
    seen=set()
    for value in out:
        if value not in seen:
            seen.add(value)
            dedup.append(value)
    return dedup


def fetch_replay(ts,url,archive_url=""):
    errors=[]
    for candidate in replay_urls(ts,url,archive_url):
        try:
            return get(candidate,15,attempts=2),candidate
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
    raise RuntimeError("; ".join(errors))


def decode(b):
    for enc in ("utf-8","cp949","euc-kr"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("latin-1","replace")


def safe(v,n=700):
    v=" ".join(str(v).split())
    return "".join(c for c in v if c>=" " and c!="\x7f").replace("|","%7C")[:n]


def same_site_page(base,target):
    if not target or target.lower().startswith(("javascript:","mailto:","#")):
        return None
    absolute=urllib.parse.urljoin(base,target)
    p=urllib.parse.urlsplit(absolute)
    host=(p.hostname or "").lower()
    if host not in {"stoneage.enium.co.kr","www.stoneage.enium.co.kr"}:
        return None
    path=p.path.lower()
    if not (path.endswith(PAGE_EXT) or path.endswith("/")):
        return None
    return urllib.parse.urlunsplit((p.scheme or "http",p.netloc,p.path,p.query,""))


def analyze(url,cap):
    ts=cap["timestamp"]
    body,used=fetch_replay(ts,url,cap.get("archive_url",""))
    text=decode(body)
    p=P()
    p.feed(text)
    hits=[]
    children=set()
    for tag,attr,target,label in p.links:
        absolute=urllib.parse.urljoin(url,target) if not target.lower().startswith("javascript:") else target
        if KEY.search(absolute+" "+label):
            hits.append(("LINK",tag,attr,absolute,label))
        if tag=="a" and attr=="href":
            child=same_site_page(url,target)
            if child:
                children.add(child)
    for t in p.text:
        line=safe(t,300)
        if KEY.search(line):
            hits.append(("TEXT","","",line,""))
    return hits,children,used


def locate(jobs):
    available=[]
    errors=[]
    def one(x):
        label,date,url=x
        try:
            return label,date,url,availability(url,date),None
        except Exception as exc:
            return label,date,url,None,(type(exc).__name__,str(exc))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for label,date,url,cap,err in ex.map(one,jobs):
            if err:
                errors.append(("availability",label,date,err[0],err[1]))
            elif cap:
                available.append((label,date,url,cap))
    return available,errors


def main():
    print("StoneAge Inium trial-menu locator — R2")
    print("SCOPE|archived-menu-and-child-page-metadata-only|no-client-binary-download")
    print("METHOD|availability+multi-replay-fallback+one-hop-same-site-page-discovery")

    seed_jobs=[(page,date,ROOT+page) for page in PAGES for date in DATES]
    seed_av,errors=locate(seed_jobs)
    seed_unique={}
    for page,date,url,cap in seed_av:
        seed_unique[(url,cap["timestamp"])]=(page,date,url,cap)

    found=[]
    child_jobs={}
    seed_ok=0
    for page,date,url,cap in sorted(seed_unique.values(),key=lambda x:(x[0],x[3]["timestamp"])):
        try:
            hits,children,used=analyze(url,cap)
            seed_ok+=1
        except Exception as exc:
            errors.append(("replay",page,cap["timestamp"],type(exc).__name__,str(exc)))
            continue
        for h in hits:
            found.append(("seed",page,cap["timestamp"])+h+(used,))
        for child in children:
            child_jobs.setdefault((child,date),(child,date,child))

    selected=[child_jobs[k] for k in sorted(child_jobs)[:MAX_CHILDREN]]
    child_av,child_errors=locate(selected)
    errors.extend(child_errors)
    child_unique={}
    for label,date,url,cap in child_av:
        child_unique[(url,cap["timestamp"])]=(label,date,url,cap)

    child_ok=0
    for label,date,url,cap in sorted(child_unique.values(),key=lambda x:(x[0],x[3]["timestamp"])):
        try:
            hits,_,used=analyze(url,cap)
            child_ok+=1
        except Exception as exc:
            errors.append(("child-replay",label,cap["timestamp"],type(exc).__name__,str(exc)))
            continue
        page=urllib.parse.urlsplit(url).path.lstrip("/") or url
        for h in hits:
            found.append(("child",page,cap["timestamp"])+h+(used,))

    print(f"COUNT|seed_availability_queries|{len(seed_jobs)}")
    print(f"COUNT|seed_available_snapshots|{len(seed_unique)}")
    print(f"COUNT|seed_replay_success|{seed_ok}")
    print(f"COUNT|discovered_internal_page_jobs|{len(child_jobs)}")
    print(f"COUNT|child_jobs_selected|{len(selected)}")
    print(f"COUNT|child_available_snapshots|{len(child_unique)}")
    print(f"COUNT|child_replay_success|{child_ok}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|trial_download_hits|{len(found)}")

    for phase,page,marker,kind,msg in errors:
        print(
            f"ERROR|phase={safe(phase)}|page={safe(page)}|marker={safe(marker)}|"
            f"kind={safe(kind)}|message={safe(msg)}"
        )
    for scope,page,ts,kind,tag,attr,value,label,used in sorted(found):
        print(
            f"HIT|scope={scope}|page={safe(page)}|timestamp={safe(ts)}|kind={kind}|tag={tag}|attr={attr}|"
            f"value={safe(value)}|label={safe(label,250)}|replay={safe(used,350)}"
        )


if __name__=="__main__":
    main()
