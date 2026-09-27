import unittest
from tools.stoneage_waei_fileid133_route_probe import TARGETS
class Route133Tests(unittest.TestCase):
    def test_targets(self):
        self.assertTrue(any("fileid=133" in u for _,u in TARGETS))
        self.assertTrue(any("spr_1.bin" in u for _,u in TARGETS))
if __name__=="__main__":unittest.main()
