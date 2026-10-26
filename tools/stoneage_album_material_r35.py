"""Source-qualified album state candidates, never a server species master.

Opaque account keys, free names and uninitialized face/stat fields are omitted.
The observed 224-slot format is not the current descendant's compile profile.
"""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import re
import struct
from tools.stoneage_mixed25_data_prefix_r35 import TARGETS,ROOT

SLOTS=224
RECORD_BYTES=80
BLOCK_BYTES=16+SLOTS*RECORD_BYTES
SOURCE='research/recovered/STONEAGE-MIXED25-THREE-DATA-SOURCE-R35.json'
REPORT='research/recovered/STONEAGE-ALBUM-OBSERVED-NAMES-MATERIAL-R35.json'
PET_TABLE_BLOB='d42c67f76ca453a778a8f49e51220a265c1eeb06'
SOURCE_SHA='d9daeb4305a0f246586eb5b6716139b75caecf2ebba161de29bcd4b3356c3baf'
REPORT_SHA='54c02c1dfd987cd9f2774a5be45de1a3bdfd4f68d40bd3a369526d0a8d998034'
UPSTREAM={'repository':'BismarckDD/stoneage','head':'2f736808ff4361f5429ee919b718c88fabb60346',
 'tree':'b36a900861b8f550f1725a5a5b43732b4705d2fb','exact_same_compiled_build_proven':False,
 'files':{'client/stoneage/system/menu.cpp':'af1f30b33876b143519a4c9273f7d8b848ab4bc2',
 'client/stoneage/systeminc/menu.h':'4730c1ada506169acf9e15d5daebd941be9f6b88',
 'client/stoneage/systeminc/pc.h':'12b032114bccc49bc8a28251ee828638d2dee474',
 'client/stoneage/system/ai_setting.cpp':'424a66d90e0bbf71471c5c56c816ba12556d469d',
 'client/resources/pet_name.h':PET_TABLE_BLOB},
 'semantic_source_lines':{'album_random_initialization':[2186,2202],'local_user_block_reader':[2217,2250],
 'seen_name_only_write':[8600,8612],'photograph_stat_and_face_write':[13510,13538],
 'PET_ALBUM_struct':[747,758],'old_224_constant':[60,61],
 'AI_user_keyed_reader':[68,171]}}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':sha(raw),'git_blob':blob(raw)}

