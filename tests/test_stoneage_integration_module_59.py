"""INTEGRATION59: public source-derived crosswalk guards; private original bytes are not CI inputs."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "research/recovered"
REPORT = PUB / "STONEAGE-INTEGRATION59-FOUR-VILLAGE-SHOP-120-ORIGINAL-NUMERIC-TW1-PIXEL-CROSSWALK-R1.json"
SHOP = PUB / "STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json"
SHARDS = [PUB / "item-module-01" / f"STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json" for i in range(1, 8)]


class TestIntegration59(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.old_shops = json.loads(SHOP.read_text(encoding="utf-8"))
        cls.old_rows = {}
        for path in SHARDS:
            old = json.loads(path.read_text(encoding="utf-8"))
            cls.old_rows.update({row[0]: row for row in old["rows"]})
        cls.item_records = {r["id"]: r for r in cls.report["original_item_numeric_row_records"]}

    def test_source_anchors(self):
        r = self.report
        self.assertEqual(r["baseline_main_HEAD"], "bf3c1ab27cfa71abb4a9ea32687aa9a178caf0e7")
        self.assertEqual(r["source_boundaries"]["preserved_ITEM01_private_replay_ZIP_sha256"], "cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa")
        self.assertEqual(r["source_boundaries"]["preserved_private_ZIP_member_CRC_pass"], 838)
        self.assertEqual(r["source_boundaries"]["underlying_source_RAR_sha256"], self.old_shops["source_original_mixed25_community_RAR_SHA256"])
        self.assertFalse(r["source_boundaries"]["original_RAR_binary_reopened_this_unit"])
        self.assertFalse(r["source_boundaries"]["original_RD_binary_redecoded_this_unit"])

    def test_exact_eight_original_create_parameter_source_relations(self):
        r = self.report["original_shop_records"]
        self.assertEqual(len(r), 8)
        actual = {(s["floor_id"], s["source_coordinate_raw"]) for s in r}
        self.assertEqual(len(actual), 8)
        old_args = {s["path"]: s for s in self.old_shops["shop_argument_rows"]}
        for s in r:
            self.assertIn(s["original_argument_path"], old_args)
            old = old_args[s["original_argument_path"]]
            self.assertEqual(s["original_argument_sha256"], old["source_sha256"])
            self.assertEqual(s["original_itemlist_expression_sha256"], old["raw_ItemList_expression_sha256"])
            self.assertEqual(s["source_item_ids_in_order"], old["expanded_candidate_IDs_not_proven_runtime"])
            self.assertFalse(old["range_expressions_literal"])
            creates = [x for x in self.old_shops["npcgen_shop_creation_rows"] if x["argument_path"] == s["original_argument_path"]]
            self.assertEqual(len(creates), 1)
            create = creates[0]
            self.assertEqual([s["source_create_path"], s["source_create_full_sha256"], s["floor_id"], s["source_coordinate_raw"]],
                             [create["create_path"], create["create_full_sha256"], create["source_floorid_raw"], create["source_location_raw"]])

    def test_village_and_profile_counts(self):
        shops = self.report["original_shop_records"]
        self.assertEqual({s["floor_id"] for s in shops}, {1001, 2001, 3001, 4001})
        self.assertEqual([s["source_numeric_item_count"] for s in shops], [17, 13, 16, 14, 16, 13, 18, 13])
        self.assertEqual(sum(s["source_numeric_item_count"] for s in shops), 120)
        self.assertEqual(sum(s["source_numeric_item_count"] for s in shops if s["research_bucket"] == "attack_profile"), 67)
        self.assertEqual(sum(s["source_numeric_item_count"] for s in shops if s["research_bucket"] == "defense_profile"), 53)
        self.assertEqual(len(self.item_records), 56)
        self.assertEqual(len({v["original_image_alias"] for v in self.item_records.values()}), 45)

    def test_original_row_identity_and_pixel_qualification(self):
        for id_, row in self.item_records.items():
            old = self.old_rows[id_]
            self.assertEqual(row["original_itemset_A_and_B_row_sha256"], old[1])
            self.assertEqual(old[1], old[2])
            self.assertEqual(row["original_image_alias"], old[3])
            self.assertEqual(old[3], old[4])
            self.assertEqual(row["raw_type"], old[6])
            self.assertEqual(row["raw_cost"], old[5])
            self.assertEqual(row["raw_level"], old[7])
            self.assertEqual([old[8], old[9]], ["REAL_RD_DECODED_CROSS_CARRIER"] * 2)

    def test_source_stat_pair_fidelity_and_negative_values(self):
        for row in self.item_records.values():
            six = row["original_six_fields_col37_to42"]
            self.assertEqual(len(six), 6)
            self.assertEqual(six[::2], six[1::2])
            self.assertTrue(all(type(v) is int for v in six))
        self.assertEqual(self.item_records[0]["original_six_fields_col37_to42"], [9, 9, -3, -3, -3, -3])
        self.assertEqual(self.item_records[1030]["original_six_fields_col37_to42"], [0, 0, 17, 17, -5, -5])

    def test_all_120_source_refs_have_original_rows(self):
        refs = [id_ for s in self.report["original_shop_records"] for id_ in s["source_item_ids_in_order"]]
        self.assertEqual(len(refs), 120)
        self.assertEqual(set(refs), set(self.item_records))
        for shop in self.report["original_shop_records"]:
            allowed = {0, 1, 2, 3, 18} if shop["research_bucket"] == "attack_profile" else {6, 7}
            for id_ in shop["source_item_ids_in_order"]:
                self.assertIn(int(self.item_records[id_]["raw_type"]), allowed)

    def test_bounded_unknowns_remain_unknown(self):
        b = self.report["bounds"]
        for key in ("same_historical_official_deployment_proven", "original_client_equipment_effect_execution_proven",
                    "retail_TW1_PNG_is_later_mixed25_native_selector_proven", "original_npc_shop_open_executed",
                    "original_proprietary_text_binary_art_published"):
            self.assertIs(b[key], False)
        self.assertEqual(b["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertIsNone(b["overall_percent"])


if __name__ == "__main__":
    unittest.main()
