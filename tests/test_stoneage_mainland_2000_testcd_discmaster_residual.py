import unittest
from tools.stoneage_mainland_2000_testcd_discmaster_residual import strict, rows_from

class Mainland2000TestCDDiscMasterResidualTests(unittest.TestCase):
    def test_strict(self):
        self.assertTrue(strict({"itemName":"StoneAge beta Waei CD"}))
        self.assertTrue(strict({"filename":"StoneAge_test.exe"}))
        self.assertTrue(strict({"text":"石器时代 晶合 测试"}))
        self.assertFalse(strict({"itemName":"Stone Age archaeology photos"}))
        self.assertFalse(strict({"itemName":"Other Game beta"}))

    def test_rows_deduplicate(self):
        obj={"a":[
            {"itemid":"1","fileid":"a","filename":"StoneAge.exe"},
            {"itemid":"1","fileid":"a","filename":"StoneAge.exe"},
        ]}
        self.assertEqual(len(rows_from(obj)),1)

if __name__=="__main__":
    unittest.main()
