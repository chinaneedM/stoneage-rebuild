#!/usr/bin/env python3
"""Probe archive indexes for the Korean Netmarble StoneAge 1.74 bridge client.

Only archive metadata and transiently extracted link targets are emitted.
No client binary or archived HTML body is committed.
"""

from __future__ import annotations

import html.parser
import json
import re
import urllib.error
import urllib.parse
import urllib.request


UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
ARQUIVO_CDX="https://arquivo.pt/wayback/cdx"
AVAIL="https://archive.org/wayback/available"
WAYBACK="https://web.archive.org/web/{timestamp}id_/{url}"
REQUEST_TIMEOUT_SECONDS=12
ARCHIVE_TIMEOUT_SECONDS=15
ROOT_SNAPSHOT_LIMIT=3
ROOT_KEY_DATES=("20030721","20030728","20030815","20030915")

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


def request(url,*,timeout=REQUEST_TIMEOUT_SECONDS):
    """Perform one bounded request; the caller records failures in the report."""
    try:
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        with urllib.request.urlopen(req,timeout=timeout) as response:
            return response.read()
    except (urllib.error.URLError,TimeoutError,ConnectionError,OSError) as exc:
        raise RuntimeError(f"request failed: {url}: {exc}") from exc


def decode_html(data):
    for encoding in ("utf-8","cp949","euc-kr"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1","replace")


def cdx_query(pattern,start=2003,end=2004,*,collapse=True,limit=2000):
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


def parse_arquivo_cdx(data):
    """Normalize Arquivo.pt pywb NDJSON records to the Wayback row shape."""
    rows=[]
    for line_number,line in enumerate(
        data.decode("utf-8","replace").splitlines(),
        start=1,
    ):
        line=line.strip()
        if not line:
            continue
        value=json.loads(line)
        if not isinstance(value,dict):
            raise ValueError(
                f"Arquivo.pt CDX line {line_number} is not a JSON object"
            )
        rows.append(
            {
                "timestamp":str(value.get("timestamp","")),
                "original":str(value.get("url","")),
                "statuscode":str(value.get("status","")),
                "mimetype":str(value.get("mime","")),
                "digest":str(value.get("digest","")),
                "length":str(value.get("length","")),
            }
        )
    return rows


def arquivo_cdx_query(pattern,start=2003,end=2004,*,limit=2000):
    params=[
        ("url",pattern),("from",str(start)),("to",str(end)),
        ("output","json"),
        ("fields","timestamp,url,status,mime,digest,length"),
        ("filter","=status:200"),("limit",str(limit)),
    ]
    return parse_arquivo_cdx(
        request(ARQUIVO_CDX+"?"+urllib.parse.urlencode(params))
    )


def classify_probe_result(*,hit_count,successful_queries,failed_queries):
    hit_count=int(hit_count)
    successful_queries=int(successful_queries)
    failed_queries=int(failed_queries)
    if hit_count > 0:
        return "HITS"
    if successful_queries == 0:
        return "INCONCLUSIVE"
    if failed_queries > 0:
        return "PARTIAL_NO_HITS"
    return "BOUNDED_NO_HITS"


def parse_availability_closest(payload):
    snapshots=payload.get("archived_snapshots")
    if not isinstance(snapshots,dict):
        return None
    closest=snapshots.get("closest")
    if not isinstance(closest,dict) or not closest.get("available"):
        return None
    return {
        "timestamp":str(closest.get("timestamp","")),
        "status":str(closest.get("status","")),
        "url":str(closest.get("url","")),
    }


def availability(root,date):
    params=urllib.parse.urlencode({"url":root,"timestamp":date})
    payload=json.loads(
        request(AVAIL+"?"+params,timeout=8).decode("utf-8","replace")
    )
    return parse_availability_closest(payload)


def archived_links(timestamp,original):
    url=WAYBACK.format(
        timestamp=timestamp,
        url=urllib.parse.quote(original,safe=":/?&=%#+,;@[]!$'()*"),
    )
    parser=LinkParser()
    parser.feed(decode_html(request(url,timeout=ARCHIVE_TIMEOUT_SECONDS)))
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


def select_launch_snapshots(rows,*,limit=8):
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
    # Query each official StoneAge subtree once, then filter archive rows locally.
    # This replaces dozens of wildcard requests while preserving every archived
    # executable/archive URL and every path containing a client/download term.
    surfaces=[
        ("game3","game3.netmarble.net/stoneage/*"),
        ("game3-www","www.game3.netmarble.net/stoneage/*"),
        ("game3-cp-site","game3.netmarble.net/cp_site/stoneage/*"),
        ("game3-www-cp-site","www.game3.netmarble.net/cp_site/stoneage/*"),
        ("brand","stoneage.netmarble.net/*"),
        ("brand-www","www.stoneage.netmarble.net/*"),
    ]
    roots=[
        ("game3-root","http://game3.netmarble.net/stoneage/"),
        ("game3-root-www","http://www.game3.netmarble.net/stoneage/"),
        ("game3-cp-site-root","http://game3.netmarble.net/cp_site/stoneage/"),
        ("game3-cp-site-root-index","http://game3.netmarble.net/cp_site/stoneage/index.asp"),
        ("brand-root","http://stoneage.netmarble.net/"),
        ("brand-root-www","http://www.stoneage.netmarble.net/"),
    ]

    print("StoneAge Korea Netmarble 1.74 archive client probe — R1")
    print("SCOPE|metadata-and-link-targets-only|no-client-binary-download")
    print("YEARS|from=2003|to=2004")
    print("INDEX_BACKENDS|wayback,arquivo.pt")
    print(
        f"REQUEST_POLICY|request_timeout={REQUEST_TIMEOUT_SECONDS}|"
        f"archive_timeout={ARCHIVE_TIMEOUT_SECONDS}|"
        f"root_snapshot_limit={ROOT_SNAPSHOT_LIMIT}|"
        f"root_key_dates={','.join(ROOT_KEY_DATES)}|attempts=1"
    )
    errors=[]
    indexed=[]
    index_stats={
        "wayback":{"succeeded":0,"failed":0},
        "arquivo":{"succeeded":0,"failed":0},
    }
    backends=(
        ("wayback",lambda pattern: cdx_query(pattern,limit=5000)),
        ("arquivo",lambda pattern: arquivo_cdx_query(pattern,limit=5000)),
    )

    for backend,query in backends:
        for surface,pattern in surfaces:
            try:
                rows=query(pattern)
            except Exception as exc:
                index_stats[backend]["failed"]+=1
                errors.append(
                    (backend+":"+surface,type(exc).__name__,str(exc))
                )
                continue
            index_stats[backend]["succeeded"]+=1
            for row in rows:
                original=str(row.get("original",""))
                if DOWNLOAD_EXT.search(original) or INTEREST.search(original):
                    indexed.append((backend,surface,row))

    uniq={}
    for backend,surface,row in indexed:
        original=str(row.get("original",""))
        uniq.setdefault(
            (backend,surface,original),
            (backend,surface,row),
        )
    print(f"COUNT|indexed_urls|{len(uniq)}")
    for backend,surface,row in sorted(
        uniq.values(),
        key=lambda x:(x[0],x[1],str(x[2].get("original","")).lower()),
    ):
        print(
            "URL|"
            + "|".join(
                safe(x)
                for x in (
                    backend,surface,row.get("timestamp",""),
                    row.get("statuscode",""),row.get("mimetype",""),
                    row.get("length",""),row.get("digest",""),
                    row.get("original",""),
                )
            )
        )

    snapshots=[]
    root_stats={
        "cdx_succeeded":0,
        "cdx_failed":0,
        "availability_succeeded":0,
        "availability_failed":0,
        "availability_hits":0,
    }
    for surface,root in roots:
        try:
            rows=cdx_query(root,collapse=False,limit=500)
            root_stats["cdx_succeeded"]+=1
        except Exception as exc:
            rows=[]
            root_stats["cdx_failed"]+=1
            errors.append((surface,type(exc).__name__,str(exc)))
        for row in select_launch_snapshots(rows,limit=ROOT_SNAPSHOT_LIMIT):
            snapshots.append((surface,row))

        for date in ROOT_KEY_DATES:
            try:
                cap=availability(root,date)
                root_stats["availability_succeeded"]+=1
            except Exception as exc:
                root_stats["availability_failed"]+=1
                errors.append(
                    (
                        f"availability:{surface}@{date}",
                        type(exc).__name__,
                        str(exc),
                    )
                )
                continue
            if cap is None or cap.get("status") != "200":
                continue
            ts=str(cap.get("timestamp",""))
            if not ts:
                continue
            root_stats["availability_hits"]+=1
            snapshots.append(
                (
                    surface,
                    {
                        "timestamp":ts,
                        "original":root,
                        "statuscode":cap.get("status",""),
                        "mimetype":"",
                        "digest":"",
                        "length":"",
                    },
                )
            )

    snapshot_unique={}
    for surface,row in snapshots:
        key=(
            surface,
            str(row.get("timestamp","")),
            str(row.get("original","")),
        )
        snapshot_unique.setdefault(key,(surface,row))
    snapshots=[
        item
        for _,item in sorted(
            snapshot_unique.items(),
            key=lambda pair:pair[0],
        )
    ]

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
    print(f"COUNT|root_cdx_queries_succeeded|{root_stats['cdx_succeeded']}")
    print(f"COUNT|root_cdx_queries_failed|{root_stats['cdx_failed']}")
    print(
        f"COUNT|root_availability_queries_succeeded|"
        f"{root_stats['availability_succeeded']}"
    )
    print(
        f"COUNT|root_availability_queries_failed|"
        f"{root_stats['availability_failed']}"
    )
    print(f"COUNT|root_availability_hits|{root_stats['availability_hits']}")
    print(f"COUNT|interesting_links|{len(links)}")
    print(f"COUNT|download_links|{sum(1 for _,_,target,_ in links if DOWNLOAD_EXT.search(target))}")
    for surface,ts,target,anchor in sorted(links):
        kind="download" if DOWNLOAD_EXT.search(target) else "interest"
        print(
            "LINK|"
            + "|".join(safe(x) for x in (surface,ts,kind,target,anchor))
        )
    for backend in ("wayback","arquivo"):
        print(
            f"COUNT|{backend}_index_queries_succeeded|"
            f"{index_stats[backend]['succeeded']}"
        )
        print(
            f"COUNT|{backend}_index_queries_failed|"
            f"{index_stats[backend]['failed']}"
        )
    for surface,kind,message in sorted(errors):
        print(f"ERROR|{safe(surface)}|{safe(kind)}|{safe(message)}")
    print(f"COUNT|errors|{len(errors)}")
    successful_queries=(
        sum(item["succeeded"] for item in index_stats.values())
        + root_stats["cdx_succeeded"]
        + root_stats["availability_succeeded"]
    )
    failed_queries=(
        sum(item["failed"] for item in index_stats.values())
        + root_stats["cdx_failed"]
        + root_stats["availability_failed"]
    )
    hit_count=len(uniq)+len(links)
    result=classify_probe_result(
        hit_count=hit_count,
        successful_queries=successful_queries,
        failed_queries=failed_queries,
    )
    print(
        f"RESULT|{result}|hits={hit_count}|"
        f"index_queries_succeeded={successful_queries}|"
        f"index_queries_failed={failed_queries}"
    )


if __name__=="__main__":
    main()
