import unittest
from tools.stoneage_yegame_matched_carrier_description_probe import TARGET, visible, snippets

class T(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET,"22636573895893")

    def test_visible_and_snippet(self):
        text=visible("<html><body>正版 石器时代 1.82 客户端 光盘</body></html>")
        self.assertIn("石器时代",text)
        self.assertTrue(snippets(text))

if __name__=="__main__":
    unittest.main()
