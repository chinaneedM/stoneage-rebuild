import unittest
from tools.stoneage_yegame_early_carrier_visual_match import YEGAME_TS, YEGAME_ORIG, YEGAME_URL

class T(unittest.TestCase):
    def test_reference(self):
        self.assertEqual(YEGAME_TS,"20010828031151")
        self.assertIn("EN0ZGKJ0002.jpg",YEGAME_ORIG)
        self.assertTrue(YEGAME_URL.startswith("https://web.archive.org/web/"))

if __name__=="__main__":
    unittest.main()
