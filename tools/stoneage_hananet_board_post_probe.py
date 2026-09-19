#!/usr/bin/env python3
"""Probe exact Hananet StoneAge board records for full/trial download metadata."""

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

POSTS=[
    (
        "stad-full",
        "20010814230641",
        "http://www.hananet.net/cgi-bin/pkboard.cgi?"
        "k1=GAM2:STAD:4:2000000000:0:12:1:2:1&k2=8119:1:0:0&k3=0::",
    ),
    (
        "stad-trial",
        "20010814230641",
        "http://www.hananet.net/cgi-bin/pkboard.cgi?"
        "k1=GAM2:STAD:4:2000000000:0:12:1:2:1&k2=8120:2:0:0&k3=0::",
    ),
    (
        "staf-full-question",
        "20010126065300",
        "http://www.hananet.net/cgi-bin/pkboard.cgi?"
        "k1=GAM2:STAF:4:2000000000:0:12:1:327:1&k2=7750:246:0:0&k3=0::",
    ),
]

KEY=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|정식|체험|풀버전|full|trial|"
    r"다운로드|download|자료|파일|설치|setup|install|client|클라이언트|"
    r"patch|패치|update|업데이트|버전|version|용량|"
    r"\.exe\b|\.zip\b|\.rar\b|\.cab\b|\.lzh\b|"
    r"\b\d+(?:\.\d+){1,3}\b|\b\d+(?:\.\d+)?\s*(?:kb|mb|gb)\b)"
)
FILE_RE=re.compile(r"(?i)\b[a-z0-9][a-z0-9._-]{1,180}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)\b")
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.text=[]; self.inputs=[]
        self._href=None; self._anchor=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower(); a=dict(attrs)
        if tag=="a" and a.get("href"):
            self._href=a["href"]; self._anchor=[]
        elif a.get("href"):
            self.links.append((tag,"href",a["href"],a.get("alt") or a.get("title") or ""))
        for attr in ("src","action"):
            if a.get(attr):
                self.links.append((tag,attr,a[attr],a.get("alt") or a.get("title") or ""))
        if tag=="input":
            self.inputs.append((a.get("type",""),a.get("name",""),a.get("value","")))
    def handle_data(self,data):
        if data.strip():self.text.append(data)
        if self._href is not None:self._anchor.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.links.append(("a","href",self._href," ".join(self._anchor).strip()))
            self._href=None; self._anchor=[]


def request(url,timeout=15):
    last=None
    for attempt in range(3):
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read(),str(getattr(r,"url",url))
        except urllib.error.HTTPError as exc:
            last=exc
            if exc.code!=429 or attempt==2:raise
            time.sleep(2*(attempt+1))
        except (urllib.error.URLError,TimeoutError,ConnectionError) as exc:
            last=exc
            if attempt==2:raise
            time.sleep(1+attempt)
    raise RuntimeError(last)


def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def safe(v,limit=900):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def normalize(base,target):
    target=target.strip()
    if not target or target.startswith(("javascript:","#","mailto:")):return ""
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def analyze(item):
    label,ts,url=item
    data,resolved=request(replay(ts,url))
    text=decode(data)
    p=Parser(); p.feed(text)
    alltext="\n".join(p.text)
    snippets=sorted({safe(x,520) for x in p.text if KEY.search(x) or FILE_RE.search(x)})
    files=sorted(set(FILE_RE.findall(text)))
    links=set()
    for tag,attr,target,anchor in p.links:
        n=normalize(url,target)
        if not n:continue
        combined=n+" "+anchor
        if KEY.search(combined) or FILE_RE.search(combined) or "pkboard.cgi" in n.lower():
            links.add((tag,attr,safe(n),safe(anchor,280)))
    inputs=sorted({tuple(safe(x,300) for x in row) for row in p.inputs if KEY.search(" ".join(row))})
    return {
        "label":label,"requested":ts,"url":url,"resolved":resolved,
        "bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
        "snippets":snippets,"files":files,"links":sorted(links),"inputs":inputs,
        "stoneage":bool(re.search(r"(?i)(stone\s*age|stoneage|스톤\s*에이지)",alltext)),
    }


def main():
    print("StoneAge Hananet board-record probe — R1")
    print("SCOPE|transient-html|hash-sparse-text-links-only|no-client-binary-download")
    results=[];errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs={ex.submit(analyze,p):p for p in POSTS}
        for fut,p in futs.items():
            try:results.append(fut.result())
            except Exception as exc:errors.append((p[0],p[1],p[2],type(exc).__name__,str(exc)))
    print(f"COUNT|posts|{len(POSTS)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|fetched|{len(results)}")
    for label,ts,url,kind,msg in sorted(errors):
        print(f"ERROR|post={label}|timestamp={ts}|kind={kind}|url={safe(url)}|message={safe(msg)}")
    for row in sorted(results,key=lambda x:x["label"]):
        print(
            f"PAGE|post={row['label']}|requested={row['requested']}|stoneage={1 if row['stoneage'] else 0}|"
            f"bytes={row['bytes']}|sha256={row['sha256']}|resolved={safe(row['resolved'])}"
        )
        for f in row["files"]:print(f"FILE|post={row['label']}|value={safe(f)}")
        for v in row["snippets"]:print(f"TEXT|post={row['label']}|value={v}")
        for typ,name,value in row["inputs"]:
            print(f"INPUT|post={row['label']}|type={typ}|name={name}|value={value}")
        for tag,attr,target,anchor in row["links"]:
            print(f"LINK|post={row['label']}|tag={tag}|attr={attr}|target={target}|anchor={anchor}")


if __name__=="__main__":main()
