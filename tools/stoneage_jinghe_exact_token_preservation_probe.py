#!/usr/bin/env python3
"""Search preservation indexes for exact Jinghe/Yegame StoneAge artifact tokens.

New source-grounded tokens:
- EN0ZGKJ0002: StoneAge 1-CD retail product key
- EZ0JHSD0003: StoneAge WGS 620-point card key
- archived product-image hashes

Metadata/search only. No archived game or disc payload is downloaded.
"""
from __future__ import annotations
import hashlib,json,re,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
DM="https://discmaster.textfiles.com/search"
TOKENS=(
 ("client-code","EN0ZGKJ0002"),
 ("wgs-code","EZ0JHSD0003"),
 ("cover-md5","980e7d3336fa7557c166f2ff8ba3957c"),
 ("cover-sha1","95ae12136e77355bac09aee8d7490a29a073e969"),
)

def clean(v,n=5000):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def fetch_json(url,timeout=60,max_bytes=8*1024*1024):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,text/plain,*/*;q=0.2","Accept-Encoding":"identity"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(max_bytes+1)
        if len(b)>max_bytes: raise ValueError("response-too-large")
        return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8"))

def ia_url(token):
    p=[
      ("q",f'"{token}"'),
      ("fl[]","identifier"),("fl[]","title"),("fl[]","description"),("fl[]","date"),("fl[]","mediatype"),
      ("rows","100"),("page","1"),("output","json"),
    ]
    return IA+"?"+urllib.parse.urlencode(p)

def dm_url(token,qfields):
    p=[
      ("q",f'"{token}"'),("qfields",qfields),("mode","deep"),("dedup","dedup"),
      ("limit","200"),("outputAs","json"),("showItemName","showItemName"),
      ("tsMin","1999"),("tsMax","2010"),
    ]
    return DM+"?"+urllib.parse.urlencode(p)

def dm_rows(v):
    rows=[]
    def walk(n):
        if isinstance(n,dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n or "name" in n):
                rows.append(n)
            for c in n.values(): walk(c)
        elif isinstance(n,list):
            for c in n: walk(c)
    walk(v)
    out=[];seen=set()
    for r in rows:
        k=(str(r.get("itemid","")),str(r.get("fileid","")),str(r.get("href","")),str(r.get("filename","")))
        if k not in seen: seen.add(k);out.append(r)
    return tuple(out)

def blob(v):
    if isinstance(v,dict): return " ".join(str(x or "") for x in v.values()).lower()
    return str(v or "").lower()

def main():
    print("StoneAge Jinghe exact-token preservation-index probe — R1")
    print("SCOPE|Internet Archive advanced metadata search + DiscMaster name/full-text|exact source-grounded tokens|no payload")
    hits=0;errors=[]
    for label,token in TOKENS:
        try:
            st,final,b,data=fetch_json(ia_url(token),timeout=45)
            docs=((data.get("response") or {}).get("docs") or []) if isinstance(data,dict) else []
            strict=[d for d in docs if token.lower() in json.dumps(d,ensure_ascii=False).lower()]
            print(f"IA|label={label}|token={token}|status={st}|docs={len(docs)}|strict={len(strict)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for d in strict:
                hits+=1
                print(f"IA_HIT|label={label}|identifier={clean(d.get('identifier'))}|title={clean(d.get('title'))}|date={clean(d.get('date'))}|mediatype={clean(d.get('mediatype'))}|description={clean(d.get('description'),1600)}")
        except Exception as e:
            errors.append((label,"ia",type(e).__name__,str(e)))
            print(f"ERROR|label={label}|scope=ia|kind={type(e).__name__}|message={clean(e)}")
        for scope,qfields in (("name","name"),("text","t")):
            try:
                st,final,b,data=fetch_json(dm_url(token,qfields),timeout=60)
                rr=dm_rows(data)
                strict=[r for r in rr if token.lower() in blob(r)]
                print(f"DM|label={label}|scope={scope}|token={token}|status={st}|rows={len(rr)}|strict={len(strict)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
                for r in strict:
                    hits+=1
                    print(f"DM_HIT|label={label}|scope={scope}|itemid={clean(r.get('itemid'))}|itemName={clean(r.get('itemName'))}|fileid={clean(r.get('fileid'))}|filename={clean(r.get('filename') or r.get('name'))}|size={clean(r.get('size'))}|ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}")
            except Exception as e:
                errors.append((label,"dm-"+scope,type(e).__name__,str(e)))
                print(f"ERROR|label={label}|scope=dm-{scope}|kind={type(e).__name__}|message={clean(e)}")
    print(f"COUNT|tokens|{len(TOKENS)}")
    print(f"COUNT|surfaces_attempted|{len(TOKENS)*3}")
    print(f"COUNT|strict_hits|{hits}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|EXACT_TOKEN_PRESERVATION_HIT|authenticate candidate carrier/file tree before payload recovery")
    elif errors:
        print("RESOLUTION|PARTIAL_EXACT_TOKEN_SEARCH|retry only failed index surfaces")
    else:
        print("RESOLUTION|EXACT_TOKEN_ROUTE_BOUNDED|new catalog/hash tokens expose no indexed preserved carrier; return to independent test-CD/trial-client recovery")
    print("EVIDENCE_BOUNDARY|zero index hits cannot negate documented physical/online clients; no payload is downloaded.")

if __name__=="__main__": main()
