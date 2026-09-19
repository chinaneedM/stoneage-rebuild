#!/usr/bin/env python3
"""Probe the exact early GameTime StoneAge download endpoint recovered from article IDX=11."""

from __future__ import annotations

import hashlib
import html.parser
import re
import urllib.parse
import urllib.request
import urllib.error

UA="stoneage-rebuild-archaeology/1.0"
TS="20001208213500"
NAME="스톤에이지"
BASE="http://www.gametime.co.kr/webzine/online/download.asp"

def variants():
    raw=BASE+"?name="+NAME
    utf8=BASE+"?name="+urllib.parse.quote(NAME,encoding="utf-8")
    cp949=BASE+"?name="+urllib.parse.quote_from_bytes(NAME.encode("cp949"))
    euckr=BASE+"?name="+urllib.parse.quote_from_bytes(NAME.encode("euc-kr"))
    alt=BASE.replace("www.","")+"?name="+NAME
    return list(dict.fromkeys([raw,utf8,cp949,euckr,alt]))

KEY=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|정식|체험|"
    r"파일|용량|setup|install|client|version|버전|\.exe\b|\.zip\b|"
    r"240\s*m|257\s*mb|260\s*m)"
)
FILE_RE=re.compile(r"(?i)[a-z0-9][a-z0-9._~:/?&=%+-]{1,400}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)(?:[?&#][^\s\"'<>]*)?")
SIZE_RE=re.compile(r"(?i)\b\d{1,9}(?:[.,]\d{1,3})?\s*(?:bytes?|kb|mb|gb|m)\b")

class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.text=[];self.attrs=[];self._href=None;self._anchor=[]
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

def replay(url):return f"https://web.archive.org/web/{TS}id_/{url}"

def fetch(url,limit=524288):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept-Encoding":"identity"})
    try:
        with urllib.request.urlopen(req,timeout=15) as r:
            body=r.read(limit)
            return True,str(getattr(r,"status","")),str(getattr(r,"url",url)),str(r.headers.get("Content-Type","")),str(r.headers.get("Content-Length","")),body,""
    except urllib.error.HTTPError as exc:
        return False,str(exc.code),"","","",b"",str(exc)
    except Exception as exc:
        return False,"","","","",b"",f"{type(exc).__name__}: {exc}"

def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")

def safe(v,limit=1400):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]

def main():
    print("StoneAge GameTime early download endpoint probe — R1")
    print("SOURCE|article=IDX11|href=../download.asp?name=스톤에이지|snapshot=20001208213500")
    print("SCOPE|direct-replay-encoding-variants|max-512KiB-read|no-complete-client-binary-download")
    success=0
    for original in variants():
        ok,status,resolved,ctype,clen,body,error=fetch(replay(original))
        print(
            f"REPLAY|ok={1 if ok else 0}|status={safe(status)}|url={safe(original)}|"
            f"resolved={safe(resolved)}|content_type={safe(ctype)}|content_length={safe(clen)}|"
            f"read_bytes={len(body)}|magic_hex={body[:16].hex()}|"
            f"read_sha256={hashlib.sha256(body).hexdigest() if body else ''}|error={safe(error)}"
        )
        if not ok:continue
        success+=1
        text=decode(body);p=Parser();p.feed(text)
        for token in sorted(set(FILE_RE.findall(text))):
            print(f"FILE|value={safe(token)}")
        for token in sorted(set(SIZE_RE.findall("\n".join(p.text)))):
            print(f"SIZE|value={safe(token)}")
        for value in sorted({safe(x,900) for x in p.text if KEY.search(x) or FILE_RE.search(x) or SIZE_RE.search(x)}):
            print(f"TEXT|value={value}")
        for tag,name,value in p.attrs:
            if KEY.search(value) or FILE_RE.search(value):
                print(f"ATTR|tag={tag}|name={name}|value={safe(value)}")
    print(f"COUNT|success|{success}")

if __name__=="__main__":main()
