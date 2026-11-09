"""INTEGRATION25: public, pinned original-source joins; no proprietary game content."""
import copy
import hashlib
import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research" / "recovered"
REPORT = SOURCE / "STONEAGE-INTEGRATION25-ORIGINAL-2009-MARKET-SEVEN-SHOPS-SOURCE-R1.json"
SHOP = SOURCE / "STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json"
MAP = SOURCE / "STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json"
ITEM2 = SOURCE / "item-module-01" / "STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json"
ITEM4 = SOURCE / "item-module-01" / "STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-04-R1.json"
PINS = {
    SHOP: "3bde3b7df43725f28cdac355823667a0ba87e9b1",
    MAP: "137580e7c25aadf3d679b6ebfb5080b79912cc4f",
    ITEM2: "b91bc8335db508998f4595144ce371979ea8c849",
    ITEM4: "14c7816054375863c91e474b58d2202f76e821c5",
}
EXPECTED = (
    (15, 468, 16053, "0328e59728a23572d04b9650b8fb8b0a4af40768232488c2d79648d87771a895", 501, False),
    (17, 471, 16207, "7041e514ec81e4ece7fc8a0cca80f22800f8659f06fb06b94273462b1e5b9119", 524, True),
    (23, 474, 16017, "5257854a8e101ea42ad9eb375c0b43a705c652183f97fed8448523e687a565e9", 588, True),
    (26, 477, 16018, "61481e003c909bb951e225c2d1d67c285ca8faadd039f25f569e4b875f8d3fca", 646, True),
    (29, 480, 16015, "a9c7c534e274c8aa3bade37f60438c2b762c5e9bb09ea9b3369317508e322732", 654, True),
    (34, 483, 16210, "f53bb5d22e9329dce8d224f7411d3c6d0baaa2f904421bb3ea379c480728be91", 580, True),
    (37, 486, 16065, "73b484a1af4fde6e3d71c2bffe1c26f9d49ef3d701196caaf3b04e8d652a00d2", 744, True),
)


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def source_json(path):
    raw = path.read_bytes()
    if git_blob_sha(raw) != PINS[path]:
        raise ValueError("source blob drift: " + path.name)
    return json.loads(raw)


