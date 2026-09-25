#!/usr/bin/env python3
"""Recover 2001 Sina download-server topology from archived col=map CGI neighbors.

The target aid=43172 itself is absent from Wayback's CGI index.  This probe
uses archived same-era/same-column neighbors, replaying only small HTML pages
and extracting external/download-looking links to infer server/path topology.
It then probes synthesized target paths in Wayback metadata only.
"""
from __future__ import annotations
import hashlib, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIX="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl"
TARGET_AID=43172
TARGET_FILENAME="Estoneage2.0map_1127.exe"
WINDOWS=(("2001-q4","20011001","20011231"),("2002-q1","20020101","20020331"))

def clean(v,limit=6000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]

def fetch(url,timeout=45,max_bytes=2*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def cdx_url(start,end):
    p=[
      ("url",PREFIX),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length"),
      ("from",start),("to",end),("filter","statuscode:200"),
      ("collapse","urlkey"),("limit","10000")
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def parse_cdx(b):
    d=json.loads(b.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list): return ()
    h=d[0]; return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def params(url):
    try: return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query,keep_blank_values=True))
    except Exception: return {}

def decode_html(b):
    for enc in ("gb18030","utf-8","latin1"):
        try:return b.decode(enc)
        except UnicodeDecodeError:pass
    return b.decode("latin1","replace")

def extract_links(body,base):
    text=decode_html(body)
    vals=[]
    vals += re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    vals += re.findall(r'(?is)src\s*=\s*["\']([^"\']+)["\']',text)
    vals += re.findall(r'(?is)url\s*=\s*([^"\'>\s]+)',text)
    vals += re.findall(r'(?i)(?:https?|ftp)://[^\s"\'<>]+',text)
    out=[]
    for x in vals:
        x=x.replace("&amp;","&").strip()
        u=urllib.parse.urljoin(base,x)
        low=urllib.parse.unquote_plus(u).lower()
        if (
          u.startswith(("http://","https://","ftp://")) and
          (
            any(ext in low for ext in (".exe",".zip",".rar",".cab")) or
            "download" in low or "down" in low or "ftp" in low or
            "games" in low
          )
        ):
            out.append(u)
    return tuple(dict.fromkeys(out))

def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def filename_path_templates(url,filename):
    p=urllib.parse.urlsplit(url)
    path=p.path
    leaf=path.rsplit("/",1)[-1]
    if "." not in leaf: return ()
    directory=path.rsplit("/",1)[0]+"/"
    vals=[
      urllib.parse.urlunsplit((p.scheme,p.netloc,directory+filename,"","")),
      urllib.parse.urlunsplit((p.scheme,p.netloc,directory+filename.lower(),"","")),
    ]
    return tuple(dict.fromkeys(vals))

def exact_cdx(url):
    p=[
      ("url",url),("matchType","exact"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from","2001"),("to","2005"),("limit","100")
    ]
    return CDX+"?"+urllib.parse.urlencode(p)

def main():
    print("StoneAge 2001 Sina map-download topology probe — R1")
    print("SCOPE|same-col-map-neighbors+small-CGI-replays+body-link-extraction+target-path-synthesis|no-payload")
    print(f"TARGET|aid={TARGET_AID}|filename={TARGET_FILENAME}")
    errors=[]; rows=[]
    for label,start,end in WINDOWS:
        try:
            st,final,h,b=fetch(cdx_url(start,end),timeout=55)
            part=parse_cdx(b); rows.extend(part)
            print(f"CDX_WINDOW|label={label}|status={st}|rows={len(part)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        except Exception as e:
            errors.append((f"cdx:{label}",type(e).__name__,str(e)))
    mapped=[]
    for r in rows:
        p=params(str(r.get("original") or ""))
        aid=p.get("aid","")
        if p.get("col","").lower()=="map" and aid.isdigit():
            mapped.append((abs(int(aid)-TARGET_AID),int(aid),r,p))
    mapped.sort(key=lambda x:(x[0],x[1],str(x[2].get("timestamp",""))))
    print(f"COUNT|all_rows|{len(rows)}")
    print(f"COUNT|col_map_rows|{len(mapped)}")
    unique_aids=[]
    seen=set()
    for d,aid,r,p in mapped:
        if aid in seen: continue
        seen.add(aid);unique_aids.append((d,aid,r,p))
    print(f"COUNT|col_map_unique_aids|{len(unique_aids)}")
    extracted=[]
    # Replay up to 40 nearest same-column records.
    for rank,(dist,aid,r,p) in enumerate(unique_aids[:40],1):
        ts=str(r.get("timestamp") or ""); orig=str(r.get("original") or "")
        print(
          f"NEIGHBOR|rank={rank}|distance={dist}|aid={aid}|timestamp={clean(ts)}|"
          f"filename={clean(p.get('filename'))}|size={clean(p.get('size'))}|original={clean(orig)}"
        )
        if not ts: continue
        try:
            st,final,h,b=fetch(replay(ts,orig),timeout=35,max_bytes=512*1024)
            links=extract_links(b,orig)
            print(f"REPLAY|aid={aid}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|links={len(links)}")
            for u in links:
                extracted.append((aid,p.get("filename",""),u))
                print(f"BODY_LINK|aid={aid}|source_filename={clean(p.get('filename'))}|url={clean(u)}")
        except Exception as e:
            errors.append((f"replay:{aid}:{ts}",type(e).__name__,str(e)))
    # Learn direct file directories from neighbor links and substitute target filename.
    synth=[]
    for aid,source_filename,u in extracted:
        low=u.lower()
        if source_filename and source_filename.lower() in urllib.parse.unquote_plus(low):
            synth.extend(filename_path_templates(u,TARGET_FILENAME))
        elif any(low.endswith(ext) for ext in (".exe",".zip",".rar",".cab")):
            synth.extend(filename_path_templates(u,TARGET_FILENAME))
    synth=tuple(dict.fromkeys(synth))
    print(f"COUNT|body_links|{len(extracted)}")
    print(f"COUNT|synthesized_target_urls|{len(synth)}")
    for i,u in enumerate(synth,1):
        print(f"SYNTH|index={i}|url={clean(u)}")
        try:
            st,final,h,b=fetch(exact_cdx(u),timeout=45)
            rr=parse_cdx(b)
            print(f"SYNTH_CDX|index={i}|status={st}|rows={len(rr)}|bytes={len(b)}")
            for x in rr:
                print(f"TARGET_CANDIDATE|timestamp={clean(x.get('timestamp'))}|original={clean(x.get('original'))}|statuscode={clean(x.get('statuscode'))}|mimetype={clean(x.get('mimetype'))}|digest={clean(x.get('digest'))}|length={clean(x.get('length'))}|redirect={clean(x.get('redirect'))}")
        except Exception as e:
            errors.append((f"synth:{i}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|errors|{len(errors)}")
    if synth:
        print("RESOLUTION|SINA_2001_DOWNLOAD_TOPOLOGY_RECOVERED|evaluate synthesized target CDX rows above")
    elif extracted:
        print("RESOLUTION|BODY_LINKS_RECOVERED_NO_FILENAME_TEMPLATE|inspect host/path patterns manually")
    else:
        print("RESOLUTION|NO_DOWNLOAD_BODY_TOPOLOGY|same-column CGI replays expose no usable file-server links")
    print("EVIDENCE_BOUNDARY|neighbor CGI body links establish historical download topology only; synthesized target paths are hypotheses until the exact filename is independently archived.")

if __name__=="__main__": main()
