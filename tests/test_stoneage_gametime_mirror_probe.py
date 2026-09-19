import unittest
from tools.stoneage_gametime_mirror_probe import replay, TARGETS

class GameTimeMirrorProbeTests(unittest.TestCase):
    def test_targets(self):
        self.assertTrue(any("GW_IDX=9" in x[2] for x in TARGETS))
        self.assertTrue(any("IDX=11" in x[2] for x in TARGETS))
    def test_replay(self):
        self.assertIn("id_",replay("20010609062605","http://x/"))

if __name__=="__main__":unittest.main()
