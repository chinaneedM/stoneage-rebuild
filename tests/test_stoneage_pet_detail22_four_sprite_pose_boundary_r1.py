"""PET22 authenticated original TW1 PC four source-pose fallback and strict missing-portrait gates."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R="research/pets/PET-DETAIL-EVIDENCE22-TW10-FOUR-POSES-NO-PORTRAIT-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def sha(p):
 b=(ROOT/p).read_bytes();return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
class FourMissingPortraits(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=read(R)
  cls.a=read("research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
  cls.m=read("research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json")
 def test_original_archived_sources_not_rewritten(self):
  for path,blob in self.r["pinned_public_git_blobs"].items():self.assertEqual(sha(path),blob,path)
  self.assertEqual(self.r["original_source"]["physical_original_RD_source_records_verified"],16)
  self.assertTrue(self.r["original_source"]["original_SPR_ADRN_REAL_bytes_reopened"])
 def test_four_distinct_real_pose_selections_and_null_portraits(self):
  cases=self.r["records"]
  self.assertEqual([(r["graphic_number"],r["original_spr_group_index"],r["original_portrait_logical_alias"]) for r in cases],
                   [(100389,355,28085),(100390,356,28086),(100391,357,28087),(100392,358,28088)])
  for r in cases:
   k=r["graphic_number"];g=next(x for x in self.m["groups"] if x["graphic"]==k)
   a=next(x for x in self.a["records"] if x["graphic_number"]==k)
   p=read("research/pets/profiles/TW10-G"+str(k)+".json")
   self.assertEqual(r["original_spr_segment_sha256"],g["segment_sha256"])
   self.assertEqual(r["original_spr_group_index"],g["group_index"])
   self.assertIsNone(a["portrait_rd"])
   self.assertEqual(r["same_decimal_physical_bitmap_record"]["logical_alias_field_value"],0)
   self.assertTrue(r["same_decimal_physical_bitmap_record"]["NOT_A_VALID_ORIGINAL_PORTRAIT"])
   self.assertIsNone(p["appearance"]["portrait"]["source_rd_sha256"])
   self.assertIsNone(p["appearance"]["portrait"]["source_rd_bitmap_number"])
   self.assertEqual(p["appearance"]["portrait"]["status"],"OPEN_NOT_PROVEN")
   self.assertEqual(p["appearance"]["source_SPR_pose_reference"]["evidence_blob"],sha(R))
   self.assertFalse(p["appearance"]["source_SPR_pose_reference"]["is_original_album_portrait"])
   self.assertEqual(p["appearance"]["source_SPR_pose_reference"]["source_frame_numbers"],[v["first_frame_bitmap_number"] for v in r["source_pose_bitmaps"]])
   self.assertEqual([v["direction_code"] for v in r["source_pose_bitmaps"]],[0,2,4,6])
   for v in r["source_pose_bitmaps"]:
    self.assertRegex(v["original_RD_sha256"],r"^[0-9a-f]{64}$")
   self.assertIn("PET-DETAIL22",(ROOT/("docs/pets/TW10-G"+str(k)+".md")).read_text())
 def test_no_false_completion(self):
  c=self.r["release_guards"]
  self.assertEqual((c["original_album_portraits_still_missing"],c["tw10_client_named_dossiers_partial"],c["historically_complete_dossiers"]),(4,124,0))
  self.assertEqual(c["confirmed_new_official_live_species"],0)
  self.assertIsNone(c["overall_percent"])
  self.assertEqual(c["public_git_proprietary_bitmap_files"],0)
  self.assertFalse(self.r["original_source"]["original_client_executed"])
if __name__=="__main__":unittest.main()
