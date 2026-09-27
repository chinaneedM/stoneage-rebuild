import unittest
from tools.stoneage_waei_saupdate_lineage_probe import NEEDLES,path_sets,battle_ids,pe_timestamp

class WaeiSaupdateLineageTests(unittest.TestCase):
    def test_needles(self):
        self.assertIn("CheckForUpdate",NEEDLES)
        self.assertIn("ClientLogin",NEEDLES)
    def test_paths(self):
        p=path_sets(["xx data\\battleMap\\battle219.sab yy","data\\AISetting.dat"])
        self.assertIn("data\\battleMap\\battle219.sab",p)
        self.assertEqual(battle_ids(p),[219])
    def test_nonpe(self):
        self.assertIsNone(pe_timestamp(b"abc"))
if __name__=="__main__":
    unittest.main()
