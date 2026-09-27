import unittest
from tools.stoneage_waei_www9_download_pages import plain,links
class Tests(unittest.TestCase):
    def test_plain(self):self.assertEqual(plain("<b>A</b>  B"),"A B")
    def test_links(self):self.assertEqual(links('<a href="x.exe">X</a>',"http://a/")[0][0],"http://a/x.exe")
if __name__=="__main__":unittest.main()
