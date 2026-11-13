"""INTEGRATION88 derived source and negative claims, not execution of original game."""
import json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"research"/"recovered"
def read(name): return json.loads((ROOT/name).read_text(encoding="utf-8"))
class TestSourceBoundTeamCamps(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=read("STONEAGE-INTEGRATION88-TEAM-CAMP-GATE-WARP-ORIGINAL-2D-R1.json")
  cls.c=read("STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json")
  cls.p=read("STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
 def test_original_parent_file_bytes_crc_sha(self):
  a=next(x for x in self.c["source_files"] if x[0]=="genout/500npc_m.create")
  v=self.d["provenance"]
  self.assertEqual([14674,v["source_create_original_sha256"],v["source_create_original_crc32"]],a[1:4])
 def test_full_original99_per_byte_source_span_sha_and_references(self):
  orig=[r for r in self.c["create_rows"] if r[0]=="genout/500npc_m.create"]
  out=self.d["full_99_original_source_create_numeric_sha_rows"]
  self.assertEqual(99,len(orig));self.assertEqual(99,len(out))
  for s,r in zip(orig,out):
   self.assertEqual([s[1],[s[2],s[3]],*s[4:16]],[r[k] for k in ("ordinal","bytes","sha256","floor","graphic","borncorner","borncenter","createnum","direction","function_token","template_link_class","template_ref","original_name_sha256","original_file_targets")])
 def test_original_source_type_not_species_or_one_npc_per_block(self):
  d=self.d["summary"]
  self.assertEqual({"npcgen_man":50,"npcgen_warpman":3,"npcgen_shop":1,"npcgen_signboard":1,"npcgen_warp":44},d["source_function_counts"])
  self.assertEqual(55,d["with_graphic"]);self.assertEqual(44,d["without_graphic"])
  self.assertEqual(99,d["original_CREATE_blocks"])
  self.assertEqual(11,d["source_distinct_floor_values"])
 def test_exact_original_source_file_targets(self):
  refs=[a for r in self.d["full_99_original_source_create_numeric_sha_rows"] for a in r["original_file_targets"]]
  self.assertEqual(46,len(refs))
  self.assertEqual(46,len(set(x[0] for x in refs)))
  self.assertTrue(all(x[1]=="EXACT_SAME_NPC_SUBTREE_PATH" and len(x[2])==64 for x in refs))
 def test_three_original_source_guard_conditions(self):
  gates=self.d["three_original_source_warpman_gate_parameter_literals"]
  self.assertEqual([7,19,36],[g["ordinal"] for g in gates])
  self.assertEqual([18553,18554,18555],[g["literal_FREE_ITEM"] for g in gates])
  self.assertEqual([[5532,0,22],[5536,30,13],[5533,30,11]],[g["literal_WARP"] for g in gates])
  by={x["ordinal"]:x for x in self.d["full_99_original_source_create_numeric_sha_rows"]}
  for g in gates:
   r=by[g["ordinal"]]
   self.assertEqual("npcgen_warpman",r["function_token"])
   self.assertEqual(g["origin"][0],r["floor"])
   self.assertEqual(g["origin"][1:],r["borncorner"][:2])
   self.assertEqual(g["original_target_sha256"],r["original_file_targets"][0][2])
   self.assertEqual(-1,g["literal_MONEY"])
 def test_all44_original_warp_source_literals_preserved(self):
  d=self.d
  w=d["source_44_npcgen_warp_destination_literals"]
  self.assertEqual(44,len(w));self.assertEqual(list(range(55,99)),[x["ordinal"] for x in w])
  self.assertEqual(42,sum(x["source_floor"]==500 for x in w))
  self.assertEqual(2,sum(x["source_floor"]==5530 for x in w))
  self.assertEqual([5530,23,59,"N"],w[0]["original_target_arg_tuple"])
  self.assertEqual([500,189,318,None],w[-1]["original_target_arg_tuple"])
  self.assertEqual(1,sum(x["original_target_arg_tuple"][3] is not None for x in w))
  self.assertEqual(2,len(d["original_duplicate_spawn_source_positions_not_collapsed"]))
 def test_tw10_original_source_2d_groups_exact_public_numeric_hash(self):
  groups=self.d["source_numeric_TW1_original_2D_graphic_candidates"]
  public={x[0]:x for x in self.p["source_groups"]}
  rows={x["ordinal"]:x for x in self.d["full_99_original_source_create_numeric_sha_rows"]}
  self.assertEqual([100259,100379,100401,100432],[x["graphic"] for x in groups])
  self.assertEqual(29,sum(len(x["matching_source_create_ordinals"]) for x in groups))
  self.assertEqual(57,sum(len(x["original_existing_pixels"]) for x in groups))
  for g in groups:
   src=public[g["graphic"]]
   self.assertEqual([src[1],src[2],src[3],src[4]],[g["tw1_source_group_index"],g["original_spr_group_sha256"],g["source_full_animation_count"],g["all_selected_original_source_frame_positions"]])
   self.assertEqual(src[5],g["source_original_action_direction0_segments"])
   self.assertEqual([g["graphic"]]*len(g["matching_source_create_ordinals"]),[rows[i]["graphic"] for i in g["matching_source_create_ordinals"]])
 def test57_original_pixel_digest_size_from_earlier_real_source(self):
  lookup={r[0]:r for r in self.p["source_actual_pixel_receipts"]}
  seen=set()
  for g in self.d["source_numeric_TW1_original_2D_graphic_candidates"]:
   for pix in g["original_existing_pixels"]:
    self.assertNotIn(pix[0],seen);seen.add(pix[0])
    old=lookup[pix[0]]
    self.assertEqual([old[0],old[2],old[5],old[6],old[8]],pix)
  self.assertEqual(57,len(seen))
 def test_three_original_gate_items_both_94_field_masters_and_icon_candidate(self):
  shard=read("item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-07-R1.json")
  source={r[0]:r for r in shard["rows"]}
  out=self.d["original_three_guard_pass_item_same_carrier_two_original_itemsets_source_rows"]
  self.assertEqual([18553,18554,18555],[x["item_id"] for x in out])
  self.assertEqual([24124,24126,24127],[x["original_itemset_B_image_alias"] for x in out])
  for r in out:
   prior=source[r["item_id"]]
   self.assertEqual([r["item_id"],r["original_itemset_A_94_fields_full_row_sha256"],r["original_itemset_B_94_fields_full_row_sha256"],r["original_itemset_A_image_alias"],r["original_itemset_B_image_alias"],r["source_B_original_cost_raw"],r["source_B_original_type_raw"],r["source_B_original_level_raw"],r["source_A_prior_TW1_RD_qualification"],r["source_B_prior_TW1_RD_qualification"],r["original_changed_columns_between_same_archived_itemset_rows"]],prior)
   self.assertEqual(r["original_itemset_A_94_fields_full_row_sha256"],r["original_itemset_B_94_fields_full_row_sha256"])
   self.assertEqual("REAL_RD_DECODED_CROSS_CARRIER",r["source_A_prior_TW1_RD_qualification"])
  self.assertEqual([x["literal_FREE_ITEM"] for x in self.d["three_original_source_warpman_gate_parameter_literals"]],[x["item_id"] for x in out])
  self.assertFalse(self.d["evidence_limits"]["cross_carrier_TW1_item_icon_is_verified_same_deployment_of_mixed25_gate"])
 def test_unrenderable_82729_and_uncaptured_100406_not_promoted(self):
  g=next(x for x in self.d["source_numeric_TW1_original_2D_graphic_candidates"] if x["graphic"]==100401)
  self.assertEqual([82729],g["prior_strict_RD_RLE_error_action0"]["original_bitmap"] if isinstance(g["prior_strict_RD_RLE_error_action0"]["original_bitmap"],list) else [g["prior_strict_RD_RLE_error_action0"]["original_bitmap"]])
  self.assertEqual(26,g["prior_strict_RD_RLE_error_action0"]["not_rendered_original_frame_positions"])
  self.assertEqual(2,g["private_observer_shown_sequence_count"])
  self.assertEqual(75,self.d["summary"]["private_observer_visible_source_frame_positions"])
  self.assertEqual(101,self.d["summary"]["TW1_PET07_original_index_action_source_frame_positions"])
  self.assertEqual(10,self.d["summary"]["source_graphic_100406_not_in_PET07_subset"])
 def test_source_boundary_no_native_claim(self):
  n=self.d["evidence_limits"]
  for k in ("same_numeric_graphic_proves_same_early_official_deployment","source_99_configs_prove_NPCs_spawned_in_native_world","source_44_warp_literals_prove_native_warp_triggers","original_WARP_FREE_ITEM_and_MONEY_minus_one_runtime_effect_verified","original_private_modern_viewer_is_native_original_game","original_binary_scripts_dialogue_artwork_publicly_committed"):
   self.assertFalse(n[k],k)
  self.assertTrue(n["original_100401_action0_82729_strict_RD_unrenderable_is_preserved"])
  self.assertEqual(0,self.d["summary"]["new_original_RD_decode"])
  self.assertIsNone(n["overall_percent"])
if __name__=="__main__": unittest.main()
