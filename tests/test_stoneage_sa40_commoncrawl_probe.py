import unittest
from tools.stoneage_sa40_commoncrawl_probe import hget
class CCTests(unittest.TestCase):
    def test_header(self):
        self.assertEqual(hget("HTTP/1.1 302 Found\r\nLocation: http://x/y.zip\r\n","Location"),"http://x/y.zip")
if __name__=="__main__":unittest.main()
