import unittest
from tools.stoneage_wayi_official_systems import identify_claims, anchored_sections, GEAR, FEET, ULI

def specimen():
    return [
        "本站的購物意見調查", "寵物裝備系統",
        "依照不同類型之寵物，給予不同之裝備欄位，也可以透過合成系統製作寵物裝備。",
        "七大類", "分別是頭、 牙、 爪、 胸、 背、 翅、 腳（兩隻腳、四隻腳、魚鰭）",
        "烏力頭盔〔水〕攻擊力+15", "烏力〔地 8 水 2〕", "烏力烏力〔水 4 火 6〕",
        "依照相生相剋關係調整", "烏力最多只能裝備：頭、牙、胸、背、腳",
        "導師系統", "〔領導聲望〕〔導師帳號〕〔導師姓名〕〔導師〕〔學生〕",
        "百分之五聲望", "任務日誌", "曾經解過的任務", "未曾解過的任務",
        "〔遊戲線上說明〕",
    ]

class SystemContractTests(unittest.TestCase):
    def test_bounded_contract(self):
        r=identify_claims(specimen())
        self.assertEqual(r["equipment"]["slot_categories_in_source_order"], GEAR)
        self.assertEqual(r["equipment"]["foot_subtypes_in_source_order"], FEET)
        self.assertEqual(r["equipment"]["uli_example_eligible_slots"], ULI)
        self.assertIsNone(r["equipment"]["exact_stat_scaling_formula"])
        self.assertEqual(r["mentor"]["leadership_prestige_described_as_student_prestige_share"], "5%")
        self.assertFalse(r["mentor"]["student_reputation_deducted_proven"])
        self.assertIsNone(r["quest_log"]["original_task_ids_or_completion_flags"])
    def test_missing_or_misordered_anchor_rejected(self):
        s=specimen()
        with self.assertRaises(ValueError):
            anchored_sections([x for x in s if x!="任務日誌"])
        with self.assertRaises(ValueError):
            anchored_sections(["任務日誌"] + s)
    def test_category_and_stats_corruption_rejected(self):
        s=specimen()
        with self.assertRaises(ValueError):
            identify_claims([x.replace("兩隻腳、四隻腳、魚鰭", "魚鰭") for x in s])
        with self.assertRaises(ValueError):
            identify_claims([x.replace("攻擊力+15", "攻擊力+50") for x in s])
    def test_unknown_field_and_mentor_not_promoted(self):
        s=specimen()
        with self.assertRaises(ValueError):
            identify_claims([x.replace("百分之五聲望", "百分之十聲望") for x in s])
        with self.assertRaises(ValueError):
            identify_claims([x.replace("未曾解過的任務", "解過的任務") for x in s])

if __name__=="__main__":
    unittest.main()
