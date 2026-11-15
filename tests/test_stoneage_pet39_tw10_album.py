"""Check the client-album supplement against independent earlier source receipts."""

import json
import lzma
import unittest
from pathlib import Path

from tools.stoneage_pet16_lookup import CLIENT_ALBUM, PET39_PATH, graphic_trace, load_catalog, lookup

ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "research/recovered"


class TaiwanRetailClientAlbumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(PET39_PATH.read_text(encoding="utf-8"))
        cls.catalog = load_catalog()
        cls.rows = cls.receipt["records"]

    def test_named_and_empty_positions_cover_the_compiled_window(self):
        table = self.receipt["table"]
        named = {row["graphic_number"] for row in self.rows}
        empty = set(table["placeholder_graphics"])
        self.assertEqual((len(self.rows), len(named), len(empty)), (124, 124, 57))
        self.assertEqual(len({row["name_as_written"] for row in self.rows}), 124)
        self.assertFalse(named & empty)
        self.assertEqual(named | empty, set(range(100250, 100431)))
        self.assertEqual(table["placeholder_graphics_with_spr"], list(range(100400, 100430)))
        for row in self.rows:
            self.assertEqual(row["source_file_offset"],
                             table["file_offset"] + (row["graphic_number"] - 100250) * table["stride"])
            self.assertEqual(row["evidence"], "CLIENT_PET_IDENTITY_CANDIDATE")
            self.assertFalse(row["official_live_release_confirmed"])
        self.assertIsNone(self.receipt["historical_pet_count"])
        self.assertFalse(self.receipt["official_live_release_roster_verified"])

    def test_every_named_group_matches_existing_same_disc_motion(self):
        visual = {row["graphic_number"]: row for row in self.catalog["datasets"]["tw10_visual"]}
        for row in self.rows:
            original = visual[row["graphic_number"]]
            for field in ("spr_group_index", "spr_original_segment_sha256", "source_sequences",
                          "source_frame_positions"):
                self.assertEqual(row[field], original[field])
        self.assertEqual(sum(row["source_sequences"] for row in self.rows), 6944)
        self.assertEqual(sum(row["source_frame_positions"] for row in self.rows), 70236)

    def test_original_portrait_bytes_match_prior_taiwan_snapshot(self):
        with lzma.open(RECOVERED / "STONEAGE-ALBUM-CROSSVERSION-MATERIAL-R43.json.xz",
                       "rt", encoding="utf-8") as report:
            prior = json.load(report)
        refs = {int(ref["logical_alias"]): (int(ref["physical_bitmapno"]), int(ref["adrn_offset"]),
                                          ref["rd_bytes"], ref["rd_sha256"])
                for entry in prior["rows"] for ref in entry["profiles"]["TW10"]["references"]}
        actual = {row["portrait_logical_alias"]:
                  tuple(row["portrait_rd"][field] for field in ("bitmap_number", "offset", "bytes", "sha256"))
                  for row in self.rows if row["portrait_rd"] is not None}
        self.assertEqual(len(actual), 120)
        self.assertEqual(actual, refs)
        self.assertEqual([row["graphic_number"] for row in self.rows if row["portrait_rd"] is None],
                         [100389, 100390, 100391, 100392])

    def test_lookup_keeps_same_client_name_and_community_matches_distinct(self):
        names = lookup(self.catalog, "烏力", CLIENT_ALBUM)
        self.assertIn((100250, "烏力"), [(row["graphic_number"], row["name"]) for row in names])
        trace = graphic_trace(self.catalog, 100329)
        self.assertEqual(trace["tw10_same_client_album_record"]["name_as_written"], "格魯西斯")
        mixed = trace["source_separated_matches"]["mixed25_main"]["records"]
        self.assertIn("卡特利奴", [row["name_as_written"] for row in mixed])
        self.assertIsNone(trace["tw10_original_species_name"])
        self.assertIsNone(graphic_trace(self.catalog, 100400)["tw10_same_client_album_record"])


if __name__ == "__main__":
    unittest.main()
