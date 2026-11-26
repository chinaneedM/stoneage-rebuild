"""PET109: retain PET108 verified derived index; bounded serial replay control."""
import argparse
import json
from pathlib import Path
import zipfile
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_104_accept as replay
from tools import stoneage_pet_high_first_108_cn75_archive_routes as prev
P=idx.ROOT/"research/pets"
SOURCE=P/"PET-HIGH-FIRST-108-CN75-ARCHIVE-ROUTES-R1.json"
RECEIPT=P/"PET-HIGH-FIRST-108-CUSTODY-R1.json"
OUT=P/"PET-HIGH-FIRST-109-CN75-BOUNDED-REPLAY-R1.json"
ZIP_SHA="b613c22d134a64fd5a27e1a1fe35398af2d67837ac7dfb625971442514b3c548"
REPORT_SHA="d8cb0265ae8d8deeaddefad0f151ca6792aefda10377e6b17e73a9b35ab9f793"
def dump(d):return (json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
def verify(raw):
    assert idx.sha(raw)==REPORT_SHA
    d=json.loads(raw)
    assert d["route_count"]==21 and d["query_count"]==25
    assert [(r["kind"],r["target_or_query"],r["request_url"]) for r in d["results"]]==prev.jobs()
    assert d["routes"]==[dict(name=n,url=u) for n,u in prev.ROUTES]
    assert d["original_payloads"]==d["official_closures"]==0 and not d["original_assets_published"]
    cd=d["results"][:21];ia=d["results"][21:]
    assert [x["metadata"]["row_count"] for x in cd if x["result"]=="METADATA_PARSED"]==[44,100,21,5,2,9,7,12,12,26,13,17,19,3,4,8,15,6,34,41]
    assert cd[-1]["result"]=="ACCESS_OR_PARSE_ERROR"
    assert cd[1]["metadata"]["limit_reached"]
    assert [x["metadata"]["num_found"] for x in ia]==[0,0,32,0]
    assert len(d["page_replays"])==19
    assert all(x["result"]=="ACCESS_ERROR" and "Connection refused" in x["error"] for x in d["page_replays"])
    assert [x["replay_url"] for x in d["page_replays"]]==[x["replay_url"] for x in prev.choices(d["results"])]
    return d
def main():
    p=argparse.ArgumentParser();p.add_argument("--artifact",type=Path,required=True);a=p.parse_args()
    z=a.artifact.read_bytes();assert len(z)==17918 and idx.sha(z)==ZIP_SHA
    with zipfile.ZipFile(a.artifact) as f:
        assert f.namelist()==["pet108.json"]
        raw=f.read("pet108.json")
    d=verify(raw)
    SOURCE.write_bytes(raw)
    rec=dict(schema="stoneage.pet108.custody.r1",source_head="fb60d199f9cd52f9587b5162c3e810588eb0a500",run=45815563230,job=139894306873,artifact=15116410155,zip_bytes=len(z),zip_sha256=ZIP_SHA,report_sha256=REPORT_SHA,report_git_blob=idx.blob(raw),official_closures=0,original_payloads=0)
    RECEIPT.write_bytes(dump(rec));assert verify(SOURCE.read_bytes())==d
    # First attempt all 19 returned the same connection-level error. Do not
    # repeat the entire batch: replay exactly two operator pages and NetEase.
    chosen=prev.choices(d["results"])[:3]
    assert [r["target"] for r in chosen]==[v for _,v in prev.ROUTES[:3]]
    pages=[replay.replay(row) for row in chosen]
    out=dict(schema="stoneage.pet109.cn75.bounded_replay.r1",prior_report_git_blob=idx.blob(raw),prior_report_sha256=REPORT_SHA,prior_common_error="Connection refused",attempts=pages,archive_catalogue_candidates=d["results"][23]["metadata"]["rows"],official_closures=0,original_payloads=0,original_assets_published=False)
    OUT.write_bytes(dump(out))
    print("PET108_CUSTODY="+json.dumps(rec,sort_keys=True),flush=True)
    print("PET109_RESULT="+json.dumps(out,ensure_ascii=False,sort_keys=True),flush=True)
    print("PET109_REPORT_SHA256="+idx.sha(OUT.read_bytes()),flush=True)
if __name__=="__main__":main()
