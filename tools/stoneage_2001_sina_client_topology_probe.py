#!/usr/bin/env python3
"""Recover Sina 2001 client download topology for StoneAge 2.0.

Target:
  aid=41967
  filename=stoneage2.0setup.exe
  col=demo

Uses both historical Sina CGI aliases because the 2000 map recovery proved that
Wayback may index games.sina.com.cn while the surviving page links games1.
Only small archived CGI HTML and archive metadata are fetched; no client binary.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIXES=(
    "http://games.sina.com.cn/cgi-bin/games/downgames/download.pl",
    "http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl",
)
TARGET_AID=41967
TARGET_FILENAME="stoneage2.0setup.exe"
TARGET_COL="demo"

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=3*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def cdx_url(prefix,start="20010101",end="20020331"):
    p=[
      ("url",prefix),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from",start),("to",end),("filter","statuscode:200"),
      ("collapse","urlkey"),("limit","10000"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def exact_cdx(url):
    p=[
      ("url",url),("matchType","exact"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from","2001"),("to","2006"),("limit","100"),
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def params(url):
    try:return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(str(url)).query,keep_blank_values=True))
    except Exception:return {}

def decode_html(body):
    for enc in ("gb18030","utf-8","latin1"):
        try:return body.decode(enc)
        except UnicodeDecodeError:pass
    return body.decode("latin1","replace")

def extract_links(body,base):
    text=decode_html(body);vals=[]
    for pat in (
      r'(?is)href\s*=\s*["\']([^"\']+)["\']',
      r'(?is)src\s*=\s*["\']([^"\']+)["\']',
      r'(?is)action\s*=\s*["\']([^"\']+)["\']',
      r'(?i)(?:https?|ftp)://[^\s"\'<>]+',
    ):
        vals.extend(re.findall(pat,text))
    out=[]
    for raw in vals:
        raw=html.unescape(str(raw)).strip()
        if not raw:continue
        u=urllib.parse.urljoin(base,raw)
        low=urllib.parse.unquote_plus(u).lower()
        if TARGET_FILENAME.lower() in low or any(ext in low for ext in (".exe",".zip",".rar",".cab")) or any(k in low for k in ("download","down/","ftp")):
            out.append(u)
    return tuple(dict.fromkeys(out))

def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def filename_path_templates(url,filename):
    p=urllib.parse.urlsplit(url);path=p.path;leaf=path.rsplit("/",1)[-1]
    if "." not in leaf:return ()
    directory=path.rsplit("/",1)[0]+"/"
    return tuple(dict.fromkeys((
      urllib.parse.urlunsplit((p.scheme,p.netloc,directory+filename,"","")),
      urllib.parse.urlunsplit((p.scheme,p.netloc,directory+filename.lower(),"","")),
    )))

def main():
    print("StoneAge 2001 Sina client-download topology probe — R1")
    print("SCOPE|games+games1 col=demo neighbors + nearest CGI replay + target-path synthesis|no-client-payload")
    print(f"TARGET|aid={TARGET_AID}|filename={TARGET_FILENAME}|col={TARGET_COL}")
    errors=[];rows=[]
    for prefix in PREFIXES:
        host=urllib.parse.urlsplit(prefix).netloc
        try:
            st,final,h,b=fetch(cdx_url(prefix),timeout=60)
            part=parse_cdx(b);rows.extend(part)
            colrows=[r for r in part if str(params(r.get("original") or "").get("col") or "").lower()==TARGET_COL]
            print(f"CDX|host={host}|status={st}|rows={len(part)}|col_rows={len(colrows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        except Exception as e:errors.append((f"cdx:{host}",type(e).__name__,str(e)))
    mapped=[]
    for r in rows:
        p=params(r.get("original") or "");aid=str(p.get("aid") or "")
        if str(p.get("col") or "").lower()==TARGET_COL and aid.isdigit():
            mapped.append((abs(int(aid)-TARGET_AID),int(aid),r,p))
    mapped.sort(key=lambda x:(x[0],x[1],str(x[2].get("timestamp") or "")))
    uniq=[];seen=set()
    for item in mapped:
        if item[1] in seen:continue
        seen.add(item[1]);uniq.append(item)
    print(f"COUNT|col_rows|{len(mapped)}")
    print(f"COUNT|unique_aids|{len(uniq)}")
    extracted=[]
    for rank,(dist,aid,r,p) in enumerate(uniq[:10],1):
        ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
        print(f"NEIGHBOR|rank={rank}|distance={dist}|aid={aid}|timestamp={clean(ts)}|filename={clean(p.get('filename'))}|size={clean(p.get('size'))}|original={clean(orig)}")
        if not ts:continue
        try:
            st,final,h,b=fetch(replay(ts,orig),timeout=20,max_bytes=512*1024)
            links=extract_links(b,orig)
            print(f"REPLAY|aid={aid}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|links={len(links)}")
            for u in links:
                extracted.append((aid,str(p.get("filename") or ""),u))
                print(f"BODY_LINK|aid={aid}|source_filename={clean(p.get('filename'))}|url={clean(u)}")
        except Exception as e:errors.append((f"replay:{aid}:{ts}",type(e).__name__,str(e)))
    synth=[]
    for aid,src,u in extracted:
        low=urllib.parse.unquote_plus(u).lower()
        if src and src.lower() in low:
            synth.extend(filename_path_templates(u,TARGET_FILENAME))
        elif any(low.endswith(ext) for ext in (".exe",".zip",".rar",".cab")):
            synth.extend(filename_path_templates(u,TARGET_FILENAME))
    synth=tuple(dict.fromkeys(synth))
    print(f"COUNT|body_links|{len(extracted)}")
    print(f"COUNT|synthesized_target_urls|{len(synth)}")
    for i,u in enumerate(synth,1):
        print(f"SYNTH|index={i}|url={clean(u)}")
        try:
            st,final,h,b=fetch(exact_cdx(u),timeout=40)
            rr=parse_cdx(b)
            print(f"SYNTH_CDX|index={i}|status={st}|rows={len(rr)}|bytes={len(b)}")
            for x in rr:
                print(f"TARGET_CANDIDATE|index={i}|timestamp={clean(x.get('timestamp'))}|original={clean(x.get('original'))}|statuscode={clean(x.get('statuscode'))}|mimetype={clean(x.get('mimetype'))}|digest={clean(x.get('digest'))}|length={clean(x.get('length'))}|redirect={clean(x.get('redirect'))}")
        except Exception as e:errors.append((f"synth:{i}",type(e).__name__,str(e)))
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if synth:print("RESOLUTION|CLIENT_DOWNLOAD_TOPOLOGY_RECOVERED|evaluate synthesized exact target rows")
    elif extracted:print("RESOLUTION|CLIENT_NEIGHBOR_LINKS_NO_TARGET_TEMPLATE|inspect recovered host/path families")
    else:print("RESOLUTION|NO_CLIENT_DOWNLOAD_TOPOLOGY|exact client token remains mirror-search only")
    print("EVIDENCE_BOUNDARY|neighbor routes establish download topology only; target client identity requires an exact recovered installer.")

if __name__=="__main__":
    main()
