import unittest
from tools.stoneage_sa25_smzdm_disc_probe import section, image_urls

class T(unittest.TestCase):
    def test_section(self):
        s="x游戏安装光盘<img src='https://a.example/disc.jpg'>游戏说明书y"
        seg,a,b=section(s)
        self.assertIn("disc.jpg",seg)
    def test_images(self):
        self.assertEqual(image_urls("<img src='https://a.example/disc.jpg'>"),("https://a.example/disc.jpg",))

if __name__=="__main__":
    unittest.main()
