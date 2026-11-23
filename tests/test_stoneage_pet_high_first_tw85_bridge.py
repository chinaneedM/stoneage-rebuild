"""Source-only PET08 native TW85 graphics-to-local-album bridge guards."""
import copy
import unittest

from tools.stoneage_pet_high_first_tw85_native_bridge import (
    EXPECTED, PROGRAMS, load, query, route_slot, validate,
)


class TestTw85NativeSourceBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j = load()
        cls.summary = validate(cls.j)

    def test_native_source_550_group_554_physical_conservation(self):
        self.assertEqual(self.summary["source_graphic_numbers"], 550)
        self.assertEqual(self.summary["source_physical_sprite_groups"], 554)
        self.assertEqual(self.summary["source_graphic_name_conflicts_across_programs"], 41)
        self.assertEqual(self.summary["official_live_pet_species_confirmed"], 0)

    def test_four_separate_native_action_object_lanes(self):
        self.assertEqual(set(PROGRAMS), set(EXPECTED))
        for f, expected in EXPECTED.items():
            row = self.j["metrics"]["per_program"][f]
            self.assertEqual(
                (row["named_graphic_numbers"], row["distinct_named_local_album_slots"],
                 row["blank_or_unqualified_graphic_numbers"],
                 row["outside_local_source_grid_graphic_numbers"],
                 row["source_route_segments"]), expected)

    def test_one_original_name_and_cross_program_variant(self):
        one = query(self.j, graphic=101501)
        self.assertEqual(len(one), 4)
        self.assertEqual({r["original_name_cp950"] for r in one}, {"雷帝斯洛"})
        self.assertTrue(all(r["official_live_pet_issued"] is False for r in one))
        alt = query(self.j, graphic=101669)
        self.assertEqual([r["original_name_cp950"] for r in alt],
                         ["利則諾頓", "利則諾頓", None, "地人龍"])

    def test_outside_local_table_and_duplicate_physical_source(self):
        later = query(self.j, graphic=102050)
        self.assertEqual(len(later), 4)
        self.assertTrue(all(r["record_source_status"] == "OUTSIDE_QUALIFIED_LOCAL_GRID" for r in later))
        duplicate = query(self.j, graphic=101866)
        self.assertEqual(len(duplicate[0]["original_group_occurrences"]), 3)

    def test_mutated_sprite_binding_rejected(self):
        wrong = copy.deepcopy(self.j)
        wrong["records"][0]["program_routes"]["sa.exe"]["local_album_slot"] += 1
        with self.assertRaises(ValueError):
            validate(wrong)

    def test_mutated_source_alias_or_variant_rejected(self):
        wrong = copy.deepcopy(self.j)
        wrong["records"][0]["program_routes"]["sa.exe"]["original_portrait_alias_u32"] = 999999
        with self.assertRaises(ValueError):
            validate(wrong)
        wrong = copy.deepcopy(self.j)
        wrong["records"][0]["graphic_has_conflicting_names_across_installer_programs"] = True
        with self.assertRaises(ValueError):
            validate(wrong)


if __name__ == "__main__":
    unittest.main()
