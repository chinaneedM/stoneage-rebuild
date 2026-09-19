#!/usr/bin/env python3
"""Resolve archived GameTime StoneAge records from a bounded set of proven Wayback anchors.

HTML/CDX metadata only. No client payload bytes are requested.
"""

from __future__ import annotations

import concurrent.futures
import html.parser
import json
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
CDX="https://web.archive.org/cdx/search/cdx"

ANCHORS=[
    (
        "stoneage-search",
        "20010701053412",
        "http://www.gametime.co.kr/data/data_list.asp?"
        "search_word=%bd%ba%c5%e6%bf%a1%c0%cc%c1%f6&category=online",
    ),
    (
        "stoneage-news-idx11",
        "20001208213500",
        "http://www.gametime.co.kr/webzine/online/news/"
        "content.asp?name=New&IDX=11&Cpage=1&page=",
    ),
    (
        "webzine-download",
        "20001109191700",
        "http://www.gametime.co.kr/webzine/online/download.asp",
    ),
    (
        "webzine-down-record",
        "20010417163846",
        "http://www.gametime.co.kr/webzine/online/down/"
        "content.asp?name=online&num=34&ref=42&page=2",
    ),
]

INTEREST=re.compile(
    r"(?i)(스톤에이지|stone\s*age|stoneage|GW_IDX|GW_Name|download|"
    r"data_(?:view|read)|content\.asp|view\.asp|read\.asp|\.exe|\.zip|"
    r"온라인|정식|체험)"
)
CHILD=re.compile(
    r"(?i)(GW_IDX|GW_Name|download\.asp|data_(?:view|read)\.asp|"
    r"/down/content\.asp)"
)
MAX_CANDIDATES=24


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.text=[]
        self._href=None
        self._onclick=None
        self._label=[]

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        tag=tag.lower()
        if tag=="a":
            self._href=a.get("href")
            self._onclick=a.get("onclick")
            self._label=[]
        for key in ("src","action"):
            if a.get(key):
                self.links.append((tag,key,a[key],""))

    def handle_data(self,data):
        if data.strip():
            self.text.append(data)
        if self._href is not None or self._onclick is not None:
            self._label.append(data)

    def handle_endtag(self,tag):
        if tag.lower()=="a" and (self._href is not None or self._onclick is not None):
            label=" ".join(self._label).strip()
            if self._href:
                self.links.append(("a","href",self._href,label))
            if self._onclick:
                self.links.append(("a","onclick",self._onclick,label))
            self._href=None
            self._onclick=None
            self._label=[]


def clean(v,limit=1000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=9,attempts=1):
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
                time.sleep(0.4*(i+1))
    raise last


def decode(body):
    for enc in ("cp949","euc-kr","utf-8"):
        try:
            return body.decode(enc)
        except UnicodeDecodeError:
            pass
    return body.decode("latin-1","replace")


def replay_urls(ts,url):
    return [
        f"https://web.archive.org/web/{ts}id_/{url}",
        f"https://web.archive.org/web/{ts}/{url}",
    ]


def fetch_replay(ts,url):
    errors=[]
    for replay in replay_urls(ts,url):
        try:
            status,final,body=get(replay,9,1)
            return status,final,body,replay
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
    raise RuntimeError("; ".join(errors))


def html_unescape(value):
    return value.replace("&amp;","&").replace("&#38;","&")


def is_gametime(url):
    host=(urllib.parse.urlsplit(url).hostname or "").lower()
    return host in {"gametime.co.kr","www.gametime.co.kr"}


def js_urls(base,value):
    out=set()
    raw=html_unescape(value)
    for m in re.finditer(
        r"""(?i)(?:location(?:\.href)?\s*=|window\.open\s*\(|open\s*\()\s*['"]([^'"]+)""",
        raw,
    ):
        u=urllib.parse.urljoin(base,m.group(1))
        if is_gametime(u):
            out.add(u)
    for m in re.finditer(
        r"""(?i)['"]([^'"]*(?:download|data_(?:view|read)|view\.asp|read\.asp)[^'"]*)['"]""",
        raw,
    ):
        u=urllib.parse.urljoin(base,m.group(1))
        if is_gametime(u):
            out.add(u)
    idxs=set(re.findall(r"(?i)GW_IDX\s*[=,]\s*['\"]?(\d+)",raw))
    idxs.update(re.findall(r"(?i)(?:download|down)\s*\(\s*['\"]?(\d+)",raw))
    for idx in idxs:
        root="http://www.gametime.co.kr/data/"
        out.add(root+f"download.asp?GW_IDX={idx}&GW_Name=Online")
        out.add(root+f"data_view.asp?GW_IDX={idx}&GW_Name=Online")
    return out


def snippets(text,radius=220):
    out=[]
    seen=set()
    for m in INTEREST.finditer(text):
        value=clean(text[max(0,m.start()-radius):min(len(text),m.end()+radius)],650)
        if value not in seen:
            seen.add(value)
            out.append(value)
        if len(out)>=80:
            break
    return out


