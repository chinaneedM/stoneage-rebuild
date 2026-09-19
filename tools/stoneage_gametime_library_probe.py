#!/usr/bin/env python3
"""Probe public Korean catalog metadata for the 2001 GameTime StoneAge guide bonus CD.

Metadata only. No book/CD payload is requested. R2 focuses on structural identifiers
and holdings/detail navigation rather than dumping generic page links.
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
KOLIS="https://www.nl.go.kr/kolisnet/search/searchResultAllList.do"
KEYWORDS=(
    "스톤 에이지","스톤에이지","2 개 도서관 소장","2개 도서관 소장",
    "컴팩트디스크","딸림자료","청구기호","등록번호","제어번호","소장기관",
)
STRUCTURAL_RE=(
    re.compile(r"(?i)\b[MU]\d{6,}\b"),
    re.compile(r"(?i)\b(?:control_no|controlNo|controlno|rec_key|recKey|reckey|manage_code|manageCode|managecode)\b[^\s<>'\"]{0,120}"),
    re.compile(r"(?i)[0-9a-f]{32,64}"),
    re.compile(r"(?i)(?:search|detail|hold|holding|library)[A-Za-z0-9_./?=&%:+-]{3,180}"),
)


class AnchorParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors=[]
        self._attrs=None
        self._text=[]

    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            self._attrs=dict(attrs)
            self._text=[]

    def handle_data(self,data):
        if self._attrs is not None:
            self._text.append(data)

    def handle_endtag(self,tag):
        if tag.lower()=="a" and self._attrs is not None:
            self.anchors.append((self._attrs," ".join(self._text)))
            self._attrs=None
            self._text=[]


def clean(v,limit=900):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def get(url,timeout=15,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,
                "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"ko-KR,ko;q=0.9,en;q=0.7",
            })
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.status,r.geturl(),r.read()
        except Exception as exc:
            last=exc
            if i+1<attempts:
                time.sleep(0.6)
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


def contexts(text,needles,radius=260,limit=30):
    low=text.lower()
    out=[]
    seen=set()
    for needle in needles:
        n=needle.lower()
        pos=0
        while len(out)<limit:
            i=low.find(n,pos)
            if i<0:
                break
            value=clean(text[max(0,i-radius):min(len(text),i+len(needle)+radius)],650)
            if value not in seen:
                seen.add(value)
                out.append((needle,value))
            pos=i+max(1,len(n))
    return out


def structural_tokens(text):
    found=set()
    for rx in STRUCTURAL_RE:
        for m in rx.finditer(text):
            found.add(clean(m.group(0),220))
    return sorted(found)


def interesting_anchor(attrs,label):
    blob=" ".join([label]+[f"{k}={v}" for k,v in attrs.items()])
    low=blob.lower()
    return (
        any(k.lower() in low for k in KEYWORDS)
        or ISBN10 in blob or ISBN13 in blob
        or "riss.kr/link?id=" in low
        or any(x in low for x in ("detail","hold","library","searchresult","control","reckey","manage"))
    )


def anchor_rows(text,base):
    p=AnchorParser()
    try:
        p.feed(text)
    except Exception:
        pass
    out=[]
    seen=set()
    for attrs,label in p.anchors:
        if not interesting_anchor(attrs,label):
            continue
        href=attrs.get("href","")
        if href:
            href=urllib.parse.urljoin(base,href)
        attr_text=";".join(f"{k}={v}" for k,v in sorted(attrs.items()) if k in {
            "href","onclick","id","class","data-id","data-value","data-key","title"
        })
        row=(clean(label,260),clean(href,500),clean(attr_text,700))
        if row not in seen:
            seen.add(row)
            out.append(row)
    return out[:120]


def targets():
    params=urllib.parse.urlencode({"keyword1":ISBN10,"keywordType1":"total","tab":"ALL"})
    rows=[("kolis-isbn10",KOLIS+"?"+params)]
    rows += [(f"riss-{rid}",f"https://www.riss.kr/link?id={rid}") for rid in RISS_IDS]
    return rows


def probe(label,url):
    try:
        status,final,body=get(url)
    except Exception as exc:
        return {"label":label,"url":url,"error":f"{type(exc).__name__}: {exc}"}
    raw=decode(body)
    plain=strip_markup(raw)
    return {
        "label":label,"url":url,"error":"","status":status,"final":final,
        "plain_contexts":contexts(plain,KEYWORDS,220,24),
        "raw_contexts":contexts(raw,(ISBN10,*RISS_IDS,*TITLE_TERMS,"2 개 도서관 소장","fnEdtionList","searchResultEditonList.do","24118251","LibraryList.do","providerId=07","LibraryLocalBibno"),520,36),
        "tokens":structural_tokens(raw),
        "edition_keys":sorted(set(re.findall(r"fnEdtionList\(\s*[\"']?(\d+)",raw))),
        "anchors":anchor_rows(raw,final),
    }


def main():
    print("StoneAge GameTime 2001 library supplementary-material probe — R3")
    print("SCOPE|public-catalog-metadata-only|no-book-or-cd-payload-download")
    print("METHOD|focused-kolis-isbn+riss-aliases+edition-key-and-holdings-call-extraction")
    print(f"TARGET|isbn10={ISBN10}|isbn13={ISBN13}|riss_ids={','.join(RISS_IDS)}")
    results=[probe(label,url) for label,url in targets()]
    print(f"COUNT|queries|{len(results)}")
    print(f"COUNT|errors|{sum(bool(r.get('error')) for r in results)}")
    for r in results:
        if r.get("error"):
            print(f"ERROR|source={clean(r['label'])}|url={clean(r['url'])}|message={clean(r['error'])}")
            continue
        print(f"RESPONSE|source={clean(r['label'])}|status={r['status']}|final={clean(r['final'])}")
        for token,value in r["plain_contexts"]:
            print(f"FACT_CONTEXT|source={clean(r['label'])}|token={clean(token)}|text={clean(value,620)}")
        for token,value in r["raw_contexts"]:
            print(f"RAW_CONTEXT|source={clean(r['label'])}|token={clean(token)}|html={clean(value,820)}")
        for key in r["edition_keys"]:
            print(f"EDITION_KEY|source={clean(r['label'])}|value={clean(key)}")
        for value in r["tokens"]:
            print(f"STRUCT|source={clean(r['label'])}|value={clean(value)}")
        for label_text,href,attrs in r["anchors"]:
            print(f"ANCHOR|source={clean(r['label'])}|label={label_text}|href={href}|attrs={attrs}")


if __name__=="__main__":
    main()
