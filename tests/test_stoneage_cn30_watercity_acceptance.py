import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "research/recovered/STONEAGE-CN30-WATERCITY-SOURCE-BOUNDARY-ACCEPTANCE-R1.json"

class WatercityDerivedCustodyReceipt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_retained_derived_git_and_sha256(self):
        for entry in self.receipt["permanently_retained_derived"]:
            raw=(ROOT/entry["path"]).read_bytes()
            self.assertEqual(len(raw),entry["bytes_utf8"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),entry["sha256_utf8"])
            git_blob=b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw
            self.assertEqual(hashlib.sha1(git_blob).hexdigest(),entry["git_blob_sha"])

    def test_source_original_not_misrepresented(self):
        r=self.receipt
        self.assertEqual(r["status"],"DERIVED_GIT_PERSISTENT_SOURCE_RAW_UNATTESTED")
        self.assertTrue(all(x["raw_original_html_sha256"] is None for x in r["inputs"]))
        self.assertFalse(r["validation"]["source_independent_http_byte_replay"])
        self.assertIsNone(r["validation"]["archived_ci_zip_artifact_id"])
        self.assertIsNone(r["validation"]["archived_ci_zip_sha256"])
        self.assertIsNone(r["accepted_content_main"]["original_server_binary"])
        self.assertIsNone(r["accepted_content_main"]["original_event_script"])

    def test_exact_parent_source_runs_not_self_certifying(self):
        r=self.receipt
        self.assertEqual(r["validation"]["candidate_workflow_count"],10)
        self.assertEqual(r["validation"]["main_workflow_count"],11)
        self.assertIn("18 tests",r["validation"]["main_dedicated_log_summary"])
        self.assertEqual(r["accepted_content_main"]["sha"],r["validation"]["main_sha"])
        self.assertEqual(r["followup_priority"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18")
