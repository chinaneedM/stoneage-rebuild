"""Independent offline re-encoding and source-bounded name/SPR integration R40."""
from collections import Counter
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
import struct
from tools.stoneage_preserved_pet_spr_r40 import EXPECTED,SCOPE,SERVER_SHA,source_keys
from tools.stoneage_pet_template_material_r39 import SOURCE as SERVER_SOURCE,validate as server_validate
from tools.stoneage_native_album_source_r36 import PREFIX,need
from tools.stoneage_tw85_spr137_material_r28 import REFERENCES,REFERENCE_SHA256
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/recovered/STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json'
MATERIAL=ROOT/'research/recovered/STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json'
SOURCE_SHA='076eeab6710d9a88bf36081da4ca0718c7cbb13d99aaf6f19dd9cb9c4baf75ea'
def sha(raw):return hashlib.sha256(raw).hexdigest()

def validate(report):
 need(report['schema']=='stoneage.preserved_pet_spr_source.r40','source schema')
 need(report['status']=='ORIGINAL_PAIR_SHA_CRC_MATCH_SELECTED_SPR_DERIVED','actual original pair acquired')
 need(report['source_scope']==SCOPE and report['server_source_sha256']==SERVER_SHA,'bounded source identity')
 for key in ('original_payload_published','original_program_executed','same_deployed_build_proven','official_species_identity_authenticated','actual_render_or_audio_proven'):
  need(report[key] is False,key)
 need(report['new_official_clients']==0,'no new official clients')
 receipt=report['receipt'];need(receipt['whole_package_rehashed'] is False,'no full archive hash claim')
 need(0<receipt['headers_visited']<=10000,'finite full header walk')
 ranges=receipt['range_receipts'];need(len(ranges)==receipt['range_requests']<=256,'finite range requests')
 need(sum(r['bytes'] for r in ranges)==receipt['actual_range_bytes']<=16*1024*1024,'finite source byte budget')
 seen=set()
 for r in ranges:
  need(r['part'] in (1,2) and r['end']-r['start']+1==r['bytes'] and r['start']>=0,'exact source extent')
  key=(r['part'],r['start']);need(key not in seen,'unique cache range');seen.add(key)
  need(len(r['sha256'])==64,'range digest')
 need(len(receipt['members'])==2,'two complete source files')
 for leaf,(size,digest) in EXPECTED.items():
  rows=[r for r in receipt['members'] if r['name']==PREFIX+'data/'+leaf];need(len(rows)==1,'unique exact source member')
  r=rows[0];need((r['bytes'],r['sha256'])==(size,digest),'whole original file identity')
  need(r['flags']&(1|2|4|16)==0 and r['extractor_returncode']==0,'independent static extraction')
 m=report['material'];keys=source_keys();need(m['selected_graphic_keys']==keys,'keys exclusively from original R39')
 index=m['all_index_rows'];need(len(index)==m['index_rows_count']==847,'full original index conservation')
 encoded=[]
 for i,row in enumerate(index):
  need(len(row)==5 and all(type(v) is int for v in row) and row[0]==i,'exact native index occurrence')
  encoded.append(struct.pack('<IIHH',*row[1:]));need(0<=row[2]<EXPECTED['spr_4.bin'][0],'bounded index offset')
 need(sha(b''.join(encoded))==EXPECTED['spradrn_5.bin'][1],'independent full SPR index original SHA')
 for field,col in [('duplicate_group_keys',1),('duplicate_physical_offsets',2)]:
  counts=Counter(r[col] for r in index);need(m[field]=={str(k):v for k,v in sorted(counts.items()) if v>1},'all duplicate occurrences preserved')
 chosen=[r for r in index if r[1] in keys];groups=m['selected_groups'];need(len(groups)==len(chosen),'all selected source occurrences')
 offsets=sorted({r[2] for r in index});ends={v:(offsets[i+1] if i+1<len(offsets) else EXPECTED['spr_4.bin'][0]) for i,v in enumerate(offsets)}
 total_frames=sentinels=total_animations=0
 for expected,g in zip(chosen,groups):
  need([g['group_index'],g['spr_no'],g['offset'],g['anim_count'],g['reserved']]==expected,'source group identity and order')
  need(g['index_record_sha256']==sha(encoded[expected[0]]),'selected original index record digest')
  cursor=g['offset'];packed=[];bmps=[]
  need(len(g['animations'])==g['anim_count'],'all selected animation occurrences')
  for ai,animation in enumerate(g['animations']):
   need(animation['index']==ai and animation['header_offset']==cursor,'original animation position and order')
   frames=animation['frames'];need(len(frames)==animation['frame_count'],'all original frames retained')
   packed.append(struct.pack('<HHII',animation['direction'],animation['anim_no'],animation['duration'],len(frames)));cursor+=12
   for frame in frames:
    need(len(frame)==4 and all(type(v) is int for v in frame),'four exact frame fields')
    packed.append(struct.pack('<IhhH',*frame));cursor+=10;bmps.append(frame[0])
   need(animation['end_offset']==cursor,'animation exact end')
  need(cursor==g['end_offset']==ends[g['offset']],'next distinct physical offset boundary')
  need(sha(b''.join(packed))==g['segment_sha256'],'independent all-frame original segment SHA')
  need(g['frame_count']==len(bmps) and g['sentinel_frames']==bmps.count(0xffffffff),'group frame and sentinel counts')
  need(g['distinct_non_sentinel_bitmap_keys']==len(set(bmps)-{0xffffffff}),'bitmap uniqueness is not occurrence loss')
  total_frames+=len(bmps);sentinels+=bmps.count(0xffffffff);total_animations+=len(g['animations'])
 need(m['selected_frame_occurrences']==total_frames and m['selected_sentinel_occurrences']==sentinels and m['selected_animation_occurrences']==total_animations,'all selected totals')
 need(m['unmatched_graphic_keys']==[k for k in keys if not any(g['spr_no']==k for g in groups)],'explicit missing keys')
 return m

