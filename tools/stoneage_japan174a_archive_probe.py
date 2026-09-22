#!/usr/bin/env python3
"""Probe public web-archive indexes for Japanese StoneAge 1.74a client metadata.

Only CDX metadata and link targets extracted from transient archived HTML are
emitted. Client binaries and archived page bodies are never stored.
"""

from __future__ import annotations

import html.parser
import json
import re
import urllib.error
import urllib.parse
import urllib.request


UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
ARQUIVO_CDX = "https://arquivo.pt/wayback/cdx"
AVAIL = "https://archive.org/wayback/available"
WAYBACK = "https://web.archive.org/web/{timestamp}id_/{url}"
REQUEST_TIMEOUT_SECONDS = 12
ARCHIVE_TIMEOUT_SECONDS = 15
ROOT_SNAPSHOT_LIMIT = 3
HANGAME_GAMANIA_STONEAGE_PATTERN = "hangame.gamania.co.jp/stoneage/*"
HANGAME_GAMANIA_STONEAGE_ROOT = "http://hangame.gamania.co.jp/stoneage/"
ROOT_KEY_DATES = ("20031212","20031216","20031217","20040115")

DOWNLOAD_EXT = re.compile(
    r"(?i)\.(?:exe|zip|rar|cab|lzh|lha|arj|gz|tgz|bz2|msi)(?:$|[?#])"
)
INTEREST = re.compile(
    r"(?i)(stone\s*age|stoneage|client|download|setup|install|patch|update|"
    r"クライアント|ダウンロード|インストール|セットアップ|パッチ|"
    r"アップデート)"
)


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str,str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        attrs = dict(attrs)
        self._href = attrs.get("href")
        self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, "".join(self._text).strip()))
            self._href = None
            self._text = []


