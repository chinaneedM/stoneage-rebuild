import unittest
from tools.stoneage_waei_download_id12_probe import isfile,hits,STONE
class Id12Tests(unittest.TestCase):
    def test_file(self):
        self.assertTrue(isfile("http://x/download/file/a/spr_1.bin"))
        self.assertFalse(isfile("http://x/dldetial.asp?ID=1"))
    def test_hits(self):
        self.assertTrue(hits("<html>石器時代</html>",STONE))
if __name__=="__main__":unittest.main()
