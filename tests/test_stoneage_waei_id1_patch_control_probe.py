import unittest
from tools.stoneage_waei_id1_patch_control_probe import TARGETS
class ProbeTests(unittest.TestCase):
    def test_targets(self):
        self.assertEqual(len(TARGETS),3)
        self.assertIn("石器隱形人無所遁形修正檔",TARGETS)
if __name__=="__main__":unittest.main()
