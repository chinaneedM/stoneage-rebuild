#!/usr/bin/env python3
"""Availability fallback for historical StoneAge 2.5 portal pages.

R1 CDX replay recovered Sina page snapshots but no client/download href; several
17173 CDX requests failed at the archive service. This R2 probe uses the lighter
Wayback Availability API at bounded dates, then replays only distinct captures.
No client payload is downloaded.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
AVAIL="https://archive.org/wayback/available"
SEEDS=(
    ("sina-http","http://games.sina.com.cn/newgames/0202/02057854.shtml"),
    ("sina-https","https://games.sina.com.cn/newgames/0202/02057854.shtml"),
    ("17173-subdomain","http://stoneage.17173.com/banben/sa25-up.htm"),
    ("17173-www","http://www.17173.com/stoneage/banben/sa25-up.htm"),
    ("17173-news","http://news.17173.com/z/stoneage/banben/sa25-up.htm"),
)
DATES=("20020120","20020201","20020205","20020301","20020601","20021201","20030115","20040115")
PAYLOAD_EXTS=(".exe",".zip",".rar",".cab",".msi",".001",".002",".iso")
URL_HINTS=("download","/down/","update","upgrade","patch","setup","client","sa25")
EXCLUDE=("comment.cgi","cgi-bin/comment","javascript:","mailto:")
TERMS=("指定网址","指定網址","完整升级版","完整升級版","升级程序","升級程序","575兆","580兆","8.25兆","石器时代2.5","石器2.5")


def clean(v,limit=2400):
    return " ".join(str(v or "").split()).replace("|","%7C")[:limit]


def fetch(url,timeout=15):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b


def availability(label,original,date):
    u=AVAIL+"?"+urllib.parse.urlencode({"url":original,"timestamp":date})
    try:
        st,final,b=fetch(u,timeout=12)
        obj=json.loads(b.decode("utf-8","replace"))
        c=(obj.get("archived_snapshots") or {}).get("closest") or {}
        return label,original,date,st,final,b,c,None
    except Exception as e:
        return label,original,date,None,u,b"",{},(type(e).__name__,str(e))


def candidate_href(absolute):
    low=urllib.parse.unquote_plus(absolute).lower()
    if any(x in low for x in EXCLUDE):
        return False
    if "waei.com.cn" in low:
        return True
    if any(low.split("?",1)[0].endswith(ext) for ext in PAYLOAD_EXTS):
        return True
    if any(h in low for h in URL_HINTS):
        return True
    return False


def extract(raw,base):
    hrefs=[]
    for raw_href in re.findall(r"""(?is)href\s*=\s*["']([^"']+)["']""",raw):
        href=html.unescape(raw_href).strip()
        absolute=urllib.parse.urljoin(base,href)
        if candidate_href(absolute):
            hrefs.append((href,absolute))
    hrefs=list(dict.fromkeys(hrefs))
    plain=re.sub(r"(?is)<script.*?</script>|<style.*?</style>"," ",raw)
    plain=html.unescape(re.sub(r"(?s)<[^>]+>"," ",plain))
    plain=" ".join(plain.split())
    low=plain.lower()
    contexts=[]
    for term in TERMS:
        i=low.find(term.lower())
        if i>=0:
            contexts.append(plain[max(0,i-180):i+520])
    return hrefs,list(dict.fromkeys(contexts))


def main():
    print("StoneAge 2.5 historical portal Availability fallback — R2")
    print("SCOPE|Sina+17173|bounded-date-Availability+capture-replay|no-client-payload")
    print("R1_CORRECTION|Sina comment.cgi was a false positive caused by article-title query text; it is excluded here.")
    captures={}
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futs=[ex.submit(availability,label,url,date) for label,url in SEEDS for date in DATES]
        rows=[f.result() for f in concurrent.futures.as_completed(futs)]

    for label,original,date,st,final,b,c,err in sorted(rows,key=lambda x:(x[0],x[2])):
        if err:
            errors.append((f"{label}:{date}",err[0],err[1]))
            print(f"AVAIL_ERROR|label={label}|date={date}|kind={clean(err[0])}|message={clean(err[1])}")
            continue
        available=bool(c.get("available"))
        ts=str(c.get("timestamp") or "")
        url=str(c.get("url") or "")
        status=str(c.get("status") or "")
        bounded=bool(ts and ts[:4] in ("2002","2003","2004"))
        print(
            f"AVAIL|label={label}|requested={date}|status={st}|bytes={len(b)}|"
            f"sha256={hashlib.sha256(b).hexdigest()}|available={int(available)}|"
            f"capture_ts={clean(ts)}|capture_status={clean(status)}|bounded={int(bounded)}|"
            f"capture_url={clean(url)}"
        )
        if available and status=="200" and bounded and ts and url:
            # Extract original URL from /web/<ts>/<original> when possible.
            m=re.search(r"/web/\d+(?:id_)?/(.+)$",url)
            cap_original=m.group(1) if m else original
            key=(ts,cap_original)
            captures[key]=(label,cap_original)

    print(f"COUNT|bounded_unique_captures|{len(captures)}")
    hrefs={}
    replay_errors=[]
    for (ts,original),(label,_) in sorted(captures.items())[:24]:
        replay=f"https://web.archive.org/web/{ts}id_/{original}"
        try:
            st,final,b=fetch(replay,timeout=15)
            raw=b.decode("utf-8","replace")
            hs,contexts=extract(raw,original)
            print(
                f"REPLAY|label={label}|timestamp={ts}|source={clean(original)}|status={st}|"
                f"bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|hrefs={len(hs)}|"
                f"contexts={len(contexts)}|final={clean(final)}"
            )
            for ctx in contexts[:10]:
                print(f"TEXT_CONTEXT|label={label}|timestamp={ts}|text={clean(ctx)}")
            for href,absolute in hs:
                hrefs[absolute]=(label,ts,original,href)
                print(
                    f"HREF|label={label}|timestamp={ts}|source={clean(original)}|"
                    f"href={clean(href)}|absolute={clean(absolute)}"
                )
        except Exception as e:
            replay_errors.append((f"{label}:{ts}",type(e).__name__,str(e)))
            print(f"REPLAY_ERROR|label={label}|timestamp={ts}|kind={type(e).__name__}|message={clean(e)}")

    for absolute,(label,ts,source,href) in sorted(hrefs.items()):
        print(
            f"TARGET_HREF|label={label}|timestamp={ts}|source={clean(source)}|"
            f"href={clean(href)}|absolute={clean(absolute)}"
        )
    for scope,kind,msg in errors+replay_errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|replay_errors|{len(replay_errors)}")
    print(f"COUNT|target_hrefs|{len(hrefs)}")
    if hrefs:
        print("RESOLUTION|HISTORICAL_DOWNLOAD_TARGET_FOUND|validate target identity and archive metadata next")
    elif captures:
        print("RESOLUTION|HISTORICAL_PORTAL_CAPTURES_NO_DOWNLOAD_TARGET|bounded captures replayed without qualifying download href")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_CAPTURE|Availability service incomplete; do not treat as archive-negative")
    else:
        print("RESOLUTION|NO_BOUNDED_PORTAL_CAPTURE|tested Availability dates expose no 2002-2004 target capture")


if __name__=="__main__":
    main()
