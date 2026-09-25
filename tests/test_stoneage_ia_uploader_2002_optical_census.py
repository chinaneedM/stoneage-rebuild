import unittest
from tools.stoneage_ia_uploader_2002_optical_census import optical
class CensusTests(unittest.TestCase):
    def test_optical_filter(self):
        rows=[{"name":"CD [STA4].bin"},{"name":"CD [STA4].cue"},{"name":"cover.jpg"}]
        self.assertEqual(len(optical(rows)),2)
if __name__=="__main__": unittest.main()
