import unittest
from tools.stoneage_waei_2001q4_launch_residual_probe import day_distance, route_score

class WaeiQ4LaunchResidualProbeTests(unittest.TestCase):
    def test_target_date_closest(self):
        self.assertLess(day_distance("20011102090000"),day_distance("20011027090000"))
    def test_client_binary_scores_high(self):
        self.assertGreaterEqual(route_score("http://1.2.3.4/down/stoneage2.0setup.exe"),10)
    def test_asset_scores_low(self):
        self.assertLess(route_score("http://www.waei.com.cn/img/logo.gif"),4)

if __name__=="__main__":
    unittest.main()
