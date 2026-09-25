import unittest
from tools.stoneage_xinhaonanhai_carrier_census import IA_QUERIES, DM_QUERIES, TARGETS, strict_leaf

class XinhaonanhaiCarrierCensusTests(unittest.TestCase):
    def test_alias_and_both_generations_are_covered(self):
        joined="\n".join(q for _,q in IA_QUERIES)+"\n"+"\n".join(DM_QUERIES)
        self.assertIn("xinhaonanhai",joined)
        self.assertIn("Estoneage2.0map_1127",joined)
        self.assertIn("shiqi4updatex_02_11_08",joined)

    def test_strict_leaf_requires_exact_target_filename(self):
        self.assertEqual(strict_leaf("/x/Estoneage2.0map_1127.exe"),TARGETS[0])
        self.assertEqual(strict_leaf("shiqi4updatex_02_11_08.zip"),TARGETS[1])
        self.assertEqual(strict_leaf("copy-Estoneage2.0map_1127.exe"),"")

if __name__=="__main__":
    unittest.main()