def request(
    url: str,
    *,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> bytes:
    """Perform one bounded request; the caller records failures in the report."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read()
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
        raise RuntimeError(f"request failed: {url}: {exc}") from exc


def decode_html(data: bytes) -> str:
    for encoding in ("utf-8","cp932","shift_jis","euc-jp","iso2022_jp"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1","replace")


def cdx_query(
    url_pattern: str,
    start: int,
    end: int,
    *,
    collapse: bool = True,
    limit: int = 2000,
):
    params = [
        ("url",url_pattern),
        ("from",str(start)),
        ("to",str(end)),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("filter","statuscode:200"),
        ("limit",str(limit)),
    ]
    if collapse:
        params.append(("collapse","urlkey"))
    raw=request(CDX+"?"+urllib.parse.urlencode(params))
    rows=json.loads(raw.decode("utf-8","replace"))
    if not rows:
        return []
    header,*body=rows
    indexes={name:i for i,name in enumerate(header)}
    return [
        {key:row[idx] for key,idx in indexes.items()}
        for row in body
        if isinstance(row,list) and len(row)>=len(header)
    ]


def parse_arquivo_cdx(data: bytes):
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


def arquivo_cdx_query(
    url_pattern: str,
    start: int,
    end: int,
    *,
    limit: int = 2000,
):
    params=[
        ("url",url_pattern),
        ("from",str(start)),
        ("to",str(end)),
        ("output","json"),
        ("fields","timestamp,url,status,mime,digest,length"),
        ("filter","=status:200"),
        ("limit",str(limit)),
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


def archived_links(timestamp: str, original: str):
    target=WAYBACK.format(
        timestamp=timestamp,
        url=urllib.parse.quote(original,safe=":/?&=%#+,;@[]!$'()*"),
    )
    body=request(target,timeout=ARCHIVE_TIMEOUT_SECONDS)
    parser=LinkParser()
    parser.feed(decode_html(body))
    out=[]
    for href,anchor in parser.links:
        absolute=urllib.parse.urljoin(original,href)
        if DOWNLOAD_EXT.search(absolute) or INTEREST.search(absolute) or INTEREST.search(anchor):
            out.append((absolute,anchor))
    return out


def safe(value: str, limit: int = 500) -> str:
    value=" ".join(str(value).split())
    value="".join(ch for ch in value if ch >= " " and ch != "\x7f")
    return value[:limit]


def select_launch_snapshots(rows, *, limit: int = 8):
    """Prefer snapshots around the 2003-12-12/16 launch window."""
    def rank(row):
        ts=str(row.get("timestamp",""))
        launch=0 if "20031201" <= ts[:8] <= "20040131" else 1
        return (launch,ts)
    unique={}
    for row in rows:
        key=(str(row.get("timestamp","")),str(row.get("original","")))
        unique.setdefault(key,row)
    return sorted(unique.values(),key=rank)[:limit]


def snapshot_period(timestamp):
    """Separate launch-window evidence from pre/post-launch archive clues."""
    day=str(timestamp)[:8]
    if len(day) != 8 or not day.isdigit():
        return "unknown"
    if "20031201" <= day <= "20040131":
        return "launch"
    if day < "20031201":
        return "prelaunch"
    return "postlaunch"


def main() -> None:
    # Query each official StoneAge subtree once, then filter archive rows locally.
    # This keeps request count bounded while retaining executable/archive URLs
    # and paths that explicitly mention client/download/update concepts.
    surfaces=[
        ("official-bare","stoneage.to/*"),
        ("official-www","www.stoneage.to/*"),
        ("hangame-sa","www.hangame.co.jp/publish/sa/*"),
        ("hangame-sa-bare","hangame.co.jp/publish/sa/*"),
        ("hangame-gamania-stoneage",HANGAME_GAMANIA_STONEAGE_PATTERN),
        ("hangame-bare-stoneage","hangame.co.jp/*stoneage*"),
        ("hangame-www-stoneage","www.hangame.co.jp/*stoneage*"),
    ]
    roots=[
        ("official-root-bare","http://stoneage.to/"),
        ("official-root-www","http://www.stoneage.to/"),
        ("official-root-bare-https","https://stoneage.to/"),
        ("official-root-www-https","https://www.stoneage.to/"),
        ("hangame-sa-main","http://www.hangame.co.jp/publish/sa/main.asp"),
        ("hangame-sa-root","http://www.hangame.co.jp/publish/sa/"),
        ("hangame-gamania-root",HANGAME_GAMANIA_STONEAGE_ROOT),
    ]

    print("StoneAge Japan 1.74a public archive client probe — R2")
    print("SCOPE|metadata-and-link-targets-only|no-client-binary-download")
    print("YEARS|from=2003|to=2005")
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
        (
            "wayback",
            lambda pattern: cdx_query(
                pattern,2003,2005,limit=5000
            ),
        ),
        (
            "arquivo",
            lambda pattern: arquivo_cdx_query(
                pattern,2003,2005,limit=5000
            ),
        ),
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

    dedup={}
    for backend,surface,row in indexed:
        original=str(row.get("original",""))
        dedup.setdefault(
            (backend,surface,original),
            (backend,surface,row),
        )
    print(f"COUNT|indexed_urls|{len(dedup)}")
    for backend,surface,row in sorted(
        dedup.values(),
        key=lambda item:(
            item[0],item[1],str(item[2].get("original","")).lower()
        ),
    ):
        print(
            "URL|"
            + "|".join(
                safe(x)
                for x in (
                    backend,
                    surface,
                    row.get("timestamp",""),
                    row.get("statuscode",""),
                    row.get("mimetype",""),
                    row.get("length",""),
                    row.get("digest",""),
                    row.get("original",""),
                )
            )
        )

    root_snapshots=[]
    root_stats={
        "cdx_succeeded":0,
        "cdx_failed":0,
        "availability_succeeded":0,
        "availability_failed":0,
        "availability_hits":0,
    }
    for surface,root in roots:
        try:
            rows=cdx_query(root,2003,2005,collapse=False,limit=500)
            root_stats["cdx_succeeded"]+=1
        except Exception as exc:
            rows=[]
            root_stats["cdx_failed"]+=1
            errors.append((surface,type(exc).__name__,str(exc)))
        for row in select_launch_snapshots(rows,limit=ROOT_SNAPSHOT_LIMIT):
            root_snapshots.append((surface,row))

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
            timestamp=str(cap.get("timestamp",""))
            if not timestamp:
                continue
            root_stats["availability_hits"]+=1
            root_snapshots.append(
                (
                    surface,
                    {
                        "timestamp":timestamp,
                        "original":root,
                        "statuscode":cap.get("status",""),
                        "mimetype":"",
                        "digest":"",
                        "length":"",
                    },
                )
            )

    snapshot_unique={}
    for surface,row in root_snapshots:
        key=(
            surface,
            str(row.get("timestamp","")),
            str(row.get("original","")),
        )
        snapshot_unique.setdefault(key,(surface,row))
    root_snapshots=[
        item
        for _,item in sorted(
            snapshot_unique.items(),
            key=lambda pair:pair[0],
        )
    ]

    emitted=set()
    snapshot_period_counts={
        "launch":0,"prelaunch":0,"postlaunch":0,"unknown":0
    }
    for surface,row in root_snapshots:
        timestamp=str(row.get("timestamp",""))
        period=snapshot_period(timestamp)
        snapshot_period_counts[period]+=1
        original=str(row.get("original",""))
        try:
            links=archived_links(timestamp,original)
        except Exception as exc:
            errors.append((surface+"@"+timestamp,type(exc).__name__,str(exc)))
            continue
        for target,anchor in links:
            emitted.add((period,surface,timestamp,target,anchor))

    download_indexed={
        row
        for row in dedup.values()
        if DOWNLOAD_EXT.search(str(row[2].get("original","")))
    }
    download_links={
        row for row in emitted if DOWNLOAD_EXT.search(row[3])
    }
    page_links=emitted-download_links

    print(f"COUNT|root_snapshots_probed|{len(root_snapshots)}")
    print(f"COUNT|root_snapshots_launch_window|{snapshot_period_counts['launch']}")
    print(f"COUNT|root_snapshots_prelaunch|{snapshot_period_counts['prelaunch']}")
    print(f"COUNT|root_snapshots_postlaunch|{snapshot_period_counts['postlaunch']}")
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
    print(f"COUNT|interesting_links|{len(emitted)}")
    print(f"COUNT|page_candidate_links|{len(page_links)}")
    print(f"COUNT|download_indexed_urls|{len(download_indexed)}")
    print(f"COUNT|download_links|{len(download_links)}")
    for period,surface,timestamp,target,anchor in sorted(page_links):
        print(
            "PAGE_LINK|"
            + "|".join(
                safe(x)
                for x in (period,surface,timestamp,"interest",target,anchor)
            )
        )
    for period,surface,timestamp,target,anchor in sorted(download_links):
        print(
            "DOWNLOAD_LINK|"
            + "|".join(
                safe(x)
                for x in (period,surface,timestamp,"download",target,anchor)
            )
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
    payload_hit_count=len(download_indexed)+len(download_links)
    page_candidate_count=(
        len(dedup)-len(download_indexed)+len(page_links)
    )
    result=classify_probe_result(
        hit_count=payload_hit_count,
        successful_queries=successful_queries,
        failed_queries=failed_queries,
    )
    print(
        f"RESULT|{result}|payload_hits={payload_hit_count}|"
        f"page_candidates={page_candidate_count}|"
        f"index_queries_succeeded={successful_queries}|"
        f"index_queries_failed={failed_queries}"
    )


if __name__ == "__main__":
    main()
