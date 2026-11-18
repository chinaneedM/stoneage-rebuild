"""PET85: 2011 original PC period named pet source vs announced/runtime/species gates."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"


class PET85Year2011(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads((REC / "STONEAGE-PET85-YEAR2011-CN85-TW-OFFICIAL-PET-EVENT-CANDIDATES-R1.json").read_text(encoding="utf-8"))
        cls.q = json.loads((REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))

    def test_chronological_cursor_receipt_append_only(self):
        a, q = self.a, self.q
        y = q["yearly_work_queue"][2011 - 1999]
        self.assertEqual((a["year"], a["year_frontier_before"], a["year_frontier_after"]), (2011, 2011, 2011))
        self.assertGreaterEqual(q["current_frontier"]["year"], 2011)
        self.assertIn(y["research_gate"], ("NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"))
        # PET85 remains a unique historical receipt even after PET86/PET87 append newer ones.
        self.assertIn(a["id"], [x["id"] for x in y["partial_source_review_receipts"]])
        self.assertIn(a["id"], [x["id"] for x in q["root_source_census_receipts"]])
        self.assertEqual(sum(x["id"] == a["id"] for x in y["partial_source_review_receipts"]), 1)
        self.assertEqual(sum(x["id"] == a["id"] for x in q["root_source_census_receipts"]), 1)
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}), len(q["root_source_census_receipts"]))
        self.assertFalse(a["historically_complete"])
        self.assertIsNone(a["confirmed_2011_first_new_species"])

    def test_cn_january_separate_pet_input_vs_random_reward(self):
        e = self.a["exact_event_contracts"]
        x = e["2011_CN_JAN17"]
        self.assertEqual((x["input_pet"], x["input_level"]), ("乌力斯坦", 50))
        self.assertEqual(x["pet_training_reward"], "RANDOM_TOYS_NOT_PETS")
        self.assertEqual(x["separate_monster_event_reward"], "PET_EXCHANGE_VOUCHER_RANDOM_SPECIES_UNKNOWN")
        j = e["2011_CN_JAN26_FEB09"]
        self.assertEqual(j["rage_input_pet"], "朵巴奈特")
        self.assertEqual(j["rage_input_min_level_inclusive"], 100)
        self.assertEqual(j["rage_input_level_operator_text"], "Lv100以上")
        self.assertEqual(j["scorpion_input_min_level_inclusive"], 120)
        self.assertEqual(j["scorpion_input_level_operator_text"], "Lv120以上")
        self.assertNotIn("rage_input_level_greater_than", j)
        self.assertNotIn("scorpion_input_level_greater_than", j)
        self.assertEqual(j["rage_output"], "狂暴版朵巴奈特")
        self.assertEqual(j["rage_skill"], "狂暴攻击")
        self.assertEqual(j["scorpion_input_pet"], "欧西摩米")
        self.assertEqual(j["scorpion_random_outputs"], ["史卡皮诺", "史卡皮克", "史卡皮奥", "史卡皮顿"])
        self.assertEqual(j["scorpion_advertised_skills"], ["精准", "深层注射"])
        self.assertFalse(j["actual_grant_receipt_verified"])

    def test_honor_shop_predicted_vs_operator_current(self):
        src = {x["id"]: x for x in self.a["sources"]}
        self.assertEqual(src["CN2011-JUN20-HONOR-SHOP-PLANNED"]["date"], "2011-06-20")
        self.assertEqual(src["CN2011-JUL08-HONOR-SHOP-CURRENT"]["date"], "2011-07-08")
        h = self.a["exact_event_contracts"]["2011_CN_JUN_JUL_SHOP"]
        self.assertEqual(h["announced_shop_open"], "2011-06-22")
        self.assertEqual(h["availability_claim_labels"], ["夏克", "多芬", "洛奇斯德"])
        self.assertTrue(h["july_operator_says_currently_available"])
        self.assertTrue(h["honor_points_earnable_via_dailies"])
        self.assertFalse(h["real_money_required_for_this_shop"])
        self.assertFalse(h["shop_transaction_verified"])
        named = self.a["named_pet_claims"]
        self.assertEqual(len(named), 11)
        self.assertEqual(
            [x["name"] for x in named if x["source_id"] == "CN2011-JUN20-HONOR-SHOP-PLANNED"],
            ["扑满乌力", "猴子蒙奇", "人鱼艾尔摩米"],
        )
        self.assertTrue(all(x["native_pet_id"] is None and not x["official_first_release_2011_proven"] for x in named))

    def test_region_and_version_boundaries(self):
        a = self.a
        t = a["exact_event_contracts"]["2011_TW_APR"]
        self.assertEqual((t["announced_original_client_and_patch_download"], t["announced_nonwipe_public_test"]), ("2011-04-25", "2011-04-29"))
        self.assertEqual(t["actual_client_bytes_acquired"], 0)
        self.assertEqual(set(a["regional_gaps"]), {"CN", "TW", "JP", "KR", "OTHER"})
        self.assertTrue(all(a["negative_gates"].values()))
        self.assertEqual((a["new_original_2011_client_bytes"], a["new_native_2011_pet_ids"], a["new_actual_original_reward_logs"]), (0, 0, 0))
        self.assertIsNone(a["global_species_count"])
        self.assertEqual(a["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual((a["stage_B_wiki"], a["r79"], a["overall_percent"]), ("GATED", "PAUSED_NON_BLOCKING", None))

    def test_full_historical_current_blob_unmodified(self):
        raw = (ROOT / "docs" / "CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        got = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(got, self.a["startup"]["original_current_git_blob"])


if __name__ == "__main__":
    unittest.main()
