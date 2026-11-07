"""INTEGRATION05 original GetPet CREATE → QUEST05 actual DAT provenance and coverage.
Read-only derived metadata tests; no original proprietary scripts, images or runtime.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "research/recovered/STONEAGE-INTEGRATION05-GETPET-QUEST-MAP-ORIGINAL-SOURCE-GRAPH-R1.json"


def git_blob_sha(payload):
    return hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload).hexdigest()


def source_read(report):
    data = {}
    for name, pin in report["prior_qualified_public_source_blobs"].items():
        payload = (ROOT / pin["path"]).read_bytes()
        assert git_blob_sha(payload) == pin["sha"], name
        data[name] = json.loads(payload)
    return data


def verify(report, src):
    assert report["schema"] == "stoneage.integration05.GetPet_original_CREATE_script_item_floor_to_qualified_DAT_map_source.r1"
    assert report["baseline_main_head"] == "253da64e4d1e726e89a4389c17dc5a0baf8eabfe"
    assert report["historical_CURRENT_blob_untouched"] == "c89e0e33537990aa2132b47c40fef49a985a935c"
    i1, i2, q, i4 = (src[x] for x in ["integration01", "integration02", "quest05", "integration04"])
    assert report["source_RAR_sha256"] == q["source_original_mixed25_RAR_sha256"] == i1["source_original_mixed25_RAR_identity"]["sha256"]
    qcreate = {(x["source_CREATE_file"], x["source_CREATE_block_ordinal"]): x
               for x in q["source_CREATE_references"] if x["cohort"] == "QUEST01"}
    floors = {x["floor_id"]: x for x in i2["per_floor_source_qualification"]}
    scripts = {x["script_path"]: x for x in i1["source_GetPet_distinct_QUEST_script_item_number_source_catalog"]}
    expected = {}
    for x in i1["source_GetPet_CREATE_QUEST_script_AND_floor_joins"]:
        key = (x["original_CREATE_file"], x["original_CREATE_ordinal"])
        assert key not in expected
        qc = qcreate[key]
        floor = floors[x["floor_id"]]
        script = scripts[x["script_path"]]
        assert qc["source_parameter_file"] == x["script_path"]
        assert qc["source_parameter_sha256"] == x["script_original_sha256"] == script["source_file_sha256"]
        assert qc["source_floor_id"] == x["floor_id"]
        if qc["source_DAT_sha256"] is not None:
            assert qc["source_DAT_sha256"] == floor["qualified_complete_original_DAT"]["original_dat_sha256"]
        if qc["map_status"] == "MAP09_GT99_RD_SOURCE_READY_CANDIDATE":
            grade = "DAT_SHA_MATCH_MAP09_VISIBLE_CANDIDATE"
        elif qc["map_status"] == "DAT_PRESENT_GT99_QUALIFIED_RD_MISSING":
            grade = "DAT_SHA_MATCH_GT99_RD_MISSING"
        else:
            assert qc["map_status"] == "NO_MATCHING_DAT_IN_955"
            grade = ("INDEPENDENT_VERIFIED_DAT_1000_NOT_IN_955" if
                     floor["source_DAT_qualification"].startswith("MAP02_") else
                     "SOURCE_DAT_NOT_QUALIFIED")
        if grade == "SOURCE_DAT_NOT_QUALIFIED":
            assert floor["qualified_complete_original_DAT"] is None
        qualified = floor["qualified_complete_original_DAT"]
        expected[key] = {
            "source_CREATE_file": x["original_CREATE_file"],
            "source_CREATE_block_ordinal": x["original_CREATE_ordinal"],
            "source_CREATE_block_sha256": x["source_CREATE_block_sha256"],
            "source_QUEST05_whole_CREATE_sha256": qc["source_CREATE_sha256"],
            "source_script_path": x["script_path"],
            "source_script_original_sha256": x["script_original_sha256"],
            "source_floor_id": x["floor_id"],
            "source_quest_origin_class": "ORIGIN_UNRESOLVED",
            "original_GetPet_commands_source_lines": x["source_GETPET_command_lines"],
            "original_GetPet_numeric_literals_ordered": x["source_GETPET_numeric_literals_ordered"],
            "source_script_item_candidate_numeric_ids": script["distinct_source_item_numeric_candidates"],
            "source_script_item_numeric_occurrences": script["source_item_number_occurrences"],
            "Q05_955_map_status": qc["map_status"],
            "qualifying_DAT_grade": grade,
            "qualifying_source_DAT_sha256": qualified["original_dat_sha256"] if qualified else None,
            "qualifying_source_DAT_bytes": qualified["source_bytes"] if qualified else None,
            "floor_has_prior_DAT_read_errors": bool(floor["preserved_MAP01_extraction_error_rows"]),
            "source_visual_native_rendering_verified": False,
            "original_GetPet_command_reward_actually_delivered": False,
        }
    actual = {(x["source_CREATE_file"], x["source_CREATE_block_ordinal"]): x for x in report["rows"]}
    assert len(actual) == len(report["rows"]) == len(expected) == 24
    assert actual == expected
    counts = dict(Counter(x["qualifying_DAT_grade"] for x in actual.values()))
    assert counts == {
        "DAT_SHA_MATCH_MAP09_VISIBLE_CANDIDATE": 16,
        "DAT_SHA_MATCH_GT99_RD_MISSING": 5,
        "SOURCE_DAT_NOT_QUALIFIED": 2,
        "INDEPENDENT_VERIFIED_DAT_1000_NOT_IN_955": 1,
    }
    s = report["summary"]
    assert s["original_GetPet_source_CREATE_refs"] == 24
    assert s["original_distinct_scripts"] == len({x["source_script_path"] for x in actual.values()}) == 23
    assert s["original_distinct_floor_ids"] == len({x["source_floor_id"] for x in actual.values()}) == 19
    literals = {v for row in actual.values() for v in row["original_GetPet_numeric_literals_ordered"]}
    assert s["original_distinct_GetPet_numeric_literals"] == len(literals) == 36
    assert s["original_QUEST01_GetPet_script_item_candidate_distinct_numeric_ids"] == len(
        i1["source_GetPet_QUEST_scripts_item_numeric_candidate_two_itemset_receipts"]) == 101
    assert s["source_qualified_DAT_grade_counts"] == counts
    independent = [x for x in actual.values() if x["qualifying_DAT_grade"] == "INDEPENDENT_VERIFIED_DAT_1000_NOT_IN_955"]
    assert len(independent) == 1
    assert independent[0]["source_floor_id"] == s["map02_independent_1000_source_floor_id"] == 1000
    assert independent[0]["qualifying_source_DAT_sha256"] == s["map02_independent_1000_source_DAT_sha256"]
    assert s["unqualified_floor_ids"] == sorted({
        x["source_floor_id"] for x in actual.values() if x["qualifying_DAT_grade"] == "SOURCE_DAT_NOT_QUALIFIED"
    }) == [100, 3000]
    compiled = sorted(x["compiled_capture_work_key_53"] for x in i4["rows"])
    assert s["compiled_capture_keys_of_INTEGRATION04"] == compiled
    assert s["GetPet_literal_numeric_overlap_with_INTEGRATION04_compiled_capture_keys"] == sorted(literals.intersection(compiled)) == []
    b = report["evidence_boundaries"]
    for key, value in b.items():
        if key == "overall_percent":
            assert value is None
        elif key == "stage_A":
            assert value == "7_PARTIAL_2_OPEN"
        elif key == "stage_B_wiki":
            assert value == "GATED"
        elif key == "R79":
            assert value == "PAUSED_NON_BLOCKING"
        else:
            assert value is False, key


class Integration05CrossModuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(TARGET.read_text(encoding="utf-8"))
        cls.sources = source_read(cls.report)

    def run_check(self, bad):
        with self.assertRaises(AssertionError):
            verify(bad, self.sources)

    def test_original_source_join_and_full_population(self):
        verify(self.report, self.sources)

    def test_reject_1000_missing_even_with_independent_DAT(self):
        bad = deepcopy(self.report)
        row = next(x for x in bad["rows"] if x["source_floor_id"] == 1000)
        row["qualifying_DAT_grade"] = "SOURCE_DAT_NOT_QUALIFIED"
        self.run_check(bad)

    def test_reject_100_missing_DAT_imagined(self):
        bad = deepcopy(self.report)
        row = next(x for x in bad["rows"] if x["source_floor_id"] == 100)
        row["qualifying_source_DAT_sha256"] = "0" * 64
        self.run_check(bad)

    def test_reject_wrong_source_CREATE_block_or_whole_file_sha(self):
        bad = deepcopy(self.report)
        bad["rows"][0]["source_QUEST05_whole_CREATE_sha256"] = "0" * 64
        self.run_check(bad)

    def test_reject_dropped_duplicate_GetPet_numeric_token(self):
        bad = deepcopy(self.report)
        row = next(x for x in bad["rows"] if x["source_floor_id"] == 3000)
        row["original_GetPet_numeric_literals_ordered"].pop()
        self.run_check(bad)

    def test_reject_claim_2D_map_ready_as_native_game_render(self):
        bad = deepcopy(self.report)
        bad["rows"][0]["source_visual_native_rendering_verified"] = True
        self.run_check(bad)

    def test_reject_promoted_event_as_historical_operated_festival(self):
        bad = deepcopy(self.report)
        bad["rows"][0]["source_quest_origin_class"] = "OPERATED_FESTIVAL"
        self.run_check(bad)

    def test_reject_confused_GetPet_script_literal_with_compiled_capture_key(self):
        bad = deepcopy(self.report)
        bad["summary"]["GetPet_literal_numeric_overlap_with_INTEGRATION04_compiled_capture_keys"] = [524]
        self.run_check(bad)


if __name__ == "__main__":
    unittest.main()
