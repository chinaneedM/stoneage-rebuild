"""Source-bounded INTEGRATION50 28-room service argument replay; no proprietary source assets."""
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"
I49 = ROOT / "STONEAGE-INTEGRATION49-28-ORIGINAL-ROOM-NPC-WARP-SOURCE-ATLAS-R1.json"
ITEM = ROOT / "STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json"
I50 = ROOT / "STONEAGE-INTEGRATION50-28-ROOM-SHOP-PET-ARGUMENT-BRIDGE-R1.json"


class TestSourceBoundRoomShopPetArguments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.i49 = json.loads(I49.read_text(encoding="utf-8"))
        cls.item = json.loads(ITEM.read_text(encoding="utf-8"))
        cls.i50 = json.loads(I50.read_text(encoding="utf-8"))
        cls.rows = cls.i50["source_records"]

    def test_original_counts_and_full_create_identity(self):
        original = Counter()
        for room in self.i49["rooms"]:
            for rec in room["source_records"]:
                role = rec["source_functionset"]
                if role not in ("ItemShop", "PetShop", "PetSkillShop"):
                    continue
                self.assertEqual(len(rec["source_arg_refs"]), 1)
                ref = rec["source_arg_refs"][0]
                key = (
                    room["floor_id"], role, tuple(rec["coordinate"]) if rec["coordinate"] is not None else None,
                    rec["source_CREATE_path"], rec["source_CREATE_block_ordinal"],
                    rec["source_CREATE_block_sha256"], ref["path"], ref["sha256"],
                )
                original[key] += 1
        published = Counter(
            (r["source_floor_id"], r["role"],
             tuple(r["source_coordinate"]) if r["source_coordinate"] is not None else None,
             r["source_CREATE_path"], r["source_CREATE_block_ordinal"],
             r["source_CREATE_block_sha256"], r["source_arg_path"], r["source_arg_sha256"])
            for r in self.rows
        )
        self.assertEqual(original, published)
        self.assertEqual(len(self.rows), 44)
        self.assertEqual(Counter(r["role"] for r in self.rows),
                         {"ItemShop": 32, "PetShop": 6, "PetSkillShop": 6})

    def test_itemshop_fields_preserve_missing_and_empty(self):
        shop = [r for r in self.rows if r["role"] == "ItemShop"]
        self.assertEqual(
            Counter(r["source_LimitItemType_state"] if r["source_LimitItemType_state"] != "LITERAL"
                    else r["source_LimitItemType_literal"] for r in shop),
            {"OFFENCE": 7, "DEFENCE": 5, "ACCESSORY": 6, "EMPTY_LITERAL": 8, "ABSENT": 6})
        for r in shop:
            kind = r["source_LimitItemType_state"]
            if kind == "ABSENT":
                self.assertIsNone(r["source_LimitItemType_literal"])
            elif kind == "EMPTY_LITERAL":
                self.assertEqual(r["source_LimitItemType_literal"], "")
            else:
                self.assertIn(r["source_LimitItemType_literal"], ("OFFENCE", "DEFENCE", "ACCESSORY"))

    def test_itemlist_link_must_match_both_original_path_and_whole_sha(self):
        source = {row["path"]: row for row in self.item["shop_argument_rows"]}
        indexed = 0
        absent = 0
        for r in self.rows:
            if r["role"] != "ItemShop":
                continue
            prev = source.get(r["source_arg_path"])
            if prev is None:
                absent += 1
                self.assertFalse(r["source_ItemList_present"])
                self.assertIsNone(r["previously_indexed_ItemList"])
                self.assertTrue(r["source_arg_path"].startswith("genout/lbis_"))
                continue
            indexed += 1
            self.assertTrue(r["source_ItemList_present"])
            self.assertEqual(prev["source_sha256"], r["source_arg_sha256"])
            x = r["previously_indexed_ItemList"]
            self.assertEqual(x["source_raw_expression_sha256"],
                             prev["raw_ItemList_expression_sha256"])
            self.assertEqual(x["explicit_numeric_ID_count"], prev["explicit_numeric_item_ID_count"])
            self.assertEqual(x["range_expression_count"], len(prev["range_expressions_literal"]))
            self.assertEqual(x["candidate_expanded_ID_count"],
                             len(prev["expanded_candidate_IDs_not_proven_runtime"]))
            self.assertEqual(x["source_buy_rate_literal"], prev["source_buy_rate_text"])
            self.assertEqual(x["source_sell_rate_literal"], prev["source_sell_rate_text"])
        self.assertEqual((indexed, absent), (29, 3))

    def test_duplicate_create_is_retained_not_collapsed(self):
        duplicates = [r for r in self.rows if r["source_arg_path"] == "genout/ss_1302_12_15"]
        self.assertEqual(len(duplicates), 2)
        self.assertEqual({r["source_floor_id"] for r in duplicates}, {1302})
        self.assertEqual(len({r["source_CREATE_block_sha256"] for r in duplicates}), 2)

    def test_six_original_pet_shop_literal_rates_and_pool_fields(self):
        rows = [r for r in self.rows if r["role"] == "PetShop"]
        self.assertEqual({r["source_floor_id"] for r in rows},
                         {1003, 1103, 1203, 1303, 2003, 3003})
        self.assertEqual([r["source_pet_rates_and_pool_literals"]["nomal_rate"]
                          for r in rows].count("0.7"), 1)
        self.assertEqual([r["source_pet_rates_and_pool_literals"]["special_rate"]
                          for r in rows], ["1.5"] * 6)
        self.assertEqual({r["source_floor_id"] for r in rows
                          if "pool_flg" in r["source_pet_rates_and_pool_literals"]},
                         {1003, 2003, 3003})
        for r in rows:
            self.assertTrue(r["source_special_pet_empty_literal"])
            x = r["source_pet_rates_and_pool_literals"]
            self.assertEqual("pool_flg" in x, "pool_cost" in x)
            if "pool_flg" in x:
                self.assertEqual((x["pool_flg"], x["pool_cost"]), ("1", "200"))

    def test_six_skill_lists_are_numeric_source_and_not_renamed(self):
        rows = [r for r in self.rows if r["role"] == "PetSkillShop"]
        self.assertEqual({r["source_floor_id"] for r in rows},
                         {1003, 1103, 1203, 1303, 2003, 3003})
        all_ids = [v for r in rows for v in r["source_pet_skill_IDs_literal"]]
        self.assertEqual(len(all_ids), 50)
        self.assertEqual(len(set(all_ids)), 15)
        self.assertEqual(set.intersection(*(set(r["source_pet_skill_IDs_literal"]) for r in rows)),
                         {0, 1, 2, 3})
        self.assertEqual({r["source_floor_id"]: r["source_skill_rate_literal"] for r in rows},
                         {1003: "1.0", 1103: "1.0", 1203: "1.2",
                          1303: "1.1", 2003: "1.0", 3003: "1.0"})
        self.assertTrue(all(all(isinstance(x, int) for x in r["source_pet_skill_IDs_literal"]) for r in rows))

    def test_exact_public_origins_and_historical_current_guard(self):
        p = self.i50["source_origins"]
        self.assertEqual(p["original_I49_public_atlas_blob"],
                         "673fd0ebd71a909a5678d919f706bab7a8e5e7cc")
        self.assertEqual(p["earlier_itemshop_224_index_blob"],
                         "3bde3b7df43725f28cdac355823667a0ba87e9b1")
        self.assertEqual(p["original_NPC_ZIP_bytes"], 995176)
        self.assertEqual(p["original_NPC_ZIP_members_CRC_verified"], 2205)
        self.assertEqual(self.i50["historical_CURRENT_blob_preserved"]["sha"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertFalse(self.i50["historical_CURRENT_blob_preserved"]["content_edited"])

    def test_negative_scope_guard_against_runtime_or_official_promotion(self):
        b = self.i50["negative_evidence_bounds"]
        self.assertTrue(b)
        self.assertTrue(all(value is False for value in b.values()))
        self.assertEqual(self.i50["stage_A"], "7 PARTIAL + 2 OPEN")
        self.assertEqual(self.i50["stage_B"], "GATED")
        self.assertEqual(self.i50["wiki"], "GATED")
        self.assertEqual(self.i50["R79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(self.i50["overall_percent"])

    def test_latest_next_does_not_expand_same_room_work(self):
        self.assertIn("outside these same 28 rooms", self.i50["next"])
        self.assertEqual(len({r["source_arg_path"] for r in self.rows}), 43)

    def test_pet_service_role_cannot_be_assigned_from_shop_item_types(self):
        for r in self.rows:
            if r["role"] == "ItemShop":
                self.assertNotIn("source_pet_skill_IDs_literal", r)
                self.assertNotIn("source_pet_rates_and_pool_literals", r)
            elif r["role"] == "PetShop":
                self.assertNotIn("source_LimitItemType_literal", r)
                self.assertNotIn("source_pet_skill_IDs_literal", r)
            else:
                self.assertNotIn("source_LimitItemType_literal", r)
                self.assertNotIn("source_pet_rates_and_pool_literals", r)


if __name__ == "__main__":
    unittest.main()
