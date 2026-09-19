#!/usr/bin/env python3
"""Emit bounded source-order context for STAD title/size/file tokens."""

from __future__ import annotations
import hashlib
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TS="20010814230641"
URL="http://www.hananet.net/cgi-bin/pkboard.cgi?k1=GAM2:STAD"
TOKENS=[
    "온라인게임 스톤에이지 체험 버전",
    "240 M",
    "온라인게임 스톤에이지 정식 버전",
    "260 M",
    "http://stoneage.hananet.net/down/sa.exe",
    "http://stoneage.hananet.net/down/sa_demo.exe",
]

def request(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()

def replay(ts,url): return f"https://web.archive.org/web/{ts}id_/{url}"

def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError: pass
    return data.decode("latin-1","replace")

def safe(v,limit=700):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def contexts(text,token,radius=220):
    out=[]
    start=0
    while True:
        pos=text.find(token,start)
        if pos<0:break
        lo=max(0,pos-radius); hi=min(len(text),pos+len(token)+radius)
        out.append((pos,text[lo:hi]))
        start=pos+len(token)
    return out

def main():
    print("StoneAge Hananet STAD source-order context — R1")
    print("SCOPE|bounded-token-context-only|no-client-binary-download")
    data=request(replay(TS,URL)); text=decode(data)
    print(f"PAGE|timestamp={TS}|bytes={len(data)}|sha256={hashlib.sha256(data).hexdigest()}")
    rows=[]
    for token in TOKENS:
        for pos,ctx in contexts(text,token):
            rows.append((pos,token,ctx))
    print(f"COUNT|occurrences|{len(rows)}")
    for pos,token,ctx in sorted(rows):
        print(f"OCCURRENCE|pos={pos}|token={safe(token)}|context={safe(ctx)}")

if __name__=="__main__":main()
