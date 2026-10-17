"""Synthetic adversarial evidence/promotion tests for early source gap triage."""
import copy
import json
import unittest
from tools.stoneage_stage_a_early_source_gap_triage import REPORT,validate

class EarlyGapTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet=json.loads(REPORT.read_text(encoding="utf-8"))

    def test_accepted_bounded_packet(self):
        got=validate(self.packet)
        self.assertEqual(got["finite_services"],5)
        self.assertEqual(got["new_original_values"],0)

    def test_false_1999_and_tw10_promotion_fails(self):
        for name in ("original_1999_membership_proven",
                     "original_tw10_same_build_service_execution_proven",
                     "commercial_server_durable_ack_proven",
                     "whole_stage_a_accepted","stage_b_started"):
            bad=copy.deepcopy(self.packet);bad[name]=True
            with self.subTest(name=name),self.assertRaises(ValueError):
                validate(bad)

    def test_cannot_claim_negative_global_web_search(self):
        for name in ("exhaustive_global_search","source_unavailable_worldwide_claim",
                     "new_raw_source_verified","new_original_game_value_obtained"):
            bad=copy.deepcopy(self.packet);bad["public_discovery"][name]=True
            with self.subTest(name=name),self.assertRaises(ValueError):
                validate(bad)

    def test_archive_access_error_cannot_be_recast_as_absence(self):
        bad=copy.deepcopy(self.packet)
        bad["public_discovery"]["routes"][-1]["result"]="SOURCE_DOES_NOT_EXIST"
        with self.assertRaisesRegex(ValueError,"archive reader error"):
            validate(bad)

    def test_pin_or_original_value_tampering_rejected(self):
        bad=copy.deepcopy(self.packet);bad["source_pins"]["manual"]["blob"]="0"*40
        with self.assertRaises(ValueError):
            validate(bad)
        bad=copy.deepcopy(self.packet);bad["gaps"][0]["verified_original_value"]=0
        with self.assertRaisesRegex(ValueError,"invented original"):
            validate(bad)

    def test_no_silent_drop_or_fake_service_resolution(self):
        bad=copy.deepcopy(self.packet);bad["gaps"].pop()
        with self.assertRaises(ValueError):
            validate(bad)
        bad=copy.deepcopy(self.packet);bad["gaps"][1]["same_build_service_binding"]="PROVEN"
        with self.assertRaises(ValueError):
            validate(bad)

    def test_review_is_not_stage_b_start(self):
        bad=copy.deepcopy(self.packet)
        bad["portfolio_decision"]["NEXT_REQUIRES_USER_ACCEPTANCE"]=False
        with self.assertRaisesRegex(ValueError,"implicit stage promotion"):
            validate(bad)

if __name__=="__main__":
    unittest.main()
