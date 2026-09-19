#!/usr/bin/env python3
"""Recover sparse metadata from Inium's exact StoneAge download page /down.htm."""

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
TARGETS=(
    "http://stoneage.enium.co.kr/down.htm",
    "http://www.stoneage.enium.co.kr/down.htm",
)
DATES=("20001013","20001208","20010210","20010413","20010614","20010814")

KEY=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|자료|"
    r"설치|setup|install|client|클라이언트|patch|패치|update|업데이트|"
    r"version|버전|정식|체험|full|trial|용량|파일|"
    r"hananet|cnet|enium|inium|240\s*m|257\s*mb|260\s*m|"
    r"\.exe\b|\.zip\b|\.rar\b|\.cab\b|\.lzh\b|\.lha\b|"
    r"\b\d+(?:\.\d+){1,3}\b|\b\d+(?:\.\d+)?\s*(?:kb|mb|gb)\b)"
)
FILE_RE=re.compile(r"(?i)[a-z0-9][a-z0-9._~:/?&=%+-]{1,400}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)(?:[?&#][^\s\"'<>]*)?")
SIZE_RE=re.compile(r"(?i)\b\d{1,7}(?:[.,]\d{1,3})?\s*(?:bytes?|kb|mb|gb|m)\b")
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs=[];self.text=[];self.scripts=[];self._script=False
        self._anchor_href=None;self._anchor_text=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower(); a=dict(attrs)
        for name,value in attrs:
            if value is not None:self.attrs.append((tag,name.lower(),value))
        if tag=="a" and a.get("href"):
            self._anchor_href=a["href"];self._anchor_text=[]
        if tag=="script":self._script=True
    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag=="script":self._script=False
        if tag=="a" and self._anchor_href is not None:
            self.attrs.append(("a","anchor",self._anchor_href+" || "+" ".join(self._anchor_text).strip()))
            self._anchor_href=None;self._anchor_text=[]
    def handle_data(self,data):
        if data.strip():self.text.append(data)
        if self._script and data.strip():self.scripts.append(data)
        if self._anchor_href is not None:self._anchor_text.append(data)


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


def safe(v,limit=1200):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def normalize(base,target):
    target=target.strip()
    if not target:return ""
    if target.lower().startswith(("javascript:","mailto:","#")):return target
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def analyze(original,date):
    hit=closest(original,date)
    if not hit:return ("miss",original,date)
    ts,status,archived=hit
    data,resolved=request(replay(ts,original),timeout=12)
    text=decode(data);p=Parser();p.feed(text)
    links=set();attrs=set()
    for tag,name,value in p.attrs:
        if name=="anchor":
            href,_,label=value.partition(" || ")
            n=normalize(original,href)
            if n:links.add((tag,"href",safe(n),safe(label,360)))
            continue
        n=normalize(original,value)
        if name in ("href","src","action","data","value") and n:
            links.add((tag,name,safe(n),safe("",1)))
        if KEY.search(value) or FILE_RE.search(value) or name.startswith("on"):
            attrs.add((tag,name,safe(n or value,1400)))
    snippets=sorted({safe(x,900) for x in p.text+p.scripts if KEY.search(x) or FILE_RE.search(x) or SIZE_RE.search(x)})
    files=sorted(set(FILE_RE.findall(text)))
    sizes=sorted(set(SIZE_RE.findall("\n".join(p.text))))
    return ("ok",{
        "original":original,"requested":date,"timestamp":ts,"status":status,
        "archived":archived,"resolved":resolved,"bytes":len(data),
        "sha256":hashlib.sha256(data).hexdigest(),"links":sorted(links),
        "attrs":sorted(attrs),"snippets":snippets,"files":files,"sizes":sizes,
    })


def main():
    print("StoneAge Inium exact down.htm probe — R1")
    print("SCOPE|transient-html|all-link-metadata+sparse-text|no-client-binary-download")
    jobs=[(u,d) for u in TARGETS for d in DATES]
    results=[];errors=[];misses=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs={ex.submit(analyze,u,d):(u,d) for u,d in jobs}
        for fut,(u,d) in futs.items():
            try:
                result=fut.result()
                if result[0]=="ok":results.append(result[1])
                else:misses.append((u,d))
            except Exception as exc:errors.append((u,d,type(exc).__name__,str(exc)))
    unique={}
    for row in results:unique[(row["original"],row["timestamp"])]=row
    print(f"COUNT|queries|{len(jobs)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|misses|{len(misses)}")
    print(f"COUNT|unique_pages|{len(unique)}")
    for u,d,kind,msg in sorted(errors):
        print(f"ERROR|requested={d}|kind={kind}|url={safe(u)}|message={safe(msg)}")
    for u,d in sorted(misses):
        print(f"MISS|requested={d}|url={safe(u)}")
    for (_,ts),row in sorted(unique.items(),key=lambda x:(x[0][1],x[0][0])):
        print(
            f"PAGE|requested={row['requested']}|timestamp={ts}|status={row['status']}|"
            f"bytes={row['bytes']}|sha256={row['sha256']}|url={safe(row['original'])}|"
            f"resolved={safe(row['resolved'])}"
        )
        for token in row["files"]:print(f"FILE|timestamp={ts}|value={safe(token)}")
        for token in row["sizes"]:print(f"SIZE|timestamp={ts}|value={safe(token)}")
        for tag,name,value in row["attrs"]:
            print(f"ATTR|timestamp={ts}|tag={tag}|name={name}|value={value}")
        for tag,name,target,label in row["links"]:
            print(f"LINK|timestamp={ts}|tag={tag}|attr={name}|target={target}|label={label}")
        for value in row["snippets"]:
            print(f"TEXT|timestamp={ts}|value={value}")


if __name__=="__main__":main()
