import json
import unittest
from pathlib import Path


class Pet35HistoricalSourceBoundary(unittest.TestCase):
    def test_later_operator_is_not_1999_named_pet(self):
        d = json.loads(Path("research/recovered/STONEAGE-PET35-JP1999-OPERATOR-AND-PRINT-LEADS-R1.json").read_text(encoding="utf-8"))
        s = d["operator_statement"]
        self.assertEqual(s["published"], "2005-04-04")
        self.assertTrue(s["jss_1999_operation_recalled"])
        self.assertFalse(s["same_build_1999_pet_release_verified"])
        self.assertFalse(s["original_raw_http_fetched_this_audit"])
        self.assertIsNone(s["source_html_sha256"])
        self.assertEqual(s["specific_released_1999_pet_names"], [])
        self.assertEqual(d["new_qualified_official_1999_named_pet_releases"], [])
        self.assertIsNone(d["historical_1999_pet_population"])
        self.assertEqual(d["year_review_status"], "NOT_YEAR_AUDITED")
        self.assertEqual(d["active_module"], "PET")

    def test_catalogue_is_unread_not_no_pets(self):
        d = json.loads(Path("research/recovered/STONEAGE-PET35-JP1999-OPERATOR-AND-PRINT-LEADS-R1.json").read_text(encoding="utf-8"))
        p = d["contemporary_print_leads"]
        self.assertEqual(len(p["listed_issues"]), 5)
        self.assertFalse(p["source_pages_read_this_audit"])
        self.assertFalse(p["pet_page_found_this_audit"])
        self.assertFalse(p["scan_sha256_verified"])
        self.assertFalse(p["issue_016_download_size_verified"])
        self.assertEqual(p["source_status"], "UNREAD_SOURCE_LEAD_ONLY")
        q = json.loads(Path("research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))
        self.assertEqual(q["current_frontier"]["year"], 1999)
        self.assertEqual(q["yearly_work_queue"][0]["research_gate"], "NOT_YEAR_AUDITED")
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"], "PET35-JP1999-SUCCESSOR-OPERATOR-PRINT-LEADS-20261115")
        self.assertEqual(d["preserved_current_blob"], "c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
