#!/usr/bin/env python3
"""Exact preservation-index lookup for archived Yegame StoneAge code EN0ZGKJ0002."""
from __future__ import annotations
import hashlib

from tools.stoneage_mainland_2000_testcd_probe import (
    fetch_json, ia_url, discm_url, ia_docs, discm_rows, clean
)

CODE="EN0ZGKJ0002"
QUERIES=(CODE, f"StoneAge {CODE}", f"石器时代 {CODE}")

def main():
    print("StoneAge Yegame exact product-code preservation lookup — R1")
    print(f"TARGET|code={CODE}|identity=石器时代|archived_medium=1-CD")
    print("SCOPE|InternetArchive+DiscMaster metadata only|no payload")
    errors=[]; ia_hits=[]; dm_hits=[]

    for q in QUERIES:
        try:
            st,final,b,obj=fetch_json(ia_url(q),timeout=40)
            docs=ia_docs(obj)
            strict=[d for d in docs if CODE.lower() in " ".join(str(v or "") for v in d.values()).lower()]
            ia_hits.extend(strict)
            print(f"IA_QUERY|query={clean(q)}|status={st}|items={len(docs)}|strict={len(strict)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for d in strict:
                print(f"IA_HIT|identifier={clean(d.get('identifier'))}|title={clean(d.get('title'))}|date={clean(d.get('date'))}|year={clean(d.get('year'))}|mediatype={clean(d.get('mediatype'))}")
        except Exception as e:
            errors.append((f"ia:{q}",type(e).__name__,str(e)))

        try:
            st,final,b,obj=fetch_json(discm_url(q),timeout=40)
            rows=discm_rows(obj)
            strict=[d for d in rows if CODE.lower() in " ".join(str(v or "") for v in d.values()).lower()]
            dm_hits.extend(strict)
            print(f"DISCM_QUERY|query={clean(q)}|status={st}|rows={len(rows)}|strict={len(strict)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
            for d in strict:
                print(f"DISCM_HIT|itemid={clean(d.get('itemid'))}|itemName={clean(d.get('itemName'))}|fileid={clean(d.get('fileid'))}|filename={clean(d.get('filename'))}|size={clean(d.get('size'))}")
        except Exception as e:
            errors.append((f"discm:{q}",type(e).__name__,str(e)))

    for scope,k,m in errors:
        print(f"ERROR|scope={clean(scope)}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|ia_hits|{len(ia_hits)}")
    print(f"COUNT|discm_hits|{len(dm_hits)}")
    print(f"COUNT|errors|{len(errors)}")
    if ia_hits or dm_hits:
        print("RESOLUTION|YEGAME_CODE_PRESERVATION_HIT|inspect exact carrier/file metadata next")
    elif errors:
        print("RESOLUTION|YEGAME_CODE_LOOKUP_PARTIAL|retry failed exact-token surfaces only")
    else:
        print("RESOLUTION|YEGAME_CODE_LOOKUP_BOUNDED|exact code absent from tested preservation indexes")
    print("EVIDENCE_BOUNDARY|Index absence does not negate the first-party archived Yegame product identity.")

if __name__=="__main__":
    main()
