import unittest
from tools.stoneage_sa25_shiqiclub_body_images_probe import body_slice, body_images

class T(unittest.TestCase):
    def test_slice_and_images(self):
        s='<div>nav<img src="/nav.jpg"></div><p>我又来更新</p><img src="/zb_users/upload/a.jpg"><p>x</p><img data-src="//x/b.jpg"><p>Tags：</p><img src="/footer.jpg">'
        frag,a,b=body_slice(s)
        self.assertGreaterEqual(a,0)
        imgs=body_images(frag)
        self.assertEqual([x[1] for x in imgs],["https://www.shiqi.club/zb_users/upload/a.jpg","https://x/b.jpg"])

if __name__=="__main__":
    unittest.main()
