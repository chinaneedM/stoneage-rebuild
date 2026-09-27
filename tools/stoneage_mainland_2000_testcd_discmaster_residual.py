#!/usr/bin/env python3
"""Retry only the five DiscMaster English residuals that timed out in the
Mainland Dec-2000 official test-CD R1 preservation probe.

Two scopes are kept distinct:
1) filename/name-index search, which is cheaper and should complete;
2) full-text deep search, matching the R1 surface, run sequentially with a
   larger timeout to avoid self-induced concurrent timeouts.

Metadata only; no carrier payload is downloaded.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
DISCM="https://discmaster.textfiles.com/search"

QUERIES=(
    ("latin-test-cd","StoneAge test CD"),
    ("latin-beta-waei","StoneAge beta Waei"),
    ("latin-trial-waei","StoneAge trial Waei"),
    ("latin-jinghe","StoneAge Jinghe"),
    ("latin-jhpop","StoneAge jhpop"),
)

def clean(v,n=3000):
    return " ".join(str(v or "").split()).replace("|","%7C")[:n]

def normalized(v):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+","",str(v or "").lower())

def row_blob(row):
    if not isinstance(row,dict):
        return ""
    return normalized(" ".join(str(v or "") for v in row.values()))

def strict(row):
    blob=row_blob(row)
    title="stoneage" in blob or "石器时代" in blob
    marker=any(x in blob for x in ("test","trial","beta","waei","jinghe","jhpop","测试","试玩","晶合"))
    return title and marker

def fetch_json(url,timeout):
    req=urllib.request.Request(
        url,
        headers={
            "User-Agent":UA,
            "Accept":"application/json,text/plain,*/*;q=0.5",
            "Accept-Encoding":"identity",
        },
    )
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read(4*1024*1024)
        return int(getattr(r,"status",r.getcode())),r.geturl(),body,json.loads(body.decode("utf-8"))

def search_url(q,qfields):
    p=[
        ("q",f'"{q}"'),
        ("qfields",qfields),
        ("mode","deep"),
        ("dedup","dedup"),
        ("limit","200"),
        ("outputAs","json"),
        ("showItemName","showItemName"),
        ("tsMin","1999"),
        ("tsMax","2002"),
    ]
    return DISCM+"?"+urllib.parse.urlencode(p)

def rows_from(v):
    rows=[]
    def walk(n):
        if isinstance(n,dict):
            if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n or "name" in n):
                rows.append(n)
            for c in n.values():
                walk(c)
        elif isinstance(n,list):
            for c in n:
                walk(c)
    walk(v)
    out=[];seen=set()
    for r in rows:
        k=(str(r.get("itemid","")),str(r.get("fileid","")),str(r.get("href","")),str(r.get("filename","")))
        if k not in seen:
            seen.add(k);out.append(r)
    return tuple(out)

def main():
    print("StoneAge Mainland Dec-2000 test-CD DiscMaster English residual — R2")
    print("PARENT|STONEAGE-MAINLAND-2000-TEST-CD-PRESERVATION-R1|five-English-DiscMaster-timeouts-only")
    print("SCOPE|DiscMaster metadata only|filename-index + sequential full-text-deep|no-payload")
    hits={}
    errors=[]

    for label,q in QUERIES:
        for scope,qfields,timeout in (("name","name",45),("text","t",75)):
            try:
                st,final,body,data=fetch_json(search_url(q,qfields),timeout=timeout)
                rows=rows_from(data)
                strict_rows=[r for r in rows if strict(r)]
                print(
                    f"QUERY|label={label}|scope={scope}|query={clean(q)}|status={st}|"
                    f"bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
                    f"rows={len(rows)}|strict={len(strict_rows)}|final={clean(final)}"
                )
                for r in strict_rows:
                    key=(str(r.get("itemid","")),str(r.get("fileid","")),str(r.get("filename","")),scope)
                    hits[key]=r
                    print(
                        f"HIT|label={label}|scope={scope}|itemid={clean(r.get('itemid'))}|"
                        f"itemName={clean(r.get('itemName'))}|fileid={clean(r.get('fileid'))}|"
                        f"filename={clean(r.get('filename') or r.get('name'))}|size={clean(r.get('size'))}|"
                        f"ts={clean(r.get('ts'))}|b3sum={clean(r.get('b3sum'))}"
                    )
            except Exception as e:
                errors.append((label,scope,type(e).__name__,str(e)))
                print(f"ERROR|label={label}|scope={scope}|kind={clean(type(e).__name__)}|message={clean(e)}")

    print(f"COUNT|query_identities|{len(QUERIES)}")
    print(f"COUNT|surfaces_attempted|{len(QUERIES)*2}")
    print(f"COUNT|strict_hits|{len(hits)}")
    print(f"COUNT|errors|{len(errors)}")
    name_errors=sum(1 for _,s,_,_ in errors if s=="name")
    text_errors=sum(1 for _,s,_,_ in errors if s=="text")
    print(f"COUNT|name_errors|{name_errors}")
    print(f"COUNT|text_errors|{text_errors}")

    if hits:
        print("RESOLUTION|STRICT_DISCM_METADATA_FOUND|authenticate candidate against Dec-2000 China.com/Jinghe provenance")
    elif not errors:
        print("RESOLUTION|ENGLISH_DISCM_RESIDUAL_BOUNDED|all five R1 timeout identities completed with zero strict hits")
    elif not name_errors and text_errors:
        print("RESOLUTION|NAME_INDEX_BOUNDED_TEXT_RESIDUAL_OPEN|filename/name index completed; only full-text timeouts remain")
    else:
        print("RESOLUTION|PARTIAL_RESIDUAL|retry only failed DiscMaster surfaces")
    print("EVIDENCE_BOUNDARY|no indexed hit cannot negate the contemporaneously documented test CD; official giveaway original and player-burned copies must remain separate provenance classes.")

if __name__=="__main__":
    main()
