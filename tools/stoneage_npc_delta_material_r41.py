"""Offline source-bound NPC byte delta and configuration projections R41."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_native_album_source_r36 import need
from tools.stoneage_preserved_npc_delta_r41 import EXPECTED,PREFIX,SCOPE
from tools.stoneage_npc_genkou_source_gate import SOURCE_SHA,ARG_SHA,KEYS,NUMS
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/recovered/STONEAGE-PRESERVED-NPC-DELTA-SOURCE-R41.json'
MATERIAL=ROOT/'research/recovered/STONEAGE-PRESERVED-NPC-DELTA-MATERIAL-R41.json'
PRIOR=ROOT/'research/recovered/STONEAGE-NPC-GENKOU-DERIVED-ARG-R1.json'
LOCAL=ROOT/'research/recovered/STONEAGE-PRESERVED-NPC-LOCAL-COMPARISON-R41.json'
INDEX_SOURCE=ROOT/'research/recovered/STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json'
SOURCE_REPORT_SHA='b51bbe6ecff9f2763b5f3725ca98d20a0fec2db9cab4085c0dc687fb62ea707d'
LOCAL_REPORT_SHA='ecfd9198c93b0e60a8c9f8c734d216b1c237c66b40b1d309b51459564169ed24'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def blocks(profile,header):
 result=[];current=None;outside=[]
 for row in profile['line_profiles']:
  kind=row['kind']
  if kind in ('BLANK','COMMENT'):continue
  if row['line']==1 and row['line_utf8_sha256']==sha(header.encode()):continue
  if kind=='BLOCK_MARKER':
   if row['marker']=='{':
    need(current is None,'no nested NPC blocks');current={'open_line':row['line'],'assignments':[]}
   else:
    need(current is not None,'matching NPC block close');current['close_line']=row['line'];result.append(current);current=None
  elif kind=='ASSIGNMENT':
   if current is None:outside.append(row)
   else:current['assignments'].append(row)
  else:raise ValueError('unclassified original config syntax at '+str(row['line']))
 need(current is None,'all NPC blocks closed')
 return {'blocks':result,'outside_assignments':outside}

def validate(report):
 need(report['schema']=='stoneage.preserved_npc_delta_source.r41' and report['source_scope']==SCOPE,'source schema/scope')
 need(report['status']=='THREE_ORIGINAL_NPC_SHA_CRC_MATCH_MODERN_DELTA_DERIVED','actual source acquisition')
 for key in ('original_server_executed','official_same_build_authenticated','raw_script_bodies_published'):need(report[key] is False,key)
 need(report['verified_base_quests_added']==0 and report['origin_class']=='ORIGIN_UNRESOLVED','quest origin boundary')
 receipt=report['receipt'];need(receipt['whole_package_rehashed'] is False,'no whole archive rehash')
 ranges=receipt['range_receipts'];need(0<receipt['headers_visited']<=10000,'finite header traversal')
 need(len(ranges)==receipt['range_requests']<=256 and sum(r['bytes'] for r in ranges)==receipt['actual_range_bytes']<=16*1024*1024,'finite source range budget')
 need(len({(r['part'],r['start']) for r in ranges})==len(ranges),'no duplicate cache receipt')
 for r in ranges:need(r['part'] in (1,2) and r['start']>=0 and r['end']-r['start']+1==r['bytes'] and len(r['sha256'])==64,'exact source range')
 need(len(receipt['members'])==3,'three original source members')
 for leaf,(size,digest) in EXPECTED.items():
  hits=[m for m in receipt['members'] if m['name']==PREFIX+leaf];need(len(hits)==1,'one exact original member')
  r=hits[0];need((r['bytes'],r['sha256'])==(size,digest),'old full original file identity')
  need(r['flags']&(1|2|4|16)==0 and r['extractor_returncode']==0,'static independent extraction')
 modern=report['modern_source'];need(modern['git_blob']==SOURCE_SHA,'pinned modern YAML git identity')
 need(modern['prior_qualified_report']==json.loads(PRIOR.read_text()),'modern whole qualification replay')
 delta=report['argument_delta'];need((delta['old_bytes'],delta['old_sha256'])==EXPECTED['sb_kbu.arg'],'original argument identity')
 need(delta['modern_bytes']==258 and delta['modern_sha256']==ARG_SHA,'modern embedded argument identity')
 need(delta['raw_bytes_equal'] is False and delta['equal_byte_lengths'] is True,'same length does not mean same original bytes')
 need(delta['dialogue_text_published'] is False,'no dialogue output')
 offsets=delta['different_byte_offsets'];need(len(offsets)>0 and offsets==sorted(set(offsets)) and all(0<=i<258 for i in offsets),'actual byte delta positions')
 fields=delta['modern_fields'];need(tuple(f['key'] for f in fields)==KEYS,'original field ordering')
 profile_by_codec={p['codec']:p for p in delta['decode_candidates']};need(len(profile_by_codec)==len(delta['decode_candidates']),'unique decoder candidates')
 exact=[p['codec'] for p in delta['decode_candidates'] if p.get('exact_transcode_to_modern_gb18030')]
 need(delta['exact_transcode_candidates']==exact,'all exact conversion outcomes')
 need(exact==[],'pure transcode was disproved by original bytes')
 changed_fields=[]
 for codec in ('cp950','big5'):
  p=profile_by_codec[codec];need(p['strict_decode'] and p['exact_unicode_equal_to_modern_gb18030'] is False and p['exact_transcode_to_modern_gb18030'] is False,'preserve non-transcode original result')
  need(tuple(f['key'] for f in p['fields'])==KEYS,'old field order')
  differences=[old['key'] for old,new in zip(p['fields'],fields) if old!=new]
  need(differences==['askbattlemsg1','startmsg','deniedmsg'],'only three original dialogue fields differ')
  for old,new in zip(p['fields'],fields):
   need(old['value_chars']==new['value_chars'],'all original Unicode field lengths')
   if old['key'] not in differences:need(old==new,'unchanged original fields')
  changed_fields=differences
 need(profile_by_codec['cp950']['fields']==profile_by_codec['big5']['fields'],'old two decoders same field text')
 numeric={f['key']:f.get('numbers') for f in fields}
 need(numeric['entype']==[2] and numeric['dieact']==[0] and numeric['onebattle']==[0] and numeric['time']==[180] and numeric['enemyno']==list(NUMS),'all original argument numbers preserved')
 for leaf in ('sb_geno.create','sb_geno.template'):
  profiles=report['configuration_profiles'][leaf];need([p['codec'] for p in profiles]==['cp950','big5'],'configuration decode candidates retained')
  need(profiles[0]['decoded_text_sha256']==profiles[1]['decoded_text_sha256'],'configuration decoder agreement')
  for p in profiles:
   need(p['raw_script_body_published'] is False and len(p['line_profiles'])==p['line_count'],'config source lines and no body publication')
   need([r['line'] for r in p['line_profiles']]==list(range(1,p['line_count']+1)),'all original physical line occurrences')
 return delta

def assignment(block,key):
 matches=[r for r in block['assignments'] if r['key']==key];need(len(matches)==1,'one original field '+key)
 return matches[0]

def validate_local(local,report):
 need(local['schema']=='stoneage.npc_private_original_comparison.r41','independent local comparison schema')
 need(local['original_file_pins']=={name:{'bytes':size,'sha256':digest} for name,(size,digest) in EXPECTED.items()},'independent full source identities')
 need(local['modern_yaml_git_blob']==SOURCE_SHA and local['modern_argument_sha256']==ARG_SHA,'independent modern identity')
 need(local['exact_modern_bytes_reproduced_after_observed_map_and_gb18030'] is True,'whole modern argument reproduced')
 need(local['whole_unicode_text_equal_before_replacement'] is False and local['source_unicode_cp950_big5_equal'] is True,'two layers of text change')
 need(local['whole_script_or_dialogue_published'] is False and local['official_same_build_authenticated'] is False,'private comparison boundaries')
 pairs=local['character_differences'];mapping={}
 need(len(pairs)==14 and len({(p['field'],p['character_index_0']) for p in pairs})==14,'all observed character positions')
 for row in pairs:
  need(row['field'] in ('askbattlemsg1','startmsg','deniedmsg') and row['character_index_0']>=0,'bounded dialogue difference position')
  a,b=row['old_character'],row['modern_character'];need(len(a)==len(b)==1 and a!=b,'one observed changed character')
  need(a not in mapping or mapping[a]==b,'consistent observed character substitution');mapping[a]=b
 need(mapping==local['observed_character_map'] and len(mapping)==9,'all nine observed character pairs')
 need(local['raw_byte_difference_count']==len(report['argument_delta']['different_byte_offsets'])==114,'all source byte changes')
 return local

def build(report):
 delta=validate(report);local_raw=LOCAL.read_bytes();need(sha(local_raw)==LOCAL_REPORT_SHA,'independent actual private comparison immutable digest')
 local=validate_local(json.loads(local_raw),report)
 configs={leaf:blocks(report['configuration_profiles'][leaf][0],header) for leaf,header in [('sb_geno.create','NPCCREATE'),('sb_geno.template','NPCTEMPLATE')]}
 need(len(configs['sb_geno.create']['blocks'])==3 and len(configs['sb_geno.template']['blocks'])==2,'three original create blocks and two templates')
 templates=configs['sb_geno.template']['blocks'];records=[]
 index_raw=INDEX_SOURCE.read_bytes();need(sha(index_raw)=='076eeab6710d9a88bf36081da4ca0718c7cbb13d99aaf6f19dd9cb9c4baf75ea','same-carrier original full SPR index report')
 source_index=json.loads(index_raw)['material']['all_index_rows']
 for ordinal,block in enumerate(configs['sb_geno.create']['blocks']):
  enemy=assignment(block,'enemy')['ascii_token'];template_name,argument=enemy.split('|file:')
  matched=[(i,t) for i,t in enumerate(templates) if assignment(t,'templatename').get('ascii_token')==template_name]
  need(len(matched)==1,'one exact original referenced template');ti,template=matched[0]
  graphic=assignment(block,'graphicname')['numbers'];need(len(graphic)==1,'one original graphic field')
  name=assignment(block,'name');need(name['value_utf8_sha256']==sha('風的守護獸'.encode()),'actual original name fingerprint')
  need(assignment(template,'type')['numbers']==graphic and assignment(template,'functionset')['ascii_token']=='NPCEnemy','original template type and function token')
  records.append({'create_block_index':ordinal,'open_line':block['open_line'],'name_cp950':'風的守護獸',
   'floorid_values':assignment(block,'floorid')['numbers'],'borncenter_values':assignment(block,'borncenter')['numbers'],
   'movecenter_values':assignment(block,'movecenter')['numbers'],'createnum_values':assignment(block,'createnum')['numbers'],
   'time_values_uninterpreted_units':assignment(block,'time')['numbers'],'dir_values':assignment(block,'dir')['numbers'],
   'graphicname_values':graphic,'enemy_template_token':template_name,'argument_path':argument,'template_block_index':ti,
   'template_functionset_token':'NPCEnemy','same_carrier_spr_index_numeric_candidates':[row for row in source_index if row[1]==graphic[0]],
   'original_spawn_or_render_executed':False})
 old_map_records=[r for r in records if r['floorid_values']==[11208]]
 modern=report['modern_source']['prior_qualified_report']['modern_npc_occurrences'];need(len(old_map_records)==len(modern)==2,'exact modern map scope')
 for old,new in zip(old_map_records,modern):
  need(old['borncenter_values'][:2]==[new['x'],new['y']] and old['create_block_index']==new['create_block_index'] and old['open_line']==new['create_line'],'two scoped original/modern position and line correspondences')
 return {'schema':'stoneage.preserved_npc_delta_material.r41','source_scope':SCOPE,
  'source_report_sha256':sha((json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()),
  'local_comparison_sha256':sha(LOCAL.read_bytes()),'classification':'ENCODING_CHANGE_PLUS_OBSERVED_TRADITIONAL_SIMPLIFIED_REPLACEMENTS_NUMERIC_FIELDS_IDENTICAL',
  'argument_byte_difference_count':len(delta['different_byte_offsets']),'exact_transcode_candidates':delta['exact_transcode_candidates'],
  'character_difference_occurrences':len(local['character_differences']),'observed_character_pair_count':len(local['observed_character_map']),
  'modern_argument_fields':delta['modern_fields'],'old_cp950_argument_fields':next(p for p in delta['decode_candidates'] if p['codec']=='cp950')['fields'],
  'configuration_blocks':configs,'original_create_records':records,'modern_npc_occurrences':modern,'modern_warp_count':3,
  'original_create_11208_record_count':2,'original_create_11214_record_count':1,
  'same_carrier_resource_index_source':{'path':str(INDEX_SOURCE.relative_to(ROOT)),'sha256':sha(index_raw)},
  'limits':{'official_same_build_authenticated':False,'original_server_executed':False,'verified_base_quests_added':0,
   'origin_class':'ORIGIN_UNRESOLVED','three_modern_warps_certified_from_old_create':False,'whole_script_or_dialogue_published':False,
   'third_record_deleted_in_modern_proven':False,'original_guard_graphic_pixels_or_full_animation_proven':False},
  'next':'PRESERVED_GENKOU_THIRD_GUARD_ARGUMENT_42','overall_restoration_percent':None}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');a=parser.parse_args()
 source_raw=SOURCE.read_bytes();need(sha(source_raw)==SOURCE_REPORT_SHA,'immutable original source report')
 result=build(json.loads(source_raw));raw=(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
 if a.write:MATERIAL.write_bytes(raw)
 else:need(MATERIAL.read_bytes()==raw,'exact archived NPC material replay')
 print(json.dumps({'status':'PASS','byte_changes':result['argument_byte_difference_count'],'classification':result['classification']}))
if __name__=='__main__':main()
