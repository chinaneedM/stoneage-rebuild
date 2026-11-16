"""PET66: dated Taiwanese and mainland 2003 pet-source boundaries."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"

class TestPet66(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads((REC / "STONEAGE-PET66-2003-TW6-CN7-PET-SOURCE-R1.json").read_text(encoding="utf8"))
        cls.q = json.loads((REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf8"))

    def record(self, name):
        return next(x for x in self.d["primary_source_records"] if x["id"] == name)

    def test_tw_2003_promise_is_not_server_grant(self):
        a = self.record("TW_20030221_TGS_WATER_JELLY")
        self.assertEqual((a["printed_pet_name"], a["printed_category"]), ("貝沃特", "水母"))
        self.assertIn("403", a["access"])
        self.assertFalse(a["pet_delivered_to_any_account_verified"])
        b = self.record("TW_20030319_WEEWEE_LOTTERY")
        self.assertEqual((b["required_existing_pet"], b["minimum_level"]), ("威威", 30))
        self.assertEqual(b["advertised_prize_labels"], ["水藍人龍", "黑鳥"])
        self.assertTrue(b["separate_prize_categories_from_species"])
        self.assertFalse(b["actual_awards_verified"])

    def test_cn_2003_preexisting_suzaku_and_native_carrier_gap(self):
        a = self.record("CN_20031217_SUZAKU_AUCTION")
        self.assertEqual(a["printed_pet_names"], ["朱雀", "菲奇亚"])
        self.assertTrue(a["prior_record_already_has_named_suzaku"])
        self.assertEqual(a["new_species_discovery_count"], 0)
        self.assertFalse(a["actual_auction_winner_verified"])
        c = self.record("CN_20031219_CLIENT_7_DISTRIBUTION")
        self.assertEqual(c["original_advertised_filenames"], ["StoneAge7.rar"])
        self.assertEqual(c["currently_retrieved_original_bytes"], 0)
        self.assertIsNone(c["original_archive_sha256"])
        self.assertFalse(c["single_client_all_old_vers_compatible"])
        self.assertTrue(c["original_client_distribution_claim_not_live_pets"])

    def test_distinguish_2004_followup_and_2003_player_claim(self):
        a = self.record("CN_20040112_SUZAKU_FOLLOWUP_EXCLUDED_FROM_2003")
        self.assertEqual(a["year_of_activity"], 2004)
        self.assertTrue(a["do_not_backdate_into_2003"])
        self.assertTrue(a["promised_quantity_not_actual_grants"])
        b = self.record("CN_20030707_GOLD_APE_PLAYER")
        self.assertEqual(b["grade"], "CONTEMPORANEOUS_FIRST_PERSON_PLAYER_REPORT")
        self.assertTrue(b["same_pet_as_previous_CN20_catalog_not_established"])
        self.assertFalse(b["official_operator_same_build_id_verified"])

    def test_forward_only_year_and_global_source_boundary(self):
        d,q=self.d,self.q
        self.assertEqual(q["current_frontier"]["year"],2003)
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"],d["id"])
        self.assertTrue(q["current_frontier"]["next"].startswith("PET67:"))
        y=next(x for x in q["yearly_work_queue"] if x["year"]==2003)
        self.assertEqual(y["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(y["documentary_event_count_NOT_species"],1)
        self.assertEqual(sum(x["id"]==d["id"] for x in q["root_source_census_receipts"]),1)
        self.assertEqual(len([x for x in y["partial_source_review_receipts"] if x["id"]==d["id"]]),1)
        self.assertEqual(d["new_2003_original_official_client_bytes"],0)
        self.assertEqual(d["new_confirmed_official_server_pet_grants"],0)
        self.assertIsNone(d["new_true_global_official_species_count"])
        self.assertTrue(d["historical_CURRENT_untouched"])
        self.assertTrue(d["no_paid_marketplace"])
        self.assertFalse(d["commercial_pixels_or_installers_published"])
        self.assertEqual(d["startup"]["historical_CURRENT_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")

if __name__=="__main__":
    unittest.main()
