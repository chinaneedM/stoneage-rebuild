"""Public-only QUEST32 module census and deduplication verification."""
import unittest
from tools.stoneage_quest32_module_audit import audit, verify_snapshot

class Quest32SourceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.derived = verify_snapshot()

    def test_01_all_24_source_reports_reconcile_to_the_catalog(self):
        self.assertEqual(self.derived["report_count"], 24)
        self.assertEqual((self.derived["catalogue_scripts"], self.derived["catalogue_event_TYPE_sections"]), (295, 1349))

    def test_02_occurrences_are_not_distinct_quests_or_scripts(self):
        d = self.derived
        self.assertEqual((d["report_script_occurrences"], d["distinct_selected_paths"], d["matched_catalogue_paths"]), (236, 235, 233))
        self.assertEqual(d["cross_report_duplicate_paths"], {"king/event69_1": ["10", "29"]})

    def test_03_unreferenced_source_files_are_not_falsely_added_to_quest01(self):
        self.assertEqual(self.derived["outside_catalogue_paths"], ["giiru/event/event30_5", "giiru/event/event30_5.old"])

    def test_04_remaining_directory_counts_conserve_295_original_script_paths(self):
        d = self.derived
        self.assertEqual(d["catalogue_not_selected"], 62)
        self.assertEqual(sum(d["remaining_by_directory"].values()), 62)
        self.assertEqual(d["matched_catalogue_paths"] + d["catalogue_not_selected"], 295)

    def test_05_exact_replay(self):
        self.assertEqual(audit(), self.derived)

if __name__ == "__main__":
    unittest.main()
