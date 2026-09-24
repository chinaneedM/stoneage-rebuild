import unittest
from tools.stoneage_sa25_bahamut_client_package_probe import image_sequence, token_hits

class T(unittest.TestCase):
    def test_image_sequence(self):
        s='a https://cos.stoneage.cn/uploads/article/minisnsimg/20200923/abc.jpg b https://cos.stoneage.cn/uploads/article/minisnsimg/20200923/abc.jpg'
        self.assertEqual(len(image_sequence(s)),1)
    def test_tokens(self):
        b='2.5精靈王傳說用戶端WGS'.encode('utf-8')
        h=token_hits(b,b.decode())
        self.assertIn('2.5',h)
        self.assertIn('精靈王傳說',h)
        self.assertIn('WGS',h)

if __name__=="__main__":
    unittest.main()
