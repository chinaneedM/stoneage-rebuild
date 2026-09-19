#!/usr/bin/env python3
"""Recover StoneAge record identity from the archived Hananet PDS catalog/search surface."""

from __future__ import annotations

import hashlib
import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
API="https://archive.org/wayback/available"
BASE="http://pds.hananet.net:80/"
ROOT_TS="20001018214759"
STONE_RE=re.compile(r"(?i)(stone\s*age|stoneage|스톤\s*에이지)")
VIEW_RE=re.compile(r"(?i)sub_view\.asp\?[^\s\"'<>]+")
FILE_RE=re.compile(r"(?i)\b[a-z0-9][a-z0-9._-]{1,160}\.(?:exe|zip|rar|cab|lzh|lha|msi)\b")


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors=[]
        self.forms=[]
        self.text=[]
        self._href=None
        self._anchor=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower(); a=dict(attrs)
        if tag=="a" and a.get("href"):
            self._href=a["href"]; self._anchor=[]
        if tag=="form":
            self.forms.append((a.get("action",""),a.get("method","GET")))
    def handle_data(self,data):
        if data.strip(): self.text.append(data)
        if self._href is not None:self._anchor.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.anchors.append((self._href," ".join(self._anchor).strip()))
            self._href=None; self._anchor=[]


def request(url,timeout=15):
    last=None
    for attempt in range(3):
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()
        except urllib.error.HTTPError as exc:
            last=exc
            if exc.code!=429 or attempt==2: raise
            time.sleep(3*(attempt+1))
        except (urllib.error.URLError,TimeoutError,ConnectionError) as exc:
            last=exc
            if attempt==2: raise
            time.sleep(2*(attempt+1))
    raise RuntimeError(last)


def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def safe(v,limit=700):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def closest(url,date="20001018"):
    q=urllib.parse.urlencode({"url":url,"timestamp":date})
    payload=json.loads(request(API+"?"+q,timeout=8).decode("utf-8","replace"))
    c=payload.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):return None
    return str(c.get("timestamp","")),str(c.get("status",""))


def fetch_candidate(label,url,preferred_ts=ROOT_TS):
    direct_error=""
    try:
        data=request(replay(preferred_ts,url))
        return label,url,preferred_ts,"direct",direct_error,data
    except Exception as exc:
        direct_error=f"{type(exc).__name__}:{exc}"
    hit=closest(url)
    if not hit:raise RuntimeError(f"direct={direct_error}; availability=no-snapshot")
    ts,status=hit
    data=request(replay(ts,url))
    return label,url,ts,f"availability:{status}",direct_error,data


def query_urls():
    korean="스톤에이지".encode("euc-kr")
    encoded=urllib.parse.quote_from_bytes(korean)
    return [
        ("content",BASE+"content.html"),
        ("search-stoneage",BASE+"sub_list.asp?page=1&keyword=stoneage"),
        ("search-StoneAge",BASE+"sub_list.asp?page=1&keyword=StoneAge"),
        ("search-korean-euckr",BASE+f"sub_list.asp?page=1&keyword={encoded}"),
    ]


def main():
    print("StoneAge Hananet PDS catalog/search probe — R1")
    print("SCOPE|catalog-metadata-short-labels-links-only|transient-html|no-client-binary-download")
    print(f"KOREAN_QUERY_EUCKR|{urllib.parse.quote_from_bytes('스톤에이지'.encode('euc-kr'))}")

    for label,url in query_urls():
        try:
            label,url,ts,retrieval,direct_error,data=fetch_candidate(label,url)
        except Exception as exc:
            print(f"ERROR|query={label}|url={safe(url)}|kind={type(exc).__name__}|message={safe(exc)}")
            continue
        p=Parser(); p.feed(decode(data))
        print(f"PAGE|query={label}|timestamp={ts}|retrieval={retrieval}|bytes={len(data)}|sha256={hashlib.sha256(data).hexdigest()}|url={safe(url)}")
        if direct_error:print(f"FALLBACK|query={label}|direct_error={safe(direct_error)}|timestamp={ts}")
        for action,method in p.forms:
            print(f"FORM|query={label}|method={safe(method.upper())}|action={safe(urllib.parse.urljoin(url,action))}")

        candidates=[]
        for href,anchor in p.anchors:
            absolute=urllib.parse.urljoin(url,href)
            if "sub_view.asp" in absolute.lower():
                candidates.append((absolute,safe(anchor,260)))
        print(f"COUNT|query={label}|detail_links|{len(candidates)}")
        for absolute,anchor in sorted(set(candidates)):
            flag="stoneage" if STONE_RE.search(anchor+" "+absolute) else "other"
            print(f"DETAIL|query={label}|match={flag}|url={safe(absolute)}|anchor={anchor}")

        text="\n".join(p.text)
        for m in STONE_RE.finditer(text):
            start=max(0,m.start()-100); end=min(len(text),m.end()+180)
            print(f"TEXT|query={label}|value={safe(text[start:end],320)}")
        for tok in sorted(set(FILE_RE.findall(text))):
            print(f"FILE|query={label}|value={safe(tok)}")


if __name__=="__main__":main()
