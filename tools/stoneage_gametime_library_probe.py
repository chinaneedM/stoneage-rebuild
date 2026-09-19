#!/usr/bin/env python3
"""Probe public Korean library/catalog metadata for the 2001 GameTime StoneAge guide bonus CD.

Metadata only. The probe does not request or download any book/CD payload.
"""

from __future__ import annotations

import html
import html.parser
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
ISBN10="8995182121"
ISBN13="9788995182123"
RISS_IDS=("M10029631","U10029631")
TITLE_TERMS=("스톤 에이지","스톤에이지")
TOKENS=(
    ISBN10,ISBN13,"M10029631","U10029631",
    "스톤 에이지","스톤에이지","게임타임",
    "compact disc","컴팩트디스크","cd-rom","cd 1","부록","딸림자료",
    "국립중앙도서관","소장","청구기호","등록번호","제어번호",
)
KOLIS="https://www.nl.go.kr/kolisnet/search/searchResultAllList.do"


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self._href=None
        self._text=[]

    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            href=dict(attrs).get("href")
            if href:
                self._href=href
                self._text=[]

    def handle_data(self,data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._href is not None:
            self.links.append((self._href," ".join(self._text)))
            self._href=None
            self._text=[]


def clean(v,limit=900):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=20,attempts=3):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(
                url,
                headers={
                    "User-Agent":UA,
                    "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                    "Accept-Language":"ko-KR,ko;q=0.9,en;q=0.7",
                },
            )
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.status,r.geturl(),r.read()
        except Exception as exc:
            last=exc
            if i+1<attempts:
                time.sleep(0.8*(i+1))
    raise last


def decode(b):
    for enc in ("utf-8","cp949","euc-kr"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("latin-1","replace")


def strip_markup(text):
    text=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    text=re.sub(r"(?is)<style\b.*?</style>"," ",text)
    text=re.sub(r"(?s)<[^>]+>"," ",text)
    return " ".join(html.unescape(text).split())


def snippets(text,tokens=TOKENS,radius=180):
    lower=text.lower()
    emitted=set()
    out=[]
    for token in tokens:
        needle=token.lower()
        start=0
        while True:
            i=lower.find(needle,start)
            if i<0:
                break
            s=max(0,i-radius)
            e=min(len(text),i+len(token)+radius)
            value=clean(text[s:e],500)
            if value not in emitted:
                emitted.add(value)
                out.append((token,value))
            start=i+len(needle)
            if len(out)>=80:
                return out
    return out


def relevant_link(href,label):
    joined=(href+" "+label).lower()
    return any(t.lower() in joined for t in TOKENS) or "riss.kr/link?id=" in joined


def kolis_urls():
    rows=[]
    for q in (ISBN10,ISBN13,*TITLE_TERMS):
        for kind in ("total","title","standardNumber"):
            params=urllib.parse.urlencode({"keyword1":q,"keywordType1":kind,"tab":"ALL"})
            rows.append((f"kolis-{kind}-{q}",KOLIS+"?"+params))
    return rows


def riss_urls():
    return [(f"riss-{rid}",f"https://www.riss.kr/link?id={rid}") for rid in RISS_IDS]


def probe(label,url):
    try:
        status,final,body=get(url)
    except Exception as exc:
        return {
            "label":label,"url":url,"error":f"{type(exc).__name__}: {exc}",
            "status":"","final":"","snippets":[],"links":[],"ids":[],
        }

    text=decode(body)
    plain=strip_markup(text)
    p=LinkParser()
    try:
        p.feed(text)
    except Exception:
        pass

    links=[]
    for href,label_text in p.links:
        absolute=urllib.parse.urljoin(final,href)
        if relevant_link(absolute,label_text):
            links.append((absolute,clean(label_text,250)))

    ids=sorted(set(re.findall(r"(?i)(?:[?&]id=|\b)([MU]\d{6,})",text)))
    return {
        "label":label,"url":url,"error":"","status":status,"final":final,
        "snippets":snippets(plain),"links":links[:80],"ids":ids,
    }


def main():
    print("StoneAge GameTime 2001 library supplementary-material probe — R1")
    print("SCOPE|public-catalog-metadata-only|no-book-or-cd-payload-download")
    print(f"TARGET|isbn10={ISBN10}|isbn13={ISBN13}|riss_ids={','.join(RISS_IDS)}")
    targets=kolis_urls()+riss_urls()
    results=[probe(label,url) for label,url in targets]

    print(f"COUNT|queries|{len(results)}")
    print(f"COUNT|errors|{sum(bool(r['error']) for r in results)}")
    print(f"COUNT|responses|{sum(not r['error'] for r in results)}")
    print(f"COUNT|snippet_hits|{sum(len(r['snippets']) for r in results)}")
    print(f"COUNT|relevant_links|{sum(len(r['links']) for r in results)}")

    for r in results:
        if r["error"]:
            print(f"ERROR|source={clean(r['label'])}|url={clean(r['url'])}|message={clean(r['error'])}")
            continue
        print(
            f"RESPONSE|source={clean(r['label'])}|status={r['status']}|"
            f"requested={clean(r['url'])}|final={clean(r['final'])}|ids={clean(','.join(r['ids']))}"
        )
        for token,value in r["snippets"]:
            print(f"SNIPPET|source={clean(r['label'])}|token={clean(token)}|text={clean(value,520)}")
        seen=set()
        for href,label_text in r["links"]:
            key=(href,label_text)
            if key in seen:
                continue
            seen.add(key)
            print(f"LINK|source={clean(r['label'])}|href={clean(href)}|label={clean(label_text)}")


if __name__=="__main__":
    main()
