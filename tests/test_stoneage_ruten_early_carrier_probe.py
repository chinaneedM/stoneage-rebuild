import unittest

from tools.stoneage_ruten_early_carrier_probe import (
    BASELINE,
    TARGETS,
    detail_rows,
    image_dimensions,
    image_urls,
)


class EarlyCarrierProbeTests(unittest.TestCase):
    def test_targets_unique_and_region_controls_present(self):
        ids = [pid for pid, _ in TARGETS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("22625938996449", ids)
        self.assertIn("22636573895893", ids)
        self.assertIn("22638643800877", ids)

    def test_baseline_identity_is_explicit(self):
        self.assertEqual(BASELINE["model"], "P-RPG-0008")
        self.assertEqual(BASELINE["barcode"], "4710739350098")

    def test_detail_rows(self):
        self.assertEqual(detail_rows({"data": [{"id": "x"}]}), [{"id": "x"}])
        self.assertEqual(detail_rows([{"id": "y"}]), [{"id": "y"}])

    def test_image_urls_full_size_only(self):
        row = {"images": {"url": ["https://a.rimg.com.tw/a.jpg", "//a.rimg.com.tw/b.jpg"]}}
        self.assertEqual(image_urls(row), [
            "https://a.rimg.com.tw/a.jpg",
            "https://a.rimg.com.tw/b.jpg",
        ])

    def test_png_dimensions(self):
        body = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + (640).to_bytes(4, "big") + (480).to_bytes(4, "big")
        self.assertEqual(image_dimensions(body), (640, 480))

    def test_gif_dimensions(self):
        body = b"GIF89a" + (320).to_bytes(2, "little") + (200).to_bytes(2, "little")
        self.assertEqual(image_dimensions(body), (320, 200))


if __name__ == "__main__":
    unittest.main()
