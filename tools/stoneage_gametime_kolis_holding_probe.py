#!/usr/bin/env python3
"""Resolve the KOLIS edition/holding layer for the 2001 GameTime StoneAge guide.

Public catalog metadata only. This follows the same POST that the KOLIS title link
submits; it never requests book/CD payload bytes.
"""

from __future__ import annotations

import html
import html.parser
import re
import time
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
BASE="https://www.nl.go.kr"
SEARCH=BASE+"/kolisnet/search/searchResultAllList.do?keyword1=8995182121&keywordType1=total&tab=ALL"
TITLE_KEYS=("스톤 에이지","게임타임","도서관 소장","소장기관","소장","청구기호","등록번호","딸림자료","컴팩트디스크","CD","KMO")
ID_RE=re.compile(r"\b(?:KMO|EMO|BMO|CMO|GMO|KJU|KSE|KSI|KVM)\d{6,}\b",re.I)


class FormParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms=[]
        self.current=None

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag.lower()=="form":
            self.current={"attrs":a,"inputs":{}}
        elif self.current is not None and tag.lower()=="input":
            name=a.get("name")
            if name:
                self.current["inputs"][name]=a.get("value","")

    def handle_endtag(self,tag):
        if tag.lower()=="form" and self.current is not None:
            self.forms.append(self.current)
            self.current=None


class AnchorParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows=[]
        self.current=None
        self.text=[]

    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            self.current=dict(attrs)
            self.text=[]

    def handle_data(self,data):
        if self.current is not None:
            self.text.append(data)

    def handle_endtag(self,tag):
        if tag.lower()=="a" and self.current is not None:
            self.rows.append((self.current," ".join(self.text)))
            self.current=None
            self.text=[]


def clean(v,limit=1000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def decode(b):
    for enc in ("utf-8","cp949","euc-kr"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("latin-1","replace")


def get(url,timeout=18,attempts=2):
    last=None
    for i in range(attempts):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":UA,"Accept-Language":"ko-KR,ko;q=0.9,en;q=0.7",
            })
            with urllib.request.urlopen(req,timeout=timeout) as r:
                return r.status,r.geturl(),r.read()
        except Exception as exc:
            last=exc
            if i+1<attempts:
                time.sleep(0.7)
    raise last


def post(url,fields,referer,timeout=18):
    data=urllib.parse.urlencode(fields).encode("utf-8")
    req=urllib.request.Request(url,data=data,headers={
        "User-Agent":UA,
        "Accept-Language":"ko-KR,ko;q=0.9,en;q=0.7",
        "Content-Type":"application/x-www-form-urlencoded",
        "Referer":referer,
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.status,r.geturl(),r.read()


def strip_markup(text):
    text=re.sub(r"(?is)<script\b.*?</script>"," ",text)
    text=re.sub(r"(?is)<style\b.*?</style>"," ",text)
    text=re.sub(r"(?s)<[^>]+>"," ",text)
    return " ".join(html.unescape(text).split())


def context_rows(text,needles=TITLE_KEYS,radius=280):
    low=text.lower()
    out=[]
    seen=set()
    for needle in needles:
        n=needle.lower()
        start=0
        while True:
            i=low.find(n,start)
            if i<0:
                break
            row=clean(text[max(0,i-radius):min(len(text),i+len(needle)+radius)],720)
            if row not in seen:
                seen.add(row)
                out.append((needle,row))
            start=i+max(1,len(n))
            if len(out)>=50:
                return out
    return out


def search_form(raw):
    p=FormParser()
    p.feed(raw)
    for form in p.forms:
        attrs=form["attrs"]
        if attrs.get("name")=="searchParamForm" or "ufKey" in form["inputs"]:
            return attrs,dict(form["inputs"])
    raise RuntimeError("searchParamForm not found")


def edition_key(raw):
    m=re.search(r"fnEdtionList\\(\\s*[\\\"']?(\\d+)",raw)
    if not m:
        raise RuntimeError("edition key not found")
    return m.group(1)


def interesting_anchors(raw,base):
    p=AnchorParser()
    try:
        p.feed(raw)
    except Exception:
        pass
    out=[]
    seen=set()
    for attrs,label in p.rows:
        blob=(label+" "+" ".join(f"{k}={v}" for k,v in attrs.items()))
        if not any(k.lower() in blob.lower() for k in TITLE_KEYS) and not re.search(r"(?i)(detail|holding|library|reckey|ufkey)",blob):
            continue
        href=attrs.get("href","")
        if href:
            href=urllib.parse.urljoin(base,href)
        attr_text=";".join(f"{k}={v}" for k,v in sorted(attrs.items()) if k in {"href","onclick","id","class","title"})
        row=(clean(label,300),clean(href,600),clean(attr_text,800))
        if row not in seen:
            seen.add(row)
            out.append(row)
    return out[:100]


def main():
    print("StoneAge GameTime 2001 KOLIS holding-layer probe — R1")
    print("SCOPE|public-catalog-metadata-only|no-book-or-cd-payload-download")
    s_status,s_final,s_body=get(SEARCH)
    s_raw=decode(s_body)
    key=edition_key(s_raw)
    attrs,fields=search_form(s_raw)
    action=urllib.parse.urljoin(s_final,attrs.get("action") or "/kolisnet/search/searchResultEditonList.do")
    # KOLIS JavaScript explicitly overwrites the form action and ufKey before submit.
    action=BASE+"/kolisnet/search/searchResultEditonList.do"
    fields["ufKey"]=key

    print(f"SEARCH|status={s_status}|final={clean(s_final)}|edition_key={clean(key)}")
    print(f"POST|action={clean(action)}|field_count={len(fields)}|ufKey={clean(fields.get('ufKey'))}")

    try:
        d_status,d_final,d_body=post(action,fields,s_final)
    except Exception as exc:
        print(f"ERROR|phase=edition-post|kind={type(exc).__name__}|message={clean(exc)}")
        return

    raw=decode(d_body)
    plain=strip_markup(raw)
    ids=sorted(set(ID_RE.findall(raw)))
    print(f"DETAIL|status={d_status}|final={clean(d_final)}|bytes={len(d_body)}")
    print(f"IDENTIFIERS|count={len(ids)}|values={clean(','.join(ids))}")

    for token,row in context_rows(plain):
        print(f"FACT_CONTEXT|token={clean(token)}|text={clean(row,760)}")

    for token in ("24118251","ufKey","reckey","RECKEY","KMO","fnEdtionList","fnDetail","searchResult","소장"):
        for _,row in context_rows(raw,(token,),420):
            print(f"RAW_CONTEXT|token={clean(token)}|html={clean(row,900)}")

    for label,href,attr_text in interesting_anchors(raw,d_final):
        print(f"ANCHOR|label={label}|href={href}|attrs={attr_text}")


if __name__=="__main__":
    main()
