#!/usr/bin/env python3
"""PET25: query documentary official-release records; never equate them to global species."""
import argparse
import json
from pathlib import Path

DATA=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json"

def select(d,region=None,product=None,name="",only_leads=False,limit=100):
    if not 1 <= limit <= 1000: raise ValueError("limit must be 1..1000")
    rows=d["remaining_unconfirmed_official_leads"] if only_leads else d["confirmed_official_release_records"]
    needle=name.casefold().strip()
    return [r for r in rows
            if (not region or r["region"]==region)
            and (not product or r["product_line"]==product)
            and (not needle or needle in (r.get("official_name_as_written") or r.get("name_as_source") or "").casefold())][:limit]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region",choices=["CN","TW","JP","KR"])
    parser.add_argument("--product")
    parser.add_argument("--name",default="")
    parser.add_argument("--leads",action="store_true")
    parser.add_argument("--summary",action="store_true")
    parser.add_argument("--limit",type=int,default=100)
    a=parser.parse_args()
    d=json.loads(DATA.read_text(encoding="utf-8"))
    v=d["counts"] if a.summary else select(d,a.region,a.product,a.name,a.leads,a.limit)
    print(json.dumps(v,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
