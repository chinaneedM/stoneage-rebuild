#!/usr/bin/env python3
"""DiscMaster filename-only residual for exact Yegame StoneAge code EN0ZGKJ0002."""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request
from tools.stoneage_mainland_2000_testcd_probe import discm_rows, clean

UA="stoneage-rebuild-archaeology/1.0"
CODE="EN0ZGKJ0002"
DISCM="https://discmaster.textfiles.com/search"

def url():
    p=[("q",f'"{CODE}"'),("qfields","name"),("mode","deep"),("dedup","dedup"),
       ("limit","200"),("outputAs","json"),("showItemName","showItemName"),
       ("tsMin","1999"),("tsMax","2005")]
    return DISCM+"?"+urllib.parse.urlencode(p)

def main():
    print("StoneAge Yegame product-code DiscMaster filename residual — R2")
    print(f"TARGET|code={CODE}|field=name")
    print("SCOPE|DiscMaster filename index only|no payload")
    try:
        req=urllib.request.Request(url(),headers={"User-Agent":UA,"Accept":"application/json,*/*","Accept-Encoding":"identity"})
        with urllib.request.urlopen(req,timeout=45) as r:
            b=r.read(8*1024*1024)
            st=int(getattr(r,"status",r.getcode()));final=r.geturl()
        obj=json.loads(b.decode("utf-8","replace"))
        rows=discm_rows(obj)
        strict=[x for x in rows if CODE.lower() in " ".join(str(v or "") for v in x.values()).lower()]
        print(f"QUERY|status={st}|rows={len(rows)}|strict={len(strict)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
        for x in strict:
            print(f"HIT|itemid={clean(x.get('itemid'))}|itemName={clean(x.get('itemName'))}|fileid={clean(x.get('fileid'))}|filename={clean(x.get('filename'))}|size={clean(x.get('size'))}")
        print(f"COUNT|strict_hits={len(strict)}")
        print("RESOLUTION|YEGAME_CODE_FILENAME_HIT" if strict else "RESOLUTION|YEGAME_CODE_FILENAME_BOUNDED|exact code absent from DiscMaster filename index")
    except Exception as e:
        print(f"ERROR|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|YEGAME_CODE_FILENAME_PARTIAL|retry exact filename lookup only")
    print("EVIDENCE_BOUNDARY|Index absence does not negate archived Yegame product identity.")

if __name__=="__main__":main()
