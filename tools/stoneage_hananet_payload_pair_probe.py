#!/usr/bin/env python3
"""Probe exact Hananet StoneAge formal/trial payloads without downloading full binaries."""

from __future__ import annotations
import concurrent.futures
import hashlib
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
AVAIL="https://archive.org/wayback/available"
DATES=["20001004","20010210","20010430","20010814","20011231","20020601"]
KNOWN_TS=["20010814230641"]
TARGETS=[
 ("formal-sa-exe","http://stoneage.hananet.net/down/sa.exe","260 M"),
 ("formal-sa-exe-www","http://www.stoneage.hananet.net/down/sa.exe","260 M"),
 ("trial-sa-demo-exe","http://stoneage.hananet.net/down/sa_demo.exe","240 M"),
 ("trial-sa-demo-exe-www","http://www.stoneage.hananet.net/down/sa_demo.exe","240 M"),
]

def request(url,timeout=12,headers=None,limit=None):
    h={"User-Agent":UA,"Accept-Encoding":"identity"}
    if headers:h.update(headers)
    req=urllib.request.Request(url,headers=h)
    with urllib.request.urlopen(req,timeout=timeout) as r:
        data=r.read() if limit is None else r.read(limit)
        return data,str(getattr(r,"url",url)),str(getattr(r,"status","")),dict(r.headers)

def availability(url,date):
    q=urllib.parse.urlencode({"url":url,"timestamp":date})
    data,_,_,_=request(AVAIL+"?"+q,timeout=8)
    obj=json.loads(data.decode("utf-8","replace"))
    c=obj.get("archived_snapshots",{}).get("closest")
    if not isinstance(c,dict) or not c.get("available"):return None
    return str(c.get("timestamp","")),str(c.get("status","")),str(c.get("url",""))

def replay(ts,url):return f"https://web.archive.org/web/{ts}id_/{url}"

def safe(v,limit=800):
    v=" ".join(str(v).split())
    return "".join(ch for ch in v if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def prefix(ts,url):
    data,resolved,status,headers=request(replay(ts,url),timeout=15,headers={"Range":"bytes=0-63"},limit=64)
    return {
      "status":status,"resolved":resolved,"len":len(data),
      "magic":data[:16].hex(),"sha256":hashlib.sha256(data).hexdigest(),
      "type":headers.get("Content-Type",""),"length":headers.get("Content-Length",""),
      "range":headers.get("Content-Range","")
    }

def main():
    print("StoneAge Hananet formal/trial payload probe — R1")
    print("SCOPE|availability+64-byte-prefix-only|no-complete-binary-download")
    print("MAPPING|formal=sa.exe:260 M|trial=sa_demo.exe:240 M|source=Hananet STAD archived HTML comment block")

    jobs=[(label,url,size,date) for label,url,size in TARGETS for date in DATES]
    hits={}; errors=[]
    def one(job):
        label,url,size,date=job
        try:return ("ok",label,url,size,date,availability(url,date))
        except Exception as exc:return ("err",label,url,size,date,type(exc).__name__,str(exc))
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        for row in ex.map(one,jobs):
            if row[0]=="err":
                _,label,url,size,date,kind,msg=row
                errors.append(("availability",label,date,kind,msg,url))
            else:
                _,label,url,size,date,hit=row
                if hit:
                    ts,status,archived=hit
                    hits[(label,url,size,ts)]=(status,archived)

    print(f"COUNT|availability_queries|{len(jobs)}")
    print(f"COUNT|availability_errors|{len(errors)}")
    print(f"COUNT|unique_available_snapshots|{len(hits)}")
    for phase,label,marker,kind,msg,url in sorted(errors):
        print(f"ERROR|phase={phase}|target={safe(label)}|marker={safe(marker)}|kind={safe(kind)}|url={safe(url)}|message={safe(msg)}")
    for (label,url,size,ts),(status,archived) in sorted(hits.items()):
        print(f"SNAPSHOT|target={safe(label)}|size_label={safe(size)}|timestamp={ts}|status={safe(status)}|original={safe(url)}|archived={safe(archived)}")

    probes={(label,url,size,ts,"availability") for label,url,size,ts in hits}
    for label,url,size in TARGETS:
        for ts in KNOWN_TS:
            probes.add((label,url,size,ts,"known-stad"))

    ok=0
    for label,url,size,ts,source in sorted(probes):
        try:
            meta=prefix(ts,url)
        except Exception as exc:
            print(f"PREFIX_ERROR|target={safe(label)}|size_label={safe(size)}|timestamp={ts}|source={source}|kind={type(exc).__name__}|message={safe(exc)}")
            continue
        ok+=1
        print(
            f"PREFIX|target={safe(label)}|size_label={safe(size)}|timestamp={ts}|source={source}|"
            f"http_status={safe(meta['status'])}|content_type={safe(meta['type'])}|content_length={safe(meta['length'])}|"
            f"content_range={safe(meta['range'])}|prefix_len={meta['len']}|magic_hex={meta['magic']}|prefix_sha256={meta['sha256']}|resolved={safe(meta['resolved'])}"
        )
    print(f"COUNT|prefix_success|{ok}")

if __name__=="__main__":main()
