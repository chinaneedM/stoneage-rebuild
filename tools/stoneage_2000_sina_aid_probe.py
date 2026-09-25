#!/usr/bin/env python3
"""Recover query-order/encoding variants for Sina aid=23223 (samap_1220.zip)."""
from __future__ import annotations
import hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
SOURCE="http://games.sina.com.cn/downgames/map/1220492.shtml"
PREFIX="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl"
AID="23223"; FILENAME="samap_1220.zip"
WINDOWS=(("2000-q4","20001001","20001231"),("2001-h1","20010101","20010630"),("2001-h2","20010701","20011231"),("2002","20020101","20021231"))

def clean(v,limit=5000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=45,max_bytes=3*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):return ()
    h=d[0];return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cgi_cdx(start,end):
    p=[("url",PREFIX),("matchType","prefix"),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),("from",start),("to",end),("limit","10000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def source_cdx():
    p=[("url",SOURCE),("matchType","exact"),("output","json"),("fl","timestamp,original,statuscode,mimetype,digest,length"),("from","2000"),("to","2004"),("limit","100")]
    return CDX+"?"+urllib.parse.urlencode(p)

def relevant(rows):
    out=[]
    for r in rows:
        u=urllib.parse.unquote_plus(str(r.get("original") or "")).lower()
        if f"aid={AID}" in u or FILENAME.lower() in u:out.append(r)
    return tuple(out)

def hrefs(b):
    t=b.decode("gb18030","replace")
    out=[]
    for x in re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',t):
        low=urllib.parse.unquote_plus(x).lower()
        if f"aid={AID}" in low or FILENAME.lower() in low:out.append(x.replace("&amp;","&"))
    return tuple(dict.fromkeys(out))

def replay(ts,u):return f"https://web.archive.org/web/{ts}id_/{u}"

def main():
    print("StoneAge 2000 Sina aid=23223 variant probe — R1")
    print("SCOPE|CGI-prefix-query-variants+historical-source-replay|metadata+small-html-only|no-payload")
    print(f"TARGET|aid={AID}|filename={FILENAME}|source={SOURCE}")
    errors=[];hits=[];source_rows=[]
    for label,start,end in WINDOWS:
        try:
            st,final,h,b=fetch(cgi_cdx(start,end),timeout=55)
            rows=parse_cdx(b);rr=relevant(rows);hits.extend(rr)
            print(f"CGI_CDX|window={label}|status={st}|rows={len(rows)}|relevant={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rr:
                print(f"CGI_HIT|window={label}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
        except Exception as e:errors.append((f"cgi:{label}",type(e).__name__,str(e)))
    try:
        st,final,h,b=fetch(source_cdx(),timeout=45);source_rows=list(parse_cdx(b))
        print(f"SOURCE_CDX|status={st}|rows={len(source_rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        for r in source_rows:
            ts=str(r.get("timestamp") or "");orig=str(r.get("original") or SOURCE)
            print(f"SOURCE_CAPTURE|timestamp={clean(ts)}|original={clean(orig)}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
            if ts:
                try:
                    st2,final2,h2,b2=fetch(replay(ts,orig),timeout=35,max_bytes=512*1024)
                    hs=hrefs(b2)
                    print(f"SOURCE_REPLAY|timestamp={ts}|status={st2}|bytes={len(b2)}|sha256={hashlib.sha256(b2).hexdigest()}|hrefs={len(hs)}")
                    for x in hs:print(f"SOURCE_HREF|timestamp={ts}|href={clean(x)}")
                except Exception as e:errors.append((f"replay:{ts}",type(e).__name__,str(e)))
    except Exception as e:errors.append(("source-cdx",type(e).__name__,str(e)))
    for date in ("20001220","20010101","20011220","20020101"):
        try:
            q=AVAIL+"?"+urllib.parse.urlencode({"url":SOURCE,"timestamp":date})
            st,final,h,b=fetch(q,timeout=25);d=json.loads(b.decode("utf-8"));c=(d.get("archived_snapshots") or {}).get("closest") or {}
            print(f"SOURCE_AVAIL|date={date}|status={st}|hit={int(bool(c.get('available')))}|timestamp={clean(c.get('timestamp'))}|capture={clean(c.get('url'))}")
        except Exception as e:errors.append((f"avail:{date}",type(e).__name__,str(e)))
    uniq={(str(r.get("timestamp","")),str(r.get("original",""))) for r in hits}
    print(f"COUNT|cgi_relevant_unique|{len(uniq)}")
    print(f"COUNT|source_captures|{len(source_rows)}")
    for scope,kind,msg in errors:print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if uniq:print("RESOLUTION|CGI_VARIANT_CAPTURE_FOUND|replay exact historical response and recover redirect/body target")
    elif source_rows:print("RESOLUTION|SOURCE_CAPTURE_ONLY|historical page exists but CGI payload route remains unindexed")
    else:print("RESOLUTION|NO_VARIANT_CAPTURE|retain exact aid/filename for independent mirror search")
    print("EVIDENCE_BOUNDARY|query-variant matches are route evidence only; payload identity requires recovered bytes.")

if __name__=="__main__":main()
