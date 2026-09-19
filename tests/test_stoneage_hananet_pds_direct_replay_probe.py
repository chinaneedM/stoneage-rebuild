import unittest
from tools.stoneage_hananet_pds_direct_replay_probe import replay, URLS

class HananetPdsDirectReplayProbeTests(unittest.TestCase):
    def test_variants(self):
        self.assertTrue(any(":80/view.asp" in x for x in URLS))
        self.assertTrue(any("type=C03&app_id=" in x for x in URLS))
    def test_replay(self):
        self.assertIn("20001210160500id_",replay("20001210160500","http://x/"))

if __name__=="__main__":unittest.main()
