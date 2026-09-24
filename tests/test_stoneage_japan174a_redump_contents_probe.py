import unittest
from tools.stoneage_japan174a_redump_contents_probe import TARGETS

class Japan174aRedumpContentsProbeTests(unittest.TestCase):
    def test_coverdisc_queries_are_pinned(self):
        targets=dict(TARGETS)
        self.assertEqual(targets["jp-pc-coverdisc-latin"]["category"],"Coverdiscs")
        self.assertEqual(targets["jp-pc-coverdisc-latin"]["contents"],"StoneAge")
        self.assertEqual(targets["jp-pc-coverdisc-filename"]["contents"],"sa174hg.exe")

    def test_global_filename_fallback_is_pinned(self):
        targets=dict(TARGETS)
        self.assertEqual(targets["global-pc-any-filename"],{"system":"PC","contents":"sa174hg.exe"})

if __name__=="__main__":
    unittest.main()
