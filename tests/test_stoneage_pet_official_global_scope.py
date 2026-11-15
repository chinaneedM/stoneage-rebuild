"""Only confirmed officially released pets may enter the official game roster."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from stoneage_pet_official_lookup import select
class OfficialPetScope(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.data=json.loads((ROOT/"research/recovered/STONEAGE-PET-OFFICIAL-GLOBAL-RELEASE-EVIDENCE-R1.json").read_text(encoding="utf-8"))
  c.entries=c.data["official_web_evidence_queue_NOT_RELEASE_PROVEN"]
 def test_original_official_website_evidence_only(self):
  self.assertEqual(len(self.entries),228)
  self.assertEqual(len([x for x in self.entries if x["region"]=="JP"]),124)
  self.assertEqual(len([x for x in self.entries if x["region"]=="CN"]),104)
  self.assertEqual(len({x["source_id"] for x in self.entries}),228)
  self.assertTrue(all(x["game_release_verification"]=="OFFICIAL_WEB_LISTED_NOT_IN_GAME_PROVED" for x in self.entries))
  self.assertTrue(all(x["officially_released_pet_count_eligible"] is False for x in self.entries))
 def test_official_image_sha_is_not_game_release_proof(self):
  jp=[x for x in self.entries if x["region"]=="JP"]
  self.assertEqual(sum(bool(x["original_archived_image_sha256_or_null"]) for x in jp),38)
  self.assertEqual(sum(bool(x["original_archived_image_sha256_or_null"]) for x in self.entries if x["region"]=="CN"),0)
  self.assertEqual(len(self.data["confirmed_in_game_official_pets_in_this_register"]),0)
  self.assertIsNone(self.data["confirmed_official_species_count_global"])
 def test_private_server_excluded_from_official_roster(self):
  m=self.data["quarantined_existing_community_research"]
  self.assertFalse(m["automatic_conversion_into_official_roster_allowed"])
  self.assertEqual(set(m["source_namespaces"]),{"later2016_templates","later2016_graphics","mixed25_main","mixed25_alternative"})
  self.assertFalse(any(x["source_namespace"] in m["source_namespaces"] for x in self.entries))
 def test_region_queries_and_names_as_source_only(self):
  self.assertEqual(len(select(self.data,"",region="JP",limit=999)),124)
  self.assertEqual(len(select(self.data,"",region="CN",limit=999)),104)
  self.assertEqual(select(self.data,confirmed_only=True),[])
  self.assertTrue(select(self.data,query="ウーリ",region="JP"))
 def test_user_examples_are_only_research_queue(self):
  examples=self.data["user_named_official_release_research_targets_unverified"]
  self.assertEqual([x["user_supplied_search_term"] for x in examples],
                   ["年兽","马年宠","机豹","蒙奇","海胆","肥龙"])
  self.assertTrue(all(not x["counts_as_official_pet"] for x in examples))
 def test_source_pins_and_invariant_stage(self):
  self.assertEqual(self.data["historical_sources"]["full_historical_current_blob_unmodified"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual(self.data["evidence_summary"]["verified_Japan_archived_image_SHA_positions"],38)
  self.assertEqual(self.data["active_module"],"PET")
  self.assertEqual(self.data["stage_a"],"7_PARTIAL_2_OPEN")
if __name__=="__main__":unittest.main()
