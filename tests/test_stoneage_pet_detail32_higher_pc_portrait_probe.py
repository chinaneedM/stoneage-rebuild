import hashlib
import json
import struct
import unittest
from tools.stoneage_pet_detail32_higher_pc_portrait_probe import (
    ROOT, ALIAS_TO_PET, audit, select_rows, brief_rd
)
from pathlib import Path
import tempfile
import gzip
from tools.stoneage_pet_detail33_portrait_pixels import PET32, RECEIPT, compare_album_cohort


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

    def test_pet32_collision_projection_shows_last_of_two_records(self):
        from json import loads
        from pathlib import Path
        expected = [(100389, 126222, 126066), (100390, 126223, 126067),
                    (100391, 126224, 126068), (100392, 126225, 126069)]
        for row, (graphic, saved_cn_id, distinct_tw_id) in zip(self.result["records"], expected):
            with self.subTest(pet=row["pet_id"]):
                self.assertEqual(row["tw10_original_graphic"], graphic)
                self.assertEqual(len(row["cn50_saved_5_0_ADRN_plus76_alias_candidate_rows"]), 1)
                cn = row["cn50_saved_5_0_ADRN_plus76_alias_candidate_rows"][0]
                self.assertEqual(int(cn["source_RD"]["bitmapno"]), saved_cn_id)
                self.assertEqual([int(cn["source_RD"][k]) for k in ("width","height")], [96,104])
                variants = row["tw85_saved_8_5_native_exact_RD_from_official_patch"]
                self.assertEqual(len(variants), 2)
                self.assertEqual([int(v["original_2005_official_patch"]["bitmapno"]) for v in variants],
                                 [distinct_tw_id,saved_cn_id])
                self.assertNotEqual(variants[0]["saved_tw85_native_RD_sha256_if_source_exact"],
                                    variants[1]["saved_tw85_native_RD_sha256_if_source_exact"])
                self.assertEqual(variants[1]["saved_tw85_native_RD_sha256_if_source_exact"],
                                 cn["source_RD"]["rd_block_sha256"])
                profile = loads((ROOT / f"research/pets/profiles/TW10-G{graphic}.json").read_text(encoding="utf8"))
                self.assertIsNone(profile["appearance"]["portrait"]["source_rd_bitmap_number"])
                self.assertIsNone(profile["appearance"]["portrait"]["source_rd_sha256"])
                cross = profile["appearance"]["cross_version_original_portrait_rd_candidates"]
                self.assertEqual(cross["CN50_preserved_PC5"]["native_bitmapno"], saved_cn_id)
                self.assertEqual(len(cross["TW85_saved_PC_higher_variants"]),2)
                self.assertTrue(cross["original_TW10_portrait_remains_missing"])
                self.assertFalse(cross["CN50_preserved_PC5"]["actual_pixel_decoded_this_run"])

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
            for y in x["tw85_official_2005_patch_plus76_alias_candidates"]:
                self.assertEqual(
                    int(y["original_2005_official_patch"]["map_number"]),
                    x["album_logical_alias_original_both_versions"]
                )
                if y["same_saved_tw85_native_RD_exact_original_record"]:
                    self.assertTrue(y["saved_tw85_native_RD_sha256_if_source_exact"])
                    self.assertTrue(y["saved_tw85_native_indexes"])
                else:
                    self.assertIsNone(y["saved_tw85_native_RD_sha256_if_source_exact"])

    def test_pet33_receipt_and_profiles_preserve_both_source_verified_variants(self):
        replay = json.loads((ROOT / RECEIPT).read_bytes())
        self.assertEqual(
            replay["sources"][PET32]["sha256"],
            hashlib.sha256((ROOT / PET32).read_bytes()).hexdigest(),
        )
        self.assertEqual(replay["verified_pixel_blocks"], 8)
        self.assertEqual(replay["tw10_native_portraits_newly_verified"], 0)
        self.assertFalse(replay["original_game_or_native_portrait_selection_observed"])
        cohort = replay["album_cohort"]
        self.assertEqual(cohort["tw10_match_count_by_alias"], {"0": 4, "1": 120})
        self.assertEqual(cohort["cn50_match_count_by_alias"], {"1": 120, "2": 4})
        self.assertEqual(cohort["cn50_match_count_by_alias"], cohort["mixed25_match_count_by_alias"])
        self.assertEqual(cohort["tw10_missing_aliases"], cohort["later_sources_duplicate_aliases"])

        for original, record in zip(self.result["records"], replay["records"], strict=True):
            with self.subTest(pet=record["pet_id"]):
                self.assertEqual(record["pet_id"], original["pet_id"])
                variants = record["variants"]
                self.assertEqual(len(variants), 2)
                self.assertNotEqual(variants[0]["indexed_pixels_sha256"], variants[1]["indexed_pixels_sha256"])
                self.assertGreater(record["differing_index_positions"], 0)
                before = original["tw85_saved_8_5_native_exact_RD_from_official_patch"]
                for variant, candidate in zip(variants, before, strict=True):
                    self.assertEqual(variant["rd_sha256"], candidate["saved_tw85_native_RD_sha256_if_source_exact"])
                    self.assertEqual(variant["indexed_pixel_count"], 96 * 104)
                    self.assertEqual(
                        variant["mixed25_adrn_record_sha256"],
                        candidate["original_2005_official_patch"]["record_sha256"],
                    )

                profile_path = ROOT / "research/pets/profiles" / f"TW10-G{record['tw10_graphic']}.json"
                appearance = json.loads(profile_path.read_bytes())["appearance"]
                profile = appearance["cross_version_original_portrait_rd_candidates"]
                self.assertIsNone(appearance["portrait"]["source_rd_bitmap_number"])
                self.assertEqual(profile["pixel_replay"]["physical_bitmap_numbers_in_ADRN_order"],
                                 [variant["physical_bitmap_number"] for variant in variants])
                self.assertEqual(profile["pixel_replay"]["evidence_path"], RECEIPT)
                self.assertTrue(all(v["same_real_RD_bytes_as_preserved_CN50"]
                                    for v in profile["TW85_saved_PC_higher_variants"]))

    def test_album_cohort_requires_ordered_occurrences_not_last_alias_only(self):
        first = struct.pack("<I72xI", 126066, 28085)
        last = struct.pack("<I72xI", 126222, 28085)
        native = struct.pack("<I72xI", 8010, 28001)
        result = compare_album_cohort(native, native + first + last, native + first + last,
                                      {28001, 28085}, {28085})
        self.assertEqual(result["cn50_match_count_by_alias"], {1: 1, 2: 1})
        with self.assertRaisesRegex(ValueError, "unexpected missing, duplicate or changed record"):
            compare_album_cohort(native, native + last, native + first + last,
                                 {28001, 28085}, {28085})
        with self.assertRaisesRegex(ValueError, "unexpected missing, duplicate or changed record"):
            compare_album_cohort(native, native + last + first, native + first + last,
                                 {28001, 28085}, {28085})


if __name__ == "__main__":
    unittest.main()
