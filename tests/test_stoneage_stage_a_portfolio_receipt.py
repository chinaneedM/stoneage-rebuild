"""Verify archived Stage A portfolio checkpoint without source or stage promotion."""
from copy import deepcopy
import json
import hashlib
from pathlib import Path
import unittest

from tools.stoneage_stage_a_portfolio_checkpoint import (
    REPORT, ROOT, validate
)

RECEIPT=ROOT/"research/recovered/STONEAGE-STAGE-A-PORTFOLIO-CHECKPOINT-ACCEPTANCE-R2.json"
VALIDATOR=ROOT/"tools/stoneage_stage_a_portfolio_checkpoint.py"


def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


class CheckpointReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads(RECEIPT.read_bytes())
        cls.report=json.loads(REPORT.read_bytes())

    def test_permanent_derived_and_validator_are_pinned(self):
        self.assertEqual(blob(REPORT.read_bytes()), self.receipt["derived_report_git_blob"])
        self.assertEqual(blob(VALIDATOR.read_bytes()), self.receipt["validator_git_blob"])
        self.assertEqual(validate(self.report)["status"],"PASS")

    def test_source_ci_custody_cannot_be_relabelled_original_execution(self):
        rc=self.receipt
        self.assertEqual(rc["source_commit"],"c69cc89c1221739f9df8f38ae6bf2b0f7612847f")
        self.assertEqual(rc["source_tree"],"2205596037b55257fcbf4d564bafcf8ab11149d1")
        self.assertEqual(rc["conclusion"],"success")
        self.assertEqual(rc["workflow_run_id"],38999995941)
        self.assertEqual(rc["tests"],{"new_checkpoint":8,"prior_stage_a_review":5,
                                       "tw10_original_ui":10,"early_manual":7,"total":30})
        for field in ("authenticated_new_jss1999_bytes_acquired",
                      "original_game_binary_or_server_executed",
                      "original_npc_or_quest_data_added","stage_a_accepted",
                      "joint_user_review_completed"):
            self.assertIs(rc[field],False,field)
        self.assertEqual(rc["stage_b_gate"],"GATED")
        self.assertEqual(rc["savedata_r79"],"PAUSED_NON_BLOCKING")

    def test_existing_review_source_and_history_pins_retained(self):
        c=self.receipt["machine_check"]
        self.assertEqual((c["families"],c["playflows"],c["blockers"]),(9,7,5))
        self.assertEqual(c["immutable_source_git_blobs"],8)
        self.assertEqual(c["review_packet_source_pins"],54)
        self.assertEqual(c["historical_prefixes"],8)

    def test_prioritization_handoff_cannot_claim_stage_b(self):
        self.assertEqual(self.receipt["highest_next"],"EARLY-VILLAGE-SERVICE-JOURNEY-01")
        self.assertEqual(self.report["next_priority"],self.receipt["highest_next"])
        self.assertFalse(self.report["stage_a_accepted"])
        self.assertFalse(self.report["production_engine_changes"])


if __name__=="__main__":
    unittest.main()
