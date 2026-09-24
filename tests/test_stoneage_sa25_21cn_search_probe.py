import unittest
import urllib.parse

from tools.stoneage_sa25_21cn_search_probe import (
    catalogue_id, encoded_query, stoneage_anchors
)


class SA2521CNSearchTests(unittest.TestCase):
    def test_gb2312_query(self):
        u=encoded_query("http://download.21cn.com/forsearch.php","s_keyword","石器时代","gb2312")
        self.assertIn("s_keyword=",u)
        self.assertIn("%CA%AF",u)

    def test_catalogue_id(self):
        self.assertEqual(catalogue_id("./list.php?id=20165"),"20165")

    def test_anchor(self):
        text='<a href="./list.php?id=9">石器时代2.5完整客户端</a><a href="x">other</a>'
        rows=stoneage_anchors(text)
        self.assertEqual(rows[0][2],"9")
        self.assertEqual(len(rows),1)


if __name__=="__main__":
    unittest.main()
