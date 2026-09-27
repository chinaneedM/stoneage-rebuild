import json
import unittest
from tools.stoneage_popsoft_2000_launch_window_probe import (
    launch_window_ocr_file,
    month_key,
    stoneage_context_hits,
    strong_hits,
)

class Popsoft2000LaunchWindowProbeTests(unittest.TestCase):
    def test_selects_launch_window_djvu(self):
        self.assertTrue(launch_window_ocr_file({"name":"2000/大众软件-2000年12月A_djvu.txt"}))
        self.assertTrue(launch_window_ocr_file({"name":"2001/大众软件-2001年01月B_djvu.txt"}))
        self.assertFalse(launch_window_ocr_file({"name":"2002/大众软件-2002年02月A_djvu.txt"}))
        self.assertFalse(launch_window_ocr_file({"name":"2000/大众软件-2000年12月A.pdf"}))

    def test_month_key(self):
        self.assertEqual(month_key("2000/大众软件-2000年11月A_djvu.txt"),"2000年11月")
        self.assertEqual(month_key("x"),"")

    def test_strong_context(self):
        text="前文 石器时代 游戏测试光盘由晶合软件领取 后文"
        hits=stoneage_context_hits(text)
        self.assertTrue(hits)
        strong=strong_hits(hits)
        self.assertTrue(strong)
        flags=strong[0][2]
        self.assertIn("测试",flags)
        self.assertIn("光盘",flags)
        self.assertIn("晶合",flags)

    def test_editorial_only_not_strong(self):
        text="石器时代是一款网络角色扮演游戏，宠物系统很受欢迎。"
        hits=stoneage_context_hits(text)
        self.assertTrue(hits)
        self.assertFalse(strong_hits(hits))

if __name__=="__main__":
    unittest.main()
