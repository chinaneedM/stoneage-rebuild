"""O74 derived evidence gates; no proprietary original assets or executable needed."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
O74 = ROOT / "research/recovered/STONEAGE-O74-COMMISSION-BOOK-SELLER-ORIGINAL-SOURCE-R1.json"
O70 = ROOT / "research/recovered/STONEAGE-O70-FOUR-VILLAGE-COMMISSION-R1.json"


class CommissionBookSellerDerivedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(O74.read_text(encoding="utf-8"))
        cls.prior = json.loads(O70.read_text(encoding="utf-8"))

    def test_source_rows_and_unique_four_seller_bindings(self):
        r = self.r
        self.assertEqual(r["schema"], "stoneage.o74.four_hall_commission_book_seller_and_original_npc_pixels.r1")
        self.assertEqual(len(r["original_source_files"]), 12)
        for x in r["original_source_files"].values():
            self.assertTrue(x["exact_member_extracted_and_crc_rechecked"])
            self.assertTrue(x["cp950_roundtrip"])
            self.assertEqual(len(x["sha256"]), 64)
        sellers = r["shop_seller_records"]
        self.assertEqual([x["floor"] for x in sellers], [1009, 2009, 3009, 4009])
        self.assertEqual([len(x["ticket_ids"]) for x in sellers], [6, 6, 5, 6])
        self.assertTrue(all(x["seller_npc_position"] == [20, 12] and
                            x["manager_npc_position"] == [18, 12] and
                            x["seller_graphic_alias"] == 16201 and
                            x["manager_graphic_alias"] == 16200 for x in sellers))
        self.assertEqual(r["npc_template_binding"]["source_functionset"], "ItemShop")
        self.assertIs(r["npc_template_binding"]["native_execution_observed"], False)

    def test_join_with_prior_actual_active_commission_ids(self):
        rows = self.prior["source_quest_record_rows"]
        self.assertEqual(self.prior["totals"]["pet_rows"], 23)
        self.assertEqual(self.prior["totals"]["cooking_rows"], 24)
        pet = {x["ticket_id"] for x in rows if x["task_kind"] == "pet_handover"}
        cooking = {x["ticket_id"] for x in rows if x["task_kind"] == "cooking_handover"}
        seller = {x for s in self.r["shop_seller_records"] for x in s["ticket_ids"]}
        self.assertEqual(len(seller), sum(len(x["ticket_ids"]) for x in self.r["shop_seller_records"]))
        self.assertEqual(seller, pet)
        self.assertFalse(seller & cooking)
        self.assertNotIn(20064, seller)
        self.assertIn(20064, [x["ticket_id"] for x in self.prior["exceptional_records"]])
        self.assertEqual(self.r["directly_source_qualified_ticket_join"]["seller_listed_unique"], 23)
        self.assertEqual(self.r["directly_source_qualified_ticket_join"]["cooking_ticket_ids_listed_in_these_four_sellers"], 0)

    def test_new_seller_bitmap_and_negative_boundaries(self):
        art = self.r["npc_source_art"]
        self.assertEqual(art["actual_original_ADRN_alias_16200"]["dimensions"], [40, 92])
        self.assertEqual(art["actual_original_ADRN_alias_16201"]["dimensions"], [32, 86])
        self.assertTrue(art["both_RD_full_index_two_decoders_equal"])
        self.assertTrue(art["actual_original_pixel_previews_generated_and_viewed"])
        self.assertIs(art["actual_runtime_visual_deployment_not_proven"], True)
        self.assertIs(self.r["bounded_negative_evidence"]["not_claiming_unavailable_in_other_source_or_actual_server"], True)
        self.assertEqual(self.r["bounded_negative_evidence"]["verified_npc_small_source_files_scanned"], 2201)
        self.assertEqual(self.r["bounded_negative_evidence"]["matching_npc_ItemList_entries_for_cooking_tickets"], 0)
        delivery = self.r["private_delivery"]
        self.assertEqual(delivery["members"], 6)
        self.assertTrue(delivery["all_ZIP_member_CRC_pass"])
        self.assertTrue(delivery["private_only"])
        self.assertFalse(delivery["personal_library_uploaded"])
        self.assertEqual(set(delivery["four_hall_candidate_full_PNG_sha256"]), {"1009", "2009", "3009", "4009"})
        for digest in delivery["four_hall_candidate_full_PNG_sha256"].values():
            self.assertEqual(len(digest), 64)
        for field in ("original_world_entered", "original_client_executed", "original_server_executed",
                      "actual_itemshop_transaction_confirmed", "actual_quest_reward_transaction_confirmed",
                      "same_original_official_release_confirmed",
                      "complete_47_book_acquisition_routes_confirmed",
                      "native_scene_order_or_palette_confirmed"):
            self.assertIs(self.r["boundary"][field], False, field)
        self.assertIsNone(self.r["boundary"]["overall_completion_percentage"])
        self.assertEqual(self.r["boundary"]["R79"], "PAUSED_NON_BLOCKING")


if __name__ == "__main__":
    unittest.main()
