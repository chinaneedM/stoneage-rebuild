#!/usr/bin/env python3
"""Probe public web-archive indexes for Japanese StoneAge 1.74a client metadata.

Only CDX metadata and link targets extracted from transient archived HTML are
emitted. Client binaries and archived page bodies are never stored.
"""

from __future__ import annotations

import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request


UA = "stoneage-rebuild-archaeology/1.0"
CDX = "https://web.archive.org/cdx/search/cdx"
WAYBACK = "https://web.archive.org/web/{timestamp}id_/{url}"

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


def request(url: str, *, timeout: int = 30) -> bytes:
    last = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"request failed: {url}: {last}")


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


def archived_links(timestamp: str, original: str):
    target=WAYBACK.format(
        timestamp=timestamp,
        url=urllib.parse.quote(original,safe=":/?&=%#+,;@[]!$'()*"),
    )
    body=request(target,timeout=45)
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


def main() -> None:
    # Keep archive queries narrow. Full-host wildcards are both expensive and
    # low-value for client archaeology; every pattern below is directly
    # download/client related.
    official_patterns=(
        "*.exe","*.zip","*.lzh","*.lha","*.cab","*.msi",
        "*download*","*client*","*setup*","*install*","*patch*","*update*",
    )
    surfaces=[
        (f"official-bare:{pattern}","stoneage.to/"+pattern)
        for pattern in official_patterns
    ] + [
        (f"official-www:{pattern}","www.stoneage.to/"+pattern)
        for pattern in official_patterns
    ] + [
        ("hangame-bare:stoneage","hangame.co.jp/*stoneage*"),
        ("hangame-www:stoneage","www.hangame.co.jp/*stoneage*"),
    ]
    roots=[
        ("official-root-bare","http://stoneage.to/"),
        ("official-root-www","http://www.stoneage.to/"),
        ("official-root-bare-https","https://stoneage.to/"),
        ("official-root-www-https","https://www.stoneage.to/"),
    ]

    print("StoneAge Japan 1.74a public archive client probe — R1")
    print("SCOPE|metadata-and-link-targets-only|no-client-binary-download")
    print("YEARS|from=2003|to=2005")

    errors=[]
    indexed=[]
    for surface,pattern in surfaces:
        try:
            rows=cdx_query(pattern,2003,2005)
        except Exception as exc:
            errors.append((surface,type(exc).__name__,str(exc)))
            continue
        for row in rows:
            indexed.append((surface,row))

    dedup={}
    for surface,row in indexed:
        original=str(row.get("original",""))
        dedup.setdefault((surface,original),(surface,row))
    print(f"COUNT|indexed_urls|{len(dedup)}")
    for surface,row in sorted(
        dedup.values(),
        key=lambda item:(item[0],str(item[1].get("original","")).lower()),
    ):
        print(
            "URL|"
            + "|".join(
                safe(x)
                for x in (
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
    for surface,root in roots:
        try:
            rows=cdx_query(root,2003,2005,collapse=False,limit=500)
        except Exception as exc:
            errors.append((surface,type(exc).__name__,str(exc)))
            continue
        for row in select_launch_snapshots(rows):
            root_snapshots.append((surface,row))

    emitted=set()
    for surface,row in root_snapshots:
        timestamp=str(row.get("timestamp",""))
        original=str(row.get("original",""))
        try:
            links=archived_links(timestamp,original)
        except Exception as exc:
            errors.append((surface+"@"+timestamp,type(exc).__name__,str(exc)))
            continue
        for target,anchor in links:
            emitted.add((surface,timestamp,target,anchor))

    print(f"COUNT|root_snapshots_probed|{len(root_snapshots)}")
    print(f"COUNT|interesting_links|{len(emitted)}")
    print(f"COUNT|download_links|{sum(1 for _,_,target,_ in emitted if DOWNLOAD_EXT.search(target))}")
    for surface,timestamp,target,anchor in sorted(emitted):
        kind="download" if DOWNLOAD_EXT.search(target) else "interest"
        print(
            "LINK|"
            + "|".join(
                safe(x)
                for x in (surface,timestamp,kind,target,anchor)
            )
        )

    for surface,kind,message in errors:
        print(f"ERROR|{safe(surface)}|{safe(kind)}|{safe(message)}")
    print(f"COUNT|errors|{len(errors)}")


if __name__ == "__main__":
    main()
