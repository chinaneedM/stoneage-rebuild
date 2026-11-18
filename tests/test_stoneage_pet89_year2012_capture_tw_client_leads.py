"""PET89: 2012 original PC capture-place claims, Taozhu client leads, and negative provenance guards."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "recovered"


def read(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


class PET89Year2012(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("STONEAGE-PET89-YEAR2012-CN-PET-CAPTURE-TW-OFFICIAL-CLIENT-RELAY-REGIONAL-GATES-R1.json")
        cls.q = read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_2012_forward_compatible_partial_receipt(self):
        a, q = self.a, self.q
        year = q["yearly_work_queue"][13]
        self.assertEqual((a["year"], a["year_frontier_before"], a["year_frontier_after"]), (2012, 2012, 2012))
        self.assertGreaterEqual(q["current_frontier"]["year"], 2012)
        self.assertIn(year["research_gate"], ("NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"))
        self.assertFalse(a["historically_complete"])
        self.assertEqual(a["year_research_gate"], "NOT_YEAR_AUDITED")
        self.assertIsNone(a["first_new_species_in_2012_count"])
        self.assertIsNone(a["global_2012_species_count"])
        rid = a["id"]
        self.assertEqual(sum(x["id"] == rid for x in year["partial_source_review_receipts"]), 1)
        self.assertEqual(sum(x["id"] == rid for x in q["root_source_census_receipts"]), 1)
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}), len(q["root_source_census_receipts"]))

    def test_same_source_cn_capture_place_2012_not_native_map(self):
        a = self.a
        source = {x["id"]: x for x in a["sources"]}
        s = source["CN2012FEB20HUBABA"]
        self.assertEqual(s["same_origin_count"], 1)
        self.assertFalse(s["native_encounter_table_verified"])
        expected = {
            "呼拔拔": "霍特尔村野外",
            "多萨金格": "漆黑洞窟",
            "鲁尼帖斯": "吉鲁山岭地下",
        }
        self.assertEqual({x["name"]: x["reported_location"]
                          for x in a["named_pet_source_mentions"] if x["source_id"] == s["id"]}, expected)
        self.assertEqual(a["capture_geography_text_only"]["original_native_encounter_map_row_count"], 0)
        self.assertIsNone(a["capture_geography_text_only"]["exact_capture_probability"])
        self.assertTrue(a["capture_geography_text_only"]["version_specific_CN_25_vs_85_not_attested"])
        self.assertTrue(all(x["native_pet_id"] is None and not x["confirmed_first_released_2012"]
                            for x in a["named_pet_source_mentions"]))

    def test_alias_and_historical_dating_negative_controls(self):
        a = self.a
        source = {x["id"]: x for x in a["sources"]}
        self.assertEqual(len(a["sources"]), 10)
        self.assertEqual(len(a["named_pet_source_mentions"]), 8)
        self.assertEqual([x["name"] for x in a["named_pet_source_mentions"] if x["source_id"] == "CN2012FEB03WOLF"],
                         ["怀肯沃", "坏肯沃", "塔斯夫"])
        self.assertTrue(a["contradiction_and_negative_gates"]["坏肯沃_怀肯沃_article_variants_not_two_species"])
        self.assertTrue(a["contradiction_and_negative_gates"]["old_2010_dragon_names_not_new_2012_species"])
        self.assertFalse(source["CN2012OCT25MYSTERY"]["named_pet_in_article"])
        self.assertFalse(source["CN2012NOV07BID"]["named_pet_in_article"])
        self.assertEqual([x["name"] for x in a["named_pet_source_mentions"] if x["source_id"] == "CN2012DEC12DRAGON"],
                         ["邦恩多斯", "斯天多斯"])
        self.assertTrue(all(a["contradiction_and_negative_gates"].values()))

    def test_taozhu_original_client_source_links_not_authenticated(self):
        a = self.a
        tw = a["tw_original_client_candidate"]
        self.assertEqual(tw["source_period_post_date"], "2012-12-28")
        self.assertEqual(tw["unmodified_original_provider_binary_url"],
                         "http://61.66.116.158/Sa_Free_installation.exe")
        self.assertEqual(tw["unmodified_original_provider_patch_url"], "http://61.66.116.158/sa.rar")
        self.assertFalse(tw["direct_binary_read_or_hash_verified"])
        self.assertEqual((tw["installer_bytes_acquired"], tw["patch_bytes_acquired"]), (0, 0))
        self.assertIsNone(tw["md5"])
        self.assertIsNone(tw["sha256"])
        self.assertFalse(tw["exact_2012_build_or_versions_verified"])
        g = a["tw_graphics_notice"]
        self.assertEqual(g["date_of_contemporaneous_player_post"], "2012-05-22")
        self.assertEqual(g["claimed_period_operator_notice"],
                         "2012-05-23 maintenance adds 特里卡莊園專屬騎寵圖檔")
        self.assertFalse(g["actual_png_spr_bitmap_acquired"])
        self.assertIsNone(g["entity_species_name"])

    def test_region_gaps_no_private_media_and_source_custody(self):
        a = self.a
        self.assertEqual(set(a["region_gaps"]), {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"})
        self.assertEqual((a["new_authentic_2012_client_bytes"], a["new_original_sprite_bytes"],
                          a["new_native_pet_ids"], a["new_native_encounter_records"],
                          a["new_actual_account_pet_grants"]), (0, 0, 0, 0, 0))
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))

    def test_original_historical_current_blob(self):
        a = self.a
        raw = (ROOT / "docs" / "CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(sha, a["startup"]["current_native_git_blob"])


if __name__ == "__main__":
    unittest.main()
