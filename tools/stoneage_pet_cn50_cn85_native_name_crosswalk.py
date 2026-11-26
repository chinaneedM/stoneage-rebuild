"""Replay CN5-to-CN8.5 compiled name crosswalk from exact source blobs."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P50=ROOT/"research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json"
P85=ROOT/"research/pets/PET-HIGH-FIRST-122-CN85-COMPLETE-TRANSFER-R1.json"
REPORT=ROOT/"research/pets/PET-CN50-CN85-NATIVE-NAME-CROSSWALK-R1.json"
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def main():
    d=json.loads(REPORT.read_bytes())
    assert blob(P50.read_bytes())==d["input_git_blobs"]["cn50"]=="8b1058a43c267dfeaa298d4c2c472209cebd24d9"
    assert blob(P85.read_bytes())==d["input_git_blobs"]["cn85"]=="a6ed895e5b6b18ebaa1c02e809da5a17937dd176"
    old=[dict(ordinal=x["ordinal"],slot=x["source_raw_first_i32"],face=x["source_raw_trailing_u32"],name=x["label_as_compiled_GB18030"]) for x in json.loads(P50.read_bytes())["records"]]
    q=json.loads(P85.read_bytes())["analysis"]["compiled_table_candidates"]
    assert q[1]["candidates"][0]["entries"]==q[2]["candidates"][0]["entries"]
    assert q[1]["candidates"][1]["entries"]==q[2]["candidates"][1]["entries"]
    new=[dict(x,ordinal=j+(593 if i else 0)) for i,c in enumerate(q[1]["candidates"]) for j,x in enumerate(c["entries"])]
    by={x["ordinal"]:x for x in new};n=[x for x in new if x["slot"]>=0];o=[x for x in old if x["slot"]>=0]
    rows=[]
    for x in old:
        y=by.get(x["ordinal"])
        rows.append(dict(cn50=x,cn85_same_ordinal=y,exact_same_ordinal=y==x,cn85_same_name_candidates=[z for z in n if z["name"]==x["name"]] if x["slot"]>=0 else [],same_deployment_verified=False))
    assert rows==d["rows"]
    later=[x for x in n if x["ordinal"]>=362];names={x["name"] for x in o}
    added=[x for x in n if x["name"] not in names]
    assert later==d["cn85_later_parsed_positions"] and added==d["cn85_names_absent_from_cn50_positions"]
    summary=dict(cn50_physical_positions=len(old),cn50_named_positions=len(o),cn85_parsed_positions=len(new),cn85_named_positions=len(n),cn85_distinct_names=len({x["name"] for x in n}),old_named_positions_with_same_name=sum(x["cn50"]["slot"]>=0 and bool(x["cn85_same_name_candidates"]) for x in rows),old_named_exact_ordinal_slot_face_name=sum(x["cn50"]["slot"]>=0 and x["exact_same_ordinal"] for x in rows),old_placeholder_exact_ordinal=sum(x["cn50"]["slot"]==-1 and x["exact_same_ordinal"] for x in rows),later_named_positions=len(later),new_distinct_names=len({x["name"] for x in added}),unparsed_record_lengths=49)
    summary["old_placeholder_same_ordinal_slot_face"]=sum(x["cn50"]["slot"]==-1 and x["cn50"]["face"]==0 and x["cn85_same_ordinal"] is not None and x["cn85_same_ordinal"]["slot"]==-1 and x["cn85_same_ordinal"]["face"]==0 for x in rows)
    assert summary["old_placeholder_same_ordinal_slot_face"]==57
    assert summary==d["summary"]
    assert summary["old_named_exact_ordinal_slot_face_name"]==304 and summary["old_named_positions_with_same_name"]==305 and summary["new_distinct_names"]==208
    assert d["official_closures"]==0 and not d["original_assets_published"] and d["active_module"]=="PET"
    print("CN50_CN85_CROSSWALK_PASS",json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
