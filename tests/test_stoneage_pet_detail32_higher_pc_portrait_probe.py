import unittest
from tools.stoneage_pet_detail32_higher_pc_portrait_probe import (
    ROOT, ALIAS_TO_PET, audit, select_rows, brief_rd
)
from pathlib import Path
import tempfile
import gzip


class Pet32HigherPcPortraitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit(ROOT)

    def test_four_original_unresolved_avatars_in_higher_pc_sources(self):
        r = self.result
        self.assertEqual(len(r["records"]), 4)
        self.assertEqual([x["pet_id"] for x in r["records"]],
                         ["PET-000116","PET-000117","PET-000118","PET-000119"])
        self.assertEqual([x["album_logical_alias_original_both_versions"] for x in r["records"]],
                         [28085,28086,28087,28088])
        for x in r["records"]:
            self.assertEqual(len(x["tw10_cn50_full_SPR_segment_SHA256_exact"]), 64)
            self.assertFalse(x["tw10_original_album_face_recovered_this_audit"])
            self.assertFalse(x["official_original_pet_issuance_certified"])
        self.assertEqual(r["stats"]["original_TW10_album_faces_newly_authenticated"],0)
        self.assertIsNone(r["boundaries"]["overall_completion_percent"])

    def test_physical_bitmapno_does_not_become_alias(self):
        for x in self.result["records"]:
            for source in ("cn50_saved_5_0_ADRN_physical_bitmapno_same_integer_NOT_alias",
                           "tw85_saved_8_5_ADRN_physical_bitmapno_same_integer_NOT_alias"):
                for row in x[source]:
                    self.assertEqual(int(row["bitmapno"]), x["album_logical_alias_original_both_versions"])
                    self.assertNotIn("map_number",row)
        self.assertTrue(self.result["boundaries"]["same_number_at_physical_ADRN_bitmapno_NOT_a_portrait_alias"])

    def test_exact_field_filter_requires_map_number_not_integer_guess(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.tsv.gz"
            with gzip.open(path,"wt") as f:
                f.write("map_number\tbitmapno\n0\t28085\n28085\t765432\n")
            matches = select_rows(path,"map_number",[28085])
            self.assertEqual([int(x["bitmapno"]) for x in matches[28085]],[765432])

    def test_source_native_rd_hash_structures_not_equal_era_claim(self):
        for x in self.result["records"]:
            for y in x["cn50_saved_5_0_ADRN_plus76_alias_candidate_rows"]:
                self.assertTrue(y["source_RD"]["rd_block_sha256"])
            for y in x["tw85_saved_8_5_ADRN_plus76_alias_candidate_rows"]:
                self.assertTrue(y["rd_sha256"])
                self.assertIn(y["rd_status"],("HEADER_MATCH","HEADER_MISMATCH","BAD_RD_MAGIC","OUT_OF_BOUNDS_OR_SHORT"))


if __name__ == "__main__":
    unittest.main()
