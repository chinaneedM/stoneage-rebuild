#!/usr/bin/env python3
"""Replay the archived China.com StoneAge giveaway-result article 63271 safely.

The live Dec-2000 StoneAge test-CD giveaway page links to article 63271 as the
post-activity list/results page. Wayback CDX proves multiple captures survive.

This probe intentionally does NOT commit archived raw HTML or any participant
names/addresses/phone numbers. It records only:
- capture/replay success and raw-body hash;
- encoding/title;
- non-personal archaeology token counts;
- coarse privacy-risk markers;
- sanitized first-party path tokens without query strings.

No proprietary binary/game payload is downloaded.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA="stoneage-rebuild-archaeology/1.0"
ORIGINAL="http://game.china.com:80/zh_cn/news/news1/444/20001220/63271.html"
CAPTURES=(
    "20010309223137",
    "20010821105406",
    "20020618233325",
    "20020918074618",
    "20030124210355",
    "20030313075906",
    "20030509054114",
    "20030901054956",
)
MAX_BYTES=512_000

ARCHAEOLOGY_TOKENS=(
    "石器时代",
    "石器時代",
    "测试光盘",
    "測試光碟",
    "测试版",
    "測試版",
    "试玩版",
    "試玩版",
    "免费大赠送",
    "免費大贈送",
    "赠送",
    "贈送",
    "名单",
    "名單",
    "晶合",
    "华义",
    "華義",
    "光盘",
    "光碟",
    "2000年12月",
    "12月15日",
    "12月31日",
    "2001年1月10日",
)

PRIVACY_MARKERS=(
    "地址",
    "姓名",
    "电话",
    "電話",
    "邮编",
    "郵編",
    "邮政编码",
    "電子郵件",
    "电子邮件",
    "E-mail",
    "Email",
)

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title=False
        self.title_parts=[]
        self.text_parts=[]
        self.paths=[]
        self.skip=0

    def handle_starttag(self,tag,attrs):
        low=tag.lower()
        if low in ("script","style"):
            self.skip+=1
        if low=="title":
            self.in_title=True
        if low=="a":
            href=dict(attrs).get("href")
            if href:
                self._add_href(href)

    def handle_endtag(self,tag):
        low=tag.lower()
        if low in ("script","style") and self.skip:
            self.skip-=1
        if low=="title":
            self.in_title=False

    def handle_data(self,data):
        if self.skip:
            return
        if self.in_title:
            self.title_parts.append(data)
        self.text_parts.append(data)

    def _add_href(self,href):
        href=html.unescape(href).strip()
        if not href or href.lower().startswith(("mailto:","javascript:","tel:","#")):
            return
        joined=urllib.parse.urljoin(ORIGINAL,href)
        p=urllib.parse.urlsplit(joined)
        host=(p.hostname or "").lower()
        if host not in ("game.china.com","china.com","www.china.com"):
            return
        path=p.path or "/"
        # Never retain query/fragment values; only first-party path topology.
        if path not in self.paths:
            self.paths.append(path)


def replay_url(timestamp,mode="id_"):
    return f"https://web.archive.org/web/{timestamp}{mode}/{ORIGINAL}"


def fetch(url,timeout=45):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.2",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(MAX_BYTES+1)
        if len(body)>MAX_BYTES:
            raise ValueError(f"body exceeds limit: {len(body)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),r.headers,body


def candidate_encodings(headers,body):
    out=[]
    try:
        cs=headers.get_content_charset()
    except Exception:
        cs=None
    if cs:
        out.append(cs)
    head=body[:8192].decode("latin1","ignore")
    for pat in (
        r'charset\s*=\s*["\']?\s*([a-zA-Z0-9._-]+)',
        r'encoding\s*=\s*["\']\s*([a-zA-Z0-9._-]+)',
    ):
        for m in re.finditer(pat,head,flags=re.I):
            out.append(m.group(1))
    out.extend(["gb18030","gbk","gb2312","utf-8","big5","latin1"])
    seen=[]
    for enc in out:
        e=str(enc).strip().lower()
        if e and e not in seen:
            seen.append(e)
    return seen


def decode_score(text):
    target=sum(text.count(tok) for tok in ARCHAEOLOGY_TOKENS)
    cjk=sum(1 for ch in text if "\u4e00"<=ch<="\u9fff")
    bad=text.count("\ufffd")
    return target*10000 + min(cjk,5000) - bad*50


def decode_body(headers,body):
    best=None
    for enc in candidate_encodings(headers,body):
        try:
            text=body.decode(enc,errors="replace")
        except Exception:
            continue
        score=decode_score(text)
        if best is None or score>best[0]:
            best=(score,enc,text)
    if best is None:
        return "unknown",body.decode("utf-8","replace")
    return best[1],best[2]


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def token_counts(text,tokens):
    return {token:text.count(token) for token in tokens if text.count(token)}


def classify(text):
    arch=token_counts(text,ARCHAEOLOGY_TOKENS)
    privacy=token_counts(text,PRIVACY_MARKERS)
    if (arch.get("名单",0)+arch.get("名單",0)) and privacy:
        role="GIVEAWAY_RESULTS_OR_RECIPIENT_LIST"
    elif arch.get("赠送",0)+arch.get("贈送",0):
        role="GIVEAWAY_RELATED_PAGE"
    else:
        role="UNCLASSIFIED_ARCHIVED_ARTICLE"
    return role,arch,privacy


def main():
    print("StoneAge China.com article 63271 privacy-safe replay — R1")
    print(f"TARGET|original={ORIGINAL}|role=live-giveaway-page-linked-results")
    print("PRIVACY_BOUNDARY|raw archived HTML and participant identities/contact details are never emitted or committed")
    errors=[]
    success=None

    # Try earliest capture first; later captures are fallbacks only.
    for ts in CAPTURES:
        for mode in ("id_","if_"):
            url=replay_url(ts,mode)
            try:
                status,final,headers,body=fetch(url)
                enc,text=decode_body(headers,body)
                parser=PageParser()
                parser.feed(text)
                title=clean(" ".join(parser.title_parts),500)
                visible=" ".join(parser.text_parts)
                role,arch,privacy=classify(visible)
                print(f"REPLAY|timestamp={ts}|mode={mode}|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|encoding={clean(enc)}|title={title}|role={role}|first_party_paths={len(parser.paths)}|final={clean(final)}")
                for token,count in arch.items():
                    print(f"ARCH_TOKEN|token={clean(token)}|count={count}")
                for token,count in privacy.items():
                    print(f"PRIVACY_MARKER|token={clean(token)}|count={count}")
                for path in parser.paths[:80]:
                    print(f"FIRST_PARTY_PATH|{clean(path)}")
                success=(ts,mode,role,title,len(body),len(privacy),len(parser.paths))
                break
            except Exception as exc:
                errors.append((ts,mode,type(exc).__name__,str(exc)))
        if success:
            break

    for ts,mode,kind,message in errors:
        print(f"ERROR|timestamp={ts}|mode={mode}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|captures_registered|{len(CAPTURES)}")
    print(f"COUNT|attempt_errors|{len(errors)}")
    if success:
        ts,mode,role,title,size,privacy_kinds,path_count=success
        print(f"RESOLUTION|ARCHIVED_63271_REPLAY_RECOVERED|timestamp={ts}|mode={mode}|role={role}|bytes={size}|privacy_marker_kinds={privacy_kinds}|first_party_paths={path_count}")
        if role=="GIVEAWAY_RESULTS_OR_RECIPIENT_LIST":
            print("NEXT|Do not recover/commit participant rows. Mine only non-personal page-level carrier tokens and linked first-party archaeology paths.")
        else:
            print("NEXT|Use only page-level non-personal evidence; do not persist raw body.")
    else:
        print("RESOLUTION|ARCHIVED_63271_REPLAY_UNRESOLVED|CDX capture exists but tested replay modes failed")

if __name__=="__main__":
    main()
