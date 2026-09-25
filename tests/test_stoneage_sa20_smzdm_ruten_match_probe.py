import unittest
from tools.stoneage_sa20_smzdm_ruten_match_probe import (
    SMZDM_20_IMAGE,SMZDM_20_SHA256,TARGET_CARRIERS
)

class SA20SmzdmRutenMatchTests(unittest.TestCase):
    def test_reference_is_locked_to_known_photo_one(self):
        self.assertIn("576276487bf54",SMZDM_20_IMAGE)
        self.assertEqual(
            SMZDM_20_SHA256,
            "98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3"
        )

    def test_controls_cover_all_early_mainland_roles(self):
        self.assertEqual(set(TARGET_CARRIERS),{
            "22631284715652","22636573895893","22638643800877"
        })

if __name__=="__main__":
    unittest.main()
