import unittest

from tools.stoneage_sa25_21cn_ranking_id_probe import catalogue_id, matching_anchors


class SA2521CNRankingIdTests(unittest.TestCase):
    def test_catalogue_id(self):
        self.assertEqual(catalogue_id("./list.php?id=12345"),"12345")
        self.assertEqual(catalogue_id("http://download.21cn.com/list.php?id=999&x=1"),"999")

    def test_matching_anchor(self):
        text='<a href="./list.php?id=77">石器时代2.5-精灵王传说</a><a href="x">other</a>'
        rows=matching_anchors(text)
        self.assertEqual(rows,(("石器时代2.5-精灵王传说","./list.php?id=77"),))


if __name__=="__main__":
    unittest.main()
