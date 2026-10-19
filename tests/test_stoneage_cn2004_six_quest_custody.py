import hashlib
import json
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
FILE=BASE/"research/recovered/STONEAGE-CN2004-SIX-QUEST-CUSTODY-R1.json"
class SixQuestSourceCustody(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads(FILE.read_text(encoding="utf-8"))
    def test_sha256_git_blob_persisted(self):
        d=self.receipt["derived"]
        raw=(BASE/d["path"]).read_bytes()
        self.assertEqual(len(raw),d["bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(),d["sha256"])
        self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest(),d["git_blob"])
    def test_original_html_and_images_not_attested(self):
        s=self.receipt["sources"]
        self.assertTrue(all(x["original_byte_sha256"] is None for x in s))
        self.assertFalse(self.receipt["negative_bounds"]["original_source_html_hashes_verified"])
        self.assertFalse(s[1]["original_image_bytes_obtained"])
        self.assertIsNone(self.receipt["negative_bounds"]["zip_artifact_id"])
        self.assertEqual(self.receipt["negative_bounds"]["original_server_quest_scripts_recovered"],0)
    def test_parent_actions_not_new_commit_approval(self):
        v=self.receipt["validations"]
        self.assertEqual((v["branch_checks"],v["main_checks"]),(10,11))
        self.assertEqual(v["main_workflow_tests"],8)
        self.assertEqual(self.receipt["this_receipt_self_validation"],"PENDING_CANDIDATE_AND_MAIN_ACTIONS")
        self.assertEqual(self.receipt["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-21")
