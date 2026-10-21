"""R58 bounded 2002 player quest guides, not original game script execution."""
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2002-QUEST-WORLDLINE-SOURCE-R1.json"

class TestCn2002QuestWorldlineSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_provenance_no_server_promotion(self):
        d = self.d
        self.assertEqual(d["task"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-58")
        self.assertEqual([s["id"] for s in d["sources"]], ["S1", "S2"])
        self.assertEqual([s["date_as_page"] for s in d["sources"]], ["2002-09-16", "2002-12-17"])
        self.assertIsNone(d["sources"][1]["source_named_version"])
        for s in d["sources"]:
            self.assertIsNone(s["original_raw_html_sha256"])
            self.assertFalse(s["source_raw_bytes_archived"])
        self.assertTrue(all(v is False or v is None for v in d["source_replay"].values()))

    def test_guide_tasks_bounded(self):
        rows = self.d["s1_4_0_quest_gates"]
        self.assertEqual(len(rows), 12)
        self.assertEqual([r["row"] for r in rows], list(range(1, 13)))
        self.assertEqual(len({r["task_id"] for r in rows}), 12)
        self.assertTrue(all(not r["same_build_server_config_verified"] and not r["original_tw10_quest_presence_verified"] for r in rows))
        d = {r["task_id"]: r for r in rows}
        self.assertEqual(d["SKY_ISLAND"]["guide_min_level"], 30)
        self.assertEqual(d["GOLDEN_FLIGHT"]["guide_min_level"], 81)
        self.assertEqual(d["FIRE_WARRIOR"]["guide_prerequisite_task_ids"], ["FIRE_RITUAL"])
        self.assertEqual(d["RIRARA"]["guide_item_requirements"], ["MYSTERIOUS_SHELL"])
        self.assertEqual(d["WATER_MONSTER"]["guide_min_level"], 91)
        self.assertIn("PET_REBIRTH", d["RIRARA"]["guide_prerequisite_task_ids"])

    def test_eight_story_nodes_remain_source_claim(self):
        n = self.d["s2_mechanical_civilization_story_beats"]
        self.assertEqual(len(n), 8)
        self.assertEqual([x["sequence"] for x in n], list(range(1, 9)))
        self.assertTrue(all(x["source_id"] == "S2" and not x["original_server_script_proven"] for x in n))
        self.assertTrue(all(not x["canonical_story_worldline_proven"] for x in n))
        self.assertTrue(any("五次转生" in x["named_entities"] for x in n))
        self.assertTrue(any("四属性" in x["named_entities"] for x in n))

    def test_six_negative_cases(self):
        q = {x["kind"]: x for x in self.d["boundary_cases"]}
        self.assertEqual(len(q), 6)
        level = q["SKY_ACCEPT_VS_RECOMMEND"]
        self.assertEqual((level["entry_level"], level["recommended_level"]), (30, 80))
        self.assertFalse(level["hard_four_cave_gate_justified"])
        black = q["BLACK_TIGER_START_VS_FINISH"]
        self.assertEqual((black["older_guide_level"], black["reported_changed_completion_level"]), (91,101))
        self.assertIsNone(black["verified_patch_version"])
        self.assertFalse(q["RIRARA_BETWEEN_VERSION_CHANGE"]["independent_official_patch_notes"])
        self.assertFalse(q["SHELL_CROSSSOURCE_SHARED_NAME"]["same_original_item_master_id_verified"])
        self.assertFalse(q["S1_TO_S2_SAME_BUILD_UNPROVEN"]["same_exact_version_or_server_build"])

    def test_r55_join_remains_name_only(self):
        c = self.d["previous_derived_crosswalk"]
        self.assertEqual(c["task"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-55")
        self.assertEqual(c["source_path"], "research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.json")
        self.assertIn("SHARED_SHELL_NAME_ONLY", c["relation"])

    def test_no_false_completion(self):
        self.assertTrue(all(not v for v in self.d["negative_claims"].values()))
        self.assertEqual(self.d["next"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-59")
        self.assertEqual(len(self.d["s1_4_0_quest_gates"]), 12)
        self.assertEqual(len(self.d["s2_mechanical_civilization_story_beats"]), 8)

    def test_source_receipt_matches_raw_bytes(self):
        import hashlib
        p = SOURCE.parent / "STONEAGE-CN2002-QUEST-WORLDLINE-ACCEPTANCE-R1.json"
        r = json.loads(p.read_text(encoding="utf-8"))
        b = SOURCE.read_bytes()
        info = r["source_derived"]
        self.assertEqual(len(b), info["utf8_byte_length"])
        self.assertEqual(hashlib.sha256(b).hexdigest(), info["raw_sha256"])
        self.assertEqual(info["git_blob_sha1"], "5026707c16e0fdc306daf188739dcd75cb79b8b5")
        self.assertTrue(info["persisted_in_git"])
        self.assertFalse(info["contains_original_html_or_game_assets"])
        self.assertEqual(r["candidate_validation"]["artifact_count"], 0)
        self.assertEqual(r["main_validation"]["artifact_count"], 0)
        self.assertEqual(r["candidate_validation"]["tested_checks"], 6)
        self.assertEqual(r["main_validation"]["tested_checks"], 6)
        self.assertTrue(r["old_history_prefix_preserved"])
        self.assertTrue(r["source_scope_not_advanced_by_ci"])
        self.assertTrue(all(s["original_http_sha256"] is None and not s["source_archive_replay"] for s in r["web_sources"]))


if __name__ == "__main__":
    unittest.main()
