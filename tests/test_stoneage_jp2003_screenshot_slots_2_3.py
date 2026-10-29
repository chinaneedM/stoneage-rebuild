import io
import unittest
from PIL import Image
from tools import stoneage_jp2003_screenshot_slots_2_3 as s


def make_jpeg(color):
    im = Image.new("RGB", (640, 480), color)
    out = io.BytesIO()
    im.save(out, "JPEG")
    return out.getvalue()


def wrap(i):
    stem = "image%04d" % i
    return ('<html><title>ストーンエイジ</title>'
            '<img src="../images/' + stem + '.jpg" alt="' + stem + '"></html>').encode("cp932")


class TestSourceQualifiedImagePair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raws = [wrap(2), wrap(3), make_jpeg((220, 90, 30)), make_jpeg((30, 60, 210))]

    def test_pinned_2003_gallery_provenance(self):
        refs = s.existing_gallery_refs()
        self.assertEqual([refs[i]["href"] for i in s.ORDINALS],
                         ["pages/image0002.html", "pages/image0003.html"])

    def test_exact_two_new_positions(self):
        d = s.derive(self.raws)
        self.assertEqual([x["ordinal"] for x in d["source_rows"]], [2, 3])
        self.assertEqual(d["source_count"], 2)
        self.assertEqual({r["original_jpeg"]["format"] for r in d["source_rows"]}, {"JPEG"})

    def test_unknowns_stay_unknown(self):
        d = s.derive(self.raws)
        self.assertFalse(d["official_early1999_or_tw1_build_authenticated"])
        self.assertFalse(d["picture_visual_content_reviewed_by_human"])
        self.assertIsNone(d["overall_restoration_percentage"])
        for r in d["source_rows"]:
            self.assertFalse(r["visual_description_reviewed"])
            self.assertIsNone(r["original_native_resolution"])
            self.assertIsNone(r["visual_description"])

    def test_swapped_wrapper_rejected(self):
        bad = list(self.raws)
        bad[0], bad[1] = bad[1], bad[0]
        with self.assertRaises(ValueError):
            s.derive(bad)

    def test_wrong_image_binding_rejected(self):
        bad = list(self.raws)
        bad[0] = bad[0].replace(b"image0002", b"image0003")
        with self.assertRaises(ValueError):
            s.derive(bad)

    def test_non_jpeg_rejected(self):
        bad = list(self.raws)
        bad[2] = b"not-a-jpeg"
        with self.assertRaises(Exception):
            s.derive(bad)

    def test_dimensions_rejected(self):
        im = Image.new("RGB", (320, 240), (0, 0, 0))
        data = io.BytesIO()
        im.save(data, "JPEG")
        bad = list(self.raws)
        bad[2] = data.getvalue()
        with self.assertRaisesRegex(ValueError, "dimension"):
            s.derive(bad)

    def test_all_source_pixels_not_published(self):
        d = s.derive(self.raws)
        text = __import__("json").dumps(d)
        self.assertNotIn("data:image/", text)
        self.assertNotIn("JFIF", text)
        self.assertFalse(d["raw_http_original_bytes_published"])

    def test_replay_published_exact_source_identities(self):
        import json
        report = json.loads(s.PUBLISHED.read_text(encoding="utf-8"))
        self.assertTrue(s.verify_published(report))
        self.assertEqual([x["ordinal"] for x in report["source_rows"]], [2, 3])
        self.assertTrue(report["http_response_url_binding_verified"])

    def test_altered_publication_image_digest_rejected(self):
        import json
        d = json.loads(s.PUBLISHED.read_text(encoding="utf-8"))
        d["source_rows"][1]["original_jpeg"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "JPEG identity"):
            s.verify_published(d)

    def test_false_visual_or_original_client_claim_rejected(self):
        import json
        d = json.loads(s.PUBLISHED.read_text(encoding="utf-8"))
        d["original_game_client_executed"] = True
        with self.assertRaisesRegex(ValueError, "status promoted"):
            s.verify_published(d)
        d["original_game_client_executed"] = False
        d["source_rows"][0]["visual_description"] = "Unverified pet name"
        with self.assertRaisesRegex(ValueError, "interpretation promoted"):
            s.verify_published(d)

    def test_source_image_swap_rejected_by_pinned_publication(self):
        import json
        d = json.loads(s.PUBLISHED.read_text(encoding="utf-8"))
        a, b = d["source_rows"]
        a["original_jpeg"], b["original_jpeg"] = b["original_jpeg"], a["original_jpeg"]
        with self.assertRaisesRegex(ValueError, "JPEG identity"):
            s.verify_published(d)


if __name__ == "__main__":
    unittest.main()
