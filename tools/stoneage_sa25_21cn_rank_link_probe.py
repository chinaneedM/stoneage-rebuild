#!/usr/bin/env python3
"""Recover the native 21CN list.php ID behind the sidebar text '石器时代2.5-精…'.

The already recovered 21CN record 22318 page contains a category download ranking
whose #1 entry is visibly '石器时代2.5-精…'. This probe replays selected archived
HTML pages only and extracts anchor text/href pairs. It never follows download links.
"""
from __future__ import annotations

import hashlib
import html
from html.parser import HTMLParser
import re
import time
import urllib.parse
import urllib.request

from tools.stoneage_sa25_host_identity_probe import declared_charset, decode

UA="stoneage-rebuild-archaeology/1.0"
CAPTURES=(
    ("2003-03-13","20030313042912","http://download.21cn.com:80/list.php?id=22318"),
    ("2003-04-22","20030422065326","http://download.21cn.com:80/list.php?id=22318"),
    ("2003-06-27","20030627085748","http://download.21cn.com:80/list.php?id=22318"),
    ("2003-08-14","20030814070703","http://download.21cn.com:80/list.php?id=22318"),
)
TOKENS=("石器时代2.5","石器時代2.5","精灵王","精靈王")

def clean(v,limit=2200):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]

def fetch(url,timeout=30,attempts=4):
    last=None
    for n in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read(1_500_001)
                if len(b)>1_500_000: raise ValueError("page-too-large")
                return int(getattr(r,"status",r.getcode())),r.geturl(),b
        except Exception as e:
            last=e
            if n+1<attempts: time.sleep(1.2*(n+1))
    raise last

def replay(ts,url):
    return f"https://web.archive.org/web/{ts}id_/{url}"

class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.href=None
        self.buf=[]
        self.out=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            self.href=dict(attrs).get("href","")
            self.buf=[]
    def handle_data(self,data):
        if self.href is not None:
            self.buf.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self.href is not None:
            self.out.append((html.unescape(self.href), " ".join("".join(self.buf).split())))
            self.href=None
            self.buf=[]

def anchors(text):
    p=AnchorParser()
    p.feed(text)
    return tuple(p.out)

def relevant_anchor(text,href):
    low=text.lower()
    return (
        any(t.lower() in low for t in TOKENS)
        or ("stoneage" in low and "2.5" in low)
        or ("list.php" in href.lower() and ("石器时代" in text or "石器時代" in text))
    )

def record_id(href):
    try:
        q=urllib.parse.parse_qs(urllib.parse.urlsplit(html.unescape(href)).query)
        v=(q.get("id") or [""])[0]
        return str(v)
    except Exception:
        return ""

def main():
    print("StoneAge 2.5 21CN ranking-link ID recovery — R1")
    print("SCOPE|archived-html-anchor-extraction|no-download-follow|no-game-payload")
    hits=[]; errors=[]
    for label,ts,url in CAPTURES:
        try:
            st,final,b=fetch(replay(ts,url))
            enc,text=decode(b,declared_charset(b))
            aa=anchors(text)
            rel=[(href,txt) for href,txt in aa if relevant_anchor(txt,href)]
            print(
                f"PAGE|label={label}|timestamp={ts}|status={st}|bytes={len(b)}|"
                f"sha256={hashlib.sha256(b).hexdigest()}|encoding={clean(enc)}|anchors={len(aa)}|"
                f"relevant={len(rel)}|final={clean(final)}"
            )
            for n,(href,txt) in enumerate(rel,1):
                rid=record_id(href)
                hits.append((label,ts,rid,href,txt))
                print(
                    f"ANCHOR|label={label}|order={n}|id={clean(rid)}|"
                    f"text={clean(txt,1200)}|href={clean(href,1800)}"
                )
        except Exception as e:
            errors.append((label,type(e).__name__,str(e)))
    ids=sorted({rid for _,_,rid,_,txt in hits if rid and "2.5" in txt})
    print(f"IDS|stoneage25={','.join(ids)}")
    for label,kind,msg in errors:
        print(f"ERROR|label={clean(label)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|captures|{len(CAPTURES)}")
    print(f"COUNT|relevant_anchors|{len(hits)}")
    print(f"COUNT|stoneage25_ids|{len(ids)}")
    print(f"COUNT|errors|{len(errors)}")
    if ids:
        print("RESOLUTION|NATIVE_21CN_STONEAGE25_ID_RECOVERED|trace exact list record and downit/file metadata next")
    elif errors:
        print("RESOLUTION|PARTIAL_RANK_LINK_RECOVERY|retry failed captures")
    else:
        print("RESOLUTION|NO_ID_IN_TESTED_RANKING_HTML|expand to other successful record captures")
    print("EVIDENCE_BOUNDARY|a ranking anchor identifies the native 21CN catalogue record; it does not authenticate linked client bytes.")

if __name__=="__main__":
    main()
