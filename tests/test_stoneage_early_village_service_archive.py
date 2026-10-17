"""Independent archive replay of five-service evidence, not original game execution."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_early_village_service_journey import DEFAULT, ROOT, validate, claim_result

RECEIPT = ROOT / "research/recovered/STONEAGE-EARLY-VILLAGE-SERVICE-ACCEPTANCE-R1.json"
PROBE = ROOT / "tools/stoneage_early_village_service_journey.py"


def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


class VillageServiceArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads(RECEIPT.read_bytes())
        cls.report=json.loads(DEFAULT.read_bytes())

    def test_permanent_git_blob_and_source_logic(self):
        self.assertEqual(git_blob(DEFAULT.read_bytes()),
                         self.receipt["archive"]["permanent_git_blob"])
        self.assertEqual(git_blob(PROBE.read_bytes()),
                         self.receipt["archive"]["source_tool_git_blob"])
        self.assertEqual(validate(self.report)["status"],"PASS")

    def test_source_ci_and_first_failed_overclaim_not_relabelled(self):
        r=self.receipt
        self.assertEqual(r["source_commit"],"5f27611d23fb344cec5731698bf0fe1b04aecb2f")
        self.assertEqual(r["source_tree"],"66c577d69c09686bfb5bf20c2a9d7e2fc1c5494a")
        self.assertEqual(r["source_validation"]["run_id"],39001090987)
        self.assertEqual(r["source_validation"]["job_id"],117303967477)
        self.assertEqual(r["source_validation"]["conclusion"],"success")
        self.assertEqual(r["source_validation"]["tests"],36)
        self.assertEqual(r["prior_initial_run"]["run_id"],39000978456)
        self.assertTrue(r["prior_initial_run"]["then_classifier_evidence_boundary_hardened"])

    def test_distinct_manual_claim_from_missing_gameplay_evidence(self):
        self.assertEqual(self.receipt["validated"]["manual_behavior_assertions"],12)
        self.assertEqual(self.receipt["validated"]["metadata_boundary_assertions"],1)
        self.assertEqual(claim_result(self.report,"GROUND_ITEM_EXPIRY",
                                       "QUEST_DROP_LOGOUT_FLAG_PROVEN",False),
                         "MATCHES_ARCHIVED_EVIDENCE_BOUNDARY")
        self.assertEqual(claim_result(self.report,"GROUND_ITEM_EXPIRY",
                                       "SECONDS_TO_EXPIRE",0),"NO_SOURCE_ASSERTION")

    def test_no_fake_recovered_commercial_server_asset_or_account(self):
        receipt=self.receipt
        for v in receipt["evidence_promotion"].values():
            self.assertIs(v,False)
        self.assertIs(receipt["archive"]["original_2001_web_download_run_this_iteration"],False)
        self.assertEqual(receipt["archive"]["source_artifact_zip"],
                         "NOT_APPLICABLE_NO_NEW_BINARY_OR_WEB_BYTES")
        self.assertIs(receipt["stage_a_accepted"],False)
        self.assertIs(receipt["joint_user_review_completed"],False)
        self.assertEqual(receipt["stage_b_gate"],"GATED")

    def test_forged_stage_or_event_binding_cannot_replay(self):
        x=deepcopy(self.report)
        x["services"][0]["tw10_generic_observables"][0]["service_event_binding"]="PROVEN"
        with self.assertRaises(ValueError):
            validate(x)
        x=deepcopy(self.report)
        x["stage_a_accepted"]=True
        with self.assertRaises(ValueError):
            validate(x)

    def test_next_is_stop_and_audit_not_engine(self):
        self.assertEqual(self.receipt["next"],"STAGE-A-EARLY-SOURCE-GAP-TRIAGE-01")
        self.assertEqual(self.report["next"],self.receipt["next"])
        self.assertEqual(self.receipt["r79"],"PAUSED_NON_BLOCKING")


if __name__=="__main__":
    unittest.main()
