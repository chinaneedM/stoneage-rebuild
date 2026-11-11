"""INTEGRATION61: derived-only original two-chef menu/item/TW1 RD source gate."""
import json
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"research"/"recovered"
class Integration61(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((P/"STONEAGE-INTEGRATION61-TWO-CHEFS-THREE-DISHES-TW1-PIXEL-SOURCE-R1.json").read_text())
  cls.old=json.loads((P/"STONEAGE-O75-ORIGINAL-COOKING-CRAFTING-NPC-SOURCE-R1.json").read_text())
  cls.shard={row[0]:row for row in json.loads((P/"item-module-01"/"STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-04-R1.json").read_text())["rows"]}
 def test_two_original_chefs(self):
  self.assertEqual(self.r["source_two_chefs"],[x for x in self.old["original_NPC_spawn_from_menu_create"] if x["kind"]=="chef"])
  self.assertEqual([x["floor"] for x in self.r["source_two_chefs"]],[2009,3009])
  self.assertEqual(self.r["source_2009_unmatched_item_IDs_status"],"UNKNOWN_NONEXACT_NAMES")
 def test_three_exact_menu_rows_only(self):
  old=[x for x in self.old["chef_menu_to_itemset"] if x["exact_unique_itemset_name"]]
  new=self.r["source_3009_three_exact_items"]
  self.assertEqual([x["item_id"] for x in new],[12607,12780,12754])
  self.assertEqual([x["item_id"] for x in new],[x["item_id"] for x in old])
  self.assertEqual(sum(x["item_id"] is None for x in self.old["chef_menu_to_itemset"]),3)
 def test_original_row_ingredient_and_callback(self):
  for x in self.r["source_3009_three_exact_items"]:
   old=next(r for r in self.old["chef_menu_to_itemset"] if r["item_id"]==x["item_id"])
   ix=self.shard[x["item_id"]]
   self.assertEqual(x["source_A_B_full_row_sha256"],old["full_source_row_sha256"])
   self.assertEqual(x["source_A_B_full_row_sha256"],ix[1])
   self.assertEqual(ix[1],ix[2])
   self.assertEqual(x["original_item_image_alias"],ix[3])
   self.assertEqual(ix[3],ix[4])
   self.assertEqual(x["original_source_price_text"],ix[5])
   self.assertEqual(x["original_source_type_text"],ix[6])
   self.assertEqual(ix[8:10],["REAL_RD_DECODED_CROSS_CARRIER"]*2)
   self.assertEqual(x["source_callback"],old["item_usefunc"])
   self.assertEqual(x["source_material_names"],old["atom_names"])
   self.assertEqual(x["source_material_values_not_recipe_quantities"],old["atom_values"])
 def test_three_retained_original_RDs_are_not_alias_numbers(self):
  ds=self.r["source_3009_three_exact_items"]
  self.assertEqual([x["original_item_image_alias"] for x in ds],[24484,24443,24531])
  self.assertEqual([x["TW1_saved_original_pixel"]["adrn_ordinal"] for x in ds],[6651,6610,6698])
  self.assertEqual([x["TW1_saved_original_pixel"]["dimensions"] for x in ds],[[28,42],[44,35],[32,34]])
  for x in ds:
   q=x["TW1_saved_original_pixel"]
   self.assertNotEqual(x["original_item_image_alias"],q["adrn_ordinal"])
   self.assertTrue(all(len(q[f])==64 for f in ["original_adrn_record_sha256","original_rd_sha256","original_indexed_pixel_sha256","candidate_rgba_sha256","candidate_png_sha256"]))
   self.assertTrue(x["private_pixel_filename"].endswith("/alias-%s.png"%x["original_item_image_alias"]))
 def test_custody_and_negative_scope(self):
  self.assertEqual(self.r["private_replay"]["retained_png_file_sha256_dimension_rgba_sha256_checked"],3)
  self.assertTrue(self.r["private_replay"]["zip_member_CRC_all_pass"])
  self.assertFalse(self.r["private_replay"]["old_original_RAR_reread"])
  self.assertEqual(self.r["private_replay"]["new_RD_binary_decodes"],0)
  for value in self.r["negative"].values(): self.assertFalse(value)
  self.assertEqual(self.r["historical_CURRENT_git_blob_unchanged"],"c89e0e33537990aa2132b47c40fef49a985a935c")
  self.assertEqual(self.r["stage_A"],"7_PARTIAL_2_OPEN")
  self.assertIsNone(self.r["overall_percent"])
if __name__=="__main__": unittest.main()
