"""Replay only rights-safe, source-qualified metadata; no commercial originals."""
import json
import pathlib
import re
import unittest
from collections import Counter

ROOT=pathlib.Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-INTEGRATION108-DUELROOM-34-CREATE-26-SOURCE-WARP-ITEM-R1.json'
MAP=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json'
ITEMDIR=ROOT/'research/recovered/item-module-01'

class DuelRoomSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.v=json.loads(REPORT.read_text(encoding='utf-8'))
  cls.map=json.loads(MAP.read_text(encoding='utf-8'))
  cls.rows=cls.v['original_CREATE_numeric_rows_with_sha256']
  cls.handlers=cls.v['original_referenced_handler_sha_and_parsed_directives']
  cls.warps=cls.v['original_bounded_warpman_values']

 def test_parent_evidence_and_immutable_current(self):
  p=self.v['provenance']
  self.assertEqual(p['original_NPC_private_ZIP_sha256'],'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
  self.assertEqual(p['source_file_full_sha256'],'4c47e9c320f9d3fe6616e6860d14d2681df1994bb8c4a849e5b6d93a38998a91')
  self.assertEqual(p['prior_MAP01_original_RAR_sha256'],self.map['original_rar_sha256'])
  self.assertEqual(self.v['baseline']['full_prior_CURRENT_git_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
  self.assertEqual(self.v['baseline']['prior_CURRENT_bytes'],2709173)

 def test_count_consistency_and_sha_length(self):
  c=self.v['counts']
  self.assertEqual(len(self.rows),34)
  self.assertEqual(c['create_blocks'],34)
  self.assertEqual(len({(r['floor'],*r['xy']) for r in self.rows}),34)
  self.assertEqual(Counter(r['floor'] for r in self.rows),{130:29,1000:1,2000:1,3000:1,4000:1,110:1})
  self.assertEqual(c['source_template_counts'],dict(sorted(Counter(r['template'] for r in self.rows).items())))
  self.assertEqual(len(self.handlers),26)
  self.assertEqual(sum(r['original_handler_relative_path'] is not None for r in self.rows),26)
  self.assertEqual([r['ordinal'] for r in self.rows],list(range(34)))
  self.assertTrue(all(re.fullmatch(r'[0-9a-f]{64}',r['original_create_block_sha256']) for r in self.rows))

 def test_original_source_byte_spans_and_refs(self):
  s=self.v['provenance']['source_file_bytes']
  spans=[r['original_byte_span'] for r in self.rows]
  self.assertTrue(all(0<=a<b<=s for a,b in spans))
  self.assertTrue(all(spans[i][1]<spans[i+1][0] for i in range(33)))
  self.assertEqual({r['original_handler_relative_path'] for r in self.rows if r['original_handler_relative_path'] is not None},set(self.handlers))
  self.assertTrue(all(re.fullmatch(r'[0-9a-f]{64}',h['original_full_sha256']) and h['original_bytes']>0 for h in self.handlers.values()))

 def test_map01_qualified_geometry_not_passability(self):
  c=self.v['counts'];meta=self.v['prior_original_map_DAT_metadata']
  self.assertEqual(c['prior_MAP01_qualified_coordinate_in_bounds'],32)
  self.assertEqual(c['prior_MAP01_no_qualified_DAT'],2)
  self.assertEqual(c['prior_MAP01_qualified_out_of_bounds'],0)
  self.assertEqual(sorted(r['floor'] for r in self.rows if r['map01_DAT_dimension_qualification']=='NO_QUALIFIED_DAT_IN_MAP01'),[1000,3000])
  self.assertTrue(all(r['map01_DAT_dimension_qualification']=='WITHIN_QUALIFIED_DAT_HEADER' for r in self.rows if r['floor']==130))
  self.assertEqual(next(x['dimensions'] for x in meta if x['floor']==130),[60,60])
  actual={int(r[5]):r for r in self.map['original_decoded_source_rows'] if r[0]==0 and str(r[1]).upper().endswith('.DAT') and r[5] is not None and r[8]}
  self.assertEqual({x['floor'] for x in meta},set([110,130,2000,4000]))
  for x in meta:
   r=actual[x['floor']]
   self.assertEqual(x['source_sha256'],r[3]);self.assertEqual(x['dimensions'],[r[6],r[7]])
   self.assertEqual(x['original_bytes'],8+6*r[6]*r[7])

 def test_nine_static_guide_parameters_not_live_warps(self):
  self.assertEqual(len(self.warps),9)
  self.assertEqual(Counter(x['source_floor'] for x in self.warps),{130:4,1000:1,2000:1,3000:1,4000:1,110:1})
  self.assertEqual(Counter(x['original_target_tuple'][0] for x in self.warps),{130:5,1000:1,2000:1,3000:1,4000:1})
  self.assertEqual([x['original_target_tuple'] for x in self.warps if x['source_floor'] in (1000,2000,3000,4000)],[[130,57,13],[130,57,22],[130,57,31],[130,57,40]])
  self.assertEqual([x['source_xy'] for x in self.warps if x['source_floor']==130],[[57,12],[57,21],[57,30],[57,39]])
  self.assertTrue(all(x['source_MONEY_raw']=='-1' for x in self.warps))
  self.assertEqual(sum(x['target_DAT_qualification']=='WITHIN_QUALIFIED_DAT_HEADER' for x in self.warps),7)

 def test_original_ticket_gates_as_values_not_transactions(self):
  self.assertEqual(sorted(set(v for w in self.warps for v in w['source_FREE_item_ids'])),[2597,2598,2599,2600,2601])
  self.assertEqual(len([w for w in self.warps if w['source_floor']==110 and w['source_FREE_item_ids']==[2597,2598,2599,2600,2601]]),1)
  self.assertEqual([w['source_FREE_item_ids'] for w in self.warps if w['source_floor']==130],[[2597],[2598],[2599],[2600]])
  self.assertEqual(self.v['limitations']['native_warp_exec_or_collision_proven'],False)

 def test_nine_limited_shop_list_rows(self):
  shops=[x for x in self.handlers.values() if x['source_template']=='npcgen_shop']
  self.assertEqual(len(shops),9)
  ids=[i for x in shops for i in x['literal_ItemList_explicit_ids']]
  self.assertEqual(len(ids),127)
  self.assertEqual(len(set(ids)),100)
  self.assertEqual(set(ids),set(self.v['original_shop_all_explicit_item_IDs_once']))
  self.assertTrue(all(re.fullmatch('[a-f0-9]{64}',x['literal_ItemList_sha256']) for x in shops))
  self.assertEqual(sum(x['literal_LimitItemNo_has_range_syntax'] for x in shops),2)

 def test_cross_saved_item_catalog_rows_if_available(self):
  fs=sorted(ITEMDIR.glob('STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-*-R1.json'))
  self.assertEqual(len(fs),7,'Required pre-existing public item shard files not present')
  idx={}
  for p in fs:
   dat=json.loads(p.read_text(encoding='utf-8'))
   for r in dat['rows']:
    idx[r[0]]=r
  for x in self.v['cross_existing_two_original_itemsets_numeric_rows']:
   r=idx[x['item_id']]
   self.assertEqual(r[1],x['source_a_original_row_sha256'])
   self.assertEqual(r[2],x['source_b_original_row_sha256'])
   self.assertEqual(r[4],x['source_b_image_number'])
  self.assertEqual(len(self.v['cross_existing_two_original_itemsets_numeric_rows']),110)

 def test_same_carrier_actor_and_cross_carrier_icons_are_not_original_screen(self):
  a=self.v['original_same_carrier_sprite_candidate']
  self.assertEqual(a['original_SPR_graphic_group'],100250)
  self.assertEqual(a['first_frame_bitmap'],95883)
  self.assertEqual(a['prior_candidate_PNG_sha256'],'32020af425521f05014d68538fa2355ff70d3c52d73761044ed2e6532bec8a43')
  self.assertTrue(a['private_PNG_recovery_SHA_matches_prior_report'])
  self.assertEqual(sum(x['graphicname']==100250 for x in self.rows),1)
  icons=self.v['cross_carrier_TW1_original_item_PNG_candidates']
  self.assertEqual(len(icons),2)
  self.assertEqual({p.split('alias-')[-1].split('.')[0] for p in icons},{'24176','24177'})
  self.assertTrue(all(re.fullmatch('[0-9a-f]{64}',v['sha256']) for v in icons.values()))

 def test_negative_mismatches_and_rights_boundary(self):
  e=self.v['counterexamples'];self.assertEqual(len(e),2)
  self.assertEqual(e[0]['literal_handler'],'genout/ss_130_3_14');self.assertEqual(e[0]['create_xy'],[1,14])
  self.assertEqual(e[1]['literal_handler'],'genout/pis_1009_14_13');self.assertEqual(e[1]['create_floor'],130)
  self.assertTrue(all(x['not_autocorrected'] for x in e))
  self.assertFalse(any(self.v['limitations'].values()))

if __name__=='__main__':unittest.main()
