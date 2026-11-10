"""Public checks for the private mixed25 registration and floor 3000 replay."""
import hashlib
import json
from pathlib import Path
import unittest


RECOVERED = Path(__file__).resolve().parents[1] / "research" / "recovered"
I41 = "STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-CHECKPOINTS-SOURCE-R1.json"
I27 = "STONEAGE-INTEGRATION27-PET-TUTORS-AND-3400-DAT-SOURCE-R1.json"
REPORT = "STONEAGE-INTEGRATION42-JARUGA-REGISTRATION-ORIGINAL-TILES-R1.json"


def load(name):
    raw = (RECOVERED / name).read_bytes()
    git_blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    return json.loads(raw), git_blob


class RegistrationSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report, _ = load(REPORT)
        cls.i41, cls.i41_blob = load(I41)
        cls.i27, cls.i27_blob = load(I27)
        cls.previous = cls.i41["sites"][0]
        cls.full = cls.report["full_floor_3000"]

    def test_exact_source_receipts(self):
        self.assertEqual(self.report["upstream"],
                         {"integration41": self.i41_blob, "integration27": self.i27_blob})
        self.assertEqual(self.report["parent_rar"], self.i27["parent_rar"])
        source = self.i27["extraction"]["complete_graphic_source_members"]
        members = self.report["archive_members"]
        for name in ("adrn_15.bin", "real_15.bin", "Palet_1.sap"):
            self.assertEqual(members[name], source[name])
        dat = next(row for row in self.i41["map_files"] if row["floor"] == 3000)
        for key in ("bytes", "sha256", "crc32"):
            self.assertEqual(members["3000.dat"][key], dat[key])

    def test_mixed25_logical_aliases_are_distinct_from_physical_bitmaps(self):
        rows = self.report["recovered_assets"]
        self.assertEqual({r["alias"]: r["physical_bitmap"] for r in rows},
                         {24307: 126055, 24309: 126057, 24310: 126058})
        for row in rows:
            self.assertEqual(row["RD_flag"], 1)
            self.assertGreaterEqual(row["adrn_ordinal"], 125996)
            self.assertGreaterEqual(row["RD_offset"], 315842228)
            self.assertLessEqual(row["RD_offset"] + row["RD_bytes"],
                                 self.report["archive_members"]["real_15.bin"]["bytes"])
        self.assertEqual(len({r["RD_sha256"] for r in rows}), 3)
        self.assertEqual(self.report["extraction"]["whole_ADRN_records"], 234564)

    def test_exact_source_cells_and_registration_coverage(self):
        site = self.report["site"]
        for key in ("floor", "borncorner", "window", "center_three_u16"):
            self.assertEqual(site[key], self.previous[key])
        self.assertEqual(site["original_block_sha256"], self.previous["block_sha256"])
        cells = self.report["recovered_DAT_cells"]
        values = {(r["alias"], *r["xy"]) for r in cells}
        self.assertEqual(values, {(24307,82,98),(24309,80,96),(24309,81,97),(24310,81,98)})
        self.assertEqual(len(cells), 4)
        for row in cells:
            x, y = row["xy"]
            self.assertEqual(row["plane"], 1)
            self.assertEqual(row["DAT_byte_offset"], 8 + 2 * (150 * 150 + y * 150 + x))
        cover = self.report["coverage"]
        self.assertEqual((cover["prior"],cover["after"],cover["distinct_tiles"]), (122,126,55))
        self.assertEqual(cover["gt99_references"],cover["after"])
        self.assertEqual(cover["source_low_nonzero_values_1_to_99"], 2)
        self.assertEqual(cover["other_windows_regenerated"], 0)
        same = self.report["prior_exact_mixed25_ADRN_and_RD_aliases"]
        self.assertEqual(len(set(same)),52)
        self.assertTrue(all(str(alias) in self.i41["map_pixel_sources"] for alias in same))

    def test_only_second_plane_changed_in_registration_window(self):
        before = self.report["before_frames"]
        after = self.report["after_frames"]
        self.assertEqual(before, self.previous["frames"])
        self.assertEqual(before["plane0"],after["plane0"])
        self.assertNotEqual(before["plane1"],after["plane1"])
        self.assertNotEqual(before["combined"],after["combined"])
        self.assertEqual(self.report["changed_RGBA_pixel_counts"],
                         {"plane0":0,"plane1":4513,"combined":4512})

    def test_full_floor_missing_alias_stays_unresolved(self):
        floor = self.full
        self.assertEqual(floor["source_dimensions"], [150,150])
        self.assertEqual((floor["high_value_references"],floor["placements_rendered"]), (10853,10851))
        self.assertEqual((floor["high_value_aliases"],floor["distinct_source_tiles"]), (1007,1006))
        self.assertEqual(floor["unknown_logical_aliases"], [22413])
        self.assertEqual({tuple(r["xy"]) for r in floor["unknown_cells"]}, {(80,99),(79,96)})
        for row in floor["unknown_cells"]:
            x, y = row["xy"]
            self.assertEqual((row["alias"],row["plane"]), (22413,1))
            self.assertEqual(row["DAT_byte_offset"], 8 + 2 * (150 * 150 + y * 150 + x))
        self.assertEqual(floor["low_nonzero_references"], 4364)
        self.assertTrue(floor["complete_canvas_independently_replayed"])

    def test_duplicate_records_are_preserved_as_equivalent_candidates(self):
        groups = self.full["equivalent_duplicate_aliases"]
        self.assertEqual([r["alias"] for r in groups], [8326,8327,8328])
        for group in groups:
            a, b = group["variants"]
            self.assertNotEqual(a["ADRN_sha256"], b["ADRN_sha256"])
            self.assertNotEqual(a["physical_bitmap"], b["physical_bitmap"])
            for key in ("RD_sha256","index_sha256","width","height","xoff","yoff"):
                self.assertEqual(a[key], b[key])
        unique = self.full["original_unique_index_aliases"]
        self.assertEqual(unique + 2 * len(groups), self.full["original_RD_blocks_double_decoded"])

    def test_reuse_scan_and_historical_boundaries(self):
        scan = self.report["reuse_scan"]
        self.assertEqual(scan["source_files"], {"MAP09":955,"I10":12})
        self.assertEqual({r["floor"]:sum(r["references"].values()) for r in scan["matching_floors"]},
                         {2000:2,3000:7,4000:1,7002:8})
        self.assertEqual(scan["total_references"], 18)
        bounds = self.report["boundaries"]
        for key in ("native_client_executed","early_official_deployment_authenticated",
                    "native_draw_layer_or_palette_verified","collision_or_quest_execution_verified",
                    "native_semantics_for_low_values_verified","original_assets_public"):
            self.assertIs(bounds[key], False)
        self.assertEqual(bounds["stage_A"], {"PARTIAL":7,"OPEN":2})
        self.assertEqual(bounds["stage_B"], "GATED")
        self.assertIsNone(bounds["overall_percent"])


if __name__ == "__main__":
    unittest.main()
