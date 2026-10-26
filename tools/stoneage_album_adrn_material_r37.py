"""Deterministic offline R37 provenance/cross-namespace contract."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'research/recovered'
PATHS=('STONEAGE-PRESERVED-ALBUM-ALIAS-R37.json','STONEAGE-ALBUM-ADRN-SOURCE-R37.json','STONEAGE-ALBUM-ADRN-SOURCE-ATTEMPT1-R37.json','STONEAGE-NATIVE-ALBUM-MATERIAL-R36.json')
EXPECTED=((28001,'乌力',0,7246),(28002,'乌力乌力',1,7247),(28003,'乌力斯坦',2,7248))
def read_all():
 return [json.loads((BASE/x).read_text(encoding='utf-8')) for x in PATHS]
def check(m,s,f,old):
 def need(ok,message):
  if not ok:raise ValueError(message)
 need(m['schema']=='stoneage.preserved_album_adrn_material.r37','schema')
 need(s['status']=='ORIGINAL_ADRN_FULL_HASH_MATCH','real source status')
 need(f['status']=='NOT_ACQUIRED' and f['error']['message']=='finite sparse read required','failed source unchanged')
 need(m['attempts'][0]['source_status']=='NOT_ACQUIRED' and m['attempts'][1]['source_status']=='ORIGINAL_ADRN_FULL_HASH_MATCH','failed and good sources distinct')
 need(m['attempts'][1]['run']==40420077051 and m['attempts'][1]['job']==121912033214,'successful run')
 need(s['source_member']==m['full_member'] and s['source_member']['bytes']==18765120,'full member')
 need(s['source_member']['sha256']=='92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74','original member hash')
 need(s['receipt']['selected_header']['original_crc32']==823378952,'original member CRC')
 need(s['receipt']['extractor']['return_code']==0 and m['range_requests']==71 and m['range_bytes']==4653056,'sparse extraction')
 sd=s['selected_metadata']
 need(sd['records_scanned']==234564 and sd['record_bytes']==80 and m['records']==234564,'full80B index')
 need(sd['nonzero_duplicate_alias_occurrences']==m['nonzero_duplicate_alias_occurrences']==514,'all duplicate aliases')
 need(sd['all_occurrences_retained'] and sd['original_real_payload_read'] is False,'no dropped occurrence or pixels')
 need(old['table']['compiled_rows']==281 and old['table']['populated_rows']==224 and len(old['table']['rows'])==281,'R36 source table')
 need(set(m['album_joins'])=={'28001','28002','28003'},'bounded three aliases only')
 for n,name,slot,physical in EXPECTED:
  k=str(n);entry=m['album_joins'][k];p=entry['program']
  rows=[x for x in old['table']['rows'] if x['album_slot']==slot and x['table_face_value']==n and x['name_gbk']==name]
  need(len(rows)==1,'source table unique')
  need(p=={'name':name,'slot':slot,'face':n,'r36_table_row_sha256':rows[0]['record_sha256'],'r36_table_index':rows[0]['table_index']},'R36 immutable origin')
  a=sd['selected_logical_aliases'][k];b=sd['physical_same_number_counterexamples'][k]
  need(a==entry['adrn_alias_rows'] and b==entry['physical_same_number_counterexamples'],'same-source raw rows')
  need(len(a)==len(b)==1,'all selected occurrence counts')
  real,wrong=a[0],b[0]
  need(real['logical_alias']==n and real['bitmapno']==physical and real['index']==physical,'alias physical index')
  need(real['source_offset']==80*real['index'] and wrong['source_offset']==80*wrong['index'],'real source offset')
  need(wrong['bitmapno']==n and wrong['logical_alias']==0,'same-number is NOT alias')
  need(wrong['record_sha256']!=real['record_sha256'] and wrong['index']!=real['index'],'separate namespaces')
  for x in (real,wrong):
   need(len(x['record_sha256'])==len(x['attr_sha256'])==64 and x['size']>0 and x['width']>0 and x['height']>0,'record digests and dimensions')
 need(m['unproven']['overall_percent'] is None and m['unproven']['new_official_clients']==0,'no invented completion')
 need(m['unproven']['original_real_pixel_payload_read'] is False and m['unproven']['official_build_authenticated'] is False,'no inflated evidence')
 return {'alias_joins':3,'original_adrn_records':234564,'same_number_counterexamples':3,'source_attempts':2}
if __name__=='__main__':print(json.dumps(check(*read_all()),sort_keys=True))
