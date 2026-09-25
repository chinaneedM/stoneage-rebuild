#!/usr/bin/env python3
"""Probe Sina download CGI host aliases for the 2001-11-27 StoneAge full-map package.

The 2000 target was recovered because Wayback preserved the same CGI on
games.sina.com.cn even though the surviving page linked games1.sina.com.cn.
This applies the proven alias method to aid=43172 / Estoneage2.0map_1127.exe.
No binary payload is downloaded.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
AVAIL="https://archive.org/wayback/available"
HOSTS=("games.sina.com.cn","games1.sina.com.cn")
PATH="/cgi-bin/games/downgames/download.pl"
TARGET_AID="43172"
TARGET_FILENAME="Estoneage2.0map_1127.exe"
WINDOWS=(("2001","20010101","20011231"),("2002","20020101","20021231"),("2003","20030101","20031231"))

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=60,max_bytes=5*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def cdx_url(base,start,end):
    p=[("url",base),("matchType","prefix"),("output","json"),
       ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
       ("from",start),("to",end),("limit","10000")]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def params(url):
    try:return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(str(url)).query,keep_blank_values=True))
    except Exception:return {}

def relevant(row):
    p=params(row.get("original") or "")
    return str(p.get("aid") or "")==TARGET_AID or str(p.get("filename") or "").lower()==TARGET_FILENAME.lower()

def replay_url(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def decode_html(body):
    for enc in ("gb18030","utf-8","latin1"):
        try:return body.decode(enc)
        except UnicodeDecodeError:pass
    return body.decode("latin1","replace")

def extract_route_values(body,base):
    text=decode_html(body);vals=[]
    pats=(
      r'(?is)href\s*=\s*["\']([^"\']+)["\']',
      r'(?is)src\s*=\s*["\']([^"\']+)["\']',
      r'(?is)action\s*=\s*["\']([^"\']+)["\']',
      r'(?is)value\s*=\s*["\']([^"\']+)["\']',
      r'(?i)(?:https?|ftp)://[^\s"\'<>]+',
    )
    for pat in pats:vals.extend(re.findall(pat,text))
    out=[]
    for raw in vals:
        raw=html.unescape(str(raw)).strip()
        if not raw:continue
        u=urllib.parse.urljoin(base,raw)
        low=urllib.parse.unquote_plus(u).lower()
        if TARGET_FILENAME.lower() in low or any(ext in low for ext in (".zip",".exe",".rar",".cab")) or any(k in low for k in ("download","down/","ftp","map")):
            out.append(u)
    return tuple(dict.fromkeys(out))

def relevant_text_lines(body):
    text=decode_html(body);out=[]
    for line in re.split(r'[\r\n]+',text):
        s=" ".join(line.split());low=urllib.parse.unquote_plus(s).lower()
        if TARGET_FILENAME.lower() in low or any(k in low for k in ("download","ftp","location","window.","document.","href","form")):
            out.append(s[:1800])
    return tuple(dict.fromkeys(out))[:60]

def main():
    print("StoneAge 2001 Sina download-host alias probe — R1")
    print("SCOPE|games + games1 download.pl aliases|Wayback metadata + small HTML replay|no-payload")
    print(f"TARGET|aid={TARGET_AID}|filename={TARGET_FILENAME}")
    errors=[];hits=[]
    for host in HOSTS:
        base=f"http://{host}{PATH}"
        for label,start,end in WINDOWS:
            try:
                st,final,h,b=fetch(cdx_url(base,start,end),timeout=65)
                rows=parse_cdx(b);rr=[r for r in rows if relevant(r)]
                maprows=[r for r in rows if str(params(r.get("original") or "").get("col") or "").lower()=="map"]
                print(f"CDX|host={host}|window={label}|status={st}|rows={len(rows)}|map_rows={len(maprows)}|relevant={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
                for r in rr:
                    hits.append((host,r))
                    print(f"HIT|host={host}|timestamp={clean(r.get('timestamp'))}|original={clean(r.get('original'))}|statuscode={clean(r.get('statuscode'))}|mimetype={clean(r.get('mimetype'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
            except Exception as e:errors.append((f"cdx:{host}:{label}",type(e).__name__,str(e)))
    uniq={}
    for host,r in hits:
        uniq[(str(r.get("timestamp","")),str(r.get("original","")))]=(host,r)
    print(f"COUNT|relevant_unique|{len(uniq)}")
    replayed=0
    for host,r in uniq.values():
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        if not ts or not orig:continue
        try:
            st,final,h,b=fetch(replay_url(ts,orig),timeout=50,max_bytes=384*1024)
            replayed+=1;vals=extract_route_values(b,orig);lines=relevant_text_lines(b)
            print(f"REPLAY|host={host}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|route_values={len(vals)}|relevant_lines={len(lines)}")
            for u in vals:print(f"ROUTE_VALUE|host={host}|timestamp={ts}|url={clean(u)}")
            for line in lines:print(f"BODY_LINE|host={host}|timestamp={ts}|text={clean(line,1800)}")
        except Exception as e:errors.append((f"replay:{host}:{ts}",type(e).__name__,str(e)))
    print(f"COUNT|replayed_hits|{replayed}")
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if replayed:
        print("RESOLUTION|HOST_ALIAS_CGI_REPLAYED|classify recovered direct routes and probe exact archive objects")
    elif uniq:
        print("RESOLUTION|HOST_ALIAS_ROW_FOUND_REPLAY_FAILED|retain exact row and retry alternate replay modes")
    else:
        print("RESOLUTION|NO_2001_TARGET_ROW_ON_HOST_ALIASES|move to contributor-domain and independent mirror routes")
    print("EVIDENCE_BOUNDARY|host-alias CGI evidence can establish a historical delivery URL; package contents still require recovered exact bytes.")

if __name__=="__main__":
    main()
