import unittest
from tools.stoneage_shiqi_blog_early_disc_probe import discover_article,image_urls,relevant_text,TITLE

class ShiqiBlogEarlyDiscProbeTests(unittest.TestCase):
    def test_discovers_article_by_title(self):
        h=f'<a href="/post/abc.htm">{TITLE}</a>'
        self.assertEqual(discover_article(h),("https://blog.shiqi.so/post/abc.htm",))

    def test_extracts_images_and_relevant_text(self):
        h='<p>大陆版2.0客户端光盘，北京华义。</p><img src="/img/a.jpg">'
        self.assertEqual(image_urls(h,"https://blog.shiqi.so/x.htm"),("https://blog.shiqi.so/img/a.jpg",))
        self.assertTrue(any("2.0" in x for x in relevant_text(h)))

if __name__=="__main__":
    unittest.main()
