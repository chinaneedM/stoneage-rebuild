import unittest
import urllib.parse

from tools.stoneage_yegame_game_catalog_probe import (
    FROM,
    TO,
    QUERIES,
    cdx_url,
    candidate_page,
    product_code,
    token_hits,
)


class YegameGameCatalogProbeTests(unittest.TestCase):
    def test_source_grounded_game_target(self):
        urls = [row[1] for row in QUERIES]
        self.assertTrue(any("/product/game/" in url for url in urls))
        self.assertLessEqual(FROM, "20010208")
        self.assertGreaterEqual(TO, "20010208")

    def test_cdx_scope(self):
        url = cdx_url("http://www.yegame.com/product/game/", "prefix")
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        self.assertEqual(q["matchType"], ["prefix"])
        self.assertEqual(q["from"], [FROM])
        self.assertEqual(q["to"], [TO])

    def test_product_code(self):
        self.assertEqual(
            product_code("http://www.yegame.com/product/detail.asp?prodencode=ABC123"),
            "ABC123",
        )

    def test_candidate_pages(self):
        self.assertTrue(candidate_page("http://x/product/game/index.asp"))
        self.assertTrue(candidate_page("http://x/product/game/prod_secshow.asp?x=1"))
        self.assertFalse(candidate_page("http://x/image/foo.gif"))

    def test_stone_tokens(self):
        hits = token_hits("石器时代 客户端 光盘")
        self.assertIn("石器时代", hits)
        self.assertIn("客户端", hits)
        self.assertIn("光盘", hits)


if __name__ == "__main__":
    unittest.main()
