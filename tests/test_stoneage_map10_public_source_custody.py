"""Public MAP10 metadata and evidence-boundary tests. No private DAT/RD/PNG is committed."""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "research/recovered"
A = "STONEAGE-MAP10-PUBLIC-ORIGINAL-SOURCE-CUSTODY-R1.json"
I = "STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json"
G = "STONEAGE-MAP09-264-EXCLUDED-SOURCE-GAPS-R1.json"

def validate(r, i, g):
    columns = i["per_floor_source_row_columns"]
    floors = {a[0]: dict(zip(columns, a)) for a in i["per_floor_source_rows"]}
    excluded = g["excluded_maps"]
    low_only = {n for n, a in excluded.items() if a["unqualified_gt99_occurrences"] == 0}
    gt99_missing = {n for n, a in excluded.items() if a["unqualified_gt99_occurrences"] > 0}
    assert len(low_only) == 60 and len(gt99_missing) == 204
    assert set(r["maps"]) == {n[:-4] for n in low_only}
    assert len(floors) == 955 and len(r["maps"]) == 60
    assert r["pinned_start"]["current_state_git_blob"] == "c89e0e33537990aa2132b47c40fef49a985a935c"
    assert r["previous_691"] == {"maps":691, "full_RGBA_frame_states":2073,
                                 "source_png_aliases":3496, "old_receipt_unchanged":True}
    assert r["new_60"] == {"maps":60, "full_RGBA_frame_states":180,
         "qualified_gt99_position_occurrences":64526, "unrendered_low_1_to_99_occurrences":69830,
         "qualified_gt99_aliases_used":1138, "additional_original_PNG_from_MAP04":138,
         "new_original_RD_decodes":0, "pillow_numpy_frame_SHA_all_equal":True}
    assert r["combined_private_observer"] == {"maps":751,"source_PNG_aliases":3634,
                                                "source_bound_full_RGBA_states":2253}
    assert r["missing_source"] == {"still_excluded_gt99_maps":204,
          "distinct_unqualified_gt99_aliases":1114,"unqualified_gt99_occurrences":29748}
    assert r["original_DAT_source_zip"]["sha256"] == "c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a"
    assert r["original_MAP04_PNG_archive"]["sha256"] == i["provenance"]["source_private_png_zip_sha256"]
    assert r["private_archive"]["bytes"] == 50540298
    assert r["private_archive"]["zip_members"] == 4394
    assert r["private_archive"]["private_library_uploaded"] is False
    assert r["full_60_map_180_frame_private_receipt_sha256"] == "abb8370abb0bbd17029b844ca6484ea188863b924ff647fd3d80e754ed2deefb"
    assert all(re.fullmatch("[0-9a-f]{64}", value) for value in (
        r["private_archive"]["sha256"], r["full_60_map_180_frame_private_receipt_sha256"]))
    assert r["stage_A"] == "7_PARTIAL_2_OPEN" and r["stage_B"] == r["wiki"] == "GATED"
    assert r["overall_percent"] is None and r["R79"] == "PAUSED_NON_BLOCKING"
    assert all(v is False for v in r["unverified"].values())
    for name, item in r["maps"].items():
        prior = floors[name + ".dat"]
        gap = excluded[name + ".dat"]
        assert item["source_DAT_sha256"] == prior["source_full_file_SHA256"]
        assert item["source_DAT_bytes"] == prior["source_file_bytes"]
        assert item["original_grid"] == [prior["original_header_width"], prior["original_header_height"]]
        assert item["qualified_nonzero_numeric_positions_all_layers"] == prior["number_of_nonzero_positions_matching_source_qualified_TW1_RD"]
        assert item["low_value_unqualified_occurrences"] == prior["number_of_nonzero_positions_missing_source_qualified_TW1_RD"]
        assert item["low_value_unqualified_occurrences"] > 0
        assert item["has_unqualified_gt99_images"] is False
        assert item["low_value_semantics_open"] is True
        assert gap["unqualified_gt99_alias_occurrences"] == {}
    unmatched = {a[0]:a[2] for a in i["unmatched_numeric_alias_rows"]}
    for key, count, status in (
        ("15999",6107,"LATER_MULTIPLE_ADRN_RECORDS_INDEX_ONLY"),
        ("9440",4833,"LATER_UNIQUE_ADRN_INDEX_ONLY"),
        ("3150",4760,"UNMAPPED_BOTH_SAVED_TW1_AND_LATER_ADRN_INDEXES"),
        ("22413",4,"UNMAPPED_BOTH_SAVED_TW1_AND_LATER_ADRN_INDEXES"),
    ):
        row = r["focus_numeric_gaps"][key]
        assert row["source_occurrences"] == count == g["unqualified_gt99_alias_totals"][key]
        assert row["later_index_only_status"] == unmatched[int(key)] == status
        assert row["source_original_RD_verified"] is False
        assert row["map_files"] == sum(key in v["unqualified_gt99_alias_occurrences"] for v in excluded.values())
    assert sum(v["unqualified_gt99_occurrences"] for v in excluded.values()) == 29748
    return True

class Map10Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads((ROOT/A).read_bytes())
        cls.i = json.loads((ROOT/I).read_bytes())
        cls.g = json.loads((ROOT/G).read_bytes())
    def test_source_conservation(self): self.assertTrue(validate(self.r,self.i,self.g))
    def test_reject_drop_original_dat(self):
        r=copy.deepcopy(self.r);r["maps"].pop(next(iter(r["maps"])))
        with self.assertRaises(AssertionError): validate(r,self.i,self.g)
    def test_reject_source_hash_drift(self):
        r=copy.deepcopy(self.r);next(iter(r["maps"].values()))["source_DAT_sha256"]="0"*64
        with self.assertRaises(AssertionError): validate(r,self.i,self.g)
    def test_reject_original_client_promotion(self):
        r=copy.deepcopy(self.r);r["unverified"]["original_game_running"]=True
        with self.assertRaises(AssertionError): validate(r,self.i,self.g)
    def test_reject_low_value_semantics_promotion(self):
        r=copy.deepcopy(self.r);next(iter(r["maps"].values()))["low_value_semantics_open"]=False
        with self.assertRaises(AssertionError): validate(r,self.i,self.g)
    def test_reject_missing_rd_promotion(self):
        r=copy.deepcopy(self.r);r["focus_numeric_gaps"]["9440"]["source_original_RD_verified"]=True
        with self.assertRaises(AssertionError): validate(r,self.i,self.g)
    def test_reject_unverified_private_archive_library(self):
        r=copy.deepcopy(self.r);r["private_archive"]["private_library_uploaded"]=True
        with self.assertRaises(AssertionError): validate(r,self.i,self.g)
    def test_reject_unsupported_new_rd_decode(self):
        r=copy.deepcopy(self.r);r["new_60"]["new_original_RD_decodes"]=138
        with self.assertRaises(AssertionError): validate(r,self.i,self.g)

if __name__ == "__main__":
    unittest.main()
