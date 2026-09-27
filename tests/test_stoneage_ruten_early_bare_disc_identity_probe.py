import unittest
from tools.stoneage_ruten_early_bare_disc_identity_probe import TARGET, walk, visible

class T(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET,"22111215616086")

    def test_public_field_filter(self):
        rows=dict(walk({"data":[{"name":"STONEAGE","model":"P-RPG-0008"}]}))
        self.assertEqual(rows["data[0].name"],"STONEAGE")
        self.assertEqual(rows["data[0].model"],"P-RPG-0008")

    def test_visible(self):
        self.assertIn("STONEAGE",visible("<body>STONEAGE V1.0</body>"))

if __name__=="__main__":
    unittest.main()
