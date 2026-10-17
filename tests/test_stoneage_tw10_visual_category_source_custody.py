"""Exact byte-custody and semantic replay for original TW1.0 visual frame intersection."""
import hashlib
import json
import unittest
from pathlib import Path
from tools.stoneage_tw10_visual_category_spr_join import audit
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-TW10-VISUAL-CATEGORY-SPR-JOIN-R1.json"
RECEIPT=ROOT/"research/recovered/STONEAGE-TW10-VISUAL-CATEGORY-SPR-JOIN-ACCEPTANCE-R1.json"
RAW_SHA="e33bdae8c202dcf5a1374746afc505f517d8e1afc557fd07057d2d1811a54fcd"
RAW_BLOB="20a82e4d35661785c4e50b44855cf8e8a4e98f3e"
class OriginalVisualSourceCustody(unittest.TestCase):
 def test_raw_content_and_sha_same_as_independent_artifact(self):
  content=REPORT.read_bytes()
  self.assertEqual(len(content),8369)
  self.assertEqual(hashlib.sha256(content).hexdigest(),RAW_SHA)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(content)).encode()+b"\\0"+content).hexdigest(),RAW_BLOB)
  a=json.loads(RECEIPT.read_text(encoding="utf-8"))
  self.assertEqual(a["archive"]["original_zip_sha256"],"fa5ad6bf8f926feb8f8fc54e02c206760dfcaac4dbc28ef814145de7961479ee")
  self.assertEqual(a["archive"]["original_json_sha256"],RAW_SHA)
  self.assertEqual(a["archive"]["original_json_git_blob"],RAW_BLOB)
  self.assertTrue(a["archive"]["independent_download_zip_digest_checked"])
 def test_exact_semantic_replay_and_negative_boundary(self):
  r=REPORT.read_bytes()
  expected=(json.dumps(audit(),ensure_ascii=False,sort_keys=True,indent=2)+"\\n").encode("utf-8")
  self.assertEqual(expected,r)
  d=json.loads(r)
  q={x["category_id"]:x for x in d["categories"]}
  self.assertEqual((q["character_actions"]["original_spr_frame_references"],q["character_actions"]["original_spr_groups_touching_range"]),(137508,240))
  self.assertEqual((q["pet_actions"]["original_spr_frame_references"],q["pet_actions"]["original_spr_groups_touching_range"]),(70236,124))
  self.assertTrue(all(q[x]["original_spr_frame_references"]==0 for x in ("npc_candidate","pet_portrait","character_portrait","items","ui")))
  self.assertFalse(d["any_player_category_upgraded_to_original_semantic_fact"])
  self.assertFalse(d["same_build_pet_master_available"])
  self.assertFalse(d["original_client_render_execution_tested"])
if __name__=="__main__":unittest.main()
