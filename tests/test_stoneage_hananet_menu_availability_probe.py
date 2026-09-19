import unittest
from tools.stoneage_hananet_menu_availability_probe import closest

class HananetMenuAvailabilityProbeTests(unittest.TestCase):
    def test_closest(self):
        self.assertEqual(
            closest({"archived_snapshots":{"closest":{"available":True,"timestamp":"20010118211100","status":"200","url":"x"}}}),
            ("20010118211100","200","x"),
        )
        self.assertIsNone(closest({"archived_snapshots":{}}))

if __name__=="__main__":
    unittest.main()
