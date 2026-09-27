import unittest
from tools.stoneage_china2001_jan5_mailorder_residual import TARGETS, STRICT, replay

class T(unittest.TestCase):
    def test_targets(self):
        self.assertEqual(len(TARGETS),3)
        self.assertTrue(any("80570" in u for _,_,u in TARGETS))
    def test_strict(self):
        self.assertIn("邮购",STRICT)
        self.assertIn("试玩版",STRICT)
        self.assertNotIn("石器时代",STRICT)
    def test_replay(self):
        self.assertIn("20010211062656id_",replay("20010211062656",TARGETS[0][2]))

if __name__=="__main__":unittest.main()
