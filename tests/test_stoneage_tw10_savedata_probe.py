import math
import unittest

from tools.stoneage_tw10_savedata_probe import (
    NEEDLE,
    RUNTIME_PATH,
    SAVEDATA_PATH,
    entropy,
    zero_runs,
)

class TestTw10SavedataProbe(unittest.TestCase):
    def test_targets(self):
        self.assertEqual(RUNTIME_PATH, "StoneAge/sa_3.exe")
        self.assertEqual(SAVEDATA_PATH, "StoneAge/data/savedata.dat")
        self.assertEqual(NEEDLE, b"data\\savedata.dat")

    def test_zero_runs(self):
        self.assertEqual(zero_runs(b"\x00\x00\x01\x00\x02\x00\x00"), ((0,2),(3,1),(5,2)))
        self.assertEqual(zero_runs(b"\x01\x02"), ())
        self.assertEqual(zero_runs(b"\x00\x00"), ((0,2),))

    def test_entropy(self):
        self.assertEqual(entropy(b""), 0.0)
        self.assertAlmostEqual(entropy(b"\x00"*16), 0.0)
        self.assertAlmostEqual(entropy(bytes([0,1])*8), 1.0)

if __name__=="__main__":
    unittest.main()
