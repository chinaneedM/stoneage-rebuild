#!/usr/bin/env python3
"""Inspect DiscMaster item 41879 after the StoneAge 2.0 probe found STONEAGE2.

Metadata/HTML directory topology only. No file payloads are downloaded.
"""
from __future__ import annotations
import hashlib,html,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
ITEM="41879"
BASE="https://discmaster.textfiles.com"
QUERIES=("STONEAGE2","stoneage","stoneage2.0setup.exe","stoneage.exe","sa.exe","setup.exe","install.exe","readme")
BROWSE=(f"{BASE}/browse/{ITEM}",f"{BASE}/browse/{ITEM}/STONEAGE2")

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=40,max_bytes=5*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/html,text/plain,*/*;q=0.5","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        return int(getattr(r,"status",r.getcode())),r.geturl(),dict(r.headers.items()),b

def search_url(q):
    p=[("q",q),("qfields","name"),("mode","deep"),("itemid",ITEM),("limit","500"),("outputAs","json"),("showItemName","showItemName")]
    return BASE+"/search?"+urllib.parse.urlencode(p)

def rows(node):
    out=[]
    def walk(x):
        if isinstance(x,dict):
            if ("itemid" in x or "itemName" in x) and ("fileid" in x or "filename" in x or "name" in x):
                out.append(x)
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(node)
    uniq={}
    for r in out:
        path=str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")
        uniq[(str(r.get("itemid") or ""),path,str(r.get("b3sum") or ""))]=r
    return tuple(uniq.values())

def path_of(r):
    return str(r.get("fileid") or r.get("path") or r.get("filename") or r.get("name") or "")

def main():
    print("StoneAge 2.0 DiscMaster item 41879 topology — R1")
    print("SCOPE|DiscMaster item-local search + browse HTML|metadata-only|no-payload")
    print("TARGET|itemid=41879|itemName=350 PC Games (CD-ROM)|discovered_path=STONEAGE2")
    errors=[]; seen={}
    for q in QUERIES:
        try:
            st,final,h,b=fetch(search_url(q))
            obj=json.loads(b.decode("utf-8")); rr=rows(obj)
            print(f"QUERY|q={clean(q)}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}")
            for r in rr:
                p=path_of(r); seen[(str(r.get("itemid") or ""),p)]=r
                print(f"ROW|q={clean(q)}|itemid={clean(r.get('itemid'))}|itemName={clean(r.get('itemName'))}|path={clean(p)}|size={clean(r.get('size'))}|ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}")
        except Exception as e:
            errors.append(("query:"+q,type(e).__name__,str(e)))
    for u in BROWSE:
        try:
            st,final,h,b=fetch(u,max_bytes=3*1024*1024)
            text=b.decode("utf-8","replace")
            print(f"BROWSE|url={clean(u)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            vals=[]
            for href in re.findall(r'(?is)href\s*=\s*["\']([^"\']+)["\']',text):
                href=html.unescape(href)
                full=urllib.parse.urljoin(final,href)
                low=urllib.parse.unquote_plus(full).lower()
                if any(k in low for k in ("stoneage2","stoneage","setup","install","readme","sa.exe")):
                    vals.append(full)
            for x in dict.fromkeys(vals):
                print(f"BROWSE_LINK|url={clean(x)}")
            for line in re.split(r'[\r\n]+',text):
                low=urllib.parse.unquote_plus(line).lower()
                if any(k in low for k in ("stoneage2","stoneage2.0setup","stoneage.exe","sa.exe")):
                    print(f"BROWSE_TEXT|text={clean(re.sub(r'<[^>]+>',' ',line),1800)}")
        except Exception as e:
            errors.append(("browse:"+u,type(e).__name__,str(e)))
    relevant=[]
    for r in seen.values():
        p=path_of(r).replace("\\","/"); low=p.lower()
        if "stoneage2" in low or ("stoneage" in low and any(x in low for x in ("setup","install",".exe","readme"))):
            relevant.append(r)
    print(f"COUNT|unique_rows|{len(seen)}")
    print(f"COUNT|relevant_rows|{len(relevant)}")
    for s,k,m in errors: print(f"ERROR|scope={clean(s)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|errors|{len(errors)}")
    if any("stoneage2.0setup.exe" in path_of(r).lower() for r in relevant):
        print("RESOLUTION|EXACT_CLIENT_FILENAME_IN_ITEM|inspect carrier provenance before any payload recovery")
    elif relevant:
        print("RESOLUTION|STONEAGE2_ITEM_NEIGHBORHOOD_FOUND|classify directory contents/version identity before promotion")
    else:
        print("RESOLUTION|STONEAGE2_DIRECTORY_ONLY_OR_FALSE_POSITIVE|item does not expose a client-identifying neighbor on tested metadata surfaces")
    print("EVIDENCE_BOUNDARY|DiscMaster item metadata/directory HTML is carrier-discovery evidence only; no file is accepted as the 2001 Mainland client without exact identity and provenance.")

if __name__=="__main__":
    main()
