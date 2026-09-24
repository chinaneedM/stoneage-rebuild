import unittest

from tools.stoneage_sa25_physical_image_fingerprint_probe import (
    ImageParser,
    hamming_hex,
    insecure_tls_allowed,
    is_thumbnail,
    normalize_image_url,
)


class PhysicalImageFingerprintProbeTests(unittest.TestCase):
    def test_thumbnail_detection(self):
        self.assertTrue(is_thumbnail("https://x/y_180_m.jpg"))
        self.assertFalse(is_thumbnail("https://x/y_180.jpg"))

    def test_image_parser_sources(self):
        p = ImageParser()
        p.feed('<img src="/a.jpg" alt="a"><img data-original="//cdn.example/b.png" title="b">')
        self.assertEqual(len(p.rows), 2)
        self.assertEqual(p.rows[0]["url"], "/a.jpg")
        self.assertEqual(p.rows[1]["url"], "//cdn.example/b.png")

    def test_normalize(self):
        self.assertEqual(
            normalize_image_url("https://example.com/p/q.html", "../a.jpg"),
            "https://example.com/a.jpg",
        )

    def test_tls_exception_is_host_limited(self):
        self.assertTrue(insecure_tls_allowed("https://www.shiqi.me/pt_17.htm"))
        self.assertTrue(insecure_tls_allowed("https://shiqi.me/x"))
        self.assertFalse(insecure_tls_allowed("https://a.rimg.com.tw/x.jpg"))
        self.assertFalse(insecure_tls_allowed("https://example.com/x"))

    def test_hamming(self):
        self.assertEqual(hamming_hex("0000000000000000", "0000000000000000"), 0)
        self.assertEqual(hamming_hex("0000000000000000", "ffffffffffffffff"), 64)


if __name__ == "__main__":
    unittest.main()
