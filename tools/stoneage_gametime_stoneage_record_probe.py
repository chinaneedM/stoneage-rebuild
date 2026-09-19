#!/usr/bin/env python3
"""Resolve GameTime's archived 2001 StoneAge search result into record/download identities.

Metadata/HTML only. No client payload bytes are requested.
"""

from __future__ import annotations

import html.parser
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
TS="20010701053412"
SEED=(
    "http://www.gametime.co.kr/data/data_list.asp?"
    "search_word=%bd%ba%c5%e6%bf%a1%c0%cc%c1%f6&category=online"
)
CDX="https://web.archive.org/cdx/search/cdx"
INTEREST=re.compile(
    r"(?i)(스톤에이지|stone\s*age|stoneage|GW_IDX|GW_Name|download|data_view|data_read|"
    r"view\.asp|\.exe|\.zip|온라인|정식|체험)"
)
CHILD=re.compile(r"(?i)(GW_IDX|download|data_(?:view|read)|view\.asp|read\.asp)")


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.forms=[]
        self.text=[]
        self._href=None
        self._label=[]

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        tag=tag.lower()
        if tag=="a":
            href=a.get("href","")
            onclick=a.get("onclick","")
            if href or onclick:
                self._href=(href,onclick)
                self._label=[]
        if tag=="form":
            self.forms.append((a.get("action",""),a.get("method","")))
        for key in ("src","action","onclick"):
            if a.get(key):
                self.links.append((tag,key,a[key],""))

    def handle_data(self,data):
        if data.strip():
            self.text.append(data)
        if self._href is not None:
            self._label.append(data)

    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            href,onclick=self._href
            label=" ".join(self._label).strip()
            if href:
                self.links.append(("a","href",href,label))
            if onclick:
                self.links.append(("a","onclick",onclick,label))
            self._href=None
            self._label=[]


def clean(v,limit=1000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=20,attempts=3):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(
                url,
                headers={"User-Agent":UA,"Accept":"text/html,application/json,text/plain,*/*"},
            )
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.status,r.geturl(),r.read()
        except Exception as exc:
            last=exc
            if i+1<attempts:
                time.sleep(0.7*(i+1))
    raise last


def decode(body):
    for enc in ("cp949","euc-kr","utf-8"):
        try:
            return body.decode(enc)
        except UnicodeDecodeError:
            pass
    return body.decode("latin-1","replace")


def replay_urls(ts,url):
    # Raw replay first: avoids injected Wayback toolbar links.
    return [
        f"https://web.archive.org/web/{ts}id_/{url}",
        f"https://web.archive.org/web/{ts}/{url}",
    ]


def fetch_replay(ts,url):
    errors=[]
    for replay in replay_urls(ts,url):
        try:
            status,final,body=get(replay,20,2)
            return status,final,body,replay
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
    raise RuntimeError("; ".join(errors))


def cdx_rows(url):
    params=[
        ("url",url),("from","2000"),("to","2002"),("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length"),
        ("filter","urlkey:.*"),("collapse","digest"),("limit","100"),
    ]
    # The urlkey filter may not be supported in every CDX deployment; retry
    # without it if the first request fails.
    endpoint=CDX+"?"+urllib.parse.urlencode(params)
    try:
        _,_,body=get(endpoint,20,2)
    except Exception:
        params=[p for p in params if p[0]!="filter"]
        _,_,body=get(CDX+"?"+urllib.parse.urlencode(params),20,2)
    text=body.decode("utf-8","replace").strip()
    if not text:
        return []
    data=json.loads(text)
    if not isinstance(data,list) or not data:
        return []
    header=data[0]
    return [
        {str(header[i]):str(row[i]) if i<len(row) else "" for i in range(len(header))}
        for row in data[1:] if isinstance(row,list)
    ]


def snippets(text,radius=220):
    out=[]
    seen=set()
    for m in INTEREST.finditer(text):
        value=clean(text[max(0,m.start()-radius):min(len(text),m.end()+radius)],600)
        if value not in seen:
            seen.add(value)
            out.append(value)
        if len(out)>=60:
            break
    return out


def js_urls(base,value):
    """Extract URL-like and GW_IDX-like targets from href/onclick JavaScript."""
    out=set()
    raw=html_unescape(value)
    for m in re.finditer(r"""(?i)(?:location(?:\.href)?\s*=|window\.open\s*\(|open\s*\()\s*['"]([^'"]+)""",raw):
        out.add(urllib.parse.urljoin(base,m.group(1)))
    for m in re.finditer(r"""(?i)['"]([^'"]*(?:download|data_(?:view|read)|view\.asp|read\.asp)[^'"]*)['"]""",raw):
        out.add(urllib.parse.urljoin(base,m.group(1)))
    idxs=set(re.findall(r"(?i)GW_IDX\s*[=,]\s*['\"]?(\d+)",raw))
    idxs.update(re.findall(r"(?i)(?:download|down)\s*\(\s*['\"]?(\d+)",raw))
    for idx in idxs:
        out.add(urllib.parse.urljoin(base,f"download.asp?GW_IDX={idx}&GW_Name=Online"))
        out.add(urllib.parse.urljoin(base,f"data_view.asp?GW_IDX={idx}&GW_Name=Online"))
    return out


