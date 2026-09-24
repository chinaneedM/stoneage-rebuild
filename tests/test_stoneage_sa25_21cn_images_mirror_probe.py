import unittest
import urllib.parse

from tools.stoneage_sa25_21cn_images_mirror_probe import ZIP_URL,JPG_URL,arquivo_url


class T(unittest.TestCase):
    def test_router_derived_targets(self):
        self.assertEqual(
            ZIP_URL,
            "http://images.21cn.com/download/file/game/maoxian/sa25up.zip",
        )
        self.assertEqual(
            JPG_URL,
            "http://images.21cn.com/download/file/game/maoxian/sa25up.jpg",
        )

    def test_arquivo_exact_window(self):
        q=urllib.parse.parse_qs(urllib.parse.urlparse(arquivo_url(ZIP_URL)).query)
        self.assertEqual(q["url"],[ZIP_URL])
        self.assertEqual(q["from"],["2001"])
        self.assertEqual(q["to"],["2005"])


if __name__=="__main__":
    unittest.main()
