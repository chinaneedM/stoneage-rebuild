"""PET86: 2011 original-PC source-specific names/variants with region, native-ID and release gates."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "recovered"


class PET86Review(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads((DATA / "STONEAGE-PET86-YEAR2011-CN-NAMED-PETS-TW-HK-KR-JP-SOURCE-BOUNDARIES-R1.json").read_text(encoding="utf-8"))
        cls.q = json.loads((DATA / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))

    def test_2011_cursor_only_partial_and_forward_receipt(self):
        a, q = self.a, self.q
        self.assertEqual((a["year"], a["year_frontier_before"], a["year_frontier_after"]), (2011, 2011, 2011))
        self.assertEqual(q["current_frontier"]["year"], 2011)
        self.assertEqual(q["yearly_work_queue"][12]["research_gate"], "NOT_YEAR_AUDITED")
        self.assertFalse(a["historically_complete"])
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"], a["id"])
        self.assertEqual(sum(x["id"] == a["id"] for x in q["root_source_census_receipts"]), 1)
        self.assertEqual(sum(x["id"] == a["id"] for x in q["yearly_work_queue"][12]["partial_source_review_receipts"]), 1)
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}), len(q["root_source_census_receipts"]))
        self.assertIsNone(a["first_release_species_count_2011"])
        self.assertIsNone(a["official_species_count"])

    def test_vip_snow_penguin_and_enhanced_not_species_first(self):
        a = self.a
        self.assertEqual(len(a["sources"]), 12)
        self.assertEqual(len(a["named_pet_attestations"]), 30)
        vip = [x["name"] for x in a["named_pet_attestations"] if x["source_id"] == "CNVIP"]
        self.assertEqual(vip, ["戈力多", "戈力拉", "古丁巴拉", "古丁亚拉", "古丁拉尔", "古丁格格"])
        self.assertTrue(a["differences"]["january_vip_article_mistypes_戈力拉_as_戈力多_in_body"])
        reinforced = [x["name"] for x in a["named_pet_attestations"] if x["source_id"] == "CNREINFORCE"]
        self.assertEqual(reinforced, ["克克洛斯", "霍尔克", "奇宝", "火鸡", "邦奇诺", "利则诺顿", "邦浦洛斯", "布鲁顿", "奥卡洛斯"])
        self.assertEqual([x["skill"] for x in a["skill_claims"] if x["source_id"] == "CNREINFORCE"], ["致命攻击", "憎恨", "齿击"])
        self.assertTrue(all(x["original_client_pet_id"] is None and not x["first_release_new_species_verified"] for x in a["named_pet_attestations"]))

    def test_starter_card_version_lanes_and_wolves(self):
        a = self.a
        rows = a["named_pet_attestations"]
        self.assertEqual([(x["name"], x["version_lane"]) for x in rows if x["source_id"] == "CNSEPT" and x["version_lane"] in ("CN25", "CN85")],
                         [("齐尔格尔顿", "CN25"), ("朵巴奈特", "CN85")])
        self.assertEqual([(x["name"], x["version_lane"]) for x in rows if x["source_id"] == "CNOCT" and x["version_lane"] in ("CN25", "CN85")],
                         [("贝洛金", "CN25"), ("戈登尔顿", "CN85")])
        self.assertEqual([(x["name"], x["version_lane"]) for x in rows if x["source_id"] == "CNDEC"],
                         [("乌拉拉", "CN25"), ("格尔希洛", "CN85")])
        self.assertTrue(a["differences"]["september_black_朵巴奈特_not_automatically_equal_january_rage_version"])
        self.assertEqual(a["differences"]["october_wolf_skill"], "爆裂攻击")
        wolf = [x for x in a["skill_claims"] if x["source_id"] == "CNOCT"]
        self.assertEqual(len(wolf), 1)
        self.assertFalse(wolf[0]["native_runtime_verified"])

    def test_regional_and_client_negative_source_boundaries(self):
        a = self.a
        self.assertEqual(set(a["region_residuals"]), {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"})
        self.assertTrue(all(a["guards"].values()))
        self.assertEqual(a["client_source"]["download_error"], "HTTP_403")
        self.assertEqual(a["client_source"]["operator_url_result"], "TIMEOUT")
        self.assertFalse(a["client_source"]["original_sha_verified"])
        self.assertEqual(a["client_source"]["original_bytes_acquired"], 0)
        self.assertEqual((a["new_original_client_bytes"], a["new_native_pet_ids"], a["new_actual_server_grants"]), (0, 0, 0))
        self.assertEqual(a["differences"]["hkmo_server_planned"], "2011-10 港龍星系")
        self.assertTrue(a["differences"]["hkmo_server_actual_pet_grant_unverified"])
        self.assertTrue(a["differences"]["korea_web_petit_not_original_pc"])
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))

    def test_original_current_git_blob_preserved(self):
        raw = (ROOT / "docs" / "CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(sha, self.a["startup"]["current_blob"])


if __name__ == "__main__":
    unittest.main()
