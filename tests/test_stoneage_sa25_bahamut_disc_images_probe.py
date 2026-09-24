import unittest
from tools.stoneage_sa25_bahamut_disc_images_probe import image_sequence, local_context

class T(unittest.TestCase):
    def test_sequence_dedup(self):
        s='A https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/a.jpg B https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/b.jpg C https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/a.jpg'
        x=image_sequence(s)
        self.assertEqual([u.rsplit("/",1)[1] for _,u in x],["a.jpg","b.jpg"])

    def test_context(self):
        s="<p>到2.5精靈王傳說版本啦</p>"+("x"*20)
        self.assertIn("2.5",local_context(s,len(s)-1,100))

if __name__=="__main__":
    unittest.main()
