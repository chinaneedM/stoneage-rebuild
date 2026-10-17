"""Reproducible finite world/NPC/event/item reference records for preproduction.

A typed static relation is not a completed quest, satisfied condition or runtime
transaction. No guide coordinate is promoted to a source spawn coordinate.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW='research/recovered/STONEAGE-WORLD-NPC-QUEST-SOURCE-JOIN-R1.json'
WITNESS='research/recovered/STONEAGE-WORLD-NPC-QUEST-WITNESSES-R1.json'
CATALOG='research/recovered/STONEAGE-WORLD-NPC-QUEST-CATALOG-R1.json'
PINS={'research/recovered/STONEAGE-WORLD-NPC-QUEST-SOURCE-JOIN-R1.json': '86d4ae760aaa7028832c9d38229e0e1c5d4dfaaf', 'research/recovered/STONEAGE-WORLD-NPC-QUEST-WITNESSES-R1.json': 'cb7ed90fc6f3678ea7ca5bce3900ba0dee10128a', 'tools/stoneage_world_npc_quest_join_probe.py': 'eeb635edf71e43a4c7d0dd984c1385bb06ed05a3', 'tools/stoneage_npc_world_graph_probe.py': 'a835914d2d02350d4e1ea8561a348d4f03860994', 'tools/stoneage_transport_usage_probe.py': '5936601a83201b96145c50a5d380969a1ea5b670', 'tools/stoneage_quest_npc_item_binding_probe.py': '0f5e49885965955201c6a480cc1b383d912100c8', 'tools/stoneage_itemset_schema_probe.py': '7a0e41c409d3f2dc18953cc79947612f5d9ed5d4', 'tools/stoneage_quest_item_identity_probe.py': '275ff890b1f1029b1c1617540438ba0c0eee79d5', 'research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json': 'e39a3a6020b578da017ab0bfa9369dc083e0b700'}
PUBLIC_ITEM_TERMS={2414:'不可思議的貝殼',2415:'仙尼亞的花'}
NAMES={'YAYOI':'彌生','HIMIKO':'日美子'}

def need(ok,msg):
 if not ok:raise ValueError(msg)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def source_pins():
 for f,p in PINS.items():need(blob((ROOT/f).read_bytes())==p,'source changed: '+f)

def public_item_identity(row):
 item_id=row['numeric_fields']['id'];name=PUBLIC_ITEM_TERMS.get(item_id)
 need(name is not None and hashlib.sha256(name.encode('big5')).hexdigest()==row['name_sha256'],'exact public term/name-byte fingerprint mismatch')
 return {'item_id':item_id,'label':name,'name_evidence':'EXACT_BIG5_PUBLIC_QUERY_SHA256_MATCH',
  'source_row_sha256':row['row_sha256'],'source_physical_line':row['physical_line'],
  'numeric_fields':row['numeric_fields'],'tw10_same_item_id':None,
  'runtime_lifetime_or_shop_price_verified':False}

def build_catalog():
 source_pins();r=json.loads((ROOT/RAW).read_text());w=json.loads((ROOT/WITNESS).read_text())
 need(r['source_profile']=='LATER_RECOVERED25' and r['source_bundle_sha256']=='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5','source version')
 need(r['counts']=={'all_enemy_references':4985,'argument_MISSING_FILE':15,'unresolved_or_ambiguous_templates':30},'scope census')
 need(r['selected_item_ids']==[2414,2415],'item join scope')
 active=r['item_master_joins']['tables']['itemset.txt'];need(active['selected_by_setup'] is True,'active item table')
 inactive=r['item_master_joins']['tables']['itemset0710.txt'];need(inactive['selected_by_setup'] is False,'do not merge inactive revision')
 items=[public_item_identity(x)for x in active['joined_rows']]
 npcs=[];relations=[];events=[];maps=set()
 for p in r['selected_placements']:
  roles={m['query_role']for m in p['exact_name_matches']}
  need(len(roles)==1 and p['identity_evidence']=='EXACT_NAME_FIELD','a mere mention cannot identify an NPC')
  role=next(iter(roles));need(p['map_header_exists']is True and p['functionset']=='ExChangeMan','world/function source link')
  node='RECOVERED25:NPC:'+p['placement_key'];maps.add(p['floor_id'])
  npcs.append({'record_id':node,'public_name_query_role':role,'label':NAMES[role],
   'name_evidence':p['exact_name_matches'],'version_profile':'RECOVERED25','historical_server_npc_id':None,
   'map_id':p['floor_id'],'spawn_geometry':p['spawn_geometry'],'current_position_observed':False,
   'source_create_sha256':p['create_file_sha256'],'source_parameter_sha256':p['parameter_sha256'],
   'historical_guide_npc_identity_proven':False})
  relations.append({'kind':'MAP_HAS_CONFIGURED_NPC','from':f"RECOVERED25:MAP:{p['floor_id']}",'to':node,'runtime_verified':False})
  for e in p['event_records']:
   ev='RECOVERED25:EVENT_RECORD:'+e['event_record_sha256']
   events.append({'record_id':ev,'source_record_ordinal':e['record_ordinal'],'actions':e['actions'],
      'item_predicate_atoms':e['item_predicates'],'complete_boolean_condition':None,
      'cross_record_order_verified':False,'condition_satisfiability_verified':False,
      'execution_verified':False,'durable_quest_state_verified':False})
   relations.append({'kind':'NPC_HAS_EVENT_RECORD','from':node,'to':ev,'runtime_verified':False})
   for a in e['actions']:
    for item in a['items']:
     need(item['id']in r['selected_item_ids'],'unjoined action item')
     relations.append({'kind':a['role'],'from':ev,'to':f"RECOVERED25:ITEM:{item['id']}",'quantity':item['quantity'],'runtime_verified':False})
   for a in e['item_predicates']:
    need(a['id']in r['selected_item_ids'],'unjoined predicate item')
    relations.append({'kind':'MENTIONS_ITEM_PREDICATE_ATOM','from':ev,'to':f"RECOVERED25:ITEM:{a['id']}",'comparison':a['comparison'],'quantity':a['quantity'],'runtime_verified':False})
 need(len(npcs)==2 and {n['public_name_query_role']for n in npcs}==set(NAMES),'named NPC scope')
 need(len(events)==6,'event record scope')
 return {'schema':'stoneage.preproduction.world_npc_quest.catalog.r1','source_git_blobs':PINS,
   'version_profile':'RECOVERED25','task_label':'弥生与日美子送贝壳：静态配置关联样本',
   'npcs':npcs,'maps':[{'record_id':f'RECOVERED25:MAP:{i}','map_id':i,'map_header_exists':True,'map_name_verified':None,'tw10_same_map':None}for i in sorted(maps)],
   'items':items,'event_records':events,'relations':relations,
   'guide_profiles':w['observations']['profiles'],'guide_coordinates_are_source_spawn_tiles':False,
   'intermediate_object_equals_final_reward':False,'complete_quest_logic_verified':False,
   'original_tw10_quest_restored':False,'original_server_executed':False,
   'modern_game_or_wiki_started':False,
   'coverage_stop':'Two source-named NPCs, two source map IDs, six EventEnd records and two active master item IDs; no helper expansion or invented initial quest state',
   'next':'LEGACY-ASSISTANT-FULL-FEATURE-ARCHIVE-01: finite source-versioned feature inventories before design adoption'}

def validate_catalog(r):
 need(r==build_catalog(),'catalog differs from exact frozen-source replay')
 return True
if __name__=='__main__':print(json.dumps(build_catalog(),ensure_ascii=False,sort_keys=True))
