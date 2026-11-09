"""INTEGRATION26: source-only recovery of 12 TW10-unindexed market item images via preserved mixed25 RD."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"
REPORT = ROOT / "STONEAGE-INTEGRATION26-MARKET-12-MIXED25-ORIGINAL-PIXEL-BRIDGE-R1.json"
MARKET = ROOT / "STONEAGE-INTEGRATION25-ORIGINAL-2009-MARKET-SEVEN-SHOPS-SOURCE-R1.json"
ITEM06 = ROOT / "STONEAGE-ITEM06-MIXED25-MISSING-TW1-ITEM-ALIAS-PIXELS-R1.json"
PINS = {
    MARKET: "24fea2402176d80738267c286e94ae3298084db3",
    ITEM06: "989361a944b874e49a19c33846c6d49c2f0ca5be",
}
PNG = {
    24552: ("ffcd24fbf6bafd4042b4983cb5ae650813dc9bea40ade242e9d4bac920d08acc", (32, 33), 1352, (12226, 12227, 12228, 12229)),
    24553: ("d063b00dc3cf088ec94fd7f741457cbe723889ca44aebded27d89c9d504a0223", (32, 28), 1204, (12218, 12219, 12220, 12221)),
    24560: ("783f5ed58b050fb278efa141a748b4107b68e27dcb180b3320c05fb0feade7ac", (36, 36), 1322, (12222, 12223, 12224, 12225)),
}


def source(path):
    raw = path.read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
    if sha != PINS[path]:
        raise ValueError("source blob drift")
    return json.loads(raw)


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def verify(r, market, item06):
    require(r["schema"] == "stoneage.integration26.market_original_mixed25_missing_tw10_pixel_source_bridge.r1", "schema")
    require(r["preserved_unchanged_CURRENT_blob"] ==
            "c89e0e33537990aa2132b47c40fef49a985a935c", "historical current")
    require(r["upstream_public_Git_blobs"] ==
            {"market": PINS[MARKET], "ITEM06": PINS[ITEM06]}, "immutable parent blobs")
    p = r["original_private_source_custody"]
    require(p["private_HTML_bytes"] == item06["private_html"]["bytes"] == 1242805 and
            p["private_HTML_SHA256"] == item06["private_html"]["sha256"] ==
            "ff901220af1484a3367ef52014fe561b25bd6ee9d270b4b6d3fb220ff1f8a700", "private real PNG custodian")
    require(p["ITEM06_original_ADRN_SHA256"] == item06["original_members"]["adrn_15.bin"][1] and
            p["ITEM06_original_REAL_SHA256"] == item06["original_members"]["real_15.bin"][1] and
            p["ITEM06_original_Palet_1_SHA256"] == item06["original_members"]["Palet_1.sap"][1],
            "original mixed25 parent source identity")
    require(p["private_HTML_whole_sha256_reverified_this_turn"] is True and
            p["private_stored_three_PNG_full_sha256_and_PNG_header_dimensions_reverified_this_turn"] is True and
            p["parent_original_RAR_re_read_this_turn"] is False and
            p["original_ADRN_REAL_re_read_this_turn"] is False and
            p["original_RD_redecoded_this_turn"] is False and
            p["original_commercial_images_or_HTML_published_to_Git"] is False,
            "local pixel re-read, no fake native decode")
    original = market["exact_source_derived_item_union_candidate_or_literal"]
    missing = [x for x in original if x["TW1_original_RD_qualification"] == "TW1_INDEX_NOT_FOUND"]
    require(len(original) == 181 and len(missing) == 12, "market source scope retained")
    source_imgs = {x["alias"]: x for x in item06["aliases"] if x["alias"] in PNG}
    imgs = r["same_later_mixed25_source_qualified_three_RD_aliases"]
    require(len(source_imgs) == 3 and len(imgs) == 3 and {x["alias"] for x in imgs} == set(PNG),
            "exact 3 source alias entries")
    for x in imgs:
        i = source_imgs[x["alias"]]
        hash_, (width, height), png_bytes, ids = PNG[x["alias"]]
        require(i["status"] == x["source_status"] == "strict" and
                i["width"] == x["width"] == width and i["height"] == x["height"] == height and
                i["private_png_sha256"] == x["private_original_source_qualified_PNG_SHA256"] == hash_ and
                x["private_PNG_exact_bytes_read_now"] == png_bytes, "verified PNG source bytes")
        require(i["index"] == x["original_ADRN_index"] and i["bitmap"] == x["source_bitmap"] and
                i["record_sha256"] == x["record_SHA256"] and
                i["rd_sha256"] == x["original_RD_SHA256"] and
                i["indices_sha256"] == x["original_indices_SHA256"], "exact original RD/ADRN")
        require(tuple(x["covered_item_IDs"]) == ids and sorted(i["shop_item_ids"]) == list(ids),
                "original itemset->pixel alias ID mapping")
        require(x["original_RD_raw_bytes_redecoded_this_turn"] is False and
                x["native_runtime_image_selector_proven"] is False, "cannot promote static image")
    expected = {x["original_item_id"]: x for x in missing}
    linked = r["source_bound_twelve_item_IDs"]
    require([x["id"] for x in linked] == [x["original_item_id"] for x in missing], "ordered missing item group")
    for x in linked:
        original_item = expected[x["id"]]
        source_pixel = source_imgs[x["itemset_ImageNumber"]]
        require(x["mixed25_original_two_itemsets_full_line_SHA256"] ==
                original_item["original_mixed25_two_tables_full_row_SHA256"] and
                x["itemset_ImageNumber"] == original_item["TW1_different_carrier_candidate_image_alias"],
                "two original itemset line sha/alias")
        require(x["mixed25_original_RD_blob_SHA256"] == source_pixel["rd_sha256"] and
                x["market_source_occurrences"] == original_item["occurrences_from_source_ItemList"] and
                x["original_market_floor"] == 2009 and
                x["TW10_original_RD_index_absent"] is True and
                x["source_same_later_mixed25_image_candidate"] is True and
                x["original_native_selection_or_actual_sale_proven"] is False,
                "source-only join, keep original TW10 negative")
    n = sum(len(x["market_source_occurrences"]) for x in linked)
    require(n == 13, "keep duplicated 12221")
    m = r["metrics"]
    require(m == {
        "market_distinct_original_item_IDs": 181,
        "TW10_retail_original_RD_candidates_qualified_for_market_item_IDs": 169,
        "TW10_retail_original_RD_index_missing_market_item_IDs": 12,
        "late_mixed25_original_RD_qualified_for_those_12_IDs": 12,
        "late_mixed25_distinct_RD_aliases": 3,
        "source_qualified_original_pixel_candidates_across_TWO_distinct_source_scopes_for_market_item_IDs": 181,
        "source_ItemList_occurrences_for_12_late_mixed25_source_qualified_items": 13,
        "private_previously_qualified_PNGs_actually_read_and_SHA_reverified": 3,
        "new_original_RD_raw_decodes_this_turn": 0,
        "native_market_trade_execution_this_turn": 0,
    }, "complete derived coverage 169+12; no original new pixel decoding")
    require(all(r["boundaries"][key] is True for key in
               ("TW10_missing_RD_index_preserved",
                "mixed25_original_static_pixel_identity_source_qualified_not_native_selection",
                "no_official_same_deployment_of_client_and_server_claim",
                "no_original_game_client_execution",
                "source_Palet_1_candidate_not_native_palette_choice",
                "original_assets_private")), "evidence boundary")
    require(r["Stage_A"] == "7_PARTIAL_2_OPEN" and r["Stage_B_wiki"] == "GATED" and
            r["R79"] == "PAUSED_NON_BLOCKING" and r["overall_percent"] is None, "stage gate")


class OriginalMixed25MarketPixelBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.market = source(MARKET)
        cls.pix = source(ITEM06)

    def test_source_link(self):
        verify(self.report, self.market, self.pix)

    def test_image_three_original_hashes_match_upstream(self):
        for row in self.report["same_later_mixed25_source_qualified_three_RD_aliases"]:
            self.assertEqual(row["private_original_source_qualified_PNG_SHA256"], PNG[row["alias"]][0])

    def test_twelve_items_are_TW10_negative_not_deleted(self):
        self.assertEqual([x["id"] for x in self.report["source_bound_twelve_item_IDs"]],
                         list(range(12218, 12230)))

    def test_invented_original_rd_redecode_rejected(self):
        a = copy.deepcopy(self.report)
        a["original_private_source_custody"]["original_RD_redecoded_this_turn"] = True
        with self.assertRaises(ValueError):
            verify(a, self.market, self.pix)

    def test_original_TW10_gap_false_promotion_rejected(self):
        a = copy.deepcopy(self.report)
        a["source_bound_twelve_item_IDs"][0]["TW10_original_RD_index_absent"] = False
        with self.assertRaises(ValueError):
            verify(a, self.market, self.pix)

    def test_original_image_SHA_forgery_rejected(self):
        a = copy.deepcopy(self.report)
        a["same_later_mixed25_source_qualified_three_RD_aliases"][0]["original_RD_SHA256"] = "0"*64
        with self.assertRaises(ValueError):
            verify(a, self.market, self.pix)

    def test_original_PNG_SHA_forgery_rejected(self):
        a = copy.deepcopy(self.report)
        a["same_later_mixed25_source_qualified_three_RD_aliases"][1]["private_original_source_qualified_PNG_SHA256"] = "0"*64
        with self.assertRaises(ValueError):
            verify(a, self.market, self.pix)

    def test_double_occurrence_12221_must_remain_rejected(self):
        a = copy.deepcopy(self.report)
        row = next(x for x in a["source_bound_twelve_item_IDs"] if x["id"] == 12221)
        row["market_source_occurrences"] = row["market_source_occurrences"][:1]
        with self.assertRaises(ValueError):
            verify(a, self.market, self.pix)

    def test_runtime_shop_selector_unsupported_rejected(self):
        a = copy.deepcopy(self.report)
        a["same_later_mixed25_source_qualified_three_RD_aliases"][2]["native_runtime_image_selector_proven"] = True
        with self.assertRaises(ValueError):
            verify(a, self.market, self.pix)

    def test_forged_same_source_itemset_SHA_rejected(self):
        a = copy.deepcopy(self.report)
        a["source_bound_twelve_item_IDs"][3]["mixed25_original_two_itemsets_full_line_SHA256"] = "0"*64
        with self.assertRaises(ValueError):
            verify(a, self.market, self.pix)


if __name__ == "__main__":
    unittest.main()
