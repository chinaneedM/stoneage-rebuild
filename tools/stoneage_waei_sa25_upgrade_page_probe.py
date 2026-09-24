#!/usr/bin/env python3
"""Recover Beijing Waei's official StoneAge2 upgrade.asp page and download targets.

Three independently replayed Feb-2002 official pages link to
/ZHUANQU/stoneage2/tyro/upgrade.asp. This probe resolves that exact page across
its archived captures, extracts upgrade/client size text and all payload-like
hrefs, and records derived metadata only. It never downloads the payloads.
"""

from __future__ import annotations

import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
TARGETS=(
    "http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/upgrade.asp",
    "http://www.waei.com.cn/zhuanqu/stoneage2/tyro/upgrade.asp",
    "http://waei.com.cn/zhuanqu/stoneage2/tyro/upgrade.asp",
)
DATE_FROM="20020115"
DATE_TO="20020331"
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".001",".002",".vcd",".iso",".msi")
TEXT_TERMS=("石器时代2.5","石器2.5","精灵王传说","完整升级版","升级程序","575","580","8.25","下载","客户端")

def clean(v,limit=3000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b

def cdx_url(target):
    p=[("url",target),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length"),
       ("from",DATE_FROM),("to",DATE_TO),("filter","statuscode:200"),("collapse","digest"),("limit","100")]
    return CDX+"?"+urllib.parse.urlencode(p)

def cdx_all_status_url(target):
    p=[("url",target),("matchType","prefix"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length"),
       ("from","2002"),("to","2005"),("collapse","urlkey"),("limit","1000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def availability_url(target,date):
    return AVAIL+"?"+urllib.parse.urlencode({"url":target,"timestamp":date})

def parse_cdx(body):
    d=json.loads(body.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def decode(body):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try: return body.decode(enc)
        except Exception: pass
    return body.decode("utf-8","replace")

def textify(raw):
    t=re.sub(r"(?is)<script\b.*?</script>"," ",raw)
    t=re.sub(r"(?is)<style\b.*?</style>"," ",t)
    t=re.sub(r"(?is)<[^>]+>"," ",t)
    return " ".join(html.unescape(t).split())

def extract(body,base):
    raw=decode(body)
    plain=textify(raw)
    low=plain.lower()
    terms=tuple(x for x in TEXT_TERMS if x.lower() in low)
    hrefs=[]
    for h in re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',raw):
        h=html.unescape(h).strip()
        absu=urllib.parse.urljoin(base,h)
        dl=urllib.parse.unquote_plus(absu).lower()
        if any(ext in dl for ext in PAYLOAD_EXTS) or any(x in dl for x in ("download","down","update","upgrade","patch","setup","client","2.5","sa25")):
            hrefs.append((h,absu))
    excerpts=[]
    for term in terms:
        i=low.find(term.lower())
        if i>=0: excerpts.append(plain[max(0,i-250):i+650])
    return terms,tuple(dict.fromkeys(hrefs)),tuple(dict.fromkeys(excerpts))

def replay_urls(ts,orig):
    return (
        ("id",f"https://web.archive.org/web/{ts}id_/{orig}"),
        ("if",f"https://web.archive.org/web/{ts}if_/{orig}"),
        ("plain",f"https://web.archive.org/web/{ts}/{orig}"),
    )

def main():
    print("StoneAge Beijing-Waei official 2.5 upgrade-page probe — R1")
    print("SCOPE|exact-official-upgrade.asp|2002-Q1|Wayback-captures+page-replay|derived-text+href-only|no-payload")
    errors=[]; captures={}
    for target in TARGETS:
        try:
            u=cdx_url(target); st,final,body=fetch(u)
            rows=parse_cdx(body)
            print(f"CDX|target={clean(target)}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}")
            for row in rows:
                key=(str(row.get("timestamp") or ""),str(row.get("original") or target),str(row.get("digest") or ""))
                captures[key]=row
                print(f"CAPTURE|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|digest={clean(row.get('digest'))}|length={clean(row.get('length'))}|mimetype={clean(row.get('mimetype'))}")
        except Exception as exc:
            errors.append((f"cdx:{target}",type(exc).__name__,str(exc)))

    for target in TARGETS:
        try:
            u=cdx_all_status_url(target); st,final,body=fetch(u,timeout=45)
            rows=parse_cdx(body)
            print(f"ALL_STATUS_CDX|target={clean(target)}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|rows={len(rows)}|final={clean(final)}")
            for row in rows:
                key=(str(row.get("timestamp") or ""),str(row.get("original") or target),str(row.get("digest") or ""))
                captures[key]=row
                print(f"ALL_STATUS_CAPTURE|timestamp={clean(row.get('timestamp'))}|original={clean(row.get('original'))}|statuscode={clean(row.get('statuscode'))}|digest={clean(row.get('digest'))}|length={clean(row.get('length'))}|mimetype={clean(row.get('mimetype'))}")
        except Exception as exc:
            errors.append((f"all-status-cdx:{target}",type(exc).__name__,str(exc)))

    availability_hits={}
    for target in TARGETS:
        for date in ("20020201","20020204","20020215","20020301","20030101"):
            try:
                u=availability_url(target,date); st,final,body=fetch(u,timeout=25)
                data=json.loads(body.decode("utf-8"))
                closest=data.get("archived_snapshots",{}).get("closest") if isinstance(data,dict) else None
                hit=isinstance(closest,dict) and bool(closest.get("available"))
                print(f"AVAIL|target={clean(target)}|date={date}|status={st}|hit={int(hit)}|timestamp={clean(closest.get('timestamp') if hit else '')}|capture={clean(closest.get('url') if hit else '')}|final={clean(final)}")
                if hit:
                    availability_hits[(str(closest.get("timestamp") or ""),str(closest.get("url") or ""))]=closest
            except Exception as exc:
                errors.append((f"availability:{target}:{date}",type(exc).__name__,str(exc)))

    # Availability can expose captures missing from CDX. Promote each unique hit
    # into the replay queue using the original archived URL encoded by Wayback.
    for (ts,capture_url),closest in sorted(availability_hits.items()):
        original=""
        m=re.search(r"/web/\\d{14}(?:[a-z_]+)?/(https?://.*)$",capture_url,re.I)
        if m:
            original=m.group(1)
        if not original:
            original=TARGETS[0]
        key=(ts,original,"availability")
        if key not in captures:
            captures[key]={
                "timestamp":ts,
                "original":original,
                "digest":"availability",
                "statuscode":str(closest.get("status") or ""),
                "mimetype":"",
                "length":"",
            }
        print(f"AVAIL_REPLAY_SEED|timestamp={clean(ts)}|original={clean(original)}|capture={clean(capture_url)}")

    all_hrefs={}
    success=0
    for (ts,orig,digest),row in sorted(captures.items()):
        for mode,u in replay_urls(ts,orig):
            try:
                st,final,body=fetch(u)
                terms,hrefs,excerpts=extract(body,orig)
                success+=1
                print(f"REPLAY|timestamp={ts}|mode={mode}|original={clean(orig)}|status={st}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|terms={clean(','.join(terms))}|hrefs={len(hrefs)}|final={clean(final)}")
                for ex in excerpts[:20]:
                    print(f"EXCERPT|timestamp={ts}|text={clean(ex)}")
                for href,absu in hrefs:
                    all_hrefs[absu]=(ts,orig,href)
                    print(f"HREF|timestamp={ts}|source={clean(orig)}|href={clean(href)}|absolute={clean(absu)}")
                break
            except Exception as exc:
                errors.append((f"replay:{ts}:{mode}",type(exc).__name__,str(exc)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    strong=[]
    for absu,(ts,src,href) in all_hrefs.items():
        low=urllib.parse.unquote_plus(absu).lower()
        if any(ext in low for ext in PAYLOAD_EXTS) or any(x in low for x in ("setup","client","update","upgrade","2.5","sa25")):
            strong.append((absu,ts,src,href))
    for absu,ts,src,href in strong:
        print(f"STRONG_HREF|timestamp={ts}|source={clean(src)}|href={clean(href)}|absolute={clean(absu)}")
    print(f"COUNT|captures|{len(captures)}")
    print(f"COUNT|availability_hits|{len(availability_hits)}")
    print(f"COUNT|successful_replays|{success}")
    print(f"COUNT|unique_candidate_hrefs|{len(all_hrefs)}")
    print(f"COUNT|strong_hrefs|{len(strong)}")
    print(f"COUNT|errors|{len(errors)}")
    if strong:
        print("RESOLUTION|OFFICIAL_25_PAYLOAD_TARGETS_FOUND|archive-classify exact payload URLs before transient recovery")
    elif success:
        print("RESOLUTION|UPGRADE_PAGE_RECOVERED_NO_PAYLOAD_HREF|inspect embedded forms/scripts and adjacent captures")
    else:
        print("RESOLUTION|UPGRADE_PAGE_UNRECOVERED|exact page archive surface unavailable")

if __name__=="__main__": main()
