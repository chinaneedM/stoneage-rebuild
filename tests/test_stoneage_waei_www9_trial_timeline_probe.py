import json
import unittest
from tools.stoneage_waei_www9_trial_timeline_probe import (
    cdx_url,downloading_id,size_hits,stone_hits,trial_hits
)

class WaeiWww9TrialTimelineProbeTests(unittest.TestCase):
    def test_cdx_no_collapse(self):
        u=cdx_url("http://www9.waei.net/download.php?Dcat_ID=2")
        self.assertNotIn("collapse",u)
        self.assertIn("from=20001201",u)
        self.assertIn("to=20010112",u)

    def test_downloading_id(self):
        self.assertEqual(downloading_id("http://www9.waei.net/download/downloading.php?ID=35"),"35")
        self.assertEqual(downloading_id("http://x/y"),"")

    def test_semantics(self):
        s="<html>石器時代 遊戲試玩版 大小 274.5MB</html>"
        self.assertTrue(stone_hits(s))
        self.assertTrue(trial_hits(s))
        self.assertTrue(size_hits(s))

if __name__=="__main__":
    unittest.main()
