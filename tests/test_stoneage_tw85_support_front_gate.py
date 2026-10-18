import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research/recovered/STONEAGE-TW85-SUPPORT-FRONT-GUIDE-GATE-R1.json"

class SupportFrontWitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DATA.read_text(encoding="utf-8"))

    def test_firstparty_gate_remains_unresolved(self):
        d = self.d
        self.assertEqual(d["original_operator_source_status"], "OPEN_EVIDENCE_LIMITED_NO_AUTHENTICATED_2006_FIRST_PARTY_TASK_SCRIPT")
        self.assertFalse(d["material_search"]["historical_official_patch_or_client_quest_verified"])
        self.assertIsNone(d["material_search"]["official_quest_NPC_or_reward_table_sha256"])
        self.assertEqual(d["material_search"]["official_2006_snapshot_access"], "WEB_READER_UNAVAILABLE_FOR_REQUESTED_20060623_REPLAY_NOT_NEGATIVE_EXISTENCE_PROOF")
        self.assertFalse(d["scope"]["is_tw10_original"])
        self.assertFalse(d["scope"]["original_server_recovered"])

    def test_date_is_page_edit_not_publisher_start(self):
        s = self.d["sources"][0]
        self.assertEqual(s["displayed_edit_time"], "2006-06-23 19:00:09")
        self.assertEqual(s["date_kind"], "CURRENT_PAGE_EDIT_FIELD_NOT_ORIGINAL_PUBLICATION_OR_RUNTIME")
        self.assertIsNone(s["original_html_sha256"])
        self.assertFalse(s["original_2006_web_capture_verified"])
        self.assertFalse(s["independent_original_author_verified"])

    def test_bounded_named_npc_and_two_distinct_deliveries(self):
        a = self.d["guide_relationships"]
        self.assertEqual([x["step"] for x in a], [1, 2, 3, 4, 5])
        self.assertEqual([a[i]["npc"] for i in (0,3,4)], ["伊秋娜", "奏敷", "布克瑟"])
        self.assertEqual(a[0]["claimed_free_item_slots"], 12)
        self.assertEqual(a[0]["supply_kinds"]*a[0]["supply_each"], 12)
        self.assertEqual(a[0]["minimum_each_on_delivery"],4)
        self.assertEqual(a[3]["receives"],"前線包裹")
        self.assertEqual(a[4]["consumes"],"前線包裹")
        self.assertFalse(a[3]["exact_transaction_verified"])
        self.assertFalse(a[4]["exact_transaction_verified"])
        self.assertIsNone(a[4]["reward_id"])

    def test_coordinates_are_two_integers_not_decimal_steps(self):
        coords=[]
        for step in self.d["guide_relationships"]:
            coords.extend(v for k,v in step.items() if k.endswith("_xy"))
            coords.extend(step.get("reported_route",[]))
        self.assertGreaterEqual(len(coords), 18)
        self.assertTrue(all(isinstance(v,list) and len(v)==2 and all(type(x) is int for x in v) for v in coords))
        self.assertIn([303,130],coords)
        self.assertIn([114,309],coords)
        self.assertIsNone(self.d["guide_relationships"][1]["map_id"])

    def test_approximate_battle_count_not_server_exact(self):
        x=self.d["guide_relationships"][1]
        self.assertEqual(x["approximate_guard_fights"],10)
        self.assertFalse(x["exact_fight_count_verified"])
        self.assertIsNone(self.d["quest"]["server_flag"])
        self.assertIsNone(self.d["quest"]["party_member_rule"])

    def test_later_wiki_variants_not_silently_corrected(self):
        d=self.d
        self.assertEqual(len(d["later_wiki_variants"]),4)
        for v in d["later_wiki_variants"]:
            self.assertEqual(v["resolution"], "UNKNOWN" if "coordinates" in v["field"] else "UNVERIFIED_NOT_INFERRED_IN_2006")
        self.assertEqual(d["later_wiki_variants"][0]["period_edited_guide_xy"],[21,27])
        self.assertEqual(d["later_wiki_variants"][0]["later_wiki_xy"],[20,27])
        self.assertFalse(d["sources"][2]["is_independent_2006_source"])

    def test_player_advice_is_not_official_gameplay(self):
        x=self.d["supporting_player_advice"]
        self.assertEqual(x["kind"],"PLAYER_WORKAROUND_NOT_OFFICIAL_BEHAVIOR")
        self.assertTrue(x["mentions_logout_during_combat"])
        self.assertFalse(x["server_behavior_or_safety_verified"])

    def test_stage_and_rights_gate(self):
        d=self.d
        self.assertEqual(d["stage_a"],"7_PARTIAL_2_OPEN")
        self.assertEqual(d["stage_b"],"GATED")
        self.assertEqual(d["r79"],"PAUSED_NON_BLOCKING")
        self.assertFalse(d["copyrighted_game_assets_embedded"])
        self.assertEqual(d["dedicated_ci_interpretation"],"STRUCTURAL_CONTRACT_ONLY_NOT_ORIGINAL_SOURCE_BYTES")
        self.assertEqual(d["next"],"ALL_OFFICIAL_VERSIONS_NEW_NAMED_FIRSTPARTY_DOMAIN-01")

if __name__ == "__main__":
    unittest.main()
