#!/usr/bin/env python3
"""Probe exact 2002 StoneAge 2.5 physical/disc carrier identities.

Contemporaneous 17173/Sina records name Jan/Feb-2002 magazine/guide carriers
and the standalone game 《轰炸鸡》, while the 2.5 product page states that
specific Waei retail gift packs contain a 2.5 client CD. This probe searches
public preservation indexes by those exact carrier identities and inspects IA
file lists only for strict candidate items.
Metadata only; no disc/client payload is downloaded.
"""
from __future__ import annotations
import concurrent.futures, hashlib, json, re, urllib.parse, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
DISCM="https://discmaster.textfiles.com/search"
IA="https://archive.org/advancedsearch.php"
IAMETA="https://archive.org/metadata/"
DISC_EXTS=(".iso",".bin",".cue",".img",".nrg",".mdf",".mds",".ccd",".sub",".toast",".isz")
ARCHIVE_EXTS=(".zip",".7z",".rar",".exe",".cab")

TARGETS=(
 ("bombing-chicken-game",("轰炸鸡","轰炸鸡 华义","轰炸鸡 石器时代2.5","Chicken Shoot Waei","Chicken Shoot StoneAge"),"crosspromo"),
 ("newbie-pack",("石器时代2.5新手报到包","石器时代 2.5 新手报到包"),"product"),
 ("spring-pack",("石器时代2.5春满钱坤包","春满钱坤包","春满乾坤包"),"product"),
 ("longevity-pack",("石器时代2.5延年益兽包","延年益兽包"),"product"),
 ("computer-news-gameworld",("电脑报 游戏世界 2002年2月","电脑报 游戏世界"),"periodical"),
 ("game-king",("游戏王 2002年2月","游戏王 2002"),"periodical"),
 ("home-computer-world",("家庭电脑世界 2002年2月","家庭电脑世界 2002"),"periodical"),
 ("pc-free",("PC任我行 2002年2月","PC任我行 2002"),"periodical"),
 ("computer-fan-games",("电脑爱好者 玩游戏 2002年2月","电脑爱好者 玩游戏"),"periodical"),
 ("software-fashion",("软件时尚 2002年2月","软件时尚 2002"),"periodical"),
 ("crystal-sharp",("水晶宝合 锐 2002年2月","水晶宝盒 锐 2002年2月","水晶宝合 锐"),"periodical"),
 ("popular-games",("大众软件CD 大众游戏 2002年2月","大众游戏 2002"),"periodical"),
 ("chip-new-pc",("CHIP新电脑 2002年2月","CHIP 新电脑 2002"),"periodical"),
 ("online-club-gamebar",("网上俱乐部 游戏吧 2002年2月","网上俱乐部 游戏吧"),"periodical"),
 ("popular-pc-netbar",("大众电脑 网吧乐园 2002年2月","大众电脑光盘版 网吧乐园"),"periodical"),
 ("computer-aviation",("计算机与航空 2002年1月","计算机与航空 2002"),"periodical"),
 ("middle-school-computer",("中学生电脑 2002 攻略特刊","中学生电脑 2002"),"periodical"),
 ("tengtu-guide",("腾图 石器时代2.5","腾图 石器时代 2.5"),"guide"),
 ("saint-beer-guide",("圣比尔 石器时代2.5","圣比尔 石器时代 2.5"),"guide"),
 ("netfan-guide",("网迷 网络游戏介绍 石器时代","网迷 网络游戏介绍"),"guide"),
)

def clean(v,limit=1800):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]

def fetch_json(url,timeout=45):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read()
        return int(getattr(r,"status",r.getcode())),r.geturl(),b,json.loads(b.decode("utf-8"))

def discm_url(q):
    p=[("q",f'"{q}"'),("qfields","t"),("mode","deep"),("dedup","dedup"),
       ("limit","100"),("outputAs","json"),("showItemName","showItemName"),
       ("tsMin","2000"),("tsMax","2004")]
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
    query=f'"{q}"'
    p=[("q",query),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),
       ("fl[]","year"),("fl[]","description"),("fl[]","collection"),
       ("rows","100"),("page","1"),("output","json")]
    return IA+"?"+urllib.parse.urlencode(p)

def ia_docs(v):
    r=v.get("response",{}) if isinstance(v,dict) else {}
    d=r.get("docs",[]) if isinstance(r,dict) else []
    return tuple(x for x in d if isinstance(x,dict))

def norm(s):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+","",str(s or "").lower())

def target_tokens(q):
    n=norm(q)
    # Keep distinctive lexical chunks; generic date/version fragments alone do not qualify.
    chunks=[x for x in re.split(r"(2002|2月|1月|25)",n) if len(x)>=2]
    return tuple(chunks)

def strict_match(label,queries,kind,blob):
    nb=norm(blob)
    if kind=="crosspromo":
        # 《轰炸鸡》 is source-named as a 2.5 distribution carrier. Because the
        # base Chicken Shoot title also circulated internationally, require an
        # explicit Waei/StoneAge association before promoting an index row to a
        # strict StoneAge-carrier hit.
        if label=="bombing-chicken-game":
            chinese = norm("轰炸鸡") in nb
            english = norm("Chicken Shoot") in nb
            association = any(norm(x) in nb for x in ("华义","石器时代","StoneAge","Wayi","Waei"))
            return (chinese or english) and association
        return False
    if kind=="product":
        anchors={
          "newbie-pack":("新手报到包","石器时代"),
          "spring-pack":("春满钱坤包",),
          "longevity-pack":("延年益兽包",),
        }[label]
        return all(norm(a) in nb for a in anchors)
    # Periodical/guide: accept if at least one source-derived query has all distinctive chunks.
    for q in queries:
        toks=target_tokens(q)
        if toks and all(t in nb for t in toks):
            return True
    return False

