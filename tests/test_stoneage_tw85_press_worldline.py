import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/"research/recovered/STONEAGE-TW85-PERIOD-PRESS-WORLDLINE-R1.json"

class Taiwan85PressWorldline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DATA.read_text(encoding="utf-8"))
        cls.s = {x["id"]:x for x in cls.d["sources"]}

    def test_press_is_not_operator_script(self):
        self.assertEqual(len(self.d["sources"]), 3)
        self.assertTrue(all(not x["original_publisher_page"] for x in self.s.values()))
        self.assertEqual(self.s["17173_20060622"]["source_family"], "BAHAMUT_REPORT")
        self.assertFalse(self.s["17173_20060622"]["independent_from_gnn"])
        self.assertIsNone(self.d["independent_source_count_verified"])
        self.assertTrue(all(s["raw_sha256"] is None for s in self.s.values()))

    def test_story_does_not_bridge_80_or_10(self):
        story = self.d["named_story"]
        self.assertEqual(story["continuity_claim"]["from"], "7.5 精靈的召喚")
        self.assertEqual(story["continuity_claim"]["to"], "8.5 魔域大冒險")
        self.assertFalse(story["continuity_claim"]["bridges_80_explicitly"])
        self.assertFalse(story["continuity_claim"]["canonical_unified_timeline_proven"])
        self.assertIn({"from":"雷爾","relation":"SUBORDINATE_OF","to":"艾巴登"}, story["causal_links"])
        self.assertFalse(story["original_story_script_verified"])
        self.assertIsNone(story["character_npc_ids"])

    def test_one_source_names_quest_and_ids_open(self):
        q = self.d["named_quest"]
        self.assertEqual(q["as_written"], "支援前線")
        self.assertEqual(q["attested_by"], ["GAMEZONE_20060621"])
        self.assertIsNone(q["quest_script_id"])
        self.assertIsNone(q["item_table"])
        self.assertFalse(q["actual_rewards_verified"])
        self.assertTrue(q["absence_from_gnn_excerpt_does_not_disprove"])

    def test_planned_not_real_rollout(self):
        d = self.d["release_schedule"]
        self.assertEqual(d["early_server"], "蒼龍")
        self.assertFalse(d["actually_deployed_proven"])
        self.assertIsNone(d["original_client_sha256"])
        self.assertFalse(self.d["promoted_content"]["daily_persistence_proven"])
        self.assertIsNone(self.d["promoted_content"]["map_floor_ids"])

    def test_status_and_rights(self):
        self.assertFalse(self.d["archived_source_html"])
        self.assertFalse(self.d["proprietary_art_in_git"])
        self.assertEqual(self.d["stage_a"], "7_PARTIAL_2_OPEN")
        self.assertEqual(self.d["stage_b"], "GATED")
        self.assertEqual(self.d["r79"], "PAUSED_NON_BLOCKING")
        self.assertEqual(self.d["next"], "TW85_NAMED_QUEST_FIRSTPARTY_MATERIAL_GATE-01")

    def test_first_403_attempt_is_retained_as_failed_attempt(self):
        d=self.d["first_source_replay_attempt"]
        self.assertEqual(d["run_id"],39132023657)
        self.assertEqual(d["job_id"],117688962061)
        self.assertEqual(d["http_status"],403)
        self.assertEqual(d["conclusion"],"failure")
        self.assertIsNone(d["raw_sha256"])
        self.assertTrue(d["preserve_failed_attempt"])

    def test_runner_script_has_no_proprietary_writes(self):
        txt=(ROOT/"tools/stoneage_tw85_press_replay.py").read_text(encoding="utf-8")
        self.assertIn('SOURCE_STATUS=',txt)
        self.assertIn("raw_html_archived",txt)
        self.assertNotIn("raw_html.write",txt)

if __name__ == "__main__":
    unittest.main()
