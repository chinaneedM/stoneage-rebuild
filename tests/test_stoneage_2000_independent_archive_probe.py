import unittest
from tools.stoneage_2000_independent_archive_probe import arq_items,FILENAME,SOURCE,DIRECT

class IndependentArchive2000Tests(unittest.TestCase):
    def test_target(self):
        self.assertEqual(FILENAME,"samap_1220.zip")
        self.assertIn("1220492.shtml",SOURCE)
        self.assertEqual(DIRECT,"http://202.106.184.193/downfiles/map_1212/samap_1220.zip")
    def test_arq_items(self):
        self.assertEqual(arq_items({"response_items":[{"url":"http://x"}]}),[{"url":"http://x"}])
        self.assertEqual(arq_items({"results":[1,2]}),[1,2])

if __name__=="__main__":
    unittest.main()
