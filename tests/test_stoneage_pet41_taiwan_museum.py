"""Check early website evidence and prevent it being mistaken for a native roster."""

import json
import unittest

from tools.stoneage_pet16_lookup import (
    PET39_PATH, PET41_PATH, TW_MUSEUM, graphic_trace, load_catalog, lookup,
)
from tools.stoneage_pet41_taiwan_museum import SITE, entries


class TaiwanMuseumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(PET41_PATH.read_text(encoding="utf-8"))
        cls.album = json.loads(PET39_PATH.read_text(encoding="utf-8"))["records"]
        cls.rows = {row["web_ordinal"]: row for row in cls.report["rows"]}

    def test_archived_coverage_and_exact_printed_names(self):
        self.assertEqual(list(self.rows), list(range(1, 129)))
        pages = self.report["pages"]
        self.assertEqual(len(pages), 14)
        self.assertEqual(pages[0]["ordinals"], pages[1]["ordinals"])
        self.assertEqual([n for page in pages[1:] for n in page["ordinals"]], list(self.rows))
        names = {row["name_as_written"]: row["graphic_number"] for row in self.album}
        self.assertEqual({n: row["tw10_same_printed_name_graphic"] for n, row in self.rows.items()},
                         {n: names.get(row["name_as_written"]) for n, row in self.rows.items()})
        matches = [row["tw10_same_printed_name_graphic"] for row in self.rows.values()
                   if row["tw10_same_printed_name_graphic"] is not None]
        self.assertEqual((len(matches), len(set(matches))), (106, 105))
        self.assertIsNone(self.rows[9]["tw10_same_printed_name_graphic"])

    def test_empty_attributes_do_not_consume_the_next_record(self):
        def row(image_id, ordinal, name, elements, location):
            return (f'<img src="../../images/museum/pet/{image_id}.gif">'
                    f'<td>編號：{ordinal}</td><td>姓名：{name}</td><td>屬性：{elements}</td>'
                    f'<td>出現地點：{location}</td><td>資料提供：測試</td>')
        raw = (row("pet267", "0107", "黑烏力", "", "JOT獎品")
               + row("pet269", "0108", "柏克爾", "火：2　風：8", "玄黃的洞窟"))
        first, second = entries(raw.encode("cp950"), SITE + "pet11.htm", self.album)
        self.assertEqual((first["web_ordinal"], first["contributed_elements"]), (107, {}))
        self.assertEqual((second["web_ordinal"], second["contributed_elements"]), (108, {"火": 2, "風": 8}))

    def test_name_link_and_source_media_preserve_eligibility(self):
        catalog = load_catalog()
        result, = lookup(catalog, "布魯頓", TW_MUSEUM, details=True)
        self.assertEqual(result["web_ordinal"], 114)
        self.assertEqual(result["id"], "TW_WGS_MUSEUM:0114")
        self.assertEqual(result["contributed_elements"], {"火": 2, "風": 8})
        self.assertFalse(result["official_live_release_confirmed"])
        related = graphic_trace(catalog, 100394)
        self.assertEqual(related["tw_museum_exact_printed_name_matches"],
                         [{k: v for k, v in result.items() if k != "dataset"}])
        duplicate = graphic_trace(catalog, 100292)["tw_museum_exact_printed_name_matches"]
        self.assertEqual([row["web_ordinal"] for row in duplicate], [41, 103])
        for img in self.report["observed_website_images"]:
            self.assertEqual(img["original_url"], self.rows[img["web_ordinal"]]["web_image_url"])
            self.assertEqual((img["dimensions"], img["frames"]), ([80, 100], 1))
        self.assertFalse(self.report["bulu_dun_crosscheck"]["website_gif_equals_client_portrait"])
        self.assertFalse(self.report["card_package_image"]["identified_as_2000_august_three_card_set"])
        self.assertEqual(self.report["new_named_official_release_proofs"], 0)
        self.assertIsNone(self.report["historical_pet_population_count"])
