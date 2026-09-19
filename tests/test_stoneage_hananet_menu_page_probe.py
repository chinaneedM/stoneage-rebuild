import unittest
from tools.stoneage_hananet_menu_page_probe import Parser, normalize

class HananetMenuPageProbeTests(unittest.TestCase):
    def test_area_and_anchor(self):
        p=Parser()
        p.feed('<area href="download.htm" alt="다운로드"><a href="x.zip">받기</a>')
        self.assertTrue(any(x[0]=="area" and x[1]=="href" for x in p.links))
        self.assertTrue(any("x.zip" in x[2] for x in p.links))
    def test_normalize(self):
        self.assertEqual(normalize("http://stoneage.hananet.net/2.htm","file.zip"),"http://stoneage.hananet.net/file.zip")

if __name__=="__main__":
    unittest.main()
