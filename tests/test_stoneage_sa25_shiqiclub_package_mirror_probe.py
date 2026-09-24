import unittest
from tools.stoneage_sa25_shiqiclub_package_mirror_probe import hits, relevant_attrs

class T(unittest.TestCase):
    def test_hits(self):
        s="2.5精灵王传说 客户端礼包 WGS"
        h=hits(s.encode("utf-8"),s)
        self.assertIn("2.5精灵王传说",h)
        self.assertIn("WGS",h)
    def test_attrs(self):
        x=relevant_attrs('<img src="/upload/a.jpg"><a href="/plain">x</a>')
        self.assertEqual(x,("/upload/a.jpg",))

if __name__=="__main__":
    unittest.main()