def observe_album(raw):
 need(len(raw)>0 and len(raw)%BLOCK_BYTES==0 and len(raw)//BLOCK_BYTES<=32,'exact finite candidate user blocks')
 rows=[];blocks=[];hist=Counter()
 for block in range(len(raw)//BLOCK_BYTES):
  flags=Counter()
  for slot in range(SLOTS):
   offset=block*BLOCK_BYTES+16+slot*RECORD_BYTES;record=raw[offset:offset+RECORD_BYTES]
   flag=struct.unpack_from('<i',record,76)[0]
   need(flag in (0,1),'current specimen supports only raw flags0/1; do not guess photograph semantics')
   flags[flag]+=1;hist[flag]+=1
   if flag==0:continue
   field=record[:17];need(b'\0' in field,'name candidate must terminate inside17B')
   name_raw=field.split(b'\0',1)[0];name=name_raw.decode('gbk','strict')
   need(name and all(ord(c)>=32 for c in name),'nonempty printable name candidate')
   try:big5=name_raw.decode('big5','strict')
   except UnicodeDecodeError:big5=None
   rows.append({'local_block_ordinal':block,'album_slot':slot,'source_record_offset':offset,
     'raw_flag':flag,'observed_name_gbk':name,'name_field_sha256':sha(field),'name_token_sha256':sha(name_raw),
     'big5_decodes':big5 is not None,'big5_equals_gbk':big5==name,
     'face_stat_and_free_name_fields_interpreted':False})
  blocks.append({'local_block_ordinal':block,'slot_count':SLOTS,'flag_counts':{str(k):v for k,v in sorted(flags.items())}})
 byslot=defaultdict(set)
 for row in rows:byslot[row['album_slot']].add(row['observed_name_gbk'])
 return {'candidate_block_bytes':BLOCK_BYTES,'candidate_block_count':len(blocks),'candidate_slot_record_bytes':RECORD_BYTES,
  'candidate_slots_per_block':SLOTS,'physical_slot_occurrences':sum(hist.values()),
  'raw_flag_counts':{str(k):v for k,v in sorted(hist.items())},'blocks':blocks,'observed_name_rows':rows,
  'distinct_named_slots':len(byslot),'distinct_names':len({x['observed_name_gbk'] for x in rows}),
  'slot_name_conflicts':[slot for slot,names in sorted(byslot.items()) if len(names)>1],
  'flag1_name_decode_gbk_count':len(rows),'flag1_name_decode_big5_count':sum(x['big5_decodes'] for x in rows),
  'flag1_name_equal_both_encodings_count':sum(x['big5_equals_gbk'] for x in rows)}

def read_descendant_table(raw):
 need(blob(raw)==PET_TABLE_BLOB,'exact pinned descendant text source required')
 rows=defaultdict(list)
 for m in re.finditer(r'\{\s*(-?\d+)\s*,\s*"([^"\n]+)"\s*,\s*(\d+)\s*\}',raw.decode('utf-8-sig')):
  rows[int(m[1])].append(m[2])
 return rows

def build(directory,table_path):
 raw=(directory/'album_4.dat').read_bytes();need((len(raw),sha(raw))==TARGETS['album_4.dat'],'original source album full SHA required')
 obs=observe_album(raw);table_raw=table_path.read_bytes();table=read_descendant_table(table_raw)
 for row in obs['observed_name_rows']:
  row['same_slot_descendant_name_exact_matches']=sum(name==row['observed_name_gbk'] for name in table.get(row['album_slot'],[]))
 obj={'schema':'stoneage.album_observed_name_candidates.r35','source_scope':'EXISTING_MIXED25_CLIENT_LOCAL_ALBUM_NOT_OFFICIAL_SERVER_MASTER',
  'source_album':{'path':'data/album_4.dat',**pin(raw)},'source_metadata_projection':pin((ROOT/SOURCE).read_bytes()),
  'upstream_comparison':{**UPSTREAM,'pet_table_bytes':len(table_raw),'pet_table_sha256':sha(table_raw)},
  'album_material':obs,'same_slot_descendant_name_match_occurrences':sum(x['same_slot_descendant_name_exact_matches']>0 for x in obs['observed_name_rows']),
  'supporting_data':{'AISetting.dat':{'bytes':612,'candidate_record_bytes':68,'candidate_local_records':9,
    'scope':'16 opaque key bytes plus13 signed32 fields; compatible with descendant four-entry AI arrays, not same-build proof'},
   'auto.dat':{'bytes':250010,'internal_semantics':'UNRESOLVED_NO_PET_MASTER_ASSUMPTION'}},
  'boundaries':{'account_keys_decoded':False,'account_keys_or_pet_free_names_published':False,
   'random_face_or_stat_fields_promoted':False,'same_build_species_to_graphic_binding_proven':False,
   'original_game_executed':False,'official_tw10_entities_added':0,'all_species_denominator':None,
   'original_client_data_payloads_published':False,'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED',
   'r79':'PAUSED_NON_BLOCKING','overall_percent':None},
  'next':'PRESERVED_CLIENT_NATIVE_PET_ALBUM_TABLE_SOURCE_36'}
 return obj

def replay(d):
 need(d['schema']=='stoneage.album_observed_name_candidates.r35','material schema')
 need(d['source_scope']=='EXISTING_MIXED25_CLIENT_LOCAL_ALBUM_NOT_OFFICIAL_SERVER_MASTER','source promotion')
 need((d['source_album']['bytes'],d['source_album']['sha256'])==TARGETS['album_4.dat'],'original source identity')
 need(d['source_metadata_projection']==pin((ROOT/SOURCE).read_bytes()),'source projection drift')
 need(sha((ROOT/SOURCE).read_bytes())==SOURCE_SHA,'immutable public source projection')
 source=json.loads((ROOT/SOURCE).read_bytes())
 need(source['status']=='THREE_ORIGINAL_MEMBER_FULL_HASHES_MATCH' and source['new_official_clients']==0,'actual acquisition status')
 need({m['name']:(m['bytes'],m['sha256']) for m in source['members']}==TARGETS,'three old full member identities')
 need(source['fetch']['prefix_bytes']==16777216 and source['fetch']['range_status']==206 and source['fetch']['whole_part_or_whole_archive_rehashed'] is False,'bounded raw source scope')
 need(source['projection']['omitted_fields']==['members[*].first_four_le_u32'],'opaque header identity omission')
 obs=d['album_material'];need((obs['candidate_block_count'],obs['candidate_slots_per_block'],obs['physical_slot_occurrences'])==(9,224,2016),'source shape conservation')
 need(obs['raw_flag_counts']=={'0':1868,'1':148},'actual flag counts')
 need((obs['candidate_block_bytes'],obs['candidate_slot_record_bytes'])==(17936,80),'candidate record extents')
 rows=obs['observed_name_rows'];need(len(rows)==148 and len({(r['local_block_ordinal'],r['album_slot']) for r in rows})==148,'duplicate or missing occurrence')
 for row in rows:
  b,s=row['local_block_ordinal'],row['album_slot'];need(type(b)is int and 0<=b<9 and type(s)is int and 0<=s<224,'source record namespace')
  need(row['source_record_offset']==b*BLOCK_BYTES+16+s*80 and row['raw_flag']==1,'source offset/flag')
  need(row['face_stat_and_free_name_fields_interpreted'] is False,'random fields must stay uninterpreted')
  need(sha(row['observed_name_gbk'].encode('gbk'))==row['name_token_sha256'],'name token encoding/hash drift')
  need(row['same_slot_descendant_name_exact_matches']==1,'bounded comparison exactness')
 need(len({r['album_slot'] for r in rows})==76 and len({r['observed_name_gbk'] for r in rows})==76,'bounded named-slot count')
 need(len(obs['blocks'])==9,'all local blocks retained')
 for i,block in enumerate(obs['blocks']):
  count=sum(r['local_block_ordinal']==i for r in rows)
  need(block=={'local_block_ordinal':i,'slot_count':224,'flag_counts':({'0':224-count,'1':count} if count else {'0':224})},'local block conservation')
 need(obs['slot_name_conflicts']==[] and (obs['flag1_name_decode_gbk_count'],obs['flag1_name_decode_big5_count'],obs['flag1_name_equal_both_encodings_count'])==(148,139,0),'encoding conflict preserved')
 need(d['same_slot_descendant_name_match_occurrences']==148,'comparison count')
 flags=['account_keys_decoded','account_keys_or_pet_free_names_published','random_face_or_stat_fields_promoted','same_build_species_to_graphic_binding_proven','original_game_executed','original_client_data_payloads_published']
 need(all(d['boundaries'][f] is False for f in flags),'historical or personal-data overclaim')
 need(d['boundaries']['official_tw10_entities_added']==0 and d['boundaries']['all_species_denominator'] is None and d['boundaries']['overall_percent'] is None,'no invented original roster')
 need((d['boundaries']['stage_a'],d['boundaries']['stage_b_wiki'],d['boundaries']['r79'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING'),'project gates')
 need(all(d['upstream_comparison'].get(k)==v for k,v in UPSTREAM.items()),'descendant source or build scope drift')

def independent_original(directory,report):
 import ctypes as c
 class Slot(c.LittleEndianStructure):
  _fields_=[('name',c.c_ubyte*17),('free_name',c.c_ubyte*17)]+[(n,c.c_int32) for n in ('face','level','hp','strength','quick','defense','earth','water','fire','wind','flag')]
 need(c.sizeof(Slot)==80 and Slot.flag.offset==76 and Slot.face.offset==36,'independent C layout')
 raw=(directory/'album_4.dat').read_bytes();need(sha(raw)==TARGETS['album_4.dat'][1],'independent original SHA')
 observed=[]
 for block in range(9):
  for slot in range(224):
   item=Slot.from_buffer_copy(raw,block*17936+16+slot*80)
   need(item.flag in (0,1),'independent unknown flag')
   if item.flag==1:observed.append((block,slot,bytes(item.name).split(b'\0')[0].decode('gbk')))
 need(observed==[(r['local_block_ordinal'],r['album_slot'],r['observed_name_gbk']) for r in report['album_material']['observed_name_rows']],'independent field/source comparison')
 print('R35_INDEPENDENT_CTYPES_2016_SLOTS_AND_148_NAME_FIELDS=PASS')

def main():
 p=argparse.ArgumentParser();p.add_argument('--members',type=Path);p.add_argument('--descendant-table',type=Path);p.add_argument('--write',action='store_true');p.add_argument('--independent-original',type=Path);a=p.parse_args()
 if a.write:
  obj=build(a.members,a.descendant_table);replay(obj);(ROOT/REPORT).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 else:
  raw=(ROOT/REPORT).read_bytes();need(sha(raw)==REPORT_SHA,'exact accepted derived material report');obj=json.loads(raw);replay(obj)
 if a.independent_original:independent_original(a.independent_original,obj)
 print('R35_ALBUM_148_NAME_OCCURRENCES_76_SLOTS_NOT_SPECIES_MASTER=PASS')

if __name__=='__main__':main()
