#!/usr/bin/env python3
"""Search the official operator pet evidence queue without counting private servers."""
import argparse
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-PET-OFFICIAL-GLOBAL-RELEASE-EVIDENCE-R1.json"

def select(data, query="", region=None, confirmed_only=False, limit=20):
    if not 1 <= limit <= 1000:
        raise ValueError("limit out of bounded range")
    rows = data["confirmed_in_game_official_pets_in_this_register"] if confirmed_only else data["official_web_evidence_queue_NOT_RELEASE_PROVEN"]
    q = query.casefold().strip()
    found=[]
    for x in rows:
        if region and x.get("region")!=region:
            continue
        if q and not any(q in str(x.get(k) or "").casefold() for k in
                         ("official_name_from_page_or_null","source_id","operator_original_image_url")):
            continue
        found.append(x)
        if len(found)>=limit:
            break
    return found

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query",default="")
    p.add_argument("--region",choices=("JP","CN","TW","KR"))
    p.add_argument("--confirmed-only",action="store_true")
    p.add_argument("--summary",action="store_true")
    p.add_argument("--limit",type=int,default=20)
    args=p.parse_args()
    data=json.loads(SOURCE.read_text(encoding="utf-8"))
    result=data["evidence_summary"] if args.summary else select(data,args.query,args.region,args.confirmed_only,args.limit)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
