import unittest
from tools.stoneage_2001_discmaster_estoneage_probe import walk_rows, row_path, strict, TARGET

class DiscMasterEstoneageProbeTests(unittest.TestCase):
    def test_walk_rows(self):
        obj={"results":[{"itemid":"1","itemName":"disc","fileid":"x/estoneage.exe","b3sum":"a"}]}
        rows=walk_rows(obj)
        self.assertEqual(len(rows),1)
        self.assertEqual(row_path(rows[0]),"x/estoneage.exe")

    def test_strict(self):
        self.assertTrue(strict({"fileid":"disc/"+TARGET}))
        self.assertFalse(strict({"fileid":"disc/estoneage.exe"}))

if __name__=="__main__":
    unittest.main()
