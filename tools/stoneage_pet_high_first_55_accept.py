"""PET55: offline acceptance of retained dual source replays; no runtime claim."""
import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"research/pets"
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def walk(a,b,p=""):
    if a==b:return []
    if isinstance(a,dict) and isinstance(b,dict):
        assert a.keys()==b.keys()
        return [x for k in a for x in walk(a[k],b[k],p+"/"+k)]
    if isinstance(a,list) and isinstance(b,list):
        assert len(a)==len(b)
        return [x for i,(u,v) in enumerate(zip(a,b)) for x in walk(u,v,p+"/"+str(i))]
    return [p]
def main():
    c=(P/"PET-HIGH-FIRST-55-SOURCE-CUSTODY-R1.json").read_bytes()
    assert blob(c)=="965dbe1e69d935ccaa596554145278d56d7359fd"
    d=json.loads(c); reports=[]
    for row in d["receipts"]:
        raw=(P/row["report"]).read_bytes()
        assert (len(raw),sha(raw),blob(raw))==(row["report_bytes"],row["report_sha256"],row["report_git_blob"])
        reports.append(json.loads(raw))
    a,b=reports
    assert set(walk(a,b))=={"/original/receipt/public_pages/"+str(i)+"/"+f for i in (0,1) for f in ("bytes","sha256")}
    assert len(a["comparison_receipts"])==18 and a["comparison_receipts"]==b["comparison_receipts"]
    assert a["original"]["symbols"]==b["original"]["symbols"]
    assert [x["target"] for x in a["original"]["symbols"] if x["exact_symbols"]]==["NPC_EventAddEgg"]
    assert len(a["original"]["symbols"])==10
    f=a["original"]["symbols"][0]["intervals"][0]
    assert (f["start"],f["end"],f["instruction_count"],len(f["field_index_candidate_windows"]))==(4896128,4897696,409,6)
    assert not d["original_deployment_bridge"] and d["strict_gap_count"]==67 and d["official_acquisition_closed"]==0
    assert not d["raw_reports_equal"] and not d["original_payload_published"]
    print("PET55 acceptance: 18 source blobs, two preserved reports, one exact original symbol, nine bounded negatives, 67 open gaps")
if __name__=="__main__":main()
