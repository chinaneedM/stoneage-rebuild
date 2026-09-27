#!/usr/bin/env python3
"""Recover the 2002 Sina col=updatex direct-server timeline.

The StoneAge 4.0 target was published 2002-11-08. A preserved 2002-11-16
updatex record resolves to 202.106.185.223/updatex_1024/. This probe expands
only the same Sina CGI/category through calendar 2002, replays the bounded set
of filename-bearing updatex captures, and records each direct file URL. It is
designed to determine whether the category base existed before/around the
target date. No linked binary is fetched.
"""
from __future__ import annotations
import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
CGI="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl"
TARGET_DATE="20021108"
TARGET_AID=61620
TARGET_FILE="shiqi4updatex_02_11_08.zip"
MAX_REPLAYS=40
URLISH=re.compile(
    r'''(?is)(?:href|src|action)\s*=\s*["']([^"']+)["']'''
    r'''|(?:window\.open|location(?:\.href)?\s*=|window\.location\s*=)\s*\(?\s*["']([^"']+)["']'''
)
ABS=re.compile(r'''(?i)(?:https?|ftp)://[^\s"'<>]+''')


def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]


def fetch(url,timeout=40,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.4","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes:raise ValueError(f"response-too-large:{len(b)}")
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b


def cdx_url(start,end):
    p=[
      ("url",CGI),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length"),
      ("from",start),("to",end),("limit","20000"),("filter","statuscode:200"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)


def rows(body):
    obj=json.loads(body.decode("utf-8"))
    if not isinstance(obj,list) or len(obj)<2:return ()
    head=obj[0]
    return tuple(dict(zip(head,r)) for r in obj[1:] if isinstance(r,list))


def qparams(url):
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query,keep_blank_values=True))


def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"


def decode(b):
    for enc in ("gb18030","utf-8","big5","latin1"):
        try:return b.decode(enc)
        except UnicodeDecodeError:pass
    return b.decode("latin1","replace")


def refs(text,base):
    out=[]
    for m in URLISH.finditer(text):
        raw=(m.group(1) or m.group(2) or "").strip()
        if raw and not raw.startswith(("javascript:","mailto:","#")):
            out.append(urllib.parse.urljoin(base,html.unescape(raw)))
    for m in ABS.finditer(text):
        out.append(html.unescape(m.group(0)).rstrip("),.;"))
    return tuple(dict.fromkeys(out))


def filename_refs(text,base,filename):
    needle=filename.lower()
    return tuple(u for u in refs(text,base) if needle and needle in urllib.parse.unquote_plus(u).lower())


def main():
    print("StoneAge Sina 2002 updatex route timeline — R1")
    print("SCOPE|calendar-2002 download.pl|col=updatex only|archived HTML routing|no-linked-payload")
    print(f"TARGET|date={TARGET_DATE}|aid={TARGET_AID}|filename={TARGET_FILE}")
    errors=[]; all_rows=[]
    for label,start,end in (
        ("h1","20020101","20020630"),
        ("q3","20020701","20020930"),
        ("q4","20021001","20021231"),
    ):
        try:
            st,final,h,b=fetch(cdx_url(start,end),timeout=60)
            rr=rows(b);all_rows.extend(rr)
            print(f"CDX|label={label}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))

    update=[]
    for r in all_rows:
        orig=str(r.get("original") or "")
        qp=qparams(orig)
        if str(qp.get("col") or "").lower()!="updatex":continue
        fn=str(qp.get("filename") or "")
        if not fn:continue
        aid=str(qp.get("aid") or "")
        update.append((str(r.get("timestamp") or ""),aid,fn,orig,r))
    update.sort()
    print(f"COUNT|updatex_filename_rows|{len(update)}")
    for ts,aid,fn,orig,r in update:
        print(f"UPDATE_ROW|timestamp={ts}|aid={clean(aid)}|filename={clean(fn)}|original={clean(orig)}")

    mappings=[]
    seen=set()
    for ts,aid,fn,orig,r in update:
        key=(ts,orig)
        if key in seen:continue
        seen.add(key)
        if len(seen)>MAX_REPLAYS:break
        try:
            st,final,h,b=fetch(replay(ts,orig),timeout=24,max_bytes=128*1024)
            txt=decode(b);fr=filename_refs(txt,orig,fn)
            print(f"REPLAY|timestamp={ts}|aid={clean(aid)}|filename={clean(fn)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|filename_refs={len(fr)}")
            for u in fr:
                p=urllib.parse.urlsplit(u)
                d=p.path.rsplit("/",1)[0]+"/" if "/" in p.path else "/"
                mappings.append((ts,aid,fn,p.scheme,p.hostname or "",d,u))
                print(f"DIRECT_FILE|timestamp={ts}|aid={clean(aid)}|filename={clean(fn)}|host={clean(p.hostname or '')}|dir={clean(d)}|url={clean(u)}")
        except Exception as e:
            errors.append((f"replay:{ts}:{aid}:{fn}",type(e).__name__,str(e)))

    bases={}
    before=[];around=[];after=[]
    for ts,aid,fn,scheme,host,d,u in mappings:
        base=f"{scheme}://{host}{d}"
        bases[base]=bases.get(base,0)+1
        day=ts[:8]
        if day<TARGET_DATE:before.append((day,base,fn))
        elif day<= "20021116":around.append((day,base,fn))
        else:after.append((day,base,fn))
    for base,n in sorted(bases.items(),key=lambda kv:(-kv[1],kv[0])):
        print(f"BASE|count={n}|url={clean(base)}")
    for label,vals in (("before",before),("target_to_1116",around),("after",after)):
        print(f"WINDOW|label={label}|mapped_rows={len(vals)}")
        for day,base,fn in vals[:20]:
            print(f"WINDOW_ROW|label={label}|date={day}|base={clean(base)}|filename={clean(fn)}")

    target_base="http://202.106.185.223/updatex_1024/"
    before_same=[x for x in before if x[1].lower()==target_base.lower()]
    around_same=[x for x in around if x[1].lower()==target_base.lower()]
    print(f"COUNT|same_base_before_target|{len(before_same)}")
    print(f"COUNT|same_base_target_to_1116|{len(around_same)}")
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if before_same:
        print("RESOLUTION|UPDATE_X_BASE_PRECEDES_TARGET_DATE|target synthesis is temporally supported but still unobserved")
    elif around_same:
        print("RESOLUTION|UPDATE_X_BASE_CONFIRMED_WITHIN_EIGHT_DAYS_AFTER_TARGET|target synthesis remains plausible but pre-target directory state is open")
    elif mappings:
        print("RESOLUTION|UPDATE_X_TIMELINE_RECOVERED_DIFFERENT_BASES|do not assume 1024 base at target date")
    elif errors:
        print("RESOLUTION|UPDATE_X_TIMELINE_INCOMPLETE|retry failed same-category rows only")
    else:
        print("RESOLUTION|NO_UPDATE_X_DIRECT_TIMELINE|retain only the previously proven 2002-11-16 sample")
    print("EVIDENCE_BOUNDARY|A category base observed near the target date strengthens routing inference but does not prove the missing target URL existed or carried the advertised package.")


if __name__=="__main__":
    main()
