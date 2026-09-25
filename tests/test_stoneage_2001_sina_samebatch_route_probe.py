import unittest
from tools.stoneage_2001_sina_samebatch_route_probe import (
    row_matches, binary_links, substitute_filename, TARGET_FILENAME
)

class SameBatchRouteProbeTests(unittest.TestCase):
    def test_row_matches(self):
        row={"original":"http://x/download.pl?col=map&aid=43124&filename=dflwaztekspride_1119.zip"}
        self.assertTrue(row_matches(row,"43124","dflwaztekspride_1119.zip"))
        self.assertFalse(row_matches(row,"99999","other.zip"))

    def test_binary_links(self):
        b=b'<a href="http://202.1.2.3/map_1127/dflwaztekspride_1119.zip">download</a>'
        self.assertEqual(
            binary_links(b,"http://games.sina.com.cn/x"),
            ("http://202.1.2.3/map_1127/dflwaztekspride_1119.zip",)
        )

    def test_substitute_filename(self):
        u="http://202.1.2.3/map_1127/dflwaztekspride_1119.zip"
        self.assertEqual(
            substitute_filename(u,"dflwaztekspride_1119.zip"),
            "http://202.1.2.3/map_1127/"+TARGET_FILENAME
        )
        self.assertEqual(substitute_filename(u,"other.zip"),"")

if __name__=="__main__":
    unittest.main()
