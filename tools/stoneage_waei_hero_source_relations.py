"""Compare two accepted derived sources without merging historical entities."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tools.stoneage_early_content_probe import require

INPUTS=[
 ('research/recovered/STONEAGE-WAEI-CN20-ISLAND-HERO-CONTENT-R1.json','4fef4edbb48e837fb49cdcab7faf801040b5d2dfcab7c1ec03e4f8bfc786fe77'),
 ('research/recovered/STONEAGE-WORLD-NPC-QUEST-CATALOG-R1.json','ac402f48c7045f431d0e68a48c7c3513d283f19704f3cf6bd90c3d3a773e576e')]
REPORT=Path('research/recovered/STONEAGE-WAEI-HERO-GUIDE-SOURCE-RELATIONS-R1.json')
BOUNDARIES={'same_npc_item_quest_or_exact_build_verified':False,'coordinate_offset_or_interaction_radius_derived':False,
 'no_item_atoms_means_unconditional_gift':False,'fish_birth_predicate_recovered_from_config':False,
 'same_host_or_names_make_independent_witnesses':False,'black_wuli_absent_from_entire_descendant_bundle_proven':False,
 'original_runtime_or_complete_quest_restored':False,'new_original_network_requests':0,'new_images_or_program_requests':0,
 'new_game_entities':0,'automatic_design_adoption':False,'stage_a':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'}


def read_inputs(blobs):
 require(len(blobs)==2,'Exactly two fixed derived inputs required')
 for blob,(path,pin) in zip(blobs,INPUTS):require(sha256(blob).hexdigest()==pin,'Fixed derived input differs: '+path)
 return [json.loads(b) for b in blobs]


def relation_values(a,b):
 g=a['records'][5]['source_qualified_guide']
 require(b['version_profile']=='RECOVERED25' and len(b['npcs'])==2 and len(b['event_records'])==6,'Selected descendant catalog contract differs')
 yayoi,himiko=b['npcs'];exchange=b['event_records'][1];direct=b['event_records'][2];reverse=b['event_records'][4]
 require(yayoi['label']=='彌生' and himiko['label']=='日美子' and exchange['source_record_ordinal']==1
         and direct['source_record_ordinal']==2,'Actual NPC/event sample order differs')
 return [
  ('HOSTED_REGIONAL_NOTICE_VS_UNPROVEN_DESCENDANT_BUILD', ['/records/5/source_qualified_guide'],['/version_profile'],
   {'host_region':g['publication_host_region'],'hosted_notice':g['regional_notice_as_written'],
    'guide_exact_taiwan_build':g['exact_taiwan_client_build'],'other_source_profile':b['version_profile'],
    'same_official_release_or_build':None}),
  ('LEXICAL_ACTORS_WITH_DIFFERENT_LOCATORS', ['/records/6','/records/7'],['/npcs/0','/npcs/1'],
   {'guide_npcs':[{'label':s['npc_label'],'locator':s['coordinate_string_as_written']} for s in g['steps'][:2]],
    'descendant_npcs':[{'label':n['label'],'configured_map_id':n['map_id'],'borncorner':n['spawn_geometry'][0]['values']} for n in [himiko,yayoi]],
    'guide_locators_equal_descendant_borncorner':False,'offset_map_or_same_entity':None}),
  ('EXCHANGE_DIRECTION_RESEMBLANCE_NOT_ITEM_IDENTITY', ['/records/5/source_qualified_guide/steps/1'],['/event_records/1','/items'],
   {'guide_handoff':'未具名花→弥生→不可思议的贝','descendant_exchange_actions':exchange['actions'],
    'descendant_item_labels':[{'id':i['item_id'],'label':i['label']} for i in b['items']],
    'interpretation':'SOURCE_DESCRIBED_DIRECTION_RESEMBLANCE_ONLY',
    'guide_flower_equals_item_2415':None,'guide_shell_equals_item_2414':None}),
  ('BIRTH_EXCEPTION_NOT_RECOVERED_FROM_MISSING_ITEM_ATOMS', ['/records/5/source_qualified_guide/birth_routes','/records/5/source_qualified_guide/prerequisites'],['/event_records/2'],
   {'guide_birth_routes':g['birth_routes'],'guide_prerequisites':g['prerequisites'],
    'descendant_direct_actions':direct['actions'],'descendant_item_atoms':direct['item_predicate_atoms'],
    'descendant_complete_condition':direct['complete_boolean_condition'],
    'source_described_fish_route_proves_descendant_birth_condition':False,
    'zero_item_atoms_proves_unconditional_or_no_level_requirement':False}),
  ('THIRD_NPC_ACCESS_BEYOND_SELECTED_TWO_NPC_CONFIG_SAMPLE', ['/records/5/source_qualified_guide/steps/2'],['/npcs','/coverage_stop'],
   {'guide_third_step':g['steps'][2],'descendant_selected_npc_labels':[n['label'] for n in b['npcs']],
    'black_wuli_missing_from_entire_bundle_or_game_proven':False,
    'shell_check_or_consumption_at_hero_entry_verified':False}),
  ('ONE_DELIVERY_LEG_DOES_NOT_REVOKE_OPPOSITE_CONFIG_OR_FINAL_REWARD_LIMIT', ['/records/5/source_qualified_guide/steps'],['/event_records/4','/guide_profiles/compilation','/intermediate_object_equals_final_reward'],
   {'guide_step2_received_label':g['steps'][1]['received_item_label_as_written'],
    'guide_step3_destination':g['steps'][2]['destination_label_as_written'],
    'descendant_reverse_actions':reverse['actions'],'prior_compilation_flow':b['guide_profiles']['compilation']['flow'],
    'new_guide_claims_complete_all_deliveries_or_final_reward_table':False,
    'opposite_direction_is_contradiction_or_patch_order_proven':False,
    'guide_pet_exp_reward_or_same_master_ids':None})]


def expected_records(a,b):
 records=[]
 for i,(kind,ap,bp,values) in enumerate(relation_values(a,b),1):
  records.append({'record_id':f'waei-hero:source-relation:{i:02d}','collection':'sources',
   'entity_type':'SOURCE_RELATION_NOT_NEW_GAME_ENTITY','record_revision':1,
   'version_profile':'CN_HOST_TW_CLAIM_GUIDE_VS_LATER_RECOVERED25_NOT_SAME_BUILD',
   'source_refs':[{'path':path,'sha256':pin,'json_pointers':ps} for (path,pin),ps in zip(INPUTS,[ap,bp])],
   'verification_status':'PINNED_DERIVED_SOURCE_COMPARISON_NOT_ORIGINAL_RUNTIME',
   'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','relation_type':kind,'source_scoped_values':values,
   'game_entity_identity_or_new_rule':None})
 return records


def validate_report(o,blobs=None):
 a,b=read_inputs([Path(p).read_bytes() for p,_ in INPUTS] if blobs is None else blobs)
 require(o['records']==expected_records(a,b),'Source facts, pointers or relationship boundaries changed')
 require(o['boundaries']==BOUNDARIES,'Source comparison promoted to runtime or same entity')
 require(o['coverage']=={'fixed_derived_inputs':2,'source_relations':6,'new_original_bodies':0,'new_images':0,'new_game_entities':0},'Comparison counts inflated')
 require(o['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17','Finite return to whole-project queue required')
 # Check every permanent pointer actually resolves in its pinned source.
 for r in o['records']:
  for ref,source in zip(r['source_refs'],[a,b]):
   for pointer in ref['json_pointers']:
    node=source
    for token in pointer.lstrip('/').split('/'):
     token=token.replace('~1','/').replace('~0','~');node=node[int(token)] if isinstance(node,list) else node[token]


def build(blobs):
 a,b=read_inputs(blobs)
 o={'schema':'stoneage.waei.hero_guide_source_relations.r1','date':'2026-10-19','task':'CN20-HERO-GUIDE-SOURCE-RELATIONS-01',
    'records':expected_records(a,b),'boundaries':deepcopy(BOUNDARIES),
    'coverage':{'fixed_derived_inputs':2,'source_relations':6,'new_original_bodies':0,'new_images':0,'new_game_entities':0},
    'finite_outcome':'SOURCE_RELATIONS_CLOSED_SAME_BUILD_IDENTITY_AND_FULL_QUEST_OPEN',
    'next':'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17'}
 validate_report(o,blobs);return o


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
 o=build([Path(path).read_bytes() for path,_ in INPUTS]);payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
 print('FIXED_INPUTS=2 RELATIONS=6 NEW_ORIGINALS=0 NEW_ENTITIES=0')
 print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
