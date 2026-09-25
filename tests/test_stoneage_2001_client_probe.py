import unittest
from tools.stoneage_2001_client_probe import FILENAME,AID,source_hrefs
class ClientProbeTests(unittest.TestCase):
    def test_target(self):
        self.assertEqual(FILENAME,"stoneage2.0setup.exe")
        self.assertEqual(AID,"41967")
    def test_href(self):
        b=b'<a href="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=demo&aid=41967&filename=stoneage2.0setup.exe&size=524377">x</a>'
        self.assertEqual(len(source_hrefs(b)),1)
if __name__=="__main__": unittest.main()
