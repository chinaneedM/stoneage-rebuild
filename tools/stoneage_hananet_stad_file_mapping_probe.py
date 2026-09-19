#!/usr/bin/env python3
"""Map Hananet STAD StoneAge titles/sizes to direct file URLs by table structure."""

from __future__ import annotations

import html.parser
import hashlib
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010814230641"
URL="http://www.hananet.net/cgi-bin/pkboard.cgi?k1=GAM2:STAD"
TOKENS=("스톤에이지","sa.exe","sa_demo.exe","260 M","240 M","8119","8120")


class TableParser(html.parser.HTMLParser):
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
                self._text=[]; self._links=[]
            self._depth+=1
        if self._depth and tag=="a" and a.get("href"):
            self._href=a["href"]; self._anchor=[]
        elif self._depth:
            for attr in ("src","action"):
                if a.get(attr):
                    self._links.append((tag,attr,a[attr],""))
    def handle_data(self,data):
        if self._depth and data.strip():
            self._text.append(data)
        if self._href is not None:
            self._anchor.append(data)
    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag=="a" and self._href is not None:
            self._links.append(("a","href",self._href," ".join(self._anchor).strip()))
            self._href=None; self._anchor=[]
        if tag=="tr" and self._depth:
            self._depth-=1
            if self._depth==0:
                self.rows.append((list(self._text),list(self._links)))


def request(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.read(),str(getattr(r,"url",url))


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def replay(ts,url): return f"https://web.archive.org/web/{ts}id_/{url}"


def safe(v,limit=1400):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def normalize(target):
    return urllib.parse.urljoin(URL,target.strip())


def relevant_rows(rows):
    out=[]
    for idx,(texts,links) in enumerate(rows,1):
        blob=" ".join(texts)+" "+" ".join(t+" "+a for _,_,t,a in links)
        if any(token in blob for token in TOKENS):
            out.append((idx,texts,links))
    return out


def main():
    print("StoneAge Hananet STAD file/title mapping probe — R1")
    print("SCOPE|transient-html|relevant-table-rows-only|no-client-binary-download")
    data,resolved=request(replay(TS,URL))
    p=TableParser(); p.feed(decode(data))
    rows=relevant_rows(p.rows)
    print(f"PAGE|timestamp={TS}|bytes={len(data)}|sha256={hashlib.sha256(data).hexdigest()}|resolved={safe(resolved)}")
    print(f"COUNT|relevant_rows|{len(rows)}")
    for idx,texts,links in rows:
        print(f"ROW|index={idx}|text={safe(' || '.join(texts))}")
        for tag,attr,target,anchor in links:
            norm=normalize(target)
            if any(token in (norm+" "+anchor) for token in TOKENS):
                print(f"LINK|row={idx}|tag={tag}|attr={attr}|target={safe(norm)}|anchor={safe(anchor,300)}")


if __name__=="__main__": main()
