import unittest
from tools.stoneage_2000_sina_package_cluster_probe import TOKENS, exact_disc_rows, leaf

class PackageClusterProbeTests(unittest.TestCase):
    def test_cluster_contains_primary_target(self):
        names={x[1] for x in TOKENS}
        self.assertIn("samap_1220.zip",names)
        self.assertIn("0969-5_807.zip",names)

    def test_leaf(self):
        self.assertEqual(leaf("disc/maps/SAMAP_1220.ZIP"),"samap_1220.zip")

    def test_exact_disc_filter(self):
        data={"rows":[
            {"itemid":1,"itemName":"x","fileid":"disc/maps/samap_1220.zip"},
            {"itemid":2,"itemName":"y","fileid":"disc/maps/samap.zip"},
        ]}
        got=exact_disc_rows(data,"samap_1220.zip")
        self.assertEqual(len(got),1)
        self.assertEqual(got[0]["itemid"],1)

if __name__=="__main__":
    unittest.main()
