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


class TaiwanMuseumPet42GapTests(unittest.TestCase):
    """Recompute both sides of the frozen client/museum gap; no identity promotion."""

    @classmethod
    def setUpClass(cls):
        cls.client = json.loads(PET39_PATH.read_text(encoding="utf-8"))
        cls.museum = json.loads(PET41_PATH.read_text(encoding="utf-8"))
        cls.gaps = json.loads(
            PET41_PATH.with_name(
                "STONEAGE-PET42-TW10-OPERATOR-MUSEUM-BIDIRECTIONAL-GAP-R1.json"
            ).read_text(encoding="utf-8")
        )

    def test_exact_misses_derive_from_two_independent_source_namespaces(self):
        album = self.client["records"]
        museum = self.museum["rows"]
        web_names = {row["name_as_written"] for row in museum}
        client_names = {row["name_as_written"] for row in album}
        unmatched_web = [row for row in museum if row["name_as_written"] not in client_names]
        unmatched_client = [row for row in album if row["name_as_written"] not in web_names]
        expected_ids = [row["web_ordinal"] for row in unmatched_web]
        self.assertEqual(expected_ids,
                         [row["web_ordinal"] for row in
                          self.gaps["website_non_exact_client_name_rows"]])
        self.assertEqual(
            [row["graphic_number"] for row in unmatched_client],
            [row["client_graphic_number"] for row in
             self.gaps["client_named_graphics_not_exactly_listed_on_website"]])
        self.assertEqual(
            self.gaps["counts"],
            {
                "website_numbered_rows": 128,
                "website_name_exact_client_rows": 106,
                "website_distinct_exact_matched_client_graphics": 105,
                "website_rows_without_exact_client_name": 22,
                "client_named_graphics": 124,
                "client_named_graphics_not_in_website_exact_name": 19,
                "website_duplicate_printed_names": 2,
                "proven_official_live_release_additions": 0,
            })
        self.assertEqual(
            self.gaps["website_duplicate_printed_names"],
            [{"name": "克克爾", "ordinals": [41, 103]},
             {"name": "盜賊魯尼帖斯", "ordinals": [118, 120]}]
        )
        for derived, source in zip(
            self.gaps["client_named_graphics_not_exactly_listed_on_website"],
            unmatched_client,
        ):
            self.assertEqual(derived["client_original_row_sha256"],
                             source["source_row_sha256"])
            self.assertEqual(derived["client_same_archive_spr_segment_sha256"],
                             source["spr_original_segment_sha256"])
            self.assertEqual(derived["has_same_archive_portrait_rd"],
                             source["portrait_rd"] is not None)

    def test_candidate_names_are_not_accepted_as_identity_or_release(self):
        names = {row["name_as_written"]: row for row in self.client["records"]}

        def one_edit(a, b):
            d = list(range(len(b) + 1))
            for i, ca in enumerate(a, 1):
                old, d[0] = d[0], i
                for j, cb in enumerate(b, 1):
                    saved = d[j]
                    d[j] = min(d[j] + 1, d[j - 1] + 1,
                               old + (ca != cb))
                    old = saved
            return d[-1] == 1

        for item in self.gaps["website_non_exact_client_name_rows"]:
            web = self.museum["rows"][item["web_ordinal"] - 1]
            self.assertEqual(item["website_name_as_written"], web["name_as_written"])
            self.assertEqual(item["source_page"], web["source_page"])
            self.assertEqual(item["website_image_url"], web["web_image_url"])
            proposed = item["single_edit_client_name_candidates"]
            self.assertEqual(
                {(p["name_as_written"], p["client_graphic_number"]) for p in proposed},
                {(name, entry["graphic_number"]) for name, entry in names.items()
                 if one_edit(item["website_name_as_written"], name)}
            )
            base = item["decoration_or_role_removed_base"]
            if item["matched_client_base_graphic_candidate"] is not None:
                self.assertIsNotNone(base)
                self.assertEqual(
                    item["matched_client_base_graphic_candidate"],
                    names[base]["graphic_number"],
                )
            self.assertFalse(item["client_pet_identity_confirmed"])
            self.assertFalse(item["official_live_release_confirmed"])
        self.assertEqual(
            self.gaps["source_pins"]["pet39_client_original_archive_sha256"],
            self.client["archive"]["sha256"]
        )
        self.assertFalse(self.gaps["source_qualifications"]["original_client_reextracted_in_pet42"])
        self.assertFalse(self.gaps["source_qualifications"]["original_website_html_reextracted_in_pet42"])
        self.assertEqual(self.gaps["new_named_official_release_proofs"], 0)
        self.assertIsNone(self.gaps["historical_official_pet_population_count"])
        self.assertEqual(self.gaps["year_2000_audit_status"], "OPEN_NOT_YEAR_CLOSED")
