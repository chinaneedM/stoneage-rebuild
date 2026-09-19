#!/usr/bin/env python3
"""Direct-replay normalized variants for the exact Hananet StoneAge PDS record."""

from __future__ import annotations

import hashlib
import html.parser
import re
import urllib.error
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
APP="20001031524596220"
TIMESTAMPS=("20001210160500","20010630185101")
URLS=(
    f"http://pds.hananet.net/view.asp?app_id={APP}&type=C03",
    f"http://pds.hananet.net:80/view.asp?app_id={APP}&type=C03",
    f"http://www.pds.hananet.net/view.asp?app_id={APP}&type=C03",
    f"http://pds.hananet.net/view.asp?type=C03&app_id={APP}",
    f"http://pds.hananet.net/view.asp?app_id={APP}",
    f"http://pds.hananet.net/View.asp?app_id={APP}&type=C03",
)
BINARY_ATTEMPTS=(
    ("hananet-sa","20010801142046","http://stoneage.hananet.net/down/sa.exe"),
    ("hananet-sa","20010803115715","http://stoneage.hananet.net/down/sa.exe"),
    ("hananet-sa","20010814135008","http://stoneage.hananet.net/down/sa.exe"),
    ("gagamel","20010609062605","http://www.gagamel.com/web_data/download/stoneagebeta.zip"),
    ("gagamel","20010801142046","http://www.gagamel.com/web_data/download/stoneagebeta.zip"),
)

KEY=re.compile(r"(?i)(stone\s*age|stoneage|스톤\s*에이지|다운로드|download|정식|체험|파일|용량|\.exe\b|\.zip\b|240\s*m|260\s*m)")
FILE_RE=re.compile(r"(?i)[a-z0-9][a-z0-9._~:/?&=%+-]{1,350}\.(?:exe|zip|rar|cab|lzh|lha|msi)(?:[?&#][^\s\"'<>]*)?")


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=[];self.attrs=[]
    def handle_starttag(self,tag,attrs):
        for name,value in attrs:
            if value is not None:self.attrs.append((tag.lower(),name.lower(),value))
    def handle_data(self,data):
        if data.strip():self.text.append(data)


def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"


def safe(v,limit=1000):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def fetch(url,read_limit=None):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Range":"bytes=0-63"} if read_limit else {"User-Agent":UA})
    try:
        with urllib.request.urlopen(req,timeout=12) as r:
            body=r.read() if read_limit is None else r.read(read_limit)
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


def main():
    print("StoneAge Hananet PDS direct-replay variant probe — R1")
    print("SCOPE|direct-replay-normalization+sparse-html+64-byte-prefix-only|no-complete-binary-download")

    success=0
    for ts in TIMESTAMPS:
        for original in URLS:
            result=fetch(replay(ts,original))
            print(f"REPLAY|timestamp={ts}|status={safe(result.get('status'))}|ok={1 if result['ok'] else 0}|url={safe(original)}|resolved={safe(result.get('resolved',''))}|error={safe(result.get('error',''))}")
            if not result["ok"]:continue
            success+=1
            body=result["body"];text=decode(body);p=Parser();p.feed(text)
            print(f"HTML|timestamp={ts}|url={safe(original)}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|content_type={safe(result['content_type'])}")
            for token in sorted(set(FILE_RE.findall(text))):
                print(f"FILE|timestamp={ts}|value={safe(token)}")
            for value in sorted({safe(x,700) for x in p.text if KEY.search(x) or FILE_RE.search(x)}):
                print(f"TEXT|timestamp={ts}|value={value}")
            for tag,name,value in p.attrs:
                if KEY.search(value) or FILE_RE.search(value):
                    print(f"ATTR|timestamp={ts}|tag={tag}|name={name}|value={safe(value)}")

    print(f"COUNT|html_success|{success}")

    prefix_success=0
    for label,ts,original in BINARY_ATTEMPTS:
        result=fetch(replay(ts,original),read_limit=64)
        body=result.get("body",b"")
        print(
            f"PREFIX|target={label}|timestamp={ts}|ok={1 if result['ok'] else 0}|"
            f"status={safe(result.get('status'))}|url={safe(original)}|resolved={safe(result.get('resolved',''))}|"
            f"content_type={safe(result.get('content_type',''))}|content_length={safe(result.get('content_length',''))}|"
            f"prefix_len={len(body)}|magic_hex={body[:16].hex()}|"
            f"prefix_sha256={hashlib.sha256(body).hexdigest() if body else ''}|error={safe(result.get('error',''))}"
        )
        if result["ok"]:prefix_success+=1
    print(f"COUNT|binary_prefix_success|{prefix_success}")


if __name__=="__main__":main()
