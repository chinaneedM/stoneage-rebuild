#!/usr/bin/env python3
"""Probe exact mirror targets recovered from Inium's official StoneAge down.htm.

High-value targets:
- Hananet PDS record app_id=20001031524596220&type=C03 (linked by Inium from Nov 2000)
- Hananet direct full-version path http://stoneage.hananet.net/down/sa.exe (Inium Aug 2001)
- Gagamel mirror http://www.gagamel.com/web_data/download/stoneagebeta.zip
- GameTime dynamic download entry GW_IDX=9

Binary targets are never fully downloaded: only Wayback availability metadata and,
if archived, at most 64 response bytes are read for magic/header identification.
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

HTML_TARGETS=[
    ("hananet-pds","http://pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"),
    ("hananet-pds-www","http://www.pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"),
    ("hananet-flashlink","http://www.hananet.net/cgi-bin/flashlinks.cgi?lval=http://pds.hananet.net/view.asp?app_id=20001031524596220&type=C03"),
    ("gametime","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online"),
]
BINARY_TARGETS=[
    ("hananet-sa-exe","http://stoneage.hananet.net/down/sa.exe"),
    ("gagamel-zip","http://www.gagamel.com/web_data/download/stoneagebeta.zip"),
]
DATES=("20001109","20001208","20010210","20010413","20010609","20010801")

KEY=re.compile(
    r"(?i)(stone\s*age|stoneage|스톤\s*에이지|download|다운로드|정식|체험|"
    r"파일|용량|setup|install|client|version|버전|\.exe\b|\.zip\b|"
    r"240\s*m|257\s*mb|260\s*m|20001031524596220|8119|8120)"
)
FILE_RE=re.compile(r"(?i)[a-z0-9][a-z0-9._~:/?&=%+-]{1,400}\.(?:exe|zip|rar|cab|lzh|lha|arj|msi)(?:[?&#][^\s\"'<>]*)?")
SIZE_RE=re.compile(r"(?i)\b\d{1,9}(?:[.,]\d{1,3})?\s*(?:bytes?|kb|mb|gb|m)\b")
WAYBACK_PREFIX=re.compile(r"^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/",re.I)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs=[];self.text=[];self._href=None;self._anchor=[]
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


def request(url,timeout=10,headers=None,read_limit=None):
    merged={"User-Agent":UA}
    if headers:merged.update(headers)
    last=None
    for attempt in range(2):
        req=urllib.request.Request(url,headers=merged)
        try:
            with urllib.request.urlopen(req,timeout=timeout) as r:
                body=r.read() if read_limit is None else r.read(read_limit)
                return r,body,str(getattr(r,"url",url))
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
    _,raw,_=request(AVAILABLE+"?"+q,timeout=8)
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


def safe(v,limit=1200):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f")[:limit]


def normalize(base,target):
    target=target.strip()
    if not target:return ""
    if target.lower().startswith(("javascript:","mailto:","#")):return target
    return WAYBACK_PREFIX.sub("",urllib.parse.urljoin(base,target))


def analyze_html(label,original,date):
    hit=closest(original,date)
    if not hit:return ("miss",label,original,date)
    ts,status,archived=hit
    _,data,resolved=request(replay(ts,original),timeout=12)
    text=decode(data);p=Parser();p.feed(text)
    files=sorted(set(FILE_RE.findall(text)))
    sizes=sorted(set(SIZE_RE.findall("\n".join(p.text))))
    snippets=sorted({safe(x,800) for x in p.text if KEY.search(x) or FILE_RE.search(x) or SIZE_RE.search(x)})
    links=set()
    for tag,name,value in p.attrs:
        if name=="anchor":
            href,_,anchor=value.partition(" || ");n=normalize(original,href)
            if n:links.add((tag,"href",safe(n),safe(anchor,300)))
        elif name in ("href","src","action","value"):
            n=normalize(original,value)
            if n and (KEY.search(value) or FILE_RE.search(value) or "download" in n.lower()):
                links.add((tag,name,safe(n),safe("",1)))
    return ("html",{
        "label":label,"original":original,"requested":date,"timestamp":ts,"status":status,
        "archived":archived,"resolved":resolved,"bytes":len(data),
        "sha256":hashlib.sha256(data).hexdigest(),"files":files,"sizes":sizes,
        "snippets":snippets,"links":sorted(links)
    })


def analyze_binary(label,original,date):
    hit=closest(original,date)
    if not hit:return ("miss",label,original,date)
    ts,status,archived=hit
    try:
        r,body,resolved=request(
            replay(ts,original),timeout=15,
            headers={"Range":"bytes=0-63","Accept-Encoding":"identity"},read_limit=64
        )
        meta={
            "prefix_ok":True,"http_status":str(getattr(r,"status","")),
            "content_type":str(r.headers.get("Content-Type","")),
            "content_length":str(r.headers.get("Content-Length","")),
            "content_range":str(r.headers.get("Content-Range","")),
            "prefix_len":len(body),"magic_hex":body[:16].hex(),
            "prefix_sha256":hashlib.sha256(body).hexdigest(),"resolved":resolved,
        }
    except Exception as exc:
        meta={"prefix_ok":False,"error_kind":type(exc).__name__,"error":str(exc)}
    return ("binary",{
        "label":label,"original":original,"requested":date,"timestamp":ts,
        "status":status,"archived":archived,"meta":meta
    })


def main():
    print("StoneAge Inium-linked mirror target probe — R1")
    print("SCOPE|archive-metadata+sparse-html+64-byte-binary-prefix-only|no-complete-binary-download")
    jobs=[]
    for label,url in HTML_TARGETS:
        for date in DATES:jobs.append(("html",label,url,date))
    for label,url in BINARY_TARGETS:
        for date in DATES:jobs.append(("binary",label,url,date))

    def run(job):
        kind,label,url,date=job
        try:
            return analyze_html(label,url,date) if kind=="html" else analyze_binary(label,url,date)
        except Exception as exc:
            return ("error",kind,label,url,date,type(exc).__name__,str(exc))

    results=[];errors=[];misses=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        for res in ex.map(run,jobs):
            if res[0]=="error":errors.append(res[1:])
            elif res[0]=="miss":misses.append(res[1:])
            else:results.append(res)

    html_unique={};binary_unique={}
    for kind,row in results:
        if kind=="html":html_unique[(row["label"],row["timestamp"])]=row
        else:binary_unique[(row["label"],row["timestamp"])]=row

    print(f"COUNT|queries|{len(jobs)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|misses|{len(misses)}")
    print(f"COUNT|html_snapshots|{len(html_unique)}")
    print(f"COUNT|binary_snapshots|{len(binary_unique)}")

    for kind,label,url,date,ek,msg in sorted(errors):
        print(f"ERROR|kind={kind}|target={label}|requested={date}|error={ek}|url={safe(url)}|message={safe(msg)}")

    for (_,ts),row in sorted(html_unique.items(),key=lambda x:(x[0][0],x[0][1])):
        print(
            f"HTML|target={row['label']}|timestamp={ts}|status={row['status']}|bytes={row['bytes']}|"
            f"sha256={row['sha256']}|url={safe(row['original'])}|resolved={safe(row['resolved'])}"
        )
        for f in row["files"]:print(f"FILE|target={row['label']}|value={safe(f)}")
        for s in row["sizes"]:print(f"SIZE|target={row['label']}|value={safe(s)}")
        for tag,attr,target,anchor in row["links"]:
            print(f"LINK|target={row['label']}|tag={tag}|attr={attr}|url={target}|anchor={anchor}")
        for v in row["snippets"]:print(f"TEXT|target={row['label']}|value={v}")

    for (_,ts),row in sorted(binary_unique.items(),key=lambda x:(x[0][0],x[0][1])):
        m=row["meta"]
        if m.get("prefix_ok"):
            print(
                f"BINARY|target={row['label']}|timestamp={ts}|archive_status={row['status']}|"
                f"url={safe(row['original'])}|http_status={safe(m['http_status'])}|"
                f"content_type={safe(m['content_type'])}|content_length={safe(m['content_length'])}|"
                f"content_range={safe(m['content_range'])}|prefix_len={m['prefix_len']}|"
                f"magic_hex={m['magic_hex']}|prefix_sha256={m['prefix_sha256']}|resolved={safe(m['resolved'])}"
            )
        else:
            print(
                f"BINARY|target={row['label']}|timestamp={ts}|archive_status={row['status']}|"
                f"url={safe(row['original'])}|prefix_error={safe(m.get('error_kind'))}:{safe(m.get('error'))}"
            )


if __name__=="__main__":main()
