#!/usr/bin/env python3
"""PET13: source-bounded 11 capture-key candidates -> original mixed25 attributes and skills.

The original 56-column enemybase / 12-column petskill source remains private.
Use previously source-qualified public numeric summaries; optionally independently
replay exact raw CP950 lines and source checksums when private originals are given.
"""
from __future__ import annotations
import argparse,hashlib,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'research/recovered'
R2=BASE/'STONEAGE-STAGE-A-WORLD37-R2B3-CAPTURE-ORIGINAL-SPR-BRIDGE-R1.json'
PET10=BASE/'STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json'
WANT={
 'enemybase.txt':(147750,'1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7','29258170',56),
 'petskill.txt':(15112,'f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4','309a3165',12),
}
SKILL_LABELS={1:'攻擊',2:'防禦',60:'毒攻擊',90:'混亂攻擊',110:'催眠攻擊'}

def check(x,desc):
 if not x:raise ValueError('PET13 source gate: '+desc)

def digest(b):return hashlib.sha256(b).hexdigest()

def blobsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def read_public():
 p2=R2.read_bytes();p10=PET10.read_bytes()
 check(blobsha(p2)=='0e80e5a62dd59542c3e1ede18460d92e17927a30','WORLD37-R2B3 Git immutable input')
 check(blobsha(p10)=='25a37aeb134fb180e322e7dc335029b7374452d8','PET10 immutable public original-source numeric summary')
 r2=json.loads(p2);p=json.loads(p10)
 check(p['schema']=='stoneage.pet10_original_mixed25_rar_same_archive_full_server_material_qualified.r1','PET10 source receipt')
 check(p['preserved_original_rar']['sha256']==r2['original_source_integrity']['private_original_archive_sha256'],'two source receipts have different original RAR')
 for name,(length,s,crc,fields) in WANT.items():
  row=p['verified_original_archive_members'][name]
  check((row['bytes'],row['sha256'],row['archive_record_crc32'])==(length,s,crc),'source member source SHA/CRC differs')
 check(r2['conservation']['source_capture_rows']==11,'original compiled condition count')
 return r2,p,p2,p10

def derive():
 r2,p,r2bytes,p10bytes=read_public()
 rows=p['source_rows']['enemybase.txt']
 ids={x[1]:x for x in rows}
 check(len(ids)==988,'duplicate/missing source template ID')
 skills={x[1]:x for x in p['source_rows']['petskill.txt']}
 check(len(skills)==147,'original skill definition source census')
 summary=[];referenced=[]
 for c in r2['rows']:
  key=c['source_char_int_key53'];check(key in ids,'original capture key has no selected enemybase template')
  a=ids[key]
  check(len(a)==17,'original 56-field numeric summary shape')
  check(a[2]==c['configured_enemybase_column37_graphic_number'] and a[3]==c['configured_enemybase_column38_PETFLG'] and a[-1]==c['configured_enemybase_normalized_fields_sha256'],'original source numeric ID/graphic/flag/56-field SHA')
  check(a[0]==c['configured_enemybase_physical_line'],'selected original physical row')
  skillids=[v for v in a[15] if v is not None and v>0]
  check(all(k in skills for k in skillids),'missing same-source pet skill definition')
  referenced.extend(skillids)
  summary.append({'compiled_capture_key53':key,'original_server_template_physical_row':a[0],
   'mixed25_configured_original_name':c['configured_enemybase_name_original_cp950'],
   'original_template_numeric_ID':a[1],'original_graphic_numeric_ID':a[2],
   'original_PETFLG':a[3],'capture_required_item_IDs':c['source_required_item_ids'],
   'original_initnum_literal':a[4],'original_lvup_literal':a[5],
   'original_base_stats_literal':{'vital':a[6],'strength':a[7],'toughness':a[8],'dexterity':a[9]},
   'original_earth_water_fire_wind_literals':{'earth':a[10],'water':a[11],'fire':a[12],'wind':a[13]},
   'original_slot_literal':a[14],
   'original_seven_skill_slots_nullable':a[15],
   'same_archive_original_skill_links':[{'source_pet_skill_id':k,'original_skill_definition_physical_line':skills[k][0],'original_skill_normalized_full_row_sha256':skills[k][2]} for k in skillids],
   'original_56_column_normalized_sha256':a[-1],
   'original_physical_line_including_newline_sha256':c['configured_enemybase_original_line_sha256'],
   'original_compiled_runtime_key_to_template_loader_verified':False,'original_actual_capturable_pets_species_verified':False})
 check(len(summary)==11 and len({x['compiled_capture_key53'] for x in summary})==11,'11 compiled numeric keys')
 check(sum(x['original_PETFLG']==1 for x in summary)==10 and sum(x['original_PETFLG']==0 for x in summary)==1,'preserve non-pet flagged condition')
 check(set(referenced)==set(SKILL_LABELS),'current same-source skill ID references differ')
 check(all(int(x['original_lvup_literal'].replace('.',''))==450 for x in summary),'unexpected growth literal')
 return {'schema':'stoneage.pet13.eleven_compiled_capture_key_to_same_original_enemybase_template_and_petskill.r1',
   'original_scope':'MIXED25_PRESERVED_COMMUNITY_SERVER_STATIC_NOT_AN_OFFICIAL_SAME_BUILD_GAME_RUN',
   'source_git_blobs':{'WORLD37_R2B3':blobsha(r2bytes),'PET10':blobsha(p10bytes)},
   'source_archive_full_sha256':r2['original_source_integrity']['private_original_archive_sha256'],
   'original_same_archive_member_sha256':{name:v[1] for name,v in WANT.items()},
   'source_numeric_field_mapping':'PET10 full original 56 source fields physical column7 ID, 8 INITNUM, 9 LVUP, 10-13 base, 16-19 attributes, 26-32 seven nullable skill slots, 36 slot, 37 graphic, 38 PETFLG',
   'same_source_original_petskill_short_labels_private_verified':[{'skill_id':k,'source_short_name':v,'source_original_row_sha256':skills[k][2]} for k,v in sorted(SKILL_LABELS.items())],
   'templates':summary,
   'summary':{'compiled_candidate_rows':11,'PETFLG_1_count':10,'PETFLG_0_count':1,'all_literal_level_up_words':'4.50',
     'distinct_template_IDs':len({x['original_template_numeric_ID'] for x in summary}),
     'distinct_original_graphic_numbers':len({x['original_graphic_numeric_ID'] for x in summary}),
     'distinct_positive_source_skill_IDs':len(set(referenced)),'positive_original_skill_slot_occurrences':len(referenced),
     'all_skill_references_defined_in_same_source_master':True,
     'compiled_capture_required_item_references':sum(len(x['capture_required_item_IDs']) for x in summary),
     'distinct_capture_required_item_IDs':len(set(v for x in summary for v in x['capture_required_item_IDs']))},
   'bounds':{'original_server_executed_this_turn':False,'original_capture_success_sourced_now':False,
     'native_game_runtime_key53_is_enemybase_column7_proven':False,
     'mixed25_template_names_or_stats_are_original_TW10_TW85_CN50_server_values':False,
     'same_numeric_graphic_confirms_same_pet_species_across_versions':False,
     'original_stat_growth_and_pet_skill_runtime_formula_verified_here':False,
     'original_proprietary_CP950_text_table_published':False,'same_compiled_capture_conditions_present_in_TW10_official':False,
     'TW85_original_RD_pixels_from_this_server_table':False,'overall_percent':None,
     'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'}}

