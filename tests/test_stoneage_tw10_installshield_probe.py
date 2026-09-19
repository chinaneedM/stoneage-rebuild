import unittest
from tools.stoneage_tw10_installshield_probe import MAP_RE, STONE_RE

class TaiwanV10InstallShieldProbeTests(unittest.TestCase):
    def test_map_classifier(self):
        self.assertTrue(MAP_RE.search("map/100.dat"))
        self.assertTrue(MAP_RE.search("foo.map"))
        self.assertFalse(MAP_RE.search("battleMap/battle01.sab"))
    def test_stone_classifier(self):
        self.assertTrue(STONE_RE.search("StoneAge.exe"))
        self.assertTrue(STONE_RE.search("data/real_1.bin"))
        self.assertFalse(STONE_RE.search("other.txt"))

if __name__=="__main__":
    unittest.main()
