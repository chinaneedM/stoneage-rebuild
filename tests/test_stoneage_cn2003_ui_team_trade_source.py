"""R57 portal-derived interface assertions, not first-generation runtime validation."""
import json
import pathlib
import unittest

P = pathlib.Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.json"

class TestCn2003UiTeamTradeSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(P.read_text(encoding="utf-8"))

    def test_scope_and_readable_web_only(self):
        x = self.d
        self.assertEqual(x["task"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-57")
        self.assertEqual(x["historical_attribution"], "LATER_RECOVERED")
        self.assertTrue(x["no_tw10_membership_assumed"])
        self.assertFalse(x["original_game_executed"])
        self.assertFalse(x["original_server_execution_observed"])
        self.assertEqual([s["id"] for s in x["sources"]], ["S1", "S2"])
        self.assertEqual([s["displayed_date"] for s in x["sources"]], ["2003-04-15 23:29", "2003-11-18 15:33"])
        for s in x["sources"]:
            self.assertIsNone(s["raw_html_sha256"])
            self.assertIsNone(s["raw_http_bytes"])
            self.assertFalse(s["source_bytes_replayed"])

    def test_twenty_source_bounded_interactions(self):
        a = self.d["guide_interactions"]
        self.assertEqual(len(a), 20)
        self.assertEqual([z["ordinal"] for z in a], list(range(1, 21)))
        self.assertEqual(len({z["id"] for z in a}), 20)
        self.assertTrue(all(z["source_id"] == "S1" for z in a))
        self.assertTrue(all(not z["original_tw10_verified"] for z in a))
        self.assertTrue(all(z["exact_client_build"] is None and z["original_server_config_id"] is None for z in a))
        self.assertEqual({z["id"] for z in a if z["domain"] == "npc_dialog_ui"}, {"NPC_FACE_AND_TEXT", "SIGN_FACE_CLICK", "TEAM_FACE_CONSENT"})

    def test_two_phase_trade_and_team_claim_only(self):
        a = {z["id"]: z for z in self.d["guide_interactions"]}
        self.assertIn("双方分别按OK", a["TRADE_DOUBLE_CONFIRM"]["paraphrase"])
        self.assertIn("队长负责移动", a["TEAM_LEADER_FOLLOW"]["paraphrase"])
        self.assertIn("五人", a["HELP_PARTY_LIMIT"]["paraphrase"])
        self.assertFalse(self.d["tensions"][2]["server_transaction_algorithm_verified"])

    def test_conflicts_not_silently_resolved(self):
        t = {z["id"]: z for z in self.d["tensions"]}
        self.assertEqual(len(t), 4)
        h = t["ITEM_HOTKEY_INTERNAL_CONFLICT"]
        self.assertIn("Ctrl+I", h["s1_first"])
        self.assertIn("Ctrl+L", h["s1_second"])
        self.assertIsNone(h["resolution"])
        self.assertTrue(h["do_not_silently_choose"])
        q = t["DIFFERENT_NAMED_VERSION_CONTEXTS"]
        self.assertFalse(q["same_exact_client_build_proven"])
        self.assertTrue(q["release_history_not_conflated"])

    def test_operator_message_not_original_release(self):
        a = {z["id"]: z for z in self.d["operator_news"]}
        self.assertEqual(len(a), 3)
        self.assertIn("2003-09-04", a["CN20_2003_09_04_SERVICE"]["assertion"])
        self.assertIn("最早上市", a["CN20_2003_09_04_SERVICE"]["not_equivalent_to"])
        self.assertIn("2003-11-19", a["CN20_2003_11_19_NEW_GROUP"]["assertion"])
        self.assertIn("更安全", a["CN20_SAFE_TRADE_UNSPECIFIED"]["assertion"])

    def test_negative_boundaries_all_preserved(self):
        self.assertTrue(all(self.d["negative_evidence_boundaries"].values()))
        self.assertEqual(self.d["next"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-58")

if __name__ == "__main__":
    unittest.main()
