import unittest
import urllib.parse

from tools.stoneage_yegame_stoneage_product_detail_probe import (
    PRODUCTS,
    HOSTS,
    detail_url,
    product_code,
    is_candidate_image,
    hits,
)


class YegameStoneAgeProductDetailProbeTests(unittest.TestCase):
    def test_known_product_codes(self):
        codes = {code: name for _label, code, name in PRODUCTS}
        self.assertEqual(codes["EN0ZGKJ0002"], "石器时代")
        self.assertIn("WGS620", codes["EZ0JHSD0003"])

    def test_hosts_cover_bare_and_www(self):
        self.assertIn("yegame.com", HOSTS)
        self.assertIn("www.yegame.com", HOSTS)

    def test_detail_url_and_code(self):
        url = detail_url("yegame.com", "EN0ZGKJ0002")
        self.assertIn("prodencode=EN0ZGKJ0002", url)
        self.assertEqual(product_code(url), "EN0ZGKJ0002")

    def test_candidate_image(self):
        self.assertTrue(is_candidate_image("http://yegame.com/product_images2/EN0ZGKJ0002.jpg"))
        self.assertFalse(is_candidate_image("http://yegame.com/help/index.asp"))

    def test_token_hits(self):
        got = hits("石器时代 产品介质 1-CD 华义")
        self.assertIn("石器时代", got)
        self.assertIn("产品介质", got)
        self.assertIn("华义", got)


if __name__ == "__main__":
    unittest.main()
