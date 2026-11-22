"""Exact source and strict cross-version boundary for four missing TW1 faces."""
import unittest
from tools.stoneage_pet_detail32_high_version_portraits import collect

class Pet32Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = collect()
    def test_original_faces_still_absent_in_tw10(self):
        self.assertEqual(self.report["source_dossier_count"], 4)
        self.assertEqual(self.report["original_tw10_portraits_recovered"], 0)
        for item in self.report["records"]:
            self.assertIsNone(item["tw10_album_portrait"])
            self.assertEqual(item["later_classic_pc_sources"]["TW10"]["source_occurrences"], 0)
            self.assertIsNone(item["candidate_selection"])
    def test_two_distinct_candidates_in_both_high_version_carriers(self):
        ids=[28085, 28086, 28087, 28088]
        self.assertEqual([item["original_album_face_alias"] for item in self.report["records"]], ids)
        for item in self.report["records"]:
            later = item["later_classic_pc_sources"]
            self.assertEqual(later["CN50"]["distinct_rd_contents"],2)
            self.assertEqual(later["PATCH129"]["distinct_rd_contents"],2)
            self.assertEqual(len(later["CN50"]["candidates"]),2)
            self.assertEqual(
                {(x["rd_bytes"],x["rd_sha256"]) for x in later["CN50"]["candidates"]},
                {(x["rd_bytes"],x["rd_sha256"]) for x in later["PATCH129"]["candidates"]})
            self.assertFalse(item["native_runtime_face_selector_verified"])
            self.assertFalse(item["is_original_TW1_portrait_proven"])
    def test_never_claim_new_species_or_new_pixel_recovery(self):
        self.assertEqual(self.report["pet_official_live_issuance_newly_proven"],0)
        self.assertTrue(self.report["no_new_original_pixels_read"])
        self.assertIsNone(self.report["overall_percent"])

if __name__ == "__main__":
    unittest.main()
