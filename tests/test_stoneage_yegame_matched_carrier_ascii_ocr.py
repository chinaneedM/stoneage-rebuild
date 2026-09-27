import unittest
from tools.stoneage_yegame_matched_carrier_ascii_ocr import TARGET, TOKEN_PATTERNS

class T(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET,"22636573895893")

    def test_patterns(self):
        sample="STONEAGE V1.0 P-RPG-0008 ISBN 4710739350098"
        hits=[]
        for p in TOKEN_PATTERNS:
            hits.extend(m.group(0) for m in p.finditer(sample))
        self.assertTrue(any("P-RPG" in x for x in hits))
        self.assertTrue(any("STONEAGE" in x for x in hits))

if __name__=="__main__":
    unittest.main()