def ia_metadata(identifier):
    return fetch_json(IAMETA+urllib.parse.quote(identifier,safe=""))

def interesting_files(meta):
    files=meta.get("files",[]) if isinstance(meta,dict) else []
    out=[]
    for row in files:
        if not isinstance(row,dict): continue
        name=str(row.get("name") or "")
        low=name.lower()
        if low.endswith(DISC_EXTS+ARCHIVE_EXTS):
            out.append(row)
    return tuple(out)

def one_target(entry):
    label,queries,kind=entry
    drows=[]; idocs=[]; errors=[]
    for q in queries:
        try:
            u=discm_url(q); st,final,b,data=fetch_json(u)
            rows=discm_rows(data)
            drows.append((q,st,final,b,rows))
        except Exception as e: errors.append((f"discm:{q}",type(e).__name__,str(e)))
        try:
            u=ia_url(q); st,final,b,data=fetch_json(u)
            docs=ia_docs(data)
            idocs.append((q,st,final,b,docs))
        except Exception as e: errors.append((f"ia:{q}",type(e).__name__,str(e)))
    return label,queries,kind,drows,idocs,errors

def main():
    print("StoneAge 2.5 exact physical/disc carrier probe — R1")
    print("SCOPE|source-named-retail-packs+Jan-Feb-2002-periodical-guide+crosspromo-carriers|DiscMaster+IA-metadata|no-payload")
    errors=[]; strict_discm={}; strict_ia={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs={ex.submit(one_target,t):t for t in TARGETS}
        results=[]
        for fut in concurrent.futures.as_completed(futs):
            try: results.append(fut.result())
            except Exception as e:
                t=futs[fut]; errors.append((t[0],type(e).__name__,str(e)))
    for label,queries,kind,drows,idocs,errs in sorted(results):
        errors.extend((f"{label}:{s}",k,m) for s,k,m in errs)
        for q,st,final,b,rows in drows:
            strict=[]
            for row in rows:
                blob=" ".join(str(row.get(k) or "") for k in ("itemName","fileid","filename","href","text","title"))
                if strict_match(label,queries,kind,blob): strict.append(row)
            print(f"DISCM_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|rows={len(rows)}|strict={len(strict)}|final={clean(final)}")
            for row in strict:
                key=(str(row.get("itemid","")),str(row.get("fileid","")))
                strict_discm[key]=(label,row)
                print(f"DISCM_HIT|label={label}|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}|ts={clean(row.get('ts'))}|b3sum={clean(row.get('b3sum'))}")
        for q,st,final,b,docs in idocs:
            strict=[]
            for row in docs:
                blob=" ".join(str(row.get(k) or "") for k in ("identifier","title","description","date","year"))
                if strict_match(label,queries,kind,blob): strict.append(row)
            print(f"IA_QUERY|label={label}|query={clean(q)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|items={len(docs)}|strict={len(strict)}|final={clean(final)}")
            for row in strict:
                ident=str(row.get("identifier") or "")
                strict_ia[ident]=(label,row)
                print(f"IA_HIT|label={label}|identifier={clean(ident)}|title={clean(row.get('title'))}|date={clean(row.get('date'))}|year={clean(row.get('year'))}|collection={clean(row.get('collection'))}")
    file_hits=0
    for ident,(label,row) in sorted(strict_ia.items()):
        try:
            st,final,b,meta=ia_metadata(ident)
            files=interesting_files(meta)
            print(f"IA_META|label={label}|identifier={clean(ident)}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|interesting_files={len(files)}|final={clean(final)}")
            for fr in files[:200]:
                file_hits+=1
                print(f"IA_FILE|label={label}|identifier={clean(ident)}|name={clean(fr.get('name'))}|size={clean(fr.get('size'))}|md5={clean(fr.get('md5'))}|sha1={clean(fr.get('sha1'))}")
        except Exception as e:
            errors.append((f"ia-meta:{ident}",type(e).__name__,str(e)))
    for scope,kind,msg in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(kind)}|message={clean(msg)}")
    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|strict_discm_hits|{len(strict_discm)}")
    print(f"COUNT|strict_ia_items|{len(strict_ia)}")
    print(f"COUNT|ia_interesting_files|{file_hits}")
    print(f"COUNT|errors|{len(errors)}")
    if file_hits:
        print("RESOLUTION|PRESERVED_CARRIER_FILES_FOUND|verify exact issue/product identity before any payload recovery")
    elif strict_discm or strict_ia:
        print("RESOLUTION|STRICT_CARRIER_METADATA_FOUND|inspect carrier provenance and missing/raw media next")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_STRICT_CARRIER|one or more exact carrier queries failed")
    else:
        print("RESOLUTION|NO_STRICT_CARRIER_HIT|tested public indexes expose no exact named 2.5 carrier")

if __name__=="__main__": main()
