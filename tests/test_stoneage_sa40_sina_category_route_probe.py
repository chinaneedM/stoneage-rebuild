import unittest
from tools.stoneage_sa40_sina_category_route_probe import qparams,filename_urls,direct_shape

class SinaCategoryRouteTests(unittest.TestCase):
    def test_qparams(self):
        p=qparams("http://x/download.pl?col=updatex&aid=61620&filename=a.zip")
        self.assertEqual(p["col"],"updatex")
        self.assertEqual(p["filename"],"a.zip")

    def test_filename_url_extraction(self):
        h='<a href="http://202.1.2.3/update/a.zip">download</a>'
        self.assertEqual(filename_urls(h,"http://x/","a.zip"),("http://202.1.2.3/update/a.zip",))

    def test_direct_shape(self):
        self.assertEqual(
            direct_shape("http://202.1.2.3/update/a.zip"),
            ("http","202.1.2.3","/update/","a.zip"),
        )

if __name__=="__main__":
    unittest.main()
