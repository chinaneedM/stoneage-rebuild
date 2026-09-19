#!/usr/bin/env python3
"""Probe dated Hananet GameNet StoneAge surfaces for full/trial download targets.

The STAD catalog pins two records to 2001-02-10 (8119 full 260 M, 8120 trial
240 M) and instructs users to download game data from the corresponding
GameNet game page. This probe resolves archived page snapshots near that date
and the later 2001-08 STAD capture, then emits only sparse download-relevant
attributes/scripts/text.
"""

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

SURFACES=[
    ("game-map","http://game.hananet.net/gamenet/sitemap/map/mapstoneage.html"),
    ("game-frame","http://game.hananet.net/gamenet/newframe/frstoneage.html"),
    ("game-content","http://game.hananet.net/gamenet/newframe/contents/stoneage.html"),
    ("stoneage-main","http://stoneage.hananet.net/main.htm"),
    ("stoneage-2","http://stoneage.hananet.net/2.htm"),
    ("stoneage-2_5","http://stoneage.hananet.net/2_5.htm"),
]
DATES=("20010210","20010814")

KEY=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|정식|체험|full|trial|"
    r"다운로드|download|자료|설치|setup|install|client|클라이언트|"
    r"patch|패치|update|업데이트|240\s*m|260\s*m|257\s*mb|"
    r"8119|8120|\.exe\b|\.zip\b|\.rar\b|\.cab\b|\.lzh\b)"
)
FILE_RE=re.compile(r"(?i)[a-z0-9][a-z0-9._~:/?&=%+-]{1,300}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)(?:[?&#][^\s\"'<>]*)?")
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs=[]
        self.text=[]
        self.scripts=[]
        self._script=False
    def handle_starttag(self,tag,attrs):
        tag=tag.lower()
        for name,value in attrs:
            if value is not None:
                self.attrs.append((tag,name.lower(),value))
        if tag=="script":self._script=True
    def handle_endtag(self,tag):
        if tag.lower()=="script":self._script=False
    def handle_data(self,data):
        if data.strip():self.text.append(data)
        if self._script and data.strip():self.scripts.append(data)


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


def safe(v,limit=1000):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def normalize(base,target):
    target=target.strip()
    if not target:return ""
    if target.lower().startswith(("javascript:","mailto:","#")):return target
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def analyze(job):
    label,original,date=job
    hit=closest(original,date)
    if not hit:
        return {"label":label,"original":original,"date":date,"available":False}
    ts,status,archived=hit
    data,resolved=request(replay(ts,original),timeout=12)
    text=decode(data)
    p=Parser();p.feed(text)

    attrs=set()
    for tag,name,value in p.attrs:
        combined=value
        if KEY.search(combined) or FILE_RE.search(combined) or name.startswith("on"):
            attrs.add((tag,name,safe(normalize(original,value),1200)))

    snippets=sorted({safe(x,700) for x in p.text+p.scripts if KEY.search(x) or FILE_RE.search(x)})
    files=sorted(set(FILE_RE.findall(text)))
    return {
        "label":label,"original":original,"date":date,"available":True,
        "timestamp":ts,"status":status,"archived":archived,"resolved":resolved,
        "bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
        "attrs":sorted(attrs),"snippets":snippets,"files":files,
    }


def main():
    print("StoneAge Hananet dated GameNet download-surface probe — R1")
    print("CONTEXT|STAD full=8119/260M|trial=8120/240M|registered=2001-02-10")
    print("SCOPE|transient-html|sparse-download-attributes-scripts-text-only|no-client-binary-download")
    jobs=[(label,url,date) for label,url in SURFACES for date in DATES]
    results=[];errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(analyze,j):j for j in jobs}
        for fut,j in futs.items():
            try:results.append(fut.result())
            except Exception as exc:errors.append((*j,type(exc).__name__,str(exc)))
    print(f"COUNT|jobs|{len(jobs)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|available|{sum(1 for x in results if x.get('available'))}")
    for label,url,date,kind,msg in sorted(errors):
        print(f"ERROR|surface={label}|date={date}|kind={kind}|url={safe(url)}|message={safe(msg)}")
    for row in sorted(results,key=lambda x:(x["label"],x["date"])):
        if not row.get("available"):
            print(f"MISS|surface={row['label']}|date={row['date']}|url={safe(row['original'])}")
            continue
        print(
            f"PAGE|surface={row['label']}|requested={row['date']}|timestamp={row['timestamp']}|"
            f"status={row['status']}|bytes={row['bytes']}|sha256={row['sha256']}|"
            f"original={safe(row['original'])}|resolved={safe(row['resolved'])}"
        )
        for token in row["files"]:print(f"FILE|surface={row['label']}|value={safe(token)}")
        for tag,name,value in row["attrs"]:
            print(f"ATTR|surface={row['label']}|tag={tag}|name={name}|value={value}")
        for value in row["snippets"]:
            print(f"TEXT|surface={row['label']}|value={value}")


if __name__=="__main__":main()
