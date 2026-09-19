import unittest
from tools.stoneage_gametime_early_download_probe import variants, replay

class GameTimeEarlyDownloadProbeTests(unittest.TestCase):
    def test_variants_include_utf8_and_korean(self):
        rows=variants()
        self.assertTrue(any("스톤에이지" in x for x in rows))
        self.assertTrue(any("%EC%8A%A4" in x.upper() for x in rows))
    def test_replay(self):
        self.assertIn("20001208213500id_",replay("http://x/"))

if __name__=="__main__":unittest.main()
