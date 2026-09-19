import unittest

from tools.stoneage_netpower_2000_09_disc_scan import TARGET_ITEM
from tools.stoneage_netpower_exact_target_disc_scan import select_images


class NetPower200009DiscScanTests(unittest.TestCase):
    def test_target_is_exact(self):
        self.assertEqual(TARGET_ITEM, "netpower_cd_2000_09")

    def test_shared_image_selection_keeps_large_unique_carriers(self):
        rows = select_images(
            {
                "files": [
                    {"name": "Net01.img", "size": 700_000_000, "sha1": "a", "md5": "1"},
                    {"name": "Net01.iso", "size": 600_000_000, "sha1": "b", "md5": "2"},
                    {"name": "Net01.cue", "size": 100, "sha1": "c", "md5": "3"},
                    {"name": "tiny.iso", "size": 1000, "sha1": "d", "md5": "4"},
                ]
            }
        )
        self.assertEqual([row["name"] for row in rows], ["Net01.img", "Net01.iso"])


if __name__ == "__main__":
    unittest.main()
