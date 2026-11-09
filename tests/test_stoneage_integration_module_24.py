"""INTEGRATION24: source-only positive/negative guards. No original proprietary assets."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "recovered" / "STONEAGE-INTEGRATION24-FIVE-VILLAGE-MEDICINE-SHOPS-SOURCE-R1.json"
SHOP = ROOT / "research" / "recovered" / "STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json"
MAP = ROOT / "research" / "recovered" / "STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json"
ITEM = ROOT / "research" / "recovered" / "item-module-01" / "STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-01-R1.json"
PINS = {
    SHOP: "3bde3b7df43725f28cdac355823667a0ba87e9b1",
    MAP: "137580e7c25aadf3d679b6ebfb5080b79912cc4f",
    ITEM: "d39ef58c88f1326d227b2844ca06ed5e23e2965a",
}
FLOORS = (1005, 1105, 1205, 1305, 1405)
ITEM_IDS = (1500, 1501, 1510, 1511, 1512, 1530, 1531, 1540, 1541, 1542, 1543, 1545)
CREATE_LINES = (47, 157, 211, 265, 310)
GRAPHICS = (16023, 16059, 16059, 16059, 16023)
DIRS = (4, 6, 6, 6, 4)
BUY_RATES = ("1.0", "1.1", "1.5", "1.3", "1.4")
ARG_LENGTHS = (506, 544, 522, 558, 522)
EXPECTED_ITEMLIST_SHA = "cf24c4d42fcb288f758c7e2eb10502832a96656513f498c1302b4889d55f182b"
CREATE_SHA = "d540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b"


def sha_git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sources():
    for path, expected in PINS.items():
        if sha_git_blob(path.read_bytes()) != expected:
            raise ValueError("source Git blob changed: " + path.name)
    return load(SHOP), load(MAP), load(ITEM)


def verify(d, src):
    shop, maps, items = src
    require = lambda cond, message: None if cond else (_ for _ in ()).throw(ValueError(message))
    require(d["schema"] == "stoneage.integration24.five_original_medicine_shop_source_only.r1", "schema")
    require(d["preserved_CURRENT_original_blob"] == "c89e0e33537990aa2132b47c40fef49a985a935c", "historical CURRENT")
    require(d["prior_public_Git_blobs"] == {
        "shop_creation_and_parameters": PINS[SHOP],
        "MAP09_source_ready_original_DAT": PINS[MAP],
        "ITEM01_source_itemset_rows": PINS[ITEM],
    }, "source parent pins")
    custody = d["original_private_member_verification"]
    require(custody["CHAR01_original_2205_NPC_files_zip_sha256"] ==
            "c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f", "CHAR01 provenance")
    require(custody["ITEM01_private_838_members_zip_sha256"] ==
            "cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa", "ITEM01 provenance")
    require(custody["original_shop_m_CREATE_20491_bytes_sha256"] == CREATE_SHA, "original CREATE file")
    require(custody["parent_full_RAR_rechecked_this_unit"] is False, "false new RAR check")
    require(custody["original_MAP09_DAT_raw_re_read_this_unit"] is False, "false DAT replay")
    rooms = d["source_qualified_five_rooms"]
    require(len(rooms) == 5 and [r["floor"] for r in rooms] == list(FLOORS), "five rooms")
    expected_paths = set()
    for i, (floor, r) in enumerate(zip(FLOORS, rooms)):
        c = next((x for x in shop["npcgen_shop_creation_rows"]
                  if x["source_floorid_raw"] == floor and x["create_path"] == "genout/shop_m.create"
                  and x["argument_path"] == r["original_CREATE_enemy_parameter_path"]), None)
        require(c is not None, "CREATE must reference original argument")
        a = next((x for x in shop["shop_argument_rows"] if x["path"] == c["argument_path"]), None)
        require(a is not None, "source argument missing")
        require(c["create_full_sha256"] == CREATE_SHA and
                r["original_CREATE_source_file_sha256"] == c["create_full_sha256"] and
                r["original_CREATE_source_path"] == c["create_path"], "original CREATE source")
        require(r["original_CREATE_borncorner_literal"] == c["source_location_raw"], "original location")
        require(r["original_CREATE_gen_line"] == CREATE_LINES[i], "source line")
        require(r["original_CREATE_graphicname_numeric"] == GRAPHICS[i], "graphic source")
        require(r["original_CREATE_dir_numeric"] == DIRS[i], "direction source")
        require(r["original_argument_source_sha256"] == c["argument_sha256"] == a["source_sha256"], "argument SHA")
        require(r["original_argument_file_bytes"] == ARG_LENGTHS[i], "argument byte count")
        require(r["original_ItemList_literal_SHA256"] == a["raw_ItemList_expression_sha256"] == EXPECTED_ITEMLIST_SHA,
                "literal original ItemList SHA")
        require(r["original_ItemList_explicit_IDs"] == list(ITEM_IDS) ==
                a["expanded_candidate_IDs_not_proven_runtime"], "literal ItemList position sequence")
        require(a["range_expressions_literal"] == [] and
                a["explicit_numeric_item_ID_count"] == len(ITEM_IDS) ==
                r["original_ItemList_explicit_count"], "explicit stock vs range")
        require(r["original_buy_rate_literal"] == a["source_buy_rate_text"] == BUY_RATES[i] and
                r["original_sell_rate_literal"] == a["source_sell_rate_text"] == "0.2",
                "source literal rates")
        require(r["original_special_rate_literal"] == "1.5" and
                r["original_LimitItemType_literal"] == "" and
                r["original_LimitItemNo_literal_range"] == "1500-1550", "source limit fields")
        m = maps["maps"].get(str(floor))
        require(m is not None and m["source_bytes"] == 5408 and m["geometry"] == [30, 30], "prior MAP09")
        p = r["qualified_original_DAT_floor_from_prior_MAP09"]
        require(p["source_SHA256"] == m["source_sha256"] and p["source_bytes"] == m["source_bytes"]
                and p["geometry"] == m["geometry"] and
                p["prior_full_combined_candidate_RGBA_SHA256"] == m["frame_RGBA_sha256"]["combined"], "prior DAT SHA")
        require(p["verified_in_prior_MAP09"] is True and
                p["raw_DAT_independently_replayed_this_unit"] is False, "no new DAT claim")
        require(r["native_shop_transaction_verified"] is False and
                r["native_NPC_dialogue_verified"] is False and
                r["native_inventory_price_application_verified"] is False, "cannot claim native runtime")
        expected_paths.add(c["argument_path"])
    require(len(expected_paths) == len(FLOORS), "five distinct original parameter paths")
    records = d["original_same_carrier_itemset_rows_and_separate_retail_RD_candidates"]
    require(len(records) == len(ITEM_IDS) and
            [x["original_item_id"] for x in records] == list(ITEM_IDS), "original item ID positions")
    indexed = {r[0]: r for r in items["rows"]}
    for row in records:
        a = indexed[row["original_item_id"]]
        require(a[1] == a[2] == row["original_itemset_complete_row_SHA256"] ==
                row["original_itemset0710_complete_row_SHA256"], "two original itemsets exact line SHA")
        require(str(row["source_itemset_raw_cost_literal"]) == str(a[5]) and
                row["source_itemset_raw_type_literal"] == a[6], "raw original cost/type")
        require(row["TW10_original_RD_candidate_numeric_alias"] == a[4] and
                row["TW10_RD_qualification"] == a[9] == "REAL_RD_DECODED_CROSS_CARRIER",
                "TW10 alias is source-bounded")
        require(row["runtime_item_effect_executed"] is False and
                row["original_same_deployment_artwork_selection_proven"] is False, "no runtime/cross-version promotion")
    m = d["metrics"]
    require((m["distinct_NPC_create_nodes"], m["original_pharmacy_room_floors"],
             m["source_parameter_files"], m["each_12_literally_listed_IDs"],
             m["explicit_original_ItemList_mention_positions"],
             m["different_original_IDs"], m["source_original_itemset_rows_that_match_both_tables"],
             m["cross_carrier_original_retail_RD_numeric_aliases_distinct"],
             m["source_LimitItemNo_literal_range_candidates_not_listed_as_actual_stock"],
             m["source_buy_rate_variants_distinct"]) ==
            (5, 5, 5, 12, 60, 12, 12, 11, 39, 5), "derived metrics")
    require(m["new_original_DAT_or_RD_pixels_decoded_this_unit"] == 0 and
            m["native_trades_executed"] == 0, "native/graphics execution")
    b = d["bounds"]
    require(all(b[k] is True for k in
                ("cannot_infer_actual_native_buy_price_from_rate_literals",
                 "cannot_turn_LimitItemNo_range_into_51_listed_IDs",
                 "original_runtime_shop_inventory_selected_from_different_carrier_not_proven",
                 "official_TW10_or_JSS1999_same_deployment_NOT_proven",
                 "all_MAP09_canvas_fingerprints_inherited_not_replayed_now")), "boundary guards")
    require(b["original_client_or_MMO_server_executed"] is False and
            b["original_proprietary_source_assets_committed_to_Git"] is False, "source safety")
    require(d["Stage_A"] == "7_PARTIAL_2_OPEN" and d["Stage_B_wiki"] == "GATED" and
            d["R79"] == "PAUSED_NON_BLOCKING" and d["overall_percent"] is None, "stage gates")


class MedicineSourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load(OUT)
        cls.src = sources()

    def test_positive_full_source_join(self):
        verify(self.d, self.src)

    def test_five_independent_shop_arguments(self):
        self.assertEqual(len({r["original_argument_source_sha256"] for r in
                              self.d["source_qualified_five_rooms"]}), 5)

    def test_economics_literals_are_not_execution(self):
        self.assertEqual([r["original_buy_rate_literal"] for r in
                          self.d["source_qualified_five_rooms"]], list(BUY_RATES))
        self.assertTrue(all(not r["native_inventory_price_application_verified"]
                            for r in self.d["source_qualified_five_rooms"]))

    def test_1530_1531_same_illustration_different_items(self):
        x = {r["original_item_id"]: r for r in
             self.d["original_same_carrier_itemset_rows_and_separate_retail_RD_candidates"]}
        self.assertEqual(x[1530]["TW10_original_RD_candidate_numeric_alias"],
                         x[1531]["TW10_original_RD_candidate_numeric_alias"])
        self.assertNotEqual(x[1530]["original_itemset_complete_row_SHA256"],
                            x[1531]["original_itemset_complete_row_SHA256"])

    def test_fake_extra_51_itemlist_rejected(self):
        d = copy.deepcopy(self.d)
        d["source_qualified_five_rooms"][0]["original_ItemList_explicit_IDs"] = list(range(1500, 1551))
        with self.assertRaises(ValueError):
            verify(d, self.src)

    def test_fake_native_price_executed_rejected(self):
        d = copy.deepcopy(self.d)
        d["source_qualified_five_rooms"][1]["native_inventory_price_application_verified"] = True
        with self.assertRaises(ValueError):
            verify(d, self.src)

    def test_fake_early_official_deployment_rejected(self):
        d = copy.deepcopy(self.d)
        d["bounds"]["official_TW10_or_JSS1999_same_deployment_NOT_proven"] = False
        with self.assertRaises(ValueError):
            verify(d, self.src)

    def test_forged_original_argument_sha_rejected(self):
        d = copy.deepcopy(self.d)
        d["source_qualified_five_rooms"][2]["original_argument_source_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            verify(d, self.src)

    def test_forged_original_DAT_sha_rejected(self):
        d = copy.deepcopy(self.d)
        d["source_qualified_five_rooms"][3]["qualified_original_DAT_floor_from_prior_MAP09"]["source_SHA256"] = "0" * 64
        with self.assertRaises(ValueError):
            verify(d, self.src)

    def test_false_itemset_row_join_rejected(self):
        d = copy.deepcopy(self.d)
        d["original_same_carrier_itemset_rows_and_separate_retail_RD_candidates"][0]["original_itemset0710_complete_row_SHA256"] = "0" * 64
        with self.assertRaises(ValueError):
            verify(d, self.src)

    def test_false_TW10_item_artwork_deployment_rejected(self):
        d = copy.deepcopy(self.d)
        d["original_same_carrier_itemset_rows_and_separate_retail_RD_candidates"][0]["original_same_deployment_artwork_selection_proven"] = True
        with self.assertRaises(ValueError):
            verify(d, self.src)

    def test_false_new_DAT_replay_rejected(self):
        d = copy.deepcopy(self.d)
        d["source_qualified_five_rooms"][0]["qualified_original_DAT_floor_from_prior_MAP09"]["raw_DAT_independently_replayed_this_unit"] = True
        with self.assertRaises(ValueError):
            verify(d, self.src)


if __name__ == "__main__":
    unittest.main()