def source_set():
    return source_json(SHOP), source_json(MAP), source_json(ITEM2), source_json(ITEM4)


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def audit(d, src):
    shops, maps, shard2, shard4 = src
    require(d["schema"] == "stoneage.integration25.seven_market_food_shop_original_source_join_r1", "schema")
    require(d["preserved_historical_CURRENT_Git_blob"] == "c89e0e33537990aa2132b47c40fef49a985a935c",
            "historic CURRENT immutable blob")
    require(d["upstream_exact_Git_blob_pins"] == {
        "ITEM01_shop_224_create_191": PINS[SHOP],
        "MAP09_691_source_qualified_floors": PINS[MAP],
        "ITEM01_derived_item_shard_02": PINS[ITEM2],
        "ITEM01_derived_item_shard_04": PINS[ITEM4],
    }, "exact parent hashes")
    custody = d["private_original_source_custody"]
    require(custody["CHAR01_ZIP_bytes"] == 995176 and
            custody["CHAR01_ZIP_SHA256"] == "c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f" and
            custody["CHAR01_original_zip_CRC_verified_member_count"] == 2205, "original CHAR01 custody")
    require(custody["ITEM01_private_original_two_tables_and_832_RD_ZIP_bytes"] == 5868386 and
            custody["ITEM01_private_zip_SHA256"] == "cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa" and
            custody["ITEM01_private_ZIP_CRC_verified_member_count"] == 838, "original ITEM01 custody")
    require(custody["original_CREATE_shop_m_bytes"] == 20491 and
            custody["original_CREATE_shop_m_sha256"] == "d540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b", "original source CREATE")
    require(custody["original_7_CP950_shop_parameter_files_re_read_and_SHA_matched"] is True and
            custody["full_parent_RAR_re_read_this_unit"] is False and
            custody["original_DAT_and_TW1_RD_raw_bytes_re_read_this_unit"] is False, "source reread scope")
    verified_map = maps["maps"]["2009"]
    mp = d["prior_MAP09_floor_2009_source_only"]
    require(mp["floor"] == 2009 and mp["original_DAT_bytes"] == verified_map["source_bytes"] == 14408 and
            mp["original_DAT_sha256"] == verified_map["source_sha256"] ==
            "04b1bc0a1c6d25cedb6b22bb7fdc55771e7098172e03d2f336f3ea0d69cd0768" and
            mp["original_map_geometry"] == verified_map["geometry"] == [40, 60] and
            mp["candidate_combined_RGBA_pixel_sha256_from_prior_MAP09"] ==
            verified_map["frame_RGBA_sha256"]["combined"], "original scene map provenance")
    require(mp["original_DAT_independently_replayed_in_this_work_unit"] is False and
            mp["original_game_native_scene_not_executed"] is True, "don't invent new scene execution")
    creations = [c for c in shops["npcgen_shop_creation_rows"] if c["source_floorid_raw"] == 2009]
    mission = [c for c in creations if c["create_path"] == "genout/mission.create"]
    require(len(mission) == 2 and len([c for c in creations if c["create_path"] == "genout/shop_m.create"]) == 7,
            "independent mission nodes vs market store nodes")
    mission_report = d["mission_CREATEs_on_same_floor_excluded_from_market_count"]
    require(len(mission_report) == 2 and {(x["path"], x["argument_sha256"]) for x in mission_report} ==
            {(x["argument_path"], x["argument_sha256"]) for x in mission} and
            all(x["not_one_of_seven_shop_m_CREATEs"] is True for x in mission_report),
            "mission nodes not market shops")
    original = d["seven_original_market_shop_CREATEs_and_source_arguments"]
    require(len(original) == len(EXPECTED), "seven shops exactly")
    appearances = defaultdict(list)
    total_explicit = total_ranges = total_interval = 0
    for r, (suffix, line, graphic, file_sha, nbytes, type_present) in zip(original, EXPECTED):
        path = f"genout/ss_2009_27_{suffix}"
        c = [v for v in creations if v["create_path"] == "genout/shop_m.create" and v["argument_path"] == path]
        a = [v for v in shops["shop_argument_rows"] if v["path"] == path]
        require(len(c) == len(a) == 1, "unique original CREATE and argument")
        c, a = c[0], a[0]
        require(c["argument_sha256"] == a["source_sha256"] == r["original_argument_file_SHA256"] == file_sha,
                "original parameter SHA")
        require(c["create_full_sha256"] == r["original_CREATE_file_sha256"] ==
                custody["original_CREATE_shop_m_sha256"], "source CREATE SHA")
        require(r["source_line_marker"] == line and r["original_floor"] == 2009 and
                r["original_argument_bytes"] == nbytes and r["original_argument_path"] == path,
                "original physical source identity")
        require(r["original_graphicname_number"] == graphic and r["original_dir_number"] == 6 and
                r["original_borncorner_numeric"] == [27, suffix, 27, suffix] and
                c["source_location_raw"] == f"27,{suffix},27,{suffix}", "original position and graphic")
        require(r["original_argument_ItemList_expression_SHA256_from_prior_ITEM01"] ==
                a["raw_ItemList_expression_sha256"], "original literal expression SHA")
        require(r["source_buy_rate_literal"] == a["source_buy_rate_text"] ==
                ("4.0" if suffix == 37 else "1.0") and
                r["source_sell_rate_literal"] == a["source_sell_rate_text"] == "0.5" and
                r["source_special_rate_literal"] == "1.5", "original numeric strings, not prices")
        require(r["source_LimitItemType_key_present"] is type_present and
                r["source_LimitItemType_literal_if_present"] == ("" if type_present else None), "missing != empty")
        require(r["original_argument_ItemList_explicit_IDs_count"] ==
                a["explicit_numeric_item_ID_count"] and
                r["original_argument_ItemList_range_tokens_count"] ==
                len(a["range_expressions_literal"]) and
                r["qualified_original_map_floor_lookup"] == 2009 and
                r["source_native_shop_transaction_verified"] is False, "range/scene/native gates")
        tokens = r["original_argument_ItemList_literal_tokens"]
        require(len(tokens) == r["original_argument_ItemList_explicit_IDs_count"] +
                r["original_argument_ItemList_range_tokens_count"], "token count")
        expanded = []
        for i, token in enumerate(tokens):
            require(token["ordinal"] == i, "token order")
            if token["kind"] == "EXPLICIT_SINGLE_ID_LITERAL":
                require(suffix == 37 and "id" in token, "literal isolated")
                expanded.append((token["id"], "EXPLICIT_SINGLE_ID_LITERAL", i))
                total_explicit += 1
            else:
                require(token["kind"] == "INCLUSIVE_INTERVAL_CANDIDATE_ONLY" and suffix != 37, "range cannot be listed")
                lo, hi = token["start"], token["end"]
                require(lo <= hi and token["source_literal"] == f"{lo}-{hi}" and
                        [lo, hi] == a["range_expressions_literal"][i], "source literal interval")
                expanded.extend((v, "INCLUSIVE_INTERVAL_CANDIDATE_ONLY", i) for v in range(lo, hi + 1))
                total_interval += hi - lo + 1
                total_ranges += 1
        require([v[0] for v in expanded] == a["expanded_candidate_IDs_not_proven_runtime"] and
                len(expanded) == r["candidate_expansion_count_from_literal_intervals_not_native_verified"],
                "source text range->candidate reconstruction")
        for i, (item, kind, token_i) in enumerate(expanded):
            appearances[item].append({"shop_suffix": suffix, "ordinal_within_shop": i,
                                      "source_kind": kind, "source_token_ordinal": token_i})
    rows = {r[0]: r for r in shard2["rows"] + shard4["rows"]}
    require(set(rows).issuperset(appearances), "all original item definitions available")
    joint = d["exact_source_derived_item_union_candidate_or_literal"]
    require([r["original_item_id"] for r in joint] == sorted(appearances), "no inferred or omitted IDs")
    q = missing = 0
    known_aliases = set()
    missing_aliases = set()
    all_aliases = set()
    for item in joint:
        id_ = item["original_item_id"]
        ref = rows[id_]
        require(ref[1] and ref[1] == ref[2] == item["original_mixed25_two_tables_full_row_SHA256"] and
                ref[3] == ref[4] == item["TW1_different_carrier_candidate_image_alias"] and
                ref[10] == [], "both full original row SHA; same source image field")
        require(ref[5] == item["original_mixed25_source_price_literal"] and
                ref[6] == item["original_mixed25_source_type_literal"] and
                ref[7] == item["original_mixed25_source_level_literal"], "source item fields")
        require(item["occurrences_from_source_ItemList"] == appearances[id_], "exact source token relationships")
        require(ref[9] == item["TW1_original_RD_qualification"] and
                item["source_native_item_use_verified"] is False and
                item["official_same_deployment_with_TW1_image_proven"] is False, "retail namespace gates")
        all_aliases.add(ref[4])
        if ref[9] == "REAL_RD_DECODED_CROSS_CARRIER":
            q += 1
            known_aliases.add(ref[4])
        elif ref[9] == "TW1_INDEX_NOT_FOUND":
            missing += 1
            missing_aliases.add(ref[4])
        else:
            raise ValueError("unexpected image qualification")
    occurrence_sum = sum(map(len, appearances.values()))
    metrics = d["metrics"]
    expected_metrics = {
        "seven_original_shop_m_CREATEs": 7,
        "other_original_mission_CREATE_references_floor_2009_excluded": 2,
        "source_qualified_2009_MAP09_floors": 1,
        "original_literally_explicit_ItemList_ID_mentions": total_explicit,
        "original_interval_expression_tokens": total_ranges,
        "number_of_closed_interval_candidate_expansions_not_native_verified": total_interval,
        "total_explicit_plus_interval_candidate_item_occurrences": occurrence_sum,
        "different_item_IDs_in_source_derived_union": len(appearances),
        "duplicate_occurrences_across_separate_stores_kept": occurrence_sum - len(appearances),
        "original_two_itemset_rows_with_matching_SHA": len(joint),
        "distinct_numeric_TW1_image_aliases_all": len(all_aliases),
        "source_qualified_TW1_retail_RD_item_IDs": q,
        "source_qualified_TW1_retail_RD_aliases_distinct": len(known_aliases),
        "TW1_retail_index_not_found_item_IDs": missing,
        "TW1_retail_index_not_found_aliases_distinct": len(missing_aliases),
        "original_same_deployment_verified_item_IDs": 0,
        "native_sale_or_item_use_executed": 0,
        "new_actual_original_map_RD_pixel_decodes_in_this_unit": 0,
    }
    require(metrics == expected_metrics, "metrics from true source projections")
    require((total_explicit, total_ranges, total_interval, occurrence_sum, len(appearances),
             q, missing, len(known_aliases), len(missing_aliases)) ==
            (33, 37, 149, 182, 181, 169, 12, 88, 3), "known independent private replay")
    require(appearances[12221][0]["source_kind"] == "INCLUSIVE_INTERVAL_CANDIDATE_ONLY" and
            appearances[12221][1]["source_kind"] == "EXPLICIT_SINGLE_ID_LITERAL",
            "do not collapse mixed-certainty repeated original item")
    b = d["boundaries"]
    require(all(b[k] is True for k in (
        "closed_interval_candidate_IDs_not_native_proven_as_shop_items",
        "original_explicit_33_never_mixed_with_interval_149_as_equal_certainty",
        "source_LimitItemNo_intervals_not_promoted_to_actual_native_stocks",
        "original_NPC_buy_rate_4_0_only_literal_not_executed_price",
        "TW1_source_art_not_same_official_deployment_with_mixed25_proven",
    )), "must keep evidence boundaries")
    require(all(b[k] is False for k in (
        "original_native_item_use_and_shop_transaction_executed",
        "full_original_MAP09_2009_pixel_replay_this_unit",
        "original_game_client_executed",
        "original_npc_scripts_or_art_published_to_Git",
    )), "no false native execution claims")
    require(d["Stage_A"] == "7_PARTIAL_2_OPEN" and d["Stage_B_wiki"] == "GATED" and
            d["R79"] == "PAUSED_NON_BLOCKING" and d["overall_percent"] is None,
            "Stage A is not overall completion")


class TestMarketSourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.src = source_set()

    def test_complete_positive_join(self):
        audit(self.doc, self.src)

    def test_range_37_expands_only_candidate_149(self):
        m = self.doc["metrics"]
        self.assertEqual((m["original_literally_explicit_ItemList_ID_mentions"],
                          m["original_interval_expression_tokens"],
                          m["number_of_closed_interval_candidate_expansions_not_native_verified"]), (33, 37, 149))

    def test_custody_and_parent_source_pins(self):
        self.assertEqual(self.doc["private_original_source_custody"]["CHAR01_original_zip_CRC_verified_member_count"], 2205)
        self.assertEqual(self.doc["upstream_exact_Git_blob_pins"]["ITEM01_derived_item_shard_04"], PINS[ITEM4])

    def test_12221_same_item_different_evidence_class(self):
        found = next(x for x in self.doc["exact_source_derived_item_union_candidate_or_literal"]
                     if x["original_item_id"] == 12221)
        self.assertEqual(len(found["occurrences_from_source_ItemList"]), 2)
        self.assertNotEqual(found["occurrences_from_source_ItemList"][0]["source_kind"],
                            found["occurrences_from_source_ItemList"][1]["source_kind"])

    def test_forged_original_parameter_SHA_rejected(self):
        d = copy.deepcopy(self.doc)
        d["seven_original_market_shop_CREATEs_and_source_arguments"][0]["original_argument_file_SHA256"] = "0"*64
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_forged_explicit_list_out_of_range_rejected(self):
        d = copy.deepcopy(self.doc)
        d["seven_original_market_shop_CREATEs_and_source_arguments"][-1]["original_argument_ItemList_literal_tokens"][0]["id"] = 123456
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_forged_2009_map_SHA_rejected(self):
        d = copy.deepcopy(self.doc)
        d["prior_MAP09_floor_2009_source_only"]["original_DAT_sha256"] = "0"*64
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_forged_original_item_line_SHA_rejected(self):
        d = copy.deepcopy(self.doc)
        d["exact_source_derived_item_union_candidate_or_literal"][0]["original_mixed25_two_tables_full_row_SHA256"] = "0"*64
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_fake_TW1_missing_RD_promoted_rejected(self):
        d = copy.deepcopy(self.doc)
        target = next(x for x in d["exact_source_derived_item_union_candidate_or_literal"] if x["original_item_id"] == 12229)
        target["TW1_original_RD_qualification"] = "REAL_RD_DECODED_CROSS_CARRIER"
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_fake_native_trade_rejected(self):
        d = copy.deepcopy(self.doc)
        d["metrics"]["native_sale_or_item_use_executed"] = 1
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_fake_original_runtime_image_deployment_rejected(self):
        d = copy.deepcopy(self.doc)
        d["exact_source_derived_item_union_candidate_or_literal"][0]["official_same_deployment_with_TW1_image_proven"] = True
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_fake_mission_shop_promotion_rejected(self):
        d = copy.deepcopy(self.doc)
        d["mission_CREATEs_on_same_floor_excluded_from_market_count"][0]["not_one_of_seven_shop_m_CREATEs"] = False
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_false_rerender_or_filled_51_slots_rejected(self):
        d = copy.deepcopy(self.doc)
        d["prior_MAP09_floor_2009_source_only"]["original_DAT_independently_replayed_in_this_work_unit"] = True
        with self.assertRaises(ValueError):
            audit(d, self.src)

    def test_missing_vs_empty_item_limit_type_distinction(self):
        s = self.doc["seven_original_market_shop_CREATEs_and_source_arguments"]
        self.assertIsNone(s[0]["source_LimitItemType_literal_if_present"])
        self.assertEqual(s[1]["source_LimitItemType_literal_if_present"], "")
        d = copy.deepcopy(self.doc)
        d["seven_original_market_shop_CREATEs_and_source_arguments"][0]["source_LimitItemType_key_present"] = True
        with self.assertRaises(ValueError):
            audit(d, self.src)


if __name__ == "__main__":
    unittest.main()
