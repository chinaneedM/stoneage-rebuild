"""Public O30 derived source boundaries and existing later WarpWatch contract.

Browser/private-art acceptance is NOT replayed in this source-only CI.
"""
import json
from pathlib import Path
import unittest
from tools.stoneage_warp_transition_model import overlap_warp_triggered

FILE = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-O30-OVERLAP-WARP-INTERACTION-R1.json"


class O30OverlapWarpContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = json.loads(FILE.read_text(encoding="utf-8"))

    def test_paired_static_source_coordinates(self):
        self.assertEqual(self.p["warp_pair"], [
            {"source": [1000,63,99], "target":[1001,10,15]},
            {"source": [1001,10,15], "target":[1000,63,99]},
        ])

    def test_real_dat_event_field_is_not_warp_classifier(self):
        event = self.p["event_field_crosscheck"]
        self.assertEqual({
            event["map1000_warp_source"], event["map1000_neighbor_y_plus_one"],
            event["map1001_warp_source"], event["map1001_neighbor_y_plus_one"],
        }, {49155})
        self.assertFalse(event["value_49155_is_exclusive_warp_indicator"])
        self.assertFalse(event["map_event_value_is_native_collision_decision"])

    def test_later_descendant_overlap_watch(self):
        self.assertTrue(overlap_warp_triggered(
            mover_is_player=True, action_is_walk=True,
            previous_xy=(63,100), event_xy=(63,99)))
        self.assertFalse(overlap_warp_triggered(
            mover_is_player=True, action_is_walk=True,
            previous_xy=(63,99), event_xy=(63,99)))
        self.assertFalse(overlap_warp_triggered(
            mover_is_player=False, action_is_walk=True,
            previous_xy=(63,100), event_xy=(63,99)))
        self.assertFalse(overlap_warp_triggered(
            mover_is_player=True, action_is_walk=False,
            previous_xy=(63,100), event_xy=(63,99)))

    def test_private_execution_claim_is_bounded(self):
        b=self.p["private_browser_execution"]
        self.assertEqual((b["checks_passed"],b["checks_total"]), (18,18))
        self.assertEqual((b["console_errors"],b["external_requests"]), (0,0))
        self.assertEqual(b["execution_surface"], "playwright page.set_content")
        self.assertTrue(self.p["private_custody"]["roundtrip_readback_sha256_verified"])
        self.assertFalse(self.p["public_git_original_proprietary_bytes_included"])

    def test_negative_evidence_guards(self):
        claimed=self.p["claims_not_proven"]
        required=("native_client_executable_started","original_server_executed",
                  "original_runtime_warp_observed","native_collision_or_pathfinding",
                  "tw1_same_deployment_NPC_DAT_warp_identity",
                  "walkable_source_route_verified","native_palette_ui_FPS",
                  "native_shop_purchase")
        self.assertTrue(all(claimed[x] is False for x in required))
        self.assertIsNone(self.p["overall_percent"])
        self.assertEqual(self.p["savedata_r79"], "PAUSED_NON_BLOCKING")

if __name__ == "__main__":
    unittest.main()
