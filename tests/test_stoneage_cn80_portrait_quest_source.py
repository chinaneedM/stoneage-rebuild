"""Adversarial intake cases: prevent fabrication across versions and incomplete steps."""
import unittest
from tools.stoneage_cn80_portrait_quest_source import (
    INDEX, DETAIL, PETS, validate_url, derive, split_steps,
)
def fixtures():
    index = '<html><body><a href="sa80_05.shtml">爱作画的少女</a></body></html>'
    step = {
        1:"瑞而亚斯之都的(67.75)跟纱美加接任务",
        2:"瑞而亚斯之都的(59.17)便利店里面(26.47)迪伊恩对话",
        13:"得到5种颜色瑞而亚斯，找纱美加画画，这时不能骑宠",
        14:"得到5幅自画像"
    }
    for name, color, _place, cap, pay in PETS:
        step[cap] = "去洞窟(44.15)(37.20)(9.43)捕捉1级宠物"+name
        step[pay] = "返回迪伊恩交出"+name+"得到"+color+"颜料"
    guide = '<html><body>爱作画的少女 石器8.0版本任务全攻略 '+\
        ' '.join(f'{n}.{step[n]}' for n in range(1,15))+'</body></html>'
    return index.encode('utf-8')+b' '*500, guide.encode('utf-8')+b' '*500

class QuestSourceNegativeTests(unittest.TestCase):
    def test_positive_derived_and_unknowns(self):
        idx, page = fixtures()
        r = derive(idx,page)
        self.assertEqual(r["step_count"],14)
        self.assertEqual(len(r["pet_to_pigment"]),5)
        self.assertEqual(r["pet_to_pigment"][4]["pigment_color"],"蓝色")
        self.assertIsNone(r["unknowns"]["quest_flags"])
        self.assertIsNone(r["original_publication_date"])
        self.assertFalse(r["prerequisites"]["none_proven"])
    def test_fullwidth_source_coordinate_punctuation(self):
        index, page = fixtures()
        page = page.replace(b"(67.75)", "（67.75）".encode("utf-8"))
        page = page.replace(b"(59.17)", "（59.17）".encode("utf-8"))
        page = page.replace(b"(26.47)", "（26.47）".encode("utf-8"))
        r = derive(index, page)
        self.assertEqual(r["character_roles"][1]["reported_shop_internal_xy"], [26, 47])
    def test_wrong_official_or_redirected_location_rejected(self):
        for bad in [
            "http://news.17173.com/z/stoneage/renwu/sa80_05.shtml",
            "https://example.com/z/stoneage/renwu/sa80_05.shtml",
            "https://news.17173.com/z/stoneage/renwu/sa80_06.shtml",
            "https://news.17173.com/z/stoneage/renwu/sa80_05.shtml?modified=1"
        ]:
            with self.assertRaises(ValueError):
                validate_url(bad, DETAIL)
    def test_wrong_link_refused(self):
        idx,page=fixtures()
        with self.assertRaises(ValueError):
            derive(idx.replace(b"sa80_05",b"sa80_06"),page)
    def test_incomplete_step_sequence_refused(self):
        idx,page=fixtures()
        page=page.replace("13.得到".encode(), "15.得到".encode())
        with self.assertRaises(ValueError):
            derive(idx,page)
    def test_swapped_pet_color_refused(self):
        idx,page=fixtures()
        page=page.replace("贝洛宝利得到红色".encode(),"贝洛宝利得到紫色".encode())
        with self.assertRaises(ValueError):
            derive(idx,page)
    def test_wrong_reward_claim_rejected(self):
        idx,page=fixtures()
        page=page.replace("5幅自画像".encode(),"1幅自画像".encode())
        with self.assertRaises(ValueError):
            derive(idx,page)
    def test_step_numbers_cannot_be_inferred_from_arbitrary_text(self):
        with self.assertRaises(ValueError):
            split_steps("第二回6.0设计文案，没有任务步骤")

if __name__ == "__main__":
    unittest.main()
