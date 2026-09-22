#!/usr/bin/env python3
"""Probe archive indexes for the Korean Netmarble StoneAge 1.74 bridge client.

Only archive metadata and transiently extracted link targets are emitted.
No client binary or archived HTML body is committed.
"""

from __future__ import annotations

import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request


UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
WAYBACK="https://web.archive.org/web/{timestamp}id_/{url}"

DOWNLOAD_EXT=re.compile(
    r"(?i)\.(?:exe|zip|rar|cab|lzh|lha|arj|gz|tgz|bz2|msi)(?:$|[?#])"
)
INTEREST=re.compile(
    r"(?i)(stone\s*age|stoneage|client|download|setup|install|patch|update|"
    r"스톤\s*에이지|스톤에이지|클라이언트|다운로드|설치|패치|업데이트)"
)


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self._href=None
        self._text=[]

    def handle_starttag(self,tag,attrs):
        if tag.lower()!="a":
            return
        attrs=dict(attrs)
        self._href=attrs.get("href")
        self._text=[]

    def handle_data(self,data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.links.append((self._href,"".join(self._text).strip()))
            self._href=None
            self._text=[]


def request(url,*,timeout=30):
    last=None
    for attempt in range(2):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA})
            with urllib.request.urlopen(req,timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError,TimeoutError,ConnectionError) as exc:
            last=exc
            time.sleep(1+attempt)
    raise RuntimeError(f"request failed: {url}: {last}")


def decode_html(data):
    for encoding in ("utf-8","cp949","euc-kr"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1","replace")


def cdx_query(pattern,start=2003,end=2004,*,collapse=True,limit=10000):
    params=[
        ("url",pattern),("from",str(start)),("to",str(end)),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("filter","statuscode:200"),("limit",str(limit)),
    ]
    if collapse:
        params.append(("collapse","urlkey"))
    rows=json.loads(
        request(CDX+"?"+urllib.parse.urlencode(params)).decode("utf-8","replace")
    )
    if not rows:
        return []
    header,*body=rows
    idx={name:i for i,name in enumerate(header)}
    return [
        {key:row[pos] for key,pos in idx.items()}
        for row in body
        if isinstance(row,list) and len(row)>=len(header)
    ]


def archived_links(timestamp,original):
    url=WAYBACK.format(
        timestamp=timestamp,
        url=urllib.parse.quote(original,safe=":/?&=%#+,;@[]!$'()*"),
    )
    parser=LinkParser()
    parser.feed(decode_html(request(url,timeout=45)))
    out=[]
    for href,anchor in parser.links:
        absolute=urllib.parse.urljoin(original,href)
        if DOWNLOAD_EXT.search(absolute) or INTEREST.search(absolute) or INTEREST.search(anchor):
            out.append((absolute,anchor))
    return out


def safe(value,limit=500):
    value=" ".join(str(value).split())
    value="".join(ch for ch in value if ch >= " " and ch!="\x7f")
    return value[:limit]


def select_launch_snapshots(rows,*,limit=24):
    def rank(row):
        ts=str(row.get("timestamp",""))
        launch=0 if "20030701" <= ts[:8] <= "20030930" else 1
        return (launch,ts)
    unique={}
    for row in rows:
        key=(str(row.get("timestamp","")),str(row.get("original","")))
        unique.setdefault(key,row)
    return sorted(unique.values(),key=rank)[:limit]


def main():
    surfaces=[
        ("game3","game3.netmarble.net/stoneage/*"),
        ("game3-www","www.game3.netmarble.net/stoneage/*"),
        ("brand","stoneage.netmarble.net/*"),
        ("brand-www","www.stoneage.netmarble.net/*"),
    ]
    roots=[
        ("game3-root","http://game3.netmarble.net/stoneage/"),
        ("game3-root-www","http://www.game3.netmarble.net/stoneage/"),
        ("brand-root","http://stoneage.netmarble.net/"),
        ("brand-root-www","http://www.stoneage.netmarble.net/"),
    ]

    print("StoneAge Korea Netmarble 1.74 archive client probe — R1")
    print("SCOPE|metadata-and-link-targets-only|no-client-binary-download")
    print("YEARS|from=2003|to=2004")
    errors=[]
    indexed=[]

    for surface,pattern in surfaces:
        try:
            rows=cdx_query(pattern)
        except Exception as exc:
            errors.append((surface,type(exc).__name__,str(exc)))
            continue
        for row in rows:
            indexed.append((surface,row))

    uniq={}
    for surface,row in indexed:
        original=str(row.get("original",""))
        uniq.setdefault((surface,original),(surface,row))
    print(f"COUNT|indexed_urls|{len(uniq)}")
    for surface,row in sorted(
        uniq.values(),
        key=lambda x:(x[0],str(x[1].get("original","")).lower()),
    ):
        print(
            "URL|"
            + "|".join(
                safe(x)
                for x in (
                    surface,row.get("timestamp",""),row.get("statuscode",""),
                    row.get("mimetype",""),row.get("length",""),
                    row.get("digest",""),row.get("original",""),
                )
            )
        )

    snapshots=[]
    for surface,root in roots:
        try:
            rows=cdx_query(root,collapse=False,limit=500)
        except Exception as exc:
            errors.append((surface,type(exc).__name__,str(exc)))
            continue
        for row in select_launch_snapshots(rows):
            snapshots.append((surface,row))

    links=set()
    for surface,row in snapshots:
        ts=str(row.get("timestamp",""))
        original=str(row.get("original",""))
        try:
            found=archived_links(ts,original)
        except Exception as exc:
            errors.append((surface+"@"+ts,type(exc).__name__,str(exc)))
            continue
        for target,anchor in found:
            links.add((surface,ts,target,anchor))

    print(f"COUNT|root_snapshots_probed|{len(snapshots)}")
    print(f"COUNT|interesting_links|{len(links)}")
    print(f"COUNT|download_links|{sum(1 for _,_,target,_ in links if DOWNLOAD_EXT.search(target))}")
    for surface,ts,target,anchor in sorted(links):
        kind="download" if DOWNLOAD_EXT.search(target) else "interest"
        print(
            "LINK|"
            + "|".join(safe(x) for x in (surface,ts,kind,target,anchor))
        )
    for surface,kind,message in errors:
        print(f"ERROR|{safe(surface)}|{safe(kind)}|{safe(message)}")
    print(f"COUNT|errors|{len(errors)}")


if __name__=="__main__":
    main()
