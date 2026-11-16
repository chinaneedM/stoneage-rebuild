"""PET50 official 2000 source-bounded year review, contract/CD and 2001 transition."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"


def data(name):
    return json.loads((REC / name).read_text(encoding="utf-8"))


class Pet50Year2000Bounded(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = data("STONEAGE-PET50-YEAR2000-SOURCE-BOUNDED-AUDIT-R1.json")
        cls.q = data("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_source_bounded_2000_without_species_total(self):
        a, q = self.audit, self.q
        row = q["yearly_work_queue"][1]
        self.assertEqual((a["year"], a["review_status"]), (2000, "SOURCE_BOUNDED_REVIEWED"))
        self.assertFalse(a["historically_complete"])
        self.assertIsNone(a["all_regions_official_live_pet_species_count"])
        self.assertEqual(a["new_named_official_live_pet_release_confirmations"], 0)
        self.assertEqual(a["new_original_year2000_client_bytes_acquired"], 0)
        self.assertEqual(row["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(row["historically_complete"])
        self.assertIsNone(row["historical_species_count"])
        self.assertEqual(row["source_bounded_review_receipt"], "research/recovered/STONEAGE-PET50-YEAR2000-SOURCE-BOUNDED-AUDIT-R1.json")
        self.assertGreaterEqual(len(row["residual_reopen_triggers"]), 5)

    def test_each_2000_region_is_unknown_and_reopenable(self):
        a = self.audit
        q = self.q["yearly_work_queue"][1]
        self.assertEqual(set(a["region_source_reviews"]), {"TW", "CN", "JP", "KR", "OTHER"})
        self.assertEqual(set(q["region_source_reviews"]), set(a["region_source_reviews"]))
        for key, track in a["region_source_reviews"].items():
            self.assertIsNone(track["pet_population"], key)
            self.assertTrue(track["reopen"], key)
        self.assertEqual(a["region_source_reviews"]["TW"]["authentic_tw1_local_named_album_spr_records"], 124)
        self.assertFalse(a["region_source_reviews"]["TW"]["local_name_and_spr_is_live_roster"])
        self.assertFalse(a["region_source_reviews"]["KR"]["period_marketing_is_same_build_live_roster"])
        self.assertFalse(a["region_source_reviews"]["OTHER"]["absence_proven"])

    def test_court_is_licensed_1999_not_1999_taiwan_live_pet(self):
        a = self.audit
        x = a["sources_new_to_pet50"][0]
        self.assertEqual(x["document_date"], "2001-06-21")
        self.assertEqual(x["access_grade"], "MIRROR_HTML_FULL_TEXT_READ_NOT_OFFICIAL_ORIGINAL_BYTES")
        self.assertIsNone(x["original_court_file_sha256"])
        self.assertIsNone(x["original_licensing_contract_copy_sha256"])
        contract = x["claims"][0]
        self.assertEqual(contract["date"], "1999-10-27")
        self.assertFalse(contract["original_contract_directly_read"])
        self.assertFalse(contract["proves_1999_tw_live_game"])
        self.assertFalse(contract["proves_1999_named_pet_release"])
        cd = x["claims"][1]
        self.assertTrue(cd["manual"] and cd["product_serial_registration"] and cd["autoload_install_menu"])
        self.assertEqual(cd["registration_points_stated"], 300)
        self.assertFalse(cd["applies_to_every_2000_kit"])
        self.assertFalse(cd["proves_original_binary_custody"])
        self.assertFalse(x["claims"][2]["physical_stoneage_cd_seized_at_shop"])
        self.assertFalse(x["person_name_address_account_credentials_published"])
        self.assertIsNone(a["date_conflicts_unresolved"][0]["resolution"])

    def test_frontier_moves_only_one_year_and_history_reopens(self):
        a, q = self.audit, self.q
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2000, 2001))
        self.assertEqual(q["yearly_work_queue"][0]["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(q["yearly_work_queue"][0]["historically_complete"])
        self.assertEqual(q["yearly_work_queue"][2]["research_gate"], "NOT_YEAR_AUDITED")
        self.assertEqual(q["current_frontier"]["year"], 2001)
        self.assertEqual(q["current_frontier"]["status"], "OPEN_NOT_YEAR_CLOSED")
        # PET50 records the 2000→2001 transition; later PET work must be free to advance NEXT.
        self.assertRegex(q["current_frontier"]["next"], r"^PET\d+:")
        self.assertEqual(q["current_frontier"]["current_source_acquisition_priority"], "CLIENT_FIRST_VERSION_AUTHENTICATION_AND_PET_RESOURCE_EXTRACTION_BEFORE_EXTERNAL_NEWS")
        row, = [x for x in q["root_source_census_receipts"] if x["id"] == "PET50-YEAR2000-SOURCE-BOUNDED-REVIEW-20261116"]
        self.assertEqual((row["year_frontier_before"], row["year_frontier_after"]), (2000, 2001))
        self.assertTrue(row["reopen_on_new_original_2000_source"])

    def test_private_and_stage_b_guardrails(self):
        a = self.audit
        self.assertFalse(a["private_commercial_originals_committed"])
        self.assertEqual(a["historical_current_blob_unchanged"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(a["baseline"]["current_blob_size_bytes"], 2709173)
        self.assertEqual(a["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(a["stage_B_wiki"], "GATED")
        self.assertEqual(a["r79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(a["overall_completion_percent"])


if __name__ == "__main__":
    unittest.main()
