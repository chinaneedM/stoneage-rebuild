import unittest
from tools.stoneage_2001_redump_november_census import QUERIES

class NovemberPreservationCensusTests(unittest.TestCase):
    def test_queries_cover_both_collections(self):
        joined="\n".join(q for _,q in QUERIES)
        self.assertIn("collection:redump",joined)
        self.assertIn("collection:softwarecapsules",joined)
        self.assertIn("2001.11",joined)
        self.assertIn("2001-11",joined)

if __name__=="__main__":
    unittest.main()