def verify_private(directory,public):
 directory=Path(directory)
 want={x['original_template_numeric_ID']:x for x in public['templates']}
 labels={x['skill_id']:x for x in public['same_source_original_petskill_short_labels_private_verified']}
 for name,(length,s,crc,ncols) in WANT.items():
  raw=(directory/name).read_bytes()
  check(len(raw)==length and digest(raw)==s and f'{zlib.crc32(raw)&0xffffffff:08x}'==crc,'actual private original file whole SHA/CRC: '+name)
  got=[]
  for i,line in enumerate(raw.splitlines(keepends=True),1):
   if not line.strip():continue
   f=line.rstrip(b'\r\n').decode('cp950').split(',')
   check(len(f)==ncols,'original CP950 field count')
   got.append((i,line,f))
  if name=='enemybase.txt':
   check(len(got)==988,'selected master full source records')
   chosen={int(f[6]):(i,line,f) for i,line,f in got if int(f[6]) in want}
   check(set(chosen)==set(want),'11 original source lines')
   for id,x in want.items():
    i,line,f=chosen[id]
    check(i==x['original_server_template_physical_row'] and digest(line)==x['original_physical_line_including_newline_sha256'] and digest(','.join(f).encode('cp950'))==x['original_56_column_normalized_sha256'],'original template raw row and normalized SHA')
    check(f[0]==x['mixed25_configured_original_name'] and f[36]==str(x['original_graphic_numeric_ID']) and f[37]==str(x['original_PETFLG']),'original source written name/image/flag')
    check(f[25:32]==[str(v) if v is not None else '' for v in x['original_seven_skill_slots_nullable']],'seven true skill slots')
  else:
   check(len(got)==147,'original skill source row count')
   selected={int(f[6]):(i,f) for i,line,f in got if int(f[6]) in labels}
   check(set(selected)==set(labels),'all five skill definitions')
   for id,x in labels.items():
    i,f=selected[id]
    check(f[0]==x['source_short_name'] and digest(','.join(f).encode('cp950'))==x['source_original_row_sha256'],'original skill name/row SHA')
 return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--check',type=Path);ap.add_argument('--private-original-dir',type=Path);ap.add_argument('--emit-json',action='store_true')
 a=ap.parse_args();r=derive()
 if a.check:check(json.loads(a.check.read_text())==r,'archived source-derived metadata mismatch')
 if a.private_original_dir:verify_private(a.private_original_dir,r)
 if a.output:a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 if a.emit_json:print('PET13_SOURCE_JSON_BEGIN\n'+json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\nPET13_SOURCE_JSON_END')
 print('PET13_REPLAY_PASS: 11 exact original rows; 5 original source skill definitions; 13 item refs; private source bytes=',bool(a.private_original_dir))

if __name__=='__main__':main()