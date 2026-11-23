"""Conservation and source-bound negative acceptance of TW85 PC local album."""
import unittest
from tools.stoneage_pet_high_first_tw85_lookup import load, query


class TestTw85NativePetAlbum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = load()

    def test_four_source_local_album_counts_and_blanks(self):
        expected = {"sa.exe": (574, 508, 57, 9),
                    "sb.exe": (551, 491, 57, 3),
                    "sc.exe": (464, 407, 57, 0),
                    "sd.exe": (540, 483, 57, 0)}
        for name, vals in expected.items():
            f = self.a["programs"][name]
            self.assertEqual(
                (f["total_grid_slots"], f["named_rows"],
                 f["blank_source_first_i32_minus_one"], f["unqualified_nonblank_rows"]), vals)
            self.assertEqual(len(f["source_records"]), vals[1])
            self.assertEqual(len(f["blank_or_unqualified"]), vals[2] + vals[3])
            self.assertEqual(len({r["original_first_i32"] for r in f["source_records"]}), vals[1])
            self.assertEqual(f["cn50_same_first_i32_and_portrait_alias_pair_count"], 305)

    def test_source_variants_not_flattened(self):
        diffs = self.a["measurements_not_official_species"]["sa_vs_other_per_file"]
        self.assertEqual(len(diffs["sb.exe"]["changed_same_original_i32_rows"]), 0)
        self.assertEqual(len(diffs["sc.exe"]["changed_same_original_i32_rows"]), 1)
        self.assertEqual(len(diffs["sd.exe"]["changed_same_original_i32_rows"]), 5)
        self.assertEqual({x["local_original_i32"] for x in diffs["sd.exe"]["changed_same_original_i32_rows"]},
                         {410, 411, 412, 413, 422})

    def test_lookup_preserves_program_and_one_source_row(self):
        hits = query(self.a, name="烏力", program="sa.exe")
        self.assertGreaterEqual(len(hits), 1)
        self.assertTrue(all(r["source_program"] == "sa.exe" for r in hits))
        self.assertTrue(all(r["official_live_pet_id_verified"] is False for r in hits))
        self.assertTrue(query(self.a, original_i32=410, program="sd.exe")[0]["original_name_cp950"] == "地人龍")
        self.assertTrue(query(self.a, original_i32=410, program="sa.exe")[0]["original_name_cp950"] == "利則諾頓")

    def test_negative_gates_and_source_custody(self):
        x = self.a
        self.assertEqual(x["measurements_not_official_species"]["official_live_species_confirmed_by_this_report"], 0)
        self.assertFalse(x["measurements_not_official_species"]["tw85_extra_spr_to_native_name_selector_proven"])
        self.assertTrue(all(x["negative_evidence"].values()))
        self.assertFalse(x["source_program_recovery"]["original_executables_executed"])
        self.assertFalse(x["source_program_recovery"]["static_unpack_original_bytes_retained_in_public_git"])


if __name__ == "__main__":
    unittest.main()
