"""Public contract for the private Jaruga route B source observations."""
import hashlib
import json
from pathlib import Path
import unittest


RECOVERED = Path(__file__).resolve().parents[1] / "research" / "recovered"
REPORT = "STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-CHECKPOINTS-SOURCE-R1.json"
INPUTS = {
    "q25_blob": "STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json",
    "map04_blob": "STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json",
    "integration10_blob": "STONEAGE-INTEGRATION10-TWELVE-RECOVERED-DAT-SEVEN-CHECKPOINT-SCENES-R1.json",
}


def load(name):
    return json.loads((RECOVERED / name).read_bytes())


class RouteBSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = load(REPORT)
        cls.route = next(row for row in load(INPUTS["q25_blob"])["routes"] if row["label"] == "B")
        cls.map04 = load(INPUTS["map04_blob"])
        cls.integration10 = load(INPUTS["integration10_blob"])
        cls.sites = cls.report["sites"]

    def test_input_blobs_are_exact(self):
        for key, filename in INPUTS.items():
            raw = (RECOVERED / filename).read_bytes()
            header = f"blob {len(raw)}\0".encode()
            self.assertEqual(hashlib.sha1(header + raw).hexdigest(), self.report["input_git_blobs"][key])

    def test_source_sequence_and_exact_blocks(self):
        expected = [self.route["registration"],
                    *(checkpoint["source"] for checkpoint in self.route["checkpoints"]),
                    self.route["finish"]]
        self.assertEqual([row["label"] for row in self.sites],
                         ["start", *(f"B{i:02d}" for i in range(1, 13)), "finish"])
        scripts = {s["path"]: s["sha256"] for s in load(INPUTS["q25_blob"])["source_scripts"]}
        for row, source in zip(self.sites, expected, strict=True):
            for key in ("floor", "borncorner", "create_ordinal", "block_sha256",
                        "direction", "graphic_alias", "script_path"):
                self.assertEqual(row[key], source[key], (row["label"], key))
            self.assertEqual(row["script_sha256"], scripts[row["script_path"]])

    def test_stone_chain_and_first_checkpoint_flag(self):
        for actual, source in zip(self.sites[1:-1], self.route["checkpoints"], strict=True):
            for key in ("number", "incoming_item", "outgoing_item", "event_ordinal", "condition_literal"):
                self.assertEqual(actual[key], source[key])
        self.assertEqual([row["incoming_item"] for row in self.sites[1:-1]], list(range(2552, 2564)))
        self.assertEqual([row["outgoing_item"] for row in self.sites[1:-1]], list(range(2553, 2565)))
        self.assertEqual([row["label"] for row in self.sites[1:-1] if "&ENDEV=2" in row["condition_literal"]],
                         ["B01"])

    def test_exact_DAT_identity_and_window_bounds(self):
        map_files = {row["floor"]: row for row in self.report["map_files"]}
        self.assertEqual(set(map_files), {200, 3000, 20105, 20301, 20403, 20505, 20601, 20703})
        recovered = {row["floor"]: row for row in self.integration10["recovered_DAT"]}
        original = {int(row[0][:-4]): row[1:5] for row in self.map04["per_floor_source_rows"]}
        for floor, row in map_files.items():
            keys = ("bytes", "sha256", "width", "height")
            actual = [row[key] for key in keys]
            self.assertEqual(row["bytes"], 8 + 6 * row["width"] * row["height"])
            if floor in (200, 3000):
                self.assertEqual(actual, [recovered[floor][key] for key in keys])
                self.assertEqual(row["crc32"], recovered[floor]["crc32"])
                self.assertEqual(row["plane_sha256"], [p["sha256"] for p in recovered[floor]["planes"]])
            else:
                self.assertEqual(actual, original[floor])
        for row in self.sites:
            x, y, x2, y2 = row["borncorner"]
            self.assertEqual((x, y), (x2, y2))
            self.assertEqual(row["window"], [x-5, y-5, x+5, y+5])
            self.assertLess(x+5, map_files[row["floor"]]["width"])
            self.assertLess(y+5, map_files[row["floor"]]["height"])
            self.assertGreaterEqual(min(x, y), 5)
            self.assertEqual(len(row["center_three_u16"]), 3)
            self.assertTrue(all(0 <= value <= 65535 for value in row["center_three_u16"]))

    def test_missing_pixels_stay_open(self):
        expected_missing = {"24307": 1, "24309": 2, "24310": 1}
        self.assertEqual(self.sites[0]["missing_alias_occurrences"], expected_missing)
        self.assertTrue(all(not r["missing_alias_occurrences"] for r in self.sites[1:]))
        self.assertEqual(set(self.report["later_index_only_aliases"]), set(map(int, expected_missing)))
        self.assertFalse(set(expected_missing) & self.report["map_pixel_sources"].keys())
        for row in self.sites:
            self.assertEqual(row["gt99_references"] - row["rendered_references"],
                             sum(row["missing_alias_occurrences"].values()))
            self.assertEqual(set(row["frames"]), {"plane0", "plane1", "combined"})
        self.assertEqual(sum(r["gt99_references"] for r in self.sites), 1712)
        self.assertEqual(sum(r["rendered_references"] for r in self.sites), 1708)
        self.assertEqual(sum(r["low_nonzero"] for r in self.sites), 343)

    def test_tile_and_NPC_identity_namespaces(self):
        catalog = {row[0]: row for row in self.map04["source_TW1_real_RD_rows"]}
        tiles = self.report["map_pixel_sources"]
        self.assertEqual(len(tiles), 342)
        for alias, row in tiles.items():
            known = catalog[int(alias)]
            self.assertEqual([row[key] for key in ("index", "width", "height", "bytes", "RD_sha256")], known[1:6])
        portraits = self.report["separate_NPC_image_candidates"]
        expected = {"16027": 5873, "16033": 5879, "16065": 5911, "16066": 5912}
        self.assertEqual({alias: row["physical_bitmap"] for alias, row in portraits.items()}, expected)
        self.assertEqual(set(map(int, portraits)), {row["graphic_alias"] for row in self.sites})
        self.assertEqual(len({row["RD_sha256"] for row in portraits.values()}), 4)

    def test_no_native_or_early_official_claims(self):
        boundary = self.report["boundaries"]
        for key in ("native_client_executed", "original_runtime_reachability_verified",
                    "same_official_deployment_authenticated", "NPC_native_appearance_verified",
                    "original_low_value_render_semantics_verified", "original_assets_published"):
            self.assertIs(boundary[key], False)
        self.assertEqual(boundary["stage_A"], {"PARTIAL": 7, "OPEN": 2})
        self.assertEqual(boundary["stage_B"], "GATED")
        self.assertIsNone(boundary["overall_percent"])


if __name__ == "__main__":
    unittest.main()