def html_unescape(value):
    return value.replace("&amp;","&").replace("&#38;","&")


def analyze(url,ts):
    status,final,body,replay=fetch_replay(ts,url)
    text=decode(body)
    p=Parser()
    p.feed(text)
    links=[]
    child=set()
    for tag,attr,target,label in p.links:
        absolute=target
        if attr in ("href","src","action") and not target.lower().startswith("javascript:"):
            absolute=urllib.parse.urljoin(url,target)
        joined=absolute+" "+label
        if INTEREST.search(joined):
            links.append((tag,attr,absolute,label))
        if attr=="href" and CHILD.search(target+" "+label):
            child.add(urllib.parse.urljoin(url,target))
        if attr=="onclick" or target.lower().startswith("javascript:"):
            child.update(js_urls(url,target))
    for m in re.finditer(r"""(?i)(?:href|src|action)\s*=\s*['"]([^'"]+)['"]""",text):
        if CHILD.search(m.group(1)):
            child.add(urllib.parse.urljoin(url,html_unescape(m.group(1))))
    ids=sorted(set(re.findall(r"(?i)GW_IDX(?:=|%3D)(\d+)",text)))
    return {
        "status":status,"final":final,"replay":replay,"text":text,
        "snippets":snippets(text),"links":links,"children":sorted(child),"ids":ids,
    }


def main():
    print("StoneAge GameTime archived record resolver — R1")
    print("SCOPE|archived-html-and-cdx-metadata-only|no-client-payload-download")
    print(f"SEED|timestamp={TS}|url={clean(SEED)}")

    errors=[]
    try:
        seed=analyze(SEED,TS)
    except Exception as exc:
        print(f"FATAL|seed|{type(exc).__name__}|{clean(exc)}")
        return

    print(
        f"SEED_RESULT|status={seed['status']}|replay={clean(seed['replay'])}|"
        f"gw_ids={clean(','.join(seed['ids']))}|child_candidates={len(seed['children'])}|"
        f"interest_links={len(seed['links'])}|snippets={len(seed['snippets'])}"
    )
    for value in seed["snippets"]:
        print(f"SEED_SNIPPET|text={clean(value,650)}")
    for tag,attr,value,label in seed["links"]:
        print(
            f"SEED_LINK|tag={clean(tag)}|attr={clean(attr)}|value={clean(value)}|"
            f"label={clean(label,350)}"
        )
    for child in seed["children"]:
        print(f"CHILD_CANDIDATE|url={clean(child)}")

    # Always include the historically attested GW_IDX=9 candidates even if the
    # archived HTML expresses the action only through opaque JavaScript.
    candidates=set(seed["children"])
    for idx in set(seed["ids"])|{"9"}:
        candidates.add(urllib.parse.urljoin(SEED,f"download.asp?GW_IDX={idx}&GW_Name=Online"))
        candidates.add(urllib.parse.urljoin(SEED,f"data_view.asp?GW_IDX={idx}&GW_Name=Online"))

    followed=[]
    for child in sorted(candidates)[:40]:
        if "web.archive.org" in child.lower():
            continue
        try:
            result=analyze(child,TS)
        except Exception as exc:
            errors.append(("replay",child,type(exc).__name__,str(exc)))
            result=None
        if result is not None:
            followed.append((child,result))
            print(
                f"CHILD_RESULT|url={clean(child)}|status={result['status']}|"
                f"replay={clean(result['replay'])}|gw_ids={clean(','.join(result['ids']))}|"
                f"links={len(result['links'])}|snippets={len(result['snippets'])}"
            )
            for value in result["snippets"]:
                print(f"CHILD_SNIPPET|url={clean(child)}|text={clean(value,650)}")
            for tag,attr,value,label in result["links"]:
                print(
                    f"CHILD_LINK|page={clean(child)}|tag={clean(tag)}|attr={clean(attr)}|"
                    f"value={clean(value)}|label={clean(label,350)}"
                )

        try:
            rows=cdx_rows(child)
        except Exception as exc:
            errors.append(("cdx",child,type(exc).__name__,str(exc)))
            rows=[]
        print(f"CHILD_CDX|url={clean(child)}|rows={len(rows)}")
        for row in rows:
            print(
                f"CDX_ROW|candidate={clean(child)}|timestamp={clean(row.get('timestamp'))}|"
                f"url={clean(row.get('original'))}|mime={clean(row.get('mimetype'))}|"
                f"status={clean(row.get('statuscode'))}|digest={clean(row.get('digest'))}|"
                f"length={clean(row.get('length'))}"
            )

    print(f"COUNT|candidate_children|{len(candidates)}")
    print(f"COUNT|followed_successfully|{len(followed)}")
    print(f"COUNT|errors|{len(errors)}")
    for phase,url,kind,msg in errors:
        print(
            f"ERROR|phase={clean(phase)}|url={clean(url)}|kind={clean(kind)}|"
            f"message={clean(msg)}"
        )


if __name__=="__main__":
    main()
