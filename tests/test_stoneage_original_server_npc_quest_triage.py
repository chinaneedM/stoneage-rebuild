"""Gold boar riddle three-brothers historical quest source boundary tests."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"research/recovered/STONEAGE-ORIGINAL-SERVER-NPC-QUEST-TRIAGE-R1.json"
PET=ROOT/"research/recovered/STONEAGE-PET-IDENTITY-SAME-BUILD-TRIAGE-R1.json"
OLDER=ROOT/"research/recovered/STONEAGE-EARLY-MEDIA-ARTICLE-PET-SOURCE-R1.json"
LATER=ROOT/"research/recovered/STONEAGE-WORLD-NPC-QUEST-CATALOG-R1.json"

class OriginalNPCQuestSameBuildBoundary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=json.loads(FILE.read_text(encoding="utf-8"))
  cls.pet=json.loads(PET.read_text(encoding="utf-8"))
  cls.old=json.loads(OLDER.read_text(encoding="utf-8"))
  cls.later=json.loads(LATER.read_text(encoding="utf-8"))
 def test_real_existing_player_pet_sources_no_new_tw10_identity(self):
  s={x["id"]:x for x in self.d["web_witnesses"]}
  self.assertEqual(len(s),6)
  self.assertEqual(len(set(x["url"] for x in s.values())),6)
  self.assertFalse(any(x["original_date_page_bytes_certified"] or x["original_server_code"] for x in s.values()))
  self.assertEqual(s["W20010614_124"]["source_history"],"ALREADY_USED_IN_PRIOR_124_ROW_PACKAGE")
  self.assertEqual(s["W20010614_20"]["source_history"],"ALREADY_ARCHIVED_IN_20_ROW_PACKAGE")
  row=next(x for x in self.pet["selected_lexical_overlaps"] if x["source_name"]=="金布伊")
  self.assertEqual(row["lv1_row"],7)
  self.assertFalse(row["same_species_certified"])
  self.assertTrue(any(x["source_name"]=="金布伊" and x["original_species_id"] is None for x in self.old["pet_name_candidates"]))
 def test_tension_kept_not_reconciled_across_version(self):
  claims={x["key"]:x for x in self.d["player_claim_layers"]}
  self.assertEqual([x["reported_site"] for x in (claims["C1"],claims["C2"])],["fishing_village_dojo","Karuta_village_dojo"])
  self.assertEqual(claims["C4"]["version"],"PLAYER_EXPLICIT_2_0")
  self.assertEqual(claims["C4"]["reported_threshold_level"],70)
  self.assertEqual(claims["C4"]["required_gold_boar_level"],77)
  self.assertFalse(claims["C4"]["original_tw10_equality_verified"])
  self.assertFalse(claims["C3"]["success_verified"])
  self.assertTrue(claims["C3"]["reported_disconnection"])
  self.assertTrue(all(x["resolution"] for x in self.d["tensions"]))
  self.assertTrue(all(x["retroactive_2_0_explanation_not_allowed"] for x in self.d["tensions"] if x["id"]=="location_mismatch"))
  self.assertEqual(next(x for x in self.d["tensions"] if x["id"]=="catalog_id_010")["tw10_pet_id"],None)
 def test_no_recovered25_other_quest_promotion_and_no_tw10_server_script(self):
  self.assertEqual(len(self.later["npcs"]),2)
  self.assertEqual(len(self.later["event_records"]),6)
  self.assertTrue(all(x["version_profile"]=="RECOVERED25" for x in self.later["npcs"]))
  self.assertIn("RECOVERED25_YAYOI_HIMIKO_EXCHANGE_IS_DIFFERENT_QUEST_AND_BUILD",self.d["prohibited_crosswalks"])
  self.assertTrue(all(v is None or v is False for v in self.d["exact_same_build_server_join"].values()))
  self.assertEqual(self.d["same_build_original_server_script_count"],0)
 def test_stop_and_preserve_project_boundaries(self):
  self.assertEqual(self.d["disposition"],"OPEN_EVIDENCE_LIMITED_NO_ORIGINAL_TW10_SAME_BUILD_NPC_REWARD_SCRIPT")
  self.assertTrue(self.d["stop_condition_met"])
  self.assertEqual(self.d["stage_a_status"],"7_PARTIAL_2_OPEN")
  self.assertEqual(self.d["next_priority"],"PREPRODUCTION-22-DOMAIN-SOURCE-READY-PORTFOLIO-REVIEW-02")
  self.assertTrue(self.d["stage_b_gated"] and self.d["local_savedata_R79_paused"] and self.d["no_original_game_payload_added"])
  self.assertFalse(self.d["historical_total_complete"])
if __name__=="__main__": unittest.main()
