"""Source-bounded derived-only INTEGRATION60 clinic, item-handler, and original-pixel crosswalk."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "research/recovered"
NEW = P / "STONEAGE-INTEGRATION60-FIVE-ORIGINAL-CLINICS-NURSE-MEDICINE-ITEM-HANDLER-PIXEL-SOURCE-R1.json"
I49 = P / "STONEAGE-INTEGRATION49-28-ORIGINAL-ROOM-NPC-WARP-SOURCE-ATLAS-R1.json"
I50 = P / "STONEAGE-INTEGRATION50-28-ROOM-SHOP-PET-ARGUMENT-BRIDGE-R1.json"
GAME05 = P / "STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json"
SHOP = P / "STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json"


class TestOriginalClinics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(NEW.read_text(encoding="utf-8"))
        cls.i49 = json.loads(I49.read_text(encoding="utf-8"))
        cls.i50 = json.loads(I50.read_text(encoding="utf-8"))
        cls.g05 = json.loads(GAME05.read_text(encoding="utf-8"))
        cls.shops = json.loads(SHOP.read_text(encoding="utf-8"))
        cls.idx = {}
        for k in range(1, 8):
            path = P / "item-module-01" / f"STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{k:02d}-R1.json"
            cls.idx.update({x[0]: x for x in json.loads(path.read_text(encoding="utf-8"))["rows"]})

    def test_preserved_custody_and_stage(self):
        s = self.r["source_origin"]
        self.assertEqual(s["NPC_ZIP_sha256"], "c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f")
        self.assertEqual(s["ITEM01_ZIP_sha256"], "cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa")
        self.assertEqual([s["NPC_ZIP_original_members_CRC_verified"], s["ITEM01_ZIP_original_members_CRC_verified"]], [2205, 838])
        self.assertEqual(s["new_private_custody_zip_sha256"], "940617f696b2dc45f8b2e8009e0e4286a764fea24a0c979dd5843306be84e280")
        self.assertEqual(s["new_private_custody_zip_members_CRC_verified"], 28)
        self.assertFalse(s["full_mixed25_RAR_reread_this_unit"])
        self.assertFalse(s["original_binary_TW1_RD_redecoded_this_unit"])
        self.assertEqual(self.r["negative_bounds"]["stage_A"], "7_PARTIAL_2_OPEN")

    def test_five_original_room_DAT_and_two_NPC_blocks(self):
        rows = self.r["original_five_clinics"]
        self.assertEqual([r["source_floor_id"] for r in rows], [1105,1205,1305,2005,3005])
        for r in rows:
            i49 = next(x for x in self.i49["rooms"] if x["floor_id"] == r["source_floor_id"])
            self.assertEqual(r["original_room_DAT_sha256_previous_verified"], i49["original_DAT_sha256"])
            for role,oldrole in [("nurse","WindowHealer"),("pharmacist","ItemShop")]:
                got=r[role]
                originals=[x for x in i49["source_records"] if x["source_functionset"]==oldrole]
                self.assertEqual(len(originals),1)
                old=originals[0]
                self.assertEqual([got["source_coordinate"],got["source_CREATE_block_sha256"],got["source_graphic_alias"]],
                                 [old["coordinate"],old["source_CREATE_block_sha256"],old["graphic_alias"]])

    def test_nurse_four_original_inline_values_are_exact(self):
        for row in self.r["original_five_clinics"]:
            n=row["nurse"]
            old=[x for x in self.g05["original_CREATE_refs_and_derived_numeric_fields"]
                 if x["floorid"]==row["source_floor_id"] and x["source_function"]=="npcgen_winhealer"]
            self.assertEqual(len(old),1)
            self.assertEqual(n["original_inline_four_tokens"],old[0]["source_enemy_argument_tokens"])
            self.assertEqual(n["source_CREATE_ordinal"],old[0]["create_ordinal"])
            self.assertEqual(n["source_CREATE_block_sha256"],old[0]["create_block_sha256"])
            self.assertEqual(len(n["original_inline_four_tokens"]),4)

    def test_pharmacist_arguments_have_original_paths_sha_and_rates(self):
        idx={x["path"]:x for x in self.shops["shop_argument_rows"]}
        prior={x["source_arg_path"]:x for x in self.i50["source_records"] if x["role"]=="ItemShop"}
        for row in self.r["original_five_clinics"]:
            p=row["pharmacist"];old=idx[p["original_argument_path"]];prev=prior[p["original_argument_path"]]
            self.assertEqual(p["original_argument_full_sha256"],old["source_sha256"])
            self.assertEqual(p["original_argument_full_sha256"],prev["source_arg_sha256"])
            self.assertEqual(p["original_ItemList_text_sha256"],old["raw_ItemList_expression_sha256"])
            self.assertEqual(p["source_ItemList_original_ID_order"],old["expanded_candidate_IDs_not_proven_runtime"])
            self.assertEqual(p["source_buy_rate_literal"],old["source_buy_rate_text"])
            self.assertEqual(p["source_sell_rate_literal"],old["source_sell_rate_text"])
            self.assertEqual(p["source_CREATE_block_sha256"],prev["source_CREATE_block_sha256"])
            self.assertEqual(p["source_LimitItemType_state"],"EMPTY_LITERAL")
            self.assertFalse(old["range_expressions_literal"])

    def test_sixty_source_references_twelve_distinct_with_exact_identity(self):
        clinics=self.r["original_five_clinics"]
        ids=[id for room in clinics for id in room["pharmacist"]["source_ItemList_original_ID_order"]]
        items=self.r["original_twelve_eligible_medicine_rows"]
        self.assertEqual(len(ids),60)
        self.assertEqual(len(set(ids)),12)
        self.assertEqual(set(ids),{x["original_item_id"] for x in items})
        self.assertTrue(all(room["pharmacist"]["source_ItemList_original_ID_order"]==clinics[0]["pharmacist"]["source_ItemList_original_ID_order"] for room in clinics))
        for r in items:
            old=self.idx[r["original_item_id"]]
            self.assertEqual(r["original_item_A_B_complete_row_sha256"],old[1])
            self.assertEqual(old[1],old[2])
            self.assertEqual(r["original_item_raw_cost_zero_based_col18"],old[5])
            self.assertEqual(r["original_item_type_zero_based_col19"],old[6])
            self.assertEqual(r["original_item_image_alias_zero_based_col17"],old[4])
            self.assertEqual(old[8],"REAL_RD_DECODED_CROSS_CARRIER")
            self.assertEqual(old[9],"REAL_RD_DECODED_CROSS_CARRIER")

    def test_three_original_handler_buckets_and_raw_field_shapes(self):
        items=self.r["original_twelve_eligible_medicine_rows"]
        groups={}
        for x in items:
            groups.setdefault(x["original_item_use_handler_zero_based_col10"],[]).append(x["original_item_id"])
        self.assertEqual(groups,{
           "ITEM_useRecovery":[1500,1501,1510,1511,1512],
           "ITEM_useRessurect":[1530,1531],
           "ITEM_useStatusRecovery":[1540,1541,1542,1543,1545]
        })
        self.assertEqual([x["original_item_scene_zero_based_col20"] for x in items],["0"]*5+["1"]*7)
        self.assertEqual([x["original_item_target_zero_based_col21"] for x in items],["1"]*5+["101"]*2+["1"]*5)
        self.assertEqual([x["original_item_effect_token_zero_based_col3"] for x in items[-5:]],["毒","石","亂","醉","眠"])

    def test_eleven_original_pixel_qualifications_and_one_shared_sprite(self):
        rows=self.r["original_twelve_eligible_medicine_rows"]
        alias={x["original_item_image_alias_zero_based_col17"] for x in rows}
        self.assertEqual(len(alias),11)
        self.assertEqual([x["original_item_image_alias_zero_based_col17"] for x in rows if x["original_item_id"] in [1530,1531]],[23021,23021])
        for x in rows:
            self.assertEqual(x["retail_TW1_RD_qualification"],"VERIFIED_ORIGINAL_RD_INDEXED_PIXELS_CROSS_CARRIER_NOT_SELECTOR")
            for key in ("independently_retained_TW1_original_RD_sha256","independently_retained_TW1_candidate_PNG_sha256"):
                self.assertRegex(x[key],r"^[a-f0-9]{64}$")
            w,h=x["original_RD_bitmap_dimensions"]
            self.assertGreater(w,0)
            self.assertGreater(h,0)

    def test_no_native_transaction_or_crossversion_promotion(self):
        bounds=self.r["negative_bounds"]
        for key in ("clinic_native_UI_or_healing_executed","client_shop_purchase_tested","actual_recovery_revive_status_effect_for_all_12_tested","shop_buy_rate_as_actual_price_formula_proven","nurse_inline_four_arg_interpretation_proven","TW1_retained_pixel_is_native_mixed25_selected_graphic_proven","tw1_early_or_JSS_official_same_deployment_proven","private_original_proprietary_content_published"):
            self.assertFalse(bounds[key])
        self.assertIsNone(bounds["overall_percent"])
        self.assertEqual(bounds["stage_B_wiki"],"GATED")
        self.assertEqual(bounds["R79"],"PAUSED_NON_BLOCKING")


if __name__ == "__main__":
    unittest.main()
