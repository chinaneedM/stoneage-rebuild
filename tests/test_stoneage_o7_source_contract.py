"""Public O7 numerical source and historical-limits regressions only; no private art."""
import copy
import unittest
from tools import stoneage_o7_source_contract as o7

class O7SourceOnlyTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.records=o7.read()
 def modified(self,key,fn):
  r=copy.deepcopy(self.records);fn(r[key]);return r
 def expect(self,key,fn,error):
  with self.assertRaisesRegex(ValueError,error):o7.validate(self.modified(key,fn))
 def test_accept_archived_source_bounded_rows(self):
  r=o7.validate(self.records);self.assertEqual(r["source_item_ids"],[0,4,10]);self.assertFalse(r["historical_game_world_entered"])
 def test_three_source_descriptive_stat_sets(self):
  self.assertEqual(o7.validate(self.records)["source_modifiers"],[[9,-3,-3],[7,-2,-2],[14,-5,-5]])
 def test_original_shop_outside_bounded_window(self):
  s=self.records["o7"]["shop"];b=s["o6_room_sample_bounds"];x,y=s["xy"]
  self.assertFalse(b[0]<=x<=b[2] and b[1]<=y<=b[3])
 def test_item_id_zero_is_not_missing(self):
  self.assertEqual(self.records["o7"]["items"][0]["id"],0)
 def test_invalid_item_cost_rejected(self):
  self.expect("o7",lambda x:x["items"][0].__setitem__("source_cost",66),"identity/price")
 def test_invalid_item_raw_stats_rejected(self):
  self.expect("o7",lambda x:x["items"][1]["description_modifiers"].__setitem__("attack",99),"text modifier")
 def test_wrong_repeated_raw_fields_rejected(self):
  self.expect("o7",lambda x:x["items"][2]["raw_numeric_values"].__setitem__(1,44),"numeric column")
 def test_wrong_raw_column_numbers_rejected(self):
  self.expect("o7",lambda x:x["items"][0].__setitem__("raw_duplicate_numeric_columns_0based",[36,38,39,40,41,42]),"numeric column")
 def test_item_order_or_id_tampering_rejected(self):
  self.expect("o7",lambda x:x["items"][0].__setitem__("id",4),"identity/price")
 def test_png_hash_forgery_rejected(self):
  self.expect("o7",lambda x:x["items"][2].__setitem__("source_candidate_png_sha256","0"*64),"PNG fingerprint")
 def test_source_alias_namespace_confusion_rejected(self):
  self.expect("scene24",lambda x:x["items"][0]["alias_candidate"].__setitem__("bitmapno",20033),"alias mismatch")
 def test_wrong_original_map_dat_rejected(self):
  self.expect("o7",lambda x:x.__setitem__("room_source_map_dat_sha256","0"*64),"DAT source")
 def test_false_shop_npc_visible_rejected(self):
  self.expect("o7",lambda x:x["shop"].__setitem__("shop_inside_o6_sample",True),"false shop NPC visibility")
 def test_no_extra_item_or_stock_inferred(self):
  self.expect("o7",lambda x:x["shop"].__setitem__("original_stock_count",3),"stock count")
 def test_original_transaction_claim_rejected(self):
  self.expect("o7",lambda x:x["historical_limits"].__setitem__("original_shop_NPC_interaction_or_buying_authenticated",True),"historical claim")
 def test_false_taiwan_official_mapping_rejected(self):
  self.expect("o7",lambda x:x.__setitem__("provenance","OFFICIAL_TW1"),"official provenance")
 def test_private_browser_source_frame_claim_rejected(self):
  self.expect("o7",lambda x:x["private_O7"].__setitem__("pet_frame_positions_visited_in_real_browser",351),"pet replay counts")
 def test_forged_browser_file_open_claim_rejected(self):
  self.expect("o7",lambda x:x["private_O7"].__setitem__("original_O7_html_file_url_navigation_verified",True),"false original native")
 def test_browser_network_request_rejected(self):
  self.expect("o7",lambda x:x["private_O7"].__setitem__("external_network_requests",1),"external request")
 def test_public_github_cannot_certify_original_png(self):
  self.assertFalse(self.records["o7"]["private_O7"]["original_game_exe_executed"])
  self.assertEqual(self.records["o7"]["private_O7"]["shop_candidate_PNGs_decoded_in_real_browser"],3)
 def test_o6_original_source_custody_protected(self):
  self.expect("o7",lambda x:x["private_original_input_zip_sha256"].__setitem__("o6","0"*64),"O6 private source")

if __name__=="__main__":unittest.main()
