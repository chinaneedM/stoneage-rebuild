import unittest
import urllib.parse
from tools.stoneage_sa25_21cn_prefix_probe import STEMS,query_url

class T(unittest.TestCase):
    def test_images_stem_present(self):
        self.assertIn(
            ("images-2002","http://images.21cn.com/download/file/game/maoxian/sa25up"),
            STEMS,
        )
    def test_prefix_query(self):
        p=urllib.parse.urlparse(query_url(STEMS[0][1]))
        q=urllib.parse.parse_qs(p.query)
        self.assertEqual(q["url"],[STEMS[0][1]])
        self.assertEqual(q["matchType"],["prefix"])
        self.assertEqual(q["from"],["2002"])
        self.assertEqual(q["to"],["2006"])

if __name__=="__main__":
    unittest.main()
