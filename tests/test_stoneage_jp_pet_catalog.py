"""Source admission, actual DOM name bindings and mixed-epoch catalog guards."""
import json
from pathlib import Path
import unittest
from tools.stoneage_jp_pet_catalog import (
    BASE, IMAGES, IMAGE_URL, IMAGE_CAPTURE, PAGES, REPORT, archive,
    classify_page, inspect_page, inspect_image,
)


def specimen(page):
    pin = PAGES[page - 1]
    rows = []
    for group in range((pin["count"] + 8) // 9):
        for kind in ("number", "name", "image"):
            cells = []
            for col in range(9):
                local = group * 9 + col + 1
                value = ""
                if local <= pin["count"]:
                    n = pin["start"] + local - 1
                    value = str(n) if kind == "number" else f"ペット{n}" if kind == "name" else f'<img src="{IMAGES}petpicgroup{page}-{local}.gif" width="60" height="65">'
                cells.append("<td>" + value + "</td>")
            rows.append("<tr>" + "".join(cells) + "</tr>")
    files = ("chara2.asp", "chara2-2.asp", "chara2-3.asp")
    labels = ("【１～４５】", "【４６～９０】", "【９１～１２４】")
    links = "".join(f'<font onclick="location.href=\'{file}\';">{label}</font>'
                    for i, (file, label) in enumerate(zip(files, labels), 1) if i != page)
    return "１００種類を超えるペット" + "<table>" + "".join(rows) + "</table>" + links


class JapanesePetCatalogTests(unittest.TestCase):
    def test_three_actual_ranges_and_reset_local_image_suffixes(self):
        first, _ = classify_page(specimen(1), 1)
        second, _ = classify_page(specimen(2), 2)
        third, _ = classify_page(specimen(3), 3)
        self.assertEqual([len(first), len(second), len(third)], [45, 45, 34])
        self.assertEqual(second[0]["web_ordinal"], 46)
        self.assertEqual(second[0]["local_image_number"], 1)
        self.assertTrue(second[0]["image_original_url"].endswith("group2-1.gif"))
        self.assertEqual(third[-1]["web_ordinal"], 124)
        self.assertEqual(third[-1]["local_image_number"], 34)

    def test_same_column_display_number_is_required(self):
        wrong = specimen(2).replace("<td>46</td>", "<td>1</td>", 1)
        with self.assertRaisesRegex(ValueError, "Displayed number"):
            classify_page(wrong, 2)

    def test_swapped_image_filenames_do_not_preserve_identity(self):
        wrong = specimen(1).replace("group1-1.gif", "group1-X.gif").replace("group1-2.gif", "group1-1.gif").replace("group1-X.gif", "group1-2.gif")
        with self.assertRaisesRegex(ValueError, "DOM relation"):
            classify_page(wrong, 1)

    def test_missing_or_duplicate_name_image_reference_rejected(self):
        for wrong in (specimen(1).replace("<td>ペット1</td>", "<td></td>"),
                      specimen(1).replace("group1-2.gif", "group1-1.gif"),
                      specimen(1).replace('width="60"', 'width="600"', 1)):
            with self.assertRaises(ValueError):
                classify_page(wrong, 1)

    def test_pagination_target_and_label_are_actual_source_data(self):
        for wrong in (specimen(1).replace("chara2-2.asp", "chara3.asp"),
                      specimen(1).replace("【４６～９０】", "【４６～１００】")):
            with self.assertRaises(ValueError):
                classify_page(wrong, 1)

    def test_comment_or_script_pictures_do_not_invent_entries(self):
        fake = f'<img src="{IMAGES}petpicgroup1-99.gif" width="60" height="65">'
        entries, _ = classify_page('<!--' + fake + '--><script>var fake=\'' + fake + '\';</script>' + specimen(1), 1)
        self.assertEqual(len(entries), 45)

    def test_unqualified_page_or_same_size_error_body_rejected(self):
        exact = archive(BASE + PAGES[0]["file"], PAGES[0]["capture"])
        for url in (exact.replace("hangame.co.jp", "example.org"), exact.replace("20031214055443", "20040220221717"), exact):
            with self.assertRaises(ValueError):
                inspect_page(b"x" * 36332, url, 1)
        with self.assertRaises(ValueError):
            classify_page(specimen(1), 0)

    def test_image_admission_separates_2006_capture_from_2003_page(self):
        with self.assertRaisesRegex(ValueError, "host/path/capture"):
            inspect_image(b"", archive(IMAGE_URL, "20031214055443"))
        with self.assertRaisesRegex(ValueError, "byte pin"):
            inspect_image(b"GIF89a" + b"x" * 4454, archive(IMAGE_URL, IMAGE_CAPTURE))

    def test_per_record_provenance_keeps_all_three_epochs_and_unknowns(self):
        p = json.loads(Path(REPORT).read_text(encoding="utf-8"))
        self.assertEqual(p["record_count"], 124)
        self.assertEqual([r["web_ordinal"] for r in p["records"]], list(range(1, 125)))
        first, ninety_first = p["records"][0], p["records"][90]
        self.assertEqual(first["name_as_written"], "ウーリ")
        self.assertEqual(first["source_refs"][0]["actual_capture"], "20031214055443")
        self.assertEqual(first["image"]["actual_capture"], "20060604065927")
        self.assertEqual(ninety_first["source_refs"][0]["actual_capture"], "20040220221717")
        self.assertEqual(p["records"][95]["name_as_written"], "ンモモ")
        for record in p["records"]:
            self.assertIsNone(record["client_species_graphic_ids"])
            self.assertIsNone(record["cross_region_aliases"])
            self.assertIsNone(record["stats_growth_habitat_skills"])
            if record["web_ordinal"] > 1:
                self.assertIsNone(record["image"]["actual_capture"])
                self.assertIsNone(record["image"]["sha256"])
        self.assertEqual(sum(r["image"]["pixels_acquired"] for r in p["records"]), 1)
        self.assertFalse(p["coverage"]["single_contemporaneous_2003_roster_proven"])
        self.assertFalse(p["coverage"]["complete_original_server_species_census_proven"])

    def test_records_fit_existing_archive_contract_without_public_asset_rights(self):
        p = json.loads(Path(REPORT).read_text(encoding="utf-8"))
        contract = json.loads(Path("research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json").read_text(encoding="utf-8"))["future_website"]
        for record in p["records"]:
            self.assertLessEqual(set(contract["record_contract"]["required"]), record.keys())
            self.assertIn(record["collection"], contract["required_collections"])
            self.assertNotEqual(record["rights_status"], "RELEASE_APPROVED")


if __name__ == "__main__":
    unittest.main()
