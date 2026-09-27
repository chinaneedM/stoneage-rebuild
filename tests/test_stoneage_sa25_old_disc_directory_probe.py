import unittest

from tools.stoneage_sa25_old_disc_directory_probe import (
    dir_from_href,
    file_class,
    is_old_disc_root,
    parse_links,
    token_hits,
    under_root,
)


class OldDiscDirectoryProbeTests(unittest.TestCase):
    def test_parse_directory_links(self):
        body = (
            '<a href="?dir=14%E8%80%81%E5%85%89%E7%9B%98%E7%BE%A4/2019-12-29">x</a>'
            '<a href="/foo/%E4%B8%AD%E5%AD%A6%E7%94%9F%E7%94%B5%E8%84%91.iso">disc</a>'
        ).encode()
        links = parse_links(body)
        self.assertEqual(len(links), 2)
        self.assertEqual(dir_from_href(links[0][0]), "14老光盘群/2019-12-29")
        self.assertIsNone(dir_from_href(links[1][0]))

    def test_root_and_tree_boundary(self):
        self.assertTrue(is_old_disc_root("14老光盘群(群号854318908)群友分享汇总"))
        self.assertFalse(is_old_disc_root("Brocade_FOS"))
        self.assertTrue(under_root("14老光盘群/a/b", "14老光盘群"))
        self.assertFalse(under_root("15老光盘群/a", "14老光盘群"))

    def test_token_matching(self):
        hits = token_hits("收藏/中学生电脑/2002年攻略特刊.iso")
        self.assertIn("中学生电脑", hits)
        self.assertIn("攻略特刊", hits)
        self.assertIn("石器时代2.5", token_hits("backup/石器时代2.5客户端.rar"))

    def test_file_classes(self):
        self.assertEqual(file_class("x.iso"), "optical")
        self.assertEqual(file_class("x.cue"), "optical")
        self.assertEqual(file_class("x.rar"), "archive")
        self.assertEqual(file_class("x.pdf"), "document")
        self.assertEqual(file_class("x.jpg"), "other")


if __name__ == "__main__":
    unittest.main()
