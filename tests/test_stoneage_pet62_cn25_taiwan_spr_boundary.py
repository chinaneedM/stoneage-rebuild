"""PET62: 2002 CN2.5 Waei product claims, source-exact TW1 ram SPR and non-native reward limits."""
import json
import unittest
from pathlib import Path

REC=Path(__file__).resolve().parents[1]/"research"/"recovered"

def load(name):
    return json.loads((REC/name).read_text(encoding="utf-8"))

class TestPet62Cn25SourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load("STONEAGE-PET62-CN25-GIFT-BLACKSHEEP-QINGLONG-TW1-SOURCE-GRADE-R1.json")
        cls.tw=load("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.tw46=load("STONEAGE-PET46-TW1-ALBUM-NAME-2D-CROSSWALK-R1.json")
        cls.q=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
        cls.pet61=load("STONEAGE-PET61-CN2002-SA30-SA40-OPERATOR-PLAYER-PET-EVIDENCE-R1.json")

    def test_3_marketed_product_rewards_include_two_explicit_names(self):
        d=self.d
        p=d["CN2_5_operator_marketing_pets"]
        self.assertEqual(len(p),3)
        names={x["name_as_printed"] for x in p}
        self.assertEqual(names,{"扑满乌力","年兽","卡伊霍恩"})
        self.assertEqual(sum(x["name_identity_kind"]=="EXACT_NAMED_PET_IN_OPERATOR_MARKETING" or
            x["name_identity_kind"]=="EXACT_NAMED_PET_IN_OPERATOR_REDEMPTION_MARKETING" for x in p),2)
        self.assertEqual(d["new_current_2002_operator_named_pet_promotions_added_as_candidate_rows"],2)
        self.assertEqual(p[0]["promoted_card_bundles"],30000)
        self.assertEqual(p[0]["receipt_probability_in_copy"],"1/3")
        self.assertEqual(p[1]["name_identity_kind"],"PET_FAMILY_UNSPLIT")
        self.assertEqual(p[1]["promoted_card_bundles"],5000)
        self.assertEqual(p[2]["claim_collect_red_sheep_cards"],5)
        self.assertEqual(p[2]["claim_other_patterns_from_remaining_seven"],6)
        self.assertEqual(p[2]["claim_pet_level"],1)
        self.assertEqual(p[2]["claim_WGS_points_award"],1060)
        self.assertTrue(all(x["actual_issued_pets_count"] is None for x in p))
        self.assertTrue(all(x["server_native_original_pet_id"] is None for x in p))

    def test_original_TW10_ram_same_named_SPR_is_asset_not_CN2002_issuance(self):
        d=self.d
        x=d["existing_TW10_original_client_same_name_SPR_candidate"]
        r=[z for z in self.tw["records"] if z["name_as_written"]=="卡伊霍恩"]
        self.assertEqual(len(r),1)
        r=r[0]
        self.assertEqual((x["source_id"],x["original_name"]), (r["id"],r["name_as_written"]))
        self.assertEqual(x["original_graphic_number"],r["graphic_number"])
        self.assertEqual(x["original_name_row_sha256"],r["source_row_sha256"])
        self.assertEqual(x["source_file_offset"],r["source_file_offset"])
        self.assertEqual(x["original_full_spr_segment_sha256"],r["spr_original_segment_sha256"])
        self.assertEqual((x["source_sequences"],x["source_frame_positions"]),(r["source_sequences"],r["source_frame_positions"]))
        self.assertEqual(x["portrait_rd_sha256"],r["portrait_rd"]["sha256"])
        self.assertEqual(x["archive_sha256"],self.tw["archive"]["sha256"])
        self.assertEqual(x["zip_members_crc_verified"],379)
        c=[z for z in self.tw46["candidate_records"] if z["client_original_album_name"]=="卡伊霍恩"]
        self.assertEqual(len(c),1)
        self.assertEqual(c[0]["pet07_original_whole_SPR_sha256"],x["original_full_spr_segment_sha256"])
        self.assertEqual(c[0]["graphic_number"],x["original_graphic_number"])
        self.assertFalse(x["TW1_original_local_asset_proves_live_2002_CN_issuance"])
        self.assertFalse(x["matched_2002_CN_same_SPR_hash_proven"])
        self.assertFalse(x["matched_2002_CN_same_skill_or_stats_proven"])
        self.assertFalse(x["privately_stored_source_pixels_republished"])

    def test_black_sheep_firsthand_claim_with_mainland_taiwan_caveat(self):
        b=self.d["CN2_5_20020520_firstperson_black_sheep"]
        self.assertEqual(b["claimed_pet_reward_name"],"黑羊")
        self.assertTrue(b["source_player_says_successful_quest_completion"])
        self.assertEqual(self.d["sources"]["CN25_PLAYER_20020520_BLACK_SHEEP"]["displayed_date"],"2002-05-20")
        self.assertTrue(b["crosscheck_portal_quest_guide"]["guide_says_black_sheep_reward"])
        self.assertTrue(b["crosscheck_portal_quest_guide"]["explicit_taiwan_end_reward_may_differ_from_mainland"])
        self.assertFalse(b["mainland_live_server_independently_authenticated"])
        self.assertFalse(b["can_promote_to_ALL_CN2_5_official_reward_rule"])
        self.assertFalse(b["claim_original_game_dialogue_or_byte_observation_verified"])

    def test_qinglong_2002_cn_card_player_claim_not_taiwan_reputation_proof(self):
        x=self.d["CN2002_qinglong_Kaien"]
        self.assertEqual((x["name"],x["date"]),("凯恩","2002-12-27"))
        self.assertTrue(x["player_claim_fourth_wave_Lucky_Card_redemption"])
        self.assertFalse(x["firstperson_live_observation"])
        self.assertTrue(x["TW_2002_May_timed_2000_reputation_requirement_only_late_copy"])
        self.assertFalse(x["same_issuer_offer_mechanism_or_server_proven"])
        self.assertFalse(x["CN_2002_official_operator_4th_wave_redemption_notice_recovered"])
        self.assertFalse(x["TW_2002_official_operator_May_event_notice_recovered"])
        self.assertIsNone(x["first_release_date"])

    def test_satire_not_firstparty_2002_release_dates(self):
        src=self.d["sources"]["CN_20020504_SATIRE_NEGATIVE_CONTROL"]
        negative=self.d["negative_control"]
        self.assertIn("搞笑篇",src["explicit_headline"])
        self.assertEqual(src["source_kind"],"PLAYER_SATIRE_NOT_OPERATOR_NOTICE")
        self.assertFalse(src["may_be_used_as_exact_waei_2002_release_dates"])
        self.assertFalse(src["may_be_used_as_black_sheep_official_release_proof"])
        self.assertFalse(negative["satire_used_as_2002_official_date_or_release_proof"])
        self.assertTrue(negative["comic_reprint_not_first_party"])

    def test_other_region_custody_remains_separate_and_open(self):
        d=self.d
        tw=d["TW2002_period_press_review"]
        self.assertEqual(tw["year"],2002)
        self.assertEqual(tw["source_depth"],"2002_DATED_NEWS_SEARCH_INDEX_ONLY_DIRECT_PAGE_403")
        self.assertEqual(tw["new_pet_names_from_primary_source"],[])
        self.assertFalse(tw["proof_live_same_2002_client_pets"])
        self.assertTrue(tw["release_not_equal_CN2003_5_0"])
        self.assertIsNone(d["JP_KR_2002_gaps"]["KR"]["pet_population"])
        self.assertFalse(d["JP_KR_2002_gaps"]["JP"]["historical_2002_service_absent_proven"])
        self.assertFalse(d["JP_KR_2002_gaps"]["OTHER"]["historical_absence_proven"])
        self.assertEqual(len(d["unresolved_issues"]),10)

    def test_2002_old_four_record_count_and_frontier_not_changed(self):
        d,q=self.d,self.q
        self.assertGreaterEqual(q["current_frontier"]["year"],2002)
        self.assertEqual(q["yearly_work_queue"][3]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertRegex(q["current_frontier"]["next"],r"^PET[0-9]+:")
        self.assertIn(d["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertEqual(q["yearly_work_queue"][3]["documentary_event_count_NOT_species"],4)
        self.assertEqual(q["yearly_work_queue"][3]["documented_release_event_ids_from_existing_PET25_PET26"],
            [x["record_id"] for x in self.pet61["original_registered_2002_documentary_records"]])
        self.assertEqual(d["year2002_prior_source_records_from_PET25_26"],4)
        self.assertEqual(d["new_historical_PET25_confirmed_official_release_event_records_created"],0)
        self.assertEqual(d["new_2002_official_live_game_pet_issuance_verified_by_original_native_bytes"],0)
        self.assertEqual(d["new_2002_original_client_binary_bytes"],0)
        self.assertEqual(d["new_native_pet_ids"],0)
        self.assertIsNone(d["global_2002_historical_pet_population"])
        self.assertEqual(sum(x["id"]==d["id"] for x in q["root_source_census_receipts"]),1)

    def test_original_historical_state_and_rights_preserved(self):
        d=self.d
        self.assertEqual(d["preserved_historical_current_state"]["sha256_git_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(d["preserved_historical_current_state"]["raw_bytes"],2709173)
        self.assertTrue(d["preserved_historical_current_state"]["unmodified"])
        self.assertTrue(d["strict_no_secondhand_paid_marketplace_research"])
        self.assertFalse(d["copyright_original_asset_bytes_publicly_committed"])
        self.assertEqual((d["stage_A"],d["stage_B_wiki"],d["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
        self.assertIsNone(d["overall_percent"])

if __name__=="__main__":
    unittest.main()
