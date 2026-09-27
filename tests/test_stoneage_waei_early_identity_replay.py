import unittest
from tools.stoneage_waei_early_identity_replay import TARGETS,score_link
class EarlyIdentityReplayTests(unittest.TestCase):
    def test_targets(self):
        labels={x[0] for x in TARGETS}
        self.assertTrue({"sasp","brd172","brd173","stoneage-badlist","pid131"}.issubset(labels))
    def test_score(self):
        self.assertGreater(score_link("http://x/gamedetail.php?P_ID=131","石器時代"),0)
if __name__=="__main__":unittest.main()
