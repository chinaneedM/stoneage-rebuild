"""PET23 true Actions byte-SHA receipts and unified catalogue non-overwrite."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered"
sys.path.insert(0,str(ROOT/"tools"))
from stoneage_pet16_lookup import operator_image_trace
def load(n): return json.loads((R/n).read_text(encoding="utf-8"))
class Pet23(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.cat=load("STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json")
  c.old=load("STONEAGE-PET-MODULE-21-OFFICIAL-WEB-ARCHIVED-IMAGE-REACCESS-R1.json")
  c.prior=load("STONEAGE-PET-MODULE-22-JP-124-ARCHIVED-IMAGE-RECOVERY-R1.json")
  c.now=load("STONEAGE-PET-MODULE-23-JP-LOW-RATE-IMAGE-REACCESS-R1.json")
 def test_exact_actual_observation_and_prior_28_preserved(self):
  x=self.now
  self.assertEqual((x["original_exact_source_workflow_run_id"],x["original_exact_source_job_id"]),(43696651764,132758581358))
  self.assertEqual((x["old_distinct_jp_positions_with_real_archived_image_sha"],x["old_unconfirmed_jp_positions"]),(28,96))
  self.assertEqual((x["observed_new_source_distinct_positions"],x["still_network_or_index_blocked_this_retry"]),(9,3))
  self.assertEqual((x["cumulative_distinct_jp_positions_with_real_archived_image_sha"],x["remaining_jp_positions_without_any_verified_image_sha"]),(37,87))
  self.assertEqual([r["web_ordinal"] for r in x["records"]],[11,22,33,43,49,60,71,84,103,110,114,124])
  self.assertEqual([r["web_ordinal"] for r in x["records"] if r["image_original_sha256_or_null"]],[11,22,33,43,49,60,71,84,103])
  self.assertEqual((x["original_media_gif_bodies_persistently_saved_privately_this_work_package"],x["original_media_gif_bodies_published_or_uploaded_to_GitHub"]),(0,0))
 def test_twelve_rows_source_exact_and_no_claims(self):
  for r in self.now["records"]:
   original=self.cat["datasets"]["jp_official_web"][r["web_ordinal"]-1]
   old=self.prior["records"][r["web_ordinal"]-1]
   self.assertIsNone(old["best_archival_observation_sha256_or_null"])
   self.assertEqual(r["original_source_record_id"],original["id"])
   self.assertEqual(r["historical_operator_original_image_url"],original["image_reference_url"])
   self.assertEqual(r["original_page_bytes_sha256"],original["source_refs"][0]["sha256"])
   self.assertFalse(r["authenticated_original_game_client_species_identity"])
   self.assertFalse(r["right_to_publish_or_reuse_image_approved"])
   if r["image_original_sha256_or_null"]:
    self.assertEqual(r["actual_probe_status"],"ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED")
    self.assertEqual(r["image_dimensions_or_null"],[60,65])
    self.assertEqual(len(r["image_original_sha256_or_null"]),64)
 def trace(self,n,latest=None,region="jp"):
  return operator_image_trace(self.cat,self.old,region,n,pet22=self.prior,pet23=self.now if latest is None else latest)
 def test_unified_pet_atlas_and_old_sha_untouched(self):
  self.assertEqual(self.trace(11)["best_observed_operator_archived_image_sha256_or_null"],self.now["records"][0]["image_original_sha256_or_null"])
  self.assertIsNotNone(self.trace(11)["pet23_source_receipt_or_null"])
  self.assertEqual(self.trace(44)["best_observed_operator_archived_image_sha256_or_null"],self.prior["records"][43]["best_archival_observation_sha256_or_null"])
  self.assertIsNone(self.trace(124)["best_observed_operator_archived_image_sha256_or_null"])
  self.assertIsNone(self.trace(1,region="cn")["pet23_source_receipt_or_null"])
  self.assertFalse(self.trace(11)["original_official_client_species_ID_proven"])
 def test_reject_page_hash_forgery_and_illegal_old_sha_replace(self):
  forged=copy.deepcopy(self.now)
  forged["records"][0]["original_page_bytes_sha256"]="0"*64
  with self.assertRaises(ValueError):self.trace(11,latest=forged)
  forged=copy.deepcopy(self.now)
  forged["records"][0]["web_ordinal"]=1
  with self.assertRaises(ValueError):self.trace(1,latest=forged)
if __name__=="__main__":unittest.main()
