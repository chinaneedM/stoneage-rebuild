import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"research/recovered/STONEAGE-PET38-CLIENT-FIRST-AVAILABLE-SOURCE-INVENTORY-R1.json"
QUEUE=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
PROTOCOL=ROOT/"docs/PROJECT-CONTINUITY-PROTOCOL-R1.md"
class TestPet38ClientFirstPriority(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads(MANIFEST.read_text(encoding="utf-8"))
  cls.q=json.loads(QUEUE.read_text(encoding="utf-8"))
  cls.p=PROTOCOL.read_text(encoding="utf-8")
 def test_policy_and_earliest_year_preserved(self):
  self.assertIn("## 23. Client-first official pet extraction",self.p)
  self.assertIn("CLIENT_ASSET_PRESENT",self.p)
  self.assertIn("OFFICIAL_IN_GAME_RELEASE_CONFIRMED",self.p)
  self.assertEqual(self.q["current_frontier"]["year"],2000)
  self.assertEqual(self.q["current_frontier"]["current_source_acquisition_priority"],"CLIENT_FIRST_VERSION_AUTHENTICATION_AND_PET_RESOURCE_EXTRACTION_BEFORE_EXTERNAL_NEWS")
  self.assertEqual(self.m["active_module"],"PET")
  self.assertFalse(self.m["year_2000_source_bounded_reviewed"])
 def test_older_taiwan_original_custody_is_not_new_extraction(self):
  m=self.m;r=next(x for x in m["records"] if x["id"]=="TW_WAEI_JSS_1_0_RETAIL")
  self.assertEqual(r["size_bytes"],372626292)
  self.assertEqual(r["zip_sha256"],"3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24")
  self.assertEqual(r["zip_crc_verified_count_prior"],379)
  self.assertEqual(r["resource_index_previously_verified"]["spr_group_records"],464)
  self.assertFalse(r["verified_bytes_in_current_session"])
  self.assertFalse(m["source_material_bytes_just_reacquired_this_session"])
  self.assertFalse(r["official_same_build_pet_roster_proven"])
 def test_other_versions_excluded_from_2000_qualifications(self):
  r={x["id"]:x for x in self.m["records"]}
  for key in ["CN5_CANDIDATE_RESOURCE_INDEX","TW85_CANDIDATE_RESOURCE_INDEX"]:
   self.assertTrue(r[key]["exclude_from_2000_official_release"])
  self.assertTrue(r["MIXED25_COMMUNITY_PRESERVED"]["exclude_from_official_release_roster"])
  self.assertFalse(self.m["prior_community_server_index"]["official_original_jss_or_tw1_server"])
  self.assertIsNone(self.m["pet_species_population_by_year"])
 def test_three_evidence_gates_preserve_release_border(self):
  d={x["id"]:x for x in self.m["pet_fact_layers"]}
  self.assertFalse(d["CLIENT_FILE_OR_SPR_PRESENT"]["count_as_official_released_pet"])
  self.assertFalse(d["CLIENT_IDENTIFIED_PET_CANDIDATE"]["count_as_official_released_pet"])
  self.assertTrue(d["OFFICIAL_VERSION_PET_RELEASE_CONFIRMED"]["count_as_official_released_pet"])
  self.assertIn("OFFICIAL_LIVE_ISSUANCE",self.m["server_only_unknown_fields"])
  self.assertEqual(self.m["original_current_blob_preserved"],"c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
