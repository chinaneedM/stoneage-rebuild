#!/usr/bin/env python3
"""Query PET25 and PET26 official operator release EVENTS; never pretend to return complete species."""
import argparse,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"research/recovered"
def load():
 a=json.loads((BASE/"STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json").read_text(encoding="utf8"))
 b=json.loads((BASE/"STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json").read_text(encoding="utf8"))
 return a,b
def search(a,b,region=None,name="",leads=False,limit=100):
 if not 1<=limit<=1000:raise ValueError("limit 1..1000")
 rows=([*a["remaining_unconfirmed_official_leads"],*b["japan_taiwan_prelaunch_or_mechanic_leads"]] if leads else [*a["confirmed_official_release_records"],*b["new_japan_classic_official_release_events"]])
 result=[]
 for r in rows:
  if r.get("product_line") and "CLASSIC_PC" not in r["product_line"]:continue
  if region and r.get("region")!=region:continue
  text=str(r.get("official_name_as_written") or r.get("official_name_as_written_or_null") or r.get("name_as_source") or "").casefold()
  if name and name.casefold() not in text:continue
  result.append(r)
  if len(result)>=limit:break
 return result
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--region",choices=["JP","TW","CN","KR"])
 p.add_argument("--name",default="")
 p.add_argument("--leads",action="store_true")
 p.add_argument("--summary",action="store_true")
 p.add_argument("--limit",type=int,default=100)
 a=p.parse_args();old,new=load()
 val={"release_events_not_species":old["counts"]["release_documentary_records"]+len(new["new_japan_classic_official_release_events"]),"global_unique_species_count":None,"japan_operator_snapshots":new["japan_official_version_species_count_snapshots"]} if a.summary else search(old,new,a.region,a.name,a.leads,a.limit)
 print(json.dumps(val,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
