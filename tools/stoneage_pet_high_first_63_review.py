"""Validate PET63 source-pinned variant and documentary joins."""
import json
import hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main():
    r = json.loads((ROOT / "research/pets/PET-HIGH-FIRST-63-VARIANT-PERIOD-WITNESSES-R1.json").read_bytes())
    s = {}
    for k, pin in r["source_pins"].items():
        raw = (ROOT / pin["path"]).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == pin["blob"]
        s[k] = json.loads(raw)
    master = s["master"]["pet_flag_1_field_projections"]
    originals = {x["tw75_row_index"]: x for x in s["acquisition"]["projection"]["records"]}
    residual = {x["position"]: x for x in s["residual"]["rows"]}
    later = {x["template_id"]: x for x in s["comparison"]["rows"]}
    assert len(residual) == 67
    assert [x["position"] for x in r["rows"]] == sorted(set(r["target_positions"] + r["supplemental_positions"]))
    assert len(r["rows"]) == 13
    compatible = []
    for row in r["rows"]:
        p = row["position"]; x = master[p]
        assert (row["template_id"],row["graphic"],row["row_sha256"],row["name"],row["elements"],row["skill_capacity"]) == (x["template_id"],x["graphic"],x["row_sha256"],x["name"],x["elements"],x["skill_slot_capacity"])
        assert residual[p]["row_sha256"] == row["row_sha256"]
        assert not row["official_acquisition_verified"] and row["retain_strict_gap"] and row["official_first_release"] is None
        for table in row["tables"]:
            a = next((v for v in s["original"]["source_rows"][table["name"]] if v[1] == x["template_id"]), None)
            if a is None:
                assert table["match"] == "ABSENT" and table["row_sha256"] is None and table["visible_differences"] is None
                continue
            fields = dict(graphic=a[2],pet_flag=a[3],initnum=int(a[4]),lvup_literal=a[5],base=list(map(int,a[6:10])),elements=list(map(int,a[10:14])),skill_slot_capacity=a[14],skill_slots=a[15])
            assert table["row_sha256"] == a[16]
            assert table["match"] == ("EXACT_ROW" if a[16] == x["row_sha256"] else "SAME_ID_DIFFERENT_ROW")
            assert table["visible_differences"] == {k:dict(claimed=x[k],saved=v) for k,v in fields.items() if x[k] != v}
        assert row["same_name_other_positions"] == [dict(position=i,template_id=y["template_id"],graphic=y["graphic"],elements=y["elements"]) for i,y in enumerate(master) if i!=p and y["name"]==x["name"]]
        a,b=originals[p]["source_pairs"]
        assert row["selected_instances"] == a["instances"] and row["alternate_instances"] == b["instances"]
        assert row["selected_group_memberships"] == a["group_variants"][0]["group_memberships"]
        assert all(v["positive_routes"]==0 for pair in (a,b) for v in pair["group_variants"])
        c=later[x["template_id"]]
        assert row["later_comparison"] == dict(status=c["comparison_status"],instance_count=c["comparison_instance_count"],petflag1_lv1_count=c["instance_petflag1_lv1_count"],positive_reference_count=c["positive_reference_count"])
        for w in row["witnesses"]:
            assert w["source"] in r["documentary_sources"]
            assert w["ratio_matches"] == (None if w["elements"] is None else w["elements"]==x["elements"])
            assert w["capacity_matches"] == (None if "capacity" not in w else w["capacity"]==x["skill_slot_capacity"])
        if any(w["ratio_matches"] and "PLAYER_REPORTED" in w["kind"] for w in row["witnesses"]):
            compatible.append(p)
    assert compatible == r["summary"]["compatible_named_acquisition_reference_positions"] == [31,32,135,238,344,345]
    assert r["summary"]["strict_gap_count"] == 67 and r["summary"]["new_official_acquisition_closures"] == 0
    assert r["official_species_count"] is None and not r["original_assets_published"] and not r["runtime_executed"]
    print("PET63: 13 positions, 6 compatible player acquisition references, zero official closures")
if __name__ == "__main__":
    main()
