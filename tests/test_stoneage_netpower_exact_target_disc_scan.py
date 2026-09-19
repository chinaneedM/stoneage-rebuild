import unittest

from tools.stoneage_netpower_exact_target_disc_scan import (
    TARGET_ITEMS,
    select_images,
)


class ExactNetPowerDiscScanTests(unittest.TestCase):
    def test_target_items_are_exact_and_bounded(self):
        self.assertEqual(
            TARGET_ITEMS,
            ("netpower_cd_2000_11", "netpower_cd_2001_02"),
        )

    def test_image_selection_filters_small_and_duplicates(self):
        data = {
            "files": [
                {"name": "disc1.iso", "size": 600_000_000, "sha1": "a", "md5": "1"},
                {"name": "dup.iso", "size": 600_000_000, "sha1": "a", "md5": "2"},
                {"name": "disc2.bin", "size": 700_000_000, "sha1": "b", "md5": "3"},
                {"name": "tiny.img", "size": 1024, "sha1": "c", "md5": "4"},
                {"name": "disc.cue", "size": 80, "sha1": "d", "md5": "5"},
            ]
        }
        rows = select_images(data)
        self.assertEqual([row["name"] for row in rows], ["disc1.iso", "disc2.bin"])


if __name__ == "__main__":
    unittest.main()
