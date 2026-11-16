"""PET49 guards for operator-issued 2000 TW software-sales claims vs original pets."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"


def receipt(filename):
    return json.loads((REC / filename).read_text(encoding="utf-8"))


class Pet49WayiOperatorProspectus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = receipt("STONEAGE-PET49-TW2000-OPERATOR-PROSPECTUS-SOURCE-R1.json")

    def test_two_issuer_sources_different_publication_years(self):
        d = self.d
        self.assertEqual([x["publication_date"] for x in d["documents"]], ["2003-05-20", "2004-02-10"])
        self.assertTrue(all(x["issuer"] == "華義國際數位娛樂股份有限公司" for x in d["documents"]))
        self.assertTrue(all("www.wayi.net" == x["issuer_original_host"] for x in d["documents"]))
        self.assertTrue(all(x["historical_claim_year"] == 2000 for x in d["documents"]))

    def test_disclosure_sales_are_not_client_or_species_counts(self):
        d = self.d
        s = d["reported_year_2000_software_product_sales"]
        self.assertEqual((s["units_thousands"], s["units_approx"]), (278, 278000))
        self.assertEqual(d["reported_year_2000_WGS_card_sales"]["units_approx"], 428000)
        self.assertEqual(s["unit_as_written"], "仟套")
        self.assertFalse(s["claims_same_executable_build"])
        self.assertFalse(s["claims_same_physical_disc"])
        self.assertFalse(s["claims_pet_species_count"])
        self.assertFalse(d["reported_year_2000_WGS_card_sales"]["claims_pet_species_count"])
        self.assertIsNone(d["regional_version_identity"]["pet_roster_officially_live_total"])
        self.assertIsNone(d["regional_version_identity"]["release_day_exact"])

    def test_pdf_is_indexed_not_raw_authenticated(self):
        d = self.d
        for source in d["documents"]:
            self.assertEqual(source["access_status"], "OPERATOR_HOSTED_PDF_INDEXED_TEXT_NOT_RAW_VERIFIED")
            self.assertIsNone(source["raw_pdf_sha256"])
            self.assertIsNone(source["raw_pdf_size_bytes"])
            self.assertIsNone(source["pdf_page_number"])
            self.assertEqual(source["pdf_screenshot_result"], "403_FORBIDDEN")
            self.assertFalse(source["original_binary_downloaded"])
        self.assertFalse(d["raw_source_bytes_preserved_public_repo"])

    def test_2000_vs_2001_and_2000_pet_lock(self):
        d = self.d
        z = d["year_2001_separation"]
        self.assertEqual(z["ownership_contract_with_digipark_month"], "2001-03")
        self.assertEqual((z["pet_bundle_150_point_series_year"], z["pet_bundles_200_point_year"]), (2001, 2001))
        self.assertTrue(z["cannot_disprove_prior_three_cards_2000_august"])
        self.assertEqual(d["prior_original_client_reused_not_reextracted"]["named_graphic_records"], 124)
        self.assertEqual(len(receipt("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")["records"]), 124)
        self.assertFalse(d["prior_original_client_reused_not_reextracted"]["claimed_2000_live_roster"])
        self.assertEqual(d["new_official_named_live_pet_release_confirmations"], 0)
        self.assertEqual(d["new_authentic_2000_client_bytes_acquired"], 0)
        self.assertIsNone(d["global_historical_pet_species_count"])
        self.assertEqual((d["active_module"], d["historical_year_frontier"], d["year_2000_gate"]), ("PET", 2000, "OPEN"))
        self.assertEqual(d["original_current_state_git_blob_unmodified"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(d["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertIsNone(d["overall_completion_percent"])


if __name__ == "__main__":
    unittest.main()
