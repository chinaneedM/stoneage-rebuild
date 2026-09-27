import unittest
from tools.stoneage_sa40_sina_updatex_timeline_probe import qparams,filename_refs,TARGET_DATE

class SinaUpdatexTimelineTests(unittest.TestCase):
    def test_qparams_updatex(self):
        p=qparams("http://x/download.pl?col=updatex&aid=1&filename=a.zip")
        self.assertEqual(p["col"],"updatex")
        self.assertEqual(p["filename"],"a.zip")

    def test_filename_ref(self):
        h='<a href="http://202.106.185.223/updatex_1024/a.zip">a</a>'
        self.assertEqual(filename_refs(h,"http://x/","a.zip"),("http://202.106.185.223/updatex_1024/a.zip",))

    def test_target_date(self):
        self.assertEqual(TARGET_DATE,"20021108")

if __name__=="__main__":
    unittest.main()
