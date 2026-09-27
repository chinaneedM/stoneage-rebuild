import unittest
from tools.stoneage_waei_saupdate_directory_replay import generations,likely_payload,TIMESTAMP

class WaeiSaupdateDirectoryReplayTests(unittest.TestCase):
    def test_timestamp(self):
        self.assertEqual(TIMESTAMP,"20010530234248")
    def test_generations(self):
        self.assertIn(("sa",40),generations("sa_40.exe"))
        self.assertIn(("real",12),generations("real_12.bin"))
    def test_relevant(self):
        self.assertTrue(likely_payload("http://x/sa_3.exe",""))
        self.assertFalse(likely_payload("http://x/","Parent Directory"))
if __name__=="__main__":
    unittest.main()
