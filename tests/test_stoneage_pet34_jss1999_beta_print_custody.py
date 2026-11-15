import json
from pathlib import Path
import unittest
from tools import stoneage_pet34_jss1999_beta_print_custody as p


class Pet34MagazineSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(Path("research/recovered/STONEAGE-PET34-JSS1999-SEPTEMBER-BETA-PRINT-SOURCE-R1.json").read_text(encoding="utf-8"))

    def test_source_fingerprint_and_not_an_original_official_disc(self):
        r=self.report
        self.assertEqual(r["source"]["sha256"],p.SHA256)
        self.assertEqual(r["source"]["bytes"],p.BYTES)
        self.assertEqual(r["source"]["page_count"],p.PAGES)
        self.assertFalse(r["source"]["native_japanese_text_reliable"])
        self.assertFalse(r["source"]["pdf_original_saved_in_public_repo"])
        self.assertFalse(r["source"]["manual_physical_copy_collation_proven"])
        self.assertTrue(r["preexisting_source_context"]["not_new_betatest_proof"])

    def test_unverified_bonus_not_assumed_to_be_pet_or_1999_release(self):
        r=self.report
        self.assertFalse(r["new_direct_audit"]["beta_bonus_was_pet_proven"])
        self.assertFalse(r["new_direct_audit"]["any_specific_1999_species_obtainable_proven"])
        self.assertFalse(r["new_direct_audit"]["original_beta_game_disc_or_executable_recovered"])
        self.assertEqual(r["new_direct_audit"]["new_qualified_named_pets"],[])
        self.assertIsNone(r["new_direct_audit"]["historical_1999_pet_population_count"])
        self.assertTrue(r["guardrails"]["unreadable_text_layer_does_not_prove_absence_of_pets"])
        self.assertEqual(r["guardrails"]["current_frontier_year"],1999)
        self.assertEqual(r["guardrails"]["active_module"],"PET")
        self.assertEqual(r["guardrails"]["year_review_status"],"NOT_YEAR_AUDITED")

    def test_wrong_bytes_redirect_and_page_count_rejected(self):
        with self.assertRaises(ValueError):
            p.build(b"%PDF-wrong",p.URL,p.PAGES)
        with self.assertRaises(ValueError):
            p.build(b"%PDF-wrong","https://fake.example/a.pdf",p.PAGES)
        with self.assertRaises(ValueError):
            p.build(b"%PDF-wrong",p.URL,42)

    def test_latest_1999_cursor_receipt(self):
        q=json.loads(Path("research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))
        self.assertEqual(q["current_frontier"]["year"],1999)
        self.assertEqual(q["current_frontier"]["status"],"OPEN_NOT_YEAR_CLOSED")
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"],"PET34-JSS1999-SEPTEMBER-BETA-PRINT-CUSTODY-20261115")
        self.assertEqual(q["root_source_census_receipts"][-1]["new_official_named_released_pets"],0)


if __name__=="__main__":
    unittest.main()
