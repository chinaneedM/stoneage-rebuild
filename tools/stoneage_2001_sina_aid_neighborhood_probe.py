#!/usr/bin/env python3
"""Recover late-2001 Sina download topology from nearest archived aid records.

Targets:
- map aid 43172 / Estoneage2.0map_1127.exe
- client aid 41967 / stoneage2.0setup.exe

Unlike category-only probes, this scans every archived download.pl CGI row on
both Sina host aliases, ranks numeric aid neighbors irrespective of col, and
replays a small set of nearest records to learn contemporaneous file-server
hosts/directories. No target payload is downloaded.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
PREFIXES=(
    "http://games.sina.com.cn/cgi-bin/games/downgames/download.pl",
    "http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl",
)
TARGETS=(
    ("map",43172,"Estoneage2.0map_1127.exe"),
    ("client",41967,"stoneage2.0setup.exe"),
)

def clean(v,n=8000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=3*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),r.read(max_bytes)

def cdx_url(prefix):
    p=[
      ("url",prefix),("matchType","prefix"),("output","json"),
      ("fl","timestamp,original,statuscode,mimetype,digest,length,redirect"),
      ("from","2001"),("to","2002"),("filter","statuscode:200"),
      ("collapse","urlkey"),("limit","20000"),
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

def extract_direct_binary_links(body,base):
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
        if any(low.endswith(ext) for ext in (".exe",".zip",".rar",".cab",".gz",".tar")):
            out.append(u)
    return tuple(dict.fromkeys(out))

def replay(ts,orig):
    return f"https://web.archive.org/web/{ts}id_/{orig}"

def binary_filename(name):
    low=str(name or "").lower()
    return any(low.endswith(ext) for ext in (".exe",".zip",".rar",".cab",".gz",".tar"))

def rank_neighbors(rows,target_aid,limit=12):
    vals=[];seen=set()
    for r in rows:
        p=params(r.get("original") or "");aid=str(p.get("aid") or "")
        if not aid.isdigit() or not binary_filename(p.get("filename")):continue
        n=int(aid)
        key=(n,str(p.get("filename") or ""),str(p.get("col") or ""))
        if key in seen:continue
        seen.add(key)
        vals.append((abs(n-target_aid),n,r,p))
    vals.sort(key=lambda x:(x[0],x[1],str(x[2].get("timestamp") or "")))
    return tuple(vals[:limit])

def main():
    print("StoneAge 2001 Sina aid-neighborhood topology probe — R1")
    print("SCOPE|all download.pl columns + nearest numeric aid records with binary filenames + small CGI replay|no-target-payload")
    errors=[];rows=[]
    for prefix in PREFIXES:
        host=urllib.parse.urlsplit(prefix).netloc
        try:
            st,final,h,b=fetch(cdx_url(prefix),timeout=65)
            part=parse_cdx(b);rows.extend(part)
            numeric=sum(1 for r in part if str(params(r.get("original") or "").get("aid") or "").isdigit())
            print(f"CDX|host={host}|status={st}|rows={len(part)}|numeric_aid_rows={numeric}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
        except Exception as e:errors.append((f"cdx:{host}",type(e).__name__,str(e)))
    replay_keys=set()
    learned=[]
    for role,target_aid,target_filename in TARGETS:
        ranked=rank_neighbors(rows,target_aid,12)
        print(f"TARGET|role={role}|aid={target_aid}|filename={target_filename}|neighbors={len(ranked)}")
        for rank,(dist,aid,r,p) in enumerate(ranked,1):
            ts=str(r.get("timestamp") or "");orig=str(r.get("original") or "")
            print(f"NEIGHBOR|role={role}|rank={rank}|distance={dist}|aid={aid}|timestamp={clean(ts)}|col={clean(p.get('col'))}|filename={clean(p.get('filename'))}|size={clean(p.get('size'))}|original={clean(orig)}")
            key=(ts,orig)
            if not ts or not orig or key in replay_keys:continue
            replay_keys.add(key)
            try:
                st,final,h,b=fetch(replay(ts,orig),timeout=18,max_bytes=384*1024)
                links=extract_direct_binary_links(b,orig)
                print(f"REPLAY|role={role}|aid={aid}|timestamp={ts}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|binary_links={len(links)}")
                for u in links:
                    learned.append((role,aid,str(p.get("col") or ""),str(p.get("filename") or ""),u))
                    print(f"DIRECT_LINK|role={role}|aid={aid}|col={clean(p.get('col'))}|source_filename={clean(p.get('filename'))}|url={clean(u)}")
            except Exception as e:errors.append((f"replay:{role}:{aid}:{ts}",type(e).__name__,str(e)))
    hosts={}
    for role,aid,col,src,u in learned:
        pu=urllib.parse.urlsplit(u)
        key=(pu.scheme,pu.netloc,pu.path.rsplit("/",1)[0]+"/")
        hosts[key]=hosts.get(key,0)+1
    for (scheme,host,directory),count in sorted(hosts.items(),key=lambda kv:(-kv[1],kv[0])):
        print(f"TOPOLOGY|scheme={scheme}|host={host}|directory={clean(directory)}|observations={count}")
    print(f"COUNT|direct_links|{len(learned)}")
    print(f"COUNT|topology_directories|{len(hosts)}")
    for s,k,m in errors:print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if learned:print("RESOLUTION|AID_NEIGHBOR_TOPOLOGY_RECOVERED|use only date/column-compatible directories for bounded target hypotheses")
    else:print("RESOLUTION|NO_AID_NEIGHBOR_BINARY_LINKS|nearest archived CGI records did not expose direct binary routes")
    print("EVIDENCE_BOUNDARY|nearby aid records are topology evidence only; numeric proximity does not prove same server directory or target bytes.")

if __name__=="__main__":
    main()
