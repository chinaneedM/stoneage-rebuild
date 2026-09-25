#!/usr/bin/env python3
"""Recover direct download topology from Sina map records adjacent to aid=43172.

The live Sina page neighborhood around /map/11271899.shtml exposes four
contiguous sibling records (aid 43124/43127/43129/43130). This probe checks
Wayback for their exact CGI URLs on games1/games aliases, replays only small
archived HTML responses, extracts direct binary links, and tests target-filename
substitution in CDX metadata. No binary payload is downloaded.
"""
from __future__ import annotations
import hashlib, html, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
TARGET_FILENAME="Estoneage2.0map_1127.exe"
SIBLINGS=(
 ("43124","dflwaztekspride_1119.zip","59"),
 ("43127","dflwbootcamp1_1119.zip","66"),
 ("43129","dflwdangerzone1_1119.zip","72"),
 ("43130","dflwdesertterror_1119.zip","71"),
)

def clean(v,n=7000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=1024*1024):
    req=urllib.request.Request(url,headers={
        "User-Agent":UA,
        "Accept":"application/json,text/html,text/plain,*/*;q=0.5",
        "Accept-Encoding":"identity",
    })
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def parse_cdx(body):
    d=json.loads(body.decode("utf-8"))
    if not isinstance(d,list) or not d or not isinstance(d[0],list):
        return ()
    h=d[0]
    return tuple(dict(zip(h,row)) for row in d[1:] if isinstance(row,list))

def cdx_url(target,match="exact"):
    q=[
      ("url",target),("matchType",match),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from","2001"),("to","2004"),("limit","500")
    ]
    return CDX+"?"+urllib.parse.urlencode(q)

def cgi_prefix(host,aid):
    base=f"http://{host}/cgi-bin/games/downgames/download.pl"
    q=[
      ("url",base),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from","2001"),("to","2003"),("filter","statuscode:200"),("limit","10000")
    ]
    return CDX+"?"+urllib.parse.urlencode(q),aid

def row_matches(row,aid,filename):
    u=urllib.parse.unquote_plus(str(row.get("original") or "")).lower()
    return f"aid={aid}" in u or filename.lower() in u

def decode(body):
    for enc in ("gb18030","utf-8","latin1"):
        try:return body.decode(enc)
        except UnicodeDecodeError:pass
    return body.decode("latin1","replace")

def binary_links(body,base):
    text=decode(body)
    vals=[]
    vals+=re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text)
    vals+=re.findall(r'(?is)src\s*=\s*["\']([^"\']+)["\']',text)
    vals+=re.findall(r'(?i)(?:https?|ftp)://[^\s"\'<>]+',text)
    out=[]
    for raw in vals:
        u=urllib.parse.urljoin(base,html.unescape(str(raw)).strip())
        low=urllib.parse.unquote_plus(u).lower()
        if any(ext in low for ext in (".zip",".exe",".rar",".cab",".7z")):
            out.append(u)
    return tuple(dict.fromkeys(out))

def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def substitute_filename(url,source_filename,target_filename=TARGET_FILENAME):
    p=urllib.parse.urlsplit(url)
    path=p.path
    leaf=path.rsplit("/",1)[-1]
    if leaf.lower()!=source_filename.lower():
        return ""
    directory=path.rsplit("/",1)[0]+"/"
    return urllib.parse.urlunsplit((p.scheme,p.netloc,directory+target_filename,"",""))

def main():
    print("StoneAge 2001 Sina same-batch route probe — R1")
    print("SCOPE|adjacent map CGI CDX/replay + direct-binary extraction + target substitution|small-response-only|no-payload")
    print(f"TARGET|filename={TARGET_FILENAME}|aid=43172")
    errors=[];hits=[];direct=[];synth=[]
    for host in ("games1.sina.com.cn","games.sina.com.cn"):
        try:
            u,_=cgi_prefix(host,"")
            st,final,h,b=fetch(u,timeout=60,max_bytes=5*1024*1024)
            rows=parse_cdx(b)
            print(f"PREFIX|host={host}|status={st}|rows={len(rows)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        except Exception as e:
            errors.append((f"prefix:{host}",type(e).__name__,str(e))); rows=()
        for aid,filename,size in SIBLINGS:
            rr=[r for r in rows if row_matches(r,aid,filename)]
            print(f"SIBLING|host={host}|aid={aid}|filename={filename}|rows={len(rr)}")
            for r in rr:
                ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
                hits.append((host,aid,filename,ts,orig))
                print(f"ROW|host={host}|aid={aid}|timestamp={clean(ts)}|statuscode={clean(r.get('statuscode'))}|original={clean(orig)}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}")
                if not ts:continue
                try:
                    rst,rfinal,rh,rb=fetch(replay(ts,orig),timeout=35,max_bytes=512*1024)
                    links=binary_links(rb,orig)
                    print(f"REPLAY|host={host}|aid={aid}|timestamp={ts}|status={rst}|bytes={len(rb)}|sha256={hashlib.sha256(rb).hexdigest()}|binary_links={len(links)}")
                    for link in links:
                        direct.append((aid,filename,link))
                        print(f"DIRECT|aid={aid}|source_filename={filename}|url={clean(link)}")
                        su=substitute_filename(link,filename)
                        if su:synth.append(su)
                except Exception as e:
                    errors.append((f"replay:{host}:{aid}:{ts}",type(e).__name__,str(e)))
    synth=tuple(dict.fromkeys(synth))
    print(f"COUNT|sibling_rows|{len({(h,a,f,t,o) for h,a,f,t,o in hits})}")
    print(f"COUNT|direct_links|{len({(a,f,u) for a,f,u in direct})}")
    print(f"COUNT|synthesized_target_urls|{len(synth)}")
    for i,u in enumerate(synth,1):
        print(f"SYNTH|index={i}|url={clean(u)}")
        try:
            st,final,h,b=fetch(cdx_url(u),timeout=45)
            rr=parse_cdx(b)
            print(f"SYNTH_CDX|index={i}|status={st}|rows={len(rr)}|bytes={len(b)}")
            for r in rr:
                print(f"TARGET_ROW|index={i}|timestamp={clean(r.get('timestamp'))}|statuscode={clean(r.get('statuscode'))}|original={clean(r.get('original'))}|digest={clean(r.get('digest'))}|length={clean(r.get('length'))}|redirect={clean(r.get('redirect'))}")
        except Exception as e:
            errors.append((f"synth:{i}",type(e).__name__,str(e)))
    for s,k,m in errors[:200]:
        print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if synth:
        print("RESOLUTION|SAME_BATCH_DIRECT_TOPOLOGY_RECOVERED|evaluate synthesized exact target rows; sibling topology is not target provenance")
    elif direct:
        print("RESOLUTION|SIBLING_DIRECT_LINKS_WITHOUT_TEMPLATE|inspect sibling paths manually")
    elif hits:
        print("RESOLUTION|SIBLING_CGI_ROWS_NO_DIRECT_LINK|archived sibling CGI exists but replay exposes no usable binary URL")
    else:
        print("RESOLUTION|NO_SIBLING_CGI_CAPTURE|same-batch live tokens are known but not indexed on tested Wayback prefix")
    print("EVIDENCE_BOUNDARY|adjacent Sina records can establish late-2001 delivery topology only; target bytes require an exact archived row or recovered payload.")

if __name__=="__main__":
    main()
