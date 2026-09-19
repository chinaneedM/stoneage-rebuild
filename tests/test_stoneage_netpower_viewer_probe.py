import unittest
from tools.stoneage_netpower_viewer_probe import clean

class NetPowerViewerProbeTests(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean("a&amp;b\x00"),"a&b")
        self.assertLessEqual(len(clean("x"*2000)),1000)

if __name__=="__main__":
    unittest.main()
