import io
import json
from pathlib import Path
import unittest
from PIL import Image
from tools.stoneage_jss_intro_source import image_metadata, page_contract, PAGE_URL, ROOT


class IntroSourceTests(unittest.TestCase):
    def jpeg(self):
        stream = io.BytesIO()
        Image.new("RGB", (17, 13), "green").save(stream, "JPEG")
        return stream.getvalue()

    def test_byte_dimensions_are_independent_of_html_size(self):
        original = ROOT + "image/sakss01.jpg"
        url = "https://web.archive.org/web/20010418000000id_/" + original
        r = image_metadata(self.jpeg(), url, original)
        self.assertEqual((r["actual_width"], r["actual_height"]), (17, 13))
        self.assertFalse(r["same_moment_as_page_proven"])
        self.assertFalse(r["tw10_same_build_authenticated"])

    def test_late_replay_is_not_early_visual_evidence(self):
        original = ROOT + "image/sakss01.jpg"
        with self.assertRaisesRegex(ValueError, "outside historical window"):
            image_metadata(self.jpeg(), "https://web.archive.org/web/20040101000000id_/" + original, original)

    def test_redirect_to_other_image_or_host_rejected(self):
        original = ROOT + "image/sakss01.jpg"
        for other in (ROOT + "image/sakss02.jpg", "http://example.com/stoneage/image/sakss01.jpg"):
            with self.assertRaisesRegex(ValueError, "another original resource"):
                image_metadata(self.jpeg(), "https://web.archive.org/web/20010418000000id_/" + other, original)

    def test_html_error_body_cannot_become_a_screenshot(self):
        original = ROOT + "image/sakss01.jpg"
        with self.assertRaises(Exception):
            image_metadata(b"<html>missing image</html>", "https://web.archive.org/web/20010418000000id_/" + original, original)

    def test_unqualified_page_is_not_silently_reinterpreted(self):
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            page_contract(b"characters 12 pets 5", PAGE_URL)

    def test_archived_source_and_visual_inference_stay_separate(self):
        path = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-JSS2001-INTRO-SCREENSHOT-SOURCES-R1.json"
        data = json.loads(path.read_text())
        self.assertEqual(data["linked_screenshot_count"], 15)
        self.assertEqual(data["contracts"]["character_body_types_reported"], 12)
        self.assertEqual(data["contracts"]["appearance_variants_including_colors_reported"], 48)
        self.assertFalse(data["boundaries"]["species_or_bitmap_id_mapping_proven"])
        self.assertFalse(data["boundaries"]["jss1999_or_tw10_same_build_proven"])
        qualified = {r["original_url"] for r in data["images"]}
        unqualified = {r["original_url"] for r in data["unqualified_image_references"]}
        self.assertFalse(qualified & unqualified)
        self.assertEqual(len(qualified | unqualified), 15)
        self.assertEqual(data["qualified_screenshot_count"], len(qualified))
        for row in data["unqualified_image_references"]:
            self.assertFalse(row["source_absence_established"])


if __name__ == "__main__":
    unittest.main()
