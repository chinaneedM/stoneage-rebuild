"""Adversarial DOM pairing and source-admission checks without original assets."""
import json
from pathlib import Path
import unittest

from tools.stoneage_jp2003_character_visual import (
    IMAGE_FINAL, IMAGE_ROOT, PAGE_FINAL, RECORD_PATH, UNNAMED_CLAUSE,
    build, classify_layout, inspect_image,
)


def specimen():
    rows = []
    for start in (1, 5, 9):
        for family, size in (("illust", (65, 75)), ("com", (75, 105))):
            cells = [f'<td><img src="{IMAGE_ROOT}charapic{family}{n}.gif" width="{size[0]}" height="{size[1]}"></td>'
                     for n in range(start, start + 4)]
            rows.append("<tr>" + "".join(cells) + "</tr>")
    links = "".join(f'<font onclick="location.href=\'chara{n}.asp\';">{label}</font>'
                    for n, label in ((2, "ペット"), (3, "呪術"), (4, "ペット技術")))
    return UNNAMED_CLAUSE + "<table><tr><td><table>" + "".join(rows) + "</table></td></tr></table>" + links


class JapaneseCharacterSourceTests(unittest.TestCase):
    def test_dom_pairs_and_actual_labelled_targets(self):
        cells, links = classify_layout(specimen())
        self.assertEqual(len(cells), 24)
        self.assertEqual((cells["illust", 5]["row"], cells["com", 5]["row"]), (2, 3))
        self.assertEqual(cells["illust", 5]["col"], cells["com", 5]["col"])
        self.assertEqual(links[0], {"relative_target": "chara2.asp", "label": "ペット"})

    def test_filename_numbers_alone_cannot_establish_dom_pair(self):
        wrong = specimen().replace("charapiccom1.gif", "charapiccomX.gif").replace("charapiccom2.gif", "charapiccom1.gif").replace("charapiccomX.gif", "charapiccom2.gif")
        with self.assertRaisesRegex(ValueError, "DOM cells"):
            classify_layout(wrong)

    def test_duplicate_missing_and_out_of_range_references_rejected(self):
        for before, after in (("charapicillust2.gif", "charapicillust1.gif"),
                              ("charapiccom12.gif", "charapiccom13.gif"),
                              ("charapiccom12.gif", "unqualified.gif")):
            with self.subTest(before=before, after=after), self.assertRaises(ValueError):
                classify_layout(specimen().replace(before, after))

    def test_different_table_is_not_same_source_grid(self):
        source = specimen().replace('</tr><tr>', '</tr></table><table><tr>', 1)
        with self.assertRaisesRegex(ValueError, "Mixed source tables"):
            classify_layout(source)

    def test_unnamed_clause_and_link_labels_are_required(self):
        for source in (specimen().replace(UNNAMED_CLAUSE, ""), specimen().replace("ペット</font>", "人物</font>")):
            with self.assertRaises(ValueError):
                classify_layout(source)

    def test_declared_picture_footprint_not_silently_reinterpreted(self):
        with self.assertRaisesRegex(ValueError, "footprint"):
            classify_layout(specimen().replace('width="65"', 'width="640"', 1))

    def test_comment_and_script_picture_text_cannot_add_characters(self):
        fake = f'<img src="{IMAGE_ROOT}charapicillust99.gif" width="65" height="75">'
        cells, _ = classify_layout('<!--' + fake + '--><script>var ignored=\'' + fake + '\';</script>' + specimen())
        self.assertEqual(len(cells), 24)

    def test_wrong_page_host_path_capture_and_rewritten_body_rejected(self):
        for url in (PAGE_FINAL.replace("hangame.co.jp", "example.org"),
                    PAGE_FINAL.replace("chara.asp", "chara2.asp"),
                    PAGE_FINAL.replace("20031214051427", "20060619160353"), PAGE_FINAL):
            with self.subTest(url=url), self.assertRaises(ValueError):
                build(b"<html>source not acquired</html>", url, b"", IMAGE_FINAL)

    def test_image_byte_and_capture_admission_is_separate(self):
        with self.assertRaisesRegex(ValueError, "host/path/capture"):
            inspect_image(b"", IMAGE_FINAL.replace("20060619160353", "20031214051427"))
        with self.assertRaisesRegex(ValueError, "byte pin"):
            inspect_image(b"GIF89a" + b"x" * 6306, IMAGE_FINAL)

    def test_permanent_records_preserve_identity_visual_and_date_limits(self):
        p = json.loads(Path(RECORD_PATH).read_text(encoding="utf-8"))
        self.assertEqual(len(p["characters"]), 12)
        self.assertTrue(p["identity"]["operator_explicitly_describes_no_fixed_names"])
        for c in p["characters"]:
            self.assertIsNone(c["canonical_character_name"])
            self.assertIsNone(c["client_body_face_sprite_ids"])
            self.assertFalse(c["companion_reference"]["pixels_acquired"])
        self.assertEqual(sum(c["illustration"]["pixels_acquired"] for c in p["characters"]), 1)
        self.assertTrue(p["page"]["actual_capture"].startswith("2003"))
        self.assertTrue(p["reviewed_image"]["actual_capture"].startswith("2006"))
        self.assertFalse(p["reviewed_image"]["same_instant_or_same_bytes_as_2003_html_proven"])
        self.assertFalse(p["boundaries"]["jss1999_tw10_or_174a_build_identity_proven"])
        self.assertFalse(p["boundaries"]["original_html_or_pixels_in_git"])


if __name__ == "__main__":
    unittest.main()
