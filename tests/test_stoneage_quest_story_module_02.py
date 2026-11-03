"""QUEST02 source-only, no private originals in GitHub CI."""
import json,hashlib,collections,re,unittest,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'research'/'recovered'
Q2=R/'STONEAGE-QUEST-STORY-MODULE-02-ORIGINAL-WARPMAN-CONDITION-SOURCE-R1.json'
Q1=R/'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
SHARDS=[R/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json' for i in range(1,8)]
HEX=re.compile(r'^[a-f0-9]{64}$')

def verify(j,q1,shards,q1raw=None):
 assert j['schema']=='stoneage.quest_story_module02_original_warp_condition_source_graph.r1'
 src=j['source'];assert (src['parent_RAR_bytes'],src['original_archive_members'],src['original_NPC_files_with_size_SHA_crc_replayed'],src['original_NPC_total_bytes'],src['CREATE_original_total_enemy_blocks'])==(361255180,7952,2205,1930332,4985)
 assert src['parent_RAR_sha256']==q1['source']['original_RAR_sha256']
 assert src['source_family_enemy_literal']=='npcgen_warpman'
 assert src['source_create_non_cp950_strict_fallback_files']==5 and src['original_script_cp950_non_strict_paths']==[]
 creates=j['source_create_references'];files=j['source_original_parameter_files'];blocks=j['source_control_segments']
 assert (len(creates),len(files),len(blocks))==(202,188,313)
 assert (j['source_create_reference_count'],j['distinct_original_warp_parameter_files'],j['source_segments_count'])==(202,188,313)
 assert j['original_script_total_bytes']==sum(f['original_size_bytes'] for f in files)==93110
 assert j['script_type_families']=={'NEWWARPMAN_HEADER':35,'UNMARKED_WARP_SOURCE':153}
 idByFile={f['original_path']:f for f in files};assert len(idByFile)==188
 refs=collections.Counter()
 for x in creates:
  assert x['origin']=='UNRESOLVED' and x['quest_status']=='NOT_PROVEN_QUEST'
  assert x['original_source_script_path'] in idByFile
  assert x['original_source_script_sha256']==idByFile[x['original_source_script_path']]['source_sha256']
  assert HEX.fullmatch(x['source_create_sha256']) and isinstance(x['source_create_brace_ordinal'],int)
  refs[x['original_source_script_path']]+=1
 assert sum(f['create_reference_count'] for f in files)==202
 for f in files:
  assert f['create_reference_count']==refs[f['original_path']]
  assert HEX.fullmatch(f['source_sha256']) and re.fullmatch('[a-f0-9]{8}',f['original_crc32'])
  assert f['origin']=='UNRESOLVED' and f['original_cp950_strict_decodable'] is True
  assert isinstance(f['raw_TALKEVENT_marker_count'],int)
 assert sum(x['raw_TALKEVENT_marker_count'] for x in files)==j['source_TALKEVENT_marker_count']==126
 assert sum(x['raw_NOFREE_lines'] for x in files)==j['source_NOFREE_marker_count']
 assert sum(x['raw_OVER_lines'] for x in files)==j['source_OVER_marker_count']
 sByFile=collections.Counter();keywords=collections.Counter();itemids=set();warps=[];npcpoints=[];flags=set();seen=set();frees=0
 for x in blocks:
  key=(x['script_path'],x['source_segment_ordinal'])
  assert key not in seen;seen.add(key)
  assert x['script_path'] in idByFile
  assert x['original_file_sha256']==idByFile[x['script_path']]['source_sha256']
  assert x['status']=='STATIC_SOURCE_ONLY_UNRESOLVED_ORIGIN'
  assert HEX.fullmatch(x['source_segment_decoded_cp950_utf8_sha256']) and HEX.fullmatch(x['original_FREE_decoded_cp950_utf8_sha256'])
  assert x['source_header_marker']=='PLAIN' or x['source_header_marker']=='PLAIN_PREFIX' or re.fullmatch('TALKEVENT[0-9]+|NOFREE',x['source_header_marker'])
  assert x['source_closing_OVER_count']>=0
  assert x['original_FREE_line_count']>=0
  keywords.update(x['source_condition_keywords']);frees+=x['original_FREE_line_count']
  warps.extend(x['source_warp_coordinate_triples']);npcpoints.extend(x['source_NPCPOINT_coordinate_triples'])
  for p in x['source_warp_coordinate_triples']+x['source_NPCPOINT_coordinate_triples']:
   assert len(p)==3 and all(isinstance(n,int) for n in p)
  for k,vals in x['source_item_numbers_by_operation'].items():
   assert k in ('condition_ITEM','AddItem','DelItem','GetItem') and vals==sorted(set(vals))
   itemids.update(vals)
  for s in x['source_NOWEV_number_values']+x['source_ENDEV_number_values']:
   if s>=0:flags.add(s)
  sByFile[x['script_path']]+=1
 assert all(f['segment_count']==sByFile[f['original_path']] for f in files)
 assert frees==j['source_FREE_conditional_count']==313
 assert len(warps)==j['source_WARP_triples_count']==249
 assert sum(p==[0,0,0] for p in warps)==j['source_WARP_all_zero_triples_count']==43
 assert len(npcpoints)==j['source_NPCPOINT_triples_count']==26
 assert sorted({p[0] for p in warps})==j['source_WARP_destination_floor_numbers']
 assert len(j['source_WARP_destination_floor_numbers'])==102
 assert len({c['floor_id'] for c in creates if c['floor_id'] is not None})==j['source_qualifying_create_origins_distinct_floors']
 assert dict(sorted(keywords.items()))==j['source_condition_token_occurrences']
 assert flags==set(j['static_positive_flag_reference_numbers']) and len(flags)==17
 bridge=j['source_state_number_overlap_QUEST01']
 if q1raw is not None:
  assert hashlib.sha256(q1raw.rstrip(b'\n')).hexdigest()==bridge['reference_QUEST01_public_report_sha256']
 assert bridge['overlap_nonnegative_EventNo_literals']==sorted(flags&set(q1['actual_original_event_number_value_list']))
 assert bridge['overlap_EndSetFlg_target_literals']==sorted(flags&{e[1] for e in q1['literal_EndSetFlg_number_pairs']})
 assert len(bridge['overlap_nonnegative_EventNo_literals'])==15
 assert len(bridge['overlap_EndSetFlg_target_literals'])==16
 assert bridge['overlap_not_proof_same_runtime'] is True
 oldids=set();ids=set()
 for sh in shards:
  for row in sh['rows']:
   ids.add(row[0]);
   if row[1] is not None:oldids.add(row[0])
 assert len(oldids)==13254 and len(ids)==13915
 rr=j['source_numeric_item_reference_summary']
 assert len(itemids)==rr['distinct_id_count']==62
 assert sorted(itemids&oldids)==rr['in_both_itemsets'] and len(rr['in_both_itemsets'])==61
 assert sorted(itemids&(ids-oldids))==rr['only_in_later_itemset']==[20296]
 assert sorted(itemids-ids)==rr['missing_in_both_itemsets']==[]
 bounds=j['bounds']
 for k in ('source_WARP_triples_not_proven_original_successful_transition','source_TALKEVENT_not_a_count_of_quests','NPCPOINT_not_a_runtime_spawn_travel_trace','event_state_number_overlap_not_same_quest_proof','source_202_create_references_all_origin_UNRESOLVED'):
  assert bounds[k] is True
 for k in ('original_game_natively_executed','same_official_TW10_or_CN182_deployment_proven','all_quest_population_complete','commercial_original_text_or_art_in_public_Git'):
  assert bounds[k] is False
 assert bounds['stage_A']=='7_PARTIAL_2_OPEN' and bounds['stage_B_and_wiki']=='GATED' and bounds['R79']=='PAUSED_NON_BLOCKING' and bounds['overall_percent'] is None
 assert j['next'].startswith('QUEST_STORY_MODULE_03')
 return True

class Quest02SourceChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=json.loads(Q2.read_text('utf-8'));cls.q1=json.loads(Q1.read_text('utf-8'))
  cls.shards=[json.loads(f.read_text('utf-8')) for f in SHARDS]
  cls.raw=Q1.read_bytes()
 def test_complete_202_188_313_source_graph(self):self.assertTrue(verify(self.a,self.q1,self.shards,self.raw))
 def test_claim_warp_exec_rejected(self):
  j=copy.deepcopy(self.a);j['bounds']['original_game_natively_executed']=True
  with self.assertRaises(AssertionError):verify(j,self.q1,self.shards,self.raw)
 def test_false_npc_quest_promotion_rejected(self):
  j=copy.deepcopy(self.a);j['source_create_references'][0]['quest_status']='OFFICIAL_PERMANENT_QUEST'
  with self.assertRaises(AssertionError):verify(j,self.q1,self.shards,self.raw)
 def test_fake_event_state_overlap_rejected(self):
  j=copy.deepcopy(self.a);j['source_state_number_overlap_QUEST01']['overlap_nonnegative_EventNo_literals'].append(999)
  with self.assertRaises(AssertionError):verify(j,self.q1,self.shards,self.raw)
 def test_riding_item_not_assigned_to_early_source(self):
  j=copy.deepcopy(self.a);j['source_numeric_item_reference_summary']['only_in_later_itemset']=[]
  with self.assertRaises(AssertionError):verify(j,self.q1,self.shards,self.raw)
 def test_zero_warp_not_inferred_success(self):
  j=copy.deepcopy(self.a);j['source_WARP_all_zero_triples_count']=0
  with self.assertRaises(AssertionError):verify(j,self.q1,self.shards,self.raw)
 def test_talkevent_not_a_quest_count(self):
  j=copy.deepcopy(self.a);j['bounds']['source_TALKEVENT_not_a_count_of_quests']=False
  with self.assertRaises(AssertionError):verify(j,self.q1,self.shards,self.raw)
 def test_source_warp_document_fabrication_rejected(self):
  j=copy.deepcopy(self.a);j['source_control_segments'][0]['source_warp_coordinate_triples'].append([999,999,999])
  with self.assertRaises(AssertionError):verify(j,self.q1,self.shards,self.raw)
if __name__=='__main__':unittest.main()