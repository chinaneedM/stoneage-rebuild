import unittest
from tools.stoneage_2000_sina_direct_route_probe import TARGET,FILENAME,HOST,variants,relevant

class DirectRouteProbeTests(unittest.TestCase):
    def test_target_identity(self):
        self.assertEqual(TARGET,"http://202.106.184.193/downfiles/map_1212/samap_1220.zip")
        self.assertEqual(FILENAME,"samap_1220.zip")
        self.assertEqual(HOST,"202.106.184.193")

    def test_variants_include_exact(self):
        self.assertIn(TARGET,variants())

    def test_relevant_filters_host_and_filename(self):
        rows=[
            {"original":"http://202.106.184.193/downfiles/map_1212/samap_1220.zip"},
            {"original":"http://example.com/downfiles/map_1212/samap_1220.zip"},
            {"original":"http://202.106.184.193/downfiles/map_1212/other.zip"},
        ]
        self.assertEqual(len(relevant(rows)),1)

if __name__=="__main__":
    unittest.main()
