#!/usr/bin/env python3
"""Enumerate archived Hananet PDS H01 detail records and identify StoneAge.

The seed list is recovered from archived content.html. Each H01 detail page is
fetched transiently. The report stores only record identity, hashes/titles and
sparse StoneAge/file/size metadata; no client bytes are downloaded.
"""

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
TS="20001018214759"
BASE="http://pds.hananet.net:80/"
SEED=BASE+"content.html"

VIEW_RE=re.compile(r"(?i)sub_view\.asp\?app_id=([^&\s\"'<>]+)&type=(H01)\b")
STONE_RE=re.compile(r"(?i)(stone\s*age|stoneage|스톤\s*에이지)")
FILE_RE=re.compile(r"(?i)\b[a-z0-9][a-z0-9._-]{1,180}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)\b")
SIZE_RE=re.compile(r"(?i)\b\d{1,7}(?:[.,]\d{1,3})?\s*(?:bytes?|kb|mb|gb)\b")
INTEREST_RE=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|다운로드|download|설치|setup|"
    r"install|patch|패치|update|업데이트|client|클라이언트|파일|용량|버전|version)"
)
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=[]
        self.links=[]
        self.title=[]
        self._in_title=False
        self._href=None
        self._anchor=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower(); a=dict(attrs)
        if tag=="title": self._in_title=True
        if tag=="a" and a.get("href"):
            self._href=a["href"]; self._anchor=[]
        elif a.get("href"):
            self.links.append((tag,"href",a["href"],a.get("alt") or a.get("title") or ""))
        for attr in ("src","action"):
            if a.get(attr):
                self.links.append((tag,attr,a[attr],a.get("alt") or a.get("title") or ""))
    def handle_data(self,data):
        if data.strip(): self.text.append(data)
        if self._in_title and data.strip(): self.title.append(data)
        if self._href is not None:self._anchor.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="title": self._in_title=False
        if tag.lower()=="a" and self._href is not None:
            self.links.append(("a","href",self._href," ".join(self._anchor).strip()))
            self._href=None; self._anchor=[]


def request(url,timeout=10):
    last=None
    for attempt in range(2):
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.read(),str(getattr(r,"url",url))
        except urllib.error.HTTPError as exc:
            last=exc
            if exc.code!=429 or attempt==1: raise
            time.sleep(2)
        except (urllib.error.URLError,TimeoutError,ConnectionError) as exc:
            last=exc
            if attempt==1: raise
            time.sleep(1)
    raise RuntimeError(last)


def replay(ts,url): return f"https://web.archive.org/web/{ts}id_/{url}"


def decode(data):
    for enc in ("utf-8","cp949","euc-kr"):
        try:return data.decode(enc)
        except UnicodeDecodeError:pass
    return data.decode("latin-1","replace")


def safe(v,limit=600):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def normalize(base,target):
    target=target.strip()
    if not target or target.startswith(("javascript:","mailto:","#")):return ""
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def extract_candidates(seed_html):
    found={}
    for m in VIEW_RE.finditer(seed_html):
        app_id=m.group(1)
        url=BASE+f"sub_view.asp?app_id={app_id}&type=H01"
        found[app_id]=url
    return sorted(found.items())


def analyze(item):
    app_id,url=item
    data,resolved=request(replay(TS,url))
    text=decode(data)
    p=Parser(); p.feed(text)
    visible="\n".join(p.text)
    title=safe(" ".join(p.title),260)
    stone=bool(STONE_RE.search(text))
    files=sorted(set(FILE_RE.findall(text)))
    sizes=sorted(set(SIZE_RE.findall(visible)))
    snippets=sorted({safe(x,420) for x in p.text if stone and INTEREST_RE.search(x)})
    links=set()
    for tag,attr,target,anchor in p.links:
        n=normalize(url,target)
        if not n:continue
        combined=n+" "+anchor
        if FILE_RE.search(combined) or (stone and INTEREST_RE.search(combined)):
            links.add((tag,attr,safe(n),safe(anchor,220)))
    return {
        "app_id":app_id,"url":url,"resolved":resolved,"bytes":len(data),
        "sha256":hashlib.sha256(data).hexdigest(),"title":title,"stone":stone,
        "files":files,"sizes":sizes,"snippets":snippets,"links":sorted(links)
    }


def main():
    print("StoneAge Hananet PDS H01 detail enumeration — R1")
    print("SCOPE|transient-html|record-hash-title-sparse-metadata-only|no-client-binary-download")
    seed_data,_=request(replay(TS,SEED),timeout=12)
    candidates=extract_candidates(decode(seed_data))
    print(f"COUNT|h01_candidates|{len(candidates)}")

    results=[]; errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs={ex.submit(analyze,item):item for item in candidates}
        for fut,item in futs.items():
            app_id,url=item
            try:results.append(fut.result())
            except Exception as exc:errors.append((app_id,url,type(exc).__name__,str(exc)))

    print(f"COUNT|fetched|{len(results)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|stoneage_matches|{sum(1 for x in results if x['stone'])}")
    print(f"COUNT|file_token_records|{sum(1 for x in results if x['files'])}")

    for app_id,url,kind,msg in sorted(errors):
        print(f"ERROR|app_id={safe(app_id)}|kind={kind}|url={safe(url)}|message={safe(msg)}")

    for row in sorted(results,key=lambda x:x["app_id"]):
        print(
            f"ENTRY|app_id={safe(row['app_id'])}|stoneage={1 if row['stone'] else 0}|"
            f"bytes={row['bytes']}|sha256={row['sha256']}|title={safe(row['title'])}|"
            f"resolved={safe(row['resolved'])}"
        )
        if not (row["stone"] or row["files"]):continue
        for token in row["files"]:print(f"FILE|app_id={safe(row['app_id'])}|value={safe(token)}")
        for token in row["sizes"]:print(f"SIZE|app_id={safe(row['app_id'])}|value={safe(token)}")
        for value in row["snippets"]:print(f"TEXT|app_id={safe(row['app_id'])}|value={value}")
        for tag,attr,target,anchor in row["links"]:
            print(f"LINK|app_id={safe(row['app_id'])}|tag={tag}|attr={attr}|target={target}|anchor={anchor}")


if __name__=="__main__":main()
