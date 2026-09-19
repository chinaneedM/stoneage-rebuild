import unittest
from tools.stoneage_inium_down_probe import Parser, normalize

class IniumDownProbeTests(unittest.TestCase):
    def test_anchor_metadata(self):
        p=Parser();p.feed('<a href="files/stoneage.zip">다운로드</a>')
        self.assertIn(("a","anchor","files/stoneage.zip || 다운로드"),p.attrs)
    def test_normalize(self):
        self.assertEqual(
            normalize("http://stoneage.enium.co.kr/down.htm","files/stoneage.zip"),
            "http://stoneage.enium.co.kr/files/stoneage.zip"
        )

if __name__=="__main__":unittest.main()
