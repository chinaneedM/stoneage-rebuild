"""PET61: 2002 CN official product copy vs player species and disputed white-tiger promotion."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"research"/"recovered"

def read(filename):
    return json.loads((SRC/filename).read_text(encoding="utf-8"))

class TestPet61CN2002SourceGrades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=read("STONEAGE-PET61-CN2002-SA30-SA40-OPERATOR-PLAYER-PET-EVIDENCE-R1.json")
        cls.p25=read("STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json")
        cls.q=read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_existing_four_operator_documentary_rows_not_incremented(self):
        d,q=self.d,self.q
        year=q["yearly_work_queue"][3]
        self.assertEqual(d["chronology_year"],2002)
        self.assertEqual(d["source_corpus_preexisting_2002_documentary_release_events"],4)
        self.assertEqual(d["source_corpus_new_documentary_operator_release_events_added_to_PET25"],0)
        self.assertEqual(year["documentary_event_count_NOT_species"],4)
        self.assertEqual(len(self.p25["confirmed_official_release_records"]),24)
        expected=set(year["documented_release_event_ids_from_existing_PET25_PET26"])
        actual={x["record_id"] for x in d["original_registered_2002_documentary_records"]}
        self.assertEqual(expected,actual)
        self.assertEqual(set(x["record_id"] for x in self.p25["confirmed_official_release_records"] if x["record_id"] in expected),expected)
        self.assertTrue(all(x["exact_2002_pet_id"] is None for x in d["original_registered_2002_documentary_records"]))

    def test_exact_four_year_names_are_contemporaneous_player_only(self):
        d=self.d
        names=d["source_claim_new_exact_player_year_beast_names"]
        self.assertEqual([x["player_name"] for x in names],["葛雷吉鲁","葛雷洛比","葛雷马恩","葛雷基欧"])
        self.assertEqual({x["element"] for x in names},{"火","水","风","地"})
        self.assertEqual(len({x["source_id"] for x in names}),1)
        self.assertTrue(all(x["source_date"]=="2002-08-28" for x in names))
        self.assertTrue(all(x["evidence_grade"]=="2002_CONTEMPORANEOUS_PLAYER_NAME_AND_ATTRIBUTE_CLAIM" for x in names))
        self.assertTrue(all(x["original_2002_CN_OFFICIAL_PET_ID"] is None for x in names))
        self.assertTrue(all(x["original_2002_CN_same_build_SPR_SHA256"] is None for x in names))
        self.assertTrue(all(not x["operator_named_exact_variant_confirmed"] for x in names))
        self.assertIsNone(d["official_portal_2002_30_promotion"]["year_beast_card_specific_variant_from_operator_copy"])

    def test_gp_and_mech_promo_skills_are_not_native(self):
        d=self.d
        rows={x["record_id"]:x for x in d["original_registered_2002_documentary_records"]}
        self.assertEqual(rows["CN-PC-3-GP"]["skill_promo"],"落马技")
        self.assertFalse(rows["CN-PC-3-GP"]["original_native_skill_logic_verified"])
        self.assertEqual(rows["CN-PC-4-MECHLEOPARD"]["evidence_label"],"艾迪希洛")
        self.assertEqual(d["official_portal_2002_40_promotion"]["mechanical_leopard_attribute_promo"],{"earth":5,"water":5})
        self.assertEqual(d["official_portal_2002_40_promotion"]["mechanical_leopard_special_skill_promo"],"疾速攻击")
        self.assertFalse(d["official_portal_2002_40_promotion"]["mechanical_leopard_skill_native_runtime_verified"])
        self.assertFalse(d["official_portal_2002_40_promotion"]["dragonboat_four_distinct_pets_verified"])
        self.assertTrue(d["official_portal_2002_40_promotion"]["dragonboat_four_random_attributes"])

    def test_stronger_player_mech_receipt_still_not_original_game_execution(self):
        p=self.d["player_firsthand_2002_mech_issuance_claim"]
        self.assertTrue(p["player_says_bought_and_registered_and_saw_in_pet_menu"])
        self.assertEqual(p["reported_pet_name"],"艾迪希洛")
        self.assertEqual(p["self_reported_level_one_stats"],{"hp":62,"attack":16,"defense":10,"agility":12})
        self.assertEqual(p["skill_effect_player_report_only"],{"defense_pct":-30,"agility_pct":30})
        self.assertFalse(p["original_native_skill_formula_verified"])
        self.assertTrue(p["player_described_year_beast_stats_not_firsthand"])
        self.assertIsNone(p["confirmed_original_CN2002_client_pet_table_ID"])

    def test_white_tiger_promotion_not_guaranteed_or_issued_species(self):
        p=self.d["official_portal_2002_40_promotion"]
        w=p["white_tiger_award_promotion"]
        self.assertEqual(w["name_as_operator_copy"],"白虎")
        self.assertTrue(p["thirdwave_30_card_designs"])
        self.assertFalse(p["thirdwave_30_pets"])
        self.assertEqual(w["promoted_award_inventory_limit"],1000)
        self.assertEqual(w["promo_deadline"],"2002-10-30")
        self.assertTrue(w["operator_copy_text_says_guaranteed_gift"])
        self.assertTrue(w["contemporary_newsroom_says_raffle"])
        self.assertTrue(w["raffle_vs_gift_conflict_unresolved"])
        self.assertIsNone(w["actual_awarded_individuals_verified"])
        self.assertFalse(w["TW_2001_white_tiger_identity_in_CN_deducted"])
        self.assertFalse(w["white_tiger_named_promo_added_as_new_native_pet"])

    def test_eight_sources_dated_correctly_no_2002_raw_html_claimed(self):
        s=self.d["source_register"]
        self.assertEqual(len(s),8)
        self.assertEqual(len(set(x["id"] for x in s)),8)
        self.assertTrue(all(x["original_2002_http_sha256"] is None for x in s))
        self.assertTrue(all(not x["primary_client_binary"] for x in s))
        self.assertEqual(next(x for x in s if "JINGHUA" in x["id"])["exact_publication_day"],"2002-09-17")
        self.assertEqual(next(x for x in s if "2012-RETROSPECTIVE" in x["id"])["grade"],"LATE_RETROSPECTIVE_EDITORIAL_NOT_2002_PRIMARY")

    def test_2002_year_not_closed_no_original_client_published(self):
        d,q=self.d,self.q
        self.assertGreaterEqual(q["current_frontier"]["year"],2002)
        self.assertEqual(q["current_frontier"]["status"],"OPEN_NOT_YEAR_CLOSED")
        self.assertRegex(q["current_frontier"]["next"], r"^PET[0-9]+:")
        self.assertEqual(q["yearly_work_queue"][3]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertIn(d["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertEqual(sum(x["id"]==d["id"] for x in q["root_source_census_receipts"]),1)
        orig=d["original_client_source_limit"]
        self.assertFalse(orig["CN3_0_complete_original_installer_or_pet_master_acquired"])
        self.assertFalse(orig["CN4_0_complete_original_installer_or_pet_master_acquired"])
        self.assertFalse(orig["existing_sa40_sa42_filename_as_4_0_proof"])
        self.assertEqual(orig["new_original_CN2002_client_bytes_acquired"],0)
        self.assertEqual(orig["new_native_pet_id_matches"],0)
        self.assertFalse(d["source_public_raw_commercial_assets_committed"])
        self.assertIsNone(d["all_world_2002_official_pet_species_count"])

    def test_original_state_protected(self):
        d=self.d
        self.assertEqual(d["baseline"]["historical_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(d["baseline"]["historical_current_original_bytes"],2709173)
        self.assertTrue(d["historical_current_blob_unmodified"])
        self.assertEqual(d["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(d["stage_B_wiki"],"GATED")
        self.assertEqual(d["r79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(d["overall_percent"])
        self.assertTrue(d["original_client_source_limit"]["dont_research_paid_marketplaces"])

if __name__=="__main__":
    unittest.main()
