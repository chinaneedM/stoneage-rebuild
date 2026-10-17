"""Historical-continuity prefix and exact initial acceptance receipt guards."""
import hashlib
import json
import unittest
from pathlib import Path
from tools.stoneage_stage_a_early_source_gap_triage import ROOT,REPORT,blob_sha,validate

BASE={
    "docs/CURRENT-STATE.md":(1871483,"d8e2d9d1bedac2a6b3506fc20aff06737ace416a"),
    "docs/SOURCE-REGISTRY.md":(661698,"9eef579399fc47e5dd696f2ef61bf79617edcd41"),
    "docs/RESTORATION-ROADMAP-R2.md":(32513,"9c81ae579ffb12fb8b28a527fc20901396df6963"),
}
ACCEPTANCE=ROOT/"research/recovered/STONEAGE-STAGE-A-EARLY-SOURCE-GAP-ACCEPTANCE-R1.json"

class EarlySourceGapArchiveTests(unittest.TestCase):
    def test_full_three_prior_historical_prefixes(self):
        for name,(n,expected) in BASE.items():
            data=(ROOT/name).read_bytes()
            with self.subTest(name=name):
                self.assertGreater(len(data),n)
                self.assertEqual(blob_sha(data[:n]),expected)
                self.assertIn(b"STAGE-A-EARLY-SOURCE-GAP-TRIAGE-01",data[n:])

    def test_source_report_exact_git_identity(self):
        self.assertEqual(blob_sha(REPORT.read_bytes()),
                         "927293c09bc04097e013bb96ad1ead5d654ce82d")
        self.assertEqual(validate(json.loads(REPORT.read_text(encoding="utf-8")))["status"],"PASS")

    def test_ci_receipt_cannot_claim_original_recovery(self):
        receipt=json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
        self.assertEqual(receipt["source_commit"],
                         "52ded1bc7a8923202daf0a2394bc8047fc0a2781")
        self.assertEqual(receipt["source_tree"],
                         "2c26a38856d9b1c60f7c72c7ac89f0e86d86d937")
        self.assertEqual(receipt["independent_action"]["id"],39001916143)
        self.assertEqual(receipt["independent_action"]["job"],117306453768)
        self.assertEqual(receipt["independent_action"]["conclusion"],"success")
        for flag in ("claims_new_original_server_evidence","claims_original_client_execution",
                     "claims_stage_a_completed","claims_stage_b_started"):
            self.assertIs(receipt[flag],False)
        self.assertEqual(receipt["later_main_ci"],"PENDING_NOT_ASSERTED")
        self.assertTrue(receipt["continuity_append_only"] and receipt["source_registry_append_only"])
if __name__=="__main__":
    unittest.main()
