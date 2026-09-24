import unittest
from tools.stoneage_sa25_21cn_rank_link_probe import anchors,record_id,relevant_anchor
class T(unittest.TestCase):
    def test_anchor(self):
        a=anchors('<a href="./list.php?id=123">石器时代2.5-精灵王传说</a>')
        self.assertEqual(a,(("./list.php?id=123","石器时代2.5-精灵王传说"),))
        self.assertEqual(record_id(a[0][0]),"123")
        self.assertTrue(relevant_anchor(a[0][1],a[0][0]))
    def test_noise(self):
        self.assertFalse(relevant_anchor("新仙剑奇侠传","./list.php?id=2"))
if __name__=="__main__": unittest.main()
