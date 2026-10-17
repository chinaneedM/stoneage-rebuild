"""Synthetic negative cases for five first-party village service descriptions."""
from copy import deepcopy
import json
import unittest

from tools.stoneage_early_village_service_journey import (
    DEFAULT, claim_result, validate,
)


class VillageServiceJourneyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(DEFAULT.read_text(encoding="utf-8"))

    def test_actual_five_services_and_original_ui_source_pins(self):
        result = validate(self.packet)
        self.assertEqual(result["five_services"], 5)
        self.assertEqual(result["qualified_manual_statements"], 13)
        self.assertEqual(result["generic_v1_client_records"], 12)
        self.assertEqual(result["source_blobs"], 5)
        self.assertFalse(result["original_server_executed"])

    def test_first_party_savepoint_requires_offering_but_not_ack(self):
        self.assertEqual(claim_result(self.packet,"SAVE_POINT","FIRST_USE_OFFERING_REQUIRED",True),
                         "MATCHES_ARCHIVED_MANUAL_DESCRIPTION")
        self.assertEqual(claim_result(self.packet,"SAVE_POINT","NEXT_LOGIN_USES_RECORDED_POINT",True),
                         "MATCHES_ARCHIVED_MANUAL_DESCRIPTION")
        self.assertEqual(claim_result(self.packet,"SAVE_POINT","DURABLE_ACK",True),
                         "NO_SOURCE_ASSERTION")
        self.assertEqual(claim_result(self.packet,"SAVE_POINT","FIRST_USE_OFFERING_REQUIRED",False),
                         "DIFFERS_FROM_ARCHIVED_MANUAL_NOT_EXECUTION_RESULT")

    def test_bus_values_not_taiwan_server_or_topology(self):
        for key,value in [("STOP_MINUTES",3),("PASSENGER_LIMIT",4),
                          ("ENCOUNTER_DURING_RIDE",False)]:
            with self.subTest(key=key):
                self.assertEqual(claim_result(self.packet,"MAMMOTH_BUS",key,value),
                                 "MATCHES_ARCHIVED_MANUAL_DESCRIPTION")
                self.assertEqual(claim_result(self.packet,"MAMMOTH_BUS",key,value,
                                              source_layer="TW10_COMMERCIAL_SERVER"),
                                 "OUTSIDE_SOURCE_SCOPE")
        self.assertEqual(claim_result(self.packet,"MAMMOTH_BUS","STOP_MINUTES",180),
                         "DIFFERS_FROM_ARCHIVED_MANUAL_NOT_EXECUTION_RESULT")
        self.assertEqual(claim_result(self.packet,"MAMMOTH_BUS","FARE",0),
                         "NO_SOURCE_ASSERTION")
        self.assertEqual(claim_result(self.packet,"MAMMOTH_BUS","DIRECT_ROUTE_EDGE",True),
                         "NO_SOURCE_ASSERTION")

    def test_bus_bool_int_not_equal(self):
        self.assertEqual(claim_result(self.packet,"MAMMOTH_BUS","PASSENGER_LIMIT",True),
                         "DIFFERS_FROM_ARCHIVED_MANUAL_NOT_EXECUTION_RESULT")
        self.assertEqual(claim_result(self.packet,"MAMMOTH_BUS","ENCOUNTER_DURING_RIDE",0),
                         "DIFFERS_FROM_ARCHIVED_MANUAL_NOT_EXECUTION_RESULT")

    def test_care_and_work_manual_not_free_or_precise_rewards(self):
        self.assertEqual(claim_result(self.packet,"VILLAGE_CARE_TRAINING",
                                       "PAID_PET_SKILL_TRAINING",True),
                         "MATCHES_ARCHIVED_MANUAL_DESCRIPTION")
        self.assertEqual(claim_result(self.packet,"VILLAGE_CARE_TRAINING",
                                       "EVERY_VILLAGE_HAS_EVERY_FACILITY",False),
                         "MATCHES_ARCHIVED_MANUAL_DESCRIPTION")
        self.assertEqual(claim_result(self.packet,"VILLAGE_WORK","PAY_PER_ORE",100),
                         "NO_SOURCE_ASSERTION")

    def test_ground_item_time_and_quest_logout_separated(self):
        self.assertEqual(claim_result(self.packet,"GROUND_ITEM_EXPIRY",
                                       "ORDINARY_GROUND_ITEM_EXPIRES",True),
                         "MATCHES_ARCHIVED_MANUAL_DESCRIPTION")
        self.assertEqual(claim_result(self.packet,"GROUND_ITEM_EXPIRY",
                                       "QUEST_DROP_LOGOUT_FLAG_PROVEN",False),
                         "MATCHES_ARCHIVED_EVIDENCE_BOUNDARY")
        self.assertEqual(claim_result(self.packet,"GROUND_ITEM_EXPIRY","SECONDS_TO_EXPIRE",60),
                         "NO_SOURCE_ASSERTION")

    def test_reject_fake_server_transaction_and_stage_b(self):
        for key in ("original_server_actions_observed","original_client_executed",
                    "original_world_quest_data_recovered","stage_a_accepted",
                    "stage_b_started","original_1999_or_tw10_service_identity_proven",
                    "production_gameplay_changed"):
            with self.subTest(key=key):
                x=deepcopy(self.packet)
                x[key]=True
                with self.assertRaises(ValueError):
                    validate(x)

    def test_wrong_manuscript_or_observable_identity_rejected(self):
        for mutation in ("wrong_blob","fake_callback","merged_version"):
            x=deepcopy(self.packet)
            if mutation=="wrong_blob":
                x["source_pins"]["manual"]["blob"]="0"*40
            elif mutation=="fake_callback":
                x["services"][0]["tw10_generic_observables"][0]["fields"]=["invented_save_ack"]
            else:
                x["services"][0]["version_identity"]="TW10_DIRECT_SERVER_SERVICE"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate(x)

    def test_reject_omitted_unknown_preconditions_or_claims(self):
        x=deepcopy(self.packet)
        x["services"][1]["preconditions_not_resolved"]=[]
        with self.assertRaisesRegex(ValueError,"hidden missing preconditions"):
            validate(x)
        x=deepcopy(self.packet)
        x["services"][1]["manual_claims"].pop()
        with self.assertRaisesRegex(ValueError,"incomplete evidence claims"):
            validate(x)


    def test_classifier_does_not_trust_modified_manual_paths_or_evidence_roles(self):
        packet=deepcopy(self.packet)
        pkt=packet["services"][0]["manual_claims"][0]
        pkt["manual_path"]="bus.stop_minutes"
        with self.assertRaisesRegex(ValueError,"untrusted claim path"):
            claim_result(packet,"SAVE_POINT","FIRST_USE_OFFERING_REQUIRED",3)
        packet=deepcopy(self.packet)
        pkt=packet["services"][4]["manual_claims"][1]
        pkt["claim_kind"]="MANUAL_BEHAVIOR"
        with self.assertRaisesRegex(ValueError,"untrusted claim role"):
            claim_result(packet,"GROUND_ITEM_EXPIRY","QUEST_DROP_LOGOUT_FLAG_PROVEN",False)

    def test_priorities_remain_bounded(self):
        self.assertEqual(self.packet["next"],"STAGE-A-EARLY-SOURCE-GAP-TRIAGE-01")
        self.assertEqual(self.packet["stage_b_gate"],"GATED")
        self.assertEqual(self.packet["r79"],"PAUSED_NON_BLOCKING")
        self.assertEqual(claim_result(self.packet,"NONEXISTENT","ANYTHING",True),
                         "NO_SOURCE_ASSERTION")


if __name__=="__main__":
    unittest.main()
