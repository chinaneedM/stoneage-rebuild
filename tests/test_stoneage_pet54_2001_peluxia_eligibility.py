"""PET54: 2001 operator's named web pet is not a 2001 live pet or 2001 client identity."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "research" / "recovered"
ID = "PET54-2001-CNTW-PELUXIA-NAME-REWARD-CONFLICT-20261116"

class TestPET54Year2001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = json.loads((P / "STONEAGE-PET54-2001-PELUXIA-REWARD-ELIGIBILITY-SOURCE-R1.json").read_text(encoding="utf-8"))
        cls.q = json.loads((P / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))

    def test_old_operator_web_page_source_exact_not_client_issuance(self):
        e = self.e["2001_cn_official_named_web_preexisting"]
        self.assertEqual(e["archive_capture"], "20011023181629")
        self.assertEqual(e["body_sha256"], "2c7aea8d0319c2070d5c7590a95bfc892c2463deb76c5b95fca8c281549c76f0")
        self.assertEqual(e["existing_record_id"], "waei-cn20:new-pet-web-position:081")
        self.assertEqual(e["name"], "佩露夏")
        self.assertEqual(e["web_position_not_pet_id"], 81)
        self.assertTrue(e["october_archive_before_reported_november_1_mainland_2_0_launch"])
        self.assertFalse(e["server_issuance_or_native_build_proven"])
        self.assertFalse(e["image_bytes_newly_recovered"])
        self.assertIn("NOT_LIVE_RELEASE", e["qualification"])

    def test_undated_entry_and_dated_player_claims_not_one_rule(self):
        e = self.e
        old = e["17173_undated_pet_page"]
        submission = e["2003_sina_player_submitted_pet_table"]
        retrospective = e["2012_17173_taiwan_retrospective"]
        self.assertIsNone(old["page_original_publication_date"])
        self.assertEqual((old["event_date_mentioned"], old["event_eligibility_reincarnation_claim"], old["event_eligibility_level_claim"]), ("2001-12-01", 5, 125))
        self.assertFalse(old["prize_actually_granted_proven"])
        self.assertFalse(old["client_stats_authenticated"])
        self.assertEqual((submission["published"], submission["byline"], submission["level_claim"]), ("2003-04-03", "网友投稿", 135))
        self.assertFalse(submission["operator_first_party_statement"])
        self.assertEqual((retrospective["published"], retrospective["claimed_year_month"], retrospective["region"], retrospective["level_claim"]), ("2012-02-21", "2001-12", "TW", 125))
        conflict = e["eligibility_conflict"]
        self.assertEqual(conflict["levels_in_sources"], [125, 135])
        self.assertTrue(conflict["unresolved"])
        self.assertTrue(conflict["source_periods_and_regions_noninterchangeable"])
        self.assertTrue(conflict["client_server_eligibility_logic_unrecovered"])

    def test_later_mixed_local_album_is_not_original_game_species(self):
        e = self.e["preserved_local_client_source_candidate"]
        self.assertEqual(e["scope"], "EXISTING_MIXED25_PRESERVED_CLIENT_SUBTREE_NOT_AUTHENTICATED_OFFICIAL_BUILD")
        self.assertEqual((e["name"], e["saved_album_slot"], e["native_table_face_value"], e["native_table_index"]), ("佩露夏", 125, 28196, 233))
        self.assertFalse(e["same_build_2001_cn_tw_proven"])
        self.assertFalse(e["original_sprite_segments_2001_authenticated"])
        self.assertFalse(e["official_server_pet_population_proven"])

    def test_pet53_iso_has_new_warning_not_retroactive_correction(self):
        e = self.e["previous_pet53_iso_provenance_caution"]
        self.assertEqual(e["catalogue_filename"], "PCFan200111.iso")
        self.assertEqual(e["later_directory_claimed_pc_fan_journal_start_year"], 2003)
        self.assertTrue(e["publication_chronology_compatibility_unknown"])
        self.assertTrue(e["not_same_2001_disc_identity_proven"])
        self.assertTrue(e["no_direct_iso_bytes"])
        self.assertTrue(e["sha1_from_store_listing_not_recalculated"])

    def test_forward_only_receipts_open_year_and_historical_state(self):
        q, e = self.q, self.e
        ids = [x["id"] for x in q["root_source_census_receipts"]]
        self.assertEqual(ids.count(ID), 1)
        self.assertEqual(ids.count("PET53-CN2001-PCFAN-ISO-SINA-FAMILY-PET-PRIZES-20261116"), 1)
        self.assertLess(ids.index("PET53-CN2001-PCFAN-ISO-SINA-FAMILY-PET-PRIZES-20261116"), ids.index(ID))
        self.assertGreaterEqual(q["current_frontier"]["year"], 2001)
        self.assertIn(next(x for x in q["yearly_work_queue"] if x["year"] == 2001)["research_gate"], {"NOT_YEAR_AUDITED","SOURCE_BOUNDED_REVIEWED"})
        self.assertEqual(q["active_module"], "PET")
        self.assertEqual((e["new_2001_original_client_bytes"], e["new_2001_named_native_pet_id_links"], e["new_2001_official_game_pet_issuance_proofs"]), (0, 0, 0))
        self.assertIsNone(e["historical_2001_official_pet_species_count"])
        self.assertEqual(e["baseline"]["current_original_sha"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(e["baseline"]["current_original_size"], 2709173)
        self.assertEqual((e["stage_A"], e["stage_B_wiki"], e["r79"]), ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING"))
        self.assertIsNone(e["overall_percent"])

if __name__ == "__main__":
    unittest.main()
