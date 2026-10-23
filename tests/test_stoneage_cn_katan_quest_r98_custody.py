"""R98 source-custody receipt checks (historical and current-source identities)."""
import hashlib
import json
import unittest
from pathlib import Path
from tools.stoneage_cn_katan_quest_r98 import P,verify
ROOT=P.parents[2]
R=ROOT/"research/recovered/STONEAGE-CN-KATAN-QUEST-ACCEPTANCE-R98.json"
RECEIPT_SHA="0fa918fb83b90025d3ee1e6c7e20547a8c971570"

def blob_sha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

class R98Custody(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert blob_sha(R.read_bytes())==RECEIPT_SHA
        cls.r=json.loads(R.read_text(encoding="utf-8"))
    def test_identity_and_history(self):
        r=self.r
        self.assertEqual(r["schema"],"stoneage.cn_katan_quest_r98_acceptance.v1")
        self.assertEqual(r["task"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-98")
        self.assertEqual(r["starting_main"]["sha"],"8697dc3808c074f98e9116d8378c711581ff2f2f")
        self.assertEqual(r["content"]["sha"],"2a2bb6bf63c7e4e1a4e9b3fdd14641379aa558b4")
        self.assertEqual(r["docs"]["sha"],"79fb6dc54f4b67dc0f12e235916ab3f5db3f8100")
    def test_source_git_blob_and_boundaries(self):
        r=self.r
        self.assertEqual(blob_sha(P.read_bytes()),"e92c249a74582ba6f5af5b41f49540ec9d1cd1d2")
        self.assertEqual(blob_sha(P.read_bytes()),r["source"]["git_blob_sha"])
        self.assertTrue(verify(json.loads(P.read_text(encoding="utf-8"))))
        self.assertTrue(r["boundaries"]["source_is_player_guide"])
    def test_no_fabricated_artifact_proof(self):
        z=self.r["artifact"]
        self.assertEqual((z["candidate_count"],z["main_count"]),(0,0))
        self.assertIsNone(z["original_html_sha256"])
        self.assertIsNone(z["original_screenshots_sha256"])
        self.assertIsNone(z["artifact_zip_sha256"])
        self.assertTrue(z["derived_blob_in_git"])
    def test_independent_real_ci_custody(self):
        r=self.r
        a=r["candidate_docs_ci"]["runs"]; b=r["main_docs_ci"]["runs"]
        self.assertEqual((len(a),len(set(a)),len(b),len(set(b))),(9,9,11,11))
        self.assertFalse(set(a)&set(b))
        self.assertEqual(r["candidate_source_ci"]["run"],39966865260)
        self.assertEqual(r["candidate_source_ci"]["job"],120458877622)
        self.assertEqual(r["candidate_source_ci"]["methods"],15)
        self.assertEqual(r["main_docs_ci"]["dedicated_run"],39967404086)
        self.assertEqual(r["main_docs_ci"]["dedicated_job"],120460766533)
        self.assertTrue(r["candidate_source_ci"]["success"])
        self.assertTrue(r["candidate_docs_ci"]["success"])
        self.assertTrue(r["main_docs_ci"]["success"])
    def test_non_destructive_publication(self):
        r=self.r
        self.assertEqual((r["git_publication"]["ahead"],r["git_publication"]["behind"],r["git_publication"]["files"],r["git_publication"]["deletions"]),(2,0,9,0))
        self.assertTrue(r["git_publication"]["nonforce_fast_forward"])
        self.assertEqual({x["path"] for x in r["prefixes"]},{"docs/CURRENT-STATE.md","docs/HISTORICAL-TIMELINE.md","docs/SOURCE-REGISTRY.md","docs/RESTORATION-ROADMAP-R2.md"})
        self.assertTrue(all(x["prefix_kept"] for x in r["prefixes"]))
    def test_no_stage_or_runtime_overstatement(self):
        g=self.r["boundaries"]
        self.assertFalse(any(g[k] for k in ("original_server_ack","original_game_build_verified","ring_reissue_conflict_resolved","authentic_NPC_screenshot","stage_a_complete","stage_b_started")))
        self.assertIsNone(g["overall_percent"])
        self.assertEqual(g["next"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-99")

if __name__=="__main__":unittest.main()
