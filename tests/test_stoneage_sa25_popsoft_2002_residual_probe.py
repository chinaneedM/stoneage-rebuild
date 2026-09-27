import unittest
import urllib.parse

from tools.stoneage_sa25_popsoft_2002_residual_probe import (
    PINNED_IDENTIFIERS,
    advanced_search_url,
    download_url,
    feb_2002_file,
    feb_ocr_file,
    ia_docs,
    metadata_url,
    optical_file,
    source_original,
    strong_stoneage_offsets,
    target_family_item,
)


class SA25Popsoft2002ResidualProbeTests(unittest.TestCase):
    def test_query_is_exactly_bounded_to_2002(self):
        parsed = urllib.parse.urlparse(advanced_search_url('"大众软件" AND year:2002'))
        query = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(query["q"], ['"大众软件" AND year:2002'])
        self.assertEqual(query["rows"], ["100"])

    def test_known_scan_family_is_pinned(self):
        self.assertIn("popsoft-magazine_202403", PINNED_IDENTIFIERS)
        self.assertTrue(metadata_url("popsoft-magazine_202403").endswith("popsoft-magazine_202403"))
        self.assertIn("2002/", download_url("popsoft-magazine_202403", "2002/x.txt"))

    def test_target_family_rejects_unrelated_iso_collision(self):
        modem = {"title": "网际纵横 v2.3 —— 实达灵犀 5600D 随机光盘", "creator": "福建实达"}
        popsoft = {"title": "Popsoft 大众软件", "creator": "Popsoft"}
        self.assertFalse(target_family_item("start-modem-5600d", modem))
        self.assertTrue(target_family_item("popsoft-magazine_202403", popsoft))

    def test_file_classifiers(self):
        optical = {"name": "disc/GAME.iso", "source": "original"}
        ocr = {"name": "2002/大众软件-2002年02月B_djvu.txt", "source": "derivative"}
        self.assertTrue(optical_file(optical))
        self.assertTrue(source_original(optical))
        self.assertTrue(feb_2002_file(ocr))
        self.assertTrue(feb_ocr_file(ocr))

    def test_strong_context_requires_version_semantics(self):
        plain = "这里提到石器时代，但没有版本信息。"
        strong = "这里提到石器时代2.5精灵王传说。"
        self.assertEqual(strong_stoneage_offsets(plain), [])
        self.assertTrue(strong_stoneage_offsets(strong))

    def test_ia_docs_filters_non_dict_rows(self):
        docs = ia_docs({"response": {"docs": [{"identifier": "x"}, "bad"]}})
        self.assertEqual(docs, ({"identifier": "x"},))


if __name__ == "__main__":
    unittest.main()
