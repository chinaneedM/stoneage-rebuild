#!/usr/bin/env python3
"""Replay the exact 2001-12-04 Waei StoneAge2 upgrade.asp capture.

Wayback Availability identifies this capture even though CDX does not expose
it through the tested exact queries. It predates the Jan/Feb 2002 2.5 rollout
and may preserve the preceding 2.X upgrade/download topology. Derived text,
hrefs and response hashes only; payload targets are never downloaded.
"""
from __future__ import annotations
import hashlib,html,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TIMESTAMP="20011204165711"
ORIGINAL="http://www.waei.com.cn:80/ZHUANQU/stoneage2/tyro/upgrade.asp"
TERMS=("石器时代","升级","下载","客户端","完整","2.0","2.5","1.82","2.X","版本","程序")
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".msi",".001",".002",".vcd",".iso")

def clean(v,limit=3500):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def urls():
    return (
        ("id",f"https://web.archive.org/web/{TIMESTAMP}id_/{ORIGINAL}"),
        ("if",f"https://web.archive.org/web/{TIMESTAMP}if_/{ORIGINAL}"),
        ("plain",f"https://web.archive.org/web/{TIMESTAMP}/{ORIGINAL}"),
    )

def fetch(url,timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),body

def decode(body):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try:return body.decode(enc)
        except Exception:pass
    return body.decode("utf-8","replace")

def textify(raw):
    t=re.sub(r"(?is)<script\b.*?</script>"," ",raw)
    t=re.sub(r"(?is)<style\b.*?</style>"," ",t)
    t=re.sub(r"(?is)<[^>]+>"," ",t)
    return " ".join(html.unescape(t).split())

def extract(body):
    raw=decode(body); plain=textify(raw); low=plain.lower()
    terms=tuple(t for t in TERMS if t.lower() in low)
    hrefs=[]
    for raw_h in re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',raw):
        h=html.unescape(raw_h).strip()
        absolute=urllib.parse.urljoin(ORIGINAL,h)
        dl=urllib.parse.unquote_plus(absolute).lower()
        if any(ext in dl for ext in PAYLOAD_EXTS) or any(x in dl for x in ("download","down","update","upgrade","patch","setup","client","stoneage","sa")):
            hrefs.append((h,absolute))
    excerpts=[]
    for t in terms:
        i=low.find(t.lower())
        if i>=0:excerpts.append(plain[max(0,i-300):i+800])
    return terms,tuple(dict.fromkeys(hrefs)),tuple(dict.fromkeys(excerpts))

def main():
    print("StoneAge Waei pre-2.5 upgrade.asp preserved-capture replay — R1")
    print("SCOPE|single-Availability-confirmed-capture|2001-12-04|text+href-only|no-payload")
    print(f"TARGET|timestamp={TIMESTAMP}|original={ORIGINAL}")
    errors=[]
    for mode,u in urls():
        try:
            st,final,body=fetch(u)
            terms,hrefs,excerpts=extract(body)
            print(f"REPLAY|mode={mode}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|terms={clean(','.join(terms))}|hrefs={len(hrefs)}|final={clean(final)}")
            for ex in excerpts[:20]:print(f"EXCERPT|mode={mode}|text={clean(ex)}")
            strong=0
            for href,absolute in hrefs:
                low=urllib.parse.unquote_plus(absolute).lower()
                is_strong=any(ext in low for ext in PAYLOAD_EXTS) or any(x in low for x in ("setup","client","update","upgrade","patch"))
                strong+=int(is_strong)
                print(f"HREF|mode={mode}|strong={int(is_strong)}|href={clean(href)}|absolute={clean(absolute)}")
            print(f"COUNT|candidate_hrefs|{len(hrefs)}")
            print(f"COUNT|strong_hrefs|{strong}")
            print("RESOLUTION|PRE25_UPGRADE_CAPTURE_RECOVERED|classify download targets and compare to 2002 rollout topology")
            return
        except Exception as exc:
            errors.append((mode,type(exc).__name__,str(exc)))
    for mode,kind,msg in errors:print(f"ERROR|mode={clean(mode)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    print("RESOLUTION|PRE25_UPGRADE_CAPTURE_REPLAY_FAILED|retain Availability metadata and try alternate archive replay path")

if __name__=="__main__":main()
