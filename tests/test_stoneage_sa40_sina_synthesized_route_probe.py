import unittest
from tools.stoneage_sa40_sina_synthesized_route_probe import BASE,TARGET,TARGET_FILE

class SinaSynthesizedRouteTests(unittest.TestCase):
    def test_exact_category_base(self):
        self.assertEqual(BASE,"http://202.106.185.223/updatex_1024/")
        self.assertTrue(TARGET.endswith("/"+TARGET_FILE))
        self.assertEqual(TARGET_FILE,"shiqi4updatex_02_11_08.zip")

if __name__=="__main__":
    unittest.main()
