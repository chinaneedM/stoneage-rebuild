"""PET-DETAIL37 source-pinned PC-only original RD overlap and non-upgrade gates."""
import json
import unittest
from pathlib import Path
from tools.stoneage_pet_detail37_tw10_cn50_rd_overlap import audit

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/pets/PET-DETAIL-EVIDENCE37-TW10-CN50-ORIGINAL-RD-OVERLAP-R1.json"


class PetDetail37(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit()
        cls.permanent = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_exact_replay_persisted_305_records(self):
        self.assertEqual(self.report, self.permanent)

    def test_disjoint_120_4_181_source_graded_partition(self):
        c = self.report["counts"]
        self.assertEqual((c["cn50_compiled_named_rows"], c["tw10_source_qualified_named_spr_bridges"],
                          c["tw10_original_portrait_exact_rd_sha256_reuse"],
                          c["tw10_native_portrait_missing_with_two_later_rd_variants"],
                          c["cn50_named_local_rows_without_qualified_tw10_identity_bridge"]),
                         (305,124,120,4,181))
        self.assertEqual(c["cn50_last_projection_rd_hashes_unique"], 305)
        self.assertEqual(len({r["cn50_album_ordinal"] for r in self.report["records"]}),305)
        for x in self.report["records"]:
            self.assertFalse(x["official_live_release_verified_by_this_crosswalk"])
            self.assertFalse(x["all_native_adrn_alias_candidates_enumerated"])

    def test_exact_hashes_are_not_numeric_or_name_only_matches(self):
        exact = [x for x in self.report["records"] if x["comparison_grade"] == "TW10_ORIGINAL_RD_SHA256_EXACT_CN50"]
        self.assertEqual(len(exact),120)
        for x in exact:
            self.assertEqual(x["cn50_last_projected_rd_sha256"], x["tw10_original_portrait_rd_sha256"])
            self.assertEqual(len(x["tw10_full_original_spr_sha256"]),64)

    def test_four_missing_original_avatars_retain_both_later_variants(self):
        four = self.report["four_original_tw10_portrait_gaps_with_existing_later_variants"]
        self.assertEqual([x["tw10_original_name"] for x in four],
                         ["洛克斯","阿伊薩","格洛格魯","朵洛將恩"])
        self.assertEqual([x["later_carrier_variant_bitmapnos"] for x in four],
                         [[126066,126222],[126067,126223],[126068,126224],[126069,126225]])
        self.assertTrue(all(x["cn50_last_projection_is_not_native_selector"] for x in four))

    def test_original_egg_and_copyright_boundary(self):
        egg=next(x for x in self.report["records"] if x["cn50_compiled_name"]=="宠物蛋")
        self.assertEqual(egg["comparison_grade"],"CN50_NAMED_LOCAL_ONLY_NO_TW10_BRIDGE")
        for val in self.report["claims_not_made"].values(): self.assertFalse(val)
        self.assertFalse(self.report["source_qualifications"]["new_source_original_binary_bytes_read_this_unit"])
        self.assertFalse(self.report["governance"]["original_commercial_assets_published"])
        self.assertIsNone(self.report["governance"]["overall_percent"])
        self.assertEqual(self.report["source_baseline_main_head"],"5e0c01f0c854af7aefa75fd0485ddf728d069168")


if __name__=="__main__":
    unittest.main()
