import unittest

from tools.stoneage_tw10_client_inventory import (
    classify_path,
    is_core_client,
    is_excluded_bundle,
    is_field_map_file,
    is_named_master_candidate,
    parse_address_table_bytes,
    parse_sab_candidate,
    split_palette_candidate,
)


class TaiwanV10ClientInventoryTests(unittest.TestCase):
    def test_core_categories(self):
        self.assertEqual(classify_path("StoneAge/sa_3.exe"), "runtime_executable")
        self.assertEqual(classify_path("StoneAge/data/real_1.bin"), "graphics_world")
        self.assertEqual(classify_path("StoneAge/data/spradrn_1.bin"), "sprite_animation")
        self.assertEqual(classify_path("StoneAge/data/battlemap/battle00.sab"), "battle_map")
        self.assertEqual(classify_path("StoneAge/data/bgm/sabgm_b0.wav"), "audio_bgm")
        self.assertEqual(classify_path("StoneAge/data/se/sak_01.wav"), "audio_sfx")
        self.assertEqual(classify_path("StoneAge/data/pal/Palet_0.sap"), "palette")
        self.assertEqual(classify_path("StoneAge/data/savedata.dat"), "local_state")

    def test_address_table_unique_vs_record_counts(self):
        rows = parse_address_table_bytes(
            b"0:4:battle00.sab 4:4:battle01.sab 8:4:battle00.sab"
        )
        self.assertEqual(
            rows,
            [
                (0, 4, "battle00.sab"),
                (4, 4, "battle01.sab"),
                (8, 4, "battle00.sab"),
            ],
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({row[2] for row in rows}), 2)

    def test_sab_candidate_parser(self):
        data = b"SAB\\x00" + b"\\x12\\x34\\x00\\x01"
        header, big_endian, little_endian = parse_sab_candidate(data)
        self.assertEqual(header, b"SAB\\x00")
        self.assertEqual(big_endian, (0x1234, 0x0001))
        self.assertEqual(little_endian, (0x3412, 0x0100))
        with self.assertRaises(ValueError):
            parse_sab_candidate(b"SAB")

    def test_palette_candidate_split(self):
        consumed = bytes([1]) * (224 * 3)
        tail = bytes([2]) * 36
        got_consumed, got_tail = split_palette_candidate(consumed + tail)
        self.assertEqual(got_consumed, consumed)
        self.assertEqual(got_tail, tail)
        with self.assertRaises(ValueError):
            split_palette_candidate(bytes([0]) * 671)

    def test_boundary_classification(self):
        self.assertTrue(is_core_client("StoneAge/data/real_1.bin"))
        self.assertTrue(is_excluded_bundle("StoneAge/人在江湖/DATA.TAG"))
        self.assertFalse(is_core_client("StoneAge/人在江湖/DATA.TAG"))
        self.assertFalse(is_field_map_file("StoneAge/data/battlemap/battle00.sab"))
        self.assertTrue(is_field_map_file("StoneAge/data/map/1000.dat"))
        self.assertTrue(is_named_master_candidate("StoneAge/data/pet_table.dat"))
        self.assertFalse(is_named_master_candidate("StoneAge/data/real_1.bin"))


if __name__ == "__main__":
    unittest.main()
