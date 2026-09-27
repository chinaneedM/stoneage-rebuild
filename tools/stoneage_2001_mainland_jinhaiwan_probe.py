#!/usr/bin/env python3
"""Probe public preservation metadata for the 2001 Mainland StoneAge launch carrier.

Searches exact historical publisher/operator/title combinations. Metadata only:
no optical or archive payload body is downloaded.
"""
from __future__ import annotations
import hashlib, json, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
IA="https://archive.org/advancedsearch.php"
IAMETA="https://archive.org/metadata/"
DISCM="https://discmaster.textfiles.com/search"
DISC_EXTS=(".iso",".bin",".cue",".img",".nrg",".mdf",".mds",".ccd",".sub",".toast")
ARCHIVE_EXTS=(".zip",".rar",".7z",".exe",".cab")

QUERIES=(
 ("jinhaiwan-full","石器时代 广西金海湾电子音像出版社"),
 ("jinhaiwan-short","石器时代 广西金海湾"),
 ("waei-jinhaiwan","石器时代 北京华义 广西金海湾"),
 ("stoneage-jinhaiwan","STONEAGE 广西金海湾"),
 ("mainland-title","石器时代网络游戏 广西金海湾"),
)

def clean(v,n=2200):
    s=" ".join(str(v or "").split())
    return s.replace("|","%7C")[:n]

def fetch_json(url,timeout=45):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8"))

def ia_url(q):
    p=[("q",f'"{q}"'),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("fl[]","year"),
       ("fl[]","description"),("fl[]","collection"),("fl[]","mediatype"),("rows","100"),
       ("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def discm_url(q):
    p=[("q",f'"{q}"'),("qfields","t"),("mode","deep"),("dedup","dedup"),("limit","200"),
       ("outputAs","json"),("showItemName","showItemName"),("tsMin","1999"),("tsMax","2003")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def ia_docs(v):
    return tuple(x for x in v.get("response",{}).get("docs",[]) if isinstance(x,dict))

def discm_rows(v):
    rows=[]
    def walk(n):
        if isinstance(n,dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n):
                rows.append(n)
            for c in n.values(): walk(c)
        elif isinstance(n,list):
            for c in n: walk(c)
    walk(v)
    out=[]; seen=set()
    for r in rows:
        k=(str(r.get("itemid","")),str(r.get("fileid","")),str(r.get("href","")))
        if k not in seen: seen.add(k); out.append(r)
    return tuple(out)

def strict(blob):
    low=str(blob or "").lower().replace(" ","")
    title=("石器时代" in low or "stoneage" in low)
    publisher=("广西金海湾" in low)
    return title and publisher

def interesting_files(meta):
    out=[]
    for row in meta.get("files",[]) if isinstance(meta,dict) else []:
        if not isinstance(row,dict): continue
        low=str(row.get("name") or "").lower()
        if low.endswith(DISC_EXTS+ARCHIVE_EXTS):
            out.append(row)
    return tuple(out)

def main():
    print("StoneAge 2001 Mainland Guangxi-Jinhaiwan carrier preservation probe — R1")
    print("SCOPE|exact-title+publisher/operator-identity|InternetArchive+DiscMaster|metadata-only|no-payload")
    ia_hits={}; dm_hits={}; errors=[]
    for label,q in QUERIES:
        try:
            u=ia_url(q); st,final,b,data=fetch_json(u); docs=ia_docs(data)
            hits=[]
            for row in docs:
                blob=" ".join(str(row.get(k) or "") for k in ("identifier","title","description","collection"))
                if strict(blob): hits.append(row)
            print(f"IA_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|items={len(docs)}|strict={len(hits)}|final={clean(final)}")
            for row in hits:
                ident=str(row.get("identifier") or "")
                ia_hits[ident]=row
                print(f"IA_HIT|label={label}|identifier={clean(ident)}|title={clean(row.get('title'))}|date={clean(row.get('date'))}|year={clean(row.get('year'))}|mediatype={clean(row.get('mediatype'))}|collection={clean(row.get('collection'))}")
        except Exception as e:
            errors.append((f"ia:{label}",type(e).__name__,str(e)))
        try:
            u=discm_url(q); st,final,b,data=fetch_json(u); rows=discm_rows(data)
            hits=[]
            for row in rows:
                blob=" ".join(str(row.get(k) or "") for k in ("itemName","fileid","filename","href","text","title"))
                if strict(blob): hits.append(row)
            print(f"DISCM_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|strict={len(hits)}|final={clean(final)}")
            for row in hits:
                key=(str(row.get("itemid","")),str(row.get("fileid","")))
                dm_hits[key]=row
                print(f"DISCM_HIT|label={label}|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}")
        except Exception as e:
            errors.append((f"discm:{label}",type(e).__name__,str(e)))

    file_hits=0
    for ident,row in sorted(ia_hits.items()):
        try:
            st,final,b,meta=fetch_json(IAMETA+urllib.parse.quote(ident,safe=""))
            files=interesting_files(meta)
            print(f"IA_META|identifier={clean(ident)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|interesting_files={len(files)}|final={clean(final)}")
            for fr in files[:300]:
                file_hits+=1
                print(f"IA_FILE|identifier={clean(ident)}|name={clean(fr.get('name'))}|size={clean(fr.get('size'))}|md5={clean(fr.get('md5'))}|sha1={clean(fr.get('sha1'))}|source={clean(fr.get('source'))}|format={clean(fr.get('format'))}")
        except Exception as e:
            errors.append((f"ia-meta:{ident}",type(e).__name__,str(e)))

    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|queries|{len(QUERIES)}")
    print(f"COUNT|strict_ia_items|{len(ia_hits)}")
    print(f"COUNT|strict_discm_hits|{len(dm_hits)}")
    print(f"COUNT|ia_interesting_files|{file_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if file_hits:
        print("RESOLUTION|PUBLIC_MEDIA_METADATA_FOUND|inspect exact carrier provenance before any payload recovery")
    elif ia_hits or dm_hits:
        print("RESOLUTION|STRICT_METADATA_FOUND|inspect candidate provenance and file availability next")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_STRICT_HIT|retry failed metadata surfaces only")
    else:
        print("RESOLUTION|NO_STRICT_PRESERVATION_HIT|tested exact public indexes expose no Guangxi-Jinhaiwan StoneAge carrier")
    print("EVIDENCE_BOUNDARY|zero indexed hit does not prove physical media absence; reopen from new ISBN/ISRC/catalogue/disc-image/file-tree token.")

if __name__=="__main__": main()
