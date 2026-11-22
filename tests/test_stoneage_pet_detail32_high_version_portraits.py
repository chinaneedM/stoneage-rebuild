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
    def test_four_dossiers_link_both_versions_without_claiming_tw10_portraits(self):
        import json
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root /
            "research/pets/PET-DETAIL-EVIDENCE32-TW1-FOUR-CN50-PATCH129-FACE-CANDIDATES-R1.json"
        ).read_text(encoding="utf-8"))
        self.assertEqual(receipt["source_dossier_count"], 4)
        self.assertEqual(receipt["r43_git_blob"],
                         "dbc1b46fe14f105898757d1199ac338e9971c330")
        for row in self.report["records"]:
            path = root / ("research/pets/profiles/TW10-G%d.json" % row["tw10_original_graphic"])
            dossier = json.loads(path.read_text(encoding="utf-8"))
            app = dossier["appearance"]
            original = app["portrait"]
            self.assertIsNone(original["source_rd_bitmap_number"])
            self.assertIsNone(original["source_rd_sha256"])
            self.assertEqual(original["status"], "OPEN_NOT_PROVEN")
            later = app["higher_version_portrait_source_candidates"]
            self.assertEqual(later["original_taiwan_1_0_face_alias"],
                             row["original_album_face_alias"])
            self.assertTrue(later["two_distinct_rd_contents_not_selected"])
            self.assertIsNone(later["native_runtime_winning_candidate"])
            self.assertIsNone(later["actual_original_taiwan_1_0_portrait"])
            for source_key, evidence_key in (
                ("cn50_preserved_pc5", "CN50"),
                ("patch129_original_pc_resource", "PATCH129")
            ):
                self.assertEqual(
                    later[source_key]["candidates"],
                    row["later_classic_pc_sources"][evidence_key]["candidates"]
                )
            self.assertFalse(dossier["status"]["all_fields_historically_complete"])
            self.assertIsNone(dossier["actual_official_pet_identity"]["source_pet_id"])
            self.assertIsNone(dossier["growth"]["growth_rate"])

    def test_never_claim_new_species_or_new_pixel_recovery(self):
        self.assertEqual(self.report["pet_official_live_issuance_newly_proven"],0)
        self.assertTrue(self.report["no_new_original_pixels_read"])
        self.assertIsNone(self.report["overall_percent"])

if __name__ == "__main__":
    unittest.main()
