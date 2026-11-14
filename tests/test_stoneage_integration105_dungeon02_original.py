"""Integration105: public metadata replay; never requires private original NPC source bytes."""
import json
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "research/recovered/STONEAGE-INTEGRATION105-DUNGEON02-151-ORIGINAL-STATIC-ROUTES-R1.json"
SOURCE_PATH = ROOT / "research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
MAP_PATH = ROOT / "research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

class Integration105Dungeon02Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = load(REPORT_PATH)
        cls.index = load(SOURCE_PATH)
        cls.maps = load(MAP_PATH)
        cls.rows = cls.report["rows"]
        cls.warps = [r for r in cls.rows if r["type"] == "npcgen_warp"]

    def test_01_exact_existing_blob_anchors(self):
        provenance = self.report["provenance"]
        for path, key in (
            (SOURCE_PATH, "original_public_all_npc_index_blob"),
            (MAP_PATH, "old_955_DAT_index_blob"),
            (ROOT / "docs/CURRENT-STATE.md", "current_state_preserved_blob"),
        ):
            actual = subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()
            self.assertEqual(provenance[key], actual)

    def test_02_original_preservation_qualifier(self):
        p = self.report
        self.assertEqual(p["schema"], "stoneage.integration105.dungeon02_static_source_routes.r1")
        self.assertIn("NOT_OFFICIAL_TW1", p["source_scope"])
        self.assertEqual(p["provenance"]["private_zip_crc_members_checked"], 2205)
        self.assertEqual(p["provenance"]["original_source_bytes"], 18174)
        self.assertEqual(p["provenance"]["original_source_sha256"], "bf047be69b5b1d3f6fda836cac4174e69868031b4e3e57f71c2f7da2b02636b6")
        self.assertEqual(self.report["limits"]["new_original_DAT_bytes_read"], 0)

    def test_03_all_151_rows_match_older_full_original_source_index(self):
        previous = sorted((r for r in self.index["create_rows"]
                           if r[0] == "genout/dungeon02.create"), key=lambda r: r[1])
        self.assertEqual(len(previous), 151)
        self.assertEqual(len(self.rows), 151)
        for ordinal, (old, new) in enumerate(zip(previous, self.rows)):
            self.assertEqual(new["ordinal"], ordinal)
            self.assertEqual(new["original_byte_span"], old[2:4])
            self.assertEqual(new["original_block_sha256"], old[4])
            self.assertEqual(new["source_floor"], old[5])
            self.assertEqual(new["source_xy"], old[7][:2])
            self.assertEqual(old[7][:2], old[7][2:])
            self.assertEqual(new["type"], old[11])

    def test_04_seven_real_handler_file_receipts(self):
        source_files = {r[0]: r for r in self.index["source_files"]}
        handlers = [r for r in self.rows if r["type"] == "npcgen_man"]
        self.assertEqual(len(handlers), 7)
        self.assertEqual(sum(r["handler_bytes"] for r in handlers), 720)
        self.assertEqual([r["ordinal"] for r in handlers], list(range(41, 48)))
        for r in handlers:
            old = source_files[r["handler_path"].removeprefix("npc/")]
            self.assertEqual(r["handler_bytes"], old[1])
            self.assertEqual(r["handler_sha256"], old[2])

    def test_05_every_destination_is_an_explicit_integer_triple(self):
        self.assertEqual(len(self.warps), 144)
        self.assertEqual(len({(r["source_floor"], *r["source_xy"],
                               r["target_floor"], *r["target_xy"]) for r in self.warps}), 144)
        for r in self.warps:
            self.assertEqual(len(r["target_xy"]), 2)
            self.assertTrue(all(isinstance(x, int) for x in
                                [r["target_floor"], *r["target_xy"], r["source_floor"], *r["source_xy"]]))

    def test_06_exact_reverse_not_graph_reachability(self):
        keys = {(r["source_floor"], *r["source_xy"], r["target_floor"], *r["target_xy"])
                for r in self.warps}
        non_reverse = []
        for r in self.warps:
            expected = (r["target_floor"], *r["target_xy"], r["source_floor"], *r["source_xy"]) in keys
            self.assertEqual(r["exact_reverse_present"], expected)
            if not expected:
                non_reverse.append(r["ordinal"])
        self.assertEqual(non_reverse, [0, 1, 34, 35, 36, 37, 38, 39, 40, 136, 149, 150])
        self.assertEqual(self.report["nonreciprocal_ordinals"], non_reverse)

    def test_07_source_and_target_existing_dat_geometry(self):
        dat = {int(r[0].removesuffix(".dat")): (r[3], r[4]) for r in self.maps["per_floor_source_rows"]
               if r[0].endswith(".dat") and r[0][:-4].isdigit()}
        def classify(floor, xy):
            if floor not in dat:
                return "NO_QUALIFIED_DAT"
            w, h = dat[floor]
            return "WITHIN_DAT_DIMENSIONS" if 0 <= xy[0] < w and 0 <= xy[1] < h else "OUTSIDE_DAT_DIMENSIONS"
        for r in self.rows:
            self.assertEqual(r["source_geometry"], classify(r["source_floor"], r["source_xy"]))
        for r in self.warps:
            self.assertEqual(r["target_geometry"], classify(r["target_floor"], r["target_xy"]))
        self.assertNotIn(300, dat)
        self.assertEqual(self.report["floor_300"]["source_rows"], 16)
        self.assertEqual(self.report["floor_300"]["target_rows"], 16)

    def test_08_aggregate_stats_recomputed(self):
        c = self.report["counts"]
        self.assertEqual((c["original_create_rows"], c["original_warp_rows"], c["original_man_rows"]), (151, 144, 7))
        self.assertEqual((c["source_floors"], c["target_floors"], c["union_floors"]), (65, 59, 65))
        self.assertEqual(c["exact_reverse_warp_rows"], sum(r["exact_reverse_present"] for r in self.warps))
        self.assertEqual(c["non_reverse_warp_rows"], sum(not r["exact_reverse_present"] for r in self.warps))
        self.assertEqual(c["source_geometry"]["WITHIN_DAT_DIMENSIONS"], 135)
        self.assertEqual(c["source_geometry"]["NO_QUALIFIED_DAT"], 16)
        self.assertEqual(c["target_geometry"]["WITHIN_DAT_DIMENSIONS"], 128)
        self.assertEqual(c["target_geometry"]["NO_QUALIFIED_DAT"], 16)
        self.assertEqual(c["source_geometry"]["OUTSIDE_DAT_DIMENSIONS"], 0)
        self.assertEqual(c["target_geometry"]["OUTSIDE_DAT_DIMENSIONS"], 0)

    def test_09_no_promoted_execution_or_proprietary_body(self):
        limits = self.report["limits"]
        for key in ("native_gameplay_or_transfers_executed", "same_official_build_qualified",
                    "original_handler_text_published", "original_1999_or_TW1_gameplay_identity_proven"):
            self.assertIs(limits[key], False)
        for row in self.rows:
            self.assertFalse(any(key in row for key in
                                 ("source_text", "original_dialogue", "script_body", "bitmap_bytes", "DAT_bytes")))
        self.assertEqual(self.report["provenance"]["current_state_preserved_blob"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")

if __name__ == "__main__":
    unittest.main()
