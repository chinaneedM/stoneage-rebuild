#!/usr/bin/env python3
"""PET27: source-dated official pet release events by earliest year, region and original product line."""
import argparse,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"research/recovered"
PATH=BASE/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
def load(): return json.loads(PATH.read_text(encoding="utf-8"))
def choose(data,year=None,region=None,product=None):
    return [x for x in data["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"] if
            (year is None or x["year"]==year) and
            (region is None or x["region"]==region) and
            (product is None or x["product_line"]==product)]
def validate(data):
    a=json.loads((BASE/"STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json").read_text(encoding="utf-8"))
    b=json.loads((BASE/"STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json").read_text(encoding="utf-8"))
    rows=data["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]
    if len(rows)!=a["counts"]["release_documentary_records"]+len(b["new_japan_classic_official_release_events"]):raise ValueError("source event count has drifted")
    expected={x["record_id"] for x in a["confirmed_official_release_records"]}|{x["id"] for x in b["new_japan_classic_official_release_events"]}
    if {x["source_id"] for x in rows}!=expected:raise ValueError("source record identities drifted")
    if any(x["source_record_is_global_unique_species"] for x in rows):raise ValueError("unsupported species count asserted")
    if [y["year"] for y in data["yearly_work_queue"]]!=list(range(1999,2027)):raise ValueError("year range drifted")
    for y in data["yearly_work_queue"]:
        if y["research_gate"]!="NOT_YEAR_AUDITED": raise ValueError("incomplete year incorrectly marked closed")
        if y["documented_release_event_ids_from_existing_PET25_PET26"]!=[x["source_id"] for x in rows if x["year"]==y["year"]]:raise ValueError("year membership drifted")
    return True
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year",type=int);p.add_argument("--region",choices=["TW","CN","JP","KR","OTHER"])
    p.add_argument("--product");p.add_argument("--summary",action="store_true");p.add_argument("--validate",action="store_true")
    opts=p.parse_args();d=load()
    if opts.validate:validate(d)
    if opts.summary:
        output={"current_frontier":d["current_frontier"],"years":len(d["yearly_work_queue"]),"existing_documentary_events_not_species":len(d["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]),"global_species_count":None}
    elif opts.year is not None:
        if opts.year<1999 or opts.year>2026:raise SystemExit("year is outside current research window")
        y=d["yearly_work_queue"][opts.year-1999]
        output={"year":opts.year,"year_research_gate":y["research_gate"],"events":choose(d,opts.year,opts.region,opts.product)}
    else:output=choose(d,None,opts.region,opts.product)
    print(json.dumps(output,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
