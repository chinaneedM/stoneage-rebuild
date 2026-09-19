#!/usr/bin/env python3
"""Recover sparse metadata from the Inium /8_1.htm child page referenced by Hananet.

Hananet archived StoneAge pages repeatedly call:
    http://stoneage.enium.co.kr/8_1.htm
This probe resolves snapshots near the Hananet dates and follows a bounded set
of same-host HTML links one hop. Only hashes, matching text and links are kept.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
AVAILABLE="https://archive.org/wayback/available"
ROOT="http://stoneage.enium.co.kr/8_1.htm"
DATES=("20010126","20010226","20010814")

KEY=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|자료|"
    r"설치|setup|install|client|클라이언트|patch|패치|update|업데이트|"
    r"version|버전|회원|가입|등록|요금|결제|정식|체험|"
    r"\.exe\b|\.zip\b|\.rar\b|\.cab\b|\.lzh\b|"
    r"\b\d+(?:\.\d+){1,3}\b|\b\d+(?:\.\d+)?\s*(?:kb|mb|gb)\b)"
)
FILE_RE=re.compile(r"(?i)[a-z0-9][a-z0-9._~:/?&=%+-]{1,300}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)(?:[?&#][^\s\"'<>]*)?")
HTML_RE=re.compile(r"(?i)^https?://(?:www\.)?stoneage\.enium\.co\.kr(?::80)?/[^?#]*\.(?:htm|html)(?:[?#].*)?$")
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs=[];self.text=[];self.scripts=[]
        self._script=False
    def handle_starttag(self,tag,attrs):
        tag=tag.lower()
        for name,value in attrs:
            if value is not None:self.attrs.append((tag,name.lower(),value))
        if tag=="script":self._script=True
    def handle_endtag(self,tag):
        if tag.lower()=="script":self._script=False
    def handle_data(self,data):
        if data.strip():self.text.append(data)
        if self._script and data.strip():self.scripts.append(data)


def request(url,timeout=10):
    last=None
    for attempt in range(2):
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read(),str(getattr(r,"url",url))
        except urllib.error.HTTPError as exc:
            last=exc
            if exc.code!=429 or attempt==1:raise
            time.sleep(2)
        except (urllib.error.URLError,TimeoutError,ConnectionError) as exc:
            last=exc
            if attempt==1:raise
            time.sleep(1)
    raise RuntimeError(last)


def closest(original,date):
    q=urllib.parse.urlencode({"url":original,"timestamp":date})
    raw,_=request(AVAILABLE+"?"+q,timeout=8)
    payload=json.loads(raw.decode("utf-8","replace"))
    c=payload.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):return None
    return str(c.get("timestamp","")),str(c.get("status","")),str(c.get("url",""))


def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def safe(v,limit=1000):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def normalize(base,target):
    target=target.strip()
    if not target:return ""
    if target.lower().startswith(("javascript:","mailto:","#")):return target
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def extract_page(original,ts):
    data,resolved=request(replay(ts,original),timeout=12)
    text=decode(data)
    p=Parser();p.feed(text)
    attrs=set();children=set()
    for tag,name,value in p.attrs:
        n=normalize(original,value)
        if not n:continue
        if name in ("href","src","action") and HTML_RE.match(n):children.add(n.split("#",1)[0])
        if KEY.search(value) or FILE_RE.search(value) or name.startswith("on"):
            attrs.add((tag,name,safe(n,1200)))
    snippets=sorted({safe(x,700) for x in p.text+p.scripts if KEY.search(x) or FILE_RE.search(x)})
    files=sorted(set(FILE_RE.findall(text)))
    return {
        "original":original,"timestamp":ts,"resolved":resolved,
        "bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
        "attrs":sorted(attrs),"snippets":snippets,"files":files,
        "children":sorted(children)
    }


def main():
    print("StoneAge Inium 8_1 child-page probe — R1")
    print("SCOPE|transient-html|bounded-one-hop|hash-sparse-metadata-only|no-client-binary-download")

    root_hits=[];errors=[]
    for date in DATES:
        try:
            hit=closest(ROOT,date)
        except Exception as exc:
            errors.append(("availability",ROOT,date,type(exc).__name__,str(exc)));continue
        if hit:
            root_hits.append((date,*hit))

    print(f"COUNT|root_dates|{len(DATES)}")
    print(f"COUNT|root_available|{len(root_hits)}")

    pages={}
    for date,ts,status,archived in root_hits:
        try:
            row=extract_page(ROOT,ts)
            pages[(ROOT,ts)]=row
        except Exception as exc:
            errors.append(("root",ROOT,ts,type(exc).__name__,str(exc)))

    children=sorted({u for row in pages.values() for u in row["children"] if u.rstrip("/")!=ROOT.rstrip("/")})
    print(f"COUNT|one_hop_candidates|{len(children)}")

    child_jobs=[]
    for child in children[:40]:
        for date in ("20010210","20010814"):
            child_jobs.append((child,date))

    def resolve_child(job):
        child,date=job
        try:
            hit=closest(child,date)
            if not hit:return ("miss",child,date)
            ts,status,archived=hit
            row=extract_page(child,ts)
            return ("ok",child,date,status,archived,row)
        except Exception as exc:
            return ("error",child,date,type(exc).__name__,str(exc))

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for result in ex.map(resolve_child,child_jobs):
            if result[0]=="ok":
                _,child,date,status,archived,row=result
                pages[(child,row["timestamp"])]=row
            elif result[0]=="error":
                _,child,date,kind,msg=result
                errors.append(("child",child,date,kind,msg))

    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|unique_pages|{len(pages)}")
    for phase,url,marker,kind,msg in sorted(errors):
        print(f"ERROR|phase={phase}|marker={marker}|kind={kind}|url={safe(url)}|message={safe(msg)}")

    for (original,ts),row in sorted(pages.items()):
        print(f"PAGE|timestamp={ts}|bytes={row['bytes']}|sha256={row['sha256']}|url={safe(original)}|resolved={safe(row['resolved'])}")
        for token in row["files"]:print(f"FILE|url={safe(original)}|value={safe(token)}")
        for child in row["children"]:print(f"CHILD|url={safe(original)}|target={safe(child)}")
        for tag,name,value in row["attrs"]:
            print(f"ATTR|url={safe(original)}|tag={tag}|name={name}|value={value}")
        for value in row["snippets"]:print(f"TEXT|url={safe(original)}|value={value}")


if __name__=="__main__":main()
