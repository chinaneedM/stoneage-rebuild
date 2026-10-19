import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/recovered/STONEAGE-CN60-TEARSTONE-DERIVED-CUSTODY-R1.json"

class TearstoneCustodyAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(PATH.read_text(encoding="utf-8"))

    def test_derived_bytes_and_git_blob_digest(self):
        d = self.r["derived_json"]
        data = (ROOT / d["path"]).read_bytes()
        self.assertEqual(len(data), d["utf8_bytes"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), d["sha256"])
        blob = b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
        self.assertEqual(hashlib.sha1(blob).hexdigest(), d["git_blob"])

    def test_original_source_is_not_byte_attested(self):
        self.assertIsNone(self.r["contemporary_source"]["historical_html_sha256"])
        self.assertFalse(self.r["contemporary_source"]["raw_bytes_replay"])
        self.assertIsNone(self.r["provenance_limits"]["source_archive_zip"])
        self.assertFalse(self.r["provenance_limits"]["original_build_confirmed"])

    def test_previous_main_checks_are_not_this_commit_checks(self):
        self.assertEqual(self.r["acceptance"]["candidate_check_count"], 10)
        self.assertEqual(self.r["acceptance"]["main_check_count"], 11)
        self.assertTrue(self.r["acceptance"]["tests_only_validate_derived_claims"])
        self.assertEqual(self.r["next"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-19")

if __name__ == "__main__":
    unittest.main()
