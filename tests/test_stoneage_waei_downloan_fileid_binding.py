import unittest
from tools.stoneage_waei_downloan_fileid_binding import anchors,strip
class T(unittest.TestCase):
    def test_anchor(self):
        a=anchors('<a href="http://www7.waei.net/download/download.asp?fileid=37">800 x 600</a>')
        self.assertEqual(a[0][3],"http://www7.waei.net/download/download.asp?fileid=37")
        self.assertEqual(a[0][4],"800 x 600")
    def test_strip(self): self.assertIn("試玩",strip("<b>試玩</b>"))
if __name__=="__main__":unittest.main()
