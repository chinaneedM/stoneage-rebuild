#!/usr/bin/env python3
"""Probe the photographed StoneAge 2.5 Wanfang-published disc identity.

Metadata-only preservation search. No proprietary payload is downloaded.
"""
from __future__ import annotations
import concurrent.futures, hashlib, json, re, time, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
DISCM="https://discmaster.textfiles.com/search"
IA="https://archive.org/advancedsearch.php"
IAMETA="https://archive.org/metadata/"
DISC_EXTS=(".iso",".bin",".cue",".img",".nrg",".mdf",".mds",".ccd",".sub",".toast",".isz")
ARCHIVE_EXTS=(".zip",".7z",".rar",".exe",".cab")

QUERIES=(
    "7-900096-07-8",
    "7900096078",
    "9787900096074",
    "永远的石器时代 2.5 精灵王传说",
    "万方数据电子出版社 石器时代2.5",
    "精灵王传说 万方数据电子出版社",
)

def clean(v,limit=1800):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch_json(url,timeout=45,attempts=3):
    last=None
    for attempt in range(attempts):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                b=r.read()
                return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8"))
        except Exception as e:
            last=e
            if attempt+1<attempts:
                time.sleep(2*(attempt+1))
    raise last

def norm(s):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+","",str(s or "").lower())

def discm_url(q):
    p=[("q",f'"{q}"'),("qfields","t"),("mode","deep"),("dedup","dedup"),
       ("limit","100"),("outputAs","json"),("showItemName","showItemName"),
       ("tsMin","1999"),("tsMax","2006")]
    return DISCM+"?"+urllib.parse.urlencode(p)

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

def ia_url(q):
    p=[("q",f'"{q}"'),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
       ("fl[]","year"),("fl[]","description"),("fl[]","collection"),
       ("rows","100"),("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def ia_docs(v):
    r=v.get("response",{}) if isinstance(v,dict) else {}
    d=r.get("docs",[]) if isinstance(r,dict) else []
    return tuple(x for x in d if isinstance(x,dict))

def strict_match(blob):
    nb=norm(blob)
    isbn = any(x in nb for x in (norm("7-900096-07-8"),norm("7900096078"),norm("9787900096074")))
    title = norm("精灵王传说") in nb and norm("石器时代") in nb
    publisher = norm("万方数据电子出版社") in nb
    return isbn or (title and publisher)

def interesting_files(meta):
    files=meta.get("files",[]) if isinstance(meta,dict) else []
    out=[]
    for row in files:
        if not isinstance(row,dict): continue
        name=str(row.get("name") or "")
        if name.lower().endswith(DISC_EXTS+ARCHIVE_EXTS):
            out.append(row)
    return tuple(out)

def one_query(q):
    out={"q":q,"errors":[]}
    try:
        u=discm_url(q); st,final,b,data=fetch_json(u)
        out["discm"]=(st,final,b,discm_rows(data))
    except Exception as e:
        out["errors"].append(("discm",type(e).__name__,str(e)))
    try:
        u=ia_url(q); st,final,b,data=fetch_json(u)
        out["ia"]=(st,final,b,ia_docs(data))
    except Exception as e:
        out["errors"].append(("ia",type(e).__name__,str(e)))
    return out

def main():
    print("StoneAge 2.5 Wanfang disc preservation probe — R1")
    print("SCOPE|photographed-disc-identity|DiscMaster+IA-metadata|no-payload")
    print("ANCHOR|title=永远的石器时代 2.5 精灵王传说|publisher=万方数据电子出版社|isbn=7-900096-07-8/Z.03|barcode=9787900096074")
    errors=[]; strict_d={}; strict_i={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        results=list(ex.map(one_query,QUERIES))
    for res in results:
        q=res["q"]
        for scope,kind,msg in res["errors"]:
            errors.append((f"{scope}:{q}",kind,msg))
        if "discm" in res:
            st,final,b,rows=res["discm"]
            strict=[]
            for row in rows:
                blob=" ".join(str(row.get(k) or "") for k in ("itemName","fileid","filename","href","text","title"))
                if strict_match(blob): strict.append(row)
            print(f"DISCM_QUERY|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|strict={len(strict)}|final={clean(final)}")
            if q=="7-900096-07-8":
                for row in rows:
                    print("DISCM_RAW_LEAD|"+"|".join(f"{k}={clean(row.get(k))}" for k in ("itemid","itemName","fileid","filename","href","size","ts","b3sum","text","title")))
            for row in strict:
                key=(str(row.get("itemid","")),str(row.get("fileid","")))
                strict_d[key]=row
                print(f"DISCM_HIT|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}|b3sum={clean(row.get('b3sum'))}")
        if "ia" in res:
            st,final,b,docs=res["ia"]
            strict=[]
            for row in docs:
                blob=" ".join(str(row.get(k) or "") for k in ("identifier","title","description","date","year"))
                if strict_match(blob): strict.append(row)
            print(f"IA_QUERY|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|items={len(docs)}|strict={len(strict)}|final={clean(final)}")
            for row in strict:
                ident=str(row.get("identifier") or "")
                strict_i[ident]=row
                print(f"IA_HIT|identifier={clean(ident)}|title={clean(row.get('title'))}|date={clean(row.get('date'))}|year={clean(row.get('year'))}|collection={clean(row.get('collection'))}")
    file_hits=0
    for ident,row in sorted(strict_i.items()):
        try:
            st,final,b,meta=fetch_json(IAMETA+urllib.parse.quote(ident,safe=""))
            files=interesting_files(meta)
            print(f"IA_META|identifier={clean(ident)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|interesting_files={len(files)}|final={clean(final)}")
            for fr in files[:200]:
                file_hits+=1
                print(f"IA_FILE|identifier={clean(ident)}|name={clean(fr.get('name'))}|size={clean(fr.get('size'))}|md5={clean(fr.get('md5'))}|sha1={clean(fr.get('sha1'))}")
        except Exception as e:
            errors.append((f"ia-meta:{ident}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|queries|{len(QUERIES)}")
    print(f"COUNT|strict_discm_hits|{len(strict_d)}")
    print(f"COUNT|strict_ia_items|{len(strict_i)}")
    print(f"COUNT|ia_interesting_files|{file_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if file_hits:
        print("RESOLUTION|PRESERVED_MEDIA_CANDIDATE_FOUND|verify disc identity and provenance before payload analysis")
    elif strict_d or strict_i:
        print("RESOLUTION|STRICT_METADATA_FOUND|inspect preservation object next")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_STRICT_HIT|retry failed exact queries only")
    else:
        print("RESOLUTION|NO_STRICT_PRESERVATION_HIT|tested exact identifier surface is bounded")
    print("EVIDENCE_BOUNDARY|the photographed disc is not assumed to be an official Beijing-Waei retail client; only byte recovery can establish contents.")

if __name__=="__main__":
    main()
