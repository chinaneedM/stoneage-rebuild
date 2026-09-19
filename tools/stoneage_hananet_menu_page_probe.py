#!/usr/bin/env python3
"""Fetch exact archived Hananet StoneAge menu pages and emit sparse link/text metadata."""

from __future__ import annotations

import concurrent.futures
import hashlib
import html.parser
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
PAGES=[
    ("1","20010118211100","http://stoneage.hananet.net/1.htm"),
    ("2","20010226185448","http://stoneage.hananet.net/2.htm"),
    ("2_2","20010226182509","http://stoneage.hananet.net/2_2.htm"),
    ("2_3","20010126160100","http://stoneage.hananet.net/2_3.htm"),
    ("2_4","20010123223000","http://stoneage.hananet.net/2_4.htm"),
]
KEY=re.compile(r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|설치|setup|install|client|patch|update|\.exe\b|\.zip\b|\.rar\b|\.cab\b|\b\d+(?:\.\d+)?\s*(?:kb|mb|gb)\b)")
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.text=[]
        self._href=None
        self._anchor=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower(); attrs=dict(attrs)
        if tag=="a" and attrs.get("href"):
            self._href=attrs["href"]; self._anchor=[]
        elif attrs.get("href"):
            self.links.append((tag,"href",attrs["href"],attrs.get("alt") or attrs.get("title") or ""))
        for attr in ("src","action"):
            if attrs.get(attr):
                self.links.append((tag,attr,attrs[attr],attrs.get("alt") or attrs.get("title") or ""))
    def handle_data(self,data):
        if data.strip(): self.text.append(data)
        if self._href is not None: self._anchor.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.links.append(("a","href",self._href," ".join(self._anchor).strip()))
            self._href=None; self._anchor=[]


def replay(ts,original):
    return f"https://web.archive.org/web/{ts}id_/{original}"


def request(url,timeout=15):
    last=None
    for attempt in range(4):
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as exc:
            last=exc
            if exc.code!=429 or attempt==3: raise
            time.sleep(3*(attempt+1))
        except (urllib.error.URLError,TimeoutError,ConnectionError) as exc:
            last=exc
            if attempt==3: raise
            time.sleep(2*(attempt+1))
    raise RuntimeError(last)


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def normalize(base,target):
    target=target.strip()
    if not target or target.startswith(("javascript:","mailto:","#")): return ""
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def safe(v,limit=700):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def analyze(page):
    label,ts,original=page
    data=request(replay(ts,original))
    p=Parser(); p.feed(decode(data))
    links=set()
    for tag,attr,target,anchor in p.links:
        n=normalize(original,target)
        if n:
            links.add((tag,attr,safe(n),safe(anchor,220)))
    texts=sorted({safe(x,350) for x in p.text if KEY.search(x)})
    return label,ts,original,len(data),hashlib.sha256(data).hexdigest(),texts,sorted(links)


def main():
    print("StoneAge Hananet exact menu-page probe — R1")
    print("SCOPE|transient-html|hash-sparse-text-links-only|no-client-binary-download")
    results=[]; errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futs={ex.submit(analyze,p):p for p in PAGES}
        for fut,p in futs.items():
            try: results.append(fut.result())
            except Exception as exc: errors.append((*p,type(exc).__name__,str(exc)))
    print(f"COUNT|pages|{len(PAGES)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|fetched|{len(results)}")
    for label,ts,original,kind,msg in sorted(errors):
        print(f"ERROR|page={label}|timestamp={ts}|kind={kind}|url={safe(original)}|message={safe(msg)}")
    for label,ts,original,size,sha,texts,links in sorted(results):
        print(f"PAGE|page={label}|timestamp={ts}|bytes={size}|sha256={sha}|url={safe(original)}")
        for v in texts: print(f"TEXT|page={label}|value={v}")
        for tag,attr,target,anchor in links:
            print(f"LINK|page={label}|tag={tag}|attr={attr}|target={target}|anchor={anchor}")


if __name__=="__main__":
    main()