def analyze_anchor(label,ts,url):
    status,final,body,replay=fetch_replay(ts,url)
    text=decode(body)
    p=Parser()
    p.feed(text)
    links=[]
    candidates=set()
    for tag,attr,target,link_label in p.links:
        if attr in ("href","src","action") and not target.lower().startswith("javascript:"):
            absolute=urllib.parse.urljoin(url,html_unescape(target))
        else:
            absolute=target
        if INTEREST.search(absolute+" "+link_label):
            links.append((tag,attr,absolute,link_label))
        if attr=="href":
            u=urllib.parse.urljoin(url,html_unescape(target))
            if CHILD.search(target+" "+link_label) and is_gametime(u):
                candidates.add(u)
        if attr=="onclick" or target.lower().startswith("javascript:"):
            candidates.update(js_urls(url,target))
    candidates.update(js_urls(url,text))
    ids=sorted(set(re.findall(r"(?i)GW_IDX(?:=|%3D)(\d+)",text)))
    return {
        "label":label,"timestamp":ts,"url":url,"status":status,"final":final,
        "replay":replay,"snippets":snippets(text),"links":links,
        "candidates":sorted(candidates),"ids":ids,
    }


def cdx_rows(url):
    params=[
        ("url",url),("from","2000"),("to","2002"),("output","json"),
        ("fl","timestamp,original,mimetype,statuscode,digest,length"),
        ("collapse","digest"),("limit","100"),
    ]
    _,_,body=get(CDX+"?"+urllib.parse.urlencode(params),10,1)
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


def main():
    print("StoneAge GameTime archived record resolver — R2")
    print("SCOPE|bounded-archived-html-and-cdx-metadata-only|no-client-payload-download")
    print(f"COUNT|proven_anchors|{len(ANCHORS)}")

    results=[]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs={ex.submit(analyze_anchor,*a):a for a in ANCHORS}
        for fut,a in futs.items():
            try:
                results.append(fut.result())
            except Exception as exc:
                errors.append(("anchor",a[0],a[2],type(exc).__name__,str(exc)))

    candidates={
        "http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online",
        "http://www.gametime.co.kr/data/data_view.asp?GW_IDX=9&GW_Name=Online",
        "http://www.gametime.co.kr/webzine/online/download.asp?name=%BD%BA%C5%E6%BF%A1%C0%CC%C1%F6",
    }

    for r in sorted(results,key=lambda x:x["label"]):
        print(
            f"ANCHOR_RESULT|label={clean(r['label'])}|timestamp={clean(r['timestamp'])}|"
            f"status={r['status']}|replay={clean(r['replay'])}|gw_ids={clean(','.join(r['ids']))}|"
            f"links={len(r['links'])}|snippets={len(r['snippets'])}|"
            f"child_candidates={len(r['candidates'])}"
        )
        for value in r["snippets"]:
            print(f"SNIPPET|anchor={clean(r['label'])}|text={clean(value,700)}")
        for tag,attr,value,link_label in r["links"]:
            print(
                f"LINK|anchor={clean(r['label'])}|tag={clean(tag)}|attr={clean(attr)}|"
                f"value={clean(value)}|label={clean(link_label,350)}"
            )
        for u in r["candidates"]:
            if is_gametime(u):
                candidates.add(u)

    selected=sorted(candidates)[:MAX_CANDIDATES]
    print(f"COUNT|candidate_urls|{len(candidates)}")
    print(f"COUNT|candidate_urls_selected|{len(selected)}")
    for u in selected:
        print(f"CANDIDATE|url={clean(u)}")

    cdx_results=[]
    def cdx_one(u):
        try:
            return u,cdx_rows(u),None
        except Exception as exc:
            return u,[],(type(exc).__name__,str(exc))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for u,rows,error in ex.map(cdx_one,selected):
            if error:
                errors.append(("cdx","candidate",u,error[0],error[1]))
            else:
                cdx_results.append((u,rows))

    for u,rows in cdx_results:
        print(f"CDX|url={clean(u)}|rows={len(rows)}")
        for row in rows:
            print(
                f"CDX_ROW|candidate={clean(u)}|timestamp={clean(row.get('timestamp'))}|"
                f"url={clean(row.get('original'))}|mime={clean(row.get('mimetype'))}|"
                f"status={clean(row.get('statuscode'))}|digest={clean(row.get('digest'))}|"
                f"length={clean(row.get('length'))}"
            )

    print(f"COUNT|anchors_replayed|{len(results)}")
    print(f"COUNT|cdx_candidates_completed|{len(cdx_results)}")
    print(f"COUNT|errors|{len(errors)}")
    for phase,label,url,kind,msg in errors:
        print(
            f"ERROR|phase={clean(phase)}|label={clean(label)}|url={clean(url)}|"
            f"kind={clean(kind)}|message={clean(msg)}"
        )


if __name__=="__main__":
    main()
