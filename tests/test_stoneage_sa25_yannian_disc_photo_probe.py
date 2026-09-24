import unittest
from tools.stoneage_sa25_yannian_disc_photo_probe import target_rows

class T(unittest.TestCase):
    def test_target_rows(self):
        rows=(("u1","普通照片","普通照片"),("u2","2.5時期的光碟","2.5時期的光碟"),)
        t=target_rows(rows)
        self.assertEqual(len(t),1)
        self.assertEqual(t[0][1],"u2")

if __name__=="__main__":
    unittest.main()
