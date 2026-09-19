#!/usr/bin/env python3
"""Extract table-row metadata for Hananet StoneAge STAD records 8119/8120."""

from __future__ import annotations

import html.parser
import hashlib
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010814230641"
URL="http://www.hananet.net/cgi-bin/pkboard.cgi?k1=GAM2:STAD"
TARGETS=("8119","8120")


class RowParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows=[]
        self._depth=0
        self._text=[]
        self._links=[]
        self._href=None
        self._anchor=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower(); a=dict(attrs)
        if tag=="tr":
            if self._depth==0:
                self._text=[];self._links=[]
            self._depth+=1
        if self._depth and tag=="a" and a.get("href"):
            self._href=a["href"];self._anchor=[]
        elif self._depth and a.get("href"):
            self._links.append((tag,"href",a["href"],a.get("alt") or a.get("title") or ""))
        if self._depth:
            for attr in ("src","action"):
                if a.get(attr):self._links.append((tag,attr,a[attr],a.get("alt") or a.get("title") or ""))
    def handle_data(self,data):
        if self._depth and data.strip():self._text.append(data)
        if self._href is not None:self._anchor.append(data)
    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag=="a" and self._href is not None:
            self._links.append(("a","href",self._href," ".join(self._anchor).strip()))
            self._href=None;self._anchor=[]
        if tag=="tr" and self._depth:
            self._depth-=1
            if self._depth==0:self.rows.append((list(self._text),list(self._links)))


def request(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read(),str(getattr(r,"url",url))


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"


def safe(v,limit=1000):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def normalize(target):
    return urllib.parse.urljoin(URL,target.strip())


def select_rows(rows):
    out=[]
    for texts,links in rows:
        combined=" ".join(texts)+" "+" ".join(x[2]+" "+x[3] for x in links)
        if any(t in combined for t in TARGETS) or "온라인게임 스톤에이지 정식 버전" in combined or "온라인게임 스톤에이지 체험 버전" in combined:
            out.append((texts,links))
    return out


def main():
    print("StoneAge Hananet STAD record-row probe — R1")
    print("SCOPE|transient-html|target-table-rows-only|no-client-binary-download")
    data,resolved=request(replay(TS,URL))
    p=RowParser();p.feed(decode(data))
    rows=select_rows(p.rows)
    print(f"PAGE|timestamp={TS}|bytes={len(data)}|sha256={hashlib.sha256(data).hexdigest()}|resolved={safe(resolved)}")
    print(f"COUNT|target_rows|{len(rows)}")
    for i,(texts,links) in enumerate(rows,1):
        print(f"ROW|n={i}|text={safe(' || '.join(texts),1400)}")
        for tag,attr,target,anchor in links:
            print(f"LINK|n={i}|tag={tag}|attr={attr}|target={safe(normalize(target))}|anchor={safe(anchor,300)}")


if __name__=="__main__":main()
