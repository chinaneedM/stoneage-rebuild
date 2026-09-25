import unittest, zipfile, io
from tools.stoneage_2000_sina_direct_recovery import TARGET,zip_inventory,choose_capture

class DirectRecoveryTests(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET,"http://202.106.184.193/downfiles/map_1212/samap_1220.zip")

    def test_zip_inventory(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,"w",zipfile.ZIP_DEFLATED) as z:
            z.writestr("map/1.DAT",b"abc")
        rows,iszip=zip_inventory(b.getvalue())
        self.assertTrue(iszip)
        self.assertEqual(rows[0]["name"],"map/1.DAT")
        self.assertEqual(rows[0]["size"],3)

    def test_choose_capture_prefers_http_200(self):
        rows=[
            {"timestamp":"20010126074600","status":"302","url":"x"},
            {"timestamp":"20010127000000","status":"200","url":"y"},
        ]
        self.assertEqual(choose_capture(rows)["url"],"y")

if __name__=="__main__":
    unittest.main()