def build(report):
 m=validate(report);server=server_validate(json.loads(SERVER_SOURCE.read_text()));refs={};pins={}
 for label,path in REFERENCES.items():
  raw=path.read_bytes();need(sha(raw)==REFERENCE_SHA256[label],'original reference group metadata pin')
  pins[label]={'path':str(path.relative_to(ROOT)),'bytes':len(raw),'sha256':sha(raw)}
  with gzip.open(path,'rt',newline='') as f:refs[label]=list(csv.DictReader(f,delimiter='\t'))
 links=[]
 for row in server['selected_rows']:
  groups=[g for g in m['selected_groups'] if g['spr_no']==row['graphic_field_column_37']]
  links.append({'server_name':row['name'],'server_original_line':row['line'],'server_template_column_7':row['template_number_column_7'],
   'server_graphic_column_37':row['graphic_field_column_37'],'server_flag_column_38':row['pet_flag_column_38'],
   'server_row_sha256':row['row_sha256'],'client_group_indices':[g['group_index'] for g in groups],
   'join_kind':'SAME_CARRIER_EQUAL_NUMERIC_KEY_ONLY_NOT_DEPLOYMENT_PROOF'})
 comparisons=[];profiles=[]
 for g in m['selected_groups']:
  action_rows=[]
  for code in sorted({a['anim_no'] for a in g['animations']}):
   matching=[a for a in g['animations'] if a['anim_no']==code]
   action_rows.append({'anim_no':code,'sequence_occurrences':len(matching),'direction_values':sorted({a['direction'] for a in matching}),
    'frame_count_values':sorted({a['frame_count'] for a in matching}),'duration_values':sorted({a['duration'] for a in matching})})
  profiles.append({'spr_no':g['spr_no'],'group_index':g['group_index'],'action_headers':action_rows})
  records={}
  for label,table in refs.items():
   records[label]=[{'index':int(r['index']),'segment_sha256':r['segment_sha256'],
    'exact_full_segment_equal':r['segment_sha256']==g['segment_sha256']} for r in table if int(r['spr_no'])==g['spr_no']]
  comparisons.append({'client_group_index':g['group_index'],'spr_no':g['spr_no'],'segment_sha256':g['segment_sha256'],'reference_occurrences':records})
 return {'schema':'stoneage.preserved_pet_spr_material.r40','source_scope':SCOPE,'server_source_sha256':SERVER_SHA,
  'source_report_sha256':sha((json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()),
  'source_index_rows':m['index_rows_count'],'selected_animation_occurrences':m['selected_animation_occurrences'],
  'selected_frame_occurrences':m['selected_frame_occurrences'],'selected_sentinel_occurrences':m['selected_sentinel_occurrences'],
  'server_occurrence_links':links,'per_group_action_header_profiles':profiles,'reference_pins':pins,'full_segment_comparisons':comparisons,
  'limits':{'same_deployed_build_proven':False,'official_early_species_name_authenticated':False,
   'actual_client_render_or_audio_proven':False,'raw_original_assets_published':False,'duration_is_fps':False},
  'next':'PRESERVED_NPC_GENKOU_ORIGINAL_BYTE_DELTA_41','overall_restoration_percent':None}

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
 source_raw=SOURCE.read_bytes();need(sha(source_raw)==SOURCE_SHA,'immutable original source report SHA')
 result=build(json.loads(source_raw));raw=(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
 if a.write:MATERIAL.write_bytes(raw)
 else:need(MATERIAL.read_bytes()==raw,'exact source-derived material replay')
 print(json.dumps({'status':'PASS','selected_animations':result['selected_animation_occurrences'],'selected_frames':result['selected_frame_occurrences'],'server_occurrences':len(result['server_occurrence_links'])}))
if __name__=='__main__':main()
