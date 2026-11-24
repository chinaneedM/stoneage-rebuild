"""Validate source-qualified egg/object distinctions; original probe remains separate."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT="research/pets/PET-HIGH-FIRST-54-EGG-ROLE-PREFLIGHT-R1.json"

def read(path):
    return json.loads((ROOT/path).read_bytes())

def main():
    r=read(REPORT)
    for path,sha in r["source_pins"].items():
        raw=(ROOT/path).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha
    m,s,table,grid,doc,q,exe=[read(p) for p in r["source_pins"]]
    assert [x["position"] for x in r["rows"]]==[387,453,454]
    for row in r["rows"]:
        i=row["position"]
        a=m["pet_flag_1_field_projections"][i]
        assert i in q["remaining_gap_row_indices"]
        for key in ("name","template_id","graphic","initnum","elements"):
            assert row[key]==a[key]
        assert row["master_row_sha256"]==a["row_sha256"] and row["base_fields"]==a["base"]
        assert row["skill_capacity"]==a["skill_slot_capacity"]
        z=next(x for x in s["projection"]["records"] if x["tw75_row_index"]==i)
        assert row["source_pairs"]==z["source_pairs"]
        assert row["selected_base_row"]==next(x for x in table["source_rows"]["enemybase.txt"] if x[1]==a["template_id"])
        assert row["alternate_base_row"]==next((x for x in table["source_rows"]["enemybase2.txt"] if x[1]==a["template_id"]),None)
        assert row["source_named_album_rows"]==[dict(program=p,**x) for p,v in grid["programs"].items() for x in v["source_records"] if x["original_name_cp950"]==a["name"]]
        assert row["client_join_status"]==a["client_join_status"]
        assert row["retain_strict_gap"] and not row["official_acquisition_verified"] and not row["actual_hatching_verified"] and row["official_first_release"] is None
    egg,mela,mela_egg=r["rows"]
    assert (egg["template_id"],mela["template_id"],mela_egg["template_id"])==(1045,1140,1145)
    assert egg["graphic"]==mela_egg["graphic"]==101489 and mela["graphic"]==101760
    assert egg["role"]==mela_egg["role"]=="EGG_INTERMEDIATE_OBJECT_CANDIDATE_NOT_DISTINCT_SPECIES"
    assert mela["role"]=="NAMED_PET_CANDIDATE"
    assert [len(x["source_named_album_rows"]) for x in r["rows"]]==[4,4,0]
    assert [x["source_pairs"][0]["match"] for x in r["rows"]]==["EXACT_ROW","SAME_ID_DIFFERENT_ROW","EXACT_ROW"]
    assert [x["source_pairs"][0]["instances"][0]["instance_id"] for x in r["rows"]]==[2055,2474,2479]
    assert all(x["source_pairs"][0]["instances"][0]["pet_flag"]==1 and x["source_pairs"][0]["instances"][0]["level"]==[1,1] for x in r["rows"])
    assert all(x["source_pairs"][0]["group_variants"][0]["positive_routes"]==0 for x in r["rows"])
    assert r["documented_2002_stage_order"]==doc["extraction"]["fusion_hatching"]["reported_stage_order"]
    assert r["documentary_native_egg_id"] is None and not r["documentary_to_saved_template_bridge_verified"]
    assert r["same_graphic_does_not_identify_hatch_result"] and r["strict_gap_count"]==len(q["remaining_gap_row_indices"])==67
    assert r["official_acquisition_closed"]==0 and r["official_species_count"] is None
    assert not r["original_assets_published"] and not r["new_original_source_bytes"] and not r["runtime_executed"]
    assert r["source_probe_status"]=="PENDING_ORIGINAL_SOURCE_JOB"
    print("PET54_PREFLIGHT_PASS: two distinct egg objects, one named pet, no proven hatch route")

if __name__=="__main__":
    main()
