import unittest
from tools.stoneage_2001_independent_archive_probe import arq_items, FILENAME, STEM

class IndependentArchive2001Tests(unittest.TestCase):
    def test_targets(self):
        self.assertEqual(FILENAME,"Estoneage2.0map_1127.exe")
        self.assertEqual(STEM,"Estoneage2.0map_1127")

    def test_arq_items(self):
        self.assertEqual(arq_items({"response_items":[{"url":"x"}]}),[{"url":"x"}])
        self.assertEqual(arq_items([{"url":"x"}]),[{"url":"x"}])
        self.assertEqual(arq_items({"other":1}),[])

if __name__=="__main__":
    unittest.main()
