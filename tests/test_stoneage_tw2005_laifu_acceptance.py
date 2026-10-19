import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "research/recovered/STONEAGE-TW2005-LAIFU-DERIVED-CUSTODY-R1.json"

class LaifuCustodyChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_derived_json_actual_bytes_hash_and_git_blob(self):
        q = self.r["derived_report"]
        data = (ROOT/q["path"]).read_bytes()
        self.assertEqual(len(data), q["utf8_bytes"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), q["sha256"])
        blob = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
        self.assertEqual(hashlib.sha1(blob).hexdigest(), q["git_blob"])

    def test_missing_original_sources_not_promoted(self):
        self.assertTrue(all(s["browser_open"] == "HTTP_403" for s in self.r["source_states"]))
        self.assertTrue(all(s["source_raw_sha256"] is None for s in self.r["source_states"]))
        self.assertFalse(self.r["original_server_quest_execution_verified"])
        self.assertFalse(self.r["original_first_party_html_attested"])
        self.assertFalse(self.r["artifact_zip_created"])
        self.assertIsNone(self.r["archive_zip_digest"])

    def test_parent_ci_gates_but_not_this_commit(self):
        self.assertEqual(self.r["candidate_verification"]["total"],10)
        self.assertEqual(self.r["main_verification"]["total"],11)
        self.assertEqual(self.r["main_verification"]["source_tests_pass"],9)
        self.assertEqual(self.r["new_receipt_self_ci_status"],"REQUIRES_SEPARATE_VALIDATION")
        self.assertEqual(self.r["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-20")

if __name__ == "__main__":
    unittest.main()
