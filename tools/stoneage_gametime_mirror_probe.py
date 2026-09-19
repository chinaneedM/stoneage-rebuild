#!/usr/bin/env python3
"""Probe exact GameTime StoneAge mirror/content endpoints linked by Inium."""

from __future__ import annotations

import hashlib
import html.parser
import re
import urllib.error
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"

TARGETS=(
    ("download","20010413160323","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("download","20010609062605","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("download","20010801142046","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
    ("article","20001109162800","http://www.gametime.co.kr/webzine/online/news/content.asp?name=New&IDX=11&Cpage=1&page="),
    ("article","20001208050200","http://www.gametime.co.kr/webzine/online/news/content.asp?name=New&IDX=11&Cpage=1&page="),
    ("article","20010413160323","http://www.gametime.co.kr/webzine/online/news/content.asp?name=New&IDX=11&Cpage=1&page="),
)

KEY=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|정식|체험|"
    r"파일|용량|setup|install|client|version|버전|\.exe\b|\.zip\b|"
    r"240\s*m|257\s*mb|260\s*m|GW_IDX|IDX=11)"
)
FILE_RE=re.compile(r"(?i)[a-z0-9][a-z0-9._~:/?&=%+-]{1,400}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)(?:[?&#][^\s\"'<>]*)?")
SIZE_RE=re.compile(r"(?i)\b\d{1,9}(?:[.,]\d{1,3})?\s*(?:bytes?|kb|mb|gb|m)\b")


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=[];self.attrs=[];self._href=None;self._anchor=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower();a=dict(attrs)
        for name,value in attrs:
            if value is not None:self.attrs.append((tag,name.lower(),value))
        if tag=="a" and a.get("href"):
            self._href=a["href"];self._anchor=[]
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.attrs.append(("a","anchor",self._href+" || "+" ".join(self._anchor).strip()))
            self._href=None;self._anchor=[]
    def handle_data(self,data):
        if data.strip():self.text.append(data)
        if self._href is not None:self._anchor.append(data)


def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"


def fetch(url,limit=262144):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept-Encoding":"identity"})
    try:
        with urllib.request.urlopen(req,timeout=15) as r:
            body=r.read(limit)
            return {
                "ok":True,"status":str(getattr(r,"status","")),"resolved":str(getattr(r,"url",url)),
                "content_type":str(r.headers.get("Content-Type","")),
                "content_length":str(r.headers.get("Content-Length","")),
                "body":body,
            }
    except urllib.error.HTTPError as exc:
        return {"ok":False,"status":str(exc.code),"error":str(exc)}
    except Exception as exc:
        return {"ok":False,"status":"","error":f"{type(exc).__name__}: {exc}"}


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def safe(v,limit=1200):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def main():
    print("StoneAge GameTime mirror/content direct-replay probe — R1")
    print("SCOPE|known-timestamp-direct-replay|max-256KiB-response-read|no-complete-binary-download")
    success=0
    for label,ts,original in TARGETS:
        result=fetch(replay(ts,original))
        body=result.get("body",b"")
        print(
            f"REPLAY|kind={label}|timestamp={ts}|ok={1 if result['ok'] else 0}|"
            f"status={safe(result.get('status'))}|url={safe(original)}|resolved={safe(result.get('resolved',''))}|"
            f"content_type={safe(result.get('content_type',''))}|content_length={safe(result.get('content_length',''))}|"
            f"read_bytes={len(body)}|magic_hex={body[:16].hex()}|"
            f"read_sha256={hashlib.sha256(body).hexdigest() if body else ''}|error={safe(result.get('error',''))}"
        )
        if not result["ok"]:continue
        success+=1
        ctype=result.get("content_type","").lower()
        if not any(x in ctype for x in ("html","text","xml")):
            continue
        text=decode(body);p=Parser();p.feed(text)
        for token in sorted(set(FILE_RE.findall(text))):
            print(f"FILE|kind={label}|timestamp={ts}|value={safe(token)}")
        for token in sorted(set(SIZE_RE.findall("\n".join(p.text)))):
            print(f"SIZE|kind={label}|timestamp={ts}|value={safe(token)}")
        for value in sorted({safe(x,800) for x in p.text if KEY.search(x) or FILE_RE.search(x) or SIZE_RE.search(x)}):
            print(f"TEXT|kind={label}|timestamp={ts}|value={value}")
        for tag,name,value in p.attrs:
            if KEY.search(value) or FILE_RE.search(value):
                print(f"ATTR|kind={label}|timestamp={ts}|tag={tag}|name={name}|value={safe(value)}")
    print(f"COUNT|success|{success}")


if __name__=="__main__":main()
