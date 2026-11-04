"""INTEGRATION02: independently replay the published original DAT/RD source joins."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import unittest

R = Path(__file__).resolve().parents[1] / "research" / "recovered"
P = R / "STONEAGE-INTEGRATION02-ORIGINAL-SCENE-DAT-RD-CROSSMODULE-R1.json"
I = R / "STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json"
M2 = R / "STONEAGE-MAP-SCENE-MODULE-02-THREE-ORIGINAL-DAT-FLOOR-IMAGE-JOIN-R1.json"
M4 = R / "STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json"
M5 = R / "STONEAGE-MAP-SCENE-MODULE-05-SOURCE-WINDOW-OBSERVATION-R1.json"

def validate(p, i, m2, m4, m5):
    assert p["schema"] == "stoneage.integration_module02_original_DAT_TW10_RD_scene_source_crossmodule.r1"
    assert p["starting_main_commit"] == "8a5ee6a11c9e5228a24aab38a41273e6d6e858e9"
    assert p["prior_large_CURRENT_STATE_blob_unchanged"] == "c89e0e33537990aa2132b47c40fef49a985a935c"
    assert p["exact_original_source_Git_blobs"] == {
        "INTEGRATION01": "5e526512c0277e19ca41dfcd934c230404d1dfb4",
        "MAP02": "445b6f846ae3d541bcd3ff46bd916934a19171ec",
        "MAP04": "1ef8c004179128ea44ffa4fb4259748bc8c83911",
        "MAP05": "4e87533f9d3431632b0e8ccee50630679849141c",
    }
    assert "NOT_NATIVE_SAME_DEPLOYMENT" in p["original_source_boundary"]
    src = {int(x[0].split(".")[0]): x for x in m4["per_floor_source_rows"]}
    m5floor = {x["source_floor_id"]: x for x in m5["source_floors"]}
    gp = Counter(x["floor_id"] for x in i["source_GetPet_CREATE_QUEST_script_AND_floor_joins"])
    npc = Counter(x["floor_id"] for x in i["source_NPCEnemy_CREATE_ARG_floor_AND_candidate_enemy_ID_joins"])
    rows = p["per_floor_source_qualification"]
    floors = i["source_original_main_client_floor_files_with_disqualified_read_errors"]
    assert len(rows) == len(floors) == 60
    counters = Counter()
    gp_status = Counter()
    npc_status = Counter()
    n = covered = missing = 0
    for row, old in zip(rows, floors):
        f = old["floor_id"]
        assert row["floor_id"] == f
        assert row["source_GetPet_CREATE_refs"] == gp[f]
        assert row["source_NPCEnemy_CREATE_refs"] == npc[f]
        assert row["original_main_client_DAT_source_SHA256_if_success"] == (
            (old["original_main_client_DAT"] or {}).get("source_sha256"))
        assert row["original_main_client_MAP_source_SHA256_if_success"] == (
            (old["original_main_client_MAP"] or {}).get("source_sha256"))
        assert row["preserved_MAP01_extraction_error_rows"] == old["original_extractor_read_error_members"]
        assert row["original_mapset_master_membership_not_proven"] is True
        q = row["qualified_complete_original_DAT"]
        v = row["original_TW10_RD_pixel_candidate_join"]
        status = row["source_DAT_qualification"]
        if f in src:
            s = src[f]
            assert status == "MAP04_EXACT_DAT_FULL_SHA"
            assert old["original_main_client_DAT"] and s[2] == old["original_main_client_DAT"]["source_sha256"]
            assert q == {
                "original_dat_sha256": s[2], "source_bytes": s[1],
                "width": s[3], "height": s[4], "cells": s[5],
                "source_provenance": "SAME_MIXED25_ARCHIVE_MAIN_CLIENT_DAT"}
            assert v == {
                "reference_basis": "ORIGINAL_DAT_FIRST_TWO_PLANES_NONZERO_NUMERIC_OCCURRENCES",
                "nonzero_numeric_references": s[6]+s[7],
                "tw10_verified_RD_numeric_candidate_references": s[10],
                "unmatched_tw10_verified_RD_references": s[11],
                "tw10_verified_unique_aliases_in_source": s[8],
                "unmatched_tw10_unique_aliases_in_source": s[9],
                "provenance": "CROSS_CARRIER_ORIGINAL_LATER_MAP_TO_RETAIL_TW10_RD_NOT_SAME_DEPLOYMENT"}
            assert s[6]+s[7] == s[10]+s[11]
            n += s[6]+s[7]
            covered += s[10]
            missing += s[11]
            tag = "map04_sha_matched"
        elif str(f) in m2["source_three_floors"]:
            a = m2["source_three_floors"][str(f)]
            b = m5floor[f]
            assert status == "MAP02_INDEPENDENT_PRIOR_O31_DAT_SHA_WITH_MAP01_READ_FAILURE_RETAINED"
            assert f == 1000
            assert old["original_main_client_DAT"] is None
            assert old["original_extractor_read_error_members"]
            assert q == {
                "original_dat_sha256": a["dat_sha256"], "source_bytes": a["dat_bytes"],
                "width": a["width"], "height": a["height"], "cells": a["cells"],
                "source_provenance": "INDEPENDENT_VERIFIED_O31_ORIGINAL_DAT_NOT_RECLASSIFIED_MAP01_ERROR"}
            assert b["original_DAT_source_sha256"] == a["dat_sha256"]
            assert v == {
                "reference_basis": "ORIGINAL_DAT_FIRST_TWO_PLANES_NONZERO_NUMERIC_OCCURRENCES",
                "nonzero_numeric_references": b["first_two_plane_nonzero_numeric_references"],
                "tw10_verified_RD_numeric_candidate_references": b["MAP02_and_MAP04_real_RD_covered_references"],
                "unmatched_tw10_verified_RD_references": b["unmatched_reference_occurrences"],
                "unmatched_tw10_unique_aliases": b["unmatched_unique_aliases"],
                "provenance": "CROSS_CARRIER_O31_MAP02_MAP05_TO_RETAIL_TW10_RD_NOT_SAME_DEPLOYMENT"}
            assert v["nonzero_numeric_references"] == v["tw10_verified_RD_numeric_candidate_references"] + v["unmatched_tw10_verified_RD_references"]
            tag = "map02_independent"
        else:
            assert status == "COMPLETE_SOURCE_DAT_UNVERIFIED"
            assert q is None and v is None
            tag = "unqualified_complete_DAT"
        counters[tag] += 1
        gp_status[tag] += gp[f]
        npc_status[tag] += npc[f]
    s = p["summary"]
    assert (counters["map04_sha_matched"],counters["map02_independent"],counters["unqualified_complete_DAT"]) == (55,1,4)
    assert s["unique_NPC_or_GetPet_source_floors"] == 60
    assert s["map04_original_main_client_DAT_exact_SHA_floors"] == counters["map04_sha_matched"]
    assert s["map02_independent_DAT_original_SHA_floors"] == counters["map02_independent"]
    assert s["complete_original_DAT_unverified_floors"] == counters["unqualified_complete_DAT"]
    assert s["unverified_floor_ids"] == [100,200,3000,3021]
    assert s["GetPet_original_CREATE_refs"] == sum(gp.values()) == 24
    assert s["NPCEnemy_original_CREATE_refs"] == sum(npc.values()) == 279
    assert s["GetPet_CREATE_refs_by_DAT_qualification"] == dict(gp_status)
    assert s["NPCEnemy_CREATE_refs_by_DAT_qualification"] == dict(npc_status)
    assert (s["map04_55_floors_nonzero_first_two_plane_numeric_refs"],
            s["map04_55_floors_TW10_RD_candidate_matched_refs"],
            s["map04_55_floors_missing_TW10_RD_candidate_refs"]) == (n,covered,missing) == (400100,390351,9749)
    b = m5floor[1000]
    assert (s["map02_independent_1000_nonzero_first_two_plane_numeric_refs"],
            s["map02_independent_1000_TW10_RD_candidate_matched_refs"],
            s["map02_independent_1000_missing_TW10_RD_candidate_refs"]) == (
            b["first_two_plane_nonzero_numeric_references"],
            b["MAP02_and_MAP04_real_RD_covered_references"],
            b["unmatched_reference_occurrences"]) == (26324,26310,14)
    windows = p["previous_MAP05_source_window_observation_joins"]
    assert len(windows) == len(m5["observation_windows"]) == 5
    for x, w in zip(windows, m5["observation_windows"]):
        assert x == {
            "original_source_window": w["window"], "source_floor_id": w["floor"],
            "source_rect_inclusive": w["source_coordinate_rect"],
            "original_source_DAT_sha256": w["original_DAT_sha256"], "cells": w["cells"],
            "original_first_two_planes_nonzero_numeric_references": w["two_plane_numeric_nonzero_references"],
            "original_TW10_RD_candidate_source_covered_references": w["source_qualified_RD_covered_in_union"],
            "original_TW10_RD_candidate_unmatched_references": w["source_unmatched_references"],
            "original_TW10_RD_candidate_unmatched_aliases": w["unmatched_aliases"],
            "original_TW10_RD_candidate_unmatched_per_alias": w["unmatched_references_per_alias"],
            "in_INTEGRATION01_NPC_quest_floor_cohort": w["floor"] in {r["floor_id"] for r in floors},
            "qualified_prior_private_pixel_observation_MAP05_only": True,
            "historical_native_layer_palette_collision_and_game_execution_proven": False}
    assert (s["map05_prior_private_source_observation_windows"],
            s["map05_windows_on_INTEGRATION01_floor"],
            s["map05_windows_not_in_INTEGRATION01_floor"]) == (5,4,1)
    for k,v in p["bounds"].items():
        if k.startswith("original_") or k.startswith("source_proprietary_"):
            assert v is False, (k,v)
    assert p["bounds"]["overall_percent"] is None
    assert p["bounds"]["stage_A"] == "7PARTIAL_2OPEN"
    assert p["next"].startswith("INTEGRATION-MODULE-03_")

class Integration02SourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = json.loads(P.read_text())
        cls.i = json.loads(I.read_text())
        cls.m2 = json.loads(M2.read_text())
        cls.m4 = json.loads(M4.read_text())
        cls.m5 = json.loads(M5.read_text())

    def check(self, p):
        validate(p,self.i,self.m2,self.m4,self.m5)

    def test_exact_original_source_replay(self):
        self.check(self.p)

    def test_reject_different_DAT_with_same_numeric_floor_name(self):
        p=deepcopy(self.p)
        p["per_floor_source_qualification"][0]["qualified_complete_original_DAT"]["original_dat_sha256"]="0"*64
        with self.assertRaises(AssertionError):self.check(p)

    def test_reject_promotion_of_MAP01_extraction_failure(self):
        p=deepcopy(self.p)
        r=next(x for x in p["per_floor_source_qualification"] if x["floor_id"]==1000)
        r["preserved_MAP01_extraction_error_rows"]=[]
        with self.assertRaises(AssertionError):self.check(p)

    def test_reject_claim_of_native_original_renderer(self):
        p=deepcopy(self.p)
        p["bounds"]["original_native_renderer_layers_palette_offsets_proven"]=True
        with self.assertRaises(AssertionError):self.check(p)

    def test_reject_1001_window_as_NPC_quest_static_source(self):
        p=deepcopy(self.p)
        p["previous_MAP05_source_window_observation_joins"][-1]["in_INTEGRATION01_NPC_quest_floor_cohort"]=True
        with self.assertRaises(AssertionError):self.check(p)

if __name__=="__main__":
    unittest.main()
