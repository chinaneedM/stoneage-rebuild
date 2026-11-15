"""INTEGRATION120 public-only source-conservation tests; private commercial bytes excluded."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
P=REC/'STONEAGE-INTEGRATION120-ORE-RESEARCHER-17-BRANCH-2-REAL-RD-R1.json'
W=REC/'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-SOURCE-R1.json'
ITEM=REC/'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'
HEX=re.compile(r'^[0-9a-f]{64}$')
class PublicBoundedOreResearcher(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=json.loads(P.read_text());cls.w=json.loads(W.read_text())
  cls.src=cls.p['original_community_mixed25'];cls.events=cls.src['events']
  cls.i=cls.p['original_community_two_itemsets']
 def test_01_source_real_hashes_and_single_original_create(self):
  x=next(v for v in self.w['source_scripts'] if v['path']==self.src['original_source_parameter_path'])
  self.assertEqual(x['source_sha256'],self.src['original_source_parameter_sha256'])
  self.assertEqual(x['source_bytes'],6304)
  self.assertEqual(len(x['exact_create_refs']),1)
  c=x['exact_create_refs'][0]
  self.assertEqual((c['create_path'],c['block_ordinal'],c['block_sha256']),('genout/1200npc_m.create',0,self.src['create_block_sha256']))
  self.assertEqual((c['floorid'],c['graphic_literal'],c['borncorner']),(2000,16209,[87,95,87,95]))
  self.assertRegex(self.src['original_create_SHA256'],HEX)
  self.assertEqual(self.src['source_npc_zip_size'],995176)
  self.assertEqual(self.src['zip_members_crc_verified'],2205)
 def test_02_original_17_branches_and_no_invented_runtime(self):
  self.assertEqual(len(self.events),17)
  self.assertEqual([e['ordinal'] for e in self.events],list(range(17)))
  self.assertEqual([e['type'] for e in self.events],['REQUEST','MESSAGE']+['ACCEPT']*15)
  self.assertEqual(self.events[0]['getItem'],2785)
  self.assertEqual(self.events[0]['predicate'],'LV>29&ENDEV=4&ITEM!=2785&ITEM!=2786')
  self.assertEqual(self.events[1]['predicate'],'LV>29&ENDEV=4&ITEM=2785&ITEM!=2786')
  self.assertEqual([e['predicate'] for e in self.events[2:16]],['ITEM=2785&ITEM=2786*'+str(n) for n in range(14,0,-1)])
  self.assertEqual(self.events[-1]['predicate'],'ITEM!=2785&ITEM=2786')
  self.assertEqual(self.events[-1]['delItem'],[2786])
  self.assertEqual(sum('getStone' in e for e in self.events),15)
 def test_03_rewards_already_in_world22_not_falsely_new(self):
  x=next(v for v in self.w['source_scripts'] if v['path']==self.src['original_source_parameter_path'])
  rewards=[e['getStone'] for e in self.events[2:]]
  self.assertEqual(rewards,[50000,30000,20000,15000,10000,9000,8000,7000,6000,5000,4000,3000,2000,1000,1000])
  self.assertEqual(rewards,[v['amount']['integer'] for v in x['branches']])
  self.assertEqual([e['delItem'] for e in self.events[2:16]],[[2785,2786]]*14)
  self.assertTrue(self.p['incremental_scope']['previous_world22_same_15_currency_fields_already_published'])
  self.assertEqual(self.p['incremental_scope']['new_source_script_files_discovered'],0)
  self.assertEqual(self.p['incremental_scope']['new_original_RD_bitmap_source_discovered'],0)
 def test_04_two_item_rows_share_sha_but_crosscarrier_art_not_official(self):
  z=json.loads(ITEM.read_text());rows={v[0]:v for v in z['rows']}
  self.assertEqual([v['id'] for v in self.i['items']],[2785,2786])
  self.assertEqual(self.i['zip_members_crc_verified'],838)
  for v in self.i['items']:
   row=rows[v['id']]
   self.assertEqual(row[1],row[2])
   self.assertEqual(row[1],v['source_94col_row_sha256'])
   self.assertEqual(row[3],row[4])
   self.assertEqual(row[3],v['image_alias'])
   self.assertEqual([row[8],row[9]],['REAL_RD_DECODED_CROSS_CARRIER']*2)
   for k in ['retail_original_RD_sha256','retail_original_indexed_pixels_sha256','private_PNG_sha256']:self.assertRegex(v[k],HEX)
  self.assertEqual([(v['width'],v['height']) for v in self.i['items']],[(28,39),(24,23)])
  self.assertEqual(self.p['authenticated_retail_tw1_independent']['newly_decoded_in_this_unit'],0)
 def test_05_private_roundtrip_and_no_public_binary_leak(self):
  z=self.p['private_artifact']
  self.assertEqual((z['size_bytes'],z['members_crc_passed']),(8490,6))
  self.assertEqual(z['sha256'],'87cdc57f305e997884f8ef141bddf8702228cddf3f7e1363d6ca2b8bce62cc97')
  self.assertTrue(z['personal_Library_uploaded_and_independently_read_back_SHA_CRC'])
  self.assertFalse(z['HTML_in_browser_executed'])
  self.assertTrue(self.p['historical_limits']['no_original_proprietary_bytes_or_images_in_public_Git'])
  self.assertNotIn('raw_original_CP950_text',self.p)
  self.assertNotIn('original_PNG_base64',self.p)
 def test_06_no_native_upgrade_and_history_preserved(self):
  h=self.p['historical_limits']
  for k in ['later_community_NPC_and_itemsets_certified_official_tw1_same_deployment','native_NPC_script_executed','original_CLIENT_executed','official_item_graphic_selector_proven','original_palette_and_alpha_proven','original_currency_payment_proven','original_event_condition_priority_proven']:
   self.assertIs(h[k],False)
  self.assertEqual(self.p['starting_remote']['preserved_historical_current_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
  self.assertEqual(h['source_project_StageA'],'7 PARTIAL + 2 OPEN')
  self.assertEqual(h['StageB_and_wiki'],'GATED')
  self.assertEqual(h['R79'],'PAUSED_NON_BLOCKING')
  self.assertIsNone(h['overall_percent'])
if __name__=='__main__':unittest.main()
