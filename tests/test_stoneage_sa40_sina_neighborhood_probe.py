import unittest
from tools.stoneage_sa40_sina_neighborhood_probe import aid_of, candidate_urls

class NeighborhoodTests(unittest.TestCase):
    def test_aid_parser(self):
        self.assertEqual(aid_of("http://x/download.pl?col=u&aid=61619&filename=a.zip"),61619)
        self.assertIsNone(aid_of("http://x/download.pl?aid=x"))
    def test_candidate_same_directory(self):
        rows=candidate_urls(("http://down.example.com/games/updatex/other.zip",))
        self.assertIn("http://down.example.com/games/updatex/shiqi4updatex_02_11_08.zip",rows)

if __name__=="__main__":
    unittest.main()
