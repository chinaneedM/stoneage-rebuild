import unittest
from tools.stoneage_popsoft_200012_exact_disc_probe import IMAGES, ia_url, discm_url

class T(unittest.TestCase):
    def test_exact_image_tokens(self):
        rows={label:(name,sha1,size) for label,name,sha1,size in IMAGES}
        self.assertEqual(rows["cd1"][0],"popcd2k12_a.iso")
        self.assertEqual(rows["cd2"][0],"popcd2k12_b.iso")
        self.assertEqual(rows["cd1"][1],"1D674459E1EC61706A688AA73C94DFDC1802C074")
        self.assertEqual(rows["cd2"][1],"97CF4340916C39D9AA56278C6B86615E8D486DEC")

    def test_query_modes(self):
        self.assertIn("advancedsearch.php",ia_url("popcd2k12_a.iso"))
        self.assertIn("qfields=name",discm_url("popcd2k12_a.iso","name"))
        self.assertIn("qfields=t",discm_url("popcd2k12_a.iso","t"))

if __name__=="__main__":
    unittest.main()
