import unittest

from tools.stoneage_sa25_21cn_record20165_related_probe import catalogue_id, related


class SA2521CNRecord20165RelatedTests(unittest.TestCase):
    def test_catalogue_id(self):
        self.assertEqual(catalogue_id("./list.php?id=22318"),"22318")
        self.assertEqual(catalogue_id("http://download.21cn.com/list.php?id=20165"),"20165")

    def test_related(self):
        text=(
            '<a href="./list.php?id=1">石器时代2.5完整客户端</a>'
            '<a href="./list.php?id=2">unrelated</a>'
        )
        rows=related(text)
        self.assertEqual(rows[0][2],"1")
        self.assertEqual(len(rows),1)


if __name__=="__main__":
    unittest.main()
