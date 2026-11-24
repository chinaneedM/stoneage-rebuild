"""Replay PET53 source joins; period web claims stay external and bounded."""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = "research/pets/PET-HIGH-FIRST-53-COMMERCIAL-HONOR-REWARD-REFERENCES-R1.json"

def read(p):
    return json.loads((ROOT / p).read_bytes())

def main():
    r = read(REPORT)
    for p, sha in r["source_pins"].items():
        raw = (ROOT / p).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == sha
    m, q, s, prev, p47 = [read(p) for p in r["source_pins"]]
    assert r["prior_gap_count"] == r["strict_gap_count"] == len(q["remaining_gap_row_indices"]) == 67
    assert [x["position"] for x in r["rows"]] == [208,68,75,144]
    for x in r["rows"]:
        i = x["position"]
        assert i in q["remaining_gap_row_indices"]
        a = m["pet_flag_1_field_projections"][i]
        for key in ("name","template_id","graphic","row_sha256","elements"):
            assert a[key] == x[key]
        assert x["skill_capacity"] == a["skill_slot_capacity"]
        z = next(v for v in s["projection"]["records"] if v["tw75_row_index"] == i)
        assert z["template_id"] == a["template_id"] and z["source_pairs"][0]["match"] == "EXACT_ROW"
        assert x["selected_saved_instance_ids"] == [v["instance_id"] for v in z["source_pairs"][0]["instances"]]
        assert x["positive_routes"] == z["source_pairs"][0]["group_variants"][0]["positive_routes"] == 0
        assert x["retain_strict_gap"] and not x["official_same_deployment_verified"] and not x["actual_award_verified"] and x["official_first_release"] is None
        assert all(k in r["sources"] for k in x["refs"])
    red, p1, p2, frog = r["rows"]
    assert red["elements"] == red["ratio"] == [0,50,50,0] and red["skill_capacity"] == red["capacity"] == 7
    assert red["template_id"] == 724 and red["selected_saved_instance_ids"] == [2572]
    old_red = next(x for x in prev["rows"] if x["target_position"] == 208)
    assert old_red["ordinary_reward"]["template_id"] == 303 and old_red["vip_configuration"]["template_id"] == 1223
    assert old_red["documentary_elements"] != red["elements"]
    assert any(x["tw75_row_index"] == 208 and x["qualification"] == "NAME_MATCH_ELEMENT_CONFLICT_DO_NOT_ASSIGN" for x in p47["period_links"])
    assert p1["elements"] == [0,0,50,50] and p2["elements"] == [0,50,50,0]
    assert p1["ratio"] is p2["ratio"] is None and p1["capacity"] is p2["capacity"] is None
    assert p1["refs"] == p2["refs"] == ["panda"] and r["sources"]["panda"]["date"] == "2012-02-09"
    assert not frog["reference_new"] and frog["ratio"] == [30,0,0,70]
    assert sorted(x["position"] for x in r["rows"] if x["reference_new"]) == r["new_compatible_documentary_reference_positions"] == [68,75,208]
    assert r["official_acquisition_closed"] == 0 and r["official_species_count"] is None
    assert all(r[k] is False for k in ("original_assets_published","raw_web_html_retrieved","new_original_source_bytes","runtime_executed"))
    print("PET53_ACCEPTANCE_PASS: three documentary reference positions, one bounded nonjoin, 67 strict gaps")

if __name__ == "__main__":
    main()
