import unittest
from tools.stoneage_ruten_early_bare_disc_probe import TARGET, CONTROLS, public_identity

class T(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET[0],"22111215616086")
        self.assertEqual(TARGET[1],"early-bare-disc")

    def test_controls(self):
        roles={role for _,role in CONTROLS}
        self.assertIn("taiwan-client-box",roles)
        self.assertIn("beijing-waei-newbie-control",roles)
        self.assertIn("mainland-retail-box",roles)

    def test_public_identity(self):
        row={"name":"StoneAge","images":{"url":["https://x/a.jpg"]},"post_time":1,"sold_num":2,"num":3}
        ident=public_identity(row)
        self.assertEqual(ident["name"],"StoneAge")
        self.assertEqual(len(ident["images"]),1)

if __name__=="__main__":
    unittest.main()
