"""Replay PET62 retained source joins; no runtime or official release inference."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/pets/PET-HIGH-FIRST-62-RESIDUAL-ACQUISITION-REVIEW-R1.json"
def main():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    s = {}
    for key, pin in report["source_pins"].items():
        raw = (ROOT / pin["path"]).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == pin["blob"], key
        s[key] = json.loads(raw)
    rows = report["rows"]
    assert len(rows) == len({x["position"] for x in rows}) == 67
    assert [x["position"] for x in rows] == s["a"]["remaining_gap_row_indices"]
    assert [x["position"] for x in rows] == [x["tw75_row_index"] for x in s["b"]["projection"]["records"]]
    assert report["official_species_count"] is None and not report["original_payload_published"] and not report["runtime_executed"]
    for row, original in zip(rows, s["b"]["projection"]["records"]):
        p = row["position"]
        visual = next(x for x in s["i"]["rows"] if x["position"] == p)
        skill = next(x for x in s["m"]["rows"] if x["position"] == p)
        assert row["row_sha256"] == original["row_sha256"] == visual["master_row_sha256"] == skill["row_sha256"]
        assert row["template_id"] == original["template_id"] == visual["template_id"] == skill["template_id"]
        assert row["graphic"] == original["graphic"] == visual["graphic"] == skill["graphic"]
        assert row["name"] == original["name"]
        for i, prefix in enumerate(("selected", "alternate")):
            pair = original["source_pairs"][i]
            assert row[prefix + "_match"] == pair["match"]
            assert row[prefix + "_instance_ids"] == [x["instance_id"] for x in pair["instances"]]
            assert all(x["positive_routes"] == 0 for x in pair["group_variants"])
        assert row["positive_routes"] == 0
        assert row["group_membership_candidate"] == any(x["position"] == p for x in s["c"]["target_rows"])
        assert row["context_refs"] == [x["note"] for x in s["a"]["context"] if x["tw75_row_index"] == p]
        assert row["named_variant_review"] == any(x["target_position"] == p for x in s["d"]["rows"])
        for key, field, grade in (("e","commercial_reference_grades","grade"), ("f","egg_role_grades","grade"), ("j","task_role_grades","role")):
            assert row[field] == [x[grade] for x in s[key]["rows"] if x["position"] == p]
        candidates = [x for x in s["g"]["scan"]["typed_candidate_lines"] if any(set(f.get("instance_ids",[])) & set(row["selected_instance_ids"]) for f in x["fields"])]
        assert row["original_npc_candidates"] == [{k:x[k] for k in ("path","line","line_sha256")} for x in candidates]
        group = next(x for x in s["k"]["groups"] if p in x["positions"])
        assert row["visual_group"] == group["group"] and group["graphic"] == row["graphic"]
        expected = "TW85_DIRECT_PRIOR" if group["tw85_complete_samples"] else "TW85_DIRECT_R60" if any(x["physical_group"] == group["group"] for x in s["l"]["observations"]["sequences"]) else "CN50_EXACT_INHERITANCE" if group["cn50_exact_spr_and_rd_complete_samples"] else "OPEN"
        assert row["sequence_receipt"] == expected != "OPEN"
        assert row["skill_primary_match"] == skill["scope"]["petskill.txt"]["template_match"]
        assert row["skill_primary_slots"] == len(skill["scope"]["petskill.txt"]["source_slots"])
        assert row["skill_alternate_slots"] == len(skill["scope"]["petskill1.txt"]["source_slots"])
        assert row["reopen_on"] and row["retain_strict_gap"] and not row["official_acquisition_verified"] and row["official_first_release"] is None
    from collections import Counter
    q = report["summary"]
    assert q["positions"] == 67 and q["unique_graphics"] == len({x["graphic"] for x in rows}) == 66
    assert q["selected_match"] == Counter(x["selected_match"] for x in rows)
    assert q["selected_with_instances"] == sum(bool(x["selected_instance_ids"]) for x in rows) == 65
    assert q["selected_exact_with_instances"] == sum(x["selected_match"] == "EXACT_ROW" and bool(x["selected_instance_ids"]) for x in rows) == 62
    assert q["primary_skill_slots"] == sum(x["skill_primary_slots"] for x in rows) == 135
    assert q["alternate_skill_slots"] == sum(x["skill_alternate_slots"] for x in rows) == 12
    assert q["sequence_receipts_by_position"] == Counter(x["sequence_receipt"] for x in rows)
    for key, field in (("group_membership_candidates","group_membership_candidate"),("original_npc_candidate_positions","original_npc_candidates"),("documentary_context_positions","context_refs"),("commercial_reference_positions","commercial_reference_grades"),("task_role_positions","task_role_grades"),("egg_role_positions","egg_role_grades")):
        assert q[key] == sum(bool(x[field]) for x in rows)
    assert q["new_official_acquisition_closures"] == 0
    raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
    assert len(raw) == 2709173
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == "c89e0e33537990aa2132b47c40fef49a985a935c"
    print("PET62: 67 source positions, 66 visual groups, 135 primary + 12 alternate skill slots, 0 official closures")
if __name__ == "__main__":
    main()
