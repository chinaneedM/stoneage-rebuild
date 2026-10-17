"""Fail if the Stage A priority checkpoint rewrites history or closes blockers."""
from __future__ import annotations
from copy import deepcopy
import json
import unittest

from tools.stoneage_stage_a_portfolio_checkpoint import REPORT, validate, GATES


class PortfolioCheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(REPORT.read_text(encoding="utf-8"))

    def test_eight_immutable_anchors_and_current_nine_gates(self):
        result=validate(self.data)
        self.assertEqual(result["status"],"PASS")
        self.assertEqual(result["pinned_sources"],8)
        self.assertEqual(self.data["system_gates"],GATES)

    def test_five_player_visible_primary_service_classes(self):
        result=validate(self.data)
        self.assertEqual(result["bounded_early_services"],5)
        self.assertEqual([x["id"] for x in self.data["early_service_journey_slices"]],
                         ["SAVE_POINT","MAMMOTH_BUS","VILLAGE_CARE_TRAINING","VILLAGE_WORK","GROUND_ITEM_EXPIRY"])

    def test_deny_forged_original_server_replay_and_stage_b(self):
        for key in ("original_1999_service_build_proven","same_version_tw10_service_binding_proven",
                    "original_server_transaction_or_ack_observed","actual_visual_screen_or_route_replayed",
                    "original_npc_quest_script_recovered","stage_a_accepted",
                    "joint_user_review_completed","stage_b_started"):
            with self.subTest(key=key):
                a=deepcopy(self.data)
                a[key]=True
                with self.assertRaises(ValueError):
                    validate(a)

    def test_reject_false_bus_or_durability(self):
        a=deepcopy(self.data)
        a["early_service_journey_slices"][0]["original_tw10_service_binding"]="PROVEN"
        with self.assertRaisesRegex(ValueError,"same-game inferred"):
            validate(a)
        a=deepcopy(self.data)
        a["early_service_journey_slices"][0]["missing_original_inputs"]=["unknown"]
        with self.assertRaisesRegex(ValueError,"savepoint durability"):
            validate(a)

    def test_reject_false_exact_version_and_missing_source(self):
        a=deepcopy(self.data)
        a["source_pins"]["early_manual"]["git_blob"]="0"*40
        with self.assertRaisesRegex(ValueError,"source mutation"):
            validate(a)
        a=deepcopy(self.data)
        a["early_service_journey_slices"][1]["manual_section"]="20010418"
        with self.assertRaisesRegex(ValueError,"unanchored section"):
            validate(a)

    def test_reject_scope_and_priority_drift(self):
        a=deepcopy(self.data)
        a["next_priority"]="NPC-FULL-SCAN"
        with self.assertRaisesRegex(ValueError,"NEXT drift"):
            validate(a)
        a=deepcopy(self.data)
        a["overall_percent"]=85
        with self.assertRaisesRegex(ValueError,"completion percentage"):
            validate(a)

    def test_unavailable_original_world_and_two_open_families(self):
        self.assertEqual([x for x,v in self.data["system_gates"].items() if v=="OPEN"],
                         ["npc_quests","runtime_persistence"])
        self.assertFalse(self.data["historical_quest_server_files_added"])
        self.assertFalse(self.data["production_engine_changes"])
        self.assertEqual(self.data["savedata_r79"],"PAUSED_NON_BLOCKING")

    def test_reject_r79_and_unbounded_research(self):
        a=deepcopy(self.data)
        a["savedata_r79"]="ACTIVE"
        with self.assertRaisesRegex(ValueError,"R79 reopened"):
            validate(a)
        a=deepcopy(self.data)
        a["portfolio_reassessment_trigger"]["stop_if_no_material_outcome"]=False
        with self.assertRaisesRegex(ValueError,"no stop rule"):
            validate(a)


if __name__=="__main__":
    unittest.main()
