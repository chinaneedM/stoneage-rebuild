import unittest
import urllib.parse

from tools.stoneage_sa25_21cn_mirror_variant_probe import cdx_prefix_url, plausible


class SA25MirrorVariantTests(unittest.TestCase):
    def test_prefix_query(self):
        u=cdx_prefix_url("http://images.21cn.com/download/file/game/maoxian/sa25up.zip")
        q=urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
        self.assertEqual(q["matchType"],["prefix"])
        self.assertEqual(q["from"],["2002"])

    def test_plausible(self):
        self.assertTrue(plausible({"statuscode":"200","length":"8473000"}))
        self.assertFalse(plausible({"statuscode":"404","length":"8473000"}))
        self.assertFalse(plausible({"statuscode":"200","length":"399"}))


if __name__=="__main__":
    unittest.main()
