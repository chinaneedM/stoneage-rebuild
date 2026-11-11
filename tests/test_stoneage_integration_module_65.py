"""INTEGRATION65 public-only SHA/numeric crosswalk; no commercial script, image or server execution."""
from __future__ import annotations
import json, re, unittest
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]/'research'/'recovered'
REPORT=ROOT/'STONEAGE-INTEGRATION65-GENOU-THREE-SCRIPTS-25-ITEMS-18-TW1-CANDIDATES-R1.json'
Q01=ROOT/'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
Q22=ROOT/'STONEAGE-QUEST22-HEKISEI-ORIGINAL-SOURCE-AND-THREE-SCENES-R1.json'
ITEM=[ROOT/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json' for i in (1,2)]
MAP=ROOT/'STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
HEX=re.compile(r'^[0-9a-f]{64}$')

class TestGenouOriginalSourceBridge(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(REPORT.read_text(encoding='utf8'))
  cls.q=json.loads(Q01.read_text(encoding='utf8'))
  cls.quest22=json.loads(Q22.read_text(encoding='utf8'))
  cls.item={a[0]:a for p in ITEM for a in json.loads(p.read_text(encoding='utf8'))['rows']}
  cls.map=json.loads(MAP.read_text(encoding='utf8'))['maps']

 def test_01_four_original_scripts_in_quest01_exact_provenance(self):
  r=self.r; q={x['path']:x for x in self.q['source_scripts']}
  self.assertEqual(len(r['scripts']),4)
  self.assertEqual([x['source_path'] for x in r['scripts']], [f'sainasu/event/genou_{n}' for n in range(1,5)])
  for x in r['scripts']:
   y=q[x['source_path']]
   self.assertEqual((x['original_sha256'],x['original_byte_length'],x['original_crc32']),
    (y['original_sha256'],y['original_size'],y['original_crc32']))
   self.assertTrue(HEX.fullmatch(x['original_sha256']))
  self.assertTrue(r['scripts'][0]['previous_QUEST22_genou1_context_only'])
  self.assertEqual(sum(x['previous_QUEST22_genou1_context_only'] for x in r['scripts']),1)
  self.assertIn('genou_1',json.dumps(self.quest22,ensure_ascii=False))
  self.assertEqual(r['derived']['new_subject_source_scripts'],3)

 def test_02_five_source_CREATE_references_match_quest01(self):
  src=self.r['original_create']; q=self.q['source_creation_references']
  self.assertEqual(src['original_sha256'],'d94613df0dc41560459cd99f1cb052d006c7310448c62285949768849cd6f874')
  self.assertEqual(len(src['records']),5)
  self.assertEqual([x['source_script'].split('_')[-1] for x in src['records']],['1','2','2','3','4'])
  self.assertEqual([x['floorid'] for x in src['records']],[11215,11215,11215,100,11206])
  self.assertEqual([x['borncorner_4_literals'][:2] for x in src['records']],[[10,10],[13,11],[7,11],[346,356],[5,36]])
  self.assertEqual([x['source_graphic_alias'] for x in src['records']],[100461,100446,100446,100110,16306])
  for x in src['records']:
   rows=[a for a in q if a['create_source_path']==src['path'] and a['create_brace_ordinal']==x['source_create_brace_ordinal']]
   self.assertEqual(len(rows),1)
   y=rows[0]
   self.assertEqual((y['create_source_sha'],y['original_script_path'],y['floorid'],y['graphic_alias_numeric']),
     (src['original_sha256'],x['source_script'],x['floorid'],x['source_graphic_alias']))
   self.assertEqual(y['origin_class'],'UNRESOLVED')

 def test_03_sixteen_real_TYPE_sections_with_eleventh_new(self):
  q=self.q['source_event_blocks'];total=0
  for script in self.r['scripts']:
   xs=script['TYPE_sections']; ys=[a for a in q if a['script_path']==script['source_path']]
   self.assertEqual(len(xs),len(ys))
   total+=len(xs)
   for i,(x,y) in enumerate(zip(xs,ys)):
    self.assertEqual((x['ordinal'],x['type'],x['source_type_line_1based'],int(x['event_number_literal'])),
      (y['script_block_ordinal'],y['raw_type'],y['source_type_line'],y['event_number']))
    self.assertTrue(HEX.fullmatch(x['original_event_section_CP950_raw_sha256']))
  self.assertEqual(total,16)
  self.assertEqual(self.r['derived']['new_subject_TYPE_count'],11)

 def test_04_three_distinct_source_accepts_and_literal_preconditions(self):
  s=self.r['scripts'][1]['TYPE_sections']
  self.assertEqual([x['type'] for x in s], ['ACCEPT']*3+['MESSAGE']*3)
  self.assertEqual([x['commands']['DelPet'] for x in s[:3]],[['PET>59-95*1'],['PET>42-95*1'],['PET>0-95*1']])
  self.assertTrue(all(x['commands']['DelItem']==['2758'] for x in s[:3]))
  self.assertIn('ITEM=2758LV>0',s[0]['commands']['EVENT'][0])
  self.assertIn('PET>60-95',s[0]['commands']['EVENT'][0])
  self.assertIn('PET>59-95',s[0]['commands']['EVENT'][0])
  self.assertTrue(self.r['derived']['genou_2_first_predicate_bad_join_2758LV0_literal'])
  self.assertTrue(self.r['derived']['genou_2_pet_predicate_and_DelPet_do_not_match_in_first_branch'])

 def test_05_three_GetRandItem_lists_preserve_order_and_duplicates(self):
  d=self.r['derived'];s=self.r['scripts'][1]['TYPE_sections']
  seq=[[int(v) for v in x['commands']['GetRandItem'][0].split(',')] for x in s[:3]]
  self.assertEqual(seq,d['genou_2_raw_GetRandItem_sequences'])
  self.assertEqual([len(x) for x in seq],[8,13,14]);self.assertEqual(sum(map(len,seq)),35)
  self.assertEqual(len(set(v for a in seq for v in a)),24)
  self.assertEqual(d['genou_2_raw_GetRandItem_unique_IDs'],sorted(set(v for a in seq for v in a)))
  expected=[{},{'167':2,'271':2,'676':2,'872':2,'1175':2},
    {'71':2,'171':2,'372':2,'571':2,'772':2,'972':2}]
  self.assertEqual(d['genou_2_branch_duplicate_literal_counts'],expected)
  self.assertEqual([{str(k):v for k,v in Counter(a).items() if v>1} for a in seq],expected)
  self.assertFalse(self.r['limits']['GetRandItem_list_weights_or_probability_proven'])

 def test_06_genou4_item_2758_not_pretend_harp(self):
  d=self.r['derived']; four=self.r['scripts'][3]['TYPE_sections']
  self.assertEqual(four[0]['commands']['GetItem'],['2758*1'])
  self.assertEqual(four[1]['commands']['EVENT'],['ITEM=2758'])
  self.assertTrue(d['genou_4_source_comment_mentions_feng_zhishu_qin_while_item_master_says_bracelet'])
  self.assertEqual(d['original_2758_name_in_both_original_itemsets'],'風的手鐲 [風]')
  self.assertEqual(d['genou_2_three_branches_DelItem_literal'],'2758')

 def test_07_all_25_private_verified_item_row_sha_link_to_public_shards(self):
  rows=self.r['candidate_item_rows'];self.assertEqual(len(rows),25)
  ids=[a['item_id'] for a in rows];self.assertEqual(len(set(ids)),25)
  self.assertEqual(ids,sorted(set(self.r['derived']['genou_2_raw_GetRandItem_unique_IDs'])|{2758}))
  for x in rows:
   y=self.item[x['item_id']]
   self.assertEqual((y[1],y[2]),(x['original_CP950_original_row_SHA256'],)*2)
   self.assertEqual((y[3],y[4]),(x['original_image_alias_numeric'],)*2)
   self.assertEqual((y[5],y[6],y[7]),(x['original_cost_literal'],x['original_type_literal'],x['original_level_literal']))
   self.assertEqual((y[8],y[9]),('REAL_RD_DECODED_CROSS_CARRIER',)*2)
  self.assertEqual(next(a for a in rows if a['item_id']==2758)['original_image_alias_numeric'],22119)

 def test_08_exact_18_different_original_TW1_pixel_alias_candidates(self):
  rows=self.r['candidate_item_rows']; imgs=self.r['qualified_TW1_original_RD_pngs']
  aliases={a['original_image_alias_numeric'] for a in rows}
  self.assertEqual(len(rows),25)
  self.assertEqual(len(aliases),18)
  self.assertEqual({a['item_image_alias'] for a in imgs},aliases)
  self.assertEqual(len(imgs),18)
  for a in imgs:
   self.assertTrue(a['source_TW1_ADRN_index_unique'])
   self.assertTrue(all(HEX.fullmatch(a[k]) for k in ['original_RD_SHA256','private_PNG_SHA256','private_RGBA_SHA256']))
   self.assertGreater(a['original_RD_bytes'],0)
   self.assertGreater(a['private_PNG_width'],0)
   self.assertGreater(a['private_PNG_height'],0)
  self.assertEqual(self.r['derived']['distinct_original_TW1_pixel_alias_candidates'],18)

 def test_09_actual_MAP09_scene_scope_and_negative_floor100(self):
  creates=self.r['original_create']['records']
  self.assertEqual({int(k) for k in self.map.keys()}.intersection({100,11206,11215}),{11206,11215})
  self.assertEqual(self.map['11215']['geometry'],[20,20])
  self.assertEqual(self.map['11206']['geometry'],[60,60])
  for x in creates:
   if x['floorid'] in (11206,11215):
    w,h=self.map[str(x['floorid'])]['geometry']
    assert 0<=x['borncorner_4_literals'][0]<w and 0<=x['borncorner_4_literals'][1]<h
  self.assertFalse(self.r['derived']['original_scene_floor_100_MAP09_qualifies'])
  self.assertFalse(self.r['limits']['original_map_and_npc_rendering_executed'])

 def test_10_provenance_privacy_and_stage_gates(self):
  source=self.r['original_sources'];priv=self.r['private_custody'];limits=self.r['limits']
  self.assertEqual(source['NPC_zip_sha256'],'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
  self.assertEqual(source['ITEM_zip_sha256'],'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa')
  self.assertTrue(priv['all_member_CRC_verified']);self.assertTrue(HEX.fullmatch(priv['SHA256']))
  self.assertEqual(priv['private_members'],76)
  self.assertEqual((limits['stage_A'],limits['stage_B'],limits['wiki'],limits['R79'],limits['overall_percent']),
                  ('7_PARTIAL_2_OPEN','GATED','GATED','PAUSED_NON_BLOCKING',None))
  for k in ['original_server_executed','native_event_flag_or_predicate_semantics_proven','GetRandItem_list_weights_or_probability_proven','original_2758_received_or_exchanged_proven','TW1_retail_images_same_official_server_build_proven','early_JSS_or_TW1_quest_identity_proven']:
   self.assertFalse(limits[k],k)

if __name__=='__main__':unittest.main()
