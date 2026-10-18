import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "research/recovered/STONEAGE-CN80-JUDGMENT-NAMED-CONTENT-R1.json"
OLD = ROOT / "research/recovered/STONEAGE-CN80-PORTRAIT-QUEST-R1.json"

class Judgment2005EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(P.read_text(encoding="utf-8"))
        cls.portrait = json.loads(OLD.read_text(encoding="utf-8"))

    def test_sources_not_claimed_as_operator_records(self):
        d = self.data
        self.assertEqual(len(d["sources"]), 2)
        self.assertTrue(all(s["official_operator_source"] is False for s in d["sources"]))
        self.assertIsNone(d["sources"][0]["original_publication_timestamp"])
        self.assertTrue(all(s["byte_sha256"] is None for s in d["sources"]))
        self.assertFalse(d["publisher_patch_or_build_verified"])
        self.assertEqual(d["sources"][0]["timestamp_meaning"], "EDIT_LABEL_NOT_FIRST_PUBLICATION_OR_DEPLOYMENT")

    def test_upstream_repost_and_nonindependence(self):
        d = self.data
        self.assertEqual(d["sources"][0]["upstream_claim"], "出處OURSA")
        self.assertIn("INDEPENDENCE_UNPROVEN", d["sources"][1]["relationship_to_gamer"])
        self.assertTrue(any(x["conclusion"] == "NOT_TWO_INDEPENDENT_FIRST_PARTY_WITNESSES" for x in d["evidence_contrasts"]))

    def test_named_content_is_not_server_ids(self):
        d = self.data
        self.assertEqual(len(d["npc_roles_reported"]), 3)
        self.assertEqual(len(d["required_team_roles_reported"]), 3)
        self.assertEqual(len(d["prior_quest_requirements_reported"]), 2)
        self.assertTrue(all(v["actual_npc_id"] is None for v in d["npc_roles_reported"]))
        self.assertTrue(all(v["item_id"] is None for v in d["items_reported"]))
        self.assertTrue(all(v["floor_id"] is None for v in d["locations_reported"]))
        self.assertFalse(d["original_server_quest_script_verified"])
        self.assertFalse(d["tw10_same_build_verified"])

    def test_coordinates_are_integer_pairs_not_decimal_steps(self):
        d = self.data
        coords = [v for node in d["locations_reported"] for k, v in node.items() if k.endswith("_xy")]
        coords += [v for node in d["npc_roles_reported"] for k,v in node.items() if k.endswith("_xy")]
        self.assertGreaterEqual(len(coords), 7)
        self.assertTrue(all(isinstance(p,list) and len(p)==2 and all(type(n) is int for n in p) for p in coords))
        self.assertIn([38,28], coords)
        self.assertIn([94,48], coords)

    def test_portrait_dependency_not_silently_closed(self):
        d = self.data
        self.assertFalse(d["direct_portrait_prerequisite_edge_verified"])
        self.assertIsNone(self.portrait["prerequisites"]["stated_in_this_guide"])
        self.assertFalse(self.portrait["prerequisites"]["none_proven"])
        self.assertTrue(any(x["conclusion"] == "VERSION_RULE_CHANGE_UNPROVEN" for x in d["evidence_contrasts"]))

    def test_no_stage_or_historical_scope_promotion(self):
        d = self.data
        for field in ("first_party_game_rule_verified", "original_game_runtime_verified", "source_raw_html_retained", "graph_is_gameplay_implementation"):
            self.assertFalse(d[field])
        self.assertEqual(d["stage_a_family_status"], "7_PARTIAL_2_OPEN")
        self.assertEqual(d["stage_b"], "GATED")
        self.assertEqual(d["r79"], "PAUSED_NON_BLOCKING")
        self.assertEqual(d["next"], "ALL_OFFICIAL_VERSION_NAMED_CONTENT_SOURCE-01")

if __name__ == "__main__":
    unittest.main()
