"""Original TW1.0 static bitmap catalog and real protocol field placement are source-scoped."""
import unittest
from tools.stoneage_tw10_item_static_bitmap_source import observe

class OriginalItemStaticSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=observe()

    def test_original_universes_not_guessed_items(self):
        d=self.result
        self.assertEqual(d["original_total_bitmap_numbers"],125996)
        self.assertEqual(d["original_bitmap_number_min_max"],[0,125995])
        self.assertEqual(d["item_player_band_id_count"],1031)
        self.assertEqual(d["item_player_band_spr_frame_refs"],0)
        self.assertEqual(len(d["bitmap_metadata_bands"]),5)
        b={x["player_category_id"]:x for x in d["bitmap_metadata_bands"]}
        self.assertEqual(b["items"]["original_tw10_bitmap_range"],[5973,7003])
        self.assertEqual(b["items"]["original_bitmap_id_membership_count"],1031)
        for data in b.values():
            lo,hi=data["original_tw10_bitmap_range"]
            self.assertEqual(data["original_bitmap_id_membership_count"],hi-lo+1)
            self.assertEqual(sum(x["records"] for x in data["top_dimension_pairs"]) <= hi-lo+1,True)
            self.assertEqual(sum(x["count"] for x in data["rd_flag_value_counts"]),hi-lo+1)
            self.assertLessEqual(data["distinct_nonempty_rd_block_sha256"],hi-lo+1)
            self.assertEqual(len(data["example_original_records"]),5)
            self.assertTrue(data["displayed_2001_player_text_not_original_tw10_semantic"])
            self.assertFalse(data["original_static_draw_call_verified"])

    def test_three_compiled_graphic_positions_not_claiming_selector(self):
        d=self.result
        locations=d["item_graphic_message_fields"]
        self.assertEqual([(x["wire"],x["field_position"],x["callback_rva"]) for x in locations],
                         [("S:I",5,"0x30922"),("I",6,"0x325f0"),("C",4,"0x31260")])
        self.assertTrue(all(x["position_evidence"]=="V1_DIRECT" for x in locations))
        self.assertTrue(all(x["semantic_label_evidence"]=="EARLY_LINEAGE" for x in locations))
        self.assertTrue(all(not x["direct_selector_to_original_adrn_bitmapno_verified"] for x in locations))

    def test_limit_unknown_and_original_data_not_exported(self):
        d=self.result
        self.assertTrue(d["compiled_same_build_wire_position_observed"])
        for key in ("transmitted_real_graphic_values_observed","draw_selector_graphic_id_to_bitmapno_certified",
                    "original_game_item_master_source_acquired","original_item_name_price_recipe_catalog_complete",
                    "item_count_equal_to_bitmap_candidate_count_proven","original_client_executed",
                    "copyrighted_game_pixels_published","stage_b_production_started"):
            self.assertFalse(d[key],key)
        self.assertEqual(d["next"],"TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01")
if __name__=="__main__": unittest.main()
