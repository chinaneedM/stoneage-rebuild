import unittest
from tools.stoneage_waei_download_detail_map_probe import params,is_file_link,stone_hits
class WaeiDetailMapTests(unittest.TestCase):
    def test_params(self):
        self.assertEqual(params("http://x/dldetial.asp?ID=5&xPage=2"),("5","2",""))
        self.assertEqual(params("http://x/dldetial.asp?ID=1&order=date"),("1","","date"))
    def test_file(self):
        self.assertTrue(is_file_link("http://x/download/file/foo/spr_1.bin"))
        self.assertFalse(is_file_link("http://x/dldetial.asp?ID=1"))
    def test_stone(self):
        self.assertTrue(stone_hits("<html>石器時代 spr_1.bin</html>"))
if __name__=="__main__":unittest.main()
