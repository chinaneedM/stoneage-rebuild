"""Regression contract for full 124 original TW1 classic PC client pet dossiers."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_pet_detail31_profile_coverage import audit


ROOT = Path(__file__).resolve().parents[1]


class Pet31ProfileCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit(ROOT)

    def test_all_124_indexed_by_permanent_id(self):
        self.assertEqual(self.report["source_qualified_pet_dossiers"],124)
        self.assertEqual([x["pet_id"] for x in self.report["records"]],
                         ["PET-%06d" % i for i in range(1,125)])
        self.assertEqual(self.report["records"][0]["client_name_original"],"烏力")
        self.assertEqual(self.report["records"][-1]["client_graphic"],100430)

    def test_client_art_not_promoted_to_official_server_identity(self):
        c=self.report["field_coverage_counts_NOT_OFFICIAL_SPECIES_TOTALS"]
        self.assertEqual(c["client_name"],124)
        self.assertEqual(c["sprite_segment"],124)
        self.assertEqual(c["source_motion"],124)
        for field in ("official_pet_id","official_live_release","level1_stats",
                      "initial_stat_ranges","elements","growth","skills",
                      "capture","award","historically_complete"):
            with self.subTest(field=field):
                self.assertEqual(c[field],0)
        self.assertIsNone(self.report["overall_project_percent"])

    def test_missing_faces_have_same_source_motion_fallback_only(self):
        c=self.report["field_coverage_counts_NOT_OFFICIAL_SPECIES_TOTALS"]
        self.assertEqual(c["original_portrait"],120)
        self.assertEqual(c["original_pose_fallback_only"],4)
        self.assertEqual(
            self.report["missing_original_portrait_pet_ids"],
            ["PET-000116","PET-000117","PET-000118","PET-000119"],
        )
        for row in self.report["records"][115:119]:
            self.assertTrue(row["original_pose_fallback_when_face_missing"])
            self.assertIsNone(row["original_portrait_rd"])

    def test_false_or_zero_must_not_mean_unknown(self):
        from tools.stoneage_pet_detail31_profile_coverage import present
        self.assertTrue(present(False))
        self.assertTrue(present(0))
        self.assertFalse(present(None))

    def test_source_registry_original_dossier_hashes_and_pc_scope(self):
        for row in self.report["records"]:
            self.assertEqual(len(row["dossier_git_blob"]),40)
            self.assertEqual(row["source_motion_sequences"],56)
            self.assertTrue(row["dossier_path"].startswith("research/pets/profiles/TW10-G"))
        self.assertEqual(self.report["fully_historical_pet_species_certified"],0)


if __name__=="__main__":
    unittest.main()
