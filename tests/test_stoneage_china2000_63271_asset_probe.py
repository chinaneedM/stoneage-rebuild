import struct
import unittest
from tools.stoneage_china2000_63271_asset_probe import (
    AssetParser,
    canonical_first_party,
    image_dimensions,
    specificity,
)

class China200063271AssetProbeTests(unittest.TestCase):
    def test_first_party_query_scrub(self):
        u=canonical_first_party("/x/a.gif?name=someone#frag")
        self.assertEqual(u,"http://game.china.com/x/a.gif")
        self.assertIsNone(canonical_first_party("https://example.com/x.gif"))

    def test_asset_parser(self):
        p=AssetParser()
        p.feed('<img src="/a/test.gif"><script src="/js/x.js"></script><body background="/bg.jpg">')
        self.assertIn(("img","http://game.china.com/a/test.gif"),p.assets)
        self.assertIn(("script","http://game.china.com/js/x.js"),p.assets)
        self.assertIn(("background","http://game.china.com/bg.jpg"),p.assets)

    def test_png_dimensions(self):
        body=b"\x89PNG\r\n\x1a\n"+b"0"*8+struct.pack(">II",640,480)+b"x"*20
        self.assertEqual(image_dimensions(body,"image/png","x.png"),(640,480))

    def test_specificity(self):
        self.assertGreater(specificity("/shiqi/testcd.jpg",640,480,100000),0)
        self.assertLessEqual(specificity("/images/nav_logo.gif",100,20,2000),0)

if __name__=="__main__":
    unittest.main()
