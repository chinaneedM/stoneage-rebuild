"""INTEGRATION75 static source provenance and negative scope, not original client/server execution."""
import copy,json,pathlib,collections,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered/STONEAGE-INTEGRATION75-MAMMOTH-SHRINE-SIX-FORTUNES-SOURCE-R1.json'
SHARD=ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def validate(r):
 assert r['schema']=='stoneage.integration75.mammoth_shrine_omikuji_source_bound.r1'
 assert r['baseline']['current_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
 assert r['baseline']['current_bytes']==2709173
 n=r['private_npc']
 assert n['archive_sha256']=='c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
 assert n['verified_members']==n['crc_ok']==2205
 assert len(n['files'])==4
 assert [f[1] for f in n['files']]==[1041,1044,681,681]
 assert [f[3] for f in n['files']]==[['MESSAGE','ACCEPT','MESSAGE']]*2+[['CLEAN','REQUEST']]*2
 assert n['files'][2][2]==n['files'][3][2] and n['files'][0][2]!=n['files'][1][2]
 assert n['limited_create_template_arg_conf_gen_scan_files']==578 and n['limited_scan_literal_hits']==0
 c=r['script_contract']
 assert len(c['draw_list'])==15
 assert c['draw_occurrence_counts']==[[2615,1],[2616,2],[2617,4],[2618,5],[2619,2],[2620,1]]
 assert sorted([list(a) for a in collections.Counter(c['draw_list']).items()])==c['draw_occurrence_counts']
 assert c['flag_event_number']==36 and c['draw_script_command']=='EndSetFlg:36'
 assert c['donation_script_commands']==['CleanFlg:36','DelStone:50']
 assert c['source_dialogue_mentions_once_per_day_but_runtime_reset_unproven']
 assert c['source_list_occurrences_not_runtime_probabilities']
 i=r['item_source']
 assert i['private_catalog_zip_sha256']=='cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
 assert i['crc_ok']==838 and i['old_original_parent_master_files_not_re_read_this_turn']
 assert i['ids']==list(range(2615,2621))
 assert i['source_A_1based_rows']==list(range(2198,2204))
 assert i['source_B_1based_rows']==list(range(2593,2599))
 assert len(set(i['both_table_exact_row_sha256']))==6 and all(len(h)==64 for h in i['both_table_exact_row_sha256'])
 assert i['shared_source_image_alias']==24313 and i['tw1_image_qualification']=='TW1_INDEX_NOT_FOUND'
 assert i['new_original_RD_or_PNG_in_this_turn']==0
 assert all(v is False for v in r['evidence_limits'].values())
 assert (r['stage']['A_PARTIAL'],r['stage']['A_OPEN'])==(7,2)
 assert r['stage']['overall_percent'] is None
 return True
class TestMammothShrine(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=load(REC);cls.shard=load(SHARD)
 def test_source_scope(self):self.assertTrue(validate(self.r))
 def test_replay_existing_original_item01_source_rows(self):
  s=self.shard;r=self.r['item_source']
  self.assertEqual(s['source_itemset_rows_sha256_provenance'],r['original_master_A_sha256'])
  self.assertEqual(s['source_itemset0710_rows_sha256_provenance'],r['original_master_B_sha256'])
  idx={x[0]:x for x in s['rows']}
  for iid,h in zip(r['ids'],r['both_table_exact_row_sha256']):
   row=idx[iid]
   self.assertEqual(row[1:5],[h,h,24313,24313])
   self.assertEqual(row[8:11],['TW1_INDEX_NOT_FOUND','TW1_INDEX_NOT_FOUND',[]])
 def reject(self,mutate):
  x=copy.deepcopy(self.r);mutate(x)
  with self.assertRaises(AssertionError):validate(x)
 def test_negative_invent_uniform_list(self):self.reject(lambda x:x['script_contract'].update(draw_occurrence_counts=[[i,1] for i in range(2615,2621)]))
 def test_negative_invent_pixel(self):self.reject(lambda x:x['item_source'].update(new_original_RD_or_PNG_in_this_turn=1))
 def test_negative_promote_daily_flag_runtime(self):self.reject(lambda x:x['evidence_limits'].update(daily_flag_reset_proven=True))
 def test_negative_fake_original_loader(self):self.reject(lambda x:x['evidence_limits'].update(original_CREATE_or_loader_reference_found_in_scanned_subset=True))
 def test_negative_change_original_duplicate_script(self):self.reject(lambda x:x['private_npc']['files'][3].__setitem__(2,'0'*64))
 def test_negative_invent_probability(self):self.reject(lambda x:x['script_contract'].update(source_list_occurrences_not_runtime_probabilities=False))
 def test_negative_publish_original_script(self):self.reject(lambda x:x['evidence_limits'].update(original_full_scripts_or_full_itemrows_published=True))
if __name__=='__main__':unittest.main()
