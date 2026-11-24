"""Replay PET52 against pinned, accepted source projections; no live-release promotion."""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = "research/pets/PET-HIGH-FIRST-52-NAMED-VISUAL-ACQUISITION-VARIANTS-R1.json"

def load(path):
    return json.loads((ROOT / path).read_bytes())

def main():
    report = load(REPORT)
    for path, sha in report["source_pins"].items():
        raw = (ROOT / path).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == sha, path
    master, cn, tw, saved, vip, quest, residual, replay = [load(p) for p in report["source_pins"]]
    assert [r["target_position"] for r in report["rows"]] == [144, 208]
    for row, expected in zip(report["rows"], [(93, 100343, 323, 2601, 1235), (123, 100373, 2572, 2589, 1223)]):
        ordinal, graphic, instance, vip_instance, vip_template = expected
        assert row["graphic"] == graphic and row["target_position"] in residual["remaining_gap_row_indices"]
        cr = next(x for x in cn["records"] if x["ordinal"] == ordinal)
        v = row["cn50_visual"]
        assert v == dict(ordinal=cr["ordinal"],name=cr["compiled_name"],portrait_alias=cr["portrait_alias"],portrait_bitmap=cr["portrait_lookup_after_ordered_load"],portrait_rd_sha256=cr["portrait_lookup_rd_sha256"],early_relation=cr["earlier_tw10_relation"],spr_groups=cr["spr_groups"])
        assert v["early_relation"] == "EARLY_TW10_PORTRAIT_FULL_RD_SHA_EXACT"
        assert {x["spr_group"] for x in v["spr_groups"]} == ({100343,100732} if ordinal==93 else {100373,100762})
        assert row["tw85_program_rows"] == [dict(program=k,**next(x for x in val["source_records"] if x["slot"]==ordinal)) for k,val in tw["programs"].items()]
        assert len(row["tw85_program_rows"]) == 4 and len({x["original_row_sha256"] for x in row["tw85_program_rows"]}) == 1
        for variant in row["master_variants"]:
            m = master["pet_flag_1_field_projections"][variant["position"]]
            assert m["name"] == row["name"] and m["graphic"] == graphic
            assert variant == dict(position=variant["position"],template_id=m["template_id"],row_sha256=m["row_sha256"],elements=m["elements"],initnum=m["initnum"],skill_capacity=m["skill_slot_capacity"],skill_slots=m["skill_slots"])
        src = next(x for x in saved["projection"]["records"] if x["tw75_row_index"]==row["target_position"])
        sel = src["source_pairs"][0]
        ins = next(x for x in sel["instances"] if x["instance_id"]==instance)
        assert row["selected_saved_instance"] == dict(instance_id=instance,template_id=src["template_id"],match=sel["match"],level=ins["level"],pet_flag=ins["pet_flag"],positive_routes=sel["group_variants"][0]["positive_routes"])
        assert sel["match"] == "EXACT_ROW" and ins["level"] == [1,1] and ins["pet_flag"] == 1
        assert row["selected_saved_instance"]["positive_routes"] == 0
        p = next(x for x in vip["petabi_rows"] if x["instance_id"]==vip_instance)
        assert p["template_id"] == vip_template and not p["official_delivery_verified"]
        assert not vip["compiled_vip_boundary"]["matching_loader_located_in_preserved_exe"]
        assert row["vip_configuration"] == dict(instance_id=vip_instance,template_id=vip_template,preset_fields=p["preset_fields"],vip_points=p["vip_points"],official_delivery_verified=False,matching_loader_located=False)
        assert vip_template not in {x["template_id"] for x in row["master_variants"]}
        assert row["retain_template_gap"] and not row["official_target_acquisition_verified"] and row["official_first_release"] is None
        assert all(k in report["sources"] for k in row["documentary_sources"])
    frog, red = report["rows"]
    assert frog["master_variants"][0]["elements"] == frog["documentary_elements"] == [30,0,0,70]
    assert frog["ordinary_reward"] is None
    assert red["documentary_elements"] == [0,20,80,0]
    assert [(x["template_id"],x["elements"],x["initnum"],x["skill_capacity"]) for x in red["master_variants"]] == [(106,[0,20,80,0],27,4),(303,[0,20,80,0],27,4),(724,[0,50,50,0],37,7)]
    q = next(x for x in quest["rows"] if x["award_instance_id"]==352)
    rr = next(x for x in replay["rows"] if x["award_instance_id"]==352)
    assert q["template_id"] == rr["template_id"] == 303 and rr["instance_level"] == [1,1]
    assert rr["instance_pet_flag"] == rr["template_pet_flag"] == 1
    assert any(x["path"]=="poru/boy04" and x["floor"]==5511 for x in q["script_refs"])
    assert red["ordinary_reward"] == dict(instance_id=352,template_id=303,position=171,source_script="poru/boy04",floor=5511,level=[1,1],actual_award_verified=False)
    assert not q["actual_award_verified"] and not q["official_same_deployment_verified"]
    assert report["remaining_gap_before"] == report["remaining_gap_after"] == len(residual["remaining_gap_row_indices"]) == 67
    assert report["official_acquisition_closed"] == 0 and report["official_species_count"] is None
    assert all(report[k] is False for k in ("original_assets_published","source_bytes_newly_extracted","web_html_bytes_retrieved","runtime_executed"))
    print("PET52_ACCEPTANCE_PASS: 2 native visual comparisons, 4 separate master rows, 2 VIP presets, 0 official acquisition closures")

if __name__ == "__main__":
    main()
